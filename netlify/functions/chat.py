"""
Netlify serverless function – /api/chat

Receives a POST request with JSON body:
    { "message": "...", "history": [ {"role": "...", "content": "..."}, ... ] }

Returns:
    { "answer": "...", "intent": "...", "generated_at_utc": "..." }

The function imports triple_helix_engine from the repo root by temporarily
adding the repo root to sys.path so Netlify can resolve it.
"""

from __future__ import annotations

import json
import os
import sys

# ---------------------------------------------------------------------------
# Make the repo root importable so triple_helix_engine is found regardless
# of where Netlify executes the function.
# ---------------------------------------------------------------------------
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from triple_helix_engine import generate_reply  # noqa: E402


_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Content-Type": "application/json",
}


def handler(event: dict, context: object) -> dict:
    """AWS-Lambda-compatible handler used by Netlify Functions."""

    # Handle CORS pre-flight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 204, "headers": _CORS_HEADERS, "body": ""}

    if event.get("httpMethod") != "POST":
        return {
            "statusCode": 405,
            "headers": _CORS_HEADERS,
            "body": json.dumps({"error": "Method not allowed. Use POST."}),
        }

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": _CORS_HEADERS,
            "body": json.dumps({"error": "Invalid JSON body."}),
        }

    message: str = body.get("message", "").strip()
    if not message:
        return {
            "statusCode": 400,
            "headers": _CORS_HEADERS,
            "body": json.dumps({"error": "Field 'message' is required."}),
        }

    history: list[dict[str, str]] = body.get("history", [])

    reply = generate_reply(message=message, history=history)

    response_body = {
        "answer": reply.answer,
        **reply.meta,
    }

    return {
        "statusCode": 200,
        "headers": _CORS_HEADERS,
        "body": json.dumps(response_body),
    }
