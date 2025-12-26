from __future__ import annotations

import os
from pathlib import Path
import time
import uuid
from typing import Any, Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


Role = Literal["system", "user", "assistant"]


class ChatMessage(BaseModel):
    role: Role
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(min_length=1)
    session_id: Optional[str] = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    messages: List[ChatMessage]
    provider: Literal["openai", "local"]


SYSTEM_PROMPT = """You are a Triple-Helix Innovation Chatbot.

Your job is to help design practical innovation strategies using the Triple Helix model:
- University: research, skills, labs, evidence, curriculum, talent pipelines.
- Industry: productization, market fit, operations, scaling, commercialization.
- Government: policy, regulation, funding, infrastructure, public value, procurement.

When responding:
- Ask clarifying questions if needed, but still provide a usable first draft plan.
- Structure outputs as: (1) problem framing, (2) stakeholder roles, (3) actions (0-30/30-90/90+ days),
  (4) risks + mitigations, (5) metrics/KPIs, (6) next questions.
- Keep it concise, concrete, and implementation-oriented.
"""


def _local_reply(user_text: str) -> str:
    # A deterministic fallback so the API works without external credentials.
    return (
        "### Triple-Helix draft response\n\n"
        "**1) Problem framing**\n"
        f"- {user_text.strip()}\n\n"
        "**2) Stakeholder roles**\n"
        "- **University**: research baseline, talent pipeline, pilots in labs.\n"
        "- **Industry**: define use-cases, validate customers, operationalize pilots.\n"
        "- **Government**: enabling policy, co-funding, procurement pathways.\n\n"
        "**3) Actions**\n"
        "- **0–30 days**: agree problem statement; map stakeholders; pick 1 pilot; define KPIs.\n"
        "- **30–90 days**: run pilot; iterate; secure co-funding; prepare compliance plan.\n"
        "- **90+ days**: scale to 3–5 sites/clients; formalize partnerships; publish outcomes.\n\n"
        "**4) Risks + mitigations**\n"
        "- Misaligned incentives → shared governance + clear IP/data terms.\n"
        "- Pilot doesn’t translate → parallel customer discovery + stage-gates.\n"
        "- Policy friction → early regulator engagement + sandbox approach.\n\n"
        "**5) Metrics/KPIs**\n"
        "- Pilot success rate, time-to-deploy, cost reduction or revenue uplift, adoption, compliance milestones.\n\n"
        "**6) Next questions**\n"
        "- What sector and geography? Who are the named partner orgs? What budget/timeline constraints?\n"
    )


async def _openai_reply(messages: List[Dict[str, str]], temperature: float) -> str:
    """
    Uses OpenAI if OPENAI_API_KEY is set. Otherwise raises RuntimeError.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    try:
        from openai import AsyncOpenAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"OpenAI SDK not available: {e}") from e

    client = AsyncOpenAI(api_key=api_key)
    resp = await client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
    )
    return resp.choices[0].message.content or ""


app = FastAPI(title="Triple-Helix Chatbot API", version="0.1.0")

# Serve a tiny web UI from /static
_ROOT = Path(__file__).resolve().parent
_STATIC_DIR = _ROOT / "static"
if _STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

# Allow browser-based clients by default (can be tightened via env later).
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory session store (best-effort; not durable).
_SESSIONS: Dict[str, List[ChatMessage]] = {}


@app.get("/")
def index() -> FileResponse:
    index_file = _STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="UI not found. Missing static/index.html")
    return FileResponse(index_file)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "time": int(time.time())}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    session_id = req.session_id or str(uuid.uuid4())

    # Merge any existing session messages with new ones.
    prior = _SESSIONS.get(session_id, [])
    merged: List[ChatMessage] = []
    merged.extend(prior)
    merged.extend(req.messages)

    # Ensure system prompt is present as the first message.
    if not merged or merged[0].role != "system":
        merged = [ChatMessage(role="system", content=SYSTEM_PROMPT), *merged]

    # Convert to provider format.
    provider_messages = [{"role": m.role, "content": m.content} for m in merged]

    try:
        reply = await _openai_reply(provider_messages, temperature=req.temperature)
        provider: Literal["openai", "local"] = "openai"
    except Exception:
        # Fall back to local deterministic response using the latest user message.
        last_user = next((m.content for m in reversed(merged) if m.role == "user"), "")
        if not last_user:
            raise HTTPException(status_code=400, detail="No user message found in request")
        reply = _local_reply(last_user)
        provider = "local"

    assistant_msg = ChatMessage(role="assistant", content=reply)
    updated = [*merged, assistant_msg]

    # Persist back to session store (bounded to last N messages).
    max_msgs = int(os.getenv("SESSION_MAX_MESSAGES", "50"))
    _SESSIONS[session_id] = updated[-max_msgs:]

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        messages=updated,
        provider=provider,
    )

