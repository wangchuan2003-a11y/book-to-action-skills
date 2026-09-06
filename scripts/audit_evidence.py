"""Check recorded case coverage and review integrity, not answer truth."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VERDICTS = {"pass", "fail", "uncertain"}


def audit(root: Path) -> dict:
    expected = {}
    errors, initial, retests = [], {}, {}
    for path in (root / ".agents/skills").glob("*/evals/cases.json"):
        for case in json.loads(path.read_text(encoding="utf-8")):
            key = (path.parents[1].name, case["id"])
            if key in expected:
                errors.append(f"duplicate authored case: {':'.join(key)}")
            else:
                expected[key] = case["prompt"]
    base = root / "evals/results"
    try:
        index = json.loads((base / "index.json").read_text(encoding="utf-8"))
        for kind, results in (("initial_runs", initial), ("retest_runs", retests)):
            names = index[kind]
            if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
                raise ValueError(f"invalid {kind} list")
            for name in names:
                file = base / name
                if not file.resolve().is_relative_to(base.resolve()) or file.is_symlink():
                    raise ValueError("evidence file outside results directory")
                record = json.loads(file.read_text(encoding="utf-8"))
                for item in record["cases"]:
                    key = (item["skill"], item["case_id"])
                    label = ":".join(key)
                    if key not in expected:
                        errors.append(f"unknown case: {label}")
                    elif item["prompt"] != expected[key]:
                        errors.append(f"prompt changed; select matching evidence: {label}")
                    if key in results:
                        errors.append(f"duplicate {kind} case: {label}")
                    review = item["review"]
                    if (not isinstance(item.get("answer"), str) or not item["answer"].strip()
                            or review.get("verdict") not in VERDICTS
                            or not isinstance(review.get("reason"), str) or not review["reason"].strip()):
                        errors.append(f"missing answer or review: {label}")
                    results[key] = review.get("verdict")
        for key in retests:
            if key not in initial:
                errors.append(f"retest without initial case: {':'.join(key)}")
    except (OSError, KeyError, TypeError, ValueError) as exc:
        errors.append(f"cannot audit evidence: {exc}")
    latest = {**initial, **retests}
    missing = sorted(":".join(k) for k in expected.keys() - initial.keys())
    unresolved = sorted(":".join(k) for k, verdict in latest.items()
                        if k in expected and verdict != "pass")
    return {"authored_cases": len(expected), "recorded_initial_cases": len(initial),
            "initial_verdicts": {v: list(initial.values()).count(v) for v in sorted(VERDICTS)},
            "retested_cases": len(retests), "missing_cases": missing,
            "latest_not_pass": unresolved, "errors": errors,
            "scope": "record and coverage integrity only; reviews are recorded judgments"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    result = audit(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(result["errors"] or (args.require_complete
                and (result["missing_cases"] or result["latest_not_pass"])))


if __name__ == "__main__":
    sys.exit(main())
