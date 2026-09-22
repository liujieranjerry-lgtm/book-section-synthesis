#!/usr/bin/env python3
"""Structural validation for the book-section-synthesis skill.

This is intentionally narrow: it checks frontmatter, naming, required
references, and the Codex UI metadata. It does not validate behavior.
Behavior is covered by evals/README.md and evals/rubric.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML is required to run this validator.")
    print("Install dev dependencies: python -m pip install -r requirements-dev.txt")
    raise SystemExit(1)

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}

REQUIRED_FILES = (
    "SKILL.md",
    "references/text-types.md",
    "references/fidelity.md",
    "agents/openai.yaml",
    "evals/rubric.md",
    "evals/fixtures/cases.md",
)


def fail(message: str) -> None:
    print(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read_frontmatter(skill_md: Path) -> dict:
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        raise ValueError("SKILL.md does not start with YAML frontmatter")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md frontmatter is not properly closed")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []

    if not skill_dir.is_dir():
        return [f"not a directory: {skill_dir}"]

    for relative in REQUIRED_FILES:
        if not (skill_dir / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return errors or ["SKILL.md not found"]

    try:
        frontmatter = read_frontmatter(skill_md)
    except Exception as exc:  # noqa: BLE001 - report validation error
        return errors + [f"invalid frontmatter: {exc}"]

    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER
    if unexpected:
        errors.append(
            "unexpected frontmatter key(s): " + ", ".join(sorted(unexpected))
        )

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("frontmatter.name is required and must be a string")
    else:
        name = name.strip()
        if not re.fullmatch(r"[a-z0-9-]+", name):
            errors.append("frontmatter.name must be lowercase hyphen-case")
        if name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append("frontmatter.name cannot start/end with '-' or contain '--'")
        if len(name) > MAX_NAME_LENGTH:
            errors.append(f"frontmatter.name is longer than {MAX_NAME_LENGTH} characters")
        if name != skill_dir.name:
            errors.append(
                f"frontmatter.name ({name}) must match the folder name ({skill_dir.name})"
            )

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("frontmatter.description is required and must be a string")
    else:
        description = description.strip()
        if len(description) > MAX_DESCRIPTION_LENGTH:
            errors.append(
                f"frontmatter.description is longer than {MAX_DESCRIPTION_LENGTH} characters"
            )
        if "<" in description or ">" in description:
            errors.append("frontmatter.description cannot contain angle brackets")
        if description.startswith("[TODO:"):
            errors.append("frontmatter.description contains an unfinished TODO")

    if frontmatter.get("license") != "MIT":
        errors.append("frontmatter.license should be MIT for this repository")

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict) or not metadata.get("version"):
        errors.append("frontmatter.metadata.version is required")

    skill_text = skill_md.read_text(encoding="utf-8")
    if re.search(r"\[TODO:[^\]]*\]", skill_text):
        errors.append("SKILL.md contains an unfinished TODO placeholder")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        try:
            ui = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
            interface = ui.get("interface", {}) if isinstance(ui, dict) else {}
            if not interface.get("display_name"):
                errors.append("agents/openai.yaml is missing interface.display_name")
            if not interface.get("short_description"):
                errors.append("agents/openai.yaml is missing interface.short_description")
            if not interface.get("default_prompt"):
                errors.append("agents/openai.yaml is missing interface.default_prompt")
        except Exception as exc:  # noqa: BLE001 - report validation error
            errors.append(f"invalid agents/openai.yaml: {exc}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate.py <skill-directory>")
        return 1

    skill_dir = Path(sys.argv[1]).resolve()
    errors = validate(skill_dir)

    if errors:
        for error in errors:
            fail(error)
        return 1

    ok(f"skill structure is valid: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
