# Installation

Fierly is a folder containing `SKILL.md`. Installation means placing that folder where your AI client discovers skills.

## Requirements

| Component | Requirement |
|---|---|
| Client | Any Agent Skills-compatible client (Claude Code, OpenCode, Cursor, Codex, Copilot, Gemini CLI, Windsurf, …) |
| Python (optional) | 3.9+ for `scripts/scan_project.py` and `scripts/validate.py` |
| Node.js (optional) | 22.20+ only for the `skills` CLI installer |
| Network | Not required at runtime. Scanners referenced by the security modules are optional and not bundled. |

## Option A — Agent Skills CLI

```bash
npx skills add <owner>/fierly-monoskill          # project scope
npx skills add <owner>/fierly-monoskill -g       # global scope
```

Select `fierly-monoskill` and your client when prompted. The CLI copies the whole skill folder, including modules, scripts, and templates.

## Option B — Manual copy or symlink

```bash
# Example: global Claude Code install
git clone <repository-url> /tmp/fierly-monoskill
cp -R /tmp/fierly-monoskill ~/.claude/skills/fierly-monoskill

# Development: symlink instead of copying
ln -s "$(pwd)" ~/.config/opencode/skills/fierly-monoskill
```

The final layout must be:

```text
<skills-dir>/fierly-monoskill/SKILL.md
<skills-dir>/fierly-monoskill/core/...
<skills-dir>/fierly-monoskill/security/...
```

The folder name must be exactly `fierly-monoskill`: the Agent Skills spec requires `name` to match the parent directory.

## Client paths

| Client | Project scope | Global scope |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `.agents/skills/` or `.opencode/skills/` | `~/.config/opencode/skills/` or `~/.agents/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.copilot/skills/` |
| Gemini CLI | `.agents/skills/` | `~/.gemini/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Antigravity | `.agents/skills/` | `~/.gemini/antigravity/skills/` |

Client-defined paths change. Verify against the client's current documentation if discovery fails. Several clients share the `.agents/skills/` convention, but not all.

## Verify

1. Start a new client session (skills are usually discovered at startup).
2. Confirm the skill is listed as `fierly-monoskill`.
3. Run:

   > Use Fierly MonoSkill to analyze this repository and propose a module plan. Do not write code yet.

4. Expected: the agent reads `SKILL.md`, runs the scanner (if it can execute Python), verifies the stack, and names a small module set within the budget.
5. Validate the copy:

   ```bash
   cd ~/.claude/skills/fierly-monoskill
   python3 scripts/validate.py
   ```

## Activation tips

- Mention “Fierly” or “use the engineering skill” for deterministic activation.
- Add a project instruction: “For engineering tasks, use `fierly-monoskill`; load only the modules it routes to.”
- Do not paste the whole skill into a system prompt; that defeats progressive disclosure.
- If the client cannot execute scripts, use `core/project-analysis.md` manually.

## Update

```bash
npx skills update fierly-monoskill
# or replace the folder with a reviewed version
```

Read [CHANGELOG.md](CHANGELOG.md) first if you forked or customized modules. Keep local changes in a fork; updates overwrite the folder.

## Uninstall

Remove the folder from the skills directory. Fierly installs no services, hooks, MCP servers, or global state.

## Troubleshooting

| Symptom | Check |
|---|---|
| Skill not listed | Folder depth (`skills/fierly-monoskill/SKILL.md`), exact folder name, frontmatter validity, client path, restart |
| Skill listed but not used | Description relevance; name the skill explicitly; check client auto-activation rules |
| Scripts fail | Python 3.9+, execute permission, path to `scan_project.py`; run from the skill folder or pass the repo path |
| Broken links after copy | Copy the entire folder, not only `SKILL.md` |
| Duplicate/stale behavior | Two copies installed (project + global); remove one and restart |
| Windows symlink errors | Use copy instead of `ln -s`, or enable Developer Mode |
| Scanner output looks wrong | It is heuristic; verify manifests/entry points; use `core/project-analysis.md` |

## Before installing

Skills are instructions executed with your agent's permissions. Review the diff/source, pin a version, and avoid installing untrusted forks. Fierly's scripts are read-only, dependency-free, and make no network calls; security scanners mentioned in the modules are separate tools you must install and authorize yourself.
