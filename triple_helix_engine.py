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
    if any(k in m for k in ("video ad", "video advertisement", "video commercial", "ad script",
                             "advertisement script", "marketing video", "promo video", "promotional video")):
        return "marketing"
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
        "marketing": [
            "What is the primary target audience (age range, income level, location)?",
            "What unique selling points distinguish this business from competitors?",
            "What is the desired tone (luxury, affordable, family-friendly, adventurous)?",
            "What call-to-action should the ad end with (visit showroom, call now, visit website)?",
            "What is the preferred video length (15 s, 30 s, 60 s)?",
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

    if intent == "marketing":
        answer = (
            "Here is a ready-to-use video-ad prompt for **JF MOTORES** in Finfinne city:\n\n"
            "---\n"
            "**[SCENE 1 – 0:00–0:05]**\n"
            "Aerial drone shot of Finfinne (Addis Ababa) city skyline at golden hour.\n"
            "Voiceover (confident, warm): *\"Finfinne – a city that never stops moving.\"*\n\n"
            "**[SCENE 2 – 0:05–0:15]**\n"
            "Close-up of a gleaming car rolling off the JF MOTORES showroom forecourt.\n"
            "Cut to smiling customers shaking hands with a salesperson inside a bright, modern showroom.\n"
            "Voiceover: *\"At JF MOTORES, we bring you quality vehicles and trusted service – right here in your city.\"*\n\n"
            "**[SCENE 3 – 0:15–0:22]**\n"
            "Quick montage of different car models (sedan, SUV, pickup) with price tags or finance badges.\n"
            "Text on screen: **\"Wide selection. Competitive prices. Flexible financing.\"**\n\n"
            "**[SCENE 4 – 0:22–0:28]**\n"
            "Happy family loading luggage into their new car; thumbs-up from the driver.\n"
            "Voiceover: *\"Your dream car is closer than you think.\"*\n\n"
            "**[SCENE 5 – 0:28–0:30]**\n"
            "JF MOTORES logo appears on a clean white background.\n"
            "Text: **\"JF MOTORES – Finfinne's Trusted Car Dealer\"**\n"
            "Call-to-action: *\"Visit us today | 📍 [Fill in: Showroom Address] | 📞 [Fill in: Phone Number]\"*\n"
            "---\n\n"
            "> ℹ️ Replace the bracketed placeholders above with JF MOTORES' actual address and phone number before use.\n\n"
            "To further customise this script, answer:\n"
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

