"""
Triple-Helix chatbot engine (optimized).

Now supports Azure OpenAI, structured prompting, and clean extensibility.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from openai import AzureOpenAI

from prompt_history_logger import append_prompt_log
from triple_helix_prompt_program import (
    QUESTIONS_BY_INTENT,
    COMMON_QUESTIONS,
    build_answer,  # fallback
)

# -------------------------------------------------------------------
# Azure OpenAI Client
# -------------------------------------------------------------------

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-01"
)

MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g. "gpt-4o-mini"


# -------------------------------------------------------------------
# Reply Dataclass
# -------------------------------------------------------------------

@dataclass(frozen=True)
class TripleHelixReply:
    answer: str
    meta: dict[str, Any]


# -------------------------------------------------------------------
# Intent Triage
# -------------------------------------------------------------------

def _triage_intent(message: str) -> str:
    m = message.lower().strip()

    intent_map = {
        "funding": ("grant", "funding", "proposal", "call for", "rfp"),
        "commercialization": ("startup", "product", "go-to-market", "commercial", "pricing"),
        "policy": ("policy", "regulation", "law", "compliance", "public sector", "government"),
        "research": ("research", "paper", "university", "lab", "prototype", "method"),
        "partnership": ("partnership", "mou", "consortium", "collaboration", "stakeholder"),
    }

    for intent, keywords in intent_map.items():
        if any(k in m for k in keywords):
            return intent

    return "general"


# -------------------------------------------------------------------
# Clarifying Questions
# -------------------------------------------------------------------

def _clarifying_questions(intent: str) -> list[str]:
    return (QUESTIONS_BY_INTENT.get(intent, []) + COMMON_QUESTIONS)[:5]


# -------------------------------------------------------------------
# Azure OpenAI LLM Call
# -------------------------------------------------------------------

def _llm_generate(prompt: str) -> str:
    """
    Generate a Triple-Helix style answer using Azure OpenAI.
    Falls back to build_answer() if the LLM fails.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the Triple-Helix Innovation Assistant. "
                        "Your job is to analyze user questions using the "
                        "Academia–Industry–Government framework. "
                        "Be structured, concise, and actionable."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=350,
            temperature=0.2,
        )
        return response.choices[0].message.content

    except Exception as e:
        # Fallback to deterministic offline answer
        return f"(LLM unavailable, fallback used)\n\n{build_answer([prompt])}"


# -------------------------------------------------------------------
# Main Reply Generator
# -------------------------------------------------------------------

def generate_reply(message: str, history: list[dict[str, str]] | None = None) -> TripleHelixReply:
    """
    Produce a structured Triple-Helix style response.
    Now powered by Azure OpenAI with fallback.
    """

    intent = _triage_intent(message)
    questions = _clarifying_questions(intent)

    # Build structured prompt
    prompt = (
        f"User message:\n{message}\n\n"
        f"Detected intent: {intent}\n\n"
        "Clarifying questions:\n"
        + "\n".join(f"- {q}" for q in questions)
        + "\n\n"
        "Produce a structured Triple-Helix analysis."
    )

    # Generate answer via Azure OpenAI
    answer = _llm_generate(prompt)

    # Log interaction
    append_prompt_log(
        message=message,
        history=history,
        intent=intent,
        answer=answer,
    )

    # Metadata
    meta = {
        "intent": intent,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "history_turns": len(history or []),
        "model": MODEL,
    }

    return TripleHelixReply(answer=answer, meta=meta)

