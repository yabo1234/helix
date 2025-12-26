from __future__ import annotations

from fastapi import Header, HTTPException, status

from .config import settings


def require_api_key(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    if settings.access_mode != "private":
        return

    expected = settings.api_key
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HELIX_ACCESS_MODE=private but HELIX_API_KEY is not set",
        )

    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    if not token and x_api_key:
        token = x_api_key.strip()

    if not token or token != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
