# Docker

> Load: Dockerfiles, Compose, or containerized builds.
> Pairs with: `security/infrastructure.md`, `security/supply-chain.md`, `technologies/infrastructure/kubernetes.md`.

## Image design

- Use multi-stage builds: build with toolchains, copy only runtime artifacts into a minimal final image (distroless/alpine/slim as appropriate).
- Pin base images by digest for reproducibility; rebuild regularly for patches.
- Run as a non-root user with an explicit UID/GID; set a read-only root filesystem where possible.
- Combine `RUN` steps and clean package caches in the same layer; order layers for cache efficiency (dependencies before source).
- Use `.dockerignore` to exclude `.git`, secrets, tests, and build artifacts.
- Do not install compilers/curl in the runtime image unless required; each tool is attack surface.

## Runtime

- Use exec-form `ENTRYPOINT`/`CMD` so the process receives signals; handle `SIGTERM` and shut down gracefully.
- Add a `HEALTHCHECK` only when the orchestrator does not provide one; expose liveness/readiness endpoints for Kubernetes.
- Limit CPU/memory/PIDs at runtime; set `ulimits` where needed.
- Log to stdout/stderr in structured form; do not write secrets/PII.
- Persist data in volumes, not the container filesystem; define ownership/permissions.

## Security

- Never bake secrets into images or `ARG`s that persist in history; mount them at runtime or use a secret manager.
- Drop Linux capabilities (`--cap-drop=ALL`, add only what is needed), set `no-new-privileges`, and use seccomp/AppArmor profiles.
- Do not run `--privileged` or mount the Docker socket into application containers.
- Scan images (`trivy image`) and generate an SBOM; block critical findings by policy.
- Sign images and verify signatures/digests before deploy.
- Keep the daemon/rootless configuration hardened; restrict who can build/deploy.

## Compose and local development

- Pin image versions; avoid `latest`.
- Use healthchecks and `depends_on: condition: service_healthy` for ordering.
- Keep development secrets in an ignored `.env`; provide `.env.example`.
- Do not expose databases/admin ports publicly; bind to `127.0.0.1` for local tools.
- Match production versions of databases/runtimes to avoid drift.

## Build performance

- Cache dependency layers; use BuildKit cache mounts for package managers.
- Build multi-arch images only when needed; use the native platform for CI speed.
- Keep the final image small; measure size and startup time.

## Checklist

- [ ] Multi-stage, pinned base, non-root, minimal runtime.
- [ ] No secrets in layers/history; `.dockerignore` present.
- [ ] Signals/graceful shutdown and health checks work.
- [ ] Image scanned and signed; digest recorded.
- [ ] Runtime limits and read-only filesystem where possible.
