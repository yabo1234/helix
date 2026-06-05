from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_PATH = Path("prompt_history.jsonl")


def append_prompt_log(*, message: str, history: list[dict[str, Any]] | None, intent: str, answer: str) -> None:
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "message": message,
        "history": history or [],
        "intent": intent,
        "answer": answer,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
