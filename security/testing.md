# Security Testing

> Load: security review, scanner setup/triage, or verification of a security fix.
> Pairs with: `security/gate.md`, `workflows/security-review.md`, platform testing guides.

## Tool map

| Tool | Finds | Limits |
|---|---|---|
| Semgrep | Pattern-based SAST across many languages; custom rules | Misses logic/authz flaws; rules need tuning |
| CodeQL | Deep semantic SAST; data-flow queries | Needs a build; language support varies; slower |
| Gitleaks | Secrets in Git history, files, staged changes | Only known patterns; entropy false positives |
| Trivy | Dependency/image/IaC/secret misconfigurations | Coverage depends on ecosystem and DB freshness |
| OSV-Scanner | Known vulnerabilities in lockfiles/manifests | Only known CVEs; no logic flaws |
| ZAP | Dynamic web scanning (spider/active/passive) | Needs authorization; cannot judge business logic |
| Platform tools | Android/iOS/desktop static analysis, manifest checks | Platform-specific; not a full pentest |

Run scanners only on systems you are authorized to test. Treat every finding as a lead requiring triage.

## Commands (verify flags with `--help` for the installed version)

```bash
# SAST
semgrep scan --config auto .
codeql database create codeql-db --language=<lang>
codeql database analyze codeql-db <query-pack> --format=sarif-latest --output=results.sarif

# Secrets
gitleaks detect --source . --redact
gitleaks protect --staged --redact

# Dependencies, images, IaC
trivy fs --scanners vuln,secret,misconfig .
trivy image <image>:<tag>
osv-scanner scan source -r .

# Dynamic (authorized targets only)
docker run --rm -t zaproxy/zap-stable zap-baseline.py -t https://target.example
```

Record tool version, ruleset/query pack, scope, and date. A scanner that was not run is not evidence.

## Triage

1. **Validate** the finding: is the sink reachable? Is the input attacker-controlled? Is the vulnerable path deployed?
2. **Check exploitability** with a safe reproduction in a non-production environment.
3. **Classify** severity by impact and preconditions; distinguish confirmed from suspected.
4. **Fix at the root** (parameterization, encoding, authz), not by suppressing the rule.
5. **Add a regression test** or a repeatable manual check.
6. **Record** false positives with justification and a rule-tuning note; never blanket-disable.

## Manual abuse cases

Automated tools do not find broken business logic. Test at least:

- IDOR: access another user's/tenant's object by changing an identifier.
- Vertical escalation: perform an admin action with a normal account.
- Auth bypass: missing auth on a route, method override, alternate content type, direct object reference.
- Injection: SQL/NoSQL/command/template/path traversal with encoded variants.
- File upload: executable content, double extension, content-type mismatch, oversized/zip bomb.
- SSRF: internal metadata, localhost, DNS rebinding, redirect chains.
- CSRF and CORS: state-changing request from a hostile origin.
- Session: fixation, replay after logout, expired token, concurrent sessions.
- Rate limits: credential stuffing, OTP brute force, expensive query abuse.
- Webhooks: invalid signature, stale timestamp, replay, oversized payload.

Map web coverage to OWASP WSTG, mobile to MASVS/MASTG, and requirements to ASVS 5.0.

## Fuzzing and parsers

Use property-based tests or fuzzing for parsers, protocol decoders, file formats, and anything handling untrusted bytes. Define invariants (no panic, no out-of-bounds, bounded memory/time) and run with sanitizers where available.

## Evidence

Report: scope, tools/versions, commands, findings with severity and evidence, fixes, retests, and residual risk. State explicitly what was **not** tested. A clean scan is not a security guarantee.
