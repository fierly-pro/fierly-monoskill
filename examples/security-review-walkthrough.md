# Example: Session Authentication Review

**Task:** “Review our session authentication and admin authorization. Cookies + React frontend. Tell me what is exploitable.”

## Routing

`core/engineering.md`, `workflows/security-review.md`, `security/baseline.md`, `security/auth.md`, `security/api.md`, `security/frontend.md`, `security/testing.md`, `platforms/web.md`, `platforms/backend.md`.

No native/infrastructure modules: the review scope is the web session and authorization path, not the cluster.

## Threat model excerpt

| Asset | Actor | Boundary | Threat |
|---|---|---|---|
| Session cookie | Anonymous internet | Browser → API | Theft via XSS, fixation, CSRF |
| Admin actions | Authenticated user | API → admin routes | Vertical privilege escalation |
| Order data | Tenant user | API → DB | IDOR / cross-tenant read |

## Findings (illustrative)

| Severity | Location | Finding | Fix |
|---|---|---|---|
| High | `api/orders.py:88` | Order fetched by ID without tenant filter | Derive tenant from session; scope query; add two-tenant test |
| High | `auth/session.py:41` | Session ID not rotated after login | Regenerate on authentication; invalidate old ID |
| Medium | `web/src/api.ts:12` | Session token also mirrored to `localStorage` | Remove; rely on HttpOnly cookie |
| Medium | `api/auth.py:120` | No rate limit on reset requests | Per-account/IP limit + generic response |
| Low | `api/main.py:30` | `X-Frame-Options` missing | Set `frame-ancestors 'none'` via CSP |

## Verification

- Two accounts, two tenants: attempt `GET /orders/{id}` across tenants → expect `404/403`, not data.
- Fixation: capture pre-login cookie, log in, confirm the old ID is invalid.
- CSRF: state-changing request from a hostile origin → rejected.
- Logout: replay the old cookie → rejected.
- XSS: confirm no token is readable from JavaScript storage.

## Gate decision

**FAIL** until both High findings are fixed and retested. Medium findings get owners and a deadline; Low is tracked. The decision is based on manual abuse cases, not on a scanner run.

## Report shape

```text
Verdict: request changes (2 high, 2 medium, 1 low)
Evidence: file:line, reproduction, two-account tests
Fixed/retested: pending
Residual risk: admin audit logging not verified; staging WAF not tested
```
