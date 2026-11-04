#!/usr/bin/env python3
"""Heuristic project scanner for Fierly MonoSkill.

Usage:
    python3 scripts/scan_project.py /path/to/repo --task "add OAuth login"
    python3 scripts/scan_project.py . --json

The output is a starting point, not ground truth. Verify detected stacks
against manifests and entry points before selecting modules.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "out",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".gradle",
    "Pods",
    "DerivedData",
    "coverage",
    ".idea",
    ".vscode",
    ".terraform",
    ".dart_tool",
    ".expo",
    ".kotlin",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "bin",
    "obj",
    "third_party",
    "fixtures",
    "testdata",
    "snapshots",
}

LANG_BY_EXT = {
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".py": "Python",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".swift": "Swift",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C",
    ".h": "C/C++",
    ".cpp": "C++",
    ".cc": "C++",
    ".hpp": "C++",
    ".cs": "C#",
    ".java": "Java",
    ".dart": "Dart",
    ".rb": "Ruby",
    ".php": "PHP",
    ".sql": "SQL",
    ".sh": "Shell",
    ".lua": "Lua",
    ".ex": "Elixir",
    ".exs": "Elixir",
}

LANG_MODULE = {
    "TypeScript": "typescript",
    "Python": "python",
    "Kotlin": "kotlin",
    "Swift": "swift",
    "Go": "go",
    "Rust": "rust",
    "C": "c-cpp",
    "C++": "c-cpp",
    "C/C++": "c-cpp",
    "SQL": "sql",
}

MANIFESTS = {
    "package.json",
    "tsconfig.json",
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
    "go.mod",
    "Cargo.toml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "Package.swift",
    "pubspec.yaml",
    "composer.json",
    "Gemfile",
    "CMakeLists.txt",
    "Makefile",
    "meson.build",
    "Directory.Build.props",
}

DB_DEPS = {
    "postgresql": [
        "pg",
        "postgres",
        "postgresql",
        "psycopg",
        "psycopg2",
        "asyncpg",
        "prisma",
        "@prisma/client",
        "typeorm",
        "sequelize",
        "sqlalchemy",
        "drizzle-orm",
        "knex",
    ],
    "sqlite": ["sqlite3", "better-sqlite3", "aiosqlite", "sqlx-sqlite"],
    "mongodb": ["mongoose", "mongodb", "pymongo", "motor", "mongodb-driver"],
    "redis": ["redis", "ioredis", "redis-py", "valkey", "lettuce", "jedis"],
}

SECURITY_KEYWORDS = {
    "auth": [
        "auth",
        "login",
        "logout",
        "session",
        "token",
        "password",
        "oauth",
        "oidc",
        "jwt",
        "permission",
        "role",
        "admin",
        "rbac",
        "sso",
        "mfa",
    ],
    "input": [
        "input",
        "form",
        "upload",
        "file",
        "parse",
        "query",
        "html",
        "sanitize",
        "validation",
    ],
    "database": [
        "database",
        "migration",
        "schema",
        "postgres",
        "mysql",
        "mongo",
        "sql",
        "backup",
        "pii",
    ],
    "api": [
        "api",
        "rest",
        "graphql",
        "grpc",
        "webhook",
        "endpoint",
        "cors",
        "rate limit",
    ],
    "frontend": [
        "frontend",
        "browser",
        "react",
        "vue",
        "svelte",
        "css",
        "csp",
        "xss",
        "dom",
    ],
    "native": [
        "android",
        "ios",
        "mobile",
        "desktop",
        "keychain",
        "keystore",
        "permission",
    ],
    "infrastructure": [
        "deploy",
        "docker",
        "kubernetes",
        "terraform",
        "cloud",
        "container",
        "infra",
    ],
    "supply-chain": [
        "dependency",
        "dependencies",
        "package",
        "lockfile",
        "ci",
        "build",
        "release",
        "sbom",
    ],
    "testing": [
        "security review",
        "threat model",
        "vulnerability",
        "scanner",
        "sast",
        "dast",
        "pentest",
    ],
}

WORKFLOW_ORDER = [
    (
        "security-review",
        [
            "security review",
            "threat model",
            "vulnerability",
            "pentest",
            "penetration",
            "security audit",
        ],
    ),
    ("release", ["release", "deploy", "ship", "production", "rollback", "publish"]),
    (
        "bugfix",
        ["bug", "fix", "crash", "regression", "broken", "fails", "error", "exception"],
    ),
    (
        "refactor",
        ["refactor", "restructure", "cleanup", "simplify", "technical debt", "extract"],
    ),
    (
        "performance",
        [
            "performance",
            "slow",
            "latency",
            "memory",
            "cpu",
            "optimize",
            "profile",
            "bottleneck",
        ],
    ),
    ("dependencies", ["dependency", "dependencies", "upgrade", "lockfile", "cve"]),
    (
        "feature",
        ["add", "implement", "feature", "build", "create", "support", "enable"],
    ),
    ("code-review", ["review", "pull request", "diff", "merge"]),
    (
        "testing",
        ["test strategy", "coverage", "unit test", "integration test", "e2e", "flaky"],
    ),
    (
        "architecture",
        ["architecture", "system design", "tradeoff", "adr", "technology choice"],
    ),
    (
        "existing-project",
        ["existing", "unfamiliar", "legacy", "onboard", "understand", "analyze"],
    ),
    (
        "new-project",
        ["new project", "greenfield", "from scratch", "bootstrap", "scaffold", "init"],
    ),
]


def read_text(path: Path, limit: int = 400_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except OSError:
        return ""


def load_json(path: Path) -> dict:
    try:
        return json.loads(read_text(path))
    except (ValueError, TypeError):
        return {}


def load_registry(script_path: Path) -> dict:
    candidate = script_path.resolve().parent.parent / "registry.json"
    if candidate.exists():
        try:
            return json.loads(read_text(candidate))
        except ValueError:
            pass
    return {}


def collect_files(root: Path, max_files: int):
    files = []
    lang_counts = Counter()
    truncated = False
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".git")
        )
        depth = len(Path(dirpath).relative_to(root).parts)
        if depth > 8:
            dirnames[:] = []
        for name in filenames:
            if len(files) >= max_files:
                truncated = True
                break
            path = Path(dirpath) / name
            if path.is_symlink():
                continue
            files.append(path)
            ext = path.suffix.lower()
            if ext in LANG_BY_EXT:
                lang_counts[LANG_BY_EXT[ext]] += 1
        if truncated:
            break
    return files, lang_counts, truncated


def dep_names_from_text(text: str) -> set:
    names = set()
    for line in text.splitlines():
        line = line.strip().strip("\"'")
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        match = re.match(r"([A-Za-z0-9@][A-Za-z0-9@._/-]*)", line)
        if match:
            name = (
                match.group(1).split("/")[-1].lower()
                if match.group(1).startswith("@")
                else match.group(1).lower()
            )
            names.add(name)
    return names


def parse_pyproject_deps(text: str) -> set:
    names = set()
    try:
        import tomllib

        data = tomllib.loads(text)
        project = data.get("project", {}) or {}
        groups = [project.get("dependencies", []) or []]
        optional = project.get("optional-dependencies", {}) or {}
        groups.extend(optional.values())
        tool = data.get("tool", {}).get("poetry", {}) or {}
        groups.append((tool.get("dependencies", {}) or {}).keys())
        for group in groups:
            for item in group:
                names.add(re.split(r"[<>=!~\[ ;]", str(item).strip())[0].lower())
    except Exception:
        in_deps = False
        for line in text.splitlines():
            if re.search(r"\bdependencies\s*=\s*\[", line):
                in_deps = True
            if in_deps:
                names.update(
                    m.lower()
                    for m in re.findall(r"[\"']([A-Za-z0-9][A-Za-z0-9_.-]*)", line)
                )
            if in_deps and "]" in line:
                in_deps = False
    return {n for n in names if n and n not in {"dependencies", "project", "python"}}


def detect_dependencies(root: Path):
    deps = set()
    package = root / "package.json"
    if package.exists():
        data = load_json(package)
        for key in (
            "dependencies",
            "devDependencies",
            "peerDependencies",
            "optionalDependencies",
        ):
            deps.update(str(k).lower() for k in (data.get(key) or {}))
    for name in ("requirements.txt", "requirements-dev.txt", "Pipfile"):
        path = root / name
        if path.exists():
            deps.update(dep_names_from_text(read_text(path)))
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        deps.update(parse_pyproject_deps(read_text(pyproject)))
    go_mod = root / "go.mod"
    if go_mod.exists():
        text = read_text(go_mod)
        deps.update(
            m.lower() for m in re.findall(r"^\s*([a-zA-Z0-9_.\-/]+)\s+v", text, re.M)
        )
    cargo = root / "Cargo.toml"
    if cargo.exists():
        deps.update(dep_names_from_text(read_text(cargo)))
    for name in ("build.gradle", "build.gradle.kts", "pubspec.yaml", "Package.swift"):
        path = root / name
        if path.exists():
            text = read_text(path).lower()
            for token in (
                "flutter",
                "react-native",
                "com.android.application",
                'kotlin("multiplatform")',
                'kotlin("android")',
                "compose",
                "spring-boot",
                "ktor",
                "swiftui",
            ):
                if token in text:
                    deps.add(token)
    for path in list(root.glob("*.csproj")) + list(root.glob("*/*.csproj")):
        text = read_text(path).lower()
        for token in (
            "microsoft.net.sdk.web",
            "microsoft.net.sdk.wpf",
            "microsoft.windowsappsdk",
            "microsoft.entityframeworkcore",
        ):
            if token in text:
                deps.add(token)
    return deps


def has_any(text: str, needles) -> bool:
    text = text.lower()
    return any(n in text for n in needles)


def detect_platforms(root: Path, files, deps: set, task: str) -> list:
    platforms = []
    text_task = task.lower()
    all_paths = [str(p.relative_to(root)).lower() for p in files]
    joined = "\n".join(all_paths)

    if deps & {
        "react",
        "vue",
        "svelte",
        "next",
        "nuxt",
        "@angular/core",
        "solid-js",
        "astro",
    } or any(
        p.endswith((".html", ".css", ".scss", ".vue", ".svelte")) for p in all_paths
    ):
        platforms.append("web")
    if deps & {
        "express",
        "fastify",
        "@nestjs/core",
        "koa",
        "hono",
        "fastapi",
        "flask",
        "django",
        "spring-boot",
        "ktor",
        "rails",
        "laravel",
        "microsoft.net.sdk.web",
    } or any(
        seg in joined
        for seg in ("/api/", "/routes/", "/controllers/", "/server/", "/handlers/")
    ):
        platforms.append("backend")
    if (
        "androidmanifest.xml" in joined
        or "com.android.application" in deps
        or any(p.endswith(".apk") for p in all_paths)
    ):
        platforms.append("android")
    has_apple_project = any(
        p.endswith(
            (".xcodeproj/project.pbxproj", ".xcworkspace/contents.xcworkspacedata")
        )
        for p in all_paths
    )
    swift_text = "\n".join(
        read_text(p, 20000).lower() for p in files if p.name == "Package.swift"
    )
    if has_apple_project or (
        "package.swift" in joined and "ios" in (swift_text + text_task)
    ):
        platforms.append("ios")
    if (
        "macos" in text_task
        or any("/macos/" in p or "macos/" in p for p in all_paths)
        or (swift_text and ".macos(" in swift_text)
    ):
        if "macos" not in platforms:
            platforms.append("macos")
    csproj_text = "\n".join(
        read_text(p, 20000).lower() for p in files if p.suffix == ".csproj"
    )
    if (
        "microsoft.net.sdk.wpf" in deps
        or "microsoft.windowsappsdk" in deps
        or "-windows" in csproj_text
        or "<usewpf>true" in csproj_text
        or "winui" in csproj_text
    ):
        platforms.append("windows")
    if any(p.endswith((".service", ".timer")) for p in all_paths) or any(
        p.startswith(("debian/", "rpm/", "snap/", "flatpak/")) for p in all_paths
    ):
        platforms.append("linux")
    if deps & {"electron", "tauri", "@tauri-apps/api"} or any(
        p.endswith(("tauri.conf.json", "electron-builder.yml")) for p in all_paths
    ):
        platforms.append("desktop")
    if (
        deps & {"flutter", "react-native", "expo", 'kotlin("multiplatform")', "maui"}
        or "pubspec.yaml" in joined
        or re.search(r"\bexpo\b", text_task)
    ):
        platforms.append("cross-platform")

    # Remove platform names implied by other platforms.
    if "cross-platform" in platforms and "desktop" in platforms:
        pass
    if "macos" in platforms and "ios" in platforms:
        pass
    return [
        p
        for p in dict.fromkeys(platforms)
        if p
        in {
            "web",
            "backend",
            "android",
            "ios",
            "macos",
            "windows",
            "linux",
            "cross-platform",
            "desktop",
        }
    ]


def detect_databases(deps: set, root: Path, files) -> list:
    found = []
    all_text = "\n".join(str(p.relative_to(root)).lower() for p in files)
    for db, needles in DB_DEPS.items():
        if any(n in deps for n in needles) or db in all_text:
            found.append(db)
    if (
        "firebase" in deps
        or "firebase-admin" in deps
        or (root / "firebase.json").exists()
        or (root / "firestore.rules").exists()
    ):
        found.append("firebase")
    compose = root / "docker-compose.yml"
    if not compose.exists():
        compose = root / "compose.yaml"
    if compose.exists():
        text = read_text(compose).lower()
        for db, image in (
            ("postgresql", "postgres"),
            ("mongodb", "mongo"),
            ("redis", "redis"),
        ):
            if f"image: {image}" in text or f'image: "{image}' in text:
                if db not in found:
                    found.append(db)
    return found


def detect_infrastructure(root: Path, files) -> list:
    paths = [str(p.relative_to(root)).lower() for p in files]
    joined = "\n".join(paths)
    found = []
    if "dockerfile" in joined or "compose.yaml" in joined or "docker-compose" in joined:
        found.append("docker")
    if any(k in joined for k in ("k8s/", "kubernetes/", "helm/", "chart.yaml")) or any(
        "kind: deployment" in read_text(p, 20000).lower()
        for p in files
        if p.suffix in (".yaml", ".yml")
    ):
        found.append("kubernetes")
    if any(
        k in joined
        for k in (
            ".github/workflows/",
            ".gitlab-ci.yml",
            "jenkinsfile",
            "azure-pipelines",
            ".circleci/",
            "bitbucket-pipelines",
        )
    ):
        found.append("ci-cd")
    if (
        any(p.endswith(".tf") for p in paths)
        or "serverless.yml" in joined
        or "cdk.json" in joined
    ):
        found.append("cloud")
    return found


def detect_tests(root: Path, files) -> list:
    joined = "\n".join(str(p.relative_to(root)).lower() for p in files)
    found = []
    package_text = (
        read_text(root / "package.json").lower()
        if (root / "package.json").exists()
        else ""
    )
    pyproject_text = (
        read_text(root / "pyproject.toml").lower()
        if (root / "pyproject.toml").exists()
        else ""
    )
    if (
        "pytest" in joined
        or "pytest" in pyproject_text
        or "conftest.py" in joined
        or "test_" in joined
    ):
        found.append("pytest")
    if "vitest" in joined or "vitest" in package_text:
        found.append("vitest")
    if "jest.config" in joined or "@jest" in package_text or '"jest"' in package_text:
        found.append("jest")
    if "_test.go" in joined:
        found.append("go test")
    if "src/test/" in joined or "junit" in joined:
        found.append("JUnit")
    if "xctest" in joined or ".xctest" in joined:
        found.append("XCTest")
    if "test/" in joined and "pubspec.yaml" in joined:
        found.append("flutter test")
    if "xunit" in joined or "nunit" in joined:
        found.append("xUnit/NUnit")
    return list(dict.fromkeys(found))


def detect_package_managers(root: Path) -> list:
    managers = []
    for name, label in (
        ("package-lock.json", "npm"),
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("bun.lockb", "bun"),
        ("poetry.lock", "poetry"),
        ("uv.lock", "uv"),
        ("Pipfile.lock", "pipenv"),
        ("requirements.txt", "pip"),
        ("go.mod", "go modules"),
        ("Cargo.lock", "cargo"),
        ("gradlew", "Gradle"),
        ("gradle/wrapper/gradle-wrapper.properties", "Gradle"),
        ("pubspec.lock", "pub"),
        ("packages.lock.json", "NuGet"),
        ("Gemfile.lock", "Bundler"),
    ):
        if (root / name).exists():
            managers.append(label)
    if not managers:
        if (root / "package.json").exists():
            managers.append("npm (no lockfile)")
        if (root / "pyproject.toml").exists():
            managers.append("pip/uv (no lockfile)")
        if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists():
            managers.append("Gradle (no lockfile)")
    return list(dict.fromkeys(managers))


def detect_conventions(root: Path) -> list:
    markers = [
        "AGENTS.md",
        "CLAUDE.md",
        ".cursorrules",
        ".editorconfig",
        ".prettierrc",
        "ruff.toml",
        ".ruff.toml",
        "eslint.config.js",
        ".eslintrc",
        ".eslintrc.json",
        "tsconfig.json",
        "mypy.ini",
        "pyrightconfig.json",
        ".golangci.yml",
        "rustfmt.toml",
        ".swiftlint.yml",
        "detekt.yml",
        ".github/copilot-instructions.md",
        "CONTRIBUTING.md",
    ]
    found = [m for m in markers if (root / m).exists()]
    for pattern in ("*.sln", "pnpm-workspace.yaml", "turbo.json", "nx.json"):
        if list(root.glob(pattern)):
            found.append(pattern)
    return found


def detect_sensitive(root: Path, files) -> list:
    keywords = (
        "auth",
        "login",
        "crypto",
        "payment",
        "billing",
        "admin",
        "upload",
        "secret",
        "migration",
        "permission",
        "session",
        "token",
    )
    hits = []
    for path in files:
        rel = str(path.relative_to(root)).lower()
        if any(k in rel for k in keywords) or rel.endswith(
            (".env", ".env.local", ".pem", ".key", ".rules", "firestore.indexes.json")
        ):
            hits.append(str(path.relative_to(root)))
        if len(hits) >= 12:
            break
    return hits


def pick_workflow(task: str, root: Path) -> str:
    text = task.lower()
    for name, needles in WORKFLOW_ORDER:
        if any(n in text for n in needles):
            return name
    try:
        has_code = any(root.glob("**/*"))
    except OSError:
        has_code = False
    return "existing-project" if has_code else "new-project"


def pick_security(
    task: str, platforms, technologies, dbs, infra, workflow: str
) -> list:
    text = task.lower()
    selected = ["baseline"]
    platform_set = set(platforms)

    def add(name):
        if name not in selected:
            selected.append(name)

    for name, needles in SECURITY_KEYWORDS.items():
        if any(n in text for n in needles):
            add(name)
    if "web" in platform_set:
        add("frontend")
    if "backend" in platform_set or any(
        t in technologies for t in ("fastapi", "django", "spring-boot", "dotnet")
    ):
        add("api")
    if platform_set & {
        "android",
        "ios",
        "macos",
        "windows",
        "desktop",
        "cross-platform",
    }:
        add("native")
    if dbs:
        add("database")
        add("input")
    if infra:
        add("infrastructure")
    if workflow in ("release", "dependencies", "security-review"):
        add("supply-chain")
    if workflow in ("security-review", "release", "testing"):
        add("testing")
    if workflow == "release":
        add("gate")
    return selected


def build_scan(root: Path, task: str, max_files: int, registry: dict) -> dict:
    files, lang_counts, truncated = collect_files(root, max_files)
    deps = detect_dependencies(root)
    platforms = detect_platforms(root, files, deps, task)
    dbs = detect_databases(deps, root, files)
    infra = detect_infrastructure(root, files)
    tests = detect_tests(root, files)
    managers = detect_package_managers(root)
    conventions = detect_conventions(root)
    sensitive = detect_sensitive(root, files)
    workflow = pick_workflow(task, root)

    lang_manifests = {
        "python": any(
            (root / n).exists()
            for n in ("pyproject.toml", "requirements.txt", "Pipfile")
        ),
        "typescript": (root / "tsconfig.json").exists(),
        "kotlin": any(
            (root / n).exists() for n in ("build.gradle", "build.gradle.kts")
        ),
        "swift": (root / "Package.swift").exists(),
        "go": (root / "go.mod").exists(),
        "rust": (root / "Cargo.toml").exists(),
        "c-cpp": any(
            (root / n).exists() for n in ("CMakeLists.txt", "Makefile", "meson.build")
        ),
    }
    tech = []
    for lang, count in lang_counts.most_common():
        module = LANG_MODULE.get(lang)
        if module and (count >= 3 or lang_manifests.get(module)) and module not in tech:
            tech.append(module)
    dep_to_module = {
        "typescript": "typescript",
        "react": "react",
        "next": "react",
        "fastapi": "fastapi",
        "django": "django",
        "spring-boot": "spring-boot",
        "microsoft.net.sdk.web": "dotnet",
        "microsoft.net.sdk.wpf": "dotnet",
        "flutter": "flutter",
        "postgresql": "postgresql",
        "sqlite": "sqlite",
        "mongodb": "mongodb",
        "redis": "redis",
        "firebase": "firebase",
        "docker": "docker",
        "kubernetes": "kubernetes",
        "ci-cd": "ci-cd",
        "cloud": "cloud",
    }
    for key, module in dep_to_module.items():
        if (
            key in deps or key in platforms or key in dbs or key in infra
        ) and module not in tech:
            tech.append(module)
    if (
        any("migration" in str(p.relative_to(root)).lower() for p in files)
        and "sql" not in tech
    ):
        tech.append("sql")
    if "sql" in task.lower() and "sql" not in tech:
        tech.append("sql")

    security = pick_security(task, platforms, tech, dbs, infra, workflow)
    manifests = sorted(
        str(p.relative_to(root))
        for p in files
        if p.name in MANIFESTS or p.suffix in (".csproj", ".sln", ".xcodeproj")
    )
    entry_points = sorted(
        str(p.relative_to(root))
        for p in files
        if p.name
        in (
            "main.py",
            "app.py",
            "manage.py",
            "main.go",
            "main.rs",
            "index.js",
            "index.ts",
            "server.js",
            "server.ts",
            "App.tsx",
            "main.tsx",
            "MainActivity.kt",
            "App.swift",
            "Program.cs",
            "main.dart",
            "docker-compose.yml",
            "Dockerfile",
        )
    )[:10]

    return {
        "root": str(root),
        "task": task,
        "files_scanned": len(files),
        "scan_truncated": truncated,
        "languages": dict(lang_counts.most_common(10)),
        "platforms": platforms,
        "technologies": tech,
        "databases": dbs,
        "infrastructure": infra,
        "tests": tests,
        "package_managers": managers,
        "conventions": conventions,
        "manifests": manifests[:20],
        "entry_points": entry_points,
        "sensitive_areas": sensitive,
        "workflow": workflow,
        "workflow_path": (registry.get("workflows", {}).get(workflow) or {}).get(
            "path"
        ),
        "security": security,
        "confidence": "low"
        if not manifests
        else ("medium" if len(files) < 50 else "high"),
    }


def render_markdown(scan: dict) -> str:
    def line(label, value):
        if isinstance(value, list):
            value = ", ".join(value) if value else "none detected"
        return f"- **{label}:** {value}"

    tech = scan["technologies"]
    out = [
        "# Fierly project scan",
        "",
        f"Root: `{scan['root']}`  ",
        f"Task: {scan['task'] or '(not provided)'}  ",
        f"Files scanned: {scan['files_scanned']}"
        + (" (limit reached)" if scan["scan_truncated"] else ""),
        "",
        "## Detected stack",
        line("Languages", [f"{k} ({v})" for k, v in scan["languages"].items()]),
        line("Platforms", scan["platforms"]),
        line("Technologies", tech),
        line("Databases", scan["databases"]),
        line("Infrastructure", scan["infrastructure"]),
        line("Tests", scan["tests"]),
        line("Package managers", scan["package_managers"]),
        line("Conventions", scan["conventions"]),
        line("Confidence", scan["confidence"]),
        "",
        "## Project shape",
        line("Manifests", scan["manifests"]),
        line("Entry points", scan["entry_points"]),
        line("Sensitive areas", scan["sensitive_areas"]),
        "",
        "## Suggested modules",
        f"- **Core:** `core/engineering.md`"
        + (
            " + `core/project-analysis.md`"
            if scan["workflow"] in ("existing-project", "security-review")
            else ""
        ),
        f"- **Workflow:** `{scan['workflow_path'] or 'workflows/' + scan['workflow'] + '.md'}`",
        f"- **Platform:** "
        + (
            ", ".join(f"`platforms/{p}.md`" for p in scan["platforms"])
            or "unclassified — inspect entry points"
        ),
        f"- **Technology (choose ≤4 core; infra only when deploy/infra is in scope):** "
        + (", ".join(f"`registry:{t}`" for t in tech) or "none"),
        f"- **Security (choose baseline + ≤5 matching the attack surface):** "
        + ", ".join(f"`security/{s}.md`" for s in scan["security"]),
        "",
        "## Manual checks before coding",
        "1. Verify the main language/framework in manifests, not by file count alone.",
        "2. Read the entry point, test command, CI config, and 2–3 representative source files.",
        "3. Confirm database, auth, and external integrations from configuration, not folder names.",
        "4. Note existing conventions (formatter, linter, error style, module layout) and follow them.",
        "5. If the scan is low confidence, run the existing-project workflow before editing.",
        "",
        "> Heuristic output. Never treat a detected module as proof that the technology is used.",
    ]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan a project and suggest Fierly modules."
    )
    parser.add_argument("path", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--task", default="", help="Task description used for workflow/security routing"
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit JSON instead of Markdown"
    )
    parser.add_argument(
        "--max-files", type=int, default=20000, help="Maximum files to scan"
    )
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    registry = load_registry(Path(__file__))
    if not registry:
        print(
            "warning: registry.json not found next to the skill; paths may be incomplete",
            file=sys.stderr,
        )
    scan = build_scan(root, args.task, max(100, args.max_files), registry)
    print(
        json.dumps(scan, indent=2, ensure_ascii=False)
        if args.json
        else render_markdown(scan)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
