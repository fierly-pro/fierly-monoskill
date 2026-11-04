# Platform: Windows

> Load: Windows desktop app, WinUI/WPF/UWP, Windows service, or .NET Windows integration.
> Pairs with: `technologies/frameworks/dotnet.md`, `security/native.md`, `platforms/desktop.md`.

## Defaults

- WinUI 3 for new desktop UI; WPF/WinForms for existing apps. Do not mix UI frameworks without a boundary.
- Target a supported .NET version (LTS preferred) and the minimum Windows version required by the feature.
- Use MSIX for new packaged apps; keep an installer path for enterprise deployment if needed.
- Async all the way for I/O; never block the UI thread; honor cancellation and disposal.
- Store user preferences in the proper application data location; secrets in DPAPI/Credential Manager.
- Handle DPI scaling, multi-monitor, accessibility (UI Automation), keyboard navigation, and dark/light themes.

## Non-negotiables

- No secrets in the registry, plaintext config, logs, or source.
- Request the minimum UAC level (`asInvoker` unless elevation is required); isolate privileged operations in a separate, validated component.
- Long-running services run with a least-privilege account, not LocalSystem, unless justified.
- Validate all input crossing a process boundary (named pipes, COM, localhost HTTP, CLI arguments).
- Dispose GDI/COM/native handles deterministically; avoid finalizer-dependent cleanup.
- Do not disable code-signing or SmartScreen checks to ease development.

## Security

- Sign executables and installers with an EV/standard code-signing certificate; timestamp signatures.
- Auto-updates: HTTPS, signed manifests/binaries, signature verification before install, rollback path.
- Named pipes: set an explicit ACL; verify the client identity; do not expose privileged commands to all users.
- Localhost services: bind to loopback only, authenticate callers, validate `Origin` for browser-facing endpoints, and use CSRF protection.
- DPAPI: scope secrets to the user or machine as appropriate; never roam user secrets to shared locations.
- Validate file associations, protocol handlers, and drag-and-drop inputs.
- Harden the installer: per-user vs per-machine, no world-writable install directories, no unquoted service paths.

## Testing and release

- Unit tests (xUnit/NUnit/MSTest), integration tests for services/IPC, UI automation for critical flows.
- Test on a clean Windows VM, the minimum supported version, different DPI settings, and a non-admin user.
- Verify the MSIX/installer, upgrade from the previous version, uninstall, and signature.
- Check Event Viewer/ETW logging and crash dumps for sensitive data.
- Use staged rollout via the store or update channel; monitor crashes and install failures.

## Checklist

- [ ] Code signing, timestamping, and SmartScreen behavior verified.
- [ ] Manifest UAC level and service account reviewed.
- [ ] Named-pipe/localhost endpoints authenticated and ACL-restricted.
- [ ] Secrets in DPAPI/Credential Manager; logs redacted.
- [ ] Upgrade/uninstall tested on a clean VM.
- [ ] Accessibility and high-DPI behavior checked.
