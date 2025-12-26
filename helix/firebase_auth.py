from __future__ import annotations

import json
import logging
from functools import lru_cache
from typing import Any

from .config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _init_firebase() -> None:
    try:
        import firebase_admin  # type: ignore
        from firebase_admin import credentials  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "Missing dependency 'firebase-admin'. Install requirements.txt before running."
        ) from e

    # firebase_admin keeps global app state; avoid double-init.
    if firebase_admin._apps:  # type: ignore[attr-defined]
        return

    cred_obj = None
    if settings.firebase_credentials_json:
        try:
            data = json.loads(settings.firebase_credentials_json)
        except Exception as e:
            raise RuntimeError("HELIX_FIREBASE_CREDENTIALS_JSON is not valid JSON") from e
        cred_obj = credentials.Certificate(data)
    elif settings.firebase_credentials_file:
        cred_obj = credentials.Certificate(settings.firebase_credentials_file)
    else:
        # Fall back to Application Default Credentials (Cloud Run, GCE, etc).
        cred_obj = credentials.ApplicationDefault()

    opts: dict[str, Any] = {}
    if settings.firebase_project_id:
        opts["projectId"] = settings.firebase_project_id

    firebase_admin.initialize_app(cred_obj, options=opts or None)


def verify_id_token(id_token: str) -> dict[str, Any]:
    """
    Verify a Firebase Auth ID token.

    Returns decoded claims (includes 'uid').
    """
    _init_firebase()
    from firebase_admin import auth  # type: ignore

    decoded = auth.verify_id_token(id_token)
    if not isinstance(decoded, dict) or "uid" not in decoded:
        raise RuntimeError("Invalid Firebase token payload")
    return decoded

