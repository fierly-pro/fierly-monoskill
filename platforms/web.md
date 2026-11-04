# Platform: Web

> Load: browser UI, SPA, SSR/SSG, PWA, or design system.
> Pairs with: `platforms/backend.md` for full-stack, `security/frontend.md`, `security/api.md`, `technologies/frameworks/react.md`.

## Architecture defaults

- Choose rendering per route: static for content, server rendering for SEO/first paint, client rendering for highly interactive app shells. Avoid hydrating what can stay static.
- Keep server state and client state separate. Use a server-state library or explicit cache; do not copy server data into global stores without a reason.
- Route-level code splitting; lazy-load heavy widgets; define loading, empty, error, and unauthorized states for every data view.
- Treat URL as state for shareable filters/pagination; validate it like any input.
- Define browser support from analytics and business needs; use progressive enhancement for critical journeys.
- Accessibility is a requirement: semantic HTML, keyboard paths, focus management, labels, contrast, reduced motion, screen-reader checks.

## Non-negotiables

- No secrets, private API keys, or authorization logic in client code — the bundle is public.
- No `innerHTML`/raw HTML with untrusted content; encode by context (see `security/frontend.md`).
- Authorization decisions are enforced by the server, not hidden UI.
- Every image/video has dimensions and alt text where meaningful; avoid layout shift.
- Handle slow/failed networks: timeouts, retries with backoff, offline states, cancellation.
- Do not block the main thread with large parsing/computation; move to a worker.
- Validate and sanitize URL parameters, redirect targets, and postMessage origins.

## Performance

- Measure Core Web Vitals on real devices/networks; set budgets for JS, images, fonts, and third parties.
- Optimize the critical path: server response, render-blocking assets, font loading, image formats/sizes, hydration cost.
- Cache immutable assets with content hashes; use a CDN; define cache invalidation for HTML.
- Audit third-party scripts; each one costs privacy, performance, and supply-chain risk.

## Security

- CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`; see `security/frontend.md`.
- Cookies: `HttpOnly`, `Secure`, `SameSite`; CSRF protection for cookie-auth writes.
- Rich text sanitized with a maintained allowlist sanitizer; URLs restricted to safe schemes.
- Do not cache authenticated/personal responses in shared caches.
- Subresource integrity for remote scripts; pin dependencies.

## Testing and release

- Unit/component tests for logic and states; integration for data fetching; a few E2E journeys on critical paths.
- Test keyboard navigation, focus, screen-reader semantics, zoom, and reduced motion.
- Cross-browser/device smoke tests for supported targets; visual regression where the UI is stable.
- Verify headers and caching in the deployed environment, not only locally.
- Release with atomic asset uploads, cache-busted filenames, and a rollback path for HTML/config.

## Checklist

- [ ] Loading/empty/error/unauthorized states implemented.
- [ ] Forms validate on the client for UX and on the server for security.
- [ ] No secrets or sensitive data in the bundle or source maps.
- [ ] CSP and security headers verified in production.
- [ ] Accessibility and keyboard paths checked.
- [ ] Performance budget measured on a representative device.
