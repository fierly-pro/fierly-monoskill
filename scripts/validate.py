#!/usr/bin/env python3
"""Static validator for the Fierly MonoSkill repository.

Checks Agent Skills frontmatter, module registry integrity, relative links,
required documentation, module headers, size budgets, and unsafe patterns.
No third-party dependencies. Exit code 1 on errors.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS = []
WARNINGS = []


def error(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return None, text
    data = {}
    metadata = {}
    current = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current == "metadata" and ":" in line:
                key, value = line.strip().split(":", 1)
                metadata[key.strip()] = value.strip().strip("\"'")
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        data[key] = value
        current = key
    if metadata:
        data["metadata"] = metadata
    return data, "\n".join(lines[end + 1 :])


def check_skill():
    path = ROOT / "SKILL.md"
    if not path.exists():
        error("SKILL.md is missing")
        return {}
    text = read(path)
    data, body = parse_frontmatter(text)
    if not data:
        error("SKILL.md: missing or malformed YAML frontmatter")
        return {}
    name = data.get("name", "")
    description = data.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        error(
            f"SKILL.md: invalid name '{name}' (lowercase, hyphens, no leading/trailing/consecutive hyphens)"
        )
    if name != ROOT.name:
        error(f"SKILL.md: name '{name}' does not match directory '{ROOT.name}'")
    if not description or len(description) > 1024:
        error("SKILL.md: description must be 1-1024 characters")
    if not data.get("license"):
        warn("SKILL.md: no license field")
    if len(body.splitlines()) > 500:
        error(f"SKILL.md: body is {len(body.splitlines())} lines (recommended < 500)")
    tokens = len(body) // 4
    if tokens > 6000:
        warn(f"SKILL.md: estimated {tokens} tokens; spec recommends < 5000")
    version = (data.get("metadata") or {}).get("version")
    if version:
        changelog = ROOT / "CHANGELOG.md"
        if changelog.exists():
            match = re.search(
                r"^##\s*\[?v?([0-9]+\.[0-9]+\.[0-9]+)", read(changelog), re.M
            )
            if match and match.group(1) != version:
                error(
                    f"SKILL.md version {version} != CHANGELOG version {match.group(1)}"
                )
    return data


def check_registry():
    path = ROOT / "registry.json"
    if not path.exists():
        error("registry.json is missing")
        return {}
    try:
        registry = json.loads(read(path))
    except ValueError as exc:
        error(f"registry.json: invalid JSON: {exc}")
        return {}
    paths = []
    for category in ("core", "workflows", "platforms", "technologies", "security"):
        entries = registry.get(category, {})
        if not isinstance(entries, dict):
            error(f"registry.json: '{category}' must be an object")
            continue
        for key, entry in entries.items():
            module_path = entry.get("path") if isinstance(entry, dict) else None
            if not module_path:
                error(f"registry.json: {category}.{key} has no path")
                continue
            paths.append(module_path)
            target = ROOT / module_path
            if not target.exists():
                error(f"registry.json: missing file {module_path}")
            elif target.suffix != ".md":
                error(f"registry.json: {module_path} is not Markdown")
            elif not target.read_text(encoding="utf-8", errors="ignore").strip():
                error(f"registry.json: empty module {module_path}")
    duplicates = [p for p, count in Counter(paths).items() if count > 1]
    if duplicates:
        error(f"registry.json: duplicate paths: {duplicates}")
    for item in registry.get("always", []):
        if not (ROOT / item).exists():
            error(f"registry.json: always path missing: {item}")
    return registry


def check_required_files():
    required = [
        "README.md",
        "SKILL.md",
        "LICENSE",
        "INSTALLATION.md",
        "QUICK_START.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "UPSTREAM_SOURCES.md",
        "ARCHITECTURE.md",
        "registry.json",
        "scripts/validate.py",
        "scripts/scan_project.py",
        ".github/workflows/validate.yml",
        "tests/scenarios.md",
        "tests/results.md",
        "integrations/mcp.md",
        "integrations/agents.md",
    ]
    for name in required:
        if not (ROOT / name).exists():
            error(f"required file missing: {name}")


def check_modules():
    directories = ["core", "platforms", "technologies", "workflows", "security"]
    module_files = []
    for directory in directories:
        base = ROOT / directory
        if not base.exists():
            error(f"module directory missing: {directory}")
            continue
        module_files.extend(sorted(base.rglob("*.md")))
    for path in module_files:
        text = read(path)
        lines = text.splitlines()
        if not any(
            marker in line
            for line in lines[:8]
            for marker in ("> Load:", "> Trigger:", "> Modules:")
        ):
            warn(
                f"{rel(path)}: missing '> Load:' or '> Trigger:' header in the first lines"
            )
        if len(text) // 4 > 3500:
            warn(f"{rel(path)}: estimated {len(text) // 4} tokens; consider splitting")
        if len(lines) > 400:
            warn(f"{rel(path)}: {len(lines)} lines; check density")
    nested = [p for p in ROOT.rglob("SKILL.md") if p != ROOT / "SKILL.md"]
    if nested:
        error(
            f"nested SKILL.md files are not allowed in a single-skill tree: {[rel(p) for p in nested]}"
        )


def check_links():
    all_markdown = sorted(ROOT.rglob("*.md"))
    link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for path in all_markdown:
        text = read(path)
        in_code = False
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for raw in link_re.findall(line):
                target = raw.strip().split()[0].strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                try:
                    resolved.relative_to(ROOT.resolve())
                except ValueError:
                    error(f"{rel(path)}:{lineno}: link escapes the repository: {raw}")
                    continue
                if not resolved.exists():
                    error(f"{rel(path)}:{lineno}: broken link: {raw}")


def check_workflows():
    terminal_markers = (
        "exit criteria",
        "when done",
        "done when",
        "completion criteria",
    )
    for path in sorted((ROOT / "workflows").glob("*.md")):
        text = read(path).lower()
        if not any(marker in text for marker in terminal_markers):
            error(f"{rel(path)}: workflow has no completion/exit criteria")
        if "module" not in text and "## steps" not in text:
            warn(f"{rel(path)}: workflow lacks modules/steps structure")


def check_unsafe_patterns():
    patterns = [
        r"shell\s*=\s*True",
        r"verify\s*=\s*False",
        r"InsecureSkipVerify",
        r"rejectUnauthorized\s*:\s*false",
        r"NODE_TLS_REJECT_UNAUTHORIZED",
        r"checkServerTrusted",
        r"TrustAllCerts",
        r"curl\s+[^|\n]*\|\s*(ba)?sh",
    ]
    negative = ("never", "do not", "don't", "avoid", "prohibit", "для", "не ")
    for path in sorted(ROOT.rglob("*.md")):
        for lineno, line in enumerate(read(path).splitlines(), 1):
            for pattern in patterns:
                if re.search(pattern, line, re.I):
                    if not any(word in line.lower() for word in negative):
                        warn(
                            f"{rel(path)}:{lineno}: review potentially unsafe pattern: {line.strip()[:110]}"
                        )
                    break


def check_placeholders():
    pattern = re.compile(r"\b(TODO|TBD|FIXME|LOREM IPSUM)\b", re.I)
    skip = {ROOT / "CONTRIBUTING.md", ROOT / "scripts" / "validate.py"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path in skip:
            continue
        if path.suffix.lower() not in (
            ".md",
            ".json",
            ".py",
            ".yml",
            ".yaml",
        ):
            continue
        for lineno, line in enumerate(read(path).splitlines(), 1):
            if pattern.search(line):
                warn(f"{rel(path)}:{lineno}: placeholder text: {line.strip()[:90]}")


def check_duplicates():
    counts = Counter()
    locations = {}
    for path in sorted(ROOT.rglob("*.md")):
        for lineno, line in enumerate(read(path).splitlines(), 1):
            normalized = re.sub(r"\s+", " ", line.strip().lower())
            if len(normalized) < 70 or normalized.startswith(("|", "- [", "#", ">")):
                continue
            counts[normalized] += 1
            locations.setdefault(normalized, []).append(f"{rel(path)}:{lineno}")
    for line, count in counts.most_common(8):
        if count >= 3:
            warn(
                f"duplicate line in {count} files: {line[:90]}... ({locations[line][0]})"
            )


def check_empty_dirs():
    for path in sorted(ROOT.rglob("*")):
        if path.is_dir() and not any(path.iterdir()):
            error(f"empty directory: {rel(path)}")


def check_license_and_sources():
    license_path = ROOT / "LICENSE"
    if license_path.exists() and "Apache License" not in read(license_path):
        error("LICENSE does not contain the Apache License text")
    sources = ROOT / "UPSTREAM_SOURCES.md"
    if sources.exists():
        text = read(sources)
        if not re.search(r"2026-\d{2}-\d{2}", text):
            warn("UPSTREAM_SOURCES.md: no verification date found")
        if "license" not in text.lower():
            error("UPSTREAM_SOURCES.md: licenses are not documented")


def main() -> int:
    check_skill()
    check_registry()
    check_required_files()
    check_modules()
    check_links()
    check_workflows()
    check_unsafe_patterns()
    check_placeholders()
    check_duplicates()
    check_empty_dirs()
    check_license_and_sources()

    for message in WARNINGS:
        print(f"WARN  {message}")
    for message in ERRORS:
        print(f"FAIL  {message}")
    markdown_files = list(ROOT.rglob("*.md"))
    total_chars = sum(len(read(p)) for p in markdown_files)
    print(
        f"\nSummary: {len(markdown_files)} Markdown files, "
        f"~{total_chars // 4} tokens total, {len(ERRORS)} errors, {len(WARNINGS)} warnings"
    )
    if ERRORS:
        return 1
    print("PASS  repository structure and links are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
