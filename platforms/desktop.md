# Platform: Desktop Shell

> Load: Electron, Tauri, Qt, GTK, or .NET desktop shell.
> Pairs with: the target OS module (`macos`, `windows`, `linux`), `security/native.md`, `platforms/cross-platform.md`.

## Process model

- **Electron:** main process owns privileged APIs; renderer is untrusted web content. `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`. Expose a minimal, validated preload API; never expose `ipcRenderer` or Node globals.
- **Tauri:** commands are the boundary; use capabilities/allowlists, validate every argument, and keep filesystem/shell/updater scopes narrow.
- **Qt/.NET:** keep UI and privileged services separate; validate IPC (D-Bus, named pipes) and file inputs.
- Treat all remote content, plugin content, and deep-link parameters as untrusted.

## Security

- Enforce CSP in the renderer; block remote code and `eval`; allowlist navigation and `window.open`.
- Sanitize untrusted Markdown/HTML with a maintained allowlist renderer; disable raw HTML when the format does not require it.
- Validate IPC sender identity, channel, and payload schema; never execute arbitrary commands or paths from the renderer.
- Do not disable `webSecurity`, TLS verification, or the sandbox to fix a feature.
- Store secrets in the OS keystore, not in localStorage, config files, or the bundle. Client bundles are public.
- Auto-updates: HTTPS, signed manifests/artifacts, signature verification before install, staged rollout, rollback. Never auto-update from an unauthenticated source.
- Code-sign and notarize per OS; sign installers and update metadata.
- Local data: encrypt sensitive stores; define retention and logout cleanup; exclude secrets from crash reports.

## UX and operations

- Single-instance behavior, deep links, file associations, tray/menu bar, and window state restoration.
- Handle offline mode and local data conflicts explicitly; define sync/merge rules.
- Bound memory/bundle size; lazy-load heavy modules; measure startup time.
- Graceful shutdown: flush data, stop background work, release single-instance locks.
- Crash reporting with redaction and user consent where required.

## Testing and release

- Unit tests for main-process logic; E2E with Playwright (`_electron`) or WebDriver for Tauri/Qt; test IPC with hostile payloads.
- Package and test on clean VMs for every supported OS; verify install, upgrade from the previous version, and uninstall.
- Test auto-update end-to-end, including a tampered/unsigned artifact rejection.
- Verify signatures/notarization and store compliance; keep a rollback build available.

## Checklist

- [ ] Renderer sandboxed; IPC surface minimal and validated.
- [ ] CSP and navigation allowlist enforced.
- [ ] Secrets in OS keystore; none in the bundle.
- [ ] Updater signatures verified and rollback tested.
- [ ] Install/upgrade/uninstall tested on clean VMs.
- [ ] Deep links, file associations, and single-instance behavior reviewed.
