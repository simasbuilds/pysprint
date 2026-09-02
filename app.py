"""LearnWithPython — an interactive Python learning platform.

Flask backend: pages, auth, progress API, achievements, SEO routes.
Run:  python app.py   (then open http://127.0.0.1:5000)
"""

import json
import os
import re
from datetime import date, datetime, timezone
from functools import wraps

from dotenv import load_dotenv
from flask import (Flask, Response, abort, g, jsonify, redirect, render_template, request,
                   session, url_for)

import database as db
import mailer
import supabase_auth
from data.achievements import ACHIEVEMENTS, evaluate
from data.challenges import CHALLENGES, get_challenge
from data.cheatsheet import CHEATSHEET, categories as cheat_categories
from data.resources import RESOURCES
from data.courses import COURSES, get_course, get_lesson, total_lessons
from data.glossary import get_glossary
from data.lesson_extras import get_extras
from data.projects import PROJECTS, get_project
from data.use_cases import get_course_use_cases
from data.walkthroughs import get_walkthrough

load_dotenv()

app = Flask(__name__)
def env(name, default=""):
    """Environment value with surrounding whitespace removed.

    Dashboards like Vercel happily store a trailing newline when a value is
    pasted, and it is invisible in their UI. That newline turned SITE_URL
    into "https://site.com\n", so the OAuth redirect_uri became
    "https://site.com\n/auth/google/callback" and Google rejected every
    sign-in with invalid_request. The same newline on SESSION_COOKIE_SECURE
    silently defeats the == "1" test and leaves session cookies insecure,
    which fails far more quietly.
    """
    return os.environ.get(name, default).strip()


app.config["SECRET_KEY"] = env("SECRET_KEY", "dev-only-change-me")
app.config["SITE_URL"] = env("SITE_URL", "http://127.0.0.1:5000")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = env("SESSION_COOKIE_SECURE", "0") == "1"

# ── Sign-in (Supabase Auth / GoTrue) ──────────────────────────────────
# Identity lives in Supabase, not here. Google sign-in is configured in the
# Supabase dashboard rather than in this app, so the only thing to decide
# locally is whether the feature is available at all.
app.config["GOOGLE_ENABLED"] = (
    supabase_auth.is_configured() and env("GOOGLE_ENABLED", "1") == "1"
)
app.config["AUTH_READY"] = supabase_auth.is_configured()

db.init_db()

# Admins are designated by the operator, never self-service. Set
# ADMIN_USERNAMES="alice,bob@example.com" in the environment.
db.sync_admins(os.environ.get("ADMIN_USERNAMES", "").split(","))

XP_PER_LEVEL = 250
LEVEL_TITLES = ["Newcomer", "Explorer", "Apprentice", "Coder", "Builder",
                "Engineer", "Architect", "Wizard", "Master", "Legend"]


# ── helpers ──────────────────────────────────────────────────────────

def current_user():
    """Cached per request: inject_globals calls this on every render, and
    several routes call it again, so without caching a single page issues
    the same query repeatedly.

    Reads the profile straight from Postgres rather than asking GoTrue, so a
    normal page load makes no network call to the auth service. The Flask
    signed cookie stays the source of truth for "is this person signed in";
    the GoTrue tokens are only needed to act on the auth record itself.
    """
    if "cached_user" not in g:
        uid = session.get("user_id")
        try:
            g.cached_user = db.get_user(uid) if uid else None
        except Exception:
            # A cookie predating the UUID migration holds an integer id,
            # which Postgres rejects outright. Fail soft to signed-out
            # rather than 500ing every page for anyone with a stale cookie.
            g.cached_user = None
    return g.cached_user


def forget_user():
    """Drop the request cache after a write that changes the profile."""
    g.pop("cached_user", None)


def start_session(auth):
    """Persist a GoTrue session in the Flask cookie."""
    session["user_id"] = auth["user"]["id"]
    session["access_token"] = auth.get("access_token", "")
    session["refresh_token"] = auth.get("refresh_token", "")
    session.permanent = True
    forget_user()


