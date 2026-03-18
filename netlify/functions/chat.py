"""Netlify Serverless Function — Triple-Helix chat endpoint.

Route: POST /.netlify/functions/chat
Body:  {"message": "<user input>"}
Response: {"reply": "<assistant answer>", "meta": {…}}

triple_helix_engine.py is bundled alongside this file via the
`included_files` option in netlify.toml, so the import works without
any path manipulation.
"""

from __future__ import annotations

import json

from triple_helix_engine import generate_reply

_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
}


def handler(event: dict, context: object) -> dict:  # noqa: ARG001
    # Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 204, "headers": _CORS_HEADERS, "body": ""}

    if event.get("httpMethod") != "POST":
        return {
            "statusCode": 405,
            "headers": _CORS_HEADERS,
            "body": json.dumps({"error": "Method Not Allowed"}),
        }

    try:
        body = json.loads(event.get("body") or "{}")
        message = str(body.get("message", "")).strip()
        if not message:
            return {
                "statusCode": 400,
                "headers": {**_CORS_HEADERS, "Content-Type": "application/json"},
                "body": json.dumps({"error": "message field is required"}),
            }

        reply = generate_reply(message=message)
        return {
            "statusCode": 200,
            "headers": {**_CORS_HEADERS, "Content-Type": "application/json"},
            "body": json.dumps({"reply": reply.answer, "meta": reply.meta}),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "statusCode": 500,
            "headers": {**_CORS_HEADERS, "Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error", "detail": str(exc)}),
        }
