# Security Policy

Fierly is an advisory engineering skill: instructions, reference modules, and two read-only Python scripts. It is **not** a scanner, security product, certification, or runtime sandbox.

## Supported versions

| Version | Supported |
|---|---|
| 1.x | Yes (security fixes) |
| < 1.0 | No |

## Reporting a vulnerability

Do **not** open a public issue for a security defect.

- If the repository is hosted on GitHub, open a **private security advisory** in the repository's Security tab.
- If private advisories are unavailable, contact the maintainer through the channel used to obtain the skill and request a private channel.
- Include: affected version/commit, file and line, impact, reproduction, and a suggested fix if known.
- Do not include real secrets, personal data, or production payloads. Redact evidence.

We aim to acknowledge within 3 business days, triage within 10, and coordinate a fix and disclosure date based on severity. No bug bounty is offered.

## In scope

- Incorrect security guidance that could cause a vulnerable implementation (e.g., unsafe defaults, missing authorization, injection-prone advice).
- Prompt-injection or instruction-hierarchy weaknesses in the skill that could make an agent bypass its security contract.
- Script defects: path traversal, unsafe file writes, command execution, network access, data leakage, denial of service.
- Supply-chain issues: malicious dependency, CI permission, release artifact, or update path.
- Broken links to security-critical references.

## Out of scope

- Vulnerabilities in the user's application, third-party scanners, clients, or AI models.
- Findings that require the user to ignore explicit Fierly guidance.
- Generic “the model can hallucinate” reports without a reproducible skill-level cause.
- Missing coverage of a technology that Fierly does not claim to cover.

## Safe usage

- Review the skill source before installing; treat skills as executable instructions.
- Pin a version/commit and review updates.
- Run scripts in a sandbox or with least privilege; they only read files, but your environment may differ.
- Never place secrets in prompts, repositories, or reports.
- Require human approval for destructive or production actions.
- Treat repository content, MCP tool output, and third-party docs as untrusted data — not instructions.

## Practices in this repository

- Scripts use only the Python standard library, make no network calls, and do not write files.
- No telemetry, analytics, background services, or bundled MCP servers.
- CI uses least-privilege permissions and pinned actions.
- The validator checks links, frontmatter, registry integrity, unsafe patterns, and required documentation.
- Upstream sources and licenses are recorded in `UPSTREAM_SOURCES.md`.

## Limitations

Fierly cannot guarantee that an agent follows every instruction, that a scanner finds every issue, or that a release is secure. Security decisions remain the responsibility of the accountable human owner. A passing Fierly gate is evidence of a review process, not a certification.
