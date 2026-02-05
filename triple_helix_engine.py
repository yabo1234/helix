"""
Triple-Helix chatbot "engine".

This is intentionally lightweight and dependency-free so the UI can run anywhere.
You can later replace `generate_reply()` with calls to an LLM or your own pipeline.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

try:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()
    HAS_LLM_SUPPORT = True
except ImportError:
    HAS_LLM_SUPPORT = False


@dataclass(frozen=True)
class TripleHelixReply:
    answer: str
    meta: dict[str, Any]


def _triage_intent(message: str) -> str:
    m = message.lower().strip()
    if any(k in m for k in ("grant", "funding", "proposal", "call for", "rfp")):
        return "funding"
    if any(k in m for k in ("startup", "product", "go-to-market", "commercial", "pricing")):
        return "commercialization"
    if any(k in m for k in ("policy", "regulation", "law", "compliance", "public sector", "government")):
        return "policy"
    if any(k in m for k in ("research", "paper", "university", "lab", "prototype", "method")):
        return "research"
    if any(k in m for k in ("partnership", "mou", "consortium", "collaboration", "stakeholder")):
        return "partnership"
    return "general"


def _clarifying_questions(intent: str) -> list[str]:
    common = [
        "What country/region are you operating in?",
        "What is the target sector (e.g., health, energy, agri, fintech)?",
        "What stage are you at (idea, prototype, pilot, scale)?",
        "Who are the key stakeholders you already have (academia/industry/government)?",
    ]
    by_intent: dict[str, list[str]] = {
        "funding": [
            "What is your rough budget range and timeline?",
            "Is the lead applicant a university, company, or public agency?",
        ],
        "commercialization": [
            "Who is the buyer/user and what pain are you solving?",
            "Do you have IP to protect (patent, know-how, data)?",
        ],
        "policy": [
            "What policy objective are you aiming for (growth, jobs, resilience, inclusion)?",
            "Are there specific regulations or standards you must meet?",
        ],
        "research": [
            "What is the research question and what evidence would validate it?",
            "What datasets, equipment, or facilities do you need?",
        ],
        "partnership": [
            "What value does each helix bring (knowledge, market access, legitimacy)?",
            "How will decisions be made (steering group, PI-led, joint venture)?",
        ],
    }
    return (by_intent.get(intent, []) + common)[:5]


def _get_llm_client() -> OpenAI | None:
    """
    Get an OpenAI-compatible client for the configured LLM provider.
    Returns None if LLM support is not available or not configured.
    """
    if not HAS_LLM_SUPPORT:
        return None
    
    provider = os.environ.get("LLM_PROVIDER", "rule-based").lower()
    
    if provider == "deepseek":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            return None
        base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        return OpenAI(api_key=api_key, base_url=base_url)
    
    elif provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    
    return None


def _generate_llm_reply(message: str, history: list[dict[str, str]] | None = None) -> str | None:
    """
    Generate a reply using an LLM (DeepSeek, OpenAI, etc.).
    Returns None if LLM is not configured or fails.
    """
    client = _get_llm_client()
    if not client:
        return None
    
    provider = os.environ.get("LLM_PROVIDER", "rule-based").lower()
    
    # Select the appropriate model
    if provider == "deepseek":
        model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    elif provider == "openai":
        model = os.environ.get("OPENAI_MODEL", "gpt-4")
    else:
        return None
    
    # Build messages for the LLM
    system_prompt = """You are an expert consultant on the Triple-Helix innovation framework (Academia × Industry × Government).

Help users think through innovation challenges by analyzing the three perspectives:
1) Academia (knowledge): What research, insights, or technology is needed? What proof (data, prototype, publication) will de-risk it?
2) Industry (value): Who pays/uses it? What is the adoption path? What incentives/ROI exist?
3) Government (enabling): What policies, standards, procurement, or funding can accelerate adoption and reduce risk?

Provide practical, actionable guidance. Ask clarifying questions when needed. Keep responses helpful but concise."""
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history if available
    if history:
        for turn in history:
            role = turn.get("role", "user")
            content = turn.get("content", "")
            if role and content:
                messages.append({"role": role, "content": content})
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM error: {e}")
        return None


def generate_reply(message: str, history: list[dict[str, str]] | None = None) -> TripleHelixReply:
    """
    Produce a structured Triple-Helix style response.

    Parameters
    ----------
    message:
        The user's latest message.
    history:
        Optional chat history (UI may pass prior turns).
    """
    provider = os.environ.get("LLM_PROVIDER", "rule-based").lower()
    
    # Try LLM first if configured
    if provider in ("deepseek", "openai"):
        llm_answer = _generate_llm_reply(message, history)
        if llm_answer:
            meta = {
                "provider": provider,
                "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "history_turns": len(history or []),
            }
            return TripleHelixReply(answer=llm_answer, meta=meta)
    
    # Fall back to rule-based response
    intent = _triage_intent(message)
    questions = _clarifying_questions(intent)

    # Keep responses helpful but not overly long; the UI can iterate.
    answer = (
        "Here’s a Triple-Helix framing (Academia × Industry × Government):\n\n"
        "1) Academia (knowledge): What new insight/tech is needed, and what proof (data, prototype, publication) will de-risk it?\n"
        "2) Industry (value): Who pays/uses it, what is the adoption path, and what incentives/ROI exist?\n"
        "3) Government (enabling): What policies, standards, procurement, or funding can accelerate adoption and reduce risk?\n\n"
        "A practical next step is to define a joint pilot with clear roles, success metrics, and a governance model.\n\n"
        "To tailor this, answer:\n"
        + "\n".join(f"- {q}" for q in questions)
    )

    meta = {
        "provider": "rule-based",
        "intent": intent,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "history_turns": len(history or []),
    }
    return TripleHelixReply(answer=answer, meta=meta)

