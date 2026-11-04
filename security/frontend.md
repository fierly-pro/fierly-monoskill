# Frontend Security

> Load: browser rendering, client state, CSP, cookies, third-party scripts, or SPAs.
> Pairs with: `security/input.md`, `security/api.md`, `technologies/frameworks/react.md`.

## Rendering and XSS

- Rely on framework escaping; avoid raw HTML sinks (`innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `insertAdjacentHTML`).
- If raw HTML is unavoidable, sanitize with a maintained allowlist library (e.g., DOMPurify) and keep it updated. Prefer server-side sanitization for stored rich text.
- Never build URLs or JavaScript from untrusted strings. Allowlist `http`/`https`; block `javascript:` and unexpected `data:` URIs.
- Do not use `eval`, `new Function`, or string-based timers with untrusted input.
- Use Trusted Types where supported to enforce sinks.

## Content Security Policy

- Start with `default-src 'self'`; add only required sources.
- Prefer nonces or hashes over `'unsafe-inline'`; avoid `'unsafe-eval'`.
- Set `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'none'` (or the intended embedders), `form-action 'self'`.
- Roll out with `Content-Security-Policy-Report-Only`, fix violations, then enforce.
- CSP is defense in depth; it does not replace output encoding.

## Cookies, tokens, and storage

- Prefer `HttpOnly`, `Secure`, `SameSite` cookies for session tokens; JavaScript cannot read them.
- Avoid `localStorage`/`sessionStorage` for long-lived credentials or sensitive PII; XSS can read them.
- Do not store secrets, API keys, or authorization decisions in client state.
- Clear client state on logout and when the session expires.
- Apply CSRF protection to cookie-authenticated state changes (see `security/auth.md`).

## Browser boundaries

- `postMessage`: verify `event.origin` against an allowlist and validate the message shape; never use `*` for sensitive data.
- Iframes: use `sandbox` with the minimum permissions, validate embedders, and set `frame-ancestors`.
- Third-party scripts: prefer none; if required, use SRI, limit CSP sources, review privacy/telemetry, and load asynchronously.
- Service workers: scope narrowly, version caches, and never cache authenticated responses in shared caches.
- Open redirects: validate return URLs against an allowlist.

## Build and delivery

- Never ship secrets or private keys in the bundle; treat all client code as public.
- Disable or protect production source maps unless intentionally public.
- Keep dependencies patched; run SCA on the frontend build.
- Verify the integrity of remote assets (SRI, pinned versions).
- Set security headers at the edge: HSTS, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`, CSP.
- Serve over HTTPS only; avoid mixed content.

## UX versus security

- Client-side validation is for usability; repeat every security-relevant check on the server.
- Do not hide admin actions only with CSS; enforce authorization server-side.
- Error messages should not reveal whether an account/resource exists beyond what the UX requires.
- Accessibility and security both depend on correct semantics; do not disable form protections for convenience.

## Verification

- Attempt XSS in every sink: text, attributes, URLs, rich text, file names, SVG.
- Check CSP violations and confirm the policy is enforced in production.
- Confirm cookies have the expected attributes and session invalidation works.
- Test `postMessage` with a hostile origin and third-party script failure.
- Inspect the production bundle for secrets and source maps.
