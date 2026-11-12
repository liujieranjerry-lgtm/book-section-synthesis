#!/usr/bin/env python3
"""Print one CHANGELOG section, for use as GitHub Release notes.

Usage: python scripts/release_notes.py v3.0.1
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"


def extract(changelog: str, version: str) -> str | None:
    pattern = re.compile(
        rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(changelog)
    return match.group(1).strip() if match else None


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/release_notes.py <version>", file=sys.stderr)
        return 1

    raw = sys.argv[1].strip()
    version = raw[1:] if raw.startswith("v") else raw

    if not CHANGELOG.is_file():
        print(f"[FAIL] CHANGELOG.md not found at {CHANGELOG}", file=sys.stderr)
        return 1

    notes = extract(CHANGELOG.read_text(encoding="utf-8"), version)
    if not notes:
        print(f"[FAIL] CHANGELOG.md has no section for {version}", file=sys.stderr)
        return 1

    print(notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
