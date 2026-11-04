# .NET

> Load: C#/.NET services, desktop apps, or libraries.
> Pairs with: `platforms/backend.md`/`windows.md`, `security/api.md`, `technologies/databases/postgresql.md`.

## Defaults

- Use a supported LTS .NET version; pin the SDK in `global.json` and the target framework in project files.
- Enable nullable reference types and treat warnings seriously; avoid `!` on external data.
- Async all the way for I/O; never `.Result`/`.Wait()`; pass `CancellationToken`.
- Constructor injection; register services with the correct lifetime (`Singleton` must be thread-safe; `Scoped` for per-request state).
- Validate options at startup (`ValidateOnStart`), bind from configuration, and never commit secrets.
- EF Core: use migrations, avoid N+1 with `Include`/projections, use `AsNoTracking` for reads, and keep transactions short. Do not expose entities directly.
- `HttpClient` via `IHttpClientFactory`; set timeouts and resilience policies deliberately.
- Dispose `IDisposable`/`IAsyncDisposable`; do not rely on finalizers.

## ASP.NET Core security

- Deny by default: `[Authorize]` globally or per endpoint; explicit `[AllowAnonymous]` only where intended.
- Authorize at the resource (ownership/tenant), not only by role. Use policy-based authorization.
- Validate DTOs with DataAnnotations/FluentValidation; enforce request size limits.
- Protect against over-posting with explicit DTOs; never bind EF entities directly.
- Configure CORS explicitly; no wildcard with credentials. Enable antiforgery for cookie-auth writes.
- Data Protection keys must be persisted/shared in multi-instance deployments; protect them.
- Use ASP.NET Core Identity or a vetted OIDC provider; hash passwords with the framework defaults (PBKDF2/Argon2 configured).
- Never log tokens, passwords, or PII; use structured logging with redaction.
- Keep framework packages patched; run `dotnet list package --vulnerable`.

## Testing

- xUnit/NUnit/MSTest; `WebApplicationFactory` for integration; Testcontainers for DB/broker.
- Test authorization policies with anonymous/user/admin/other-tenant identities.
- Test EF queries against a real database, not the in-memory provider, when behavior matters.
- Add architecture tests for dependency direction where the project uses them.

## Build and release

- `dotnet build`/`test` with analyzers; publish self-contained or framework-dependent deliberately.
- Trimming/AOT: verify reflection, serialization, and EF compatibility; test the published artifact.
- Build an immutable container or installer; scan dependencies and the image.
- Configure health checks, graceful shutdown, and readiness for rolling deploys.

## Checklist

- [ ] Nullable enabled; async/cancellation correct.
- [ ] Authorization deny-by-default and object-level.
- [ ] EF queries efficient; migrations reviewed.
- [ ] Secrets external; Data Protection keys shared.
- [ ] Published artifact tested, not just the debug build.
