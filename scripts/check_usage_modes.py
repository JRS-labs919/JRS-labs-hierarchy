#!/usr/bin/env python3
"""Verify the adaptive-usage contract without running paid model calls."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPARTMENTS = sorted(
    path for path in (ROOT / "skills").iterdir() if (path / "house-standards.md").exists()
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

    require("Budget: 0–1 tier-agent" in text, f"{name}: Lean budget missing")
    require("Budget: at most two tier-agent" in text, f"{name}: Balanced budget missing")
    require("Budget: five tier-agent" in text, f"{name}: Assurance budget missing")
    require("Principal trigger 4 or 6" in text, f"{name}: mandatory Assurance upgrade missing")
    require("Budgets are not safety caps" in text, f"{name}: safety budget exception missing")
    require("required Principal calls always run" in text, f"{name}: Principal budget exception missing")
    require("USAGE: <Lean | Balanced | Assurance>" in text, f"{name}: USAGE report line missing")
    require("Never omit `VERDICT:`" in text, f"{name}: required report labels may be omitted")
    require("Advisor stays on the actual session model" in text, f"{name}: session-model policy missing")
    require("`USAGE BUDGET:` and `USAGE SO FAR:`" in text, f"{name}: router usage intake missing")

    escalation = text[text.index("Escalate only when:") : text.index("<!-- JRS:PRINCIPAL:END -->")]
    require("5. Assurance requires the release-consistency review" in escalation, f"{name}: mode-specific trigger 5 missing")
    require("\n6. " in escalation, f"{name}: risk trigger missing")

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
    if path.stem in {"principal", "principal-opus", "chain-coordinator"}:
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

for quick in ("quick-draft", "quick-review", "quick-analysis"):
    text = (ROOT / "skills" / quick / "SKILL.md").read_text()
    require("USAGE: Lean fast path" in text, f"{quick}: fast-path usage line missing")
    require("0-1 tier-agent dispatches" in text, f"{quick}: fast-path dispatch budget missing")

print("Adaptive usage contract passed: 26 departments, 3 fast paths, 3 modes, 6 bundle-capable tier agents.")
