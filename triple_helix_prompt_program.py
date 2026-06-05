"""
Prompt/program file for the Triple-Helix chatbot.

This module centralizes the chatbot's reusable prompt text and question templates
so the UI/engine logic can stay separate from the response content.
"""

from __future__ import annotations

BASE_FRAMEWORK_TEXT = (
    "Here’s a Triple-Helix framing (Academia × Industry × Government):\n\n"
    "1) Academia (knowledge): What new insight/tech is needed, and what proof (data, prototype, publication) will de-risk it?\n"
    "2) Industry (value): Who pays/uses it, what is the adoption path, and what incentives/ROI exist?\n"
    "3) Government (enabling): What policies, standards, procurement, or funding can accelerate adoption and reduce risk?\n\n"
    "A practical next step is to define a joint pilot with clear roles, success metrics, and a governance model.\n\n"
    "To tailor this, answer:\n"
)

COMMON_QUESTIONS = [
    "What country/region are you operating in?",
    "What is the target sector (e.g., health, energy, agri, fintech)?",
    "What stage are you at (idea, prototype, pilot, scale)?",
    "Who are the key stakeholders you already have (academia/industry/government)?",
]

QUESTIONS_BY_INTENT: dict[str, list[str]] = {
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


def build_answer(questions: list[str]) -> str:
    return BASE_FRAMEWORK_TEXT + "\n".join(f"- {q}" for q in questions)
