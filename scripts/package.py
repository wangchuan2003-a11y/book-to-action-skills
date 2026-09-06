"""Build reproducible distribution archives after local contract checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import zipfile

from build_catalog import render
from validate import ROOT, validate_collection, validate_public_file


def archive(destination: Path, files: list[tuple[Path, str]]) -> None:
    # Small text bundles use STORE so zlib versions cannot change archive bytes.
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_STORED) as bundle:
        for source, name in sorted(files, key=lambda item: item[1]):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes())
    with zipfile.ZipFile(destination) as bundle:
        if bundle.testzip() is not None:
            raise ValueError(f"archive failed CRC check: {destination.name}")


def package(root: Path) -> list[Path]:
    errors, _ = validate_collection(root)
    if errors:
        raise ValueError("package validation failed: " + "; ".join(errors))
    catalog, readme = render(root)
    if ((root / "catalog.json").read_text(encoding="utf-8") != catalog
            or (root / "README.md").read_text(encoding="utf-8") != readme):
        raise ValueError("catalog is stale; run scripts/build_catalog.py first")
    output = root / "dist"
    if output.is_symlink() or not output.resolve().is_relative_to(root.resolve()):
        raise ValueError("dist must resolve inside the repository")
    output.mkdir(exist_ok=True)
    artifacts = []
    all_files = []
    for folder in sorted((root / ".agents/skills").iterdir()):
        if not folder.is_dir():
            continue
        files = [(p, f"{folder.name}/{p.relative_to(folder).as_posix()}")
                 for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts
                 and p.suffix != ".pyc"]
        # Complete release archives already carry each skill's license.
        if not (folder / "LICENSE").is_file():
            files.append((root / "LICENSE", f"{folder.name}/LICENSE"))
        target = output / f"{folder.name}.zip"
        archive(target, files)
        artifacts.append(target)
        all_files.extend((p, f".agents/skills/{name}") for p, name in files)
    # The reviewed manifest selects ancillary files; never recursively sweep docs/evals.
    manifest_path = root / "distribution.json"
    manifest_errors = validate_public_file(manifest_path, root)
    if manifest_errors:
        raise ValueError("; ".join(manifest_errors))
    names = json.loads(manifest_path.read_text(encoding="utf-8"))["files"]
    if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
        raise ValueError("distribution files must be a list of paths")
    if len(names) != len(set(names)):
        raise ValueError("duplicate distribution paths")
    for name in names + ["distribution.json"]:
        if Path(name).is_absolute() or ".." in Path(name).parts or "\\" in name:
            raise ValueError(f"invalid distribution path: {name}")
        file = root / name
        file_errors = validate_public_file(file, root)
        if file_errors:
            raise ValueError("; ".join(file_errors))
        all_files.append((file, name))
    if len({name for _, name in all_files}) != len(all_files):
        raise ValueError("duplicate archive member")
    target = output / "book-to-action-skills.zip"
    archive(target, all_files)
    artifacts.append(target)
    checksum = output / "SHA256SUMS.txt"
    checksum.write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
                                for p in artifacts), encoding="utf-8", newline="\n")
    return artifacts + [checksum]


def main() -> int:
    try:
        outputs = package(ROOT)
        print("\n".join(str(p.relative_to(ROOT)) for p in outputs))
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f"Packaging stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
