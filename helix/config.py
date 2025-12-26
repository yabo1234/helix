from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "helix"

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format: str = os.getenv("LOG_FORMAT", "json").lower()  # json|text
    log_requests: bool = os.getenv("LOG_REQUESTS", "true").lower() in {"1", "true", "yes"}
    log_request_body: bool = os.getenv("LOG_REQUEST_BODY", "false").lower() in {"1", "true", "yes"}

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model: str = os.getenv("HELIX_MODEL", "gpt-5.2")
    temperature: float = float(os.getenv("HELIX_TEMPERATURE", "0.2"))
    dry_run: bool = os.getenv("HELIX_DRY_RUN", "false").lower() in {"1", "true", "yes"}

    # Access control (legacy)
    # - HELIX_ACCESS_MODE=public|private (private requires HELIX_API_KEY)
    # New preferred setting is HELIX_AUTH_MODE=public|api_key|firebase.
    access_mode: str = os.getenv("HELIX_ACCESS_MODE", "public").lower()
    api_key: str = os.getenv("HELIX_API_KEY", "").strip()

    # Auth (preferred)
    auth_mode: str = os.getenv("HELIX_AUTH_MODE", "").strip().lower()

    # Firebase auth (when HELIX_AUTH_MODE=firebase)
    firebase_project_id: str = os.getenv("HELIX_FIREBASE_PROJECT_ID", "").strip()
    firebase_credentials_file: str = os.getenv("HELIX_FIREBASE_CREDENTIALS_FILE", "").strip()
    firebase_credentials_json: str = os.getenv("HELIX_FIREBASE_CREDENTIALS_JSON", "").strip()

    # Trials / persistence (used for per-user auth modes like firebase)
    db_path: str = os.getenv("HELIX_DB_PATH", "helix.sqlite3").strip() or "helix.sqlite3"
    trial_days: int = int(os.getenv("HELIX_TRIAL_DAYS", "7"))

    @property
    def effective_auth_mode(self) -> str:
        """
        Resolves auth mode with backwards compatibility:
        - If HELIX_AUTH_MODE is set, use it.
        - Else use legacy HELIX_ACCESS_MODE: private -> api_key, public -> public.
        """
        if self.auth_mode:
            return self.auth_mode
        return "api_key" if self.access_mode == "private" else "public"


settings = Settings()