def safe_next(target):
    """Only allow same-site relative redirect targets (no open redirects)."""
    if target and target.startswith("/") and not target.startswith(("//", "/\\")):
        return target
    return None


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            if request.path.startswith("/api/"):
                return jsonify({"error": "login_required"}), 401
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    """Admin-only. 404s for signed-in non-admins so the portal isn't
    discoverable, and never leaks that the URL exists."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            return redirect(url_for("login", next=request.path))
        if not user["is_admin"]:
            abort(404)
        return fn(*args, **kwargs)
    return wrapper


def level_info(xp):
    level = xp // XP_PER_LEVEL + 1
    title = LEVEL_TITLES[min(level - 1, len(LEVEL_TITLES) - 1)]
    into = xp % XP_PER_LEVEL
    return {"level": level, "title": title, "into": into,
            "needed": XP_PER_LEVEL, "pct": round(into / XP_PER_LEVEL * 100)}


ARENA_SLUGS = {c["slug"] for c in CHALLENGES}


def user_stats(user):
    lessons_by_course, challenges = db.get_progress(user["id"])
    courses_done = {c["slug"] for c in COURSES
                    if lessons_by_course.get(c["slug"], set()) >=
                    {l["slug"] for l in c["lessons"]}}
    return {
        "lessons_done": sum(len(v) for v in lessons_by_course.values()),
        "courses_done": courses_done,
        "challenges_done": len(challenges & ARENA_SLUGS),
        "total_challenges": len(CHALLENGES),
        "projects_done": len({s for s in challenges if s.startswith("project:")}),
        "total_projects": len(PROJECTS),
        "xp": user["xp"],
        "streak": user["streak"],
        "total_lessons": total_lessons(),
    }


def award_new_achievements(user):
    stats = user_stats(user)
    earned = db.get_earned_achievements(user["id"])
    new = evaluate(stats, earned)
    for a in new:
        db.grant_achievement(user["id"], a["id"])
    return [{"id": a["id"], "icon": a["icon"], "title": a["title"],
             "desc": a["desc"]} for a in new]


def display_name_for(user):
    """What to call someone on screen.

    `username` is a handle — URL-safe, unique, no spaces — so it cannot be
    "Simas Bandzevicius". `display_name` is the free-form name, and falls
    back to the handle when unset.
    """
    if not user:
        return ""
    return (user["display_name"] or "").strip() or user["username"]


@app.template_filter("stamp")
def _stamp(value):
    """Date and time for admin listings. These columns are timestamptz since
    the move to auth.users; templates used to slice them as [:16] text,
    which raises TypeError on a datetime."""
    if not value:
        return ""
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d %H:%M")
    return str(value)[:16]


@app.template_filter("day")
def _day(value):
    """Render a date for display. created_at is a real timestamp since the
    move to auth.users; it used to be TEXT that templates sliced with
    [:10], which raises TypeError on a datetime."""
    if not value:
        return ""
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    return str(value)[:10]


@app.context_processor
def inject_globals():
    user = current_user()
    return {
        "user": user,
        "level": level_info(user["xp"]) if user else None,
        "site_url": app.config["SITE_URL"],
        "display_name": display_name_for(user),
        "now_year": datetime.now(timezone.utc).year,
        "n_lessons": total_lessons(),
        "n_courses": len(COURSES),
        "n_projects": len(PROJECTS),
        "n_project_steps": sum(len(pr["steps"]) for pr in PROJECTS),
        "n_challenges": len(CHALLENGES),
        "n_cheats": len(CHEATSHEET),
        "nav_courses": [{"slug": c["slug"], "title": c["title"],
                         "color": c["color"]} for c in COURSES],
        "nav_lessons": [{"title": l["title"], "course": c["title"],
                         "color": c["color"],
                         "href": f"/courses/{c['slug']}/{l['slug']}"}
                        for c in COURSES for l in c["lessons"]],
        "google_enabled": app.config.get("GOOGLE_ENABLED", False),
    }


# ── pages ────────────────────────────────────────────────────────────

def next_unfinished_lesson(lessons_by_course):
    """The next lesson in curriculum order that isn't done yet."""
    for course in COURSES:
        done = lessons_by_course.get(course["slug"], set())
        for lesson_ in course["lessons"]:
            if lesson_["slug"] not in done:
                return {"course": course, "lesson": lesson_}
    return None


