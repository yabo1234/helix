"""
Triple Helix Innovation Agent
============================

This module provides a small, dependency-free implementation of a "Triple Helix"
innovation workflow (University ↔ Industry ↔ Government). It is designed to be
used as an entrypoint for an agent/tool runner and therefore exposes a single
public function: `run_agent`.

The code intentionally avoids external dependencies so it can run in minimal
execution environments.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union


# ----------------------------
# Data model
# ----------------------------


@dataclass(frozen=True)
class Actor:
    name: str
    capabilities: Tuple[str, ...]
    incentives: Tuple[str, ...]
    constraints: Tuple[str, ...]


@dataclass(frozen=True)
class Initiative:
    title: str
    problem: str
    approach: str
    roles: Dict[str, Tuple[str, ...]]  # keys: university/industry/government
    milestones_90d: Tuple[str, ...]
    success_metrics: Tuple[str, ...]
    risks: Tuple[str, ...]
    mitigations: Tuple[str, ...]


# ----------------------------
# Core logic
# ----------------------------


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _as_tuple(values: Optional[Iterable[str]]) -> Tuple[str, ...]:
    if not values:
        return tuple()
    out: List[str] = []
    for v in values:
        if v is None:
            continue
        s = str(v).strip()
        if s:
            out.append(s)
    return tuple(out)


def _first_nonempty(*values: Optional[str], default: str) -> str:
    for v in values:
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return default


def _normalize_payload(payload: Any) -> Dict[str, Any]:
    """
    Accept common payload shapes:
    - dict-like (Mapping)
    - JSON string
    - raw text (treated as "prompt")
    """
    if payload is None:
        return {}
    if isinstance(payload, Mapping):
        return dict(payload)
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        s = payload.strip()
        if not s:
            return {}
        try:
            obj = json.loads(s)
        except Exception:
            return {"prompt": s}
        if isinstance(obj, Mapping):
            return dict(obj)
        return {"input": obj}
    # Fallback: wrap anything else
    return {"input": payload}


def _derive_focus_areas(
    sectors: Sequence[str],
    goals: Sequence[str],
    prompt: str,
) -> Tuple[str, ...]:
    """
    Pick a few focus areas to drive initiative generation.
    """
    candidates: List[str] = []
    for s in sectors:
        ss = str(s).strip()
        if ss:
            candidates.append(ss)
    for g in goals:
        gg = str(g).strip()
        if gg and gg.lower() not in (c.lower() for c in candidates):
            candidates.append(gg)

    if not candidates and prompt:
        # Very lightweight extraction: take up to 3 comma/line separated chunks.
        rough = []
        for part in prompt.replace("\n", ",").split(","):
            p = part.strip()
            if p:
                rough.append(p)
        candidates = rough[:3]

    if not candidates:
        candidates = [
            "applied AI for public services",
            "supply chain resilience",
            "workforce upskilling",
        ]

    return tuple(candidates[:4])


def _default_actors(region: str) -> Dict[str, Actor]:
    region = region.strip()
    return {
        "university": Actor(
            name=_first_nonempty(region and f"{region} research university consortium", default="university consortium"),
            capabilities=(
                "research & evaluation",
                "talent pipeline (students, postdocs)",
                "labs and prototyping",
                "training and curriculum design",
            ),
            incentives=("publish & translate research", "funding", "student outcomes"),
            constraints=("academic timelines", "IP policy complexity", "limited deployment capacity"),
        ),
        "industry": Actor(
            name=_first_nonempty(region and f"{region} industry partners", default="industry partners"),
            capabilities=("product engineering", "go-to-market", "operations & scaling", "customer access"),
            incentives=("revenue", "cost reduction", "competitive advantage"),
            constraints=("quarterly delivery pressure", "risk management", "legacy systems"),
        ),
        "government": Actor(
            name=_first_nonempty(region and f"{region} government agencies", default="government agencies"),
            capabilities=("regulation & procurement", "public datasets", "policy levers", "convening power"),
            incentives=("public value", "equity & compliance", "economic development"),
            constraints=("procurement cycles", "legal constraints", "political risk"),
        ),
    }


def generate_initiatives(
    *,
    focus_areas: Sequence[str],
    horizon: str,
    region: str,
    constraints: Sequence[str],
    actors: Optional[Mapping[str, Actor]] = None,
) -> Tuple[Initiative, ...]:
    """
    Deterministically generate 2–4 initiatives using a simple template.
    """
    actors_map = dict(actors) if actors else _default_actors(region)
    horizon = _first_nonempty(horizon, default="12 months")
    region = region.strip() or "the region"
    extra_constraints = _as_tuple(constraints)

    initiatives: List[Initiative] = []
    for area in list(focus_areas)[:4]:
        area_s = str(area).strip()
        if not area_s:
            continue

        title = f"{area_s.title()} Testbed & Deployment Sprint"
        problem = (
            f"{region} needs faster translation of research into deployable solutions in {area_s}, "
            f"while balancing public value, commercial viability, and compliance."
        )
        approach = (
            "Stand up a joint testbed: define a reference architecture, establish data-sharing and IP terms, "
            "run 2 pilot deployments, and publish an evaluation playbook for repeatable scaling."
        )
        if extra_constraints:
            approach += " Constraints to honor: " + "; ".join(extra_constraints) + "."

        roles = {
            "university": (
                "define evaluation protocol and baseline",
                "provide prototyping support and talent placements",
                "independent impact assessment",
            ),
            "industry": (
                "build production-grade MVPs",
                "own integration, security hardening, and operations",
                "commercialization plan and customer success",
            ),
            "government": (
                "provide problem statements and procurement pathway",
                "enable access to data and deployment environments",
                "define compliance and equity requirements",
            ),
        }

        milestones_90d = (
            "Agree on governance, IP, and data-sharing terms (1–2 weeks)",
            "Select two pilot use-cases and define measurable outcomes (2–3 weeks)",
            "Deliver MVPs into a controlled test environment (6–8 weeks)",
            "Run evaluation and publish a scale/no-scale decision memo (by day 90)",
        )
        success_metrics = (
            "Time-to-pilot (weeks)",
            "Outcome lift vs. baseline (domain KPI)",
            "Compliance pass rate (security/privacy/accessibility)",
            "Adoption/usage in pilot cohorts",
        )
        risks = (
            "Misaligned incentives across partners",
            "Data access delays or poor data quality",
            "Procurement/legal bottlenecks",
            "Pilot success that fails to scale operationally",
        )
        mitigations = (
            "Single charter with decision rights and escalation path",
            "Data readiness checklist and synthetic data fallback",
            "Early legal review; pre-approved contracting vehicles where possible",
            "Operational owner named in industry; SRE/ops readiness gate before expansion",
        )

        initiatives.append(
            Initiative(
                title=title,
                problem=problem,
                approach=approach,
                roles={k: _as_tuple(v) for k, v in roles.items()},
                milestones_90d=_as_tuple(milestones_90d),
                success_metrics=_as_tuple(success_metrics),
                risks=_as_tuple(risks),
                mitigations=_as_tuple(mitigations),
            )
        )

    # Cap at 3 to keep output readable in tool UIs.
    return tuple(initiatives[:3])


def build_triple_helix_plan(payload: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Main planning function. Produces a structured plan plus a markdown summary.
    """
    prompt = _first_nonempty(payload.get("prompt"), payload.get("text"), default="")

    goals = _as_tuple(payload.get("goals") or payload.get("goal"))
    constraints = _as_tuple(payload.get("constraints") or payload.get("constraint"))
    sectors = _as_tuple(payload.get("sectors") or payload.get("sector") or payload.get("domains"))
    region = _first_nonempty(payload.get("region"), payload.get("location"), default="")
    horizon = _first_nonempty(payload.get("horizon"), payload.get("timeline"), default="12 months")

    focus_areas = _derive_focus_areas(sectors=sectors, goals=goals, prompt=prompt)
    actors = _default_actors(region)
    initiatives = generate_initiatives(
        focus_areas=focus_areas,
        horizon=horizon,
        region=region,
        constraints=constraints,
        actors=actors,
    )

    result: Dict[str, Any] = {
        "meta": {
            "generated_at": _now_utc_iso(),
            "horizon": horizon,
            "region": region or None,
        },
        "inputs": {
            "prompt": prompt or None,
            "goals": list(goals),
            "constraints": list(constraints),
            "sectors": list(sectors),
            "focus_areas": list(focus_areas),
        },
        "actors": {k: asdict(v) for k, v in actors.items()},
        "initiatives": [asdict(i) for i in initiatives],
    }

    md_lines: List[str] = []
    md_lines.append("## Triple Helix Innovation Plan")
    md_lines.append("")
    md_lines.append(f"- **Region**: {region or '—'}")
    md_lines.append(f"- **Horizon**: {horizon}")
    if goals:
        md_lines.append(f"- **Goals**: {', '.join(goals)}")
    if constraints:
        md_lines.append(f"- **Constraints**: {', '.join(constraints)}")
    if focus_areas:
        md_lines.append(f"- **Focus areas**: {', '.join(focus_areas)}")
    md_lines.append("")

    for idx, init in enumerate(initiatives, start=1):
        md_lines.append(f"### Initiative {idx}: {init.title}")
        md_lines.append("")
        md_lines.append(f"**Problem**: {init.problem}")
        md_lines.append("")
        md_lines.append(f"**Approach**: {init.approach}")
        md_lines.append("")
        md_lines.append("**Roles**:")
        md_lines.append(f"- University: {', '.join(init.roles.get('university', ())) or '—'}")
        md_lines.append(f"- Industry: {', '.join(init.roles.get('industry', ())) or '—'}")
        md_lines.append(f"- Government: {', '.join(init.roles.get('government', ())) or '—'}")
        md_lines.append("")
        md_lines.append("**90-day milestones**:")
        for m in init.milestones_90d:
            md_lines.append(f"- {m}")
        md_lines.append("")
        md_lines.append("**Success metrics**:")
        for m in init.success_metrics:
            md_lines.append(f"- {m}")
        md_lines.append("")
        md_lines.append("**Risks & mitigations**:")
        for r, m in zip(init.risks, init.mitigations):
            md_lines.append(f"- {r} → {m}")
        md_lines.append("")

    result["markdown"] = "\n".join(md_lines).rstrip() + "\n"
    return result


