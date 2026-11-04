# TypeScript

> Load: TypeScript or modern JavaScript codebases.
> Pairs with: `platforms/web.md` or `platforms/backend.md`, `security/input.md`.

## Defaults

- Enable `strict`, `noUncheckedIndexedAccess`, `noImplicitOverride`, and `noFallthroughCasesInSwitch`. Avoid weakening the config to silence errors.
- Type the boundaries: parse `unknown` from network/storage/env into domain types once (Zod, Valibot, or hand-written guards). A type assertion is not validation.
- Use discriminated unions for state machines and API results; exhaustive `switch` with `never` checks.
- Prefer `readonly`, `as const`, and immutable updates. Use `satisfies` to validate object shapes without widening.
- Keep one module system (ESM preferred); match the project's runtime and bundler. Do not mix default/named export styles inconsistently.
- `async` functions must handle rejection: `await`, `return`, or an explicit `.catch`. Never leave a floating promise.
- Avoid `any`; use `unknown` + narrowing, generics, or a precise union. `@ts-expect-error` needs a comment and a removal plan.
- Handle `null`/`undefined` explicitly; do not use non-null assertions on external data.

## Runtime and tooling

- Node version from `.nvmrc`/`engines`; use the project's package manager and lockfile.
- Format/lint with the configured tools (Prettier/ESLint/Biome); do not reformat unrelated files.
- Tests: Vitest/Jest/Node test runner; test behavior through public APIs. Mock at the boundary (HTTP, clock), not the module under test.
- Build with the project's bundler/`tsc`; verify emitted paths, source maps, and ESM/CJS interop.

## Security

- Never embed secrets or privileged keys in client code; all bundled code is public.
- Validate external data at runtime; TypeScript types disappear at runtime.
- Guard against prototype pollution when merging user objects: reject `__proto__`, `constructor`, `prototype`, or use null-prototype objects/maps.
- Avoid `eval`, `new Function`, and dynamic `require` with user input.
- Sanitize/encode at the sink (DOM, SQL, shell); see `security/input.md`.
- Pin dependencies, review install scripts, and keep the lockfile committed.

## Common pitfalls

- `JSON.parse` returns `any` — validate it.
- `Object.keys`/array indexing under `noUncheckedIndexedAccess` may be `undefined`; handle it.
- `Array.sort` mutates; copy first if the source is shared.
- `==` performs coercion; use `===` (except explicit `== null` checks).
- `setTimeout`/`setInterval` drift and leaks; clear timers and abort work on unmount/shutdown.
- Dates/time zones: store UTC ISO strings or epoch, format at the edge; avoid parsing ambiguous local strings.

## Checklist

- [ ] Strict types at boundaries; no unvalidated `any`.
- [ ] Async errors and cancellations handled.
- [ ] Tests cover success, denial, and failure paths.
- [ ] No secrets in the bundle; external input validated and encoded.
- [ ] Lockfile and toolchain versions pinned.
