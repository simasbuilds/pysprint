"""Achievement definitions. `check` receives a stats dict and returns bool.

stats keys: lessons_done, courses_done (set of slugs), challenges_done,
xp, streak, quizzes_perfect
"""

ACHIEVEMENTS = [
    {"id": "first-steps", "icon": "flag", "title": "First Steps",
     "desc": "Complete your first lesson.",
     "check": lambda s: s["lessons_done"] >= 1},
    {"id": "getting-warm", "icon": "flame", "title": "Getting Warm",
     "desc": "Complete 5 lessons.",
     "check": lambda s: s["lessons_done"] >= 5},
    {"id": "dedicated", "icon": "medal", "title": "Dedicated Learner",
     "desc": "Complete 15 lessons.",
     "check": lambda s: s["lessons_done"] >= 15},
    {"id": "completionist", "icon": "trophy", "title": "Completionist",
     "desc": "Complete every lesson on PySprint.",
     "check": lambda s: s["lessons_done"] >= s["total_lessons"]},

    {"id": "fundamentals-master", "icon": "terminal", "title": "Fundamentals Master",
     "desc": "Finish the Python Fundamentals course.",
     "check": lambda s: "python-fundamentals" in s["courses_done"]},
    {"id": "data-wrangler", "icon": "layers", "title": "Data Wrangler",
     "desc": "Finish the Data Structures course.",
     "check": lambda s: "data-structures" in s["courses_done"]},
    {"id": "architect", "icon": "nodes", "title": "Software Architect",
     "desc": "Finish the Functions & OOP course.",
     "check": lambda s: "functions-oop" in s["courses_done"]},
    {"id": "pragmatist", "icon": "wrench", "title": "The Pragmatist",
     "desc": "Finish the Practical Python course.",
     "check": lambda s: "practical-python" in s["courses_done"]},
    {"id": "api-builder", "icon": "plug", "title": "API Builder",
     "desc": "Finish the APIs with Python course.",
     "check": lambda s: "apis-with-python" in s["courses_done"]},
    {"id": "automator", "icon": "robot", "title": "The Automator",
     "desc": "Finish the Automation & Real-World Python course.",
     "check": lambda s: "automation" in s["courses_done"]},

    {"id": "challenger", "icon": "swords", "title": "Challenger",
     "desc": "Solve your first arena challenge.",
     "check": lambda s: s["challenges_done"] >= 1},
    {"id": "gladiator", "icon": "shield", "title": "Gladiator",
     "desc": "Solve 5 arena challenges.",
     "check": lambda s: s["challenges_done"] >= 5},
    {"id": "arena-legend", "icon": "crown", "title": "Arena Legend",
     "desc": "Solve 10 arena challenges.",
     "check": lambda s: s["challenges_done"] >= 10},
    {"id": "arena-perfect", "icon": "burst", "title": "Undefeated",
     "desc": "Solve every arena challenge.",
     "check": lambda s: s["challenges_done"] >= s.get("total_challenges", 99)},

    {"id": "xp-500", "icon": "star", "title": "Rising Star",
     "desc": "Earn 500 XP.",
     "check": lambda s: s["xp"] >= 500},
    {"id": "xp-1000", "icon": "star-double", "title": "Shooting Star",
     "desc": "Earn 1,000 XP.",
     "check": lambda s: s["xp"] >= 1000},
    {"id": "xp-2000", "icon": "burst", "title": "Supernova",
     "desc": "Earn 2,000 XP.",
     "check": lambda s: s["xp"] >= 2000},

    {"id": "builder", "icon": "hammer", "title": "First Build",
     "desc": "Complete your first real-life project.",
     "check": lambda s: s.get("projects_done", 0) >= 1},
    {"id": "shipper", "icon": "rocket", "title": "Shipper",
     "desc": "Complete every real-life project.",
     "check": lambda s: s.get("projects_done", 0) >= s.get("total_projects", 99)},

    {"id": "architect-real", "icon": "database", "title": "Systems Thinker",
     "desc": "Finish an Advanced real-life project.",
     "check": lambda s: s.get("advanced_projects_done", 0) >= 1},

    {"id": "streak-3", "icon": "calendar", "title": "Habit Forming",
     "desc": "Learn 3 days in a row.",
     "check": lambda s: s["streak"] >= 3},
    {"id": "streak-7", "icon": "calendar-check", "title": "Unstoppable",
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
