# Go

> Load: Go services, CLIs, or libraries.
> Pairs with: `platforms/backend.md`, `security/input.md`, `technologies/infrastructure/docker.md`.

## Defaults

- Return errors; wrap with context (`fmt.Errorf("load config: %w", err)`). Handle or return every error; no blank `_ =` on meaningful errors.
- Use `errors.Is`/`errors.As`; define sentinel/typed errors at package boundaries.
- Pass `context.Context` as the first parameter for I/O and long operations; honor cancellation and deadlines.
- Never start a goroutine without a shutdown path. Close channels from the sender; use `sync.WaitGroup`/`errgroup` for lifecycle.
- Keep interfaces small and consumer-defined; accept interfaces, return concrete types.
- Prefer explicit structs over `map[string]any` at boundaries; validate JSON with structs and explicit checks.
- Use `gofmt`, `go vet`, and `staticcheck`; keep `go.mod` tidy and dependencies minimal.
- Set timeouts on `http.Server`, clients, and database calls. The zero-value `http.Client` has no timeout.

## Testing and tooling

- Table-driven tests with `t.Run`; use `t.Cleanup`; `httptest` for handlers; `t.TempDir` for files.
- Run `go test -race ./...` for concurrent code. Test cancellation and error paths, not only happy paths.
- Use build tags/integration tests for real DBs; avoid network in unit tests.
- Benchmark with `-benchmem` only after correctness; use `pprof` for real profiles.

## Security

- Use `html/template` (auto-escaping), not `text/template`, for HTML. Sanitize rich text separately.
- Parameterize SQL (`database/sql` placeholders); never `fmt.Sprintf` a query.
- Avoid `os/exec` with a shell; pass args separately and allowlist commands.
- Validate paths with `filepath.Clean` + root confinement; reject traversal.
- Configure TLS with sane minimums; never `InsecureSkipVerify` in production.
- Do not log secrets; use `crypto/rand` for tokens, not `math/rand`.
- Set request body limits (`http.MaxBytesReader`), read/header timeouts, and rate limits.

## Common pitfalls

- Loop variable capture (fixed in Go 1.22+; still verify the module's `go` directive).
- Goroutine leaks on early return; always cancel derived contexts.
- Unbuffered channels blocking shutdown; select on `ctx.Done()`.
- `defer` inside loops accumulating resources.
- Large JSON bodies read fully into memory; decode with limits and streaming where needed.
- Ignoring `rows.Close()`/`rows.Err()`.

## Checklist

- [ ] Errors wrapped and handled; no ignored meaningful errors.
- [ ] Contexts, timeouts, and cancellation propagate.
- [ ] No goroutine leaks; shutdown is clean.
- [ ] `go vet`, `staticcheck`, tests, and `-race` pass.
- [ ] Input, SQL, templates, and commands are safe.
