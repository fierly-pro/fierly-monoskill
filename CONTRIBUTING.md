# Contributing

Fierly is a compact engineering system, not a content collection. Contributions are judged by usefulness per token, correctness, and consistency with the router.

## Before adding anything

- Is the knowledge already in `core/` or a security module? Link to it instead of repeating it.
- Is it specific to one platform/technology? Put it in that module, not in `SKILL.md`.
- Is it a stable, verifiable practice? No speculation, no vendor marketing, no deprecated APIs.
- Does the agent need it at task time? If not, it does not belong in a module.

## Module contract

Every module in `core/`, `workflows/`, `platforms/`, `technologies/`, and `security/` must:

1. Start with a one-line purpose and a load condition:
   ```markdown
   > Load: <when this module is relevant>.
   > Pairs with: <related modules>.
   ```
2. Contain actionable guidance: defaults, procedures, checklists, failure modes, verification.
3. Stay focused. Prefer one dense module over several thin ones.
4. Link related modules with relative paths; do not duplicate their rules.
5. End with concrete completion/verification criteria where the module describes a process.
6. Avoid placeholders (`TODO`, `TBD`) and unverified claims. Mark uncertainty explicitly.

There is no artificial line limit, but the validator warns above ~3,500 estimated tokens. Split only when the module serves clearly different tasks.

### Naming

- Use lowercase kebab-case file names that match the registry key (`spring-boot.md`, not `SpringBoot.md`).
- Do not add nested `SKILL.md` files. Fierly is one skill; subfolders are reference material.
- Do not create empty directories or "planned" modules.

## Routing changes

A new or renamed module requires all of:

1. A `registry.json` entry with `path`, detection `signals` (and `kind` for technologies).
2. A link in `SKILL.md`'s routing table.
3. Scanner support if the module is detectable (language extension, manifest, dependency, path).
4. An evaluation scenario in `tests/scenarios.md` if routing behavior changes.
5. `python3 scripts/validate.py` passing.

## Security content

- Never recommend disabling TLS verification, authentication, sandboxing, CSRF protection, or authorization checks.
- Do not ban characters (`<`, `>`, quotes, semicolons) as a generic defense; require context-aware encoding and parameterization.
- Do not present a scanner as proof of security or a tool as a certification.
- Prefer primary sources: OWASP ASVS/Cheat Sheets, platform documentation, language/framework docs. Record upstream sources and licenses.
- Include exploit preconditions and verification steps, not just “validate input”.
- If a recommendation depends on a version or configuration, say so.

## Licensing and attribution

- Contributions are accepted under Apache-2.0.
- Do not paste text from incompatible licenses. OWASP materials are CC-BY-SA-4.0; use facts and paraphrase with attribution, or clearly mark adapted content and comply with share-alike.
- Add every new upstream source to `UPSTREAM_SOURCES.md` with license, usage, and verification date.
- Do not copy code without checking its license and attribution requirements.

## Validate and test

```bash
python3 scripts/validate.py
python3 scripts/scan_project.py . --task "test routing"   # smoke test the scanner
```

Before a PR:

- [ ] `scripts/validate.py` passes (0 errors).
- [ ] Relative links resolve; no nested `SKILL.md`.
- [ ] Registry, `SKILL.md`, scanner, and scenarios are consistent.
- [ ] No duplicated universal rules; no placeholders.
- [ ] Security guidance is correct and does not weaken defaults.
- [ ] `UPSTREAM_SOURCES.md` updated for new sources.
- [ ] The diff is focused; no unrelated reformatting.

## Commits and PRs

- One logical change per commit; imperative message (`add kotlin coroutine pitfalls`).
- Explain the problem, the module decision, and how you verified it.
- Sign off (`git commit -s`) if your organization requires DCO.
- Expect review on correctness, density, routing, security, and license compatibility.

## Review criteria

A contribution is accepted when it is accurate, useful at task time, consistent with the core, correctly routed, and adds more value than context cost. Volume is not a criterion.
