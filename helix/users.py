from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from .config import settings
from .db import connect, init_db


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_iso(v: str | None) -> datetime | None:
    if not v:
        return None
    s = v.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


@dataclass(frozen=True)
class UserRecord:
    uid: str
    email: str | None
    name: str | None
    created_at: datetime
    last_seen_at: datetime
    plan: str
    trial_started_at: datetime | None
    trial_ends_at: datetime | None

    @property
    def trial_active(self) -> bool:
        if self.plan in {"paid", "admin"}:
            return True
        if not self.trial_ends_at:
            return False
        return _utc_now() <= self.trial_ends_at

    @property
    def trial_seconds_remaining(self) -> int | None:
        if not self.trial_ends_at:
            return None
        return max(0, int((self.trial_ends_at - _utc_now()).total_seconds()))

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "uid": self.uid,
            "email": self.email,
            "name": self.name,
            "plan": self.plan,
            "trial_started_at": _iso(self.trial_started_at),
            "trial_ends_at": _iso(self.trial_ends_at),
            "trial_active": self.trial_active,
            "trial_seconds_remaining": self.trial_seconds_remaining,
            "created_at": _iso(self.created_at),
            "last_seen_at": _iso(self.last_seen_at),
        }


def get_or_create_user(*, uid: str, email: str | None, name: str | None) -> UserRecord:
    init_db()
    now = _utc_now()
    trial_days = max(0, int(settings.trial_days))

    with connect() as con:
        row = con.execute("SELECT * FROM users WHERE uid = ?", (uid,)).fetchone()
        if row is None:
            trial_started = now if trial_days > 0 else None
            trial_ends = (now + timedelta(days=trial_days)) if trial_days > 0 else None
            con.execute(
                """
                INSERT INTO users(uid, email, name, created_at, last_seen_at, plan, trial_started_at, trial_ends_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    uid,
                    email,
                    name,
                    _iso(now),
                    _iso(now),
                    "trial" if trial_days > 0 else "free",
                    _iso(trial_started),
                    _iso(trial_ends),
                ),
            )
            row = con.execute("SELECT * FROM users WHERE uid = ?", (uid,)).fetchone()
        else:
            con.execute(
                "UPDATE users SET email = COALESCE(?, email), name = COALESCE(?, name), last_seen_at = ? WHERE uid = ?",
                (email, name, _iso(now), uid),
            )
            row = con.execute("SELECT * FROM users WHERE uid = ?", (uid,)).fetchone()

    assert row is not None
    return _row_to_user(row)


def _row_to_user(row) -> UserRecord:
    return UserRecord(
        uid=row["uid"],
        email=row["email"],
        name=row["name"],
        created_at=_parse_iso(row["created_at"]) or _utc_now(),
        last_seen_at=_parse_iso(row["last_seen_at"]) or _utc_now(),
        plan=row["plan"],
        trial_started_at=_parse_iso(row["trial_started_at"]),
        trial_ends_at=_parse_iso(row["trial_ends_at"]),
    )

