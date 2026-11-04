# Authentication and Authorization

> Load: login, registration, sessions, tokens, passwords, permissions, roles, admin, SSO.
> Pairs with: `security/api.md`, `security/input.md`, `security/database.md`, `security/native.md` for mobile/desktop storage.

## Passwords

- Hash with Argon2id (preferred), bcrypt, or scrypt using current parameters. Never use MD5, SHA-1/256, or reversible encryption.
- Use a unique salt per password (handled by the algorithm); consider a server-side pepper in a secret manager.
- Enforce minimum length (≥12), allow long passphrases, do not impose composition rules, and block known-breached passwords.
- Rate-limit attempts per account and per IP; add exponential backoff and alerting. Return generic errors to prevent enumeration.
- Password reset: random single-use token, short expiry, stored hashed, bound to the user, invalidates sessions on use. Do not reveal whether an account exists.
- Support MFA for sensitive accounts; prefer TOTP/WebAuthn over SMS. Rate-limit and single-use every OTP.

## Sessions

- Generate at least 128 bits of cryptographic randomness; never derive session IDs from user data.
- Cookies: `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict`, scoped `Path`, `__Host-` prefix where possible.
- Rotate the session ID on login and privilege change; invalidate server-side on logout and password reset.
- Enforce idle and absolute timeouts; provide a "log out all devices" path.
- Store server-side sessions in a shared store for multi-instance deployments; protect the store.
- Do not put sensitive data in client-readable cookies. Avoid `localStorage` for tokens when an HttpOnly cookie works.

## Tokens (JWT and opaque)

- Prefer short-lived access tokens plus rotating refresh tokens. Define revocation; stateless JWTs cannot be un-issued without a denylist or short TTL.
- Verify signature with an allowlisted algorithm; reject `none` and algorithm confusion. Validate `iss`, `aud`, `exp`, `nbf`, and clock skew.
- Keep signing keys in a KMS/secret manager; support rotation with key IDs.
- Never store secrets, passwords, or excessive PII in token claims; they are readable by the client.
- Do not accept tokens from query strings or logs; use headers or secure cookies.
- For OAuth/OIDC: authorization code + PKCE, exact redirect URI matching, `state`, `nonce`, issuer/audience validation. Do not use implicit flow. Request minimum scopes.

## Authorization

- **Deny by default.** Every endpoint/resource declares its policy; public access is explicit.
- Enforce **server-side**, at the resource, on every request — not just in the UI or router.
- **Object-level authorization** is mandatory: verify the caller owns or may access this specific record (prevents IDOR). Do not trust an ID from the client.
- Tenant isolation: derive tenant from the authenticated context, not from a request parameter; enforce in the query or row-level security.
- Centralize policy where practical; keep checks close to the data access for defense in depth.
- Roles are coarse; use attributes/relationships for fine-grained cases. Avoid role explosion.
- Admin actions: separate surface, stronger authentication, audit logging, and least privilege.
- Test with two accounts and multiple tenants: horizontal and vertical privilege escalation.

## CSRF, CORS, and SSRF

- **CSRF:** use `SameSite` cookies plus a per-session token for state-changing requests, or a custom header with strict CORS. Do not rely on `Origin` alone for legacy clients.
- **CORS is not authentication.** Never use it to protect data; it only controls browser read access. Do not reflect arbitrary origins or combine wildcard origins with credentials.
- **SSRF:** for user-supplied URLs, allowlist schemes/hosts, resolve and block private/link-local/metadata ranges, disable redirects or re-validate each hop, and route through an egress proxy with logging.
- Validate redirect targets after login/logout to prevent open redirects.

## Rate limiting and abuse

- Apply per identity, IP, tenant, and endpoint as appropriate. Protect login, registration, reset, OTP, search, export, and expensive operations.
- Use a shared store (Redis) for multi-instance limits; define the window and burst behavior.
- Cap request size, pagination size, and concurrent sessions.
- Alert on credential stuffing patterns; consider breached-password checks and device/session visibility.

## Verification

- Attempt IDOR with a second account, privilege escalation with a lower role, session fixation, token replay after logout, expired-token acceptance, CSRF on state-changing endpoints, and SSRF against metadata addresses.
- Confirm errors do not reveal account existence, stack traces, or internal identifiers.
- Add regression tests for authorization checks at the data layer.
