# Native Security (Mobile and Desktop)

> Load: Android, iOS, macOS, Windows, Linux, desktop, or cross-platform apps.
> Pairs with: platform modules, `security/auth.md`, `security/frontend.md` for embedded web content.

## Secret and token storage

- **iOS/macOS:** Keychain with an appropriate accessibility class (`kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` unless background needs differ). Do not store tokens in `UserDefaults` or plist files.
- **Android:** Keystore-backed keys; use `EncryptedSharedPreferences` or a vetted library. Do not store secrets in `SharedPreferences`, files, or logs.
- **Windows:** DPAPI or Credential Manager for user secrets; protect service credentials with least privilege.
- **Linux:** Secret Service/libsecret or a keyring; file permissions alone are not encryption.
- **Cross-platform:** use the platform keystore via the framework's secure-storage API; do not roll your own crypto.

## Permissions and capabilities

- Request the minimum permissions, at the moment of use, with a clear rationale.
- Android: set `android:exported="false"` unless a component must be public; protect exported components with permissions/signature checks; use scoped storage and content-provider grants.
- iOS/macOS: declare only required entitlements and usage descriptions; enable App Sandbox/hardened runtime where possible; use security-scoped bookmarks for file access.
- Do not request contacts, location, microphone, or accessibility permissions "just in case".
- Re-check authorization on the server; the app is not a trusted client.

## IPC, deep links, and web content

- Electron: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`; expose a narrow, validated preload API; validate IPC sender and payloads; disable `webSecurity` never.
- Tauri: use the capabilities/allowlist system; expose minimal commands; validate every argument; keep the updater and filesystem scopes narrow.
- Qt/.NET/WinUI: validate messages from other processes; do not expose privileged local APIs to untrusted content.
- Deep links/universal links: validate scheme, host, path, and parameters; treat them as untrusted input; do not auto-execute actions that change account state.
- WebViews: disable JavaScript/file access unless required; restrict navigation to an allowlist; never add a JS bridge to untrusted content; keep the engine patched.

## Network

- Use TLS with certificate validation enabled. Never ship "accept all certificates" code.
- Certificate pinning can raise the bar but complicates rotation and does not stop a compromised device; use it only with a rotation plan and a kill switch. Do not claim it makes the app unhackable.
- Configure ATS (iOS) and network security config (Android) deliberately; avoid cleartext exceptions.
- Validate server responses and signatures; do not trust client-side feature flags for entitlement.

## Local data and lifecycle

- Exclude sensitive files from backups (iOS `isExcludedFromBackup`, Android backup rules).
- Clear tokens and cached PII on logout; support remote session revocation.
- Encrypt local databases/files containing restricted data; manage keys in the platform keystore.
- Disable screenshots/screen recording for highly sensitive screens where the platform allows; treat it as a mitigation, not a guarantee.
- Redact logs and crash reports; disable verbose logging in release builds.

## Platform integrity and release

- Root/jailbreak detection is a risk signal, not a security boundary. Do not rely on it for authorization.
- Verify app signatures, entitlements, and update signatures. Protect signing keys; use CI with hardware-backed keys/HSM where possible.
- Apply OWASP MASVS for mobile and the platform's security checklist for desktop. State the verification level.
- Test on the minimum supported OS and a current release; review permission and exported-component changes in every release.

## Verification

- Inspect stored data on a rooted/jailbroken test device or with platform tooling; confirm no plaintext tokens.
- Attempt deep-link/URL-scheme abuse and IPC injection from an untrusted context.
- Confirm exported components and permissions in the built manifest/entitlements.
- Check release builds for debug flags, verbose logs, and test backdoors.
