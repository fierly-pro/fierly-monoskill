# Spring Boot

> Load: Spring Boot (Java/Kotlin) services.
> Pairs with: `platforms/backend.md`, `security/api.md`, `security/auth.md`, `technologies/databases/postgresql.md`.

## Defaults

- Constructor injection; avoid field injection and circular dependencies.
- Externalize configuration with profiles/environment; validate with `@ConfigurationProperties` + `@Validated`. Never commit secrets.
- Keep controllers thin; put transactions and domain rules in services. Use `@Transactional` on service boundaries, not controllers.
- JPA: avoid N+1 with fetch joins/entity graphs or projections; do not expose entities directly; use DTOs.
- Use Flyway/Liquibase for migrations; disable automatic schema generation in production (`ddl-auto=validate` or `none`).
- Set timeouts for HTTP clients, DB pools, and async executors; define graceful shutdown.
- Actuator: expose only required endpoints, secure them, and never expose `/env`, `/heapdump`, or detailed health to the public.

## Security

- Spring Security filter chain: explicit permit/deny rules, deny by default. Method security (`@PreAuthorize`) for object-level checks where needed.
- Stateless APIs: validate JWT/OAuth2 tokens (issuer, audience, signature, expiry) via the resource server; do not roll your own.
- Session apps: secure cookies, CSRF enabled, session fixation protection, logout invalidation.
- Password storage: `PasswordEncoder` with bcrypt/Argon2; never custom hashing.
- CORS: explicit origins/methods/headers; no wildcard with credentials.
- Validate request DTOs with Bean Validation; enforce size limits at the edge.
- Do not log credentials/tokens; configure logging redaction.
- Keep dependencies patched; Spring Boot patch versions matter.

## Testing

- `@SpringBootTest` for integration; slice tests (`@WebMvcTest`, `@DataJpaTest`) for focused coverage; Testcontainers for real DB/broker.
- Test security rules explicitly (anonymous, user, admin, other tenant).
- Test migrations against a real database.
- Avoid mocking the persistence layer when testing queries; use a real test database.

## Operations

- Build an executable jar or container image; pin the JDK and dependencies.
- Health/readiness probes; metrics via Micrometer; structured logs with correlation IDs.
- Configure connection pools and thread pools from measured limits, not defaults.
- Graceful shutdown and readiness during rollout.
- Run `mvn/./gradlew verify` with dependency and static analysis checks in CI.

## Checklist

- [ ] Deny-by-default security chain; object-level checks verified.
- [ ] DTO validation and error handling consistent.
- [ ] N+1 queries and transaction boundaries checked.
- [ ] Migrations validated; `ddl-auto` safe in production.
- [ ] Actuator and management endpoints secured.
- [ ] Dependency and container scans triaged.