@app.get("/")
def home():
    # One flagship real-world outcome per course for the homepage spotlight.
    spotlight = [{"course": c, "case": get_course_use_cases(c["slug"])[0]}
                 for c in COURSES if get_course_use_cases(c["slug"])]

    # Returning learners get their own progress cockpit instead of marketing
    # stats — the reason to come back is seeing your own streak move.
    me = None
    user = current_user()
    if user:
        lessons_by_course, challenges = db.get_progress(user["id"])
        done_total = sum(len(v) for v in lessons_by_course.values())
        me = {
            "lessons_done": done_total,
            "pct": round(done_total / total_lessons() * 100) if total_lessons() else 0,
            "challenges_done": len(challenges & ARENA_SLUGS),
            "achievements": len(db.get_earned_achievements(user["id"])),
            "resume": next_unfinished_lesson(lessons_by_course),
            "done_today": user["last_active"] == date.today().isoformat(),
        }

    return render_template("index.html", courses=COURSES,
                           projects=PROJECTS,
                           use_cases=spotlight,
                           me=me,
                           n_lessons=total_lessons(),
                           n_challenges=len(CHALLENGES),
                           n_achievements=len(ACHIEVEMENTS))


@app.get("/courses")
def courses():
    user = current_user()
    progress = {}
    if user:
        lessons_by_course, _ = db.get_progress(user["id"])
        for c in COURSES:
            done = len(lessons_by_course.get(c["slug"], set()))
            progress[c["slug"]] = round(done / len(c["lessons"]) * 100)
    return render_template("courses.html", courses=COURSES, progress=progress)


@app.get("/courses/<slug>")
def course_detail(slug):
    course = get_course(slug)
    if not course:
        abort(404)
    user = current_user()
    done = set()
    if user:
        lessons_by_course, _ = db.get_progress(user["id"])
        done = lessons_by_course.get(slug, set())
    total_xp = sum(l["xp"] for l in course["lessons"])
    return render_template("course.html", course=course, done=done,
                           total_xp=total_xp,
                           use_cases=get_course_use_cases(slug))


@app.get("/courses/<slug>/<lesson_slug>")
def lesson(slug, lesson_slug):
    course, idx = get_lesson(slug, lesson_slug)
    if not course or idx is None:
        abort(404)
    lessons = course["lessons"]
    user = current_user()
    done = set()
    if user:
        lessons_by_course, _ = db.get_progress(user["id"])
        done = lessons_by_course.get(slug, set())
    return render_template(
        "lesson.html", course=course, lesson=lessons[idx], idx=idx,
        prev=lessons[idx - 1] if idx > 0 else None,
        next=lessons[idx + 1] if idx + 1 < len(lessons) else None,
        done=done, n_lessons=len(lessons),
        extras=get_extras(slug, lesson_slug),
        walkthrough=get_walkthrough(slug, lesson_slug),
        glossary=get_glossary(),
    )


@app.get("/projects")
def projects():
    user = current_user()
    done = set()
    if user:
        _, challenges = db.get_progress(user["id"])
        done = {s[len("project:"):] for s in challenges if s.startswith("project:")}
    return render_template("projects.html", projects=PROJECTS, done=done)


@app.get("/projects/<slug>")
def project_detail(slug):
    project = get_project(slug)
    if not project:
        abort(404)
    user = current_user()
    completed = False
    if user:
        _, challenges = db.get_progress(user["id"])
        completed = f"project:{slug}" in challenges
    return render_template("project.html", project=project, completed=completed)


@app.get("/challenges")
def challenges():
    user = current_user()
    done = set()
    if user:
        _, done = db.get_progress(user["id"])
    return render_template("challenges.html", challenges=CHALLENGES, done=done)


