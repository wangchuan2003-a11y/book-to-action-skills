"""Preview or copy selected skills into one existing project without overwriting."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile

from validate import ROOT, validate_skill


def plan_install(source_root: Path, project: Path, names: list[str], host: str) -> list[tuple[Path, Path]]:
    project = project.expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError("project must be an existing directory")
    if host not in {"codex", "claude"}:
        raise ValueError("unsupported host")
    if not names or len(set(names)) != len(names):
        raise ValueError("select at least one skill, without duplicates")
    source_dir = source_root.resolve() / ".agents/skills"
    available = {p.name for p in source_dir.iterdir() if p.is_dir()}
    destination = project / (".agents" if host == "codex" else ".claude") / "skills"
    if not destination.resolve().is_relative_to(project):
        raise ValueError("destination resolves outside the selected project")
    result = []
    for name in names:
        if name not in available:
            raise ValueError(f"unknown skill: {name}")
        source, target = source_dir / name, destination / name
        if source.is_symlink() or not source.resolve().is_relative_to(source_dir.resolve()):
            raise ValueError(f"skill source points outside collection: {name}")
        if target.exists() or target.is_symlink():
            raise ValueError(f"destination already exists; nothing overwritten: {target}")
        errors = validate_skill(source)
        if errors:
            raise ValueError("invalid source: " + "; ".join(errors))
        result.append((source, target))
    return result


def copy_plan(plan: list[tuple[Path, Path]]) -> None:
    if not plan:
        return
    created = []
    try:
        # Prepare the entire batch before publishing any skill directory.
        with tempfile.TemporaryDirectory(prefix="skill-install-") as staging:
            staged = []
            for index, (source, target) in enumerate(plan):
                prepared = Path(staging) / str(index)
                shutil.copytree(source, prepared, symlinks=True,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                if any(path.is_symlink() for path in prepared.rglob("*")):
                    raise ValueError("source changed to contain a symlink")
                staged.append((prepared, target))
            for prepared, target in staged:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.mkdir()  # Reserve exclusively, including against dangling links.
                created.append((target, target.stat()))
                shutil.copytree(prepared, target, dirs_exist_ok=True, symlinks=True)
    except BaseException:
        for target, original in reversed(created):
            # Never remove a path replaced by someone else during installation.
            if not target.is_symlink() and target.exists():
                current = target.stat()
                if (current.st_dev, current.st_ino) == (original.st_dev, original.st_ino):
                    shutil.rmtree(target)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--skills", nargs="+", required=True)
    parser.add_argument("--host", choices=("codex", "claude"), default="codex")
    parser.add_argument("--apply", action="store_true", help="copy after successful preflight")
    args = parser.parse_args()
    try:
        plan = plan_install(ROOT, args.project, args.skills, args.host)
        if args.apply:
            copy_plan(plan)
        print(json.dumps({"applied": args.apply, "files": [
            {"source": str(s), "destination": str(t)} for s, t in plan]}, ensure_ascii=False, indent=2))
        if not args.apply:
            print("Preview only. Add --apply to copy.")
        return 0
    except (ValueError, OSError) as exc:
        print(f"Install stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
