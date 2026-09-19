"""Content identities for evaluation cases and the material supplied to an agent."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def digest(value: object) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def skill_digest(folder: Path) -> str:
    """Hash runtime material; case definitions are bound individually, not as a batch."""
    folder = folder.resolve()
    manifest = {}
    for path in sorted(folder.rglob("*")):
        relative = path.relative_to(folder)
        # Packaging adds LICENSE; it is not agent material and must not stale an archive.
        if (relative.parts[0] == "evals" or "__pycache__" in relative.parts
                or path.suffix == ".pyc" or relative.as_posix() == "LICENSE"):
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(folder):
            raise ValueError(f"external evaluation material: {relative}")
        if path.is_file():
            manifest[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest(manifest)


def case_binding(folder: Path, case: dict, material_digest: str | None = None) -> dict:
    return {"schema_version": 1, "case_sha256": digest(case),
            "skill_sha256": material_digest or skill_digest(folder)}
