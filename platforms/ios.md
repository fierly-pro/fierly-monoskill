# Platform: iOS

> Load: iPhone/iPad app or SDK.
> Pairs with: `technologies/languages/swift.md`, `security/native.md`, `security/api.md`.

## Defaults

- SwiftUI for new UI; UIKit where the project already uses it or the feature requires it. Do not mix paradigms without a boundary.
- Declare the deployment target deliberately; test on the minimum supported iOS version and the current release.
- Swift Package Manager for dependencies; minimize third-party UI/networking libraries.
- Architecture: feature modules with clear boundaries; observable state; dependency injection via initializers or a container.
- Swift concurrency: `async`/`await`, actors for shared mutable state, `@MainActor` for UI. Respect cancellation and task lifetimes.
- Persistence: SwiftData/CoreData with versioned migrations; files with appropriate protection classes; Keychain for credentials.
- Handle app lifecycle, background limits, state restoration, and deep-link entry into any screen.

## Non-negotiables

- No force unwraps or `try!` on production paths unless the invariant is proven and documented.
- No retain cycles in closures; use `[weak self]` where the ownership warrants it.
- No blocking work on the main thread; no synchronous network calls.
- Do not request permissions without a clear usage description and point-of-use rationale.
- Handle offline, loading, empty, error, and permission-denied states.
- Support Dynamic Type, VoiceOver, dark mode, and safe areas.

## Security

- Store tokens in Keychain with an appropriate accessibility class; never in `UserDefaults` or files.
- App Transport Security: HTTPS only; no arbitrary-load exceptions without a documented reason.
- Declare the minimum entitlements and capabilities; use App Sandbox/hardened runtime on macOS targets.
- Universal links/custom URL schemes: validate host, path, and parameters; treat as untrusted input.
- WebView: restrict navigation, disable unnecessary JavaScript bridges, and never expose native APIs to untrusted content.
- Add a privacy manifest for required-reason APIs and data collection; keep tracking minimal and disclosed.
- Exclude sensitive files from backups; redact logs and crash reports; clear state on logout.
- Do not rely on jailbreak detection for authorization.

## Testing and release

- Unit tests with Swift Testing/XCTest; UI tests for critical journeys; snapshot tests where stable.
- Test on the oldest supported device, a current device, and an iPad if supported.
- Verify signing certificates, provisioning profiles, entitlements, and App Store privacy/data declarations.
- Use TestFlight, then phased release; monitor crashes and hang rates; keep a halt plan.
- Upload dSYMs for symbolication; verify the release build has no debug flags or test hooks.

## Checklist

- [ ] Keychain storage and logout cleanup verified.
- [ ] ATS/entitlements/privacy manifest reviewed.
- [ ] Deep links and WebView navigation validated.
- [ ] Minimum OS and accessibility tested.
- [ ] Signing, TestFlight, and phased release configured.
- [ ] Crash reporting and dSYM upload working.
