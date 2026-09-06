"""Validate the collection's portable package contract, not factual truth."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"primary_text", "author_material", "publisher", "academic", "independent_research"}
REQUIRED_FILES = (
    "SKILL.md", "book.json", "agents/openai.yaml",
    "references/source-notes.md", "references/worked-example.md", "evals/cases.json",
)


def string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def strings(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(string(v) for v in value)


def safe_url(value: object) -> bool:
    if not string(value):
        return False
    try:
        parsed = urlsplit(value)
        return (parsed.scheme in {"http", "https"} and bool(parsed.hostname)
                and not parsed.username and not parsed.password
                and not any(c.isspace() for c in value))
    except ValueError:
        return False


def is_inside(path: Path, parent: Path) -> bool:
    return path.resolve().is_relative_to(parent.resolve())


def latest_civil_date(now: datetime | None = None) -> date:
    """Access dates are local dates; UTC runners must allow today's UTC+14 date."""
    instant = now if now is not None else datetime.now(timezone.utc)
    return instant.astimezone(timezone(timedelta(hours=14))).date()


def validate_public_file(path: Path, root: Path) -> list[str]:
    """Review every selected release file, including files outside skill folders."""
    if not path.is_file() or path.is_symlink() or not is_inside(path, root):
        return [f"missing or external distribution file: {path.name}"]
    if path.suffix not in {".md", ".json", ".yaml", ".py"} and path.name != "LICENSE":
        return [f"unsupported distributable file: {path.name}"]
    if path.stat().st_size > 500_000:
        return [f"file exceeds 500 KB review limit: {path.name}"]
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeError, OSError):
        return [f"cannot read UTF-8 text: {path.name}"]
    errors = []
    if "\ufffd" in content or "\ufeff" in content:
        errors.append(f"invalid encoding marker: {path.name}")
    if re.search(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{20,})", content):
        errors.append(f"possible credential in {path.name}")
    return errors


