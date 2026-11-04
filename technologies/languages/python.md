# Python

> Load: Python applications, services, scripts, or data pipelines.
> Pairs with: `platforms/backend.md`, `security/input.md`, `technologies/frameworks/fastapi.md`/`django.md`.

## Defaults

- Use the project's supported Python version (3.11+ for new work when possible); declare it in `pyproject.toml` and CI.
- Manage environments with `uv`, Poetry, or the project's existing tool; never install into the system interpreter.
- Type hints on public functions and boundaries; run mypy or pyright in CI. Use `from __future__ import annotations` only when the project targets older versions.
- Format/lint with Ruff (or the configured Black/Flake8/isort); keep configuration in `pyproject.toml`.
- Prefer `pathlib.Path`, f-strings, dataclasses/Pydantic models, and context managers (`with`).
- Use timezone-aware `datetime` (`datetime.now(timezone.utc)`); never use naive local time for stored timestamps.
- Avoid mutable default arguments (`def f(x=[])`); use `None` and create inside.

## Errors and structure

- Catch specific exceptions; never `except Exception: pass`. Preserve the cause with `raise ... from err`.
- Define domain exceptions at module boundaries; translate to API errors at the edge.
- Avoid import-time side effects and global mutable state; use explicit initialization.
- Keep `__init__.py` free of heavy logic; respect package boundaries.
- Use `asyncio` for I/O concurrency; never call blocking I/O or `time.sleep` inside an async function. Use `asyncio.to_thread` for unavoidable blocking calls.
- Cancel tasks on shutdown; use timeouts (`asyncio.timeout`) around external calls.

## Dependencies and packaging

- Declare dependencies in `pyproject.toml`; pin an application with a lockfile; libraries use compatible ranges.
- Review transitive dependencies and install scripts; run `pip-audit`/OSV scanning.
- Build wheels/sdist with the project's backend; include only intended files; verify the package installs in a clean environment.

## Security

- Never `pickle`, `marshal`, or unsafe-`yaml.load` untrusted data. Use JSON with validation or `yaml.safe_load`.
- Avoid `eval`/`exec` on user input; avoid `subprocess` with `shell=True` and interpolation. Pass argument lists.
- Parameterize SQL; treat ORM raw SQL as untrusted string handling.
- Do not log secrets/PII; redact exception payloads.
- Use `secrets` for tokens, not `random`. Hash passwords with Argon2id/bcrypt (see `security/auth.md`).
- Validate file paths and uploads; resolve and confine to an allowed root.

## Testing

- pytest with fixtures; parametrize edge cases; `tmp_path` for files; monkeypatch at the boundary.
- Test async code with `pytest-asyncio` or `anyio`; avoid real sleeps.
- Integration tests against real DB/queue via containers; migrations tested separately.
- Measure coverage on changed code, not as a target.

## Checklist

- [ ] Types and lint pass in CI.
- [ ] Async paths do not block the event loop.
- [ ] Exceptions are specific and preserve context.
- [ ] Untrusted data is parsed safely; no pickle/eval/shell interpolation.
- [ ] Lockfile and supported Python version declared.
