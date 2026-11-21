#!/usr/bin/env python3
"""Validate JRS runtime-evaluation definitions and optional captured results."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "tests" / "evals" / "cases.json"
REQUIRED_CASE_FIELDS = {
    "id",
    "prompt",
    "expected_skill",
    "expected_department",
    "expected_mode",
}
REQUIRED_RESULT_FIELDS = {
    "id",
    "selected_skill",
    "department",
    "mode",
    "tier_dispatches",
    "principal_calls",
    "final_output",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_array(path: Path) -> list[dict]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read {path}: {error}")
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        fail(f"{path} must contain a JSON array of objects")
    return value


cases = load_array(CASE_PATH)
case_map: dict[str, dict] = {}
for case in cases:
    missing = REQUIRED_CASE_FIELDS - case.keys()
    if missing:
        fail(f"case is missing {sorted(missing)}: {case}")
    if case["id"] in case_map:
        fail(f"duplicate case id: {case['id']}")
    if case["expected_mode"] not in {"Lean", "Balanced", "Assurance"}:
        fail(f"{case['id']}: invalid expected mode")
    case_map[case["id"]] = case

if len(cases) < 7:
    fail("runtime suite must retain at least seven release cases")

if len(sys.argv) == 1:
    print(f"Runtime evaluation definitions passed: {len(cases)} cases.")
    raise SystemExit(0)
if len(sys.argv) != 2:
    fail("usage: evaluate_results.py [results.json]")

results = load_array(Path(sys.argv[1]))
result_map = {result.get("id"): result for result in results}
missing_results = set(case_map) - result_map.keys()
if missing_results:
    fail(f"results missing cases: {sorted(missing_results)}")

errors: list[str] = []
for case_id, case in case_map.items():
    result = result_map[case_id]
    missing = REQUIRED_RESULT_FIELDS - result.keys()
    if missing:
        errors.append(f"{case_id}: missing result fields {sorted(missing)}")
        continue

    for result_key, case_key in (
        ("selected_skill", "expected_skill"),
        ("department", "expected_department"),
        ("mode", "expected_mode"),
    ):
        if result[result_key] != case[case_key]:
            errors.append(
                f"{case_id}: {result_key} {result[result_key]!r} != {case[case_key]!r}"
            )

    for metric in ("tier_dispatches", "principal_calls"):
        if not isinstance(result[metric], int) or result[metric] < 0:
            errors.append(f"{case_id}: {metric} must be a non-negative integer")
            continue
        maximum = case.get(f"max_{metric}")
        minimum = case.get(f"min_{metric}")
        if maximum is not None and result[metric] > maximum:
            errors.append(f"{case_id}: {metric} {result[metric]} exceeds {maximum}")
        if minimum is not None and result[metric] < minimum:
            errors.append(f"{case_id}: {metric} {result[metric]} is below {minimum}")

    output = result["final_output"]
    for label in ("VERDICT:", "USAGE:"):
        if label not in output:
            errors.append(f"{case_id}: final output missing {label}")
    if case["expected_skill"].startswith("jrs:quick-") and "PRINCIPAL REVIEW:" not in output:
        errors.append(f"{case_id}: quick-skill output missing PRINCIPAL REVIEW:")

if errors:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"Runtime evaluation passed: {len(cases)} captured cases.")
