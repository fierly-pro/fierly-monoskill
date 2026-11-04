# C and C++

> Load: C/C++ systems, native libraries, embedded, or performance-critical components.
> Pairs with: `platforms/linux.md`/`windows.md`, `security/input.md`, `security/native.md`.

## Defaults

- Compile with warnings enabled (`-Wall -Wextra -Wpedantic -Wconversion` or MSVC `/W4`), and treat warnings as errors in CI.
- Use the project's C/C++ standard (C11/C17, C++17/20/23); do not mix dialects casually.
- C++: RAII for all resources; `std::unique_ptr`/`std::shared_ptr` instead of raw `new`/`delete`; `std::span`/`std::string_view` only when lifetime is proven.
- C: check every allocation and I/O return; initialize memory; use `size_t` for sizes and check overflow before allocation.
- Prefer fixed-width types (`uint32_t`) at binary boundaries; define endianness and packing explicitly.
- Bounds-check every array/index; use `std::array`/`std::vector::at` where performance permits.
- Avoid undefined behavior: signed overflow, strict aliasing violations, uninitialized reads, invalid shifts, use-after-free, double-free.

## Build and tooling

- CMake (or the project's build system) with reproducible flags; no secrets or machine-specific paths.
- Run ASan/UBSan in tests; TSan for threaded code; MSan where supported.
- `clang-tidy`, `cppcheck`, and compiler static analysis in CI. Fuzz parsers with libFuzzer/AFL++.
- Keep third-party dependencies vendored/pinned with licenses recorded; check CVEs.

## Security

- Never use `gets`, `strcpy`, `sprintf`, or unbounded `scanf`; prefer `snprintf`, `strlcpy`/`std::string`, and explicit lengths.
- Validate lengths before `memcpy`/`malloc`; guard `size * count` overflow.
- Do not execute untrusted data; avoid `system`/`popen` with interpolated strings.
- Drop privileges early; use seccomp/AppArmor/capabilities where applicable; never run network parsers as root.
- Clear secrets with a non-optimized wipe; do not rely on `memset` being preserved.
- Treat file formats and network protocols as hostile; fail closed on parse errors.
- Enable stack protector, FORTIFY, RELRO, PIE, and non-executable stack in release builds.

## Concurrency

- Define ownership and synchronization for every shared object; prefer message passing or immutable data.
- Avoid lock ordering cycles; document the order; use RAII locks.
- Check `pthread`/thread return codes; join or detach every thread.
- Test with TSan and stress tests; do not assume x86 memory ordering on ARM.

## Testing

- Unit tests (GoogleTest/Catch2/Unity) for logic; sanitizer builds in CI; fuzz parsers.
- Test allocation failures and boundary sizes where practical.
- Benchmark with realistic data; measure before optimizing.

## Checklist

- [ ] Warnings/static analysis clean; sanitizers pass.
- [ ] All allocations, lengths, and I/O checked; no UB.
- [ ] No unsafe string/format functions; bounds enforced.
- [ ] Release hardening flags verified.
- [ ] Fuzzing or adversarial tests for parsers.
