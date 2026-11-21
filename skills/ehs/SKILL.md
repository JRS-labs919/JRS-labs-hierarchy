---
name: "ehs"
description: Take a task, site, incident or regulatory question to a hazard assessment with controls, or an incident report with corrective actions. Use for "write the JHA for", "is this safe to do", "investigate this incident" or /jrs:ehs. Not for the step-by-step work procedure (use jrs:field-service).
---

# JRS-EHS

Turn a task or an incident into identified hazards, controls that match them and a record that would satisfy an inspector. 5 stages, each with one owner role, one output and one handoff -
an EHS department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations and Assurance release review | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (EHS Manager) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Scope | Safety Coordinator | Opus 5.5 | Medium | Assessment brief |
| 2 | Assess | Industrial Hygienist / Safety Coordinator | Opus 5.5 | High | Hazard assessment |
| 3 | Control | Safety Coordinator | Sonnet 5.5 | Medium | Controls and documents |
| 4 | Compliance | Safety Professional (second reader) / Environmental Compliance Specialist (environmental questions) | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Issue | Safety Coordinator | Haiku 5.5 | Low | Draft assessment or report for the named qualified person |

In Assurance, each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-medium`, `clerk`, `senior-high`, `senior-medium`.

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

The point of the stages is to catch the expensive mistakes early: a hazard nobody listed,
a control that relies on people being careful, a regulatory requirement quoted from memory. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this identify a hazard, control it, or prove compliance? If none, skip it.

Size the job before starting and say which size you picked:

- **Small** - one routine task with a standing assessment to update. Run all stages in the conversation: the task steps, the hazards, the controls, a regulation check, the handoff. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/ehs/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage; load its reference only when needed.

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Planned work** - a task or site activity not yet started. Break the task into steps and list who and what is exposed at each.
- **Incident** - something has happened or nearly happened. Collect the timeline, people, conditions and evidence before any conclusion.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - safety manual, permit system, site rules or regulatory programme -
   is followed and noted in the assessment brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any exposure limit, regulation clause, measurement, rating or training record the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Cite the rule and the evidence.** Common sense is not proof; a requirement passes when it names the regulation or standard clause and the evidence it is met. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Controls are never weakened.** Never remove or downgrade a control, approve work, sign a permit or state that something is safe to proceed on the user's behalf.
5. **This is support, not sign-off.** The assessment is a draft for the qualified person who owns the work.
   This skill never approves work, signs or issues a permit or accepts residual risk; it names the
   qualified person who must (`REQUIRED INPUT` if not known).
6. **Jurisdiction matters.** If the applicable jurisdiction or regulation edition is unknown it is `REQUIRED INPUT`.
7. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
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
6. The assessment finds a risk that cannot be controlled to an acceptable level, or a reportable event.

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
- **gated**: stop after Scope and after Assess for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the task, location or jurisdiction is unclear;
- the procedure, site rules or incident evidence cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Scope (Safety Coordinator)

Turn the request into an assessment brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Activity** - what is being done, where, by whom, with what.
- **Applicable rules** - the regulations, standards and site rules that govern.
- **Done when** - 3 to 7 criteria, each checkable by a cited clause or a piece of evidence. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - jurisdiction, site rules, qualifications, permits, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Planned work track: break the task into steps and list who and what is exposed at each.
- Incident track: collect the timeline, people, conditions and evidence before any conclusion.
- Change work: before writing this, read the standing assessment, permits and past incidents for this task and add **Must not break** -
  existing controls, permit conditions and regulatory commitments.

Handoff: the assessment brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Assess (Industrial Hygienist / Safety Coordinator)

One short piece of work. Settle the step-by-step task breakdown first.

### Hazard assessment

Keep it to what Stage 3 needs to start:

- **Approach** - identify every hazard before choosing any control. Change work: reuse what exists before adding anything new.
- **Risk rating** - likelihood and severity before and after controls, using the house scale or a stated one.
- **Hazard list** - each step, hazard and who is exposed. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - highest severity first; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the hazard assessment.

## Stage 3 - Control (Safety Coordinator)

Write the controls and supporting documents in the order planned. Get controls for the highest-severity hazards complete first, then widen it.

- Planned work track: for each hazard, write -
  - **Control** - in hierarchy order: eliminate, substitute, engineer, administer, then protective equipment.
  - **Stop-work condition** - what makes the crew stop, and who restarts the work.
  - **Permit** - the type needed (for example isolation, hot work, confined space, work at height); issue stays with the site's authorised person.
  - **Competence** - the qualification or training the person doing it needs.
  - **Emergency or rescue** - the arrangement if it goes wrong (for example rescue from height or a confined space).
  - Each one the site has not supplied is `REQUIRED INPUT`, never filled from general practice.
- Planned work track: name who approves the work, issues each permit and accepts the residual risk.
- Incident track: separate facts from causes, and causes from blame. State facts and causes only - no fault or liability statements.
- Incident track: list evidence to preserve (scene, equipment, records, statements) and who holds it.
- Incident track: notification deadlines for the regulator, the insurer and the customer - each `REQUIRED INPUT` while the jurisdiction or contract is unknown.
- Incident track: name the root-cause method used (for example 5 Whys or a causal tree).
- Change work: stay inside the hazard list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the controls and documents, in a usable state.

## Stage 4 - Compliance (Safety Professional / Environmental Compliance Specialist)

A safety assessment is checked by a safety professional; environmental questions by the Environmental Compliance Specialist.

Check what was produced against the assessment brief, by checking each control and requirement against the cited rule.

1. Check every **Done when** criterion and record the evidence: regulation clauses, measurements, training and permit records.
2. Planned work track: every hazard has a control, a stop-work condition, a permit type, a competence and an
   emergency or rescue arrangement, each sourced or marked `REQUIRED INPUT`; the approver, permit issuer and
   risk acceptor are named or `REQUIRED INPUT`. Field verification of controls is `NOT RUN` unless evidence is supplied.
3. Incident track: each corrective action addresses a stated cause and has an owner; notification deadlines,
   evidence preservation and the root-cause method are stated; no fault or liability statements.
4. Change work: check every **Must not break** item still holds.
5. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. In Assurance mode, send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Issue (Safety Coordinator)

Hand it over in a state the user can use immediately.

- Deliver the hazard assessment or incident report, marked as a draft for the qualified person, in the form the user asked for or house rules require.
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
