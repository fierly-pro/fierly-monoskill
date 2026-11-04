# Upstream Sources

Research date: **2026-11-04**. Licenses were checked via the GitHub API and each repository's `LICENSE`/README on that date. Fierly contains original prose; no upstream code or documentation text was copied verbatim.

## Agent Skills and methodology

| Source | License | Used for | Attribution / obligation |
|---|---|---|---|
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | Apache-2.0 (code), CC-BY-4.0 (docs) | Skill format, frontmatter fields, progressive disclosure, size guidance | Structural compliance only; no text copied |
| [agentskills.io specification](https://agentskills.io/specification) | CC-BY-4.0 | Validation rules, name/directory match, reference layout | Reference; no adaptation |
| [anthropics/skills](https://github.com/anthropics/skills) | No root license detected; README states mixed Apache-2.0 and source-available | Patterns for self-contained skills and progressive disclosure | Ideas only; no copying |
| [obra/superpowers](https://github.com/obra/superpowers) | MIT | Methodology ideas: clarify before code, small plans, verification and review loops | Ideas only; no text/code copied |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | MIT | Lifecycle framing (define → plan → build → verify → review → ship), workflow granularity | Ideas only; no text copied |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | MIT | Ecosystem discovery | No content copied |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | MIT | Ecosystem discovery | No content copied |

## Security standards

| Source | License | Used for | Attribution / obligation |
|---|---|---|---|
| [OWASP Cheat Sheet Series](https://github.com/OWASP/CheatSheetSeries) | CC-BY-SA-4.0 | Control concepts for input, auth, sessions, files, APIs, databases | Paraphrased factual references; no text reproduced. Any future adaptation must comply with CC-BY-SA-4.0 |
| [OWASP ASVS](https://github.com/OWASP/ASVS) | CC-BY-SA-4.0 | Verification levels (L1/L2/L3), ASVS 5.0.0 (May 2025) | Referenced as a standard; no text copied |
| [OWASP WSTG](https://github.com/OWASP/wstg) | CC-BY-SA-4.0 | Web test categories and manual abuse cases | Referenced; no text copied |
| [OWASP MASVS](https://github.com/OWASP/masvs) | CC-BY-SA-4.0 | Mobile security baseline (with MASTG/MASWE) | Referenced; no text copied |

## Security tools (referenced, not bundled)

| Source | License | Used for |
|---|---|---|
| [github/codeql](https://github.com/github/codeql) | MIT | SAST role and command example |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | LGPL-2.1 | SAST role and command example |
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | MIT | Secret scanning role and command example |
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | Apache-2.0 | Dependency/image/IaC scanning role |
| [google/osv-scanner](https://github.com/google/osv-scanner) | Apache-2.0 | Vulnerability scanning role |
| [zaproxy/zaproxy](https://github.com/zaproxy/zaproxy) | Apache-2.0 | DAST role and authorized-use warning |

No tool is distributed, linked, or required by Fierly. Commands are examples; verify flags for the installed version.

## MCP

| Source | License | Used for |
|---|---|---|
| [modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | MIT → Apache-2.0 transition; docs CC-BY-4.0 | MCP concepts and security: confused deputy, token passthrough, SSRF, local server risk, authorization |
| [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | MIT → Apache-2.0 transition | Reference link only |
| [modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector) | MIT → Apache-2.0 transition | Testing reference link only |

MCP spec version observed at research time: `2026-07-28` documentation set. Fierly does not bundle or claim to implement an MCP server.

## Partner technology skills (ideas only)

| Source | License | Used for |
|---|---|---|
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | No license detected | Research only; no content used |
| [firebase/agent-skills](https://github.com/firebase/agent-skills) | Apache-2.0 | Firestore rules and App Check concepts (paraphrased) |
| [expo/skills](https://github.com/expo/skills) | MIT | Cross-platform research only |
| [supabase/agent-skills](https://github.com/supabase/agent-skills) | MIT | Postgres/auth research only |
| [getsentry/skills](https://github.com/getsentry/skills) | Apache-2.0 | Research only |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | MIT | Install CLI behavior and client paths (documented facts) |

## License compatibility

Fierly is released under Apache-2.0. No MIT/Apache-2.0 code was copied, so no additional notices are required. OWASP documents are CC-BY-SA-4.0; Fierly references public security concepts and standards but does not reproduce or adapt their text. If a contribution copies or adapts CC-BY-SA material, the contributor must add attribution and comply with share-alike; such content must be isolated and marked.

## Verification method

- GitHub REST API: `license.spdx_id`, `pushed_at`, `archived` (2026-11-04).
- Repository `LICENSE` files for MCP projects and specifications.
- `README.md` for projects with no detected root license.
- OWASP ASVS release page confirmed 5.0.0 (May 2025).

This register must be updated when a new upstream source is used or a license changes.
