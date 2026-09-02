"""Supabase Auth (GoTrue) over its REST API.

Written against `requests`, already a dependency here, rather than
`supabase-py`: that package pulls in postgrest, storage, realtime and
functions clients to make the handful of HTTP calls below, and is built
around a stateful client with its own session storage that would fight
Flask's signed cookie. This mirrors mailer.py — module-level config, one
timeout, no exceptions escaping into routes.

Every call returns a (data, error) pair instead of raising, so routes stay
flat and a network blip reads the same as a rejected password. `error` is a
short string safe to show a person; the detail goes to the log.

The service-role key bypasses Row Level Security and must never reach a
browser. Only _admin_headers() uses it, and only for the two admin calls at
the bottom of this file.
"""

import base64
import hashlib
import os
import secrets

import requests

TIMEOUT = 15


def _env(name, default=""):
    # Dashboards store a trailing newline when a value is pasted, and it is
    # invisible in their UI — the same trap that broke SITE_URL for OAuth.
    return os.environ.get(name, default).strip()


def base_url():
    return _env("SUPABASE_URL").rstrip("/")


def is_configured():
    return bool(base_url() and _env("SUPABASE_ANON_KEY"))


def admin_is_configured():
    return bool(base_url() and _env("SUPABASE_SERVICE_ROLE_KEY"))


def _url(path):
    return "%s/auth/v1%s" % (base_url(), path)


def _headers(access_token=None):
    key = _env("SUPABASE_ANON_KEY")
    h = {"apikey": key, "Content-Type": "application/json"}
    # GoTrue wants the user's own token when acting on their record, and the
    # anon key otherwise.
    h["Authorization"] = "Bearer %s" % (access_token or key)
    return h


def _admin_headers():
    key = _env("SUPABASE_SERVICE_ROLE_KEY")
    return {"apikey": key, "Authorization": "Bearer %s" % key,
            "Content-Type": "application/json"}


def _request(method, path, *, headers=None, json=None, params=None, label=""):
    """Returns (data, error). Never raises."""
    if not is_configured():
        return None, "Sign-in is not configured."
    try:
        r = requests.request(method, _url(path), headers=headers or _headers(),
                             json=json, params=params, timeout=TIMEOUT)
    except Exception as exc:
        print("[auth] %s errored: %r" % (label or path, exc))
        return None, "Could not reach the sign-in service. Try again."

    if r.status_code >= 400:
        detail = r.text[:300]
        print("[auth] %s failed: %s %s" % (label or path, r.status_code, detail))
        try:
            body = r.json()
        except Exception:
            body = {}
        # GoTrue spells the human-readable reason differently by endpoint.
        msg = (body.get("msg") or body.get("error_description")
               or body.get("message") or body.get("error") or "")
        return None, msg or "That did not work. Please try again."

    if not r.content:
        return {}, None
    try:
        return r.json(), None
    except Exception:
        return {}, None


# ── password ──────────────────────────────────────────────────────────

def sign_up(email, password, username=None, display_name=None):
    """Create an account. With email confirmation off GoTrue returns a
    session here; with it on the session is null and the caller must not
    assume the person is logged in."""
    meta = {}
    if username:
        meta["username"] = username
    if display_name:
        meta["full_name"] = display_name
    return _request("POST", "/signup", label="signup",
                    json={"email": email.strip().lower(), "password": password,
                          "data": meta})


def sign_in(email, password):
    return _request("POST", "/token", label="signin",
                    params={"grant_type": "password"},
                    json={"email": email.strip().lower(), "password": password})


def refresh(refresh_token):
    return _request("POST", "/token", label="refresh",
                    params={"grant_type": "refresh_token"},
                    json={"refresh_token": refresh_token})


def get_user(access_token):
    return _request("GET", "/user", headers=_headers(access_token), label="get_user")


def update_password(access_token, new_password):
    return _request("PUT", "/user", headers=_headers(access_token),
                    json={"password": new_password}, label="update_password")


def send_recovery(email, redirect_to=None):
    params = {"redirect_to": redirect_to} if redirect_to else None
    return _request("POST", "/recover", params=params, label="recover",
                    json={"email": email.strip().lower()})


def sign_out(access_token):
    if not access_token:
        return {}, None
    return _request("POST", "/logout", headers=_headers(access_token), label="logout")


# ── OAuth (PKCE) ──────────────────────────────────────────────────────
# PKCE returns the code as a ?code= query parameter, which the server can
# read. The implicit flow puts it in the URL fragment, which never reaches
# Flask at all — so PKCE is the only flow that works for a server-rendered
# app without JavaScript shuttling the token back.

def make_verifier():
    return secrets.token_urlsafe(64)[:96]


def challenge_for(verifier):
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def oauth_url(provider, redirect_to, code_challenge):
    from urllib.parse import urlencode
    q = urlencode({"provider": provider, "redirect_to": redirect_to,
                   "flow_type": "pkce", "code_challenge": code_challenge,
                   "code_challenge_method": "s256"})
    return "%s?%s" % (_url("/authorize"), q)


def exchange_code(auth_code, code_verifier):
    return _request("POST", "/token", label="pkce_exchange",
                    params={"grant_type": "pkce"},
                    json={"auth_code": auth_code, "code_verifier": code_verifier})


# ── admin (service-role key — never expose to a browser) ──────────────

def admin_create_user(email, password=None, email_confirm=True, meta=None):
    if not admin_is_configured():
        return None, "Admin API is not configured."
    body = {"email": email.strip().lower(), "email_confirm": email_confirm}
    if password:
        body["password"] = password
    if meta:
        body["user_metadata"] = meta
    return _request("POST", "/admin/users", headers=_admin_headers(),
                    json=body, label="admin_create_user")


def admin_delete_user(user_id):
    if not admin_is_configured():
        return None, "Admin API is not configured."
    return _request("DELETE", "/admin/users/%s" % user_id,
                    headers=_admin_headers(), label="admin_delete_user")
