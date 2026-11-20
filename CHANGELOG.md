# Changelog

All notable changes to JRS will be documented here.

## 1.1.1 - 2026-11-20

Runtime-verification follow-up for routing, review discipline and installation guidance.

- Router: ambiguous procedure-audience and BOM-structure requests now require one short clarification instead of an assumed route.
- Router: a user's explicit department or deliverable order now wins over a named flow unless the user confirms a reversal.
- Router: Quote to order now declares its final Applications Engineering pricing pass after Supply Chain instead of improvising a repeat.
- Router: directive and regulatory conformity routes explicitly flag legal applicability and interpretation for the user's Legal owner.
- Quality: a request for use-as-is or a concession fires trigger 6 even when the safe recommendation is to hold.
- All departments: final reports require the literal fenced report block and distinguish Small-job Advisor release review from Principal rulings.
- All departments: stages cannot be combined when tier agents are available; dependent work waits for a Principal ruling; material post-review edits require re-review.
- Documentation: added separate update instructions for account-synced Claude installs and Claude Code marketplace installs.
- Clarified that the department record-path convention applies to Standard records; Small deliverables stay in the conversation unless a file or project edit was requested.

## 1.1.0 - 2026-11-19

Fixes from the design consult and the supplied runtime-verification findings.

- Router: chains now run one department at a time in the main session, not in subagents, so each department keeps its tier agents and its Principal.
- Router: defined the `HANDOFF:` block; every department now reads it at Stage 1, carries inherited open items and stops as `blocked` on a missing input it cannot work without.
- Router: a chain stops before dispatching a department that needs a `REQUIRED INPUT`; a department no longer branches to a sibling that is a later step of the chain.
- Router: added a tie-break table and four flows (nonconformance to corrective action, engineering change, security incident, release to market). The routing tables no longer repeat each skill's "starts from" text.
- All departments: the risk trigger (trigger 6) now applies at every size. The five departments that had no risk trigger gained one.
- All departments: new ground rule "Drafts, not approvals". The report line is now `PRINCIPAL REVIEW:` with consistent / consistent with conditions / not consistent. An Advisor ruling made because the Principal was unavailable is reported as `NOT REVIEWED`, and on a risk question the verdict is `blocked`.
- All departments: an unfilled safety, legal, regulatory or approval-limit line in `house-standards.md` is a blocking open item, no longer ignored.
- All departments: a department that finds itself in a subagent reports `RAN FLAT` and returns risk questions to its caller.
- All departments: the model check accepts any Fable version, and a `MODELS:` line is used only when it agrees with the model actually running.
- All departments: record files are named `<yyyy-mm-dd>-<topic>.md`.
- Hardware engineering: hazard and failure-mode step, standards check on every track, physical tests reported as `NOT RUN - test plan provided`.
- EHS and field service: permits, competence, rescue and stop-work conditions required when controls are written; isolation and arc-flash inputs block electrical work; standing hazard analyses must be referenced and in date.
- Quality: nonconformance path with containment, root cause and corrective actions before Stage 5; Stage 4 renamed, and it recommends a disposition only.
- Agents: Principals review, they do not approve; tier agents state that they cannot dispatch other agents.
- Added `tests/routing-prompts.md` and a CI consistency check for the release contract.
- Not in this release: the standalone `.skill` packages are still at 1.0.3.

## 1.0.3 - 2026-11-18

- Added account-level installation steps for Claude, Claude Desktop, and Cowork.
- Clarified that the JRS plugin already installs all 27 skills and eight agents.
- Added a warning that pasting the repository URL into a Code session clones the source but does not install the plugin.

## 1.0.2 - 2026-11-18

- Refreshed the public description around JRS as your pocket-sized company inside Claude, with you as CEO.

## 1.0.1 - 2026-11-18

- Renamed the repository to `JRS-labs-hierarchy`.
- Updated the marketplace, repository links, and authorship to the `JRS-labs919` account.

## 1.0.0 - 2026-11-18

- Initial GitHub release.
- Added the router, 26 department skills, eight tier agents, and department house-standard templates.
- Added standalone `.skill` packages for Claude.ai.
- Added a self-hosted Claude Code marketplace and automated validation.
