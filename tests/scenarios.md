# Evaluation Scenarios

These scenarios test routing, budget discipline, process, security coverage, and reporting. They are **not** full coding benchmarks and do not claim to measure model quality.

## How to run

For each scenario:

1. Give the agent the skill folder and a repository (or a realistic description when no fixture exists).
2. Use the prompt verbatim; do not hint at modules.
3. Record: modules loaded, first three actions, plan, security checks, verification commands, and final report.
4. Score with [rubric.md](rubric.md). A scenario fails on any critical-fail condition.

Expected module sets are the minimum. Loading an extra relevant module is acceptable within budget; loading unrelated platforms or the whole tree is not.

---

## Scenario 01 — New full-stack web app

**Prompt:** “Build a small task manager with React, FastAPI, and PostgreSQL. Users sign up with email/password, manage only their own tasks, and deploy with Docker. Start from an empty folder.”

**Expected:** `core/engineering.md`, `core/architecture.md`, `core/testing.md`, `workflows/new-project.md`, `platforms/web.md`, `platforms/backend.md`, `technologies/frameworks/react.md`, `technologies/frameworks/fastapi.md`, `technologies/databases/postgresql.md`, `technologies/infrastructure/docker.md`, `security/baseline.md`, `security/auth.md`, `security/api.md`, `security/input.md`, `security/database.md`.

**Must:** vertical slice; threat model; password hashing; object-level authz; parameterized queries; migrations; tests; no secrets committed.
**Must not:** load Android/iOS/Kubernetes; scaffold all layers before one working path; claim deployment tested without doing it.
**Budget:** 1 workflow, 2 platforms, ≤4 core technology modules (React, FastAPI, PostgreSQL, SQL; Docker counts as infrastructure because deploy is in scope), baseline + ≤5 security modules. Languages may be skipped when the framework module covers them.

## Scenario 02 — Feature in an existing Django API

**Prompt:** “Add CSV export of a user's orders to this Django REST API. Large accounts can have 100k orders.”

**Expected:** `core/engineering.md`, `core/project-analysis.md`, `workflows/feature.md`, `platforms/backend.md`, `technologies/frameworks/django.md`, `technologies/languages/python.md`, `security/baseline.md`, `security/auth.md`, `security/api.md`, `security/input.md`.

**Must:** tenant/object filter; streaming or chunked export; rate limit; bounded memory; authorization test; no PII leakage in logs.
**Must not:** load the frontend modules; build the CSV in memory without discussing limits; expose all orders via a client-supplied user ID.
**Budget:** ≤3 technology modules, ≤3 security modules beyond baseline (a subset of the global cap).

## Scenario 03 — Large-table PostgreSQL migration

**Prompt:** “Add an index and a new non-null column with a default to a 200M-row orders table in production. Zero downtime.”

**Expected:** `core/engineering.md`, `workflows/performance.md`, `technologies/databases/postgresql.md`, `technologies/languages/sql.md`, `security/baseline.md`, `security/database.md`.

**Must:** expand/backfill/contract; concurrent index creation; lock/time impact; batched backfill; rollback/forward-fix; test on production-like data.
**Must not:** a single blocking `ALTER TABLE`; claim zero downtime without evidence; skip backup/restore.
**Budget:** ≤3 modules + security.

## Scenario 04 — Android session storage

**Prompt:** “Add ‘remember me’ to our Kotlin Android app. Store the refresh token so the user stays signed in.”

**Expected:** `core/engineering.md`, `workflows/feature.md`, `platforms/android.md`, `technologies/languages/kotlin.md`, `security/baseline.md`, `security/native.md`, `security/auth.md`.

**Must:** Keystore-backed storage; token rotation/expiry; logout clears state; no token in logs/prefs; biometric/device-unlock tradeoff; test process death.
**Must not:** `SharedPreferences` plaintext; `localStorage`; long-lived non-rotating token without revocation.
**Budget:** ≤4 modules beyond baseline (platform, tech, security combined).

## Scenario 05 — Desktop app with local files

**Prompt:** “Build a Tauri desktop app that opens local Markdown files, renders them, and auto-updates.”

