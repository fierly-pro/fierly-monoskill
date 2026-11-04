# Example: Login Rate Limiting

**Task:** “Add rate limiting to the login endpoint. We use React, FastAPI, PostgreSQL, and Redis is already deployed.”

## Routing

| Level | Loaded | Why |
|---|---|---|
| Core | `core/engineering.md` | Always |
| Workflow | `workflows/feature.md` | Behavior change in an existing system |
| Platforms | `platforms/backend.md` | Server-side control |
| Technologies | `technologies/frameworks/fastapi.md`, `technologies/databases/redis.md` | Framework implementation + shared counter store |
| Security | `security/baseline.md`, `security/auth.md`, `security/api.md` | Credential endpoint + API abuse |

Not loaded: web/React (no UI change), PostgreSQL (no schema change), mobile/infrastructure modules. The React client is out of scope; the server enforces the limit.

## Plan

1. Inspect the login route, auth dependency, existing middleware, Redis client, and test setup.
2. Define the policy: per-account and per-IP windows, burst allowance, `429` response with `Retry-After`, generic error message, metrics.
3. Implement with an atomic Redis operation (Lua or `INCR` + `EXPIRE`) and a local fallback that fails closed for login.
4. Add tests: under limit, over limit, window reset, Redis unavailable, account enumeration resistance, successful login unaffected.
5. Verify with the project's test/lint/typecheck commands and a manual burst against a local server.
6. Report the policy, evidence, and operational caveats.

## Security checks

- Limit is enforced server-side, before password verification.
- Keys are derived from normalized account + trusted client IP, not raw user input.
- No account-existence leak in the `429`/error response.
- Redis failure does not silently disable protection.
- Successful and failed attempts are counted; logs contain no credentials.
- Metrics/alerts exist for sustained `429` spikes.

## Verification

```bash
pytest tests/api/test_login_rate_limit.py -q
pytest -q
ruff check .
mypy app
```

Manual: send N+1 requests within the window; confirm `429` and `Retry-After`; confirm a valid login still succeeds after the window.

## Report shape

```text
Outcome:       login limited per account and IP; 429 with Retry-After
Changes:       auth/rate_limit.py, login route, Redis client config, tests
Verification:  pytest (42 passed), ruff, mypy; manual burst confirmed
Security:      fail-closed on Redis outage; no enumeration; credentials not logged
Assumptions:   proxy sets X-Forwarded-For only from trusted edge
Next steps:    dashboard alert for 429 spikes; tune limits after baseline
```
