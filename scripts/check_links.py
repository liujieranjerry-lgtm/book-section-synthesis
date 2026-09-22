#!/usr/bin/env python3
"""Check local Markdown links in the repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def check(repo_dir: Path) -> list[str]:
    errors: list[str] = []
    for md in sorted(repo_dir.rglob("*.md")):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(SKIP_PREFIXES):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            if not (md.parent / target).resolve().exists():
                errors.append(
                    f"{md.relative_to(repo_dir)}: missing link target -> {target}"
                )
    return errors


def main() -> int:
    repo_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = check(repo_dir)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print("[OK] all local Markdown links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
