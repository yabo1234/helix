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

    # Access control
    access_mode: str = os.getenv("HELIX_ACCESS_MODE", "public").lower()  # public|private
    api_key: str = os.getenv("HELIX_API_KEY", "").strip()


settings = Settings()
