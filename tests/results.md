# Evaluation Results

Last run: **2026-11-04**  
Environment: Linux, Python 3.14.4, git 2.53.0, `uvx` available.

## Scope and honesty statement

This document records two different kinds of evidence:

1. **Executed checks** — validator, official Agent Skills validation, Python compilation, and scanner runs against synthetic and real repositories.
2. **Routing audit** — a scenario-by-scenario check that the skill's routing tables, module budget, and module content contain the expected route and required guidance.

The routing audit is **not** a live LLM coding benchmark. No application code was generated for scenarios 01–10, and no deployment, migration, or mobile build was executed. Scores below are rubric-based audit scores for routing/coverage, not measurements of model output quality. A scenario marked **partial** needs a real target repository or CI run before it can be called fully verified.

An earlier independent routing pass identified the issues listed under “Issues found and fixed”. The table reflects the repository **after** those fixes.

## Results

| # | Scenario | Routing result | Score | Evidence / residual gap |
|---|---|---|---|---|
| 01 | New React + FastAPI + PostgreSQL app with Docker | Pass (routing) | 92/100 | Route: `new-project`, `web`+`backend`, React/FastAPI/PostgreSQL/SQL, Docker as in-scope infrastructure, baseline + auth/api/input/database. Budget: 2 platforms, 4 core tech, 1 infra, 5 security. No live scaffold/deploy. |
| 02 | CSV export in an existing Django API | Pass (routing) | 91/100 | Route: `feature`, `backend`, Django/Python, baseline + auth/api/input. CSV/formula injection guidance now present in `security/input.md`. No 100k-row streaming test. |
| 03 | 200M-row PostgreSQL migration, zero downtime | Pass (routing) | 87/100 | Explicit route to `performance`; expand/backfill/contract, concurrent index, batching, lock/replication checks, rollback/forward-fix added to `workflows/performance.md`; baseline + database. No production-like database run. |
| 04 | Android “remember me” refresh token | Pass (routing) | 90/100 | Route: `feature`, `android`, Kotlin, baseline + native/auth. Keystore storage, rotation/revocation, logout cleanup, process death, and biometric-vs-server-trust guidance present. No device/emulator test. |
| 05 | Tauri Markdown reader with auto-update | Pass (routing) | 88/100 | Route: `new-project`, `desktop` + target OS, baseline + native/supply-chain. Capability scoping, path validation, CSP, sanitization, signed updates, rollback present. Multi-OS exception documented. No packaged build or update test. |
| 06 | C daemon crash under load, running as root | Partial (needs target) | 86/100 | Route: `bugfix`, `linux`, C/C++, baseline + input. Sanitizers, reproduction, root-cause discipline, privilege drop, regression test, residual risk covered. The actual crash was not reproduced. |
| 07 | Expired password-reset link | Pass (routing) | 92/100 | Route: `bugfix`, baseline + auth/input. Server-side expiry, single-use token, invalidation, enumeration resistance, regression test, full-suite verification covered. No target tests executed. |
| 08 | Extract payment logic from a large controller | Pass (routing) | 90/100 | Route: `refactor`, `core/testing`, baseline; security links now explicitly include auth/input/database for payments and high-risk paths. Characterization tests and small steps required. No target refactor run. |
| 09 | Session auth and admin authorization review | Pass (routing) | 92/100 | Route: `security-review`, `web`/`backend`, baseline + auth/api/frontend/testing. Threat model, IDOR, fixation/rotation, CSRF, cookie flags, rate limits, abuse cases, severity, gate decision covered. No live review of a real codebase in this run. |
| 10 | Mobile + backend production release | Partial (needs evidence) | 85/100 | Route: `release`, `backend` + mobile, baseline + gate/supply-chain/testing/api/native. Signing, store metadata, migration/rollback, SBOM, artifact signing, blocking risks, post-deploy checks covered. No release evidence or store submission exists. |

**Audit average:** 89.3/100. **Critical fails:** none in the documented routing. **Partial scenarios:** 06 and 10 (and 01–05, 08–09 remain unexecuted as coding tasks).

## Issues found and fixed in this pass

