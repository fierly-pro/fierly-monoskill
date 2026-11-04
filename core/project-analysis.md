# Project Analysis

> Load: existing or unfamiliar repository, legacy work, security review, or before a large change.
> Pairs with: `workflows/existing-project.md`, `core/architecture.md`.

## Fast path

```bash
python3 scripts/scan_project.py /path/to/repo --task "what you are about to do"
```

The scanner is heuristic and read-only. It detects languages, platforms, manifests, databases, infrastructure, tests, conventions, and sensitive areas, then suggests a module budget. **Verify every material claim** before acting.

## Manual verification (required)

Read only what establishes the system:

1. **Intent** — README, docs, ADRs, issue/PR context, changelog.
2. **Build** — manifest(s), lockfile, toolchain versions, scripts, monorepo config.
3. **Entry points** — server bootstrap, app entry, CLI main, worker registration.
4. **Structure** — module boundaries, dependency direction, shared utilities, generated code.
5. **Data** — schema, migrations, ownership, retention, external stores.
6. **Interfaces** — public APIs, events, webhooks, contracts, versioning.
7. **Verification** — test layout, commands, CI jobs, current pass/fail baseline.
8. **Conventions** — formatter, linter, naming, error style, logging, commit style, `AGENTS.md`/`CLAUDE.md`.
9. **Risk** — auth, payments, PII, uploads, crypto, admin paths, infrastructure, secrets.
10. **Operability** — configuration, health checks, metrics, logs, deploy/rollback.

Run the existing test suite before editing when feasible. A failing baseline must be recorded, not "fixed" silently.

## Project brief (write before a large change)

```text
Goal:            one sentence
Stack:           languages, frameworks, runtime versions (verified from manifests)
Shape:           monolith / service / monorepo / app + API / library
Entry points:    paths
Data:            stores, schemas, migrations, ownership
Interfaces:      APIs/events consumed and exposed
Verification:    exact commands and current status
Conventions:     linter/formatter/test/style rules to follow
Risks:           security-sensitive paths and unknowns
Constraints:     compatibility, deadlines, deployment limits
Unknowns:        what must be checked before irreversible work
```

Keep it short enough to re-read. Update it when inspection contradicts the scanner.

## Respect the existing system

- Prefer extension at existing seams over new architecture.
- Match local conventions even when another style is subjectively better.
- Do not rename, reformat, or reorganize unrelated code.
- Do not upgrade dependencies as a side effect of a feature or bug fix.
- Isolate new patterns; propose a migration separately with evidence.
- If the existing design blocks the requirement, state the cost of both options before changing it.

## Risk map

Mark each area that the change touches: authentication, authorization, session/token handling, cryptography, payments, personal data, file upload/parsing, SQL/NoSQL queries, shell/process execution, deserialization, outbound requests (SSRF), admin surfaces, infrastructure/IAM, CI/CD, release signing.

Any marked area requires the matching security module and explicit verification.

## Unknowns

Record unknowns as questions with a verification method. Do not fill gaps with plausible-sounding assumptions. If an unknown blocks safe progress, ask one precise question; otherwise choose the reversible path and state the assumption.
