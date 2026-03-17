"""
Macroeconomics analysis bot "engine".

Lightweight, dependency-free engine that produces structured macroeconomics
analysis.  Replace `generate_reply()` with calls to an LLM/API when ready.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class MacroReply:
    answer: str
    meta: dict[str, Any]


def _triage_intent(message: str) -> str:
    m = message.lower().strip()
    if any(k in m for k in ("inflation", "cpi", "price level", "deflation", "stagflation")):
        return "inflation"
    if any(k in m for k in (
        "interest rate", "central bank", "fed", "monetary policy",
        "quantitative easing", "quantitative tightening", "qe", "qt",
    )):
        return "monetary_policy"
    # Check trade before fiscal so "current account deficit" maps to trade
    if any(k in m for k in ("trade", "export", "import", "current account", "balance of payments", "exchange rate", "forex")):
        return "trade"
    if any(k in m for k in ("fiscal", "government spending", "budget deficit", "budget surplus", "tax", "stimulus")):
        return "fiscal_policy"
    if any(k in m for k in ("gdp", "growth", "recession", "output gap", "business cycle", "expansion")):
        return "growth"
    if any(k in m for k in ("unemployment", "labour market", "labor market", "jobs", "wage", "employment")):
        return "labour_market"
    return "general"


def _clarifying_questions(intent: str) -> list[str]:
    common = [
        "Which country or region are you analysing?",
        "What time horizon matters most (short-run, medium-run, long-run)?",
        "What is the primary policy objective (price stability, growth, employment, sustainability)?",
        "Are there any structural factors (demographics, technology, institutions) that are especially relevant?",
    ]
    by_intent: dict[str, list[str]] = {
        "inflation": [
            "Is inflation driven more by demand-pull or cost-push factors?",
            "What are current inflation expectations (anchored or de-anchored)?",
        ],
        "monetary_policy": [
            "What is the current policy rate and where is it relative to the neutral rate?",
            "Is the central bank operating under an inflation-targeting, price-level, or average-inflation framework?",
        ],
        "fiscal_policy": [
            "What is the current debt-to-GDP ratio and how is it trending?",
            "Is fiscal space available, or are there sustainability constraints?",
        ],
        "growth": [
            "Is the slowdown/expansion demand-driven or supply-driven?",
            "What does the output gap look like, and how is total factor productivity trending?",
        ],
        "trade": [
            "Is the focus on the trade balance, capital flows, or exchange-rate dynamics?",
            "Are there tariff, sanction, or geopolitical factors distorting normal trade patterns?",
        ],
        "labour_market": [
            "Is unemployment structural, frictional, or cyclical in nature?",
            "How tight is the labour market, and what does wage growth imply for core inflation?",
        ],
    }
    return (by_intent.get(intent, []) + common)[:5]


_FRAMEWORK: dict[str, dict[str, str]] = {
    "inflation": {
        "demand_side": "Assess aggregate demand relative to potential output (output gap); check consumer spending, investment, and government expenditure.",
        "supply_side": "Examine supply-chain conditions, commodity prices, and productivity trends that shift the SRAS curve.",
        "expectations": "Anchored long-run inflation expectations are key for credibility; monitor break-even inflation rates and surveys.",
        "policy_response": "Central banks typically tighten policy to cool demand; supply-side inflation may require targeted fiscal intervention instead.",
    },
    "monetary_policy": {
        "transmission": "Rate changes work through credit, asset prices, exchange rates, and expectations; lags are typically 12–24 months.",
        "tools": "Policy rate is the primary lever; QE/QT and forward guidance are unconventional tools used at the effective lower bound.",
        "tradeoffs": "Tighter policy lowers inflation but risks slowing growth and raising unemployment — the classic sacrifice ratio.",
        "credibility": "A credible, independent central bank reduces the inflation-output tradeoff by anchoring expectations.",
    },
    "fiscal_policy": {
        "automatic_stabilisers": "Tax revenues and transfers automatically dampen cycles without legislative action.",
        "discretionary_policy": "Targeted spending or tax changes can boost demand; effectiveness depends on the multiplier and crowding-out.",
        "debt_dynamics": "Sustainable debt requires the primary balance to exceed (r − g) × debt/GDP over the long run.",
        "distributional": "Who bears the burden and who receives the benefit matters for both equity and the aggregate multiplier.",
    },
    "growth": {
        "demand_drivers": "Decompose GDP growth into consumption, investment, government spending, and net exports.",
        "supply_drivers": "Long-run growth is determined by labour, capital, and total factor productivity (Solow framework).",
        "cycle_position": "Identify whether the economy is in expansion, peak, contraction, or trough to calibrate the appropriate policy stance.",
        "structural_reforms": "Supply-side reforms (education, infrastructure, competition policy) raise potential GDP.",
    },
    "trade": {
        "comparative_advantage": "Countries benefit by specialising in goods with the lowest opportunity cost.",
        "exchange_rate": "Currency depreciation boosts competitiveness but raises import costs and inflationary pressure.",
        "current_account": "A persistent deficit may signal competitiveness issues or excess domestic spending.",
        "geopolitics": "Trade policy, sanctions, and friend-shoring are reshaping global supply chains in ways traditional models underweight.",
    },
    "labour_market": {
        "beveridge_curve": "The vacancy-unemployment relationship signals matching efficiency; an outward shift implies structural mismatch.",
        "phillips_curve": "Tight labour markets historically generate wage and price pressure, though the relationship has flattened.",
        "participation": "Changes in participation rates (demographics, discouraged workers) affect the headline unemployment figure.",
        "wage_dynamics": "Real wage growth relative to productivity determines labour's share of income and inflationary pressure.",
    },
    "general": {
        "aggregate_demand": "AD = C + I + G + (X − M); shifts in any component affect output and price level.",
        "aggregate_supply": "Short-run AS slopes upward; long-run AS is vertical at potential output.",
        "policy_mix": "The combination of monetary and fiscal policy determines the overall macroeconomic stance.",
        "global_linkages": "Open economies are connected through trade, capital flows, and global financial conditions.",
    },
}


def generate_reply(message: str, history: list[dict[str, str]] | None = None) -> MacroReply:
    """
    Produce a structured macroeconomics analysis response.

    Parameters
    ----------
    message:
        The user's latest message.
    history:
        Optional chat history (UI may pass prior turns).
    """
    intent = _triage_intent(message)
    questions = _clarifying_questions(intent)
    framework = _FRAMEWORK.get(intent, _FRAMEWORK["general"])

    framework_text = "\n".join(
        f"  • **{k.replace('_', ' ').title()}**: {v}" for k, v in framework.items()
    )

    answer = (
        f"Here is a macroeconomics framework for **{intent.replace('_', ' ').title()}**:\n\n"
        f"{framework_text}\n\n"
        "**Suggested next steps:**\n"
        "- Gather recent data (central bank releases, national statistics, IMF/World Bank reports).\n"
        "- Map the transmission channels most relevant to your context.\n"
        "- Identify the key policy tradeoffs and stakeholder interests.\n\n"
        "To sharpen the analysis, please answer:\n"
        + "\n".join(f"- {q}" for q in questions)
    )

    meta = {
        "intent": intent,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "history_turns": len(history or []),
    }
    return MacroReply(answer=answer, meta=meta)
