#!/usr/bin/env python3
"""Synchronize compact shared department sections and extract deferred references."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
RUNTIME = (ROOT / "templates" / "department-runtime.md").read_text().rstrip()
PRINCIPAL = (ROOT / "templates" / "principal-escalation.md").read_text().rstrip()
SHARED_REFERENCES = SKILLS / "_shared" / "references"

RUNTIME_START = "<!-- JRS:SHARED-RUNTIME:START -->"
RUNTIME_END = "<!-- JRS:SHARED-RUNTIME:END -->"
PRINCIPAL_START = "<!-- JRS:PRINCIPAL:START -->"
PRINCIPAL_END = "<!-- JRS:PRINCIPAL:END -->"


def departments() -> list[Path]:
    return sorted(path for path in SKILLS.iterdir() if (path / "house-standards.md").exists())


def extract_risk(text: str, label: str) -> str:
    if PRINCIPAL_START in text and PRINCIPAL_END in text:
        text = text.split(PRINCIPAL_START, 1)[1].split(PRINCIPAL_END, 1)[0]
    elif "## Principal and escalation" in text and "## Interaction mode" in text:
        text = text.split("## Principal and escalation", 1)[1].split("## Interaction mode", 1)[0]
    compact = re.search(
        r"(?:^|\n)6\. (.*?)(?=\n\n\*\*Release review by mode|\n\nTriggers 1)",
        text,
        re.DOTALL,
    )
    if not compact:
        raise ValueError(f"{label}: Principal trigger 6 was not found")
    return " ".join(compact.group(1).split())


def replace_section(text: str, start_heading: str, end_heading: str, replacement: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(start_heading)}\n.*?(?=^{re.escape(end_heading)}\n)",
        re.MULTILINE | re.DOTALL,
    )
    if not pattern.search(text):
        raise ValueError(f"section {start_heading!r} through {end_heading!r} not found")
    return pattern.sub(replacement.rstrip() + "\n\n", text, count=1)


def desired(path: Path, write_references: bool, source_text: str | None = None) -> str:
    skill_path = path / "SKILL.md"
    text = source_text if source_text is not None else skill_path.read_text()
    risk = extract_risk(text, path.name)

    runtime_block = f"{RUNTIME_START}\n{RUNTIME}\n{RUNTIME_END}"
    if RUNTIME_START in text:
        text = re.sub(
            rf"^{re.escape(RUNTIME_START)}\n.*?^{re.escape(RUNTIME_END)}$",
            runtime_block,
            text,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
    else:
        text = replace_section(text, "## Adaptive usage", "## Keep it small", runtime_block)

    principal = PRINCIPAL.replace("{{RISK_TRIGGER}}", risk)
    principal_block = f"{PRINCIPAL_START}\n{principal}\n{PRINCIPAL_END}"
    if PRINCIPAL_START in text:
        text = re.sub(
            rf"^{re.escape(PRINCIPAL_START)}\n.*?^{re.escape(PRINCIPAL_END)}$",
            principal_block,
            text,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
    else:
        text = replace_section(text, "## Principal and escalation", "## Interaction mode", principal_block)

    record_heading = "## Record template (Standard size only)"
    pointer = (
        "## Standard record\n\n"
        "For Standard work, read `references/record-template.md` immediately before creating the "
        "record. Do not load it for Small work."
    )
    if record_heading in text:
        before, record = text.split(record_heading, 1)
        reference = path / "references" / "record-template.md"
        if write_references:
            reference.parent.mkdir(parents=True, exist_ok=True)
            reference.write_text(f"# {path.name} Standard record template\n\n{record.strip()}\n")
        text = before.rstrip() + "\n\n" + pointer + "\n"
    elif "## Standard record" not in text:
        raise ValueError(f"{path.name}: Standard record pointer not found")

    text = text.replace(
        "section per stage (template at the end).",
        "section per stage; load its reference only when needed.",
    )
    text = text.replace(
        "rules on escalations, final release review (Standard size)",
        "rules on escalations and Assurance release review",
    )

    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="update skills and extract references")
    args = parser.parse_args()

    changed: list[str] = []
    for department in departments():
        skill = department / "SKILL.md"
        target = desired(department, args.write)
        if skill.read_text() != target:
            changed.append(department.name)
            if args.write:
                skill.write_text(target)

        for name in ("assurance-runtime.md", "escalation-protocol.md"):
            source_reference = SHARED_REFERENCES / name
            local_reference = department / "references" / name
            if not local_reference.exists() or local_reference.read_text() != source_reference.read_text():
                changed.append(f"{department.name}/{name}")
                if args.write:
                    local_reference.parent.mkdir(parents=True, exist_ok=True)
                    local_reference.write_text(source_reference.read_text())

    department_map = SHARED_REFERENCES / "department-map.md"
    for quick in ("quick-draft", "quick-review", "quick-analysis"):
        local_reference = SKILLS / quick / "references" / "department-map.md"
        if not local_reference.exists() or local_reference.read_text() != department_map.read_text():
            changed.append(f"{quick}/department-map.md")
            if args.write:
                local_reference.parent.mkdir(parents=True, exist_ok=True)
                local_reference.write_text(department_map.read_text())

    if changed and not args.write:
        print("ERROR: shared department contract is out of sync: " + ", ".join(changed), file=sys.stderr)
        return 1

    verb = "updated" if args.write else "verified"
    print(f"Shared department contract {verb}: {len(departments())} departments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
