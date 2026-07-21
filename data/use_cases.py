"""Concrete outcomes shown on course pages.

These are intentionally product-shaped rather than topic-shaped: learners
should be able to see what a concept unlocks before they start a lesson.
"""

COURSE_USE_CASES = {
    "python-fundamentals": [
        {"icon": "receipt", "title": "Receipt calculator",
         "desc": "Calculate totals, tax, discounts and readable customer receipts."},
        {"icon": "lock", "title": "Login rules",
         "desc": "Validate passwords and decide what each type of user can access."},
        {"icon": "ticket", "title": "Ticket pricing",
         "desc": "Apply age, membership and group discounts with clear business rules."},
        {"icon": "megaphone", "title": "Status messages",
         "desc": "Turn live values into useful alerts, labels and personalised updates."},
    ],
    "data-structures": [
        {"icon": "cart", "title": "Shopping basket",
         "desc": "Model products, quantities, prices and stock using lists and dictionaries."},
        {"icon": "chart", "title": "Survey analyser",
         "desc": "Count responses, remove duplicates and identify the most common answers."},
        {"icon": "graduation", "title": "Student gradebook",
         "desc": "Navigate nested records and calculate results for an entire class."},
        {"icon": "database", "title": "API response explorer",
         "desc": "Safely extract the exact fields you need from real JSON-shaped data."},
    ],
    "functions-oop": [
        {"icon": "truck", "title": "Delivery pricing engine",
         "desc": "Package reusable pricing rules into small, testable functions."},
        {"icon": "bank", "title": "Bank account model",
         "desc": "Keep balances and deposit or withdrawal behaviour together in a class."},
        {"icon": "check", "title": "Reusable validators",
         "desc": "Build functions that check emails, form fields and imported records."},
        {"icon": "gamepad", "title": "Game characters",
         "desc": "Use inheritance and objects for players with different abilities."},
    ],
    "practical-python": [
        {"icon": "folder", "title": "File organiser",
         "desc": "Read, classify and report on files without repetitive manual work."},
        {"icon": "tools", "title": "App configuration",
         "desc": "Load JSON settings and handle missing or invalid values safely."},
        {"icon": "broom", "title": "Data cleanup",
         "desc": "Turn inconsistent text records into clean, dependable information."},
        {"icon": "warning", "title": "Fault-tolerant importer",
         "desc": "Handle broken rows without crashing an entire batch process."},
    ],
    "apis-with-python": [
        {"icon": "cloud", "title": "Weather dashboard",
         "desc": "Read forecast responses and surface the information people need."},
        {"icon": "data", "title": "Inventory API",
         "desc": "Design create, read, update and delete routes for real products."},
        {"icon": "search", "title": "GitHub profile lookup",
         "desc": "Parse nested API responses and handle success or failure states."},
        {"icon": "bell", "title": "Webhook receiver",
         "desc": "Validate incoming events and route each event type correctly."},
    ],
    "automation": [
        {"icon": "chart", "title": "Sales report",
         "desc": "Process CSV exports and calculate revenue and best-selling products."},
        {"icon": "monitor", "title": "Log monitor",
         "desc": "Detect errors, busy endpoints and suspicious patterns in server logs."},
        {"icon": "mail", "title": "Contact extractor",
         "desc": "Find and clean email addresses buried inside unstructured text."},
        {"icon": "calendar", "title": "Deadline planner",
         "desc": "Calculate due dates, overdue work and human-readable schedules."},
    ],
    "python-games": [
        {"icon": "gamepad", "title": "Guessing & dice games",
         "desc": "Turn if/else and loops into playable game rounds with real feedback."},
        {"icon": "spark", "title": "ASCII art generator",
         "desc": "Draw triangles, walls and arrows by turning loop counters into pixels."},
        {"icon": "quiz", "title": "Word puzzle toolkit",
         "desc": "Detect palindromes and flip words with slicing and normalisation."},
        {"icon": "path", "title": "Text adventure engine",
         "desc": "Model a game world as data and walk players through it with one loop."},
    ],
    "algorithms": [
        {"icon": "checklist", "title": "Problem breakdowns",
         "desc": "Turn any vague task into small steps you can code one at a time."},
        {"icon": "search", "title": "Instant lookups",
         "desc": "Find one value among millions in ~20 steps with binary search."},
        {"icon": "layers", "title": "Multi-level sorting",
         "desc": "Order reports by department, then score, then name — in one line."},
        {"icon": "focus", "title": "Performance instincts",
         "desc": "Predict which code will crawl on big data before you ever run it."},
    ],
    "data-analysis": [
        {"icon": "chart", "title": "Honest averages",
         "desc": "Choose mean, median or mode so outliers can't mislead your report."},
        {"icon": "broom", "title": "Messy CSV rescue",
         "desc": "Strip, convert and quarantine bad values without crashing the run."},
        {"icon": "database", "title": "Category totals",
         "desc": "Group revenue, signups or errors by key — pure-Python GROUP BY."},
        {"icon": "trophy", "title": "Top-N leaderboards",
         "desc": "Rank best sellers and slowest pages with sorted, keys and slices."},
    ],
    "expert-python": [
        {"icon": "database", "title": "Streaming data pipeline",
         "desc": "Chain generators to process files bigger than memory, one record at a time."},
        {"icon": "shield", "title": "Retry & caching layers",
         "desc": "Wrap flaky API calls with decorators that retry, time and memoize them."},
        {"icon": "bank", "title": "Safe transactions",
         "desc": "Guarantee commit-or-rollback cleanup with your own context managers."},
        {"icon": "blocks", "title": "A tiny framework",
         "desc": "Use dunders, dataclasses and type hints to design APIs that feel native."},
    ],
}


def get_course_use_cases(course_slug):
    return COURSE_USE_CASES.get(course_slug, [])