def frontmatter(text: str) -> dict[str, str]:
    """This repository intentionally uses a tiny, JSON-quoted YAML subset."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening YAML delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing YAML delimiter") from exc
    fields = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep or key in fields:
            raise ValueError("invalid or duplicate frontmatter field")
        value = value.strip()
        fields[key] = json.loads(value) if value.startswith('"') else value
    if not "\n".join(lines[end + 1:]).strip():
        raise ValueError("empty skill body")
    return fields


def validate_skill(folder: Path) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(f"{folder.name}: {message}")

    require(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", folder.name))
            and len(folder.name) < 64, "invalid skill directory name")
    for item in REQUIRED_FILES:
        path = folder / item
        require(path.is_file() and is_inside(path, folder), f"missing or external file: {item}")
    if errors:
        return errors
    try:
        text = (folder / "SKILL.md").read_text(encoding="utf-8")
        fields = frontmatter(text)
        require(fields.get("name") == folder.name, "frontmatter name mismatch")
        require(string(fields.get("description")), "description is empty")
        require(len(fields.get("description", "")) <= 1024, "description exceeds 1024 characters")
        require(len(text.splitlines()) <= 220, "entrypoint exceeds project limit of 220 lines")
        for ref in ("references/source-notes.md", "references/worked-example.md"):
            require(ref in text, f"entrypoint does not route to {ref}")
        book = json.loads((folder / "book.json").read_text(encoding="utf-8"))
        if not isinstance(book, dict):
            raise ValueError("book.json must be an object")
        require(book.get("id") == folder.name, "book ID mismatch")
        for key in ("title", "title_zh", "year", "summary", "selection_rationale"):
            require(string(book.get(key)), f"invalid book field: {key}")
        for key in ("authors", "domains", "use_cases", "limits"):
            require(strings(book.get(key)), f"invalid nonempty string list: {key}")
        sources = book.get("sources")
        require(isinstance(sources, list) and bool(sources), "sources must be nonempty")
        notes = (folder / "references/source-notes.md").read_text(encoding="utf-8")
        ids = set()
        for source in sources if isinstance(sources, list) else []:
            if not isinstance(source, dict):
                require(False, "source must be an object")
                continue
            for key in ("id", "title", "accessed", "coverage", "used_for", "limitations"):
                require(string(source.get(key)), f"source field missing: {key}")
            sid = source.get("id")
            if not string(sid):
                continue
            require(sid not in ids, f"duplicate source ID: {sid}")
            ids.add(sid)
            require(sid in notes, f"source ID not discussed in notes: {sid}")
            require(source.get("kind") in KINDS, f"invalid source kind: {sid}")
            require(safe_url(source.get("url")), f"invalid source URL: {sid}")
            accessed = date.fromisoformat(source["accessed"])
            require(accessed <= latest_civil_date(), f"future access date: {sid}")
        cases = json.loads((folder / "evals/cases.json").read_text(encoding="utf-8"))
        require(isinstance(cases, list) and len(cases) >= 3, "at least three behavior cases required")
        case_ids = set()
        for case in cases if isinstance(cases, list) else []:
            if not isinstance(case, dict):
                require(False, "case must be an object")
                continue
            cid = case.get("id")
            if not string(cid):
                require(False, "invalid case ID")
                continue
            require(cid not in case_ids, f"duplicate case ID: {cid}")
            case_ids.add(cid)
            require(string(case.get("prompt")), f"missing prompt: {cid}")
            for key in ("must_include", "must_avoid"):
                require(strings(case.get(key)), f"invalid {key}: {cid}")
        interface = (folder / "agents/openai.yaml").read_text(encoding="utf-8")
        require("interface:" in interface, "missing UI interface")
        for key in ("display_name", "short_description", "default_prompt"):
            match = re.search(rf"^  {key}: (.+)$", interface, re.MULTILINE)
            if not match:
                require(False, f"missing UI field: {key}")
                continue
            value = json.loads(match.group(1))
            require(string(value), f"empty UI field: {key}")
            if key == "short_description":
                require(25 <= len(value) <= 64, "UI short_description must have 25–64 characters")
            if key == "default_prompt":
                require(f"${folder.name}" in value, "UI prompt does not invoke this skill")
        for file in folder.rglob("*"):
            require(is_inside(file, folder), f"external path: {file.name}")
            require(not file.is_symlink(), f"symlink not distributable: {file.name}")
            if "__pycache__" in file.parts or file.suffix == ".pyc":
                continue
            if file.is_file():
                errors.extend(f"{folder.name}: {error}" for error in validate_public_file(file, folder))
            if file.is_file() and file.suffix in {".md", ".json", ".yaml"}:
                content = file.read_text(encoding="utf-8")
                require(not re.search(r"(?:[A-Z]:[\\/](?:Users|codex_mianshi)|/Users/)", content),
                        f"personal absolute path: {file.name}")
                if file.suffix == ".md":
                    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
                        target = target.strip("<>")
                        if target.startswith("#"):
                            continue
                        if ":" in target:
                            require(safe_url(target), f"unsafe link in {file.name}: {target}")
                        else:
                            linked = file.parent / unquote(target.split("#", 1)[0])
                            require(is_inside(linked, folder) and linked.exists(),
                                    f"missing or external local link in {file.name}: {target}")
    except (ValueError, TypeError, KeyError, OSError) as exc:
        require(False, f"cannot validate: {exc}")
    return errors


def validate_collection(root: Path) -> tuple[list[str], int]:
    skills_dir = root / ".agents/skills"
    folders = sorted(path.parent for path in skills_dir.glob("*/SKILL.md"))
    errors = [] if folders else ["collection has no skills"]
    if skills_dir.exists():
        for folder in skills_dir.iterdir():
            if folder.is_dir() and not (folder / "SKILL.md").exists():
                errors.append(f"{folder.name}: directory has no SKILL.md")
    for folder in folders:
        errors.extend(validate_skill(folder))
    return errors, len(folders)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors, count = validate_collection(args.root)
    print(json.dumps({"skills": count, "errors": errors, "scope": "package structure only"},
                     ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
