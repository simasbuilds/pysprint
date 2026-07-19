"""Achievement definitions. `check` receives a stats dict and returns bool.

stats keys: lessons_done, courses_done (set of slugs), challenges_done,
xp, streak, quizzes_perfect
"""

ACHIEVEMENTS = [
    {"id": "first-steps", "icon": "👣", "title": "First Steps",
     "desc": "Complete your first lesson.",
     "check": lambda s: s["lessons_done"] >= 1},
    {"id": "getting-warm", "icon": "🔥", "title": "Getting Warm",
     "desc": "Complete 5 lessons.",
     "check": lambda s: s["lessons_done"] >= 5},
    {"id": "dedicated", "icon": "💪", "title": "Dedicated Learner",
     "desc": "Complete 15 lessons.",
     "check": lambda s: s["lessons_done"] >= 15},
    {"id": "completionist", "icon": "🏆", "title": "Completionist",
     "desc": "Complete every lesson on PySprint.",
     "check": lambda s: s["lessons_done"] >= s["total_lessons"]},

    {"id": "fundamentals-master", "icon": "🐍", "title": "Fundamentals Master",
     "desc": "Finish the Python Fundamentals course.",
     "check": lambda s: "python-fundamentals" in s["courses_done"]},
    {"id": "data-wrangler", "icon": "📦", "title": "Data Wrangler",
     "desc": "Finish the Data Structures course.",
     "check": lambda s: "data-structures" in s["courses_done"]},
    {"id": "architect", "icon": "⚙️", "title": "Software Architect",
     "desc": "Finish the Functions & OOP course.",
     "check": lambda s: "functions-oop" in s["courses_done"]},
    {"id": "pragmatist", "icon": "🛠️", "title": "The Pragmatist",
     "desc": "Finish the Practical Python course.",
     "check": lambda s: "practical-python" in s["courses_done"]},
    {"id": "api-builder", "icon": "🔌", "title": "API Builder",
     "desc": "Finish the APIs with Python course.",
     "check": lambda s: "apis-with-python" in s["courses_done"]},
    {"id": "automator", "icon": "🤖", "title": "The Automator",
     "desc": "Finish the Automation & Real-World Python course.",
     "check": lambda s: "automation" in s["courses_done"]},

    {"id": "challenger", "icon": "⚔️", "title": "Challenger",
     "desc": "Solve your first arena challenge.",
     "check": lambda s: s["challenges_done"] >= 1},
    {"id": "gladiator", "icon": "🛡️", "title": "Gladiator",
     "desc": "Solve 5 arena challenges.",
     "check": lambda s: s["challenges_done"] >= 5},
    {"id": "arena-legend", "icon": "👑", "title": "Arena Legend",
     "desc": "Solve all 10 arena challenges.",
     "check": lambda s: s["challenges_done"] >= 10},

    {"id": "xp-500", "icon": "⭐", "title": "Rising Star",
     "desc": "Earn 500 XP.",
     "check": lambda s: s["xp"] >= 500},
    {"id": "xp-1000", "icon": "🌟", "title": "Shooting Star",
     "desc": "Earn 1,000 XP.",
     "check": lambda s: s["xp"] >= 1000},
    {"id": "xp-2000", "icon": "💫", "title": "Supernova",
     "desc": "Earn 2,000 XP.",
     "check": lambda s: s["xp"] >= 2000},

    {"id": "streak-3", "icon": "📅", "title": "Habit Forming",
     "desc": "Learn 3 days in a row.",
     "check": lambda s: s["streak"] >= 3},
    {"id": "streak-7", "icon": "🗓️", "title": "Unstoppable",
     "desc": "Learn 7 days in a row.",
     "check": lambda s: s["streak"] >= 7},
]


def evaluate(stats, already_earned):
    """Return the list of newly earned achievement dicts."""
    new = []
    for a in ACHIEVEMENTS:
        if a["id"] not in already_earned and a["check"](stats):
            new.append(a)
    return new
