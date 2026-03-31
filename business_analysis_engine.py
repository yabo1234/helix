"""
Business Analysis Agent "engine".

Dependency-free so the UI can run anywhere.
Replace `generate_reply()` with calls to an LLM or your own pipeline when ready.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class BusinessAnalysisReply:
    answer: str
    meta: dict[str, Any]


# ---------------------------------------------------------------------------
# Intent detection
# ---------------------------------------------------------------------------

def _is_whole_word_match(word: str, text: str) -> bool:
    """Return True if *word* appears as a whole word (or phrase) in *text*."""
    return bool(re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text))


def _triage_intent(message: str) -> str:
    m = message.lower().strip()
    if any(k in m for k in ("swot", "strength", "weakness", "opportunity", "threat")):
        return "swot"
    if any(k in m for k in ("pestle", "pestel", "political", "economic", "social", "technological", "legal", "environmental")):
        return "pestle"
    if any(k in m for k in ("porter", "five forces", "competitive", "rivalry", "supplier", "buyer", "entrant", "substitute")):
        return "porters_five_forces"
    if any(k in m for k in ("business model", "canvas", "value proposition", "revenue", "cost structure", "channel")):
        return "business_model"
    # Use whole-word matching for short acronyms to avoid false positives (e.g. "som" in "some")
    if (
        any(k in m for k in ("market", "segment", "target audience", "sizing"))
        or any(_is_whole_word_match(k, m) for k in ("tam", "sam", "som"))
    ):
        return "market_analysis"
    if any(k in m for k in ("financial", "profit", "margin", "cash flow", "break-even", "roi", "valuation")):
        return "financial"
    if any(k in m for k in ("risk", "mitigation", "contingency", "scenario", "uncertainty")):
        return "risk"
    if any(k in m for k in ("strategy", "roadmap", "plan", "goal", "objective", "kpi", "okr")):
        return "strategy"
    return "general"


# ---------------------------------------------------------------------------
# Framework summaries
# ---------------------------------------------------------------------------

_FRAMEWORK_INTROS: dict[str, str] = {
    "swot": (
        "**SWOT Analysis** maps internal *Strengths* and *Weaknesses* against external "
        "*Opportunities* and *Threats*. It is a fast, structured way to align your position "
        "with the environment before choosing a strategy."
    ),
    "pestle": (
        "**PESTLE Analysis** scans the macro-environment across six dimensions: "
        "*Political, Economic, Social, Technological, Legal,* and *Environmental*. "
        "Use it to surface forces outside your control that shape strategy."
    ),
    "porters_five_forces": (
        "**Porter's Five Forces** assesses industry attractiveness by examining: "
        "*Competitive Rivalry, Threat of New Entrants, Threat of Substitutes, "
        "Bargaining Power of Suppliers,* and *Bargaining Power of Buyers*."
    ),
    "business_model": (
        "The **Business Model Canvas** captures nine building blocks: "
        "*Customer Segments, Value Propositions, Channels, Customer Relationships, "
        "Revenue Streams, Key Resources, Key Activities, Key Partnerships,* and *Cost Structure*."
    ),
    "market_analysis": (
        "**Market Analysis** defines your addressable opportunity (TAM → SAM → SOM), "
        "identifies key segments, and validates that sufficient demand exists for your offer."
    ),
    "financial": (
        "**Financial Analysis** covers revenue modelling, margin analysis, cash-flow "
        "forecasting, break-even calculation, and valuation methods (DCF, comparables)."
    ),
    "risk": (
        "**Risk Analysis** identifies, scores (likelihood × impact), and prioritises "
        "risks, then designs mitigation or contingency responses for each."
    ),
    "strategy": (
        "**Strategic Planning** translates vision into actionable roadmaps through "
        "frameworks such as OKRs, Balanced Scorecard, or Hoshin Kanri."
    ),
    "general": (
        "**Business Analysis** applies structured frameworks—SWOT, PESTLE, Porter's "
        "Five Forces, Business Model Canvas, and more—to turn business questions into "
        "clear, evidence-based recommendations."
    ),
}


# ---------------------------------------------------------------------------
# Clarifying questions
# ---------------------------------------------------------------------------

def _clarifying_questions(intent: str) -> list[str]:
    common = [
        "What industry or sector does this concern?",
        "What is the size / stage of the business (startup, SME, enterprise)?",
        "What decision are you trying to inform with this analysis?",
        "Who is the primary audience for the output (investors, board, ops team)?",
    ]
    by_intent: dict[str, list[str]] = {
        "swot": [
            "What time horizon are you analysing (current state vs. 3-year outlook)?",
            "Which competitor or reference point should we benchmark against?",
        ],
        "pestle": [
            "Which geographies or markets are in scope?",
            "Are there specific macro-factors (e.g., regulation, energy costs) that concern you most?",
        ],
        "porters_five_forces": [
            "How concentrated is the supplier base for your key inputs?",
            "Are there low-cost or digital substitutes emerging in your space?",
        ],
        "business_model": [
            "What is the core value proposition you deliver to customers?",
            "What are your primary revenue streams (subscription, transactional, licensing)?",
        ],
        "market_analysis": [
            "What data sources do you have (surveys, industry reports, sales data)?",
            "What is your current market share or customer count?",
        ],
        "financial": [
            "What is the planning horizon (1-year budget, 3-year forecast, 5-year model)?",
            "What are the key cost drivers (COGS, headcount, infrastructure)?",
        ],
        "risk": [
            "What is your risk appetite (conservative, moderate, aggressive)?",
            "Have any risks already materialised that inform this assessment?",
        ],
        "strategy": [
            "What is the strategic objective you need to achieve in the next 12–18 months?",
            "What constraints exist (budget, talent, regulatory)?",
        ],
    }
    extras = by_intent.get(intent, [])
    return (extras + common)[:4]


_FRAMEWORK_NAMES: dict[str, str] = {
    "swot": "SWOT",
    "pestle": "PESTLE",
    "porters_five_forces": "Porter's Five Forces",
    "business_model": "Business Model Canvas",
    "market_analysis": "Market Analysis",
    "financial": "Financial Analysis",
    "risk": "Risk Analysis",
    "strategy": "Strategy & Roadmap",
    "general": "General Business Analysis",
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_reply(
    message: str,
    history: list[dict[str, str]] | None = None,
) -> BusinessAnalysisReply:
    """
    Produce a structured business-analysis response.

    Parameters
    ----------
    message:
        The user's latest message.
    history:
        Optional chat history (UI may pass prior turns).
    """
    intent = _triage_intent(message)
    questions = _clarifying_questions(intent)
    intro = _FRAMEWORK_INTROS[intent]

    answer = (
        f"{intro}\n\n"
        "**Recommended analytical steps:**\n"
        "1. **Frame the question** – Define the decision, scope, and success criteria.\n"
        "2. **Gather evidence** – Collect quantitative data (financials, market stats) "
        "and qualitative inputs (interviews, expert views).\n"
        "3. **Apply the framework** – Work through each dimension systematically, "
        "noting key findings and supporting evidence.\n"
        "4. **Synthesise insights** – Identify the two or three findings that most "
        "change the decision or action.\n"
        "5. **Recommend & act** – Translate insights into clear, prioritised actions "
        "with owners and timelines.\n\n"
        "**To sharpen this analysis, please answer:**\n"
        + "\n".join(f"- {q}" for q in questions)
    )

    meta = {
        "intent": intent,
        "framework": _FRAMEWORK_NAMES.get(intent, intent.replace("_", " ").title()),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "history_turns": len(history or []),
    }
    return BusinessAnalysisReply(answer=answer, meta=meta)
