# Swift

> Load: iOS, macOS, or Swift server/CLI code.
> Pairs with: `platforms/ios.md` or `platforms/macos.md`, `security/native.md`.

## Defaults

- Prefer `let`, value types (`struct`/`enum`), and protocols for boundaries. Use classes for identity/lifetime.
- Handle optionals with `guard let`/`if let`/`??`; avoid force unwrap (`!`) and `try!` on production paths.
- Use exhaustive `switch` over enums; `@unknown default` for non-frozen system enums.
- Errors: `throws` + typed errors for expected failures; `Result` at async boundaries; never silently discard errors.
- Concurrency: `async`/`await`, structured task groups, actors for shared mutable state, `@MainActor` for UI. Respect cancellation (`Task.checkCancellation`).
- `Sendable` correctness matters under strict concurrency; do not silence warnings with `@unchecked Sendable` unless the invariants are documented.
- SwiftUI: single source of truth, `@State` for local, `@Observable`/`@StateObject` for owned models, `@Binding` for child mutation; avoid business logic in views.
- Swift Package Manager for dependencies; pin versions; minimize transitive packages.

## Testing and tooling

- Swift Testing or XCTest; UI tests for critical journeys; async tests with structured concurrency.
- Inject clocks, network clients, and persistence for determinism; avoid sleeps.
- Use `swift-format`/SwiftLint per project config; keep warnings clean.
- Test on the minimum OS and current OS; use sanitizers (ASan/TSan) for low-level code.

## Security

- Tokens in Keychain; never in `UserDefaults`, files, or logs.
- HTTPS with ATS; no disabled certificate validation. Pinning needs a rotation plan.
- Validate deep links, universal links, WebView navigation, and IPC inputs.
- Request minimum entitlements/permissions; protect sensitive screens and exclude data from backups.
- Use CryptoKit/platform crypto; never implement custom crypto.

## Common pitfalls

- Retain cycles from closures (`[weak self]` where ownership warrants).
- `Task` inheriting the wrong actor; blocking the main actor with synchronous I/O.
- `DateFormatter` creation in hot loops; use a cached formatter or `Date.FormatStyle`.
- Array index access assumptions; use safe indexing or `first`/`dropFirst`.
- Assuming `@MainActor` propagates through callbacks — annotate explicitly.

## Checklist

- [ ] No force unwraps/`try!` on external paths.
- [ ] Concurrency is structured, cancellable, and actor-correct.
- [ ] Secrets in Keychain; logs redacted.
- [ ] Deployment target and minimum OS tested.
- [ ] Lint/tests/sanitizers pass for the changed surface.
