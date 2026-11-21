#!/usr/bin/env python3
"""Verify the adaptive-usage contract without running paid model calls."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPARTMENTS = sorted(
    path for path in (ROOT / "skills").iterdir() if path.is_dir() and path.name != "route"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"ERROR: {message}", file=sys.stderr)
        raise SystemExit(1)


require(len(DEPARTMENTS) == 26, f"expected 26 departments, found {len(DEPARTMENTS)}")

for department in DEPARTMENTS:
    text = (department / "SKILL.md").read_text()
    name = department.name

    for mode in ("Lean", "Balanced", "Assurance"):
        require(text.count(f"- **{mode}**") == 1, f"{name}: {mode} mode is not defined once")

    require("Target: at most one" in text, f"{name}: Lean budget missing")
    require("Target: at most two" in text, f"{name}: Balanced budget missing")
    require("Target: five tier-agent" in text, f"{name}: Assurance budget missing")
    require("trigger 4 or 6 fires" in text, f"{name}: mandatory Assurance upgrade missing")
    require("usage budgets, not safety caps" in text, f"{name}: safety budget exception missing")
    require("Principal trigger always runs" in text, f"{name}: Principal budget exception missing")
    require("USAGE: <Lean | Balanced | Assurance>" in text, f"{name}: USAGE report line missing")
    require("Never omit `VERDICT:`" in text, f"{name}: required report labels may be omitted")
    require("Advisor stays in the session" in text, f"{name}: session-model policy missing")
    require("Lean and Balanced never require a switch to Opus" in text, f"{name}: low-usage model rule missing")
    require("USAGE BUDGET:` and `USAGE SO FAR:" in text, f"{name}: router usage intake missing")

    escalation = text[text.index("Escalate to the Principal only when:") :]
    require("5. Assurance release review" in escalation, f"{name}: mode-specific trigger 5 missing")
    require("Trigger 6 is this skill's risk trigger" in escalation, f"{name}: risk trigger missing")

route = (ROOT / "skills" / "route" / "SKILL.md").read_text()
for required in (
    "## Step 0.5 - Usage mode and budget",
    "A Balanced chain targets at most six tier-agent dispatches total",
    "intermediate department in a Balanced chain",
    "RUN MODE: <Lean | Balanced | Assurance>",
    "USAGE BUDGET:",
    "USAGE SO FAR:",
    "total tier-agent dispatches; total Principal calls",
):
    require(required in route, f"router: missing {required}")

for path in sorted((ROOT / "agents").glob("*.md")):
    if path.stem in {"principal", "principal-opus"}:
        continue
    text = path.read_text()
    require("STAGES: one stage in Assurance" in text, f"{path.stem}: stage bundle packet missing")
    require("Do not start a stage outside the bundle" in text, f"{path.stem}: bundle boundary missing")

require(
    "When Lean assigns Stage 4" in (ROOT / "agents" / "builder-medium.md").read_text(),
    "builder-medium: Lean independent-review role missing",
)
require(
    "Balanced Stages 1-3 bundle" in (ROOT / "agents" / "builder-high.md").read_text(),
    "builder-high: Balanced bundled-worker role missing",
)

print("Adaptive usage contract passed: 26 departments, 3 modes, 6 bundle-capable tier agents.")
