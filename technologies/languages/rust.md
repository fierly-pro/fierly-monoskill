# Rust

> Load: Rust applications, services, CLIs, or libraries.
> Pairs with: `platforms/linux.md`/`backend.md`, `security/input.md`.

## Defaults

- Model states with enums and the type system; make illegal states unrepresentable.
- Return `Result` for recoverable failures; use `?` with context (`anyhow` in apps, `thiserror` in libraries).
- Avoid `unwrap`/`expect`/panics in production paths. If an invariant is truly guaranteed, use `expect` with a precise message.
- Prefer borrowing over cloning; clone only when ownership requires it. Keep lifetimes local.
- Use `clippy` with warnings denied in CI, plus `rustfmt`.
- Async: choose one runtime (usually Tokio); never block the executor — use `spawn_blocking` for CPU/blocking I/O.
- Concurrency: prefer channels/message passing or scoped threads; use `Arc<Mutex<_>>` deliberately, and avoid holding locks across `.await`.
- Pin dependencies with `Cargo.lock` for applications; review features to reduce build and attack surface.

## Unsafe and FFI

- `unsafe` requires a `// SAFETY:` comment stating the invariant and why it holds.
- Minimize the unsafe surface; wrap it in a safe abstraction with tests.
- Validate pointers, lengths, and alignment at FFI boundaries; document ownership and thread-safety.
- Run Miri for unsafe/UB-sensitive code where practical.

## Security

- Treat all input bytes as untrusted: use `serde` with explicit schemas; bound sizes and nesting depth.
- Avoid `unsafe` deserialization formats; do not `bincode` untrusted data without limits.
- Use `rustls`/platform TLS correctly; never disable certificate verification.
- Constant-time comparison for secrets (`subtle`); zeroize sensitive buffers where practical.
- Do not log secrets; use `secrecy`/redaction.
- Check integer overflow behavior; use checked/saturating arithmetic for untrusted sizes.
- Audit dependencies (`cargo audit`, `cargo deny`) and licenses.

## Testing and tooling

- Unit tests in-module; integration tests in `tests/`; property tests (`proptest`) for parsers; fuzzing (`cargo-fuzz`) for untrusted byte formats.
- Test error paths and boundary sizes; use `#[should_panic]` only for documented invariants.
- Run tests under `--release` when behavior depends on optimization; use sanitizers where supported.
- Benchmark with Criterion for hot paths; profile before optimizing.

## Common pitfalls

- Holding a `MutexGuard` across `.await` (use `tokio::sync::Mutex` or restructure).
- Blocking the async runtime with synchronous file/network/CPU work.
- Over-cloning to satisfy the borrow checker, hiding a design issue.
- `unwrap` on environment/config/network data.
- Unbounded channels/queues causing memory growth.

## Checklist

- [ ] No panics/unwraps on external data.
- [ ] `clippy`, `fmt`, tests pass; unsafe code documented.
- [ ] Async runtime is not blocked; locks are not held across awaits.
- [ ] Input sizes bounded; secrets handled and redacted.
- [ ] `cargo audit`/`cargo deny` triaged.
