#!/usr/bin/env python3
"""Check release invariants that Claude's plugin validator does not cover."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
version = manifest["version"]
changelog = (ROOT / "CHANGELOG.md").read_text()
match = re.search(r"^## ([0-9]+\.[0-9]+\.[0-9]+) - ", changelog, re.MULTILINE)
require(match is not None, "CHANGELOG.md has no release heading")
require(match.group(1) == version, f"plugin version {version} != changelog {match.group(1)}")

departments = sorted(path for path in SKILLS.iterdir() if (path / "house-standards.md").exists())
require(len(departments) == 26, f"expected 26 departments, found {len(departments)}")
agent_names = {path.stem for path in AGENTS.glob("*.md")}
require(len(agent_names) == 9, f"expected 9 agents, found {len(agent_names)}")

tier_agent = {
    ("Opus 5.5", "High"): "senior-high",
    ("Opus 5.5", "Medium"): "senior-medium",
    ("Sonnet 5.5", "High"): "builder-high",
    ("Sonnet 5.5", "Medium"): "builder-medium",
    ("Sonnet 5.5", "Low"): "builder-low",
    ("Haiku 5.5", "Low"): "clerk",
}

for department in departments:
    path = department / "SKILL.md"
    text = path.read_text()
    label = department.name

    for required in (
        "<!-- JRS:SHARED-RUNTIME:START -->",
        "<!-- JRS:SHARED-RUNTIME:END -->",
        "<!-- JRS:PRINCIPAL:START -->",
        "<!-- JRS:PRINCIPAL:END -->",
        "**Flat runtime.**",
        "**Drafts, not approvals.**",
        "PRINCIPAL REVIEW:",
        "[- RAN FLAT when applicable]",
        "## Adaptive runtime",
        "**Lean**",
        "**Balanced**",
        "**Assurance**",
        "Budget: 0–1 tier-agent",
        "Budget: at most two tier-agent",
        "Budget: five tier-agent",
        "Honor an incoming `RUN MODE:` only when eligible",
        "`USAGE BUDGET:` and `USAGE SO FAR:`",
        "USAGE: <Lean | Balanced | Assurance>",
        "n rulings; Stage 4 release check:",
        "Never omit `VERDICT:`, `MODELS:`, `USAGE:` or `PRINCIPAL REVIEW:`",
        "Lean and Balanced use Stage 4 as their release",
        "references/escalation-protocol.md",
        "literal fenced report block",
        "department date-and-topic path below is for Standard records only",
        "## Standard record",
        "references/record-template.md",
    ):
        require(required in text, f"{label}: missing {required}")

    require((department / "references" / "record-template.md").exists(), f"{label}: record reference missing")

    for forbidden in (
        "sign-off: approved",
        "signs off itself",
        "session is on Fable 5.2",
        "<slug>",
        "### Fable fallback",
        "every Standard-size job",
        "Do not combine stages in one dispatch",
        "MODELS: <Fable | Fallback",
    ):
        require(forbidden not in text, f"{label}: obsolete text remains: {forbidden}")

    escalation = re.search(
        r"<!-- JRS:PRINCIPAL:START -->.*?Escalate only when:\n(.*?)\n\nTriggers 1",
        text,
        re.DOTALL,
    )
    require(escalation is not None, f"{label}: escalation block not found")
    triggers = re.findall(r"^([1-6])\. ", escalation.group(1), re.MULTILINE)
    require(triggers == ["1", "2", "3", "4", "5", "6"], f"{label}: triggers are {triggers}")

    rows: list[list[str]] = []
    for line in text.splitlines()[:70]:
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 6 and cells[0] in {"1", "2", "3", "4", "5"}:
            rows.append(cells)
    require([row[0] for row in rows] == ["1", "2", "3", "4", "5"], f"{label}: invalid stage table")

    expected_agents = {tier_agent.get((row[3], row[4])) for row in rows}
    require(None not in expected_agents, f"{label}: stage has an unmapped model/effort")
    uses = re.search(r"This skill uses ([^.]+)\.", text)
    require(uses is not None, f"{label}: missing agent summary")
    claimed_agents = set(re.findall(r"`([a-z-]+)`", uses.group(1)))
    require(claimed_agents == expected_agents, f"{label}: claimed agents differ from stage table")
    require(claimed_agents <= agent_names, f"{label}: references a missing agent")

route_text = (SKILLS / "route" / "SKILL.md").read_text()
for required in (
    "do not choose from an assumption: ask one short either/or question",
    "that order wins and becomes a custom chain",
    "final priced quote, only when supply chain ran",
    "flag applicability and legal",
    "## Step 0.5 - Usage mode and budget",
    "A Balanced chain targets at most six tier-agent dispatches total",
    "RUN MODE: <Lean | Balanced | Assurance>",
    "USAGE BUDGET:",
    "USAGE SO FAR:",
    "USAGE: <mode by department; total tier-agent dispatches",
    "## Step 2.5 - Lean fast path",
    "jrs:quick-draft",
    "jrs:quick-review",
    "jrs:quick-analysis",
    "jrs/company-profile.md",
    "references/economy-coordinator.md",
):
    require(required in route_text, f"router: missing {required}")

for support in ("onboard", "quick-draft", "quick-review", "quick-analysis"):
    path = SKILLS / support / "SKILL.md"
    require(path.exists(), f"support skill missing: {support}")
    support_text = path.read_text()
    require("USAGE:" in support_text, f"{support}: usage report missing")

for quick in ("quick-draft", "quick-review", "quick-analysis"):
    quick_text = (SKILLS / quick / "SKILL.md").read_text()
    require("0-1 tier-agent dispatches" in quick_text, f"{quick}: Lean budget missing")
    require("PRINCIPAL REVIEW:" in quick_text, f"{quick}: approval boundary missing")

quality_text = (SKILLS / "quality" / "SKILL.md").read_text()
require(
    "The user requests, or the recommended disposition is, use-as-is" in quality_text,
    "quality: use-as-is request does not explicitly fire trigger 6",
)

all_skill_names = {f"jrs:{path.parent.name}" for path in SKILLS.glob("*/SKILL.md")}
referenced_names: set[str] = set()
for path in list(SKILLS.glob("*/SKILL.md")) + [ROOT / "tests" / "routing-prompts.md"]:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    referenced_names.update(re.findall(r"jrs:[a-z0-9-]+", path.read_text()))
missing = referenced_names - all_skill_names
missing.discard("jrs:department")
require(not missing, f"references missing skills: {sorted(missing)}")

for principal in ("principal.md", "principal-opus.md"):
    text = (AGENTS / principal).read_text()
    require("consistent with conditions" in text, f"{principal}: review vocabulary missing")
    require("It is not an approval" in text, f"{principal}: human-approval boundary missing")

for tier in sorted(agent_names - {"principal", "principal-opus", "chain-coordinator"}):
    text = (AGENTS / f"{tier}.md").read_text()
    require("STAGES: one stage in Assurance" in text, f"{tier}: stage-bundle packet missing")
    require("consecutive stage bundle" in text, f"{tier}: bundled execution missing")
    require("Be concise:" in text, f"{tier}: concise handoff rule missing")

coordinator = (AGENTS / "chain-coordinator.md").read_text()
require("PROBE ONLY" in coordinator, "chain-coordinator: capability probe missing")
require("never used for Assurance" in coordinator, "chain-coordinator: Assurance exclusion missing")
require("Return control immediately" in coordinator, "chain-coordinator: handback contract missing")

require((ROOT / "tests" / "usage-mode-prompts.md").exists(), "usage-mode prompt tests missing")
require((ROOT / "scripts" / "check_usage_modes.py").exists(), "usage-mode contract checker missing")
require((ROOT / "scripts" / "check_prompt_budgets.py").exists(), "prompt-budget checker missing")
require((ROOT / "scripts" / "evaluate_results.py").exists(), "runtime evaluation helper missing")
require((SKILLS / "_shared" / "references" / "assurance-runtime.md").exists(), "Assurance reference missing")
require((SKILLS / "_shared" / "references" / "escalation-protocol.md").exists(), "escalation reference missing")
packages = list((ROOT / "packages" / "standalone").glob("jrs-*.skill"))
require(len(packages) == 31, f"expected 31 standalone packages, found {len(packages)}")

print(f"Release consistency checks passed for JRS {version}: 26 departments, 4 support skills, 9 agents.")