@app.get("/challenges/<slug>")
def challenge_detail(slug):
    ch = get_challenge(slug)
    if not ch:
        abort(404)
    user = current_user()
    done = set()
    if user:
        _, done = db.get_progress(user["id"])
    idx = next((i for i, c in enumerate(CHALLENGES) if c["slug"] == slug), None)
    return render_template(
        "challenge.html", ch=ch, done=done,
        prev=CHALLENGES[idx - 1] if idx else None,
        next=CHALLENGES[idx + 1] if idx is not None and idx + 1 < len(CHALLENGES) else None,
    )


@app.get("/playground")
def playground():
    return render_template("playground.html")


@app.get("/review")
def review():
    # Flashcards are built client-side from the full quiz bank.
    cards = []
    for course in COURSES:
        for lesson_ in course["lessons"]:
            for q in lesson_.get("quiz", []):
                cards.append({
                    "course": course["title"],
                    "q": q["q"],
                    "a": q["options"][q["answer"]],
                    "explain": q.get("explain", ""),
                })
    return render_template("review.html", cards=cards)


@app.get("/dashboard")
@login_required
def dashboard():
    user = current_user()
    lessons_by_course, challenges_done = db.get_progress(user["id"])
    stats = user_stats(user)
    earned = db.get_earned_achievements(user["id"])
    course_cards = []
    for c in COURSES:
        done = len(lessons_by_course.get(c["slug"], set()))
        course_cards.append({
            "course": c, "done": done, "total": len(c["lessons"]),
            "pct": round(done / len(c["lessons"]) * 100),
        })
    achievements_view = [
        {**{k: a[k] for k in ("id", "icon", "title", "desc")},
         "earned": a["id"] in earned}
        for a in ACHIEVEMENTS
    ]
    return render_template("dashboard.html", stats=stats,
                           course_cards=course_cards,
                           achievements=achievements_view,
                           n_earned=len(earned),
                           challenges_done=challenges_done,
                           leaders=db.leaderboard())


@app.get("/about")
def about():
    return render_template("about.html", n_lessons=total_lessons(),
                           n_challenges=len(CHALLENGES))


@app.get("/cheatsheet")
def cheatsheet():
    """A browsable reference of the Python worth knowing, by category.

    Every snippet carries the output it actually produces, so the page can
    be trusted as a reference rather than skimmed as decoration.
    """
    return render_template("cheatsheet.html",
                           entries=CHEATSHEET,
                           cats=cheat_categories(),
                           resources=RESOURCES)


@app.get("/start")
def start():
    """Onboarding for someone who has never written a line of code.

    The rest of the site assumes you know what a lesson or a challenge is.
    This page assumes nothing: it explains what Python is, what an hour
    here actually looks like, and why the site is built the way it is —
    then hands over to lesson one.
    """
    first = COURSES[0]
    return render_template("start.html",
                           first_course=first,
                           first_lesson=first["lessons"][0],
                           beginner_courses=[c for c in COURSES
                                             if c["level"] == "Beginner"][:3])


