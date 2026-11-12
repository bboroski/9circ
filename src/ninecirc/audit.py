"""Read-only repository inventory and three-stage triadic evaluation."""
from __future__ import annotations

import os
from collections import Counter
from pathlib import Path
from typing import Any

IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "__pycache__",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", "node_modules",
    "vendor", "dist", "build", "target", ".next", ".tox",
}
SOURCE_EXTENSIONS = {
    ".py": "Python", ".pyi": "Python", ".rs": "Rust", ".go": "Go",
    ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript",
    ".tsx": "TypeScript", ".java": "Java", ".kt": "Kotlin",
    ".swift": "Swift", ".c": "C", ".h": "C/C++", ".cc": "C++",
    ".cpp": "C++", ".hpp": "C++", ".cs": "C#", ".rb": "Ruby",
    ".php": "PHP", ".sh": "Shell", ".ps1": "PowerShell",
}
MANIFEST_NAMES = {
    "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt",
    "Pipfile", "poetry.lock", "uv.lock", "package.json", "Cargo.toml",
    "go.mod", "pom.xml", "build.gradle", "build.gradle.kts",
    "Gemfile", "composer.json",
}
LICENSE_NAMES = {"LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"}
CI_MARKERS = {
    ".gitlab-ci.yml", "azure-pipelines.yml", "Jenkinsfile",
    ".circleci/config.yml", ".buildkite/pipeline.yml",
}


def _axis(state: str, detail: str) -> dict[str, str]:
    return {"state": state, "detail": detail}


