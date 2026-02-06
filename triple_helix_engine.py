"""
Triple-Helix chatbot "engine".

This is intentionally lightweight and dependency-free so the UI can run anywhere.
You can later replace `generate_reply()` with calls to an LLM or your own pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


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
    # More specific check for evolution - require multiple signals or explicit terms
    evolution_keywords = ("evolution", "history", "origins", "development")
    phase_keywords = ("metaphor", "theory", "movement")
    if (any(k in m for k in evolution_keywords) or 
        (any(k in m for k in phase_keywords) and any(t in m for t in ("triple", "helix", "model", "concept")))):
        return "evolution"
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
        "evolution": [
            "Are you interested in the historical development or practical applications?",
            "Would you like to know about specific phases (metaphor, theory, or movement)?",
        ],
    }
    return (by_intent.get(intent, []) + common)[:5]


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

    # Special handling for evolution intent
    if intent == "evolution":
        answer = (
            "The Triple Helix model has evolved through three key phases:\n\n"
            "**1. Metaphor (1990s)**: Initially introduced by Henry Etzkowitz and Loet Leydesdorff as a descriptive analogy, "
            "borrowing from the DNA double helix to represent the intertwining of universities, industry, and government.\n\n"
            "**2. Theory (Late 1990s-2000s)**: Developed into a formal theoretical framework with concepts like institutional overlaps, "
            "hybrid organizations, trilateral networks, and the emergence of a 'knowledge space' where the three helices intersect.\n\n"
            "**3. Movement (2010s-Present)**: Transformed into a global movement and practical policy framework adopted by governments, "
            "universities, and industries worldwide. Now includes regional variations (Quadruple Helix with civil society, Quintuple Helix "
            "with natural environment) and applications to smart cities, sustainable development, and global challenges.\n\n"
            "**Key Insight**: Innovation emerges from the synergistic interaction of multiple institutional spheres, each taking on roles "
            "traditionally associated with others while maintaining their primary functions.\n\n"
            "For a comprehensive overview, see TRIPLE_HELIX_EVOLUTION.md in this repository.\n\n"
            "To explore further:\n"
            + "\n".join(f"- {q}" for q in questions)
        )
    else:
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
        "intent": intent,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "history_turns": len(history or []),
    }
    return TripleHelixReply(answer=answer, meta=meta)

