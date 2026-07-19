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
}


def get_course_use_cases(course_slug):
    return COURSE_USE_CASES.get(course_slug, [])
