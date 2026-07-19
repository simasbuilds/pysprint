"""PySprint — an interactive Python learning platform.

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
from data.lesson_extras import get_extras
from data.projects import PROJECTS, get_project
from data.use_cases import get_course_use_cases
from data.walkthroughs import get_walkthrough

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["SITE_URL"] = os.environ.get("SITE_URL", "http://127.0.0.1:5000")

db.init_db()

XP_PER_LEVEL = 250
LEVEL_TITLES = ["Newcomer", "Explorer", "Apprentice", "Coder", "Builder",
                "Engineer", "Architect", "Wizard", "Master", "Legend"]


# ── helpers ──────────────────────────────────────────────────────────

def current_user():
    uid = session.get("user_id")
    return db.get_user(uid) if uid else None


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            if request.path.startswith("/api/"):
                return jsonify({"error": "login_required"}), 401
            return redirect(url_for("login", next=request.path))
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
    }


# ── pages ────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return render_template("index.html", courses=COURSES,
                           projects=PROJECTS,
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
    return render_template("challenge.html", ch=ch, done=done)


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
            return redirect(url_for("dashboard"))
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
            return redirect(request.args.get("next") or url_for("dashboard"))
        error = "Invalid credentials — check your username and password."
    return render_template("login.html", error=error)


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


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


@app.get("/api/me")
def api_me():
    user = current_user()
    if not user:
        return jsonify({"logged_in": False})
    return jsonify({"logged_in": True, "username": user["username"],
                    "xp": user["xp"], "streak": user["streak"],
                    "level": level_info(user["xp"])})


# ── SEO ──────────────────────────────────────────────────────────────

@app.get("/sitemap.xml")
def sitemap():
    base = app.config["SITE_URL"].rstrip("/")
    today = date.today().isoformat()
    urls = [("", "1.0"), ("/courses", "0.9"), ("/projects", "0.9"),
            ("/challenges", "0.8"),
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
        f"User-agent: *\nAllow: /\nDisallow: /dashboard\nDisallow: /api/\n"
        f"Sitemap: {base}/sitemap.xml\n",
        mimetype="text/plain")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=debug, port=port)
