# Agent Integration

> Load: installing, activating, or troubleshooting Fierly in an AI client.
> Fierly follows the Agent Skills format (`SKILL.md` + YAML frontmatter + on-demand files).

## Install

### Generic (Agent Skills CLI, recommended)

```bash
npx skills add <owner>/fierly-monoskill        # after the repository is published
npx skills add <owner>/fierly-monoskill -g     # global, all projects
```

The CLI copies the skill into the client's skills directory. Node.js 22.20+ is required. Verify the installed folder contains `SKILL.md` and the module directories.

### Manual

Copy or symlink the repository folder (the folder containing `SKILL.md`) into the client's skills directory. The folder name must remain `fierly-monoskill` to match the `name` field.

| Client | Project | Global |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `.agents/skills/` or `.opencode/skills/` | `~/.config/opencode/skills/` or `~/.agents/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.copilot/skills/` |
| Gemini CLI | `.agents/skills/` | `~/.gemini/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |

Paths are client-defined and may change; verify against the client's current documentation. The generic `.agents/skills/` convention is supported by several clients but not all.

### Verify

- The client lists `fierly-monoskill` as an available skill.
- Ask: “Use Fierly MonoSkill to analyze this repository and propose a module plan.”
- The agent should read `SKILL.md`, run `scripts/scan_project.py`, and load only the matched modules.
- If the skill does not appear, check the folder depth (`skills/fierly-monoskill/SKILL.md`), frontmatter validity, and the client's skills path.

## Activation

- Clients load only the `name` and `description` at startup; the description is written to match engineering tasks.
- Mention “Fierly” or “use the engineering skill” when you want deterministic activation.
- For always-on behavior, add a short project instruction (e.g., `AGENTS.md`/`CLAUDE.md`): “For engineering tasks, use the `fierly-monoskill` skill; load only the modules it routes to.”
- Fierly works without MCP, hooks, plugins, or client-specific features.

## Compatibility

- Format-validated against the Agent Skills specification and OpenCode's documented loader.
- Actual behavior (auto-activation, file access, script execution) depends on the client. Test in your environment.
- Scripts require Python 3.9+; they are optional. If the client cannot execute them, perform the analysis manually with `core/project-analysis.md`.
- The client may impose its own limits (context window, allowed tools, file access). Fierly's module budget keeps activation small but cannot override those limits.

## Updating and removal

- Update by replacing the skill folder or re-running the installer; keep local changes in a fork.
- Remove the folder from the client's skills directory. No global state or background service is installed.
- Check `CHANGELOG.md` for breaking module renames before updating a customized copy.
