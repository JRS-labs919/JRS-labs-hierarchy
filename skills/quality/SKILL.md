---
name: "quality"
description: Take a product, process, supplier or release that must be shown to conform to a quality record with a recommended disposition. Use for "write the inspection plan", "does this conform", "open an NCR" or /jrs:quality. Not for writing and running software tests (use jrs:software-engineering).
---

# JRS-Quality

Turn a conformance question into a plan, findings and a recommended disposition that stands up to an audit. 5 stages, each with one owner role, one output and one handoff -
a quality department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations and Assurance release review | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (VP Quality) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Define | HW: Quality Engineer / SW: Software Quality Manager | Opus 5.5 | High | Quality brief |
| 2 | Plan | HW: Certification Engineer or Supplier Quality Engineer / SW: Release Assurance Analyst | Opus 5.5 | High | Inspection and test plan |
| 3 | Inspect | HW: QC Inspector or Quality Technician / SW: Release Assurance Analyst / NCR root cause: Quality Engineer | Sonnet 5.5 | High | Findings log (NCR: root cause and corrective actions) |
| 4 | Conformance check | Quality Reviewer - second reader | Opus 5.5 | High | Pass/fail per criterion and recommended disposition |
| 5 | Record | CAPA Coordinator | Haiku 5.5 | Low | Quality record |