# ── auth ─────────────────────────────────────────────────────────────

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,24}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def send_welcome_email(username, email):
    """Fire-and-forget welcome message. Never raises: a mail outage must not
    turn a successful signup into an error page."""
    if not mailer.is_configured():
        return
    try:
        site = (env("SITE_URL") or request.url_root).rstrip("/")
        html = render_template(
            "email/welcome.html",
            name=username,
            email=email,
            site_url=site,
            start_url=site + url_for("start"),
            doors=[
                {"title": "Start from absolute zero",
                 "body": "What Python is, what your first hour looks like, and a line you run yourself.",
                 "url": site + url_for("start")},
                {"title": "Take the course path",
                 "body": "%d lessons from your first print() to decorators, generators and real APIs." % total_lessons(),
                 "url": site + url_for("courses")},
                {"title": "Open a blank workspace",
                 "body": "Write, run and download real Python with nothing installed.",
                 "url": site + url_for("playground")},
            ],
            stats=[
                {"n": total_lessons(), "label": "Lessons"},
                {"n": len(PROJECTS), "label": "Projects"},
                {"n": len(CHALLENGES), "label": "Challenges"},
            ],
        )
        text = (
            "You're in, %s.\n\n"
            "Your account is live. Nothing to install - real Python runs in your browser.\n\n"
            "Write your first line: %s\n\n"
            "LearnWithPython - Learn Python by writing it, not watching it."
        ) % (username, site + url_for("start"))
        mailer.send(email, "You're in - welcome to LearnWithPython", html, text)
    except Exception as exc:
        print("[mail] welcome render failed: %r" % exc)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not USERNAME_RE.match(username):
            error = "Username must be 3–24 characters: letters, numbers, underscores."
        elif not EMAIL_RE.match(email):
            error = "Please enter a valid email address."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif db.username_taken(username):
            error = "That username is already taken."
        else:
            auth, err = supabase_auth.sign_up(email, password, username=username)
            if err:
                error = err
            elif not auth.get("access_token"):
                # Email confirmation is on, so no session comes back and the
                # person cannot be signed in yet.
                return render_template("register.html", check_email=email)
            else:
                # The profile row is created by a database trigger, which
                # picks its own unique username; apply the requested one now
                # that the account exists.
                uid = auth["user"]["id"]
                if not db.username_taken(username, uid):
                    db.update_profile(uid, username=username)
                send_welcome_email(username, email)
                start_session(auth)
                # Come back to the lesson they were on, so device progress
                # syncs in context instead of dumping them on the dashboard.
                return redirect(safe_next(request.args.get("next"))
                                or url_for("dashboard"))
    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        ident = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        auth, err = supabase_auth.sign_in(ident, password)
        if auth:
            start_session(auth)
            return redirect(safe_next(request.args.get("next")) or url_for("dashboard"))
        # Deliberately not distinguishing "no such account" from "wrong
        # password" — that difference tells an attacker which emails exist.
        error = "Invalid credentials — check your email and password."
    return render_template("login.html", error=error)


@app.get("/logout")
def logout():
    # Revoke the refresh token server-side as well, so signing out is not
    # merely the browser forgetting its cookie.
    supabase_auth.sign_out(session.get("access_token"))
    session.clear()
    forget_user()
    return redirect(url_for("home"))


# ── Google Sign-In (via Supabase Auth, PKCE) ─────────────────────────

# Username generation now lives in the on_auth_user_created database
# trigger, which runs in the same transaction as the auth user and so has
# no race between checking a name and taking it.


@app.get("/auth/google")
def google_login():
    if not app.config.get("GOOGLE_ENABLED"):
        return redirect(url_for("login"))
    # PKCE, not the implicit flow: implicit returns the code in the URL
    # fragment, which browsers never send to the server, so a server-rendered
    # app could not read it without JavaScript handing it back.
    verifier = supabase_auth.make_verifier()
    session["pkce_verifier"] = verifier
    session["oauth_next"] = safe_next(request.args.get("next")) or url_for("dashboard")
    redirect_uri = app.config["SITE_URL"].rstrip("/") + url_for("google_callback")
    return redirect(supabase_auth.oauth_url(
        "google", redirect_uri, supabase_auth.challenge_for(verifier)))


@app.get("/auth/google/callback")
def google_callback():
    verifier = session.pop("pkce_verifier", None)
    code = request.args.get("code")
    if not code or not verifier:
        app.logger.warning("Google callback without code or verifier")
        return redirect(url_for("login"))

    auth, err = supabase_auth.exchange_code(code, verifier)
    if err or not auth.get("access_token"):
        app.logger.warning("Google code exchange failed: %s", err)
        return redirect(url_for("login"))

    start_session(auth)
    uid = auth["user"]["id"]

    # Refresh the stored Google photo on every sign-in: people change it, and
    # an account created before this ran has none yet. Only google_avatar is
    # touched, never the avatar they picked themselves.
    meta = (auth["user"].get("user_metadata") or {})
    picture = meta.get("avatar_url") or meta.get("picture")
    if picture:
        db.update_google_avatar(uid, picture)
        forget_user()

    user = current_user()
    if user:
        award_new_achievements(user)
    return redirect(session.pop("oauth_next", None) or url_for("dashboard"))


