# Platform: Android

> Load: Android app or SDK.
> Pairs with: `technologies/languages/kotlin.md`, `security/native.md`, `security/api.md`.

## Defaults

- Kotlin + Jetpack Compose for new UI; follow the project's existing View system if present.
- Set `minSdk`/`targetSdk` deliberately; target the current Play requirement and test on the minimum supported version.
- Use Gradle version catalogs and convention plugins for multi-module projects; keep build logic out of feature modules.
- Architecture: unidirectional data flow (ViewModel → UI state), repository boundaries, dependency injection, lifecycle-aware collection.
- Coroutines/Flow for async; never block the main thread; define dispatchers and cancellation.
- Persistence: Room for relational data, DataStore for preferences; migrations are versioned and tested.
- WorkManager for deferrable guaranteed work; respect battery/network constraints.
- Handle process death, configuration changes, and deep-link entry into any screen.

## Non-negotiables

- No leaked `Context`, Activity, or View references in long-lived objects.
- No network/disk I/O on the main thread.
- Explicitly handle loading, empty, error, offline, and permission-denied states.
- Do not request unnecessary permissions; request at the point of use.
- Support edge-to-edge and system bars correctly on current Android versions.
- Keep R8/ProGuard rules minimal and tested; do not disable shrinking to hide reflection issues.

## Security

- `android:exported="false"` unless a component must be public; protect exported components with permissions and validate all inputs.
- Store tokens in Keystore-backed storage (`EncryptedSharedPreferences` or equivalent); never in plain prefs/logs.
- Treat biometric/device-unlock as local re-authentication convenience, not server trust. Define the fallback path, lockout behavior, and keep server-side session expiry and revocation authoritative.
- Network security config: HTTPS only, no user-added CAs in production unless required; certificate pinning only with rotation.
- WebView: disable JS/file access unless required; restrict navigation; never expose a JS bridge to untrusted content.
- Validate deep links and intents; do not auto-perform sensitive actions from a link.
- Exclude sensitive files from backup; redact crash logs; disable debug logging in release.

## Testing and release

- Unit tests for ViewModels/domain; Compose UI tests; instrumented tests for DB/permissions/intents; screenshot tests where stable.
- Test on a range of API levels, screen sizes, and a low-memory device.
- Build a release AAB, verify signing, R8 mapping upload, and Play policy compliance (data safety, permissions, target SDK).
- Use internal/closed testing and staged rollout; monitor crashes/ANRs; keep a halt plan.
- Baseline Profiles for startup/jank where performance matters.

## Checklist

- [ ] Manifest components/permissions reviewed.
- [ ] Tokens in Keystore-backed storage; no secrets in resources or logs.
- [ ] Process death and configuration changes handled.
- [ ] Release build tested with minification and signing.
- [ ] Data safety form and store policy requirements reviewed.
- [ ] Crash/ANR monitoring and staged rollout configured.
