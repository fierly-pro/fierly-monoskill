# Django

> Load: Django or Django REST Framework projects.
> Pairs with: `platforms/backend.md`, `technologies/languages/python.md`, `security/api.md`, `security/database.md`.

## Defaults

- Settings from environment-specific modules or `django-environ`; never commit production secrets. Keep `DEBUG=False` outside local development.
- Run `python manage.py check --deploy` and address the findings; configure `SECURE_*`, `CSRF_*`, `SESSION_*`, HSTS, and allowed hosts deliberately.
- Use the ORM; avoid raw SQL. If raw SQL is necessary, parameterize it and document why.
- Prevent N+1 queries with `select_related` (FK/one-to-one) and `prefetch_related` (many-to-many/reverse); verify query counts in tests.
- Use `transaction.atomic` for multi-step invariants; keep transactions short.
- Migrations are code: review, test on production-like data, and make them compatible with rolling deploys. Never edit applied migrations.
- DRF: explicit serializers, `permission_classes`, `authentication_classes`, pagination, throttling, and `fields` allowlists. Do not expose models directly.
- Admin: restrict access, use strong auth, avoid exposing sensitive models, and audit changes. Never rely on obscurity.

## Security

- Keep CSRF middleware enabled for cookie-authenticated forms/APIs; use DRF token/session auth deliberately.
- Templates auto-escape; do not use `|safe` or `mark_safe` on untrusted content. Sanitize rich text separately.
- Validate uploads (size, type, storage location); serve user files safely; never execute them.
- Use `django.contrib.auth` password hashers (Argon2/bcrypt) and configure `PASSWORD_HASHERS`; enforce strong passwords and rate-limit login.
- Object-level permissions: filter querysets by the authenticated user/tenant; do not rely on URL obscurity.
- Set secure cookie flags, `SECURE_SSL_REDIRECT`, HSTS, and `X_FRAME_OPTIONS`/CSP as appropriate.
- Do not log secrets/PII; configure `LOGGING` with redaction.

## Testing and operations

- pytest-django or Django `TestCase`; use factories, `APIClient`, and a real test database.
- Test permissions per role/tenant, validation errors, and query counts for hot endpoints.
- Static files via the configured storage/CDN; media storage private by default.
- Use a production WSGI/ASGI server; run migrations as a separate deploy step; collectstatic in the build.
- Health checks, structured logs, error reporting, and graceful restarts.

## Checklist

- [ ] `check --deploy` clean or documented.
- [ ] `DEBUG=False`, allowed hosts, cookies, HSTS configured.
- [ ] Querysets scoped to the user/tenant; admin restricted.
- [ ] Serializers use explicit fields; uploads validated.
- [ ] Migrations reviewed and compatible with rollout.
- [ ] N+1 queries checked on changed endpoints.