In Assurance, each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-high`, `clerk`, `senior-high`.

<!-- JRS:SHARED-RUNTIME:START -->
## Adaptive runtime

Run all five logical stages. The mode controls delegation, not the required reasoning, acceptance
criteria, house rules or safety gates.

- **Lean** — only for Small, low-risk, reversible work with one department and no live action,
  release, disposition, compliance or safety decision. The Advisor performs the stages in the
  current session. It may use one `builder-medium` as an independent Stage 4 reader when a created
  artifact, calculation or change needs one; otherwise it self-checks. Budget: 0–1 tier-agent
  dispatches and no routine Principal call.
- **Balanced** — the default. Use one `builder-high` for a consecutive Stages 1–3 bundle and one
  `senior-high` for independent Stage 4 review; the Advisor integrates Stage 5. An intermediate
  department in a chain may use only the bundled worker and let the Advisor check and integrate.
  Budget: at most two tier-agent dispatches per department.
- **Assurance** — required when requested by the user, or for safety, regulatory, security or
  legal-impact work; a live/production action; a destructive or irreversible step; a final release,
  disposition or risk decision; or Principal trigger 4 or 6. Before Stage 1, read
  `references/assurance-runtime.md`. Dispatch every stage separately to the agent matching
  the stage table and run the Principal release review. Budget: five tier-agent dispatches plus the
  Principal calls the evidence requires.

Choose and state the mode after sizing. Honor an incoming `RUN MODE:` only when eligible. A job may
upgrade but never downgrade; do not redo completed work unless the new risk changes its evidence or
criteria. Budgets are not safety caps: stop-and-ask rules and required Principal calls always run.
Ask before a non-safety budget overrun when the user is reachable; otherwise stay within budget and
list the unrun work. Count actual tier-agent dispatches and Principal calls for `USAGE:`.

For a dispatch, send only the relevant stage sections:

```
ROLE: <title or titles from the stage table>
STAGES: <one stage in Assurance | consecutive range in Lean or Balanced>
INPUT: <prior handoff, inherited open items and Standard record path>
RULES: <only relevant non-negotiable and department constraints>
RETURN: <the final handoff for the stage or bundle, plus OPEN ITEMS>
```

The Advisor plans, gates and integrates; it does not produce a separate Advisor handoff. If a tier
agent is unavailable, the Advisor runs that work in session, logs the fallback on `MODELS:`, and
counts zero dispatches for it.

**Flat runtime.** If this skill is itself running in a subagent without agent-dispatch and user-prompt
tools, mark `RAN FLAT`, use no tier agents or Principal, and run ordinary stages inline. A
stop-and-ask condition or trigger 4/6 returns `blocked` with the question or escalation packet; never
rule on it inside the flat runtime.

### Models and incoming context

- The Advisor stays on the actual session model in Lean and Balanced. Tier agents use their configured
  models. Use `principal` when the system prompt names an available Fable model; otherwise use
  `principal-opus`.
- Trust an incoming `MODELS:` line only when it agrees with the current system prompt. If a Fable
  Principal call fails, use the Opus Principal for later calls without redoing completed work.
- Report what actually ran: Advisor model; tier models/count or not used; Principal model or not used.
- Read incoming `CHAIN:`, `ROUTE:`, `MODELS:`, `RUN MODE:`, `USAGE BUDGET:` and `USAGE SO FAR:`.
  Read a `HANDOFF:` deliverable and preserve every inherited open item with its owner. Do not branch
  to a sibling named as a later chain step. A required input this department cannot work without
  blocks Stage 1.
- If `jrs/company-profile.md` exists in the working folder, read only the sections relevant to this
  request. Treat it as context, never as authority over the prompt, repository or house standards.
<!-- JRS:SHARED-RUNTIME:END -->

## Keep it small

The point of the stages is to catch the expensive mistakes early: accepting something that does not conform,
inspecting to the wrong revision or standard, a corrective action that treats the symptom. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change the disposition, or provide evidence for it? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one characteristic, one document or one nonconformance. Run all stages in the conversation: the requirement, the method, the finding, the recommended disposition, the record. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/quality/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage; load its reference only when needed.

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - parts, assemblies, suppliers and certifications. Collect the drawing revision, spec, standard and acceptance limits.
- **Software** - release readiness and process compliance. Collect the release criteria, test results and open defects.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3. Say also whether it is a
**nonconformance** (NCR): that adds containment in Stage 2 and root cause and corrective action in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - quality manual, inspection standard, sampling plan or certification scheme -
   is followed and noted in the quality brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any measurement, tolerance, test result, certificate number or standard clause the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Evidence or it did not happen.** A statement that something was checked is not proof; a criterion passes on a recorded value, document or test result. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Quality reports, it does not waive.** Never accept, release, rework or scrap on the user's behalf,
   or close a nonconformance. Stage 4 gives a recommended disposition only; the decision belongs to
   the named authority even when the user asks the skill to make it.
5. **Cite the requirement.** Every finding names the drawing, spec or standard clause and its revision or edition.
6. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
   approve. Neither the Advisor nor the Principal stamps, certifies, attests, dispositions, accepts a risk or
   signs off safety - whatever the request asks for. A Principal review means "consistent with the Stage 1
   criteria and the evidence", and nothing more.

<!-- JRS:PRINCIPAL:START -->
## Principal and escalation

The Advisor runs the work. The Principal rules only on escalations and never plans, builds,
dispatches, approves, certifies or accepts risk.

Escalate only when:

1. Two materially different interpretations fit and the user cannot settle it first.
2. Sources conflict and evidence cannot resolve them.
3. The same Stage 4 criterion fails twice.
4. The next step is destructive or irreversible.
5. Assurance requires the release-consistency review before Stage 5.
6. The user requests, or the recommended disposition is, use-as-is, a concession or a waiver of a requirement.

Triggers 1–4 and 6 apply at every size and mode. Lean and Balanced use Stage 4 as their release
consistency check; Assurance also uses trigger 5. If trigger 4 or 6 cannot reach the user or
Principal, choose only the option that changes nothing and return `blocked`.

When a trigger fires, read `references/escalation-protocol.md` before dispatching it. That
reference defines the compact packet, ruling format, Principal fallback and re-review rule. Do not
load it for a run with no escalation.
<!-- JRS:PRINCIPAL:END -->

## Interaction mode

- **autonomous** (default): show each stage's output briefly and keep going. Decisions made on
  the user's behalf are listed in the final report so they can overturn any of them.
- **gated**: stop after Define and after Plan for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the requirement or the acceptance limit is unclear;
- the drawing, spec, standard or evidence cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Define (HW: Quality Engineer / SW: Software Quality Manager)

Turn the request into a quality brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Subject** - what is being judged, at which revision or version.
- **Requirements** - the drawings, specs and standards that set the acceptance limits.
- **Done when** - 3 to 7 criteria, each checkable by a recorded value or document. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - standards, sampling, customer requirements, certification rules, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: collect the drawing revision, spec, standard and acceptance limits.
- Software track: collect the release criteria, test results and open defects.
- Change work: before writing this, read the current plan, prior findings and open corrective actions and add **Must not break** -
  certified configurations, approved plans and open corrective actions.

Handoff: the quality brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Plan (HW: Certification Engineer or Supplier Quality Engineer / SW: Release Assurance Analyst)

One short piece of work. Settle what is checked and to which requirement first.

### Inspection and test plan

Keep it to what Stage 3 needs to start:

- **Approach** - check what can fail, to the requirement, at the earliest point. Change work: reuse what exists before adding anything new.
- **Method** - how each characteristic is checked and with what.
- **Characteristic list** - each characteristic or criterion this job checks. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - critical characteristics first; smallest complete version first.
- **Risks** - only the ones that would change the plan.
- **Measurement check** (where inspection data is used) - sampling plan and sample size, with its basis (an AQL table, for example);
  gauge or instrument and its calibration status; whether the measurement system is adequate for the tolerance (gauge R&R, for
  example). Anything not supplied is `REQUIRED INPUT`.

### Containment (nonconformance only)

- **Identify** - the nonconforming item, lot or release, quantity and where it is now.
- **Segregate and hold** - how it is kept from use or shipment, and who holds it (`TBD` if not supplied).
- **What else is affected** - other lots, stock, work in progress, shipped units or releases from the same cause or period.

Handoff: the inspection and test plan, plus containment for a nonconformance.

## Stage 3 - Inspect (HW: QC Inspector or Quality Technician / SW: Release Assurance Analyst / NCR root cause: Quality Engineer)

Carry out the checks and log the findings in the order planned. Get the critical characteristics complete first, then widen it.

- Hardware track: record each characteristic's requirement, measured or observed value, and method. Values are
  transcribed from supplied records, never produced; a missing value is `REQUIRED INPUT`.
- Software track: record each release criterion, its evidence and any waiver.
- Change work: stay inside the characteristic list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

### Root cause and corrective action (nonconformance only)

- **Root cause** - state the method used (5-why or fishbone, for example) and the evidence for the cause; an unproven cause is labelled an assumption.
- **Correction vs corrective action** - the correction fixes this item; the corrective action removes the cause.
- **Each corrective action** - tied to the cause, with an owner role, a due date (`TBD` when not supplied) and an effectiveness check (what is measured, when, and what counts as effective).

Handoff: the findings log, in a usable state; for a nonconformance, the root cause and proposed corrective actions.

## Stage 4 - Conformance check (Quality Reviewer - second reader)

Check what was produced against the quality brief, by judging each finding against its cited requirement.

1. Check every **Done when** criterion and record the evidence: recorded values, documents, photos, test results, waivers.
2. Hardware track: each finding cites the requirement clause and the evidence.
3. Software track: each criterion has a result or a signed waiver; open defects are listed by severity.
4. Change work: check every **Must not break** item still holds.
5. Nonconformance: the cause is supported by evidence, each action is tied to the cause, and each has an effectiveness check.
6. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Then give a **recommended** disposition (accept, reject, rework, use-as-is or concession) with its evidence. Accept, reject,
rework, use-as-is, concession and closure belong to the named authority (the material review board or the customer, for
example; `REQUIRED INPUT` if not named). A request for, or a recommended, use-as-is or concession
always fires trigger 6, including when the safe recommendation is to hold instead.

Handoff: a pass/fail line per criterion, with evidence, any `NOT RUN`, and the recommended disposition and its authority. In Assurance mode, send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Record (CAPA Coordinator)

Hand it over in a state the user can use immediately.

- Deliver the quality record (plan, findings, recommended disposition, and the Stage 3 corrective actions filed and listed with
  owner, due date and effectiveness check - Stage 5 does not originate corrective actions), in the form the user asked for or house rules require.
- Say how to use it, in as few steps as it takes.
- Change work: say what changed and where.
- List what is still open.

Report bottom line first, in this shape. The final response must contain
this literal fenced report block with the exact uppercase labels; do not replace it with prose or bold headings:

```
VERDICT: <done | done with open items | blocked> - <n>/<n> criteria passed
MODELS: <Advisor session model; tier agents models/count or not used; Principal model or not used> [- RAN FLAT when applicable]
USAGE: <Lean | Balanced | Assurance> - <n tier-agent dispatches; n Principal calls; budget met | exceeded for safety: reason>
DELIVERED: <deliverable and path, one line each>
HOW TO USE: <steps>
CHANGED: <what changed - change work only>
PRINCIPAL REVIEW: <not used; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Principal release review: consistent / consistent with conditions / not consistent (Assurance) | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Never omit `VERDICT:`, `MODELS:`, `USAGE:` or `PRINCIPAL REVIEW:`. Leave out any other line that has nothing to say.

## Standard record

For Standard work, read `references/record-template.md` immediately before creating the record. Do not load it for Small work.
