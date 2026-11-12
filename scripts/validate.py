#!/usr/bin/env python3
"""Structural validation for the book-section-synthesis repository.

Checks the repository-level contract (docs, changelog, plugin manifests, version
alignment), the installable skill in skill/book-section-synthesis/, and the two
reference documents that SKILL.md depends on.

Standard library only: CI runs this without installing anything, so the supply
chain stays empty. It does not validate behavior; behavior is covered by
evals/README.md, evals/rubric.md and evals/fixtures/cases.md.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_CHARS = 10000

ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}

SKILL_SUBDIR = Path("skill") / "book-section-synthesis"
PLUGIN_MANIFEST = Path(".claude-plugin") / "plugin.json"
MARKETPLACE_MANIFEST = Path(".claude-plugin") / "marketplace.json"

# Top-level sections of README.md that are allowed to be absent from the 目录 list.
README_TOC_EXEMPT = {"目录"}

# Plugin entries inherit component fields from plugin.json. Declaring them again in
# the marketplace entry makes Claude Code append them a second time, so they are
# rejected here.
ENTRY_FORBIDDEN_FIELDS = {
    "skills",
    "commands",
    "agents",
    "hooks",
    "outputStyles",
    "themes",
    "mcpServers",
    "lspServers",
    "userConfig",
    "channels",
    "version",
    "description",
}

ENTRY_ALLOWED_FIELDS = {
    "name",
    "source",
    "category",
    "tags",
    "relevance",
    "defaultEnabled",
    "strict",
    "metadata",
}

REQUIRED_REPO_FILES = (
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "AGENTS.md",
    "SECURITY.md",
    "LICENSE",
    "QUICK_PROMPTS.md",
    "scripts/check_links.py",
    "scripts/release_notes.py",
    PLUGIN_MANIFEST.as_posix(),
    MARKETPLACE_MANIFEST.as_posix(),
    ".github/workflows/validate.yml",
    ".github/workflows/release.yml",
    "evals/README.md",
    "evals/rubric.md",
    "evals/fixtures/cases.md",
)

REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/text-types.md",
    "references/fidelity.md",
    "references/examples/chapter-synthetic-input.md",
    "references/examples/chapter-expected-output.md",
    "references/examples/chapter-anti-example.md",
)


class FrontmatterError(ValueError):
    """Raised when the frontmatter subset parser meets something it cannot read."""


def fail(message: str) -> None:
    print(f"[FAIL] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


# --------------------------------------------------------------------------- #
# Minimal YAML subset parser (no dependencies)
# --------------------------------------------------------------------------- #


def _unquote(raw: str) -> str:
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        inner = raw[1:-1]
        if raw[0] == '"':
            return inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner.replace("''", "'")
    return raw


def _parse_scalar(raw: str) -> object:
    raw = raw.strip()
    if raw in ("", "~", "null", "Null", "NULL"):
        return None
    if raw in ("true", "True", "TRUE"):
        return True
    if raw in ("false", "False", "FALSE"):
        return False
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return _unquote(raw)


def _strip_inline_comment(raw: str) -> str:
    """Remove a trailing ` # comment`, ignoring hashes inside quotes."""
    quote = None
    for index, char in enumerate(raw):
        if quote:
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == "#" and index > 0 and raw[index - 1] in " \t":
            return raw[:index].rstrip()
    return raw


def parse_mapping(text: str, origin: str) -> dict:
    """Parse the flat/scalar YAML subset this repository uses.

    Supports nested mappings, quoted scalars, booleans, integers and block
    scalars. Anything else (sequences, anchors, multi-line flow) raises, so a
    change in the file shape fails loudly instead of being silently misread.
    """
    lines = text.splitlines()
    result: dict = {}
    stack: list[tuple[int, dict]] = [(-1, result)]
    index = 0

    while index < len(lines):
        raw = lines[index]
        index += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw[: len(raw) - len(raw.lstrip(" \t"))]
        if "\t" in indented:
            raise FrontmatterError(f"{origin}: tabs are not allowed for indentation")
        indent = len(indented)
        body = _strip_inline_comment(raw[indent:]).strip()
        if not body:
            continue
        if ":" not in body:
            raise FrontmatterError(f"{origin}: cannot parse line: {raw!r}")
        key, _, rest = body.partition(":")
        key = _unquote(key.strip())
        rest = rest.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise FrontmatterError(f"{origin}: bad indentation near {raw!r}")
        parent = stack[-1][1]
        if key in parent:
            raise FrontmatterError(f"{origin}: duplicate key {key!r}")

        if rest in ("|", "|-", ">", ">-"):
            block: list[str] = []
            while index < len(lines):
                candidate = lines[index]
                if candidate.strip() and (
                    len(candidate) - len(candidate.lstrip(" ")) <= indent
                ):
                    break
                block.append(candidate.strip())
                index += 1
            parent[key] = ("\n" if rest.startswith("|") else " ").join(block).strip()
            continue

        if rest == "":
            child: dict = {}
            parent[key] = child
            stack.append((indent, child))
            continue

        parent[key] = _parse_scalar(rest)

    return result


def read_frontmatter(skill_md: Path) -> dict:
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        raise FrontmatterError("SKILL.md does not start with YAML frontmatter")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise FrontmatterError("SKILL.md frontmatter is not properly closed")
    data = parse_mapping(match.group(1), "SKILL.md frontmatter")
    if not isinstance(data, dict):
        raise FrontmatterError("frontmatter must be a mapping")
    return data


# --------------------------------------------------------------------------- #
# Individual checks
# --------------------------------------------------------------------------- #


def check_frontmatter(frontmatter: dict, skill_dir: Path, errors: list[str]) -> None:
    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER
    if unexpected:
        errors.append("unexpected frontmatter key(s): " + ", ".join(sorted(unexpected)))

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
            errors.append(
                f"frontmatter.name is longer than {MAX_NAME_LENGTH} characters"
            )
        if name != skill_dir.name:
            errors.append(
                f"frontmatter.name ({name}) must match the skill folder name ({skill_dir.name})"
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


def check_skill_text(skill_md: Path, skill_dir: Path, errors: list[str]) -> None:
    text = skill_md.read_text(encoding="utf-8")
    if re.search(r"\[TODO:[^\]]*\]", text):
        errors.append("SKILL.md contains an unfinished TODO placeholder")
    if len(text) > MAX_SKILL_CHARS:
        errors.append(
            f"SKILL.md is {len(text)} characters, over the {MAX_SKILL_CHARS} limit; "
            "move detail into references/"
        )

    for cited in sorted(set(re.findall(r"references/[A-Za-z0-9_./-]+\.md", text))):
        if not (skill_dir / cited).is_file():
            errors.append(f"SKILL.md cites a reference file that does not exist: {cited}")

    gate = re.search(r"^## 交付门\s*$(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not gate:
        errors.append("SKILL.md has no 交付门 section")
    else:
        numbers = [int(n) for n in re.findall(r"^(\d+)\. ", gate.group(1), re.MULTILINE)]
        if not numbers:
            errors.append("SKILL.md 交付门 lists no numbered items")
        elif numbers != list(range(1, len(numbers) + 1)):
            errors.append(f"SKILL.md 交付门 numbering is not 1..N: {numbers}")


def parse_changelog_versions(changelog: str) -> list[str]:
    return [
        match.group(1)
        for match in re.finditer(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.MULTILINE)
    ]


def check_changelog(changelog_text: str, version: str, errors: list[str]) -> None:
    if "## [Unreleased]" not in changelog_text:
        errors.append("CHANGELOG.md has no [Unreleased] section")
    versions = parse_changelog_versions(changelog_text)
    if not versions:
        errors.append("CHANGELOG.md has no released version section")
        return
    if len(set(versions)) != len(versions):
        errors.append("CHANGELOG.md repeats a version section")
    if versions != sorted(versions, key=_version_key, reverse=True):
        errors.append(f"CHANGELOG.md versions are not in descending order: {versions}")
    if versions[0] != version:
        errors.append(
            f"CHANGELOG.md newest release ({versions[0]}) does not match "
            f"SKILL.md metadata.version ({version})"
        )


def _version_key(version: str) -> tuple[int, int, int]:
    major, minor, patch = (int(part) for part in version.split("."))
    return (major, minor, patch)


def check_readme(readme_text: str, version: str, errors: list[str]) -> None:
    badge = re.search(r"badge/version-(\d+\.\d+\.\d+)-", readme_text)
    if not badge:
        errors.append("README.md has no version badge")
    elif badge.group(1) != version:
        errors.append(
            f"README.md badge says {badge.group(1)}, SKILL.md says {version}"
        )

    headings = [
        match.group(1).strip()
        for match in re.finditer(r"^## (.+)$", readme_text, re.MULTILINE)
    ]
    toc_block = re.search(r"^## 目录\s*$(.*?)(?=^## |\Z)", readme_text, re.MULTILINE | re.DOTALL)
    if not toc_block:
        errors.append("README.md has no 目录 section")
        return
    toc_entries = [
        match.group(1).strip()
        for match in re.finditer(r"^- \[(.+?)\]\(#[^)]*\)$", toc_block.group(1), re.MULTILINE)
    ]
    if not toc_entries:
        errors.append("README.md 目录 lists no entries")
        return
    for entry in toc_entries:
        if entry not in headings:
            errors.append(f"README.md 目录 entry points at no heading: {entry}")
    expected = [h for h in headings if h not in README_TOC_EXEMPT]
    for heading in expected:
        if heading not in toc_entries:
            errors.append(f"README.md heading is missing from 目录: {heading}")
    if len(expected) != len(toc_entries):
        errors.append(
            f"README.md 目录 has {len(toc_entries)} entries for {len(expected)} sections"
        )


def _load_json(path: Path, errors: list[str]) -> dict | None:
    if not path.is_file():
        errors.append(f"missing manifest: {path.as_posix()}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path.as_posix()}: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path.as_posix()} must contain a JSON object")
        return None
    return data


def _check_relative_dir(root: Path, value: str, where: str, errors: list[str]) -> Path | None:
    if ".." in value or "\\" in value:
        errors.append(f"{where}: path cannot contain '..' or a backslash: {value}")
        return None
    if not value.startswith("./"):
        errors.append(f"{where}: path must start with './': {value}")
        return None
    target = (root / value[2:]).resolve()
    if not target.is_dir():
        errors.append(f"{where}: path is not an existing directory: {value}")
        return None
    return target


def check_plugin(
    root: Path, version: str, skill_dir: Path, description: str | None, errors: list[str]
) -> None:
    manifest = _load_json(root / PLUGIN_MANIFEST, errors)
    if manifest is None:
        return
    name = manifest.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", name):
        errors.append("plugin.json: name must be kebab-case and start alphanumeric")
    elif name != skill_dir.name:
        errors.append(
            f"plugin.json: name ({name}) must match the skill folder name ({skill_dir.name})"
        )
    if manifest.get("version") != version:
        errors.append(
            f"plugin.json: version ({manifest.get('version')}) does not match "
            f"SKILL.md metadata.version ({version})"
        )
    if not manifest.get("description"):
        errors.append("plugin.json: description is required")
    elif description and manifest.get("description").strip() != description:
        errors.append(
            "plugin.json: description must match SKILL.md frontmatter.description verbatim"
        )
    if manifest.get("license") != "MIT":
        errors.append("plugin.json: license should be MIT")
    if not manifest.get("repository"):
        errors.append("plugin.json: repository is required")

    skills = manifest.get("skills")
    if not isinstance(skills, list) or not skills:
        errors.append("plugin.json: skills must be a non-empty array of directories")
        return
    for entry in skills:
        if not isinstance(entry, str):
            errors.append(f"plugin.json: skills entry must be a string: {entry!r}")
            continue
        target = _check_relative_dir(root, entry, "plugin.json: skills", errors)
        if target and not (target / "SKILL.md").is_file():
            errors.append(f"plugin.json: skills directory has no SKILL.md: {entry}")


def check_marketplace(root: Path, errors: list[str]) -> None:
    manifest = _load_json(root / MARKETPLACE_MANIFEST, errors)
    if manifest is None:
        return
    name = manifest.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        errors.append("marketplace.json: name must start alphanumeric, letters/digits/._- only")
    else:
        if ".." in name:
            errors.append("marketplace.json: name cannot contain '..'")
        if not name.isascii():
            errors.append("marketplace.json: name must be ASCII")
    owner = manifest.get("owner")
    if not isinstance(owner, dict) or not owner.get("name"):
        errors.append("marketplace.json: owner.name is required")
    plugins = manifest.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("marketplace.json: plugins must be a non-empty array")
        return
    seen: set[str] = set()
    for index, entry in enumerate(plugins):
        where = f"marketplace.json plugins[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{where}: must be an object")
            continue
        entry_name = entry.get("name")
        if not isinstance(entry_name, str) or not re.fullmatch(
            r"[a-z0-9][a-z0-9._-]*", entry_name
        ):
            errors.append(f"{where}: name must be kebab-case and start alphanumeric")
        elif entry_name in seen:
            errors.append(f"{where}: duplicate plugin name {entry_name}")
        else:
            seen.add(entry_name)
        for key in sorted(set(entry) & ENTRY_FORBIDDEN_FIELDS):
            errors.append(
                f"{where}: field '{key}' must live in plugin.json, not the marketplace entry"
            )
        for key in sorted(set(entry) - ENTRY_ALLOWED_FIELDS - ENTRY_FORBIDDEN_FIELDS):
            errors.append(f"{where}: unexpected field '{key}'")
        source = entry.get("source")
        if not isinstance(source, str):
            errors.append(f"{where}: source must be a relative path string")
            continue
        if source != ".":
            _check_relative_dir(root, source, f"{where}: source", errors)


def check_openai_yaml(skill_dir: Path, errors: list[str]) -> None:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.is_file():
        return
    try:
        data = parse_mapping(path.read_text(encoding="utf-8"), path.as_posix())
    except FrontmatterError as exc:
        errors.append(f"invalid agents/openai.yaml: {exc}")
        return
    interface = data.get("interface")
    if not isinstance(interface, dict):
        errors.append("agents/openai.yaml: interface mapping is required")
        return
    for key in ("display_name", "short_description", "default_prompt"):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"agents/openai.yaml: missing interface.{key}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    if not root.is_dir():
        return [f"not a directory: {root}"]

    for relative in REQUIRED_REPO_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required repository file: {relative}")

    skill_dir = root / SKILL_SUBDIR
    if not skill_dir.is_dir():
        errors.append(f"missing skill directory: {SKILL_SUBDIR}")
        return errors

    for relative in REQUIRED_SKILL_FILES:
        if not (skill_dir / relative).is_file():
            errors.append(f"missing required skill file: {SKILL_SUBDIR / relative}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return errors + ["SKILL.md not found"]

    try:
        frontmatter = read_frontmatter(skill_md)
    except FrontmatterError as exc:
        return errors + [f"invalid frontmatter: {exc}"]

    check_frontmatter(frontmatter, skill_dir, errors)
    check_skill_text(skill_md, skill_dir, errors)
    check_openai_yaml(skill_dir, errors)

    metadata = frontmatter.get("metadata")
    version = None
    if isinstance(metadata, dict):
        raw_version = metadata.get("version")
        if isinstance(raw_version, str) and re.fullmatch(r"\d+\.\d+\.\d+", raw_version):
            version = raw_version
    if version is None:
        errors.append("SKILL.md metadata.version must be a quoted x.y.z string")

    changelog = root / "CHANGELOG.md"
    if version and changelog.is_file():
        check_changelog(changelog.read_text(encoding="utf-8"), version, errors)

    readme = root / "README.md"
    if version and readme.is_file():
        check_readme(readme.read_text(encoding="utf-8"), version, errors)

    if version:
        description = frontmatter.get("description")
        check_plugin(
            root,
            version,
            skill_dir,
            description.strip() if isinstance(description, str) else None,
            errors,
        )
    check_marketplace(root, errors)

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate.py <repository-directory>")
        return 1

    root = Path(sys.argv[1]).resolve()
    errors = validate(root)

    if errors:
        for error in errors:
            fail(error)
        print(f"\n{len(errors)} problem(s) found")
        return 1

    ok(f"repository, skill and manifests are consistent: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