AVATARS = ["bolt", "cat", "flame", "fox", "leaf", "moon",
           "owl", "plane", "rocket", "summit", "terminal", "whale"]


def avatar_choices():
    return [{"key": a, "url": url_for("static", filename=f"images/avatars/{a}.png")}
            for a in AVATARS]


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user()
    error = saved = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        avatar = request.form.get("avatar", "").strip()
        display = request.form.get("display_name", "").strip()

        if len(display) > 40:
            error = "Display name must be 40 characters or fewer."
        elif not USERNAME_RE.match(username):
            error = "Username must be 3–24 characters: letters, numbers, underscores."
        elif db.username_taken(username, exclude_user_id=user["id"]):
            error = "That username is already taken."
        else:
            avatar_url = None
            if avatar == "none":
                avatar_url = ""
            elif avatar == "google" and user["google_avatar"]:
                avatar_url = user["google_avatar"]
            elif avatar in AVATARS:
                avatar_url = url_for("static", filename=f"images/avatars/{avatar}.png")
            db.update_profile(user["id"], username=username, avatar_url=avatar_url,
                              display_name=display)
            forget_user()
            user = current_user()
            saved = "Profile updated."

    stats = user_stats(user)
    return render_template("profile.html", error=error, saved=saved,
                           stats=stats, avatars=avatar_choices(),
                           level=level_info(user["xp"]),
                           earned=len(db.get_earned_achievements(user["id"])))


@app.get("/profile/export")
@login_required
def profile_export():
    """Download everything we hold about you, as JSON."""
    data = db.export_user(current_user()["id"])
    if not data:
        abort(404)
    payload = json.dumps(data, indent=2, default=str)
    return Response(
        payload, mimetype="application/json",
        headers={"Content-Disposition":
                 'attachment; filename="learnwithpython-my-data.json"'})


@app.post("/profile/delete")
@login_required
def profile_delete():
    """Permanently delete the signed-in account.

    Requires the person to type their username, so a stray click cannot do
    it. Accounts with a password must also confirm it — without that, anyone
    with a borrowed unlocked laptop could erase the account.

    The password is now checked by signing in against Supabase rather than
    against a local hash, which is authoritative rather than a copy. Deleting
    the auth record cascades the profile and all progress away with it, so
    the export really does describe everything that is removed.
    """
    user = current_user()
    typed = request.form.get("confirm_username", "").strip()
    password = request.form.get("password", "")

    if typed.lower() != user["username"].lower():
        return redirect(url_for("profile", delete_error="name"))

    # Google-only accounts have no password to confirm; the template hides
    # the field for them, and typing the username stays their sole guard.
    if password:
        auth, err = supabase_auth.sign_in(user["email"], password)
        if err or not auth:
            return redirect(url_for("profile", delete_error="password"))

    _, err = supabase_auth.admin_delete_user(user["id"])
    if err:
        app.logger.error("Account deletion failed for %s: %s", user["id"], err)
        return redirect(url_for("profile", delete_error="failed"))

    session.clear()
    forget_user()
    return redirect(url_for("home", deleted="1"))


@app.get("/about-me")
def creator():
    """The person behind the site. Separate from /about, which explains the
    product — a visitor deciding whether to trust a free course wants both,
    and conflating them buries each."""
    return render_template("creator.html")


@app.get("/terms")
def terms():
    return render_template("legal.html", doc="terms")


@app.get("/privacy")
def privacy():
    return render_template("legal.html", doc="privacy")


# ── progress API ─────────────────────────────────────────────────────

