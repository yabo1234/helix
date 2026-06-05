"""
Triple-Helix chatbot "engine".

This is intentionally lightweight and dependency-free so the UI can run anywhere.
You can later replace `generate_reply()` with calls to an LLM or your own pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from triple_helix_prompt_program import QUESTIONS_BY_INTENT, COMMON_QUESTIONS, build_answer


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
    return (QUESTIONS_BY_INTENT.get(intent, []) + COMMON_QUESTIONS)[:5]


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
    intent = _triage_intent(message)
    questions = _clarifying_questions(intent)
    answer = build_answer(questions)

    meta = {
        "intent": intent,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "history_turns": len(history or []),
    }
    return TripleHelixReply(answer=answer, meta=meta)
