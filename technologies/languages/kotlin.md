# Kotlin

> Load: Kotlin/JVM, Android, or Kotlin Multiplatform code.
> Pairs with: `platforms/android.md`, `security/native.md`, `technologies/frameworks/flutter.md` only for KMP boundaries.

## Defaults

- Prefer `val`, immutable data classes, sealed hierarchies, and expression-oriented code.
- Respect nullability: avoid `!!`; use `?.`, `?:`, `requireNotNull` with a message, or explicit error paths.
- Use coroutines with structured concurrency: a `CoroutineScope` tied to a lifecycle; cancel on teardown. Never use `GlobalScope` in application code.
- Choose dispatchers explicitly (`Dispatchers.IO` for blocking I/O, `Default` for CPU, `Main` for UI). Do not block inside coroutines.
- Flows for streams; `StateFlow`/`SharedFlow` with clear replay and lifecycle-aware collection.
- Gradle Kotlin DSL + version catalogs; keep dependency versions centralized. Avoid dynamic versions.
- Java interop: platform types (`String!`) are unsafe; annotate boundaries and validate.
- Use `Result`/sealed errors for expected failures; exceptions for programmer errors.

## Testing and tooling

- JUnit 5 + Kotlin test assertions; Turbine for Flow; coroutine test dispatchers (`runTest`) — never real delays.
- Prefer fakes over mocks for domain logic; integration tests for DB/network with real dependencies where practical.
- Run `ktlint`/`detekt` with the project config; do not suppress rules without a comment.
- Keep compiler warnings visible; treat new warnings as defects.

## Security

- Do not hardcode secrets, API keys, or signing material. Use platform secure storage for tokens (see `security/native.md`).
- Validate all external input (network, intents, deep links, files); do not trust client-side checks.
- Android: protect exported components, validate intents, use HTTPS, configure network security correctly.
- Avoid logging tokens/PII; strip release logs.
- Use platform crypto/Keystore; never invent cryptographic protocols.

## Common pitfalls

- `runBlocking` in production paths; `GlobalScope` leaks; swallowed `CancellationException` (rethrow it).
- Mutable shared state across coroutines without a `Mutex`/actor/atomic.
- `lateinit` used where a nullable or constructor dependency is safer.
- Collecting a Flow without lifecycle awareness on Android (use `repeatOnLifecycle`).
- Java libraries that block; wrap with the correct dispatcher and timeout.

## Checklist

- [ ] No `!!` on external data; null paths handled.
- [ ] Coroutines are structured, cancellable, and use the right dispatcher.
- [ ] Flow collection is lifecycle-aware.
- [ ] Tests use virtual time; lint/detekt clean.
- [ ] Secrets and tokens use platform secure storage.