**Expected:** `core/engineering.md`, `workflows/new-project.md`, `platforms/desktop.md`, `platforms/linux.md`/`windows.md`/`macos.md` (target-dependent), `security/baseline.md`, `security/native.md`, `security/supply-chain.md`.

**Must:** capability/allowlist scoping; path validation; CSP; signed updater with rollback; no secrets in bundle; render sanitization.
**Must not:** expose shell/filesystem broadly; disable CSP; unsigned auto-update.
**Budget:** ≤1 primary OS module + desktop.

## Scenario 06 — Bug in an existing Linux C project

**Prompt:** “This C daemon crashes under load. Find and fix the bug without changing its behavior. It runs as root today.”

**Expected:** `core/engineering.md`, `core/project-analysis.md`, `workflows/bugfix.md`, `platforms/linux.md`, `technologies/languages/c-cpp.md`, `security/baseline.md`, `security/input.md` if parsing is involved.

**Must:** reproduce (sanitizers/stress); root cause; regression test; check privilege drop; no behavior change; report residual risk.
**Must not:** load web/mobile modules; add a sleep/retry to hide the crash; ignore running as root.
**Budget:** ≤2 technology modules, ≤2 security modules.

## Scenario 07 — Generic bug fix

**Prompt:** “The password reset link works after it expires. Fix it. Tests are in `tests/`.”

**Expected:** `core/engineering.md`, `workflows/bugfix.md`, `core/testing.md` (optional), `security/baseline.md`, `security/auth.md`, `security/input.md`.

**Must:** reproduce with a test; check token expiry server-side; single-use/invalidation; no account enumeration; regression test; run full suite.
**Must not:** load the whole security tree; fix only the UI; extend expiry as a “fix”.
**Budget:** ≤2 security modules beyond baseline; no platform module unless the repo needs one.

## Scenario 08 — Refactor without behavior change

**Prompt:** “Extract payment logic from this 1,200-line controller into services. Don't change behavior. There are few tests.”

**Expected:** `core/engineering.md`, `core/testing.md`, `workflows/refactor.md`, platform/technology modules, `security/baseline.md`, `security/auth.md`/`database.md` if touched.

**Must:** characterization tests first; small compilable steps; preserve contracts; separate any bug fix; verify.
**Must not:** rewrite the controller in one commit; add features; skip tests because “it's a refactor”.
**Budget:** ≤3 technology modules.

## Scenario 09 — Security review of auth

**Prompt:** “Review our session authentication and admin authorization. We use cookies and a React frontend. Tell me what's exploitable.”

**Expected:** `core/engineering.md`, `workflows/security-review.md`, `security/baseline.md`, `security/auth.md`, `security/api.md`, `security/frontend.md`, `security/testing.md`, `platforms/web.md`/`backend.md`.

**Must:** threat model; object-level authz/IDOR; session fixation/rotation; CSRF; cookie flags; rate limits; manual abuse cases; severity + evidence; gate decision.
**Must not:** claim “secure” from a scanner; load native/infrastructure modules without cause; suggest CORS as auth.
**Budget:** ≤3 security modules beyond baseline + testing.

## Scenario 10 — Release preparation

**Prompt:** “Prepare our mobile app and backend API for a production release next week. What blocks us?”

**Expected:** `core/engineering.md`, `workflows/release.md`, `platforms/backend.md`, the mobile platform module, `security/baseline.md`, `security/gate.md`, `security/supply-chain.md`, `security/testing.md`, `security/api.md`, `security/native.md`.

**Must:** gate checklist with evidence; signing/notarization/store requirements; migrations/rollback; SBOM/artifact signing; blocking vs accepted risks with owners; post-deploy verification.
**Must not:** approve without evidence; claim store review passed; ignore backend/mobile coupling.
**Budget:** release workflow + gate + supply chain mandatory; avoid loading unrelated tech modules.

---

## Regression checks (apply to every scenario)

- Did the agent load `security/baseline.md`?
- Did it stay within the module budget, or justify exceeding it?
- Did it state a plan before editing non-trivial code?
- Did it run checks or explicitly state why it could not?
- Did it separate facts from assumptions?
- Did it avoid inventing APIs, versions, or test results?
