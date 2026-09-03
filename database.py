"""Persistence.

Postgres only, spoken directly. There is no SQLite fallback and no dialect
translation: identity now lives in Supabase's `auth.users`, which is a
hosted service with no local equivalent, so a second backend could not have
told the same story anyway.

The previous version rewrote SQLite-flavoured SQL on the way past —
"INSERT OR IGNORE" became ON CONFLICT, and any statement matching
`INSERT INTO users` had RETURNING id appended so cursor.lastrowid would
work. That regex keyed on the literal table name, so renaming the table
would have made inserts silently return None rather than fail. Writing real
Postgres removes the whole class of problem.

Identity is not stored here. `auth.users` owns email, password and OAuth
identities; `public.profiles` (keyed by the same UUID) owns only what GoTrue
has no concept of: username, display name, XP, streak and avatars.
"""

import os
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()


class _Row(dict):
    """Addressable by column name *or* position.

    psycopg's dict_row supports names only, and several queries here index
    positionally (`fetchone()[0]`), which a plain dict breaks silently.
    """

    __slots__ = ()

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self.values())[key]
        return super().__getitem__(key)


def _row_factory(cursor):
    cols = [c.name for c in cursor.description or []]
    def make(values):
        return _Row(zip(cols, values))
    return make


@contextmanager
def get_db():
    conn = psycopg.connect(DATABASE_URL, row_factory=_row_factory)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Schema lives in Supabase migrations, not in app boot.

    Kept as a no-op so callers and deploy scripts do not need to change, and
    because creating tables from the app would fight the migration ledger.
    """
    return


def _days_ago(n):
    return datetime.now(timezone.utc) - timedelta(days=n)


# ── profiles ─────────────────────────────────────────────────────────
# Rows are created by the on_auth_user_created trigger, never here: with
# OAuth the user appears inside GoTrue during the callback and the app only
# learns about it afterwards, so app-side creation would leave a window
# where an auth user exists with no profile.

def get_user(user_id):
    """Profile joined to the auth record. `email` and `has_google` are read
    through rather than copied, so they cannot drift from GoTrue."""
    if not user_id:
        return None
    with get_db() as db:
        row = db.execute("""
            SELECT p.*, au.email, au.last_sign_in_at, au.email_confirmed_at,
                   (au.banned_until IS NOT NULL AND au.banned_until > now()) AS is_banned,
                   EXISTS (SELECT 1 FROM auth.identities i
                           WHERE i.user_id = p.id AND i.provider = 'google') AS has_google
            FROM public.profiles p
            LEFT JOIN auth.users au ON au.id = p.id
            WHERE p.id = %s
        """, (str(user_id),)).fetchone()
        return dict(row) if row else None


def find_profile_by_username(username):
    with get_db() as db:
        row = db.execute(
            "SELECT id FROM public.profiles WHERE username = %s", (username,)
        ).fetchone()
        return dict(row) if row else None


def add_xp(user_id, amount):
    with get_db() as db:
        db.execute("UPDATE public.profiles SET xp = xp + %s WHERE id = %s",
                   (amount, str(user_id)))


def touch_streak(user_id):
    """Advance the streak at most once a day; reset it if a day was missed."""
    today = datetime.now(timezone.utc).date()
    user = get_user(user_id)
    if not user:
        return 0
    last = user.get("last_active")
    if last:
        try:
            last_date = datetime.strptime(last[:10], "%Y-%m-%d").date()
        except ValueError:
            last_date = None
        if last_date == today:
            return user["streak"]
        streak = user["streak"] + 1 if last_date == today - timedelta(days=1) else 1
    else:
        streak = 1
    with get_db() as db:
        db.execute(
            "UPDATE public.profiles SET streak = %s, last_active = %s WHERE id = %s",
            (streak, today.isoformat(), str(user_id)))
    return streak


def username_taken(username, exclude_user_id=None):
    """True if the name belongs to somebody else.

    Both sides are compared as strings on purpose. psycopg returns
    uuid.UUID for a uuid column while the session cookie holds a str, and
    `UUID(x) != str(x)` is always True — which would tell every person their
    own username was taken and silently block all profile edits.
    """
    with get_db() as db:
        row = db.execute("SELECT id FROM public.profiles WHERE username = %s",
                         (username,)).fetchone()
    return bool(row) and str(row["id"]) != str(exclude_user_id or "")


def update_profile(user_id, username=None, avatar_url=None, display_name=None):
    sets, params = [], []
    if username is not None:
        sets.append("username = %s"); params.append(username)
    if avatar_url is not None:
        sets.append("avatar_url = %s"); params.append(avatar_url)
    if display_name is not None:
        sets.append("display_name = %s"); params.append(display_name)
    if not sets:
        return
    params.append(str(user_id))
    with get_db() as db:
        db.execute("UPDATE public.profiles SET %s WHERE id = %%s" % ", ".join(sets),
                   tuple(params))


def update_google_avatar(user_id, url):
    with get_db() as db:
        db.execute("UPDATE public.profiles SET google_avatar = %s WHERE id = %s",
                   (url, str(user_id)))


def sync_admins(names):
    """Make ADMIN_USERNAMES authoritative, not merely additive.

    The old set_admin only ever granted, so removing someone from the env
    var left them admin forever and a stale value silently re-promoted an
    account on the next boot. This grants to everyone named and revokes
    from everyone else, in one statement, so the environment is the single
    source of truth.

    Names match either the profile username or the auth email.
    """
    names = [n.strip().lower() for n in names if n and n.strip()]
    with get_db() as db:
        db.execute("""
            UPDATE public.profiles p SET is_admin = (
                lower(p.username) = ANY(%s)
                OR lower(COALESCE((SELECT email FROM auth.users a WHERE a.id = p.id), '')) = ANY(%s)
            )
        """, (names, names))


# ── progress ─────────────────────────────────────────────────────────

def complete_lesson(user_id, course_slug, lesson_slug):
    """True only the first time, which is what gates the XP award."""
    with get_db() as db:
        cur = db.execute("""
            INSERT INTO public.lesson_progress (user_id, course_slug, lesson_slug)
            VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
        """, (str(user_id), course_slug, lesson_slug))
        return cur.rowcount == 1


def complete_challenge(user_id, challenge_slug):
    with get_db() as db:
        cur = db.execute("""
            INSERT INTO public.challenge_progress (user_id, challenge_slug)
            VALUES (%s, %s) ON CONFLICT DO NOTHING
        """, (str(user_id), challenge_slug))
        return cur.rowcount == 1


def get_progress(user_id):
    """Return {course_slug: set(lesson_slugs)} and a set of challenge slugs."""
    with get_db() as db:
        lessons = db.execute(
            "SELECT course_slug, lesson_slug FROM public.lesson_progress WHERE user_id = %s",
            (str(user_id),)).fetchall()
        challenges = db.execute(
            "SELECT challenge_slug FROM public.challenge_progress WHERE user_id = %s",
            (str(user_id),)).fetchall()
    # Callers unpack this as (by_course, challenges) — keep that contract.
    by_course = {}
    for row in lessons:
        by_course.setdefault(row["course_slug"], set()).add(row["lesson_slug"])
    return by_course, {row["challenge_slug"] for row in challenges}


def get_earned_achievements(user_id):
    with get_db() as db:
        rows = db.execute(
            "SELECT achievement_id FROM public.user_achievements WHERE user_id = %s",
            (str(user_id),)).fetchall()
    return [r["achievement_id"] for r in rows]


def grant_achievement(user_id, achievement_id):
    with get_db() as db:
        cur = db.execute("""
            INSERT INTO public.user_achievements (user_id, achievement_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING
        """, (str(user_id), achievement_id))
        return cur.rowcount == 1


def leaderboard(limit=10):
    with get_db() as db:
        rows = db.execute("""
            SELECT username, display_name, xp, streak, avatar_url
            FROM public.profiles ORDER BY xp DESC, username ASC LIMIT %s
        """, (limit,)).fetchall()
    return [dict(r) for r in rows]


# ── export / delete ──────────────────────────────────────────────────

def export_user(user_id):
    """Everything held about a person. Deliberately adjacent to
    delete_user: the export must not describe data the delete leaves."""
    with get_db() as db:
        user = db.execute("""
            SELECT p.*, au.email, au.created_at AS auth_created_at
            FROM public.profiles p
            LEFT JOIN auth.users au ON au.id = p.id
            WHERE p.id = %s
        """, (str(user_id),)).fetchone()
        if not user:
            return None
        lessons = db.execute(
            "SELECT course_slug, lesson_slug, completed_at FROM public.lesson_progress WHERE user_id = %s",
            (str(user_id),)).fetchall()
        challenges = db.execute(
            "SELECT challenge_slug, completed_at FROM public.challenge_progress WHERE user_id = %s",
            (str(user_id),)).fetchall()
        achievements = db.execute(
            "SELECT achievement_id, earned_at FROM public.user_achievements WHERE user_id = %s",
            (str(user_id),)).fetchall()
    return {
        "account": dict(user),
        "lessons": [dict(r) for r in lessons],
        "challenges": [dict(r) for r in challenges],
        "achievements": [dict(r) for r in achievements],
    }


def delete_user(user_id):
    """Only the profile side. The auth record is removed through GoTrue's
    admin API, and its ON DELETE CASCADE takes the profile and all progress
    with it — so callers should delete the auth user, not call this."""
    with get_db() as db:
        cur = db.execute("DELETE FROM public.profiles WHERE id = %s", (str(user_id),))
        return cur.rowcount > 0


# ── admin ────────────────────────────────────────────────────────────

# Keys must cover every option admin.html offers, or the select silently
# falls back to "recent" and the control looks broken for no visible reason.
SORTS = {
    "recent": "COALESCE(au.last_sign_in_at, p.created_at) DESC",
    "joined": "p.created_at DESC",
    "xp": "p.xp DESC",
    "lessons": "lessons_done DESC",
    "streak": "p.streak DESC",
    "name": "p.username ASC",
}


def list_members(search="", sort="recent", limit=200, offset=0):
    order = SORTS.get(sort, SORTS["recent"])
    where, params = "", []
    if search:
        where = "WHERE p.username ILIKE %s OR au.email ILIKE %s OR p.display_name ILIKE %s"
        params = ["%%%s%%" % search] * 3
    params.extend([limit, offset])
    with get_db() as db:
        rows = db.execute("""
            SELECT p.id, p.username, p.display_name, p.xp, p.streak, p.is_admin,
                   p.created_at, p.last_active, au.email,
                   au.last_sign_in_at, au.email_confirmed_at,
                   (au.banned_until IS NOT NULL AND au.banned_until > now()) AS is_banned,
                   EXISTS (SELECT 1 FROM auth.identities i
                           WHERE i.user_id = p.id AND i.provider = 'google') AS has_google,
                   (SELECT COUNT(*) FROM public.lesson_progress l WHERE l.user_id = p.id) AS lessons_done,
                   (SELECT COUNT(*) FROM public.challenge_progress c WHERE c.user_id = p.id) AS challenges_done,
                   (SELECT COUNT(*) FROM public.user_achievements a WHERE a.user_id = p.id) AS achievements
            FROM public.profiles p
            LEFT JOIN auth.users au ON au.id = p.id
            %s ORDER BY %s LIMIT %%s OFFSET %%s
        """ % (where, order), tuple(params)).fetchall()
        # The portal shows a member count beside the heading, so the total
        # must survive paging — callers unpack (rows, total).
        total = db.execute(
            "SELECT COUNT(*) AS n FROM public.profiles p "
            "LEFT JOIN auth.users au ON au.id = p.id %s" % where,
            tuple(params[:-2])).fetchone()["n"]
    return [dict(r) for r in rows], total


def member_detail(user_id):
    user = get_user(user_id)
    if not user:
        return None
    with get_db() as db:
        lessons = db.execute("""
            SELECT course_slug, lesson_slug, completed_at FROM public.lesson_progress
            WHERE user_id = %s ORDER BY completed_at DESC
        """, (str(user_id),)).fetchall()
        challenges = db.execute("""
            SELECT challenge_slug, completed_at FROM public.challenge_progress
            WHERE user_id = %s ORDER BY completed_at DESC
        """, (str(user_id),)).fetchall()
        achievements = db.execute(
            "SELECT achievement_id, earned_at FROM public.user_achievements WHERE user_id = %s",
            (str(user_id),)).fetchall()
    return {
        "user": user,
        "lessons": [dict(r) for r in lessons],
        "challenges": [dict(r) for r in challenges],
        "achievements": [dict(r) for r in achievements],
    }


def platform_stats():
    """Headline numbers for the admin overview.

    Key names are the contract admin.html renders against — renaming them
    silently blanks tiles rather than raising, so they stay as they were.
    """
    from datetime import date
    today = date.today()
    with get_db() as db:
        one = lambda q, p=(): db.execute(q, p).fetchone()[0]
        return {
            "members": one("SELECT COUNT(*) FROM public.profiles"),
            "admins": one("SELECT COUNT(*) FROM public.profiles WHERE is_admin"),
            "google_members": one(
                "SELECT COUNT(DISTINCT user_id) FROM auth.identities WHERE provider = 'google'"),
            "new_7d": one(
                "SELECT COUNT(*) FROM public.profiles WHERE created_at >= %s",
                (_days_ago(7),)),
            "active_7d": one(
                "SELECT COUNT(*) FROM public.profiles WHERE last_active >= %s",
                ((today - timedelta(days=7)).isoformat(),)),
            "active_today": one(
                "SELECT COUNT(*) FROM public.profiles WHERE last_active = %s",
                (today.isoformat(),)),
            "lessons_completed": one("SELECT COUNT(*) FROM public.lesson_progress"),
            "challenges_completed": one("SELECT COUNT(*) FROM public.challenge_progress"),
            "total_xp": one("SELECT COALESCE(SUM(xp), 0) FROM public.profiles"),
            "learners_with_progress": one(
                "SELECT COUNT(DISTINCT user_id) FROM public.lesson_progress"),
        }


def signups_by_day(days=14):
    with get_db() as db:
        rows = db.execute("""
            SELECT to_char(created_at, 'YYYY-MM-DD') AS day, COUNT(*) AS n
            FROM public.profiles WHERE created_at >= %s
            GROUP BY day ORDER BY day
        """, (_days_ago(days),)).fetchall()
    return [dict(r) for r in rows]


def course_engagement():
    with get_db() as db:
        rows = db.execute("""
            SELECT course_slug, COUNT(*) AS completions,
                   COUNT(DISTINCT user_id) AS learners
            FROM public.lesson_progress GROUP BY course_slug
            ORDER BY completions DESC
        """).fetchall()
    return [dict(r) for r in rows]
