"""Check evidence coverage and version bindings, not answer truth or execution."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from evidence_binding import case_binding, skill_digest

ROOT = Path(__file__).resolve().parents[1]
VERDICTS = {"pass", "fail", "uncertain"}


def evidence_file(base: Path, name: str) -> Path:
    file = base / name
    if not file.resolve().is_relative_to(base.resolve()) or file.is_symlink():
        raise ValueError("evidence file outside results directory")
    return file


def binding_state(item: dict, expected: dict, baseline: dict, filename: str,
                  record_sha256: str, label: str) -> tuple[str, str | None]:
    binding = item.get("binding")
    if binding is not None:
        if binding == expected:
            return "version-bound", None
        return "stale", "case criteria or skill material differs from the recorded binding"
    if (baseline.get("records_sha256", {}).get(filename) == record_sha256
            and baseline.get("cases_sha256", {}).get(label) == expected["case_sha256"]
            and baseline.get("skills_sha256", {}).get(item["skill"]) == expected["skill_sha256"]):
        return "adopted-baseline", None
    return "stale", "missing binding or historical audit baseline no longer matches"


def audit(root: Path) -> dict:
    expected = {}
    errors, initial, retests = [], {}, {}
    baseline = {}
    try:
        for path in (root / ".agents/skills").glob("*/evals/cases.json"):
            folder = path.parents[1]
            material = skill_digest(folder)
            for case in json.loads(path.read_text(encoding="utf-8")):
                key = (folder.name, case["id"])
                if key in expected:
                    errors.append(f"duplicate authored case: {':'.join(key)}")
                else:
                    expected[key] = {"prompt": case["prompt"], "binding": case_binding(folder, case, material)}
        base = root / "evals/results"
        index = json.loads((base / "index.json").read_text(encoding="utf-8"))
        if "adopted_baseline" in index:
            baseline = json.loads(evidence_file(base, index["adopted_baseline"]).read_text(encoding="utf-8"))
            if baseline.get("schema_version") != 1 or baseline.get("kind") != "adopted-audit-baseline":
                raise ValueError("unsupported historical audit baseline")
        for kind, results in (("initial_runs", initial), ("retest_runs", retests)):
            names = index[kind]
            if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
                raise ValueError(f"invalid {kind} list")
            for name in names:
                payload = evidence_file(base, name).read_bytes()
                record_sha256 = hashlib.sha256(payload).hexdigest()
                record = json.loads(payload)
                for item in record["cases"]:
                    key = (item["skill"], item["case_id"])
                    label = ":".join(key)
                    state, reason = "stale", "unknown case"
                    if key not in expected:
                        errors.append(f"unknown case: {label}")
                    else:
                        if item["prompt"] != expected[key]["prompt"]:
                            errors.append(f"prompt changed; select matching evidence: {label}")
                        state, reason = binding_state(item, expected[key]["binding"], baseline,
                                                      name, record_sha256, label)
                    if key in results:
                        errors.append(f"duplicate {kind} case: {label}")
                    review = item["review"]
                    if (not isinstance(item.get("answer"), str) or not item["answer"].strip()
                            or not isinstance(review, dict) or review.get("verdict") not in VERDICTS
                            or not isinstance(review.get("reason"), str) or not review["reason"].strip()):
                        errors.append(f"missing answer or review: {label}")
                    results[key] = {"verdict": review.get("verdict") if isinstance(review, dict) else None,
                                    "binding_state": state, "stale_reason": reason}
        for key in retests:
            if key not in initial:
                errors.append(f"retest without initial case: {':'.join(key)}")
    except (OSError, KeyError, TypeError, ValueError, AttributeError) as exc:
        errors.append(f"cannot audit evidence: {exc}")
    latest = {**initial, **retests}
    missing = sorted(":".join(k) for k in expected.keys() - initial.keys())
    unresolved = sorted(":".join(k) for k, item in latest.items()
                        if k in expected and item["verdict"] != "pass")
    stale = {":".join(k): item["stale_reason"] for k, item in latest.items()
             if k in expected and item["binding_state"] == "stale"}
    return {"authored_cases": len(expected), "recorded_initial_cases": len(initial),
            "initial_verdicts": {v: sum(item["verdict"] == v for item in initial.values())
                                 for v in sorted(VERDICTS)},
            "retested_cases": len(retests), "missing_cases": missing,
            "latest_not_pass": unresolved, "stale_cases": sorted(stale), "stale_reasons": stale,
            "version_bound_cases": sum(item["binding_state"] == "version-bound" for item in latest.values()),
            "adopted_baseline_cases": sum(item["binding_state"] == "adopted-baseline" for item in latest.values()),
            "errors": errors,
            "scope": "record integrity only; adopted baseline is not a rerun or proof of historical source versions"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    result = audit(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(result["errors"] or (args.require_complete
                and (result["missing_cases"] or result["latest_not_pass"] or result["stale_cases"])))


if __name__ == "__main__":
    sys.exit(main())
