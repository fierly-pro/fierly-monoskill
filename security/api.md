# API Security

> Load: HTTP/REST, GraphQL, gRPC, WebSocket, webhook, or any network-facing contract.
> Pairs with: `security/auth.md`, `security/input.md`, `security/api`-related platform module.

## Every endpoint

- **Authenticate** unless explicitly public. Make the public list reviewable and minimal.
- **Authorize at the resource** for the specific object and action; never rely on route-level checks alone.
- **Validate** path, query, headers, body, and content type against a schema. Reject unknown fields where mass assignment is a risk; allowlist writable fields.
- **Bound** body size, array length, pagination, upload size, execution time, and query complexity.
- **Rate-limit** per identity/IP/tenant; distinguish cheap reads from expensive writes and exports.
- **Return** stable error codes and a correlation ID; never stack traces, SQL, internal hostnames, or secrets.
- **Log** the security-relevant outcome without credentials, tokens, or sensitive payloads.

## Response exposure

- Use explicit response DTOs/allowlists; never serialize ORM entities or internal objects directly.
- Do not expose internal IDs when they enable enumeration; use unguessable identifiers where appropriate.
- Set correct cache headers for authenticated/personal data (`Cache-Control: no-store` where needed).
- Avoid verbose differences between "not found" and "forbidden" when they leak existence.

## CORS

- Allowlist exact origins; never reflect arbitrary `Origin`.
- Do not combine `Access-Control-Allow-Origin: *` with credentials.
- Allow only required methods/headers; keep preflight caching bounded.
- CORS is a browser read control, **not** authentication or authorization.

## Webhooks

- Verify an HMAC signature over the raw body with a shared secret; compare in constant time.
- Enforce a timestamp window and a replay cache; reject stale/duplicate deliveries.
- Validate the payload schema after signature verification; process idempotently.
- Return quickly, queue slow work, and define retry/backoff behavior.
- Never trust the source IP alone; support secret rotation.

## GraphQL

- Enforce authentication/authorization per field/resolver, not only at the gateway.
- Limit query depth, complexity, aliases, and batch size; disable or restrict introspection in production as defense in depth.
- Prevent unbounded nested queries and N+1 resolver patterns.
- Validate variables and avoid exposing internal error details.

## WebSocket and real-time

- Authenticate during the handshake and authorize each subscription/message; do not trust a one-time query token.
- Validate `Origin` for browser clients; use CSRF protections where cookies authenticate the handshake.
- Enforce message size/rate limits, connection limits, and idle timeouts.
- Re-check authorization when permissions change; close or downgrade affected connections.

## gRPC and service-to-service

- Use mutual TLS or workload identity; do not rely on network location.
- Set deadlines, message size limits, and retry policies; propagate correlation IDs.
- Authorize the caller per method/resource; validate protobuf fields as untrusted input.
- Keep admin/internal services off the public network.

## Versioning and lifecycle

- Version breaking changes; deprecate with a timeline and telemetry on old-client usage.
- Keep OpenAPI/schema documentation accurate, but treat documentation as metadata — not a security control.
- Remove debug endpoints, verbose health details, and test hooks from production.
- Apply idempotency keys to retryable writes (payments, orders, provisioning).

## Verification

- Enumerate every route and confirm authn/authz; test with anonymous, normal user, other tenant, and admin.
- Try mass assignment, oversized payloads, malformed content types, and method overrides.
- Confirm CORS with a hostile origin; confirm webhook replay and invalid signatures are rejected.
- Check error responses and logs for leaked secrets or PII.
