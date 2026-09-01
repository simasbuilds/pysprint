"""Transactional email.

Sent over Resend's HTTP API with `requests`, which is already a dependency
for Google sign-in — a dedicated SMTP client would add a package and a
connection pool for the handful of messages this app sends.

Everything here degrades to a no-op when RESEND_API_KEY is unset, so local
development and any deploy without mail configured keep working: signing up
must not fail because a welcome email could not go out.
"""

import os
import threading

import requests

API = "https://api.resend.com/emails"
TIMEOUT = 10


def _env(name, default=""):
    # Dashboards store a trailing newline when a value is pasted, and it is
    # invisible in their UI — the same trap that broke SITE_URL for OAuth.
    return os.environ.get(name, default).strip()


def is_configured():
    return bool(_env("RESEND_API_KEY"))


def _post(payload, key):
    try:
        r = requests.post(
            API,
            json=payload,
            headers={"Authorization": "Bearer %s" % key},
            timeout=TIMEOUT,
        )
        if r.status_code >= 400:
            print("[mail] %s failed: %s %s" % (payload.get("subject"), r.status_code, r.text[:200]))
    except Exception as exc:  # never surface a mail failure to the visitor
        print("[mail] %s errored: %r" % (payload.get("subject"), exc))


def send(to, subject, html, text=None):
    """Queue one message. Returns True if it was handed to a sender thread.

    Fires on a daemon thread: Resend's API answers in a few hundred
    milliseconds, and that is time a person should not spend watching a
    spinner on the page that just created their account.
    """
    key = _env("RESEND_API_KEY")
    if not key or not to:
        return False
    payload = {
        "from": _env("MAIL_FROM") or "LearnWithPython <hello@learnwithpython.com>",
        "to": [to],
        "subject": subject,
        "html": html,
    }
    if text:
        payload["text"] = text
    threading.Thread(target=_post, args=(payload, key), daemon=True).start()
    return True
