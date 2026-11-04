# Flutter

> Load: Flutter/Dart apps or shared mobile/desktop UI.
> Pairs with: `platforms/cross-platform.md`, `platforms/android.md`/`ios.md`, `security/native.md`.

## Defaults

- Use the project's state approach consistently (setState for local, Riverpod/Bloc/provider for shared). Do not mix patterns in one feature.
- Widgets stay small and composable; extract when build methods grow or rebuild too often. Use `const` constructors.
- Keys for reorderable/dynamic lists; stable identity, not indexes.
- Async: `FutureBuilder`/`StreamBuilder` with explicit loading/error/empty states; cancel/ignore stale results; never block the UI isolate.
- Navigation: one router approach; deep links validated; handle back behavior per platform.
- Platform channels: define a typed contract, validate arguments on the native side, and handle missing implementations.
- Persistence: `shared_preferences` for non-sensitive flags, SQLite/Drift/Isar for structured data, secure storage for tokens.
- Keep `pubspec.lock` committed; pin SDK constraints; review plugin quality and platform support.

## Security

- Tokens in `flutter_secure_storage` backed by Keychain/Keystore; never in shared preferences or logs.
- HTTPS only; do not disable certificate validation. Pinning needs a rotation plan.
- No secrets in the Dart bundle — it is extractable.
- Validate deep links and WebView navigation; restrict JavaScript bridges.
- Android: review manifest permissions/exported components; iOS: ATS, entitlements, privacy manifest.
- Obfuscate release builds (`--obfuscate --split-debug-info`) and keep symbols for crash reporting.

## Performance

- Profile in profile/release mode on a real device; debug mode is misleading.
- Avoid rebuilding large subtrees; use `const`, `RepaintBoundary` where measured, and lazy lists.
- Optimize images/assets; defer heavy work off the UI isolate (`compute`/isolates).
- Measure startup, jank, and app size; remove unused assets/packages.

## Testing and release

- Unit tests for logic; widget tests for UI states; integration tests on devices/emulators for critical journeys.
- Golden tests where visual stability matters; update goldens deliberately.
- Test on the minimum and current OS versions, small screens, and low-end devices.
- Build with flavors (dev/staging/prod), signing per platform, and store compliance (permissions, data safety, privacy).
- Use staged rollout and crash monitoring; keep a rollback/halt plan.

## Checklist

- [ ] State management consistent; async states handled.
- [ ] Secure storage and TLS verified on each platform.
- [ ] Manifest/entitlements/privacy declarations reviewed.
- [ ] Release build profiled and obfuscated.
- [ ] Device/OS matrix and store rollout configured.
