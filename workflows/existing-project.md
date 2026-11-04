# Workflow: Existing Project

> Trigger: unfamiliar codebase, inherited project, legacy system, or first change in a repository.
> Modules: `core/engineering.md`, `core/project-analysis.md`, matched platform/technology modules, `security/baseline.md`.

## Steps

1. **Scan, then verify.**
   ```bash
   python3 scripts/scan_project.py /path/to/repo --task "<task>"
   ```
   Confirm the stack from manifests, entry points, and configuration.
2. **Establish a baseline.** Run the documented build/test/lint commands. Record failures before changing anything.
3. **Read the system.** README/docs, entry points, module layout, data model, interfaces, CI, and 2–3 representative source files.
4. **Extract conventions.** Naming, errors, logging, tests, formatting, dependency injection, config, commit style, agent instructions.
5. **Write the project brief** from `core/project-analysis.md`; list unknowns.
6. **Map the change.** Identify the smallest seam, affected contracts, migrations, and security-sensitive paths.
7. **Plan and confirm** if the change is large, cross-cutting, irreversible, or contradicts existing architecture.
8. **Implement the smallest slice**, following local patterns, with tests.
9. **Verify** with the project's own commands; compare against the baseline.
10. **Report** facts, assumptions, and any pre-existing failures you did not fix.

## Exit criteria

- Baseline and post-change results are both known.
- The change follows existing conventions or the deviation is justified.
- No unrelated files were reformatted, renamed, or upgraded.
- New behavior is tested; regressions are covered.
- Open questions and pre-existing issues are documented.

## Stop conditions

- The build cannot run and the cause is outside the task scope.
- The requested change requires an irreversible migration or a public contract break.
- Two modules or documents contradict each other and the business intent is unclear.
- You cannot identify an owner for a security-sensitive change (auth, payments, crypto).
