#!/usr/bin/env python3
"""Validate the documentation-only baseline without claiming an app build."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MAX_README_CHARS = 5000
REQUIRED_DOCS = (
    "docs/ENGINEERING_IMPROVEMENT_INDEX.md",
    "docs/ENGINEERING_GOVERNANCE.md",
    "docs/TECHNICAL_DEBT_REGISTER.md",
)


def main() -> int:
    errors: list[str] = []
    if not README.is_file():
        errors.append("README.md is missing")
        content = ""
    else:
        content = README.read_text(encoding="utf-8")
        if len(content) > MAX_README_CHARS:
            errors.append(
                f"README.md has {len(content)} characters; limit is {MAX_README_CHARS}"
            )

    for relative in REQUIRED_DOCS:
        if not (ROOT / relative).is_file():
            errors.append(f"required governance document is missing: {relative}")

    for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", content):
        target = match.group(1).strip()
        if not target or target.startswith(("#", "https://", "http://", "mailto:", "data:")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        resolved = (ROOT / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"link escapes repository: {match.group(1)}")
            continue
        if not resolved.exists():
            errors.append(f"broken local link: {match.group(1)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Documentation checks passed (README length, required docs, local links).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
