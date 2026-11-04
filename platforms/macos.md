# Platform: macOS

> Load: macOS app, menu bar utility, or AppKit/SwiftUI desktop product.
> Pairs with: `technologies/languages/swift.md`, `security/native.md`, `platforms/desktop.md` for shared shells.

## Defaults

- SwiftUI for new UI; AppKit for windows, menus, drag-and-drop, and features SwiftUI does not cover well. Keep a clear boundary.
- Declare the minimum macOS version; build a universal binary (arm64 + x86_64) when distribution requires it.
- Sandbox the app and request the minimum entitlements (network client, user-selected files, keychain access groups).
- Use security-scoped bookmarks for persistent file access; do not assume arbitrary filesystem access.
- Persist preferences in `UserDefaults`; secrets in Keychain; documents in the document architecture with autosave/versions.
- Menu bar apps: define activation policy, window lifecycle, and quit behavior explicitly.

## Non-negotiables

- No blocking work on the main thread; long operations are async with cancellation and progress.
- Handle multiple windows, state restoration, and app termination safely.
- Do not disable App Sandbox or hardened runtime to make a feature work without documenting the distribution impact.
- Respect system appearance, accessibility, keyboard navigation, and full keyboard access.
- No force unwraps on production paths; avoid retain cycles in closures and delegates.

## Security and distribution

- **Direct distribution:** enable Hardened Runtime, sign with a Developer ID certificate, notarize with `notarytool`, and staple the ticket. Verify with `spctl`/`codesign`.
- **Mac App Store:** sandbox, store-compliant entitlements, review guidelines, and receipt validation if used.
- Auto-updates: sign update archives and the feed; verify signatures before applying; use a vetted framework (e.g., Sparkle 2) with EdDSA keys; support rollback.
- Validate XPC/IPC messages and the caller's identity; do not expose privileged helpers to untrusted clients.
- Keychain: appropriate accessibility and access groups; no secrets in plists, logs, or crash reports.
- Deep links/URL schemes and document types: validate all inputs.
- Harden the helper/privileged tool: least privilege, code-signature validation, no arbitrary command execution.

## Testing and release

- Unit tests for logic; UI tests for critical flows; test on the oldest supported macOS and the current release, on both architectures if shipped.
- Test sandbox behavior with a clean user account; verify file permissions and bookmark persistence.
- Test installer/uninstaller, notarization, Gatekeeper, and auto-update from the previous version.
- Verify crash symbolication and privacy-sensitive logging.
- Keep a notarization/stapling checklist in CI; fail the release if verification fails.

## Checklist

- [ ] Sandbox/entitlements and file-access paths reviewed.
- [ ] Hardened Runtime, signing, notarization, and stapling verified.
- [ ] Update signing and rollback tested.
- [ ] Keychain usage and log redaction verified.
- [ ] Universal binary and minimum OS tested.
- [ ] Accessibility and multi-window behavior checked.
