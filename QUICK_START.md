# Quick Start

## 1. Install

```bash
npx skills add <owner>/fierly-monoskill
```

Or copy the folder into your client's skills directory. See [INSTALLATION.md](INSTALLATION.md).

## 2. Ask for work, not for a lecture

> Use Fierly MonoSkill. Fix the failing password-reset test in this repository. Reproduce it first, add a regression test, and show the commands you ran.

The agent should:

1. scan the project and verify the stack;
2. load `core/engineering.md`, `workflows/bugfix.md`, the matched platform/technology modules, and `security/baseline.md` (+ `auth.md` if the reset flow is involved);
3. reproduce, fix at the root, add a regression test;
4. run the project's tests/lint/build and report exact results.

## 3. Use the scanner (optional)

```bash
python3 /path/to/fierly-monoskill/scripts/scan_project.py . --task "add rate limiting to login"
```

It prints languages, platforms, frameworks, databases, infrastructure, tests, conventions, sensitive areas, and a suggested module budget. Verify the output — it is heuristic.

## 4. Example prompts

| Goal | Prompt |
|---|---|
| New app | “Use Fierly to scaffold a React + FastAPI + PostgreSQL app with email login. Start with a vertical slice, tests, and a threat model.” |
| Existing code | “Use Fierly to analyze this repo before changing anything. Give me the project brief, risks, and the exact test commands.” |
| Feature | “Use Fierly to add pagination to the orders API. Preserve the contract, add tests, and check object-level authorization.” |
| Bug | “Use Fierly to fix this crash. Reproduce it, find the root cause, and add a regression test.” |
| Refactor | “Use Fierly to extract billing logic from the controller without changing behavior. Characterization tests first.” |
| Review | “Use Fierly to review this diff. Findings by severity with file:line and impact; run the checks you can.” |
| Security | “Use Fierly to threat-model the file upload path and test it. Do not claim security from scanners alone.” |
| Release | “Use Fierly to prepare v2.3.0. Run the security gate and list blocking findings, accepted risks, and rollback steps.” |
| Performance | “Use Fierly to profile this endpoint. Measure a baseline before optimizing and show the delta.” |
| Dependencies | “Use Fierly to upgrade this major dependency safely. One change, full tests, rollback plan.” |

## 5. Keep the budget honest

If the agent loads ten modules for a one-line fix, ask: “Which modules are required by the stated risk, and which can be dropped?” Fierly's budget is 1 workflow, ≤2 platforms, ≤4 core technologies (plus infrastructure when deploy is in scope), and `security/baseline.md` plus ≤5 attack-surface modules.

## 6. Verify the work

Ask for the reporting contract:

```text
Outcome / Changes / Verification (commands + results) / Security / Assumptions / Next steps
```

A response without executed checks, or with “tests should pass,” is incomplete. Ask it to run them or state why it cannot.

## 7. Before release

Use the gate:

> Run the Fierly security gate for this release. Mark each item pass/fail/n/a with evidence, list blocking findings and accepted risks with owners and expiry, and state what was not tested.

## First 10 minutes checklist

- [ ] Skill appears in the client.
- [ ] A small task triggers the expected workflow and platform.
- [ ] The agent runs the project's test command or explains why it cannot.
- [ ] No unrelated modules are loaded.
- [ ] The final report separates facts from assumptions.
