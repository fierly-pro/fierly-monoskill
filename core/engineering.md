# Core Engineering

> Load: always, for any implementation, review, or architecture task.
> Pairs with: one workflow, the matched platform/technology modules, `security/baseline.md`.

## Priority order

1. **Correctness** — satisfies the stated requirement and real edge cases.
2. **Clarity** — the next engineer can change it safely.
3. **Security** — a hard gate; a fast or clean insecure solution is not acceptable.
4. **Compactness** — less code, fewer dependencies, fewer moving parts.

When two rules conflict, security constraints and verified platform requirements win. Record the tradeoff; do not silently drop a requirement.

## Decision rules

- **Requirements before preferences.** Match existing project conventions over personal style. Match platform conventions over generic advice.
- **YAGNI, then simplest sufficient design.** Do not add abstraction for a second use case that does not exist.
- **DRY behavior, not syntax.** Duplicating two similar lines can be cheaper than a premature abstraction. Extract when the third real case appears or when the concept is stable.
- **Explicit over implicit.** Prefer clear data flow, typed boundaries, and named constants over magic.
- **Reversible over clever.** Small commits, feature flags, expand/contract migrations, and rollback paths beat heroic rewrites.
- **Measure before optimizing.** Profile with real workloads; state the baseline and the target.
- **No speculative rewrites.** Improve the touched surface; propose unrelated work separately.

## Before writing code

- Identify the entry point, the data flow, and the trust boundaries.
- Find the test command, lint command, build command, and CI configuration.
- Read 2–3 representative files to absorb naming, error handling, layout, and dependency style.
- Confirm the runtime and language versions from manifests, not memory.
- List assumptions that could invalidate the approach; verify or ask.

## Code quality

- **Names** state intent: `remainingAttempts`, not `n`; `isEligible`, not `flag`.
- **Functions** do one thing at one level of abstraction. Keep parameter lists small; pass structured objects when a concept exists.
- **Types** at boundaries: parse untrusted data into domain types once, then trust internal values.
- **Immutability by default.** Mutate only where the language or performance profile justifies it.
- **No dead code, commented-out blocks, or unused flags.** Remove them in the same change.
- **No swallowed errors.** Catch only what you can handle; preserve the cause and context.
- **No global state** unless the platform requires it. Make lifecycle and ownership explicit.
- **Resource cleanup** via the language's deterministic mechanism (`defer`, `with`, `using`, RAII, `finally`).
- **Concurrency:** define ownership, cancellation, timeouts, and backpressure. Never share mutable state without a documented synchronization strategy.
- **Comments explain why**, constraints, and non-obvious tradeoffs — not what the code already says.
- **Formatting** is automated. Do not hand-format or reformat untouched files.

## Errors and failure behavior

- Distinguish expected failures (validation, not found, conflict) from bugs (invariant violations).
- Return structured errors with stable codes at API boundaries; keep internal detail out of user-facing messages.
- Fail closed for authorization, signature verification, and policy checks. Fail open only with an explicit, documented rationale.
- Add timeouts to all network calls, retries only for idempotent operations, and jitter to avoid thundering herds.
- Never log secrets, tokens, passwords, full card data, or unnecessary personal data.

## Dependencies and configuration

- Add a dependency only when it replaces substantial, risky code; check maintenance, license, transitive weight, and security posture.
- Pin application dependencies with a lockfile; pin CI actions and container images by digest or immutable version.
- Configuration comes from the environment or a secret manager, never from committed credentials.
- Validate configuration at startup and fail with a clear message. Provide safe defaults for non-sensitive values.

## Change discipline

- Atomic commits with messages that explain intent: `fix(auth): reject expired reset tokens`.
- Do not mix refactoring, dependency upgrades, and behavior changes in one commit.
- Preserve public APIs and data formats, or version/migrate them deliberately.
- Update tests, docs, migrations, configuration examples, and changelog in the same change when affected.
- Review your own diff before reporting: remove debug prints, temporary files, and accidental edits.

## Definition of done

- Acceptance criteria are met and demonstrated.
- The relevant build, typecheck, lint, and tests pass — actually executed.
- New behavior has tests; bug fixes have a regression test or a documented reason none is possible.
- Security-relevant paths were checked against the matched security modules.
- No secrets, debug artifacts, or unrelated changes are present.
- The report separates verified facts from assumptions and lists remaining work.
