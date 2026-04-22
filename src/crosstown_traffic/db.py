from __future__ import annotations

import os

import aiosqlite

DB_PATH = os.getenv("DB_PATH", "/data/presence.db")


async def init_db() -> None:
    """Create the events table if it does not exist."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                state     TEXT    NOT NULL CHECK(state IN ('home', 'away')),
                timestamp TEXT    NOT NULL
            )
            """
        )
        await db.commit()


async def record_event(state: str) -> None:
    """Append a presence-change event ('home' or 'away')."""

    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO events (state, timestamp) VALUES (?, ?)",
            (state, now),
        )
        await db.commit()


async def get_status() -> dict:
    """
    Return current presence status from the last event.

    Returns a dict with:
        home   bool | None  – currently home? None if no events recorded
        since  str  | None  – ISO-8601 timestamp of last state change
    """

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT state, timestamp FROM events ORDER BY id DESC LIMIT 1"
        ) as cursor:
            row = await cursor.fetchone()

    if row is None:
        return {"home": None, "since": None}

    return {
        "home": row["state"] == "home",
        "since": row["timestamp"],
    }
