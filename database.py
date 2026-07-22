"""SQLite persistence layer for LearnWithPython (stdlib only, no ORM)."""

import os
import sqlite3
from contextlib import contextmanager
from datetime import date

DB_PATH = os.environ.get("DATABASE_PATH", "learnwithpython.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL COLLATE NOCASE,
    email TEXT UNIQUE NOT NULL COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    xp INTEGER NOT NULL DEFAULT 0,
    streak INTEGER NOT NULL DEFAULT 0,
    last_active TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS lesson_progress (
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_slug TEXT NOT NULL,
    lesson_slug TEXT NOT NULL,
    completed_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, course_slug, lesson_slug)
);

CREATE TABLE IF NOT EXISTS challenge_progress (
    user_id INTEGER NOT NULL REFERENCES users(id),
    challenge_slug TEXT NOT NULL,
    completed_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, challenge_slug)
);

CREATE TABLE IF NOT EXISTS user_achievements (
    user_id INTEGER NOT NULL REFERENCES users(id),
    achievement_id TEXT NOT NULL,
    earned_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, achievement_id)
);
"""


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as db:
        db.executescript(SCHEMA)
        # Lightweight, additive migrations (safe to run every boot).
        cols = {r["name"] for r in db.execute("PRAGMA table_info(users)")}
        if "google_sub" not in cols:
            db.execute("ALTER TABLE users ADD COLUMN google_sub TEXT")
        if "avatar_url" not in cols:
            db.execute("ALTER TABLE users ADD COLUMN avatar_url TEXT")


# ── users ────────────────────────────────────────────────────────────

def create_user(username, email, password_hash):
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        return cur.lastrowid


def find_user(username_or_email):
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username_or_email, username_or_email),
        ).fetchone()
        return dict(row) if row else None


def find_user_by_google(google_sub):
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM users WHERE google_sub = ?", (google_sub,)
        ).fetchone()
        return dict(row) if row else None


def create_google_user(username, email, google_sub, avatar_url=None):
    """Create a passwordless account linked to a Google identity."""
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO users (username, email, password_hash, google_sub, avatar_url) "
            "VALUES (?, ?, '', ?, ?)",
            (username, email, google_sub, avatar_url),
        )
        return cur.lastrowid


def link_google_to_user(user_id, google_sub, avatar_url=None):
    with get_db() as db:
        db.execute(
            "UPDATE users SET google_sub = ?, avatar_url = COALESCE(?, avatar_url) WHERE id = ?",
            (google_sub, avatar_url, user_id),
        )


def get_user(user_id):
    with get_db() as db:
        row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def add_xp(user_id, amount):
    with get_db() as db:
        db.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (amount, user_id))


def touch_streak(user_id):
    """Update the daily streak; returns the current streak length."""
    today = date.today().isoformat()
    user = get_user(user_id)
    if user["last_active"] == today:
        return user["streak"]
    if user["last_active"]:
        gap = (date.fromisoformat(today) - date.fromisoformat(user["last_active"])).days
        streak = user["streak"] + 1 if gap == 1 else 1
    else:
        streak = 1
    with get_db() as db:
        db.execute(
            "UPDATE users SET streak = ?, last_active = ? WHERE id = ?",
            (streak, today, user_id),
        )
    return streak


# ── progress ─────────────────────────────────────────────────────────

def complete_lesson(user_id, course_slug, lesson_slug):
    """Record completion. Returns True if this was the first completion."""
    with get_db() as db:
        cur = db.execute(
            "INSERT OR IGNORE INTO lesson_progress (user_id, course_slug, lesson_slug) VALUES (?, ?, ?)",
            (user_id, course_slug, lesson_slug),
        )
        return cur.rowcount == 1


def complete_challenge(user_id, challenge_slug):
    with get_db() as db:
        cur = db.execute(
            "INSERT OR IGNORE INTO challenge_progress (user_id, challenge_slug) VALUES (?, ?)",
            (user_id, challenge_slug),
        )
        return cur.rowcount == 1


def get_progress(user_id):
    """Return {course_slug: set(lesson_slugs)} and set of challenge slugs."""
    with get_db() as db:
        lessons = db.execute(
            "SELECT course_slug, lesson_slug FROM lesson_progress WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        challenges = db.execute(
            "SELECT challenge_slug FROM challenge_progress WHERE user_id = ?",
            (user_id,),
        ).fetchall()
    by_course = {}
    for row in lessons:
        by_course.setdefault(row["course_slug"], set()).add(row["lesson_slug"])
    return by_course, {row["challenge_slug"] for row in challenges}


# ── achievements ─────────────────────────────────────────────────────

def get_earned_achievements(user_id):
    with get_db() as db:
        rows = db.execute(
            "SELECT achievement_id, earned_at FROM user_achievements WHERE user_id = ? ORDER BY earned_at",
            (user_id,),
        ).fetchall()
        return {row["achievement_id"]: row["earned_at"] for row in rows}


def grant_achievement(user_id, achievement_id):
    with get_db() as db:
        db.execute(
            "INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, ?)",
            (user_id, achievement_id),
        )


def leaderboard(limit=10):
    with get_db() as db:
        rows = db.execute(
            "SELECT username, xp, streak FROM users ORDER BY xp DESC, username LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
