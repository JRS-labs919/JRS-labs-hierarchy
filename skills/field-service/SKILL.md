---
name: "field-service"
description: Take a service call, startup or maintenance request to a job plan with procedure, safety steps and test sheets, then the service report. Use for "plan this site visit", "write the startup procedure", "commissioning checklist for" or /jrs:field-service. Not for remote alarm triage (use jrs:remote-monitoring).
---

# JRS-Field-Service

Turn a site request into a job plan a technician can follow safely, and a report the customer can file. 5 stages, each with one owner role, one output and one handoff -
a field service organisation with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations and Assurance release review | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (VP Service) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Work Order | Service Manager | Opus 5.5 | Medium | Service brief |
| 2 | Job Plan | Field Service Engineer | Opus 5.5 | High | Job plan |
| 3 | Prepare | Commissioning Engineer / Field Service Technician | Sonnet 5.5 | High | Procedure and test sheets |
| 4 | Review | Commissioning Engineer | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Closeout | Spare Parts Coordinator / Field Service Technician | Haiku 5.5 | Low | Service report |

In Assurance, each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-high`, `clerk`, `senior-high`, `senior-medium`.

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

The point of the stages is to catch the expensive mistakes early: a step performed out of sequence on live equipment,
arriving without the part, tool or permit, a test recorded without its acceptance limit. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this make the job safer, or the result provable? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one routine task on one unit with an existing procedure. Run all stages in the conversation: the unit and task, the hazards, the steps, a check against the manual, the report. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/field-service/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage; load its reference only when needed.

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Startup** - first energisation, functional testing and handover of new equipment. Collect the equipment list, drawings, manufacturer startup documents and site prerequisites.
- **Service** - maintenance, troubleshooting, repair and warranty work. Collect the unit history, reported symptoms, manuals and parts on hand.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - site safety rules, lockout/tagout procedure, method-of-procedure template or manufacturer manual -
   is followed and noted in the service brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any setting, torque, test value, acceptance limit, part number or switching step the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Check every step against the manufacturer's document.** Experience is not proof; a step or limit passes when it matches a cited manual, drawing or approved procedure. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **People first, then equipment.** Never write a step for energised work, switching or defeating an interlock that is not taken from an approved source and flagged for the site's qualified person.
5. **A procedure is a draft until the site approves it.** Say so on the first page.
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
6. The job involves energised work, a customer outage or a deviation from the manufacturer's procedure.

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
- **gated**: stop after Work Order and after Job Plan for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the equipment, its state or the site constraints are unclear;
- the manuals, drawings or unit history cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Work Order (Service Manager)

Turn the request into a service brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Equipment and task** - which units, their current state and what must be done.
- **Site conditions** - access, outage window, permits and who the qualified person is.
- **Done when** - 3 to 7 criteria, each checkable by matching a step or value to its source. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - outage window, site rules, parts and tools, qualifications, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Startup track: collect the equipment list, drawings, manufacturer startup documents and site prerequisites.
- Service track: collect the unit history, reported symptoms, manuals and parts on hand.
- Change work: before writing this, read the unit's service history and the last approved procedure and add **Must not break** -
  live loads, customer operations and settings that must be restored.

Handoff: the service brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Job Plan (Field Service Engineer)

Two short pieces of work. Settle the hazards and the isolation sequence first.

### EHS branch

Decide whether the job has a hazard with no existing hazard analysis - energised work, confined space, lifting or working at height, then branch:

| Situation | What to do |
|---|---|
| An approved hazard analysis already covers the job | Skip. Put its reference and date in the job plan. |
| A routine task under a standing analysis | No branch. Put its reference and date in the job plan; describe the task in two or three lines and move on. |
| The job has a hazard with no existing hazard analysis - energised work, confined space, lifting or working at height | Run **jrs:ehs**. |

An existing or standing analysis with no reference, no date, or past its review date counts as no analysis: run **jrs:ehs**.

When branching, read the jrs:ehs skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the hazard analysis - not
  every stage by reflex.

The branch returns the hazard analysis and its own verdict. Record both, then continue. If
jrs:ehs is not installed, do it inline - list each hazard with its control and stop-work condition - and log
`jrs:ehs NOT AVAILABLE` in the open items.

### Job plan

Keep it to what Stage 3 needs to start:

- **Approach** - the manufacturer's procedure, adapted to the site only where needed. Change work: reuse what exists before adding anything new.
- **Parts, tools and people** - what must be on site, each confirmed or flagged.
- **Scope of work** - the units and tasks this visit covers. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - safety and isolation steps first, then the work, then restoration and test; smallest complete version first.
- **Energy isolation** - electrical or stored-energy work (electrical, pressure, spring, thermal, gravity): the
  site's isolation (LOTO) procedure reference. Electrical work also needs the arc-flash and shock boundaries and the
  PPE, from the site's study or labels (for example per NFPA 70E). Each one missing is a blocking `REQUIRED INPUT`.
- Energised work always fires escalation trigger 6, at every size.
- **Risks** - only the ones that would change the plan.

Handoff: the hazard analysis (if branched) plus the job plan.

## Stage 3 - Prepare (Commissioning Engineer / Field Service Technician)

Write the procedure and test sheets in the order planned. Get the isolation, the core task and the restoration complete first, then widen it.

- Startup track: sequence steps from pre-checks through energisation to functional tests, each with its acceptance limit.
- Service track: write isolation and verification steps before any hands-on step.
- Isolation and energisation steps come only from the referenced site procedure or manufacturer document. If
  the LOTO reference or the arc-flash data is missing, write each such step as `[HELD - per site procedure -
  REQUIRED INPUT]`, mark the first page `NOT FOR USE - isolation data missing`, and never fill it from general practice.
- Change work: stay inside the scope of work and match existing conventions.
- Work against the hazard analysis when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the procedure and test sheets, in a usable state.

## Stage 4 - Review (Commissioning Engineer)

Check what was produced against the service brief, by checking each step and limit against the cited source.

1. Check every **Done when** criterion and record the evidence: source and page per step, acceptance limits, unresolved hazards.
2. Startup track: every test has an acceptance limit taken from a cited source.
3. Service track: the procedure restores the unit to a stated, testable condition.
4. Change work: check every **Must not break** item still holds.
5. If the branch ran, check the result against the hazard analysis.
6. Independently of Stage 3, trace every safety step (isolation, verification of zero energy, energisation,
   interlock, PPE) to an approved source by reference and page; any step without one fails, and a held
   placeholder stays held.
7. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. In Assurance mode, send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Closeout (Spare Parts Coordinator / Field Service Technician)

Hand it over in a state the user can use immediately.

- Deliver the job plan, procedure and test sheets, or the service report, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:ehs stages x-y, verdict>
PRINCIPAL REVIEW: <not used; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Principal release review: consistent / consistent with conditions / not consistent (Assurance) | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Never omit `VERDICT:`, `MODELS:`, `USAGE:` or `PRINCIPAL REVIEW:`. Leave out any other line that has nothing to say.

## Standard record

For Standard work, read `references/record-template.md` immediately before creating the record. Do not load it for Small work.
