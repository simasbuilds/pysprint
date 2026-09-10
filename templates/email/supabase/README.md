# Supabase Auth email templates

Paste these into **Supabase Dashboard → Authentication → Emails → Templates**.
They are not rendered by this app — Supabase sends them — so they live here
only as the source of truth for what was pasted.

| File | Supabase template | Sent when |
|---|---|---|
| `recovery.html` | Reset Password | someone uses `/forgot` |
| `confirm_signup.html` | Confirm signup | only if "Confirm email" is turned on |
| `magic_link.html` | Magic Link | only if passwordless sign-in is enabled |

With `mailer_autoconfirm` on — the current setting — **only `recovery.html`
is ever sent.** The other two are here so the branding already exists if you
change that later.

## Why the markup looks twenty years old

Email clients are not browsers.

- **Tables, not flexbox or grid.** Outlook renders through Word's engine.
- **Inline styles only.** Gmail strips most of `<head>`.
- **Literal hex, no CSS variables.** Nothing resolves them.
- **600px width.** The long-standing safe maximum.

## The `{{ .ConfirmationURL }}` tags

Those are Go template tags that Supabase substitutes server-side. They are
**not** Jinja and must be left exactly as written. Each template uses it
twice: once on the button, once as a copy-paste fallback, because some
clients mangle button hrefs.

## Deliverability

Supabase's built-in SMTP is rate-limited and shared, which hurts inbox
placement. Point it at the same Resend domain the welcome email uses:
**Authentication → Emails → SMTP Settings**. Then every message comes from
a domain with your SPF and DKIM records on it.
