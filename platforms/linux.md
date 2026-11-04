# Platform: Linux

> Load: Linux desktop app, daemon, CLI, service, or distribution packaging.
> Pairs with: `technologies/languages/c-cpp.md` / `go` / `rust`, `security/infrastructure.md`, `security/native.md`.

## Defaults

- Follow FHS and XDG base directories (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_STATE_HOME`); never write to the user's home root or `/usr` at runtime.
- Choose packaging by audience: distro packages (deb/rpm), Flatpak, Snap, or AppImage. Ship a reproducible build and checksums.
- systemd services: dedicated user, `Restart=on-failure`, explicit `ExecStart`, no shell wrappers, logs to journald, `systemd-analyze verify` clean.
- Harden services: `NoNewPrivileges=yes`, `PrivateTmp=yes`, `ProtectSystem=strict`, `ProtectHome`, `ReadWritePaths`, `RestrictAddressFamilies`, `SystemCallFilter` where practical.
- Prefer unprivileged operation. If privileges are required, use a small, audited helper with a narrow interface (polkit/D-Bus), not a setuid binary.
- CLI: stable exit codes, `--help`, machine-readable output option, no interactive prompts in scripts, respect `NO_COLOR`/`TERM`.

## Non-negotiables

- No world-writable files/directories; create files with restrictive umask (0022 or stricter) and secrets with 0600.
- Do not run network daemons as root; bind privileged ports via capabilities or a proxy.
- Validate all paths, environment variables, and D-Bus/IPC inputs; resolve symlinks before privileged operations.
- Do not depend on a specific desktop environment unless the product does; degrade gracefully.
- Package scripts must not require network access at install time or execute unreviewed code.

## Security

- AppArmor/SELinux profiles for exposed services; seccomp filters for parsers/network daemons where supported.
- D-Bus: restrictive policy, verify sender identity, do not expose privileged methods to all users.
- systemd unit files: no `User=root` unless unavoidable; set `CapabilityBoundingSet`, `AmbientCapabilities`, and `UMask`.
- Desktop apps: portals for file access/screenshots; do not bypass the sandbox.
- Updates: signed repository metadata/packages; verify signatures; support rollback.
- Logs: journald with rate limiting; never log secrets; set retention.

## Testing and release

- Test on the oldest supported glibc/distro and a current one; use containers/VMs for the matrix.
- `shellcheck` scripts, `systemd-analyze verify` units, `lintian`/`rpmlint` packages, and integration tests for install/upgrade/remove.
- Verify the service starts after reboot, survives dependency restarts, and shuts down cleanly.
- For desktop: test Wayland and X11, HiDPI, accessibility, and portal-based file dialogs.
- Reproducible builds (`SOURCE_DATE_EPOCH`, pinned toolchain), signed artifacts, and SBOM for release.

## Checklist

- [ ] XDG paths and file permissions correct.
- [ ] Service runs unprivileged with a hardened unit.
- [ ] No setuid/world-writable paths.
- [ ] Packaging install/upgrade/remove tested on clean systems.
- [ ] Signatures and update path verified.
- [ ] Logs redacted and retention configured.
