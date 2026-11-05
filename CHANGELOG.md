# Changelog

All notable changes to Fierly MonoSkill are documented here. Format follows Keep a Changelog; versions follow Semantic Versioning.

## [1.0.0] - 2026-11-04

### Added

- Single Agent Skills entry point (`SKILL.md`) with activation contract, routing tables, module budget, universal loop, hard stops, and reporting contract.
- Universal core: engineering principles, project analysis, architecture, testing.
- 12 workflows: new project, existing project, feature, bugfix, refactor, architecture, code review, testing, security review, performance, dependencies, release.
- 9 platform modules: web, backend, Android, iOS, macOS, Windows, Linux, cross-platform, desktop.
- 23 technology modules: TypeScript, Python, Kotlin, Swift, Go, Rust, C/C++, SQL; React, FastAPI, Django, Spring Boot, .NET, Flutter; PostgreSQL, SQLite, MongoDB, Redis, Firebase/Firestore; Docker, Kubernetes, CI/CD, cloud.
- Security Shield: baseline/threat modeling, input, auth, database, API, frontend, native, infrastructure, supply chain, security testing, release gate.
- Machine-readable `registry.json`, dependency-free `scripts/scan_project.py`, and `scripts/validate.py`.
- Templates: ADR, threat model, review report, security gate.
- 10 evaluation scenarios, rubric, and a results record with executed tooling checks plus a routing audit.
- Installation, quick start, architecture, contributing, security policy, upstream source register, Apache-2.0 license.
- CI validation workflow.

### Security

- Release gate with blocking critical findings and accountable risk acceptance for high findings.
- Explicit anti-patterns for injection, authz, secrets, TLS, CORS, uploads, deserialization, CI permissions, and artifact signing.
- MCP integration guidance treats tools, descriptions, and outputs as untrusted.

### Fixed

- Validator ignores `.git`, dependency, and cache directories, so a normal checkout with empty Git internals does not fail CI.
- Scanner treats “export” as a word, not as the Expo framework, and states the security-module cap.
