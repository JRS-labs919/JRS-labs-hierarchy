#!/usr/bin/env python3
"""Keep always-loaded skill bodies within explicit word budgets."""

from __future__ import annotations

import statistics
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def words(path: Path) -> int:
    return len(path.read_text().split())


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


departments = sorted(path for path in SKILLS.iterdir() if (path / "house-standards.md").exists())
counts = {path.name: words(path / "SKILL.md") for path in departments}

if len(departments) != 26:
    fail(f"expected 26 departments, found {len(departments)}")
if max(counts.values()) > 3200:
    worst = max(counts, key=counts.get)
    fail(f"{worst} exceeds the 3,200-word department ceiling: {counts[worst]}")
if statistics.mean(counts.values()) > 2900:
    fail(f"department average exceeds 2,900 words: {statistics.mean(counts.values()):.0f}")

for path in departments:
    if not (path / "references" / "record-template.md").exists():
        fail(f"{path.name}: deferred Standard record template missing")

route_words = words(SKILLS / "route" / "SKILL.md")
if route_words > 3000:
    fail(f"router exceeds 3,000 words: {route_words}")

for name in ("onboard", "quick-draft", "quick-review", "quick-analysis"):
    count = words(SKILLS / name / "SKILL.md")
    if count > 1400:
        fail(f"{name} exceeds 1,400 words: {count}")

print(
    "Prompt budgets passed: "
    f"departments avg {statistics.mean(counts.values()):.0f}, "
    f"median {statistics.median(counts.values()):.0f}, max {max(counts.values())}; "
    f"router {route_words}."
)

