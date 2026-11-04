# Workflow: Code Review

> Trigger: pull request, diff, pre-merge check, or self-review.
> Modules: `core/engineering.md`, `security/baseline.md` + modules matching the diff, `core/testing.md`, technology module.

## Method

1. **Understand the intent.** Read the description, linked issue, and acceptance criteria. Review the change against the goal, not personal preference.
2. **Check scope.** Separate unrelated changes, generated files, and formatting noise. Flag scope creep.
3. **Read the diff by risk**, not top to bottom: auth, data access, migrations, input handling, concurrency, public contracts, error paths, then the rest.
4. **Verify behavior.** Run tests locally if possible; otherwise inspect CI evidence. Check that new behavior has tests and bug fixes have regression tests.
5. **Look for omissions.** Callers, migrations, config, docs, API schema, feature flags, rollback.
6. **Report findings** by severity with file:line, impact, and a concrete fix. Do not rewrite the patch in prose.

## Review axes

| Axis | Questions |
|---|---|
| Correctness | Does it meet the criteria? Edge cases, null/empty, concurrency, ordering, time zones, Unicode? |
| Security | Trust boundaries, input validation, authorization at the resource, secrets, injection, SSRF, unsafe deserialization, dependency risk? |
| Tests | Success + denial + failure paths? Deterministic? Would they catch a regression? |
| Maintainability | Clear names, single responsibility, no duplication/dead code, consistent with the codebase? |
| Performance | N+1 queries, unbounded loops, large payloads, missing pagination/indexes, hot-path allocations? |
| Operability | Logs, metrics, errors, timeouts, retries, config, migrations, rollback? |
| Compatibility | Public API, schema, serialized data, platform versions, accessibility, i18n? |

## Severity

- **Blocker** — incorrect, insecure, data-losing, or breaks the build/contract. Must fix before merge.
- **High** — likely production failure, authorization gap, or missing critical test. Fix before merge or record explicit risk acceptance.
- **Medium** — maintainability or edge-case defect; fix now or track with an owner.
- **Low / Nit** — style or preference consistent with the codebase. Optional.

## Output

```text
Verdict: approve | approve with comments | request changes
Scope:   what the change does and whether it matches intent

Findings:
- [Blocker] path:line — impact — required fix
- [High]    path:line — impact — required fix
- [Medium]  path:line — impact — suggested fix
- [Low]     path:line — suggestion

Evidence: checks run, tests inspected, gaps in verification
Residual risk: what remains unverified
```

## Exit criteria

- The verdict is explicit and matches the findings.
- Blockers/high issues are fixed or have documented acceptance.
- Verification evidence is stated; unverified areas are named.
- Findings are actionable, scoped, and free of unrelated refactor demands.

## Rules

- Every finding must be actionable and tied to evidence, not taste.
- Do not demand unrelated refactors; propose them separately.
- Do not approve with unverified security-sensitive changes.
- Distinguish "must fix" from "could improve"; keep the author's scope intact.
