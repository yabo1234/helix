from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import Depends, FastAPI, Request, Response
from pydantic import BaseModel, Field

from .auth import require_api_key
from .config import settings
from .logging_config import configure_logging
from .openai_client import OpenAIProvider
from .prompts import default_system_prompt
from .request_context import request_id_var


configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Helix (Triple Helix chatbot)", version="0.1.0")


@app.on_event("startup")
async def _startup() -> None:
    # Create the OpenAI client once for connection reuse on Cloud Run.
    app.state.openai_provider = OpenAIProvider()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="User message")
    system_prompt: str | None = Field(default=None, description="Override system prompt")
    context_documents: list[str] = Field(default_factory=list, description="Additional context strings")

    model: str | None = None
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_output_tokens: int | None = Field(default=None, ge=1, le=64_000)

    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    id: str
    created_at: datetime
    model: str
    response: str
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
        "access_mode": settings.access_mode,
    }


@app.post("/v1/chat", dependencies=[Depends(require_api_key)], response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request):
    provider: OpenAIProvider | None = getattr(request.app.state, "openai_provider", None)
    if provider is None:
        provider = OpenAIProvider()
        request.app.state.openai_provider = provider

    model = req.model or settings.model
    temperature = settings.temperature if req.temperature is None else req.temperature

    # For reproducibility/debugging, log shapes, not secrets.
    logger.info(
        "chat.request model=%s temperature=%s message_chars=%d docs=%d",
        model,
        temperature,
        len(req.message),
        len(req.context_documents),
    )
    if settings.log_request_body:
        logger.info("chat.request.body %s", req.model_dump_json())

    system_prompt = req.system_prompt or default_system_prompt(req.context_documents)

    result = await provider.generate(
        message=req.message,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_output_tokens=req.max_output_tokens,
        metadata=req.metadata or None,
    )

    return ChatResponse(
        id=str(uuid.uuid4()),
        created_at=datetime.now(tz=timezone.utc),
        model=result.model,
        response=result.text,
        usage=result.usage,
    )
