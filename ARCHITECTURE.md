# Architecture

## Goals

- One skill that activates once and routes to the minimum sufficient expertise.
- Consistent engineering and security behavior across platforms.
- High information density; no duplicated universal rules.
- Validatable structure, executable project scan, testable routing.
- Compatibility with the Agent Skills specification.

Non-goals: replace human review, enforce policy at runtime, bundle scanners, cover every technology, or act as a multi-skill marketplace.

## Key decisions

### 1. One skill, not one skill per platform

The repository root is the skill (`SKILL.md` + `name: fierly-monoskill`). Platform, technology, workflow, and security documents are plain Markdown reference modules loaded on demand.

**Why:** the spec discovers a skill by `SKILL.md`. Nested `SKILL.md` files would be discovered as separate skills by some clients, causing duplicate activation, routing ambiguity, and context bloat. Plain modules keep one activation surface.

**Tradeoff:** no per-module frontmatter/validation by clients; the repository validator and registry enforce integrity instead.

### 2. Three-level progressive disclosure

| Level | Content | When loaded |
|---|---|---|
| L0 | `name` + `description` | Startup, always |
| L1 | `SKILL.md` (contract, routing tables, loop, budget) | When the skill matches |
| L2 | `core/`, one workflow, platform, ≤4 technologies, security modules | On demand, routed |
| L3 | Templates, examples, tests, scanner output | Only when the task needs them |

L2 is deliberately capped: 1 workflow, ≤2 platforms (client+server), ≤4 core technologies (languages/frameworks/databases) plus ≤2 infrastructure modules only when deployment is in scope, and `security/baseline.md` plus ≤5 attack-surface modules. A multi-OS desktop release may load `platforms/desktop.md` + up to 3 OS modules when packaging/signing differs per OS. The agent must justify exceeding the budget.

### 3. Routing is deterministic first, judgment second

- `registry.json` is the machine-readable catalog used by `scripts/scan_project.py`.
- `SKILL.md` contains human/agent-readable routing tables.
- The scanner detects stack signals and proposes modules; the agent verifies and may override.
- `scripts/validate.py` prevents registry/SKILL/link drift.

The scanner is heuristic (file counts, manifests, dependencies, paths) and never writes to the target repository.

### 4. Security is an overlay, not a platform

`security/baseline.md` applies to every implementation/review/release task. Attack-surface modules load only when matched. The release gate is a separate workflow with explicit blocking severities. This avoids both “security is only a phase” and “load all security docs every time.”

### 5. Universal rules live once

`core/engineering.md` owns cross-cutting rules (correctness, clarity, change discipline, definition of done). Platform/technology modules add only their specific defaults and pitfalls. Security modules own controls; workflows own sequencing. The validator flags repeated long lines across files.

### 6. Quality is executable

- `scripts/validate.py`: frontmatter, name/directory match, registry integrity, required docs, relative links, module headers, size budgets, workflow completion criteria, unsafe patterns, duplicates, placeholders, license/source presence.
- `scripts/scan_project.py`: dry-run analyzer tested against real local repositories.
- `tests/scenarios.md`: 10 routing/behavior scenarios with expected module sets and failure-mode assertions.
- `tests/results.md`: execution record for validator/scanner checks plus a scenario routing audit; unexecuted scenarios are marked partial.

## Module graph

```text
SKILL.md
├── core/engineering.md            (always)
├── core/project-analysis.md       (existing/large change)
├── core/architecture.md           (design/migration)
├── core/testing.md                (test strategy)
├── workflows/*.md                 (exactly one)
├── platforms/*.md                 (one, or two for client+server)
├── technologies/**/*.md           (≤4, only if used)
├── security/baseline.md           (always)
└── security/*.md                  (attack-surface matched)
```

Dependencies point from task-specific modules toward core/security; core never depends on a technology. Templates and examples are leaves.

## Conflict resolution

1. Security constraints (hard gate).
2. Verified platform requirements.
3. Framework/library conventions.
4. Style preference.

If a requirement conflicts with a hard security constraint, the agent stops and asks for an explicit decision rather than silently weakening the control.

## Context budget (approximate)

| Load | Est. tokens |
|---|---|
| `SKILL.md` | ~2,000 |
| `core/engineering.md` | ~1,100 |
| One workflow | ~500–900 |
| One platform | ~700–1,000 |
| One technology | ~600–900 |
| `security/baseline.md` + 1–2 modules | ~1,200–2,500 |

A typical feature loads ~5,000–8,000 tokens of methodology, versus >40,000 for the whole tree. Exact counts depend on the tokenizer.

## Extension points

- Add a platform/technology module: registry entry + SKILL link + scanner signal (if detectable) + scenario when routing changes.
- Add a workflow: same pattern; it must have steps and exit criteria.
- Add a template: link it from the relevant workflow or `SKILL.md`.
- Add a security control: place it in the narrowest attack-surface module; update the gate only if it changes release blocking.

## Known limitations

- Auto-activation depends on the client's description matching.
- The scanner cannot infer architecture or intent; it only proposes signals.
- Modules are advisory; agents can ignore them. The contract makes violations visible but does not enforce them.
- Curated technology coverage is intentional; unlisted stacks rely on core + platform + official docs. There are no dedicated modules yet for Rails, Laravel/Symfony, Express/NestJS, ASP.NET, Gin, or Axum, so their framework-specific defaults are not covered.
- No runtime sandbox or policy engine is included.