def scan_repository(repository_path: str | os.PathLike[str], *, max_files: int = 10000, max_depth: int = 12) -> dict[str, Any]:
    """Inventory a selected folder without reading source contents or executing code."""
    root = Path(repository_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Repository folder does not exist: {root}")

    file_count = source_count = test_count = doc_count = 0
    languages: Counter[str] = Counter()
    manifests: set[str] = set()
    ci_configs: set[str] = set()
    security_policy = license_file = readme_defined = False
    sample_paths: list[str] = []
    scan_errors: list[str] = []
    truncated = False

    def record_scan_error(error: OSError) -> None:
        scan_errors.append(str(error.filename or error))

    for current, directories, filenames in os.walk(
        root, topdown=True, followlinks=False, onerror=record_scan_error
    ):
        current_path = Path(current)
        depth = len(current_path.relative_to(root).parts)
        directories.sort()
        filenames.sort()
        directories[:] = [name for name in directories if name not in IGNORED_DIRS and not (current_path / name).is_symlink()]
        if depth >= max_depth:
            if directories:
                truncated = True
            directories[:] = []

        for filename in filenames:
            path = current_path / filename
            if path.is_symlink() or filename == ".DS_Store" or filename.endswith(".pyc"):
                continue
            relative = path.relative_to(root).as_posix()
            file_count += 1
            if len(sample_paths) < 40:
                sample_paths.append(relative)

            parts = {part.lower() for part in path.relative_to(root).parts}
            lower_name = filename.lower()
            is_test_file = (
                "test" in parts
                or "tests" in parts
                or lower_name.startswith("test_")
                or ".test." in lower_name
                or ".spec." in lower_name
            )

            language = SOURCE_EXTENSIONS.get(path.suffix.lower())
            if language and not is_test_file:
                source_count += 1
                languages[language] += 1

            if is_test_file:
                test_count += 1
            if "docs" in parts or lower_name.startswith(("readme", "contributing")):
                doc_count += 1
            if filename in MANIFEST_NAMES:
                manifests.add(relative)
            if relative.startswith(".github/workflows/") or relative in CI_MARKERS:
                ci_configs.add(relative)
            if lower_name in {"security.md", "security.txt"}:
                security_policy = True
            if path.parent == root and filename in LICENSE_NAMES:
                license_file = True
            if path.parent == root and lower_name in {"readme.md", "readme.rst", "readme.txt"}:
                try:
                    readme_defined = path.stat().st_size > 160
                except OSError:
                    readme_defined = False

            if file_count >= max_files:
                truncated = True
                break
        if truncated:
            break

    if scan_errors:
        truncated = True

    findings: list[dict[str, str]] = []
    if scan_errors:
        findings.append({
            "severity": "REVIEW",
            "title": "Some folders could not be inspected",
            "detail": f"{len(scan_errors)} filesystem access error(s) occurred; the inventory is incomplete.",
        })
    if source_count == 0:
        findings.append({"severity": "INFO", "title": "No source files detected",
                         "detail": "This can be valid for a documentation or research repository; confirm its intended role."})
    elif not manifests:
        findings.append({"severity": "REVIEW", "title": "Build/runtime manifest not detected",
                         "detail": "Document the supported runtime and reproducible build or validation entry point."})
    if test_count == 0:
        findings.append({"severity": "REVIEW", "title": "Test files not detected",
                         "detail": "Add focused tests for the repository's actual behavior and public interfaces."})
    if not ci_configs:
        findings.append({"severity": "REVIEW", "title": "CI configuration not detected",
                         "detail": "Consider a repository-specific quality workflow with explicit, reproducible checks."})
    if not readme_defined:
        findings.append({"severity": "REVIEW", "title": "Project description needs evidence",
                         "detail": "Expand the README with purpose, scope, supported platforms, and run/test instructions."})
    if not security_policy:
        findings.append({"severity": "INFO", "title": "Security policy not detected",
                         "detail": "Add a SECURITY.md describing supported versions and responsible vulnerability reporting."})
    if not license_file:
        findings.append({"severity": "REVIEW", "title": "License not declared",
                         "detail": "Choose the intended license before redistributing; 9circ will not choose terms for you."})
    if truncated:
        findings.append({"severity": "INFO", "title": "Inventory limit reached",
                         "detail": "The scan reached a configured file/depth limit; review scope before relying on completeness."})

    return {
        "repository": root.name, "path": str(root), "file_count": file_count,
        "source_count": source_count, "test_count": test_count, "doc_count": doc_count,
        "languages": dict(languages.most_common()), "manifests": sorted(manifests),
        "ci_configs": sorted(ci_configs), "has_security_policy": security_policy,
        "has_license": license_file, "readme_defined": readme_defined,
        "truncated": truncated, "sample_paths": sample_paths,
        "scan_errors": scan_errors, "findings": findings,
    }


def build_triadic_matrix(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Build a three-stage × three-axis matrix from local scan evidence."""
    complete = not snapshot.get("truncated", False)
    described = bool(snapshot.get("readme_defined"))
    entry_point = bool(snapshot.get("manifests")) or snapshot.get("source_count", 0) == 0
    tested = snapshot.get("test_count", 0) > 0
    ci = bool(snapshot.get("ci_configs"))
    governed = bool(snapshot.get("has_security_policy")) and bool(snapshot.get("has_license"))

    stages = [
        {"id": "S1", "title": "Observe", "subtitle": "Local inventory and evidence collection", "axes": [
            {"name": "Evidence", **_axis("READY", f"{snapshot.get('file_count', 0)} files inventoried; source contents were not read.")},
            {"name": "Coverage", **_axis("READY" if complete else "REVIEW", "Scan stayed within configured limits." if complete else "Inventory reached a configured limit.")},
            {"name": "Safety", **_axis("READY", "Read-only inspection; no commands or repository hooks executed.")},
        ]},
        {"id": "S2", "title": "Evaluate", "subtitle": "Quality, traceability, and reproducibility", "axes": [
            {"name": "Project quality", **_axis("READY" if entry_point and tested else "REVIEW",
                "A project entry point and test files were detected." if entry_point and tested else "Review manifests and tests; documentation-only repositories may define another validation contract.")},
            {"name": "Traceability", **_axis("READY" if described else "REVIEW",
                "README contains a substantive project description." if described else "README scope and run/test instructions need review.")},
            {"name": "Governance", **_axis("READY" if governed else "REVIEW",
                "Security policy and license markers were detected." if governed else "Review security reporting and license choice before external distribution.")},
        ]},
        {"id": "S3", "title": "Propose", "subtitle": "Ranked findings and human-controlled gates", "axes": [
            {"name": "Plan evidence", **_axis("READY", f"{len(snapshot.get('findings', []))} evidence-based findings recorded.")},
            {"name": "Reversibility", **_axis("READY", "No repository or system changes were made.")},
            {"name": "Approval", **_axis("REVIEW", "Any future patch must be previewed, tested, and explicitly approved.")},
        ]},
    ]
    score_map = {"READY": 1, "REVIEW": 0, "BLOCKED": -1}
    score = sum(score_map[axis["state"]] for stage in stages for axis in stage["axes"])
    return {
        "stages": stages, "score": score, "maximum_score": 9,
        "state_legend": score_map, "findings": snapshot.get("findings", []),
        "summary": "Review recommendations before changing files or system settings.",
    }
