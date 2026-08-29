"""LearnWithPython — an interactive Python learning platform.

Flask backend: pages, auth, progress API, achievements, SEO routes.
Run:  python app.py   (then open http://127.0.0.1:5000)
"""

import os
import re
from datetime import date, datetime, timezone
from functools import wraps

from dotenv import load_dotenv
from flask import (Flask, abort, jsonify, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import database as db
from data.achievements import ACHIEVEMENTS, evaluate
from data.challenges import CHALLENGES, get_challenge
from data.courses import COURSES, get_course, get_lesson, total_lessons
from data.glossary import get_glossary
from data.lesson_extras import get_extras
from data.projects import PROJECTS, get_project
from data.use_cases import get_course_use_cases
from data.walkthroughs import get_walkthrough

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["SITE_URL"] = os.environ.get("SITE_URL", "http://127.0.0.1:5000")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"

# ── Google Sign-In (optional; activates when credentials are present) ──
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "").strip()
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "").strip()
google_oauth = None
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    try:
        from authlib.integrations.flask_client import OAuth
        _oauth = OAuth(app)
        google_oauth = _oauth.register(
            name="google",
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
    except Exception as exc:  # Authlib missing or misconfigured — stay disabled.
        app.logger.warning("Google OAuth disabled: %s", exc)
        google_oauth = None

app.config["GOOGLE_ENABLED"] = google_oauth is not None

db.init_db()

# Admins are designated by the operator, never self-service. Set
# ADMIN_USERNAMES="alice,bob@example.com" in the environment.
for _name in (n.strip() for n in os.environ.get("ADMIN_USERNAMES", "").split(",")):
    if _name:
        db.set_admin(_name, True)

XP_PER_LEVEL = 250
LEVEL_TITLES = ["Newcomer", "Explorer", "Apprentice", "Coder", "Builder",
                "Engineer", "Architect", "Wizard", "Master", "Legend"]


# ── helpers ──────────────────────────────────────────────────────────

def current_user():
    uid = session.get("user_id")
    return db.get_user(uid) if uid else None


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


@app.context_processor
def inject_globals():
    user = current_user()
    return {
        "user": user,
        "level": level_info(user["xp"]) if user else None,
        "site_url": app.config["SITE_URL"],
        "now_year": datetime.now(timezone.utc).year,
        "n_lessons": total_lessons(),
        "n_courses": len(COURSES),
        "n_projects": len(PROJECTS),
        "n_project_steps": sum(len(pr["steps"]) for pr in PROJECTS),
        "n_challenges": len(CHALLENGES),
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
        elif db.find_user(username) or db.find_user(email):
            error = "That username or email is already registered."
        else:
            uid = db.create_user(username, email, generate_password_hash(password))
            session["user_id"] = uid
            session.permanent = True
            # Come back to the lesson they were on, so device progress syncs
            # in context instead of dumping them on the dashboard.
            return redirect(safe_next(request.args.get("next"))
                            or url_for("dashboard"))
    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        ident = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = db.find_user(ident)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session.permanent = True
            return redirect(safe_next(request.args.get("next")) or url_for("dashboard"))
        error = "Invalid credentials — check your username and password."
    return render_template("login.html", error=error)


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ── Google Sign-In (OpenID Connect via Authlib) ──────────────────────

def _unique_username(base):
    """Derive an available username from a Google display name / email."""
    base = re.sub(r"[^a-zA-Z0-9_]", "", (base or "user")).lower()[:20] or "user"
    if len(base) < 3:
        base = (base + "user")[:20]
    candidate, n = base, 0
    while db.find_user(candidate):
        n += 1
        suffix = str(n)
        candidate = base[: 24 - len(suffix)] + suffix
    return candidate


@app.get("/auth/google")
def google_login():
    if not google_oauth:
        return redirect(url_for("login"))
    session["oauth_next"] = safe_next(request.args.get("next")) or url_for("dashboard")
    redirect_uri = app.config["SITE_URL"].rstrip("/") + url_for("google_callback")
    return google_oauth.authorize_redirect(redirect_uri)


@app.get("/auth/google/callback")
def google_callback():
    if not google_oauth:
        return redirect(url_for("login"))
    try:
        token = google_oauth.authorize_access_token()
        info = token.get("userinfo") or google_oauth.userinfo()
    except Exception as exc:  # user cancelled or token exchange failed
        app.logger.warning("Google callback failed: %s", exc)
        return redirect(url_for("login"))

    sub = info.get("sub")
    email = (info.get("email") or "").strip()
    if not sub or not email:
        return redirect(url_for("login"))
    avatar = info.get("picture")

    user = db.find_user_by_google(sub)
    if not user:
        existing = db.find_user(email)          # link Google to a prior password account
        if existing:
            db.link_google_to_user(existing["id"], sub, avatar)
            user = db.get_user(existing["id"])
        else:
            username = _unique_username(info.get("name") or email.split("@")[0])
            uid = db.create_google_user(username, email, sub, avatar)
            user = db.get_user(uid)

    session["user_id"] = user["id"]
    session.permanent = True
    award_new_achievements(user)
    return redirect(session.pop("oauth_next", None) or url_for("dashboard"))


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


@app.get("/admin/members/<int:uid>")
@admin_required
def admin_member(uid):
    detail = db.member_detail(uid)
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
    urls = [("", "1.0"), ("/start", "0.9"), ("/courses", "0.9"),
            ("/projects", "0.9"), ("/challenges", "0.8"),
            ("/playground", "0.7"), ("/review", "0.6"), ("/about", "0.5")]
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
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=debug, port=port)
