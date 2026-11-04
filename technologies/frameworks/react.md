# React

> Load: React or React-based frameworks (Next.js, Remix, Vite SPA).
> Pairs with: `platforms/web.md`, `security/frontend.md`, `technologies/languages/typescript.md`.

## Defaults

- Function components and hooks. Keep components focused on rendering; move data/business logic into hooks/services.
- Derive state instead of duplicating it. Keep the minimum state; lift it only when shared.
- `useEffect` is for synchronizing with external systems (network, DOM, subscriptions), not for deriving data. Clean up subscriptions, timers, and fetches.
- List keys must be stable and unique (IDs, not array index for reorderable lists).
- Controlled inputs for forms; validate on the server as well.
- Abort in-flight requests on unmount/dependency change; handle race conditions (ignore stale responses).
- Use error boundaries and explicit loading/empty/error states.
- Context for low-frequency global values; do not put rapidly changing state in a broad context.
- Memoize (`memo`, `useMemo`, `useCallback`) only after measuring or for referential stability required by a dependency. Premature memoization adds complexity.

## Framework notes

- **Next.js/Remix:** distinguish server and client code; never import server-only modules into client bundles. Server Components/loaders run on the server; validate params and authorize per request. Use framework caching deliberately and revalidate on writes.
- **SPA:** handle auth redirects, deep links, and refresh; do not assume the client enforces authorization.
- **Strict Mode:** effects run twice in development; make them idempotent and clean up correctly.

## Security and data

- Never trust client-side authorization; the server enforces access.
- Avoid `dangerouslySetInnerHTML`; sanitize rich text with a maintained sanitizer (see `security/frontend.md`).
- Do not store tokens in `localStorage` when HttpOnly cookies work; never store secrets/PII in client state.
- Validate URL params and redirect targets; encode output by context.
- Third-party scripts: minimize, use SRI, and constrain with CSP.

## Performance

- Measure with React Profiler/browser performance tools before optimizing.
- Code-split routes and heavy components; virtualize long lists; avoid unnecessary re-renders of large trees.
- Optimize images/fonts and the critical path; set performance budgets.
- Avoid layout thrash and synchronous heavy work on the main thread.

## Testing

- React Testing Library: test user-visible behavior, not implementation details. Query by role/label.
- Mock network at the boundary (MSW), not the component's own hooks.
- Add a few E2E tests for critical journeys; include accessibility checks.
- Test loading, empty, error, and unauthorized states.

## Checklist

- [ ] Effects have correct dependencies and cleanup.
- [ ] Loading/empty/error/unauthorized states implemented.
- [ ] No raw HTML or secrets on the client.
- [ ] Server-side authorization and validation exist.
- [ ] Accessibility and keyboard paths checked.
- [ ] Performance measured on a representative device.