# ----------------------------
# Agent entrypoint
# ----------------------------


def run_agent(payload: Any = None, **kwargs: Any) -> Dict[str, Any]:
    """
    Tool/agent entrypoint.

    Accepts either:
    - a dict-like payload, or
    - a JSON string, or
    - None (reads stdin as JSON/text if available).

    Returns a dict suitable for tool UIs.
    """
    if payload is None and kwargs:
        payload = dict(kwargs)

    if payload is None:
        # Best-effort stdin read. If there's nothing, default to empty payload.
        try:
            stdin_text = sys.stdin.read()
        except Exception:
            stdin_text = ""
        payload = stdin_text.strip() if stdin_text else None

    normalized = _normalize_payload(payload)
    plan = build_triple_helix_plan(normalized)
    # Provide a stable top-level "output" key for tool runners that expect it.
    return {"output": plan}


def _main(argv: Sequence[str]) -> int:
    """
    CLI wrapper for local testing:
      python triple_helix_innovation.py '{"region":"X","sectors":["health"],"goals":["reduce wait times"]}'
    Or:
      echo '{"prompt":"..."}' | python triple_helix_innovation.py
    """
    payload: Any = None
    if len(argv) > 1:
        payload = argv[1]
    out = run_agent(payload)
    sys.stdout.write(json.dumps(out, indent=2, sort_keys=True))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))

