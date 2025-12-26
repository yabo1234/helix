from __future__ import annotations

from dataclasses import dataclass

from fastapi import Header, HTTPException, status

from .config import settings
from .firebase_auth import verify_id_token
from .users import UserRecord, get_or_create_user


@dataclass(frozen=True)
class AuthContext:
    mode: str
    user: UserRecord | None = None


def require_api_key(  # backwards compatible dependency
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    # Preserve original behavior for existing deployments.
    if settings.effective_auth_mode != "api_key":
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


def require_auth(
    authorization: str | None = Header(default=None),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> AuthContext:
    """
    Auth gate for all modes.

    - public: no auth
    - api_key: static API key (Authorization: Bearer ... or X-API-Key)
    - firebase: Firebase ID token (Authorization: Bearer <id_token>)
    """
    mode = settings.effective_auth_mode

    if mode == "public":
        return AuthContext(mode="public", user=None)

    if mode == "api_key":
        require_api_key(authorization=authorization, x_api_key=x_api_key)
        return AuthContext(mode="api_key", user=None)

    if mode == "firebase":
        if not authorization or not authorization.lower().startswith("bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")
        token = authorization.split(" ", 1)[1].strip()
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")

        try:
            decoded = verify_id_token(token)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Firebase token: {e}",
            ) from e

        uid = str(decoded.get("uid") or decoded.get("user_id") or "").strip()
        if not uid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token (missing uid)")

        email = decoded.get("email")
        name = decoded.get("name") or decoded.get("display_name")
        user = get_or_create_user(uid=uid, email=str(email) if email else None, name=str(name) if name else None)
        return AuthContext(mode="firebase", user=user)

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Invalid HELIX_AUTH_MODE: {mode}",
    )