| Issue | Fix |
|---|---|
| `.NET` module existed but was missing from the `SKILL.md` technology table | Added the `.NET` link under Frameworks |
| Infrastructure budget wording implied Docker counted inside the ≤4 core-tech cap | Budget now separates ≤4 core tech (languages/frameworks/databases) from ≤2 infrastructure modules when deploy/infra is in scope; scenario 01 is consistent |
| Zero-downtime migration route was ambiguous between `feature`, `architecture`, and `release` | Added an explicit route row to `performance`, with `release` when deploy/rollback is primary; added migration steps to `workflows/performance.md` |
| No CSV/spreadsheet formula-injection guidance | Added CSV injection controls and test values to `security/input.md` |
| Refactor workflow did not name security modules for payment/high-risk code | Added auth/input/database links with trigger conditions to `workflows/refactor.md` |
| Multi-OS desktop exceeded the ≤2 platform cap without an exception | Documented a justified exception: `desktop` + up to 3 OS modules when packaging/signing differs per OS |
| Scenario 04 budget arithmetic counted 4 modules against a ≤3 cap | Corrected to ≤4 modules beyond baseline (platform + tech + security combined) |
| Scanner treated the word “export” as the “expo” framework (`expo` is a substring) | Changed to a word-boundary match; `hozdar-shop` now routes to `web`+`backend`, not `cross-platform` |
| Scanner suggested more than 5 attack-surface modules without stating the cap | Output now says “choose baseline + ≤5 matching the attack surface” |
| No dedicated modules for Rails, Laravel/Symfony, Express/NestJS, ASP.NET, Gin, Axum | Documented as a known coverage limitation in `ARCHITECTURE.md`; fallback is core + platform + official docs |

## Executed checks

### 1. Repository validator

```bash
cd "/home/denis/Документи/Типовий проєкт/fierly-monoskill"
python3 scripts/validate.py
```

Expected after this file exists: exit code 0, 0 errors, 0 warnings. It checks frontmatter/name, registry integrity, required files, relative links, module headers, size budgets, workflow exit criteria, unsafe patterns, duplicates, placeholders, and license/source presence.

### 2. Official Agent Skills validator

```bash
cd "/home/denis/Документи/Типовий проєкт"
uvx --from skills-ref agentskills validate "fierly-monoskill"
```

Recorded output:

```text
Valid skill: fierly-monoskill
```

Exit code: `0`.

### 3. Python syntax

```bash
python3 -m py_compile scripts/validate.py scripts/scan_project.py
```

Result: exit code `0` (no output).

### 4. Scanner on the synthetic full-stack fixture

Command:

```bash
python3 scripts/scan_project.py /tmp/opencode/fierly-fixture --task "Add rate limiting to login"
```

Observed: 8 files; Python/TypeScript/SQL; `web`+`backend`; React/FastAPI/PostgreSQL/Docker/SQL; pytest/vitest; PostgreSQL database; Docker infrastructure; suggested baseline + auth/api/frontend/database/input/infrastructure. This is a heuristic proposal, not proof that every technology is used.

### 5. Scanner on a real Android/Kotlin repository (`PulseWave`)

Command:

```bash
python3 scripts/scan_project.py ../PulseWave --task "Add remember me to Android app"
```

Observed: 44 files; Kotlin (26); platform `android`; technology `kotlin`; Gradle; workflow `feature`; security baseline + native. No database or infrastructure detected.

### 6. Scanner on a real Astro/Svelte/Firebase repository (`hozdar-shop`)

Command:

```bash
python3 scripts/scan_project.py ../hozdar-shop --task "Add CSV export"
```

Observed after the “expo” fix: 87 files; TypeScript/JavaScript; `web`+`backend` (no false `cross-platform`); Firebase/Firestore; npm; sensitive areas include Firestore/Storage rules, env file, payment code, admin upload/catalog endpoints; suggested baseline + frontend/api/database/input.

## Residual limitations

- **No live scenario execution.** Scenarios 01–10 were routed and audited, not implemented. Claims about tests, migrations, builds, signing, or store review are explicitly not made.
- **No target-repository verification for scenarios 03, 05, 06, 08, 09, 10.** They require a production-like database, packaged desktop builds, sanitizer runs, or release artifacts.
- **Curated framework coverage.** Rails, Laravel/Symfony, Express/NestJS, ASP.NET, Gin, and Axum have no dedicated modules; the fallback is core + platform + official docs.
- **Scanner is heuristic.** It may over-suggest modules (e.g., six security modules on the fixture); the agent must apply the budget and verify manually.
- **Official validator scope.** It validates Agent Skills structure, not the correctness of engineering advice.
- **No GitHub publication.** The repository is local; no remote URL or release was created because `gh` is unavailable and publishing requires explicit permission.

## Reproduction

```bash
cd "/home/denis/Документи/Типовий проєкт/fierly-monoskill"
python3 scripts/validate.py
python3 -m py_compile scripts/validate.py scripts/scan_project.py
python3 scripts/scan_project.py /tmp/opencode/fierly-fixture --task "Add rate limiting to login"
```

For a new scenario, run the prompt without hints, record the modules actually loaded, and score with [rubric.md](rubric.md). Do not treat this routing audit as a substitute for running the target project's tests.