@app.post("/api/complete-lesson")
@login_required
def api_complete_lesson():
    payload = request.get_json(silent=True) or {}
    course, idx = get_lesson(payload.get("course", ""), payload.get("lesson", ""))
    if not course or idx is None:
        return jsonify({"error": "unknown_lesson"}), 400
    user = current_user()
    lesson_ = course["lessons"][idx]
    first_time = db.complete_lesson(user["id"], course["slug"], lesson_["slug"])
    xp_gained = lesson_["xp"] if first_time else 0
    if first_time:
        db.add_xp(user["id"], xp_gained)
    streak = db.touch_streak(user["id"])
    new_achievements = award_new_achievements(db.get_user(user["id"]))
    fresh = db.get_user(user["id"])
    return jsonify({
        "ok": True, "first_time": first_time, "xp_gained": xp_gained,
        "xp": fresh["xp"], "streak": streak, "level": level_info(fresh["xp"]),
        "new_achievements": new_achievements,
    })


@app.post("/api/complete-challenge")
@login_required
def api_complete_challenge():
    payload = request.get_json(silent=True) or {}
    ch = get_challenge(payload.get("challenge", ""))
    if not ch:
        return jsonify({"error": "unknown_challenge"}), 400
    user = current_user()
    first_time = db.complete_challenge(user["id"], ch["slug"])
    xp_gained = ch["xp"] if first_time else 0
    if first_time:
        db.add_xp(user["id"], xp_gained)
    streak = db.touch_streak(user["id"])
    new_achievements = award_new_achievements(db.get_user(user["id"]))
    fresh = db.get_user(user["id"])
    return jsonify({
        "ok": True, "first_time": first_time, "xp_gained": xp_gained,
        "xp": fresh["xp"], "streak": streak, "level": level_info(fresh["xp"]),
        "new_achievements": new_achievements,
    })


@app.post("/api/complete-project")
@login_required
def api_complete_project():
    payload = request.get_json(silent=True) or {}
    project = get_project(payload.get("project", ""))
    if not project:
        return jsonify({"error": "unknown_project"}), 400
    user = current_user()
    first_time = db.complete_challenge(user["id"], f"project:{project['slug']}")
    xp_gained = project["xp"] if first_time else 0
    if first_time:
        db.add_xp(user["id"], xp_gained)
    streak = db.touch_streak(user["id"])
    new_achievements = award_new_achievements(db.get_user(user["id"]))
    fresh = db.get_user(user["id"])
    return jsonify({
        "ok": True, "first_time": first_time, "xp_gained": xp_gained,
        "xp": fresh["xp"], "streak": streak, "level": level_info(fresh["xp"]),
        "new_achievements": new_achievements,
    })


@app.post("/api/sync-progress")
@login_required
def api_sync_progress():
    """Merge device-local (guest) lesson progress into the signed-in account.

    Learners can take the whole curriculum without an account; when they
    finally sign up we fold that work in so the "log in to save" prompt is
    honest. Unknown slugs are ignored and XP is only granted once.
    """
    payload = request.get_json(silent=True) or {}
    items = payload.get("completions")
    if not isinstance(items, list):
        return jsonify({"error": "bad_payload"}), 400

    user = current_user()
    synced = xp_gained = 0
    for item in items[:500]:                      # bound the work per call
        if not isinstance(item, dict):
            continue
        course, idx = get_lesson(str(item.get("course", "")),
                                 str(item.get("lesson", "")))
        if not course or idx is None:
            continue
        lesson_ = course["lessons"][idx]
        if db.complete_lesson(user["id"], course["slug"], lesson_["slug"]):
            synced += 1
            xp_gained += lesson_["xp"]

    if xp_gained:
        db.add_xp(user["id"], xp_gained)
    new_achievements = award_new_achievements(db.get_user(user["id"]))
    fresh = db.get_user(user["id"])
    return jsonify({
        "ok": True, "synced": synced, "xp_gained": xp_gained,
        "xp": fresh["xp"], "level": level_info(fresh["xp"]),
        "new_achievements": new_achievements,
    })


