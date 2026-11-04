# Platform: Cross-Platform

> Load: Flutter, React Native/Expo, Kotlin Multiplatform, .NET MAUI, or a shared core across iOS/Android/desktop/web.
> Pairs with: platform modules for the targets, `security/native.md`, `technologies/frameworks/flutter.md`.

## Choose the strategy from constraints

| Option | Best fit | Costs |
|---|---|---|
| Flutter | Custom UI with high parity, fast iteration | Dart ecosystem, larger binary, platform-channel work for deep native APIs |
| React Native/Expo | JS/TS team, app-like UI, OTA updates (with constraints) | Native module gaps, JS bridge/perf tuning, upgrade churn |
| Kotlin Multiplatform | Shared business logic, native UI | Two UI stacks, Kotlin/Swift interop, build complexity |
| .NET MAUI | C#/.NET team, enterprise integration | UI maturity varies, platform-specific handlers |
| Tauri/Electron | Shared web UI on desktop | Web security model, binary size/memory (Electron), native APIs via Rust/sidecar |

Decide based on UI fidelity, native API access, team skills, performance, binary size, store rules, and long-term maintenance — not only code sharing.

## Architecture

- Share domain rules, data models, networking, and validation; keep platform UI idiomatic unless parity is a hard requirement.
- Put platform-specific behavior behind narrow adapters; never leak platform types into shared modules.
- Define a feature-parity matrix; explicitly accept platform differences (permissions, back navigation, notifications).
- Keep one source of truth for API contracts and business rules; validate on the server regardless of client.
- Plan for plugin quality: maintenance, permissions, native code, and upgrade compatibility.

## Security

- Use the platform keystore through the framework's secure storage; verify it is not a plaintext fallback.
- TLS everywhere; do not disable certificate validation in shared HTTP clients. Pinning needs a rotation plan.
- Deep links/universal links: validate scheme/host/path in shared and native code.
- WebViews: restrict navigation, disable unnecessary JS bridges, keep engines patched.
- No secrets in the shared bundle — all client code is public.
- Signing, entitlements, and store privacy declarations are per platform; do not assume shared configuration covers them.

## Testing and release

- Unit tests for shared logic; widget/component tests per UI; integration tests on real devices/emulators for each target.
- CI matrix with the supported OS/SDK versions; cache toolchains but verify clean builds.
- Test upgrade from the previous app version and migration of local data.
- OTA updates: verify store policy compliance, code signing, rollback, and version compatibility. Never use OTA to bypass review for prohibited changes.
- Release each platform through its store with staged rollout and crash monitoring.

## Checklist

- [ ] Feature-parity matrix and accepted differences documented.
- [ ] Secure storage verified on every target.
- [ ] Deep links, permissions, and WebViews reviewed per platform.
- [ ] CI builds/tests every supported target.
- [ ] Signing and privacy declarations per store completed.
- [ ] Local data migration and upgrade path tested.
