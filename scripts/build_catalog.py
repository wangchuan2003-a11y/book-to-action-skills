"""Generate a deterministic catalog and README table from per-book metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
START, END = "<!-- catalog:start -->", "<!-- catalog:end -->"


def render(root: Path) -> tuple[str, str]:
    books = [json.loads(p.read_text(encoding="utf-8"))
             for p in sorted((root / ".agents/skills").glob("*/book.json"))]
    payload = {"schema_version": 1, "books": books}
    catalog = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    rows = ["| 你遇到的问题 | 书籍 / Skill |", "| --- | --- |"]
    for book in books:
        escape = lambda s: s.replace("|", "\\|").replace("\n", " ")
        use_case = escape(book["use_cases"][0])
        title = escape(book["title_zh"])
        sid = book["id"]
        rows.append(f"| {use_case} | [{title}](.agents/skills/{sid}/SKILL.md) · `{sid}` |")
    readme = (root / "README.md").read_text(encoding="utf-8")
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must have exactly one catalog marker pair")
    before, rest = readme.split(START)
    _, after = rest.split(END)
    return catalog, before + START + "\n" + "\n".join(rows) + "\n" + END + after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog, readme = render(args.root)
    outputs = {args.root / "catalog.json": catalog, args.root / "README.md": readme}
    if args.check:
        stale = [str(p.relative_to(args.root)) for p, text in outputs.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        print("Catalog stale: " + ", ".join(stale) if stale else "Catalog is current.")
        return bool(stale)
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8", newline="\n")
    print("Generated catalog.json and README catalog.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
