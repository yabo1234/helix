from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Literal

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from pydantic import BaseModel, Field

from .auth import AuthContext, require_auth
from .config import settings
from .db import init_db
from .logging_config import configure_logging
from .openai_client import OpenAIProvider
from .prompts import default_system_prompt
from .request_context import request_id_var


configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Helix (Triple Helix chatbot)", version="0.1.0")


@app.on_event("startup")
async def _startup() -> None:
    # Optional warm-up: only create the OpenAI client if configured.
    # This keeps the service startable for health checks and dry-run testing.
    if settings.openai_api_key and not settings.dry_run:
        try:
            app.state.openai_provider = OpenAIProvider()
        except Exception:
            logger.exception("startup.openai_provider_init_failed")
    # Initialize DB early for auth modes that use it.
    if settings.effective_auth_mode in {"firebase"}:
        try:
            init_db()
        except Exception:
            logger.exception("startup.db_init_failed")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="User message")
    messages: list["ChatMessage"] = Field(
        default_factory=list,
        description="Optional prior messages for multi-turn context (excluding the current `message`).",
    )
    system_prompt: str | None = Field(default=None, description="Override system prompt")
    context_documents: list[str] = Field(default_factory=list, description="Additional context strings")

    model: str | None = None
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_output_tokens: int | None = Field(default=None, ge=1, le=64_000)

    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1)


class ChatResponse(BaseModel):
    id: str
    created_at: datetime
    model: str
    response: str
    openai_response_id: str | None = None
    usage: dict[str, Any] | None = None


@app.middleware("http")
async def request_id_and_logging(request: Request, call_next):
    rid = request.headers.get("x-request-id") or str(uuid.uuid4())
    token = request_id_var.set(rid)

    start = time.time()
    try:
        if settings.log_requests:
            logger.info("request.start %s %s", request.method, request.url.path)
        resp: Response = await call_next(request)
        resp.headers["X-Request-ID"] = rid
        return resp
    finally:
        dur_ms = int((time.time() - start) * 1000)
        if settings.log_requests:
            logger.info("request.end %s %s %dms", request.method, request.url.path, dur_ms)
        request_id_var.reset(token)


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.get("/readyz")
async def readyz():
    # Readiness is mostly "do we have config to serve".
    # We avoid calling OpenAI here to keep Cloud Run startup fast and deterministic.
    return {
        "ok": True,
        "openai_api_key_configured": bool(settings.openai_api_key),
        "model": settings.model,
        "auth_mode": settings.effective_auth_mode,
        "trial_days": settings.trial_days,
    }


@app.get("/v1/me")
async def me(auth: AuthContext = Depends(require_auth)):
    if auth.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires user auth (HELIX_AUTH_MODE=firebase).",
        )
    return auth.user.to_public_dict()


def _enforce_trial(auth: AuthContext) -> None:
    if auth.mode != "firebase":
        return
    user = auth.user
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.trial_active:
        return
    raise HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail={
            "error": "trial_expired",
            "message": "Your free trial has ended. Please upgrade to continue.",
            "trial_ends_at": user.to_public_dict().get("trial_ends_at"),
        },
    )


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request, auth: AuthContext = Depends(require_auth)):
    model = req.model or settings.model
    temperature = settings.temperature if req.temperature is None else req.temperature

    # For reproducibility/debugging, log shapes, not secrets.
    logger.info(
        "chat.request model=%s temperature=%s message_chars=%d prior_messages=%d docs=%d",
        model,
        temperature,
        len(req.message),
        len(req.messages),
        len(req.context_documents),
    )
    if settings.log_request_body:
        logger.info("chat.request.body %s", req.model_dump_json())

    _enforce_trial(auth)

    if settings.dry_run:
        logger.info("chat.dry_run enabled=true")
        return ChatResponse(
            id=str(uuid.uuid4()),
            created_at=datetime.now(tz=timezone.utc),
            model=model,
            response=f"[dry_run] Received {len(req.message)} chars. Provide OPENAI_API_KEY to enable live calls.",
            openai_response_id=None,
            usage=None,
        )

    system_prompt = req.system_prompt or default_system_prompt(req.context_documents)
    extra_system = "\n\n".join(m.content for m in req.messages if m.role == "system")
    if extra_system.strip():
        system_prompt = system_prompt + "\n\nAdditional system notes:\n" + extra_system.strip()

    input_messages: list[dict[str, str]] = [
        {"role": m.role, "content": m.content} for m in req.messages if m.role != "system"
    ]
    input_messages.append({"role": "user", "content": req.message})

    provider: OpenAIProvider | None = getattr(request.app.state, "openai_provider", None)
    if provider is None:
        provider = OpenAIProvider()
        request.app.state.openai_provider = provider

    rid = request_id_var.get()
    merged_metadata = dict(req.metadata or {})
    if rid and "request_id" not in merged_metadata:
        merged_metadata["request_id"] = rid
    if auth.user is not None and "user_id" not in merged_metadata:
        merged_metadata["user_id"] = auth.user.uid

    result = await provider.generate(
        input_messages=input_messages,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_output_tokens=req.max_output_tokens,
        metadata=merged_metadata or None,
    )

    return ChatResponse(
        id=str(uuid.uuid4()),
        created_at=datetime.now(tz=timezone.utc),
        model=result.model,
        response=result.text,
        openai_response_id=result.response_id,
        usage=result.usage,
    )
