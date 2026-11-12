#!/usr/bin/env python3
"""Link validation for the book-section-synthesis repository.

Every relative Markdown link must resolve twice: the target file must exist, and
when the link carries a `#fragment`, a heading in that file must produce the same
anchor GitHub generates. Bare `#fragment` links are checked against their own
file.

Standard library only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:")
HEADING_RE = re.compile(r"^ {0,3}#{1,6} +(.*?)\s*$")
INLINE_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
CODE_SPAN_RE = re.compile(r"`([^`]*)`")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def slugify(heading: str) -> str:
    """Approximate the anchor GitHub generates for a heading."""
    text = heading.strip()
    text = re.sub(r"\s+#+\s*$", "", text)  # closing hashes
    text = INLINE_LINK_RE.sub(r"\1", text)
    text = CODE_SPAN_RE.sub(r"\1", text)
    text = text.replace("**", "").replace("__", "").replace("*", "")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.strip().replace(" ", "-")


def anchors_of(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify(match.group(1))
        if not base:
            continue
        seen = counts.get(base, 0)
        counts[base] = seen + 1
        anchors.add(base if seen == 0 else f"{base}-{seen}")
    return anchors


def iter_markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        yield path


def check_file(path: Path, root: Path, anchor_cache: dict[Path, set[str]]) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(root)

    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip()
        if not target or target.startswith(SKIP_PREFIXES):
            continue
        target = target.split(" ", 1)[0]  # drop a Markdown title
        file_part, _, fragment = target.partition("#")

        if file_part == "":
            if not fragment:
                continue
            resolved = path
        else:
            resolved = (path.parent / file_part).resolve()
            if not resolved.exists():
                errors.append(f"{relative}: link target does not exist: {target}")
                continue
            if resolved.is_dir():
                errors.append(f"{relative}: link target is a directory: {target}")
                continue

        if not fragment or resolved.suffix != ".md":
            continue

        if resolved not in anchor_cache:
            anchor_cache[resolved] = anchors_of(resolved)
        if fragment not in anchor_cache[resolved]:
            errors.append(
                f"{relative}: no heading in {resolved.relative_to(root)} "
                f"generates the anchor #{fragment}"
            )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_links.py <repository-directory>")
        return 1

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        fail(f"not a directory: {root}")
        return 1

    anchor_cache: dict[Path, set[str]] = {}
    errors: list[str] = []
    checked = 0
    for path in iter_markdown_files(root):
        checked += 1
        errors.extend(check_file(path, root, anchor_cache))

    if errors:
        for error in errors:
            fail(error)
        print(f"\n{len(errors)} broken link(s) found")
        return 1

    ok(f"all local Markdown links and anchors resolve ({checked} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
