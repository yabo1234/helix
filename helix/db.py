from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from .config import settings


def _ensure_parent_dir(db_path: str) -> None:
    p = Path(db_path)
    if p.parent and str(p.parent) not in {"", "."}:
        p.parent.mkdir(parents=True, exist_ok=True)


def init_db() -> None:
    _ensure_parent_dir(settings.db_path)
    with connect() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
              uid TEXT PRIMARY KEY,
              email TEXT,
              name TEXT,
              created_at TEXT NOT NULL,
              last_seen_at TEXT NOT NULL,
              plan TEXT NOT NULL,
              trial_started_at TEXT,
              trial_ends_at TEXT
            )
            """
        )
        con.execute("CREATE INDEX IF NOT EXISTS idx_users_last_seen ON users(last_seen_at)")


@contextmanager
def connect():
    _ensure_parent_dir(settings.db_path)
    con = sqlite3.connect(settings.db_path, timeout=30)
    try:
        con.row_factory = sqlite3.Row
        yield con
        con.commit()
    finally:
        con.close()

