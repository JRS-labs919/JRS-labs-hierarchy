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

departments = sorted(path for path in SKILLS.iterdir() if path.is_dir() and path.name != "route")
require(len(departments) == 26, f"expected 26 departments, found {len(departments)}")
agent_names = {path.stem for path in AGENTS.glob("*.md")}
require(len(agent_names) == 8, f"expected 8 agents, found {len(agent_names)}")

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
        "**Router and department handoff.**",
        "**Running inside a subagent.**",
        "**Drafts, not approvals.**",
        "Trigger 6 is this skill's risk trigger",
        "PRINCIPAL REVIEW:",
        "[- RAN FLAT when applicable]",
    ):
        require(required in text, f"{label}: missing {required}")

    for forbidden in ("sign-off: approved", "signs off itself", "session is on Fable 5.2", "<slug>"):
        require(forbidden not in text, f"{label}: obsolete text remains: {forbidden}")

    escalation = re.search(
        r"Escalate to the Principal only when:\n(.*?)\n\*\*Small size",
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

all_skill_names = {f"jrs:{path.name}" for path in SKILLS.iterdir() if path.is_dir()}
referenced_names: set[str] = set()
for path in list(SKILLS.glob("*/SKILL.md")) + [ROOT / "tests" / "routing-prompts.md"]:
    require(path.exists(), f"missing {path.relative_to(ROOT)}")
    referenced_names.update(re.findall(r"jrs:[a-z0-9-]+", path.read_text()))
missing = referenced_names - all_skill_names
require(not missing, f"references missing skills: {sorted(missing)}")

for principal in ("principal.md", "principal-opus.md"):
    text = (AGENTS / principal).read_text()
    require("consistent with conditions" in text, f"{principal}: review vocabulary missing")
    require("It is not an approval" in text, f"{principal}: human-approval boundary missing")

print(f"Release consistency checks passed for JRS {version}: 26 departments, 8 agents.")
