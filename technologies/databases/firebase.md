# Firebase / Firestore

> Load: Firebase apps, Firestore, Storage, Cloud Functions, or security rules.
> Pairs with: `platforms/web.md`/`android.md`/`ios.md`, `security/database.md`, `security/auth.md`.

## Data model and queries

- Model from access patterns; denormalize for reads and define consistency. Keep documents small; avoid unbounded arrays.
- Composite indexes for multi-field queries; Firestore requires them for many combinations. Review index builds and costs.
- Paginate with `startAfter` cursors, not offsets.
- Use batched writes/transactions for multi-document invariants; keep them short (limits apply).
- Real-time listeners cost reads on every change; scope queries and detach listeners.

## Security rules (the primary authorization layer for client access)

- **Default deny** at the top level; grant per collection/document and per operation.
- Verify `request.auth != null` and the exact ownership/tenant claim; never trust a client-supplied `userId`/`role`.
- Validate field types and allowed keys on writes; prevent privilege escalation by blocking writes to role/admin fields.
- Rules are filters, not queries: a client query must be provably allowed by the rule. Test both allow and deny cases.
- Admin SDK bypasses rules — use it only on trusted servers and still enforce application authorization.
- Custom claims are set server-side only; propagate/refresh token claims deliberately.
- Test rules with the emulator and automated rule tests for every collection and role.

## Storage and Functions

- Storage rules: default deny, path-scoped ownership, size/content-type limits, no public write.
- Cloud Functions: verify auth/App Check, validate input, rate-limit expensive operations, keep secrets in Secret Manager, set timeouts/memory, handle retries idempotently.
- Do not expose admin credentials or service-account keys to clients; use App Check and least-privilege service accounts.
- Watch cold starts and invocation costs; avoid recursive triggers.

## Security and operations

- Enable App Check for public apps where appropriate; it reduces abuse but is not authentication.
- Restrict API keys by platform/app/bundle and API surface; Firebase API keys are identifiers, not secrets — rules are the security boundary.
- Backups: export Firestore regularly (managed export) and test restore; Storage lifecycle/retention.
- Monitor usage/cost anomalies, failed rules, function errors, and auth abuse.
- Keep SDKs and rules deployed from version control; review rules changes like code.

## Checklist

- [ ] Rules default-deny with ownership/tenant checks and field validation.
- [ ] Rule tests cover allow and deny for every role.
- [ ] Indexes match queries; listeners scoped.
- [ ] Service-account keys server-only; App Check configured where useful.
- [ ] Exports/backups tested; cost and abuse alerts set.
