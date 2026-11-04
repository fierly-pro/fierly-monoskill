# Input Protection

> Load: user input, HTML, files, parsers, queries, shell/process execution, or rich text.
> Pairs with: `security/baseline.md`, `security/auth.md` (SSRF/redirects), `security/frontend.md` (XSS/CSP).

## Model

1. **Classify the source** — trusted (code/config) vs untrusted (request, file, webhook, third-party API, LLM/tool output).
2. **Validate at the boundary** — allowlist format, type, length, range, encoding, and business rules.
3. **Canonicalize once** — decode/normalize before validation; validate the same representation you use.
4. **Encode at the sink** — output encoding depends on context (HTML, attribute, JS, URL, CSS, SQL, shell).
5. **Reject or sanitize deliberately** — prefer rejection for structured input; sanitize only rich text with a maintained sanitizer.

Do **not** globally strip or ban `<`, `>`, `"`, `'`, `;`, or `--`. These are legitimate data. Blocklists cause false rejection and bypasses. Use context-aware encoding and safe APIs.

## Injection

**SQL**
- Use parameterized queries or a query builder with bound parameters. Never concatenate untrusted values.
- Identifiers (table/column names) cannot be parameterized: map them through a strict allowlist.
- ORM raw fragments, `ORDER BY`, and `LIKE` still need handling; escape wildcards where semantics require it.
- Apply least-privilege DB roles; the app should not own the schema.

**NoSQL**
- Reject object/operator injection: validate that user-supplied filters are scalars; never pass raw JSON into query operators.
- Explicitly allow fields and operators; block keys beginning with `$` from user input.

**OS command**
- Avoid the shell. Pass an argument array (`execve`, `subprocess.run([...], shell=False)`).
- Allowlist command/target; validate paths; never interpolate user text into a shell string.
- Run with least privilege and a timeout; capture output safely.

**Templates / expression languages**
- Do not compile or evaluate user-controlled templates. Use logic-less templates or a sandbox with a strict context.
- Treat template names and includes as untrusted input; resolve against an allowlist.

**LDAP, XPath, headers, logs**
- Escape per the target grammar; strip CR/LF from values written to logs or headers (log/header injection).
- Validate redirect targets and protocol schemes.

**CSV / spreadsheet export**
- Treat exported cell values and headers as untrusted. A value starting with `=`, `+`, `-`, `@`, tab, or CR can execute as a formula when opened in Excel/Sheets (CSV/formula injection).
- Escape by prefixing a single quote or a tab per the consumer's rules, or force text encoding; do not only quote the field. Test values such as `=1+1`, `@SUM(1,1)`, and leading whitespace/control characters.
- Keep exports server-generated and authorization-filtered; never let the client supply the column set or row filter.

**Deserialization**
- Never deserialize native object formats (pickle, Java serialization, unsafe YAML) from untrusted data.
- Use JSON with an explicit schema; use safe YAML loaders; reject unknown fields where appropriate.

**XXE**
- Disable external entities and DTDs in XML parsers; prefer a hardened parser configuration.

## XSS and output encoding

- Encode for the exact context: HTML text, HTML attribute, JavaScript string, URL component, CSS.
- Prefer framework auto-escaping; avoid bypass APIs (`innerHTML`, `dangerouslySetInnerHTML`, `v-html`, raw filters).
- Rich text: sanitize with a maintained allowlist sanitizer on the server when possible; store sanitized HTML and re-sanitize on render if trust changes.
- Validate URLs: allow only `http`/`https` (and explicit schemes); block `javascript:`, `data:` where not needed.
- Add CSP as defense in depth (see `security/frontend.md`). CSP does not replace encoding.

## Path traversal and files

- Resolve the final path and verify it remains inside the intended root (`realpath` + prefix check); reject symlinks that escape.
- Never pass user input as an absolute path or as a path segment without validation.
- Uploads: enforce size limits before reading, validate content type by magic bytes, generate random server-side names, store outside the web root, never execute uploaded content, re-encode images, cap archive expansion, and scan where appropriate.
- Serve downloads with `Content-Disposition: attachment` and a safe content type where applicable.

## Unicode and size

- Normalize (e.g., NFKC) when the domain requires it, but be consistent between validation and use.
- Reject NUL bytes and invalid encodings; define behavior for overlong sequences and unpaired surrogates.
- Enforce request body, field, array, file, and decompression limits at the edge and in the application.
- Bound regex complexity and parser depth; fuzz parsers that accept complex formats.

## Verification

- Test with valid, boundary, malformed, and adversarial inputs: quotes, angle brackets, null bytes, Unicode confusables, oversized payloads, traversal sequences, encoded variants.
- Confirm the sink behavior, not just the validator: inspect the rendered HTML, executed query, command argv, and filesystem path.
- Add regression tests for every fixed injection or traversal defect.
