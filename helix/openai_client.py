from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from .config import settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OpenAIResult:
    text: str
    model: str
    response_id: str | None = None
    raw: Any | None = None
    usage: dict[str, Any] | None = None


class OpenAIProvider:
    def __init__(self) -> None:
        try:
            from openai import AsyncOpenAI  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError(
                "Missing dependency 'openai'. Install requirements.txt before running."
            ) from e

        if not settings.openai_api_key:
            raise RuntimeError("Missing OPENAI_API_KEY")

        self._client = AsyncOpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    async def generate(
        self,
        *,
        input_text: str | None = None,
        input_messages: list[dict[str, str]] | None = None,
        system_prompt: str,
        model: str,
        temperature: float,
        max_output_tokens: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> OpenAIResult:
        """Calls the OpenAI Responses API when available, with a safe fallback."""
        if (input_text is None) == (input_messages is None):
            raise ValueError("Provide exactly one of input_text or input_messages")

        normalized_input: Any
        if input_messages is not None:
            # Responses API supports structured multi-turn inputs (role + content).
            # Keep it as simple strings for broad SDK compatibility.
            normalized_input = [{"role": m.get("role", "user"), "content": (m.get("content") or "")} for m in input_messages]
        else:
            normalized_input = input_text or ""

        payload: dict[str, Any] = {
            "model": model,
            "instructions": system_prompt,
            "input": normalized_input,
            "temperature": temperature,
        }
        if max_output_tokens is not None:
            payload["max_output_tokens"] = max_output_tokens
        if metadata:
            payload["metadata"] = metadata

        # Preferred: Responses API
        if hasattr(self._client, "responses"):
            resp = await self._client.responses.create(**payload)
            response_id = getattr(resp, "id", None)
            text = getattr(resp, "output_text", None)
            if not text:
                # Fallback extraction
                try:
                    text = "".join(
                        c.text
                        for o in (resp.output or [])
                        for c in getattr(o, "content", [])
                        if getattr(c, "type", None) in {"output_text", "text"} and getattr(c, "text", None)
                    )
                except Exception:
                    text = ""

            usage_obj = getattr(resp, "usage", None)
            usage = None
            if usage_obj is not None:
                try:
                    usage = {
                        "input_tokens": getattr(usage_obj, "input_tokens", None),
                        "output_tokens": getattr(usage_obj, "output_tokens", None),
                        "total_tokens": getattr(usage_obj, "total_tokens", None),
                    }
                except Exception:
                    usage = None

            return OpenAIResult(
                text=(text or "").strip() or "(No response.)",
                model=model,
                response_id=response_id,
                raw=resp,
                usage=usage,
            )

        # Older SDK fallback: Chat Completions
        if hasattr(self._client, "chat"):
            user_text = normalized_input if isinstance(normalized_input, str) else ""
            chat_messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
            if isinstance(normalized_input, list):
                chat_messages.extend(normalized_input)
            else:
                chat_messages.append({"role": "user", "content": user_text})

            cc = await self._client.chat.completions.create(
                model=model,
                messages=chat_messages,
                temperature=temperature,
            )
            text = (cc.choices[0].message.content or "").strip() or "(No response.)"
            return OpenAIResult(
                text=text,
                model=model,
                response_id=getattr(cc, "id", None),
                raw=cc,
                usage=getattr(cc, "usage", None),
            )

        logger.error("OpenAI SDK missing both responses and chat APIs")
        raise RuntimeError("OpenAI SDK is not compatible with this service")
