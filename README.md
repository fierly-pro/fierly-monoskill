# Fierly MonoSkill

**One skill. Every platform. Plan first, load only what you need, verify what you claim.**

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](CHANGELOG.md)
[![Agent Skills](https://img.shields.io/badge/standard-Agent%20Skills-orange.svg)](https://agentskills.io/specification)

Fierly MonoSkill is a universal engineering skill for AI coding agents. It gives an agent a strict operating contract, then routes each task to the minimum set of modules it actually needs: one workflow, the matching platform and technology guides, and the relevant security controls.

The goal is simple: agents that plan before they write code, never invent APIs or test results, and spend their context window on your project instead of on methodology they do not need.

---

## Why Fierly

| Problem with unguided agents | What Fierly does |
|---|---|
| Jump into code without reading the project | Requires inspection first: manifests, entry points, tests, CI, conventions |
| Invent APIs, flags, versions, and test results | Forbids it. Everything is verified against the repository or official docs |
| Say "tests should pass" without running them | Requires exact commands and real outcomes in the final report |
| Loop on failing checks | Stops after two focused failures and reports hypothesis and evidence |
| Burn context on giant instruction files | Loads a small, routed module set instead of the whole tree |
| Treat security as a final step | Applies a security baseline to every implementation, review, and release |

---

## How it works

```
Task ──► Classify ──► Scan (optional) ──► Route ──► Execute ──► Report
          risk,        scripts/           1 workflow   universal    outcome,
          change       scan_project.py    platforms    loop         evidence,
          type                            technologies              assumptions
                                          security
```

1. **Classify** the task: new or existing project, type of change, and risk level. Authentication, payments, personal data, crypto, infrastructure, and public APIs count as high risk.
2. **Analyze** an existing repository with the bundled scanner, then verify its heuristic output manually.
3. **Route** to modules using the tables in [`SKILL.md`](SKILL.md): always `core/engineering.md` and `security/baseline.md`, exactly one workflow, and platform, technology, and security modules only when matched.
4. **Execute** the universal loop: Frame, Inspect, Plan, Implement, Verify, Harden, Report.
5. **Report** with a fixed contract: outcome, changes, verification evidence, security status, assumptions, next steps.

### Progressive disclosure

| Level | Content | Loaded |
|---|---|---|
| L0 | `name` and `description` | At startup, always |
| L1 | [`SKILL.md`](SKILL.md): contract, routing tables, loop, budget | When the skill matches the task |
| L2 | `core/`, one workflow, platform, technology, and security modules | On demand, routed |
| L3 | Templates, tests, scanner output | Only when the task needs them |

### Module budget

| Category | Limit |
|---|---|
| Workflow | 1 |
| Platforms | up to 2 (client and server) |
| Core technologies (languages, frameworks, databases) | up to 4 |
| Infrastructure | up to 2, only when deployment is in scope |
| Security | `baseline.md` plus up to 5 attack-surface modules |

The agent must state a concrete blocker to exceed the budget. According to the estimates in [ARCHITECTURE.md](ARCHITECTURE.md), a typical feature loads roughly 5,000 to 8,000 tokens of methodology, compared with more than 40,000 for the whole tree. Exact counts depend on the tokenizer.

---

## Installation

Fierly is a folder containing `SKILL.md`. Installing it means placing that folder where your client discovers skills.

**Option A: Agent Skills CLI** (requires Node.js 22.20+)

```bash
npx skills add fierly-pro/fierly-monoskill        # project scope
npx skills add fierly-pro/fierly-monoskill -g     # global scope
```

**Option B: manual**

```bash
# Example: global Claude Code install
git clone https://github.com/fierly-pro/fierly-monoskill.git ~/.claude/skills/fierly-monoskill
```

The folder name must be exactly `fierly-monoskill`, because the Agent Skills specification requires the skill `name` to match its directory.

Works with any Agent Skills-compatible client, including Claude Code, OpenCode, Cursor, Codex, GitHub Copilot, Gemini CLI, Windsurf, and Antigravity. Skill directory paths differ per client and may change. See [INSTALLATION.md](INSTALLATION.md) for the path table, verification steps, updating, and troubleshooting.

**Requirements:** Python 3.9+ is optional and only needed for the helper scripts. No network access is required at runtime.

---

## Quick start

Start a new client session, then ask for work, not for a lecture:

> Use Fierly MonoSkill. Fix the failing password-reset test in this repository. Reproduce it first, add a regression test, and show the commands you ran.

The agent should scan the project, load `core/engineering.md`, `workflows/bugfix.md`, the matching platform and technology modules, and `security/baseline.md` (plus `security/auth.md` for a reset flow), reproduce the failure, fix the root cause, add a regression test, and report exact command results.

To run the scanner yourself:

```bash
python3 scripts/scan_project.py /path/to/your/repo --task "add rate limiting to login"
```

It prints detected languages, platforms, frameworks, databases, infrastructure, tests, conventions, sensitive areas, and a suggested module budget. The scanner is read-only, dependency-free, makes no network calls, and its output is a heuristic you should verify.

### Example prompts

| Goal | Prompt |
|---|---|
| New app | "Use Fierly to scaffold a React + FastAPI + PostgreSQL app with email login. Start with a vertical slice, tests, and a threat model." |
| Existing code | "Use Fierly to analyze this repo before changing anything. Give me the project brief, risks, and the exact test commands." |
| Bug | "Use Fierly to fix this crash. Reproduce it, find the root cause, and add a regression test." |
| Review | "Use Fierly to review this diff. Findings by severity with file:line and impact." |
| Security | "Use Fierly to threat-model the file upload path and test it." |
| Release | "Use Fierly to prepare v2.3.0. Run the security gate and list blocking findings and rollback steps." |

More prompts and a first-10-minutes checklist are in [QUICK_START.md](QUICK_START.md).

---

## What is inside

| Category | Modules |
|---|---|
| **Core** (4) | `engineering` (always loaded), `project-analysis`, `architecture`, `testing` |
| **Workflows** (12) | new-project, existing-project, feature, bugfix, refactor, architecture, code-review, testing, security-review, performance, dependencies, release |
| **Platforms** (9) | web, backend, android, ios, macos, windows, linux, cross-platform, desktop |
| **Languages** (8) | TypeScript, Python, Kotlin, Swift, Go, Rust, C/C++, SQL |
| **Frameworks** (6) | React, FastAPI, Django, Spring Boot, .NET, Flutter |
| **Databases** (5) | PostgreSQL, SQLite, MongoDB, Redis, Firebase/Firestore |
| **Infrastructure** (4) | Docker, Kubernetes, CI/CD, Cloud |
| **Security** (11) | baseline, input, auth, database, api, frontend, native, infrastructure, supply-chain, testing, gate |

Templates for an ADR, a threat model, a review report, and a security gate live in `templates/`.

### Operating contract

These rules apply to every task before any module is loaded:

1. Inspect before changing.
2. Plan non-trivial work.
3. Change the smallest correct surface.
4. Never invent APIs, flags, paths, versions, or test results.
5. Reproduce bugs before fixing them.
6. Run what you claim and report exact outcomes.
7. Respect existing architecture and public contracts.
8. Treat security as a requirement and all external data as untrusted.
9. Prefer reversible steps.
10. Separate facts, assumptions, and open questions.

### Hard stops

The agent must stop and ask for an explicit decision before any change that would expose or rotate credentials or production data, weaken authentication, authorization, TLS verification, or sandboxing, run destructive migrations without a backup and rollback path, ship with a confirmed critical vulnerability or failing security gate, or break a public API or data format without a migration plan. It never disables a failing check to make a task look complete.

---

## Repository layout

```
fierly-monoskill/
├── SKILL.md              # Entry point: contract, routing tables, loop, budget
├── registry.json         # Machine-readable module catalog used by the scanner
├── core/                 # Cross-cutting engineering rules
├── workflows/            # One per task type
├── platforms/            # Web, backend, mobile, desktop, cross-platform
├── technologies/         # Languages, frameworks, databases, infrastructure
├── security/             # Baseline, attack-surface modules, release gate
├── templates/            # ADR, threat model, review report, security gate
├── scripts/              # scan_project.py, validate.py
├── tests/                # Routing scenarios and execution results
├── ARCHITECTURE.md       # Design decisions and known limitations
├── INSTALLATION.md       # Per-client install paths and troubleshooting
├── QUICK_START.md        # First steps and example prompts
├── UPSTREAM_SOURCES.md   # Licenses and sources consulted
├── CONTRIBUTING.md
├── SECURITY.md
└── CHANGELOG.md
```

---

## Quality checks

The repository validates itself:

```bash
python3 scripts/validate.py
```

The validator checks frontmatter, name and directory match, registry integrity, required documents, relative links, module headers, size budgets, workflow completion criteria, unsafe patterns, duplicated content, placeholders, and license and source presence. Routing behavior is covered by the scenarios in `tests/scenarios.md`, with execution notes in `tests/results.md`.

---

## Limitations

Fierly is guidance, not enforcement.

- Modules are advisory. An agent can ignore them, though the reporting contract makes violations visible.
- Automatic activation depends on how well your client matches the skill description. Naming the skill explicitly is the most reliable way to trigger it.
- The scanner proposes signals from manifests, dependencies, and paths. It cannot infer architecture or intent.
- Technology coverage is curated. There are no dedicated modules yet for Rails, Laravel/Symfony, Express/NestJS, ASP.NET, Gin, or Axum. For unlisted stacks the agent relies on core rules, the platform module, and official documentation.
- There is no runtime sandbox or policy engine, and Fierly does not replace human review.

---

## Security and trust

Skills are instructions executed with your agent's permissions. Review the source, pin a version, and avoid installing untrusted forks. Fierly installs no services, hooks, MCP servers, or global state, and its scripts are read-only and make no network calls. Security scanners mentioned in the modules (such as CodeQL, Semgrep, Gitleaks, Trivy, OSV-Scanner, and ZAP) are separate tools that you install and authorize yourself. To report a vulnerability, see [SECURITY.md](SECURITY.md).

---

## Contributing

Contributions are welcome. A new module needs a registry entry, a link in `SKILL.md`, a scanner signal if the technology is detectable, and a routing scenario when behavior changes. Read [CONTRIBUTING.md](CONTRIBUTING.md) first and run `python3 scripts/validate.py` before opening a pull request.

---

## License

Released under the [Apache License 2.0](LICENSE). Sources and licenses consulted during research are listed in [UPSTREAM_SOURCES.md](UPSTREAM_SOURCES.md).