@app.get("/api/me")
def api_me():
    user = current_user()
    if not user:
        return jsonify({"logged_in": False})
    return jsonify({"logged_in": True, "username": user["username"],
                    "xp": user["xp"], "streak": user["streak"],
                    "level": level_info(user["xp"])})


# ── admin portal ─────────────────────────────────────────────────────

@app.get("/admin")
@admin_required
def admin():
    search = (request.args.get("q") or "").strip()[:60]
    sort = request.args.get("sort", "recent")
    members, total = db.list_members(search=search, sort=sort)
    course_titles = {c["slug"]: c["title"] for c in COURSES}
    engagement = []
    for row in db.course_engagement():
        course = get_course(row["course_slug"])
        engagement.append({
            **row,
            "title": course_titles.get(row["course_slug"], row["course_slug"]),
            "lessons": len(course["lessons"]) if course else 0,
        })
    for m in members:
        m["level"] = level_info(m["xp"])
    return render_template("admin.html", members=members, total=total,
                           search=search, sort=sort,
                           stats=db.platform_stats(),
                           signups=db.signups_by_day(),
                           engagement=engagement,
                           n_lessons=total_lessons())


@app.get("/admin/members/<uuid:uid>")
@admin_required
def admin_member(uid):
    detail = db.member_detail(str(uid))
    if not detail:
        abort(404)
    course_titles = {c["slug"]: c["title"] for c in COURSES}
    lesson_titles = {(c["slug"], l["slug"]): l["title"]
                     for c in COURSES for l in c["lessons"]}
    by_course = {}
    for row in detail["lessons"]:
        key = row["course_slug"]
        by_course.setdefault(key, {
            "title": course_titles.get(key, key),
            "total": len(get_course(key)["lessons"]) if get_course(key) else 0,
            "items": [],
        })
        by_course[key]["items"].append({
            **row,
            "title": lesson_titles.get((key, row["lesson_slug"]), row["lesson_slug"]),
        })
    achievement_titles = {a["id"]: a for a in ACHIEVEMENTS}
    return render_template("admin_member.html", d=detail,
                           level=level_info(detail["user"]["xp"]),
                           by_course=by_course,
                           achievement_titles=achievement_titles,
                           n_lessons=total_lessons())


# ── SEO ──────────────────────────────────────────────────────────────

@app.get("/sitemap.xml")
def sitemap():
    base = app.config["SITE_URL"].rstrip("/")
    today = date.today().isoformat()
    urls = [("", "1.0"), ("/start", "0.9"), ("/cheatsheet", "0.8"),
            ("/courses", "0.9"),
            ("/projects", "0.9"), ("/challenges", "0.8"),
            ("/playground", "0.7"), ("/review", "0.6"), ("/about", "0.5"),
            ("/about-me", "0.5"),
            ("/terms", "0.3"), ("/privacy", "0.3")]
    for p in PROJECTS:
        urls.append((f"/projects/{p['slug']}", "0.7"))
    for c in COURSES:
        urls.append((f"/courses/{c['slug']}", "0.8"))
        for l in c["lessons"]:
            urls.append((f"/courses/{c['slug']}/{l['slug']}", "0.6"))
    for ch in CHALLENGES:
        urls.append((f"/challenges/{ch['slug']}", "0.6"))
    items = "".join(
        f"<url><loc>{base}{path}</loc><lastmod>{today}</lastmod>"
        f"<priority>{prio}</priority></url>"
        for path, prio in urls
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           f"{items}</urlset>")
    return app.response_class(xml, mimetype="application/xml")


@app.get("/robots.txt")
def robots():
    base = app.config["SITE_URL"].rstrip("/")
    return app.response_class(
        f"User-agent: *\nAllow: /\nDisallow: /dashboard\nDisallow: /admin\nDisallow: /api/\n"
        f"Sitemap: {base}/sitemap.xml\n",
        mimetype="text/plain")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    debug = env("FLASK_DEBUG", "1") == "1"
    port = int(env("PORT", "5000"))
    app.run(debug=debug, port=port)
