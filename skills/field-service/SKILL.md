---
name: "field-service"
description: Take a service call, startup or maintenance request to a job plan with procedure, safety steps and test sheets, then the service report. Use for "plan this site visit", "write the startup procedure", "commissioning checklist for" or /jrs:field-service. Not for remote alarm triage (use jrs:remote-monitoring).
---

# JRS-Field-Service

Turn a site request into a job plan a technician can follow safely, and a report the customer can file. 5 stages, each with one owner role, one output and one handoff -
a field service organisation with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations, final release review (Standard size) | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (VP Service) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Work Order | Service Manager | Opus 5.5 | Medium | Service brief |
| 2 | Job Plan | Field Service Engineer | Opus 5.5 | High | Job plan |
| 3 | Prepare | Commissioning Engineer / Field Service Technician | Sonnet 5.5 | High | Procedure and test sheets |
| 4 | Review | Commissioning Engineer | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Closeout | Spare Parts Coordinator / Field Service Technician | Haiku 5.5 | Low | Service report |

Each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-high`, `clerk`, `senior-high`, `senior-medium`.

Send one packet per stage, not the conversation:

```
ROLE: <title from the table>
STAGE: <n - name>, with that stage's section of this skill
INPUT: <the handoff from the stage before; the record path if Standard size>
RULES: <the ground rules of this skill>
RETURN: <that stage's handoff, plus OPEN ITEMS>
```

Do not combine stages in one dispatch when the tier agents are available. Stage 5 must be dispatched
to its listed owner; do not run it in the session when that tier agent is available.

The Advisor does not hand off its own row (planning, gates, integration). The Principal is never
dispatched for work - only consulted through the escalation protocol below. If the tier agents
are not available in this environment, the Advisor runs that stage itself and logs
`<role> model/effort NOT SET - ran in session` in the open items.

**Running inside a subagent.** If you have no tool to dispatch agents and none to ask the user, you are
running flat: no tier agents, no Principal, and the user cannot be reached. Say so on the report's
`MODELS:` line (`- RAN FLAT`). Run the stages yourself. But when a stop-and-ask condition, trigger 4 or
the risk trigger (trigger 6) applies, stop there and return `blocked`, with the questions or the
escalation packet for your caller to act on. Do not rule on it yourself.

### Fable fallback

Fable usage can run out, so every job checks the model once at the start and keeps working either way.

| Role | Fable available | Fallback (no Fable) |
|---|---|---|
| Principal | Fable 5.2 / Max | Opus 5.5 / Max |
| Advisor | Fable 5.2 / Medium | Opus 5.5 / Max |
| Stages 1-5 | as in the table above | unchanged |

- **Check at the start.** Run on Fable when your system prompt names a Fable model (any version). Use the fallback when the
  session is on any other model, or when the user says to.
  If the request arrives with a `MODELS:` line, use it only when it agrees with the model your own
  system prompt names. If they differ, go by your system prompt and log the mismatch in the open items.
- **Switch mid-job only on failure.** If a Fable call fails for usage or availability partway
  through, switch to the fallback for the rest of the job, log the stage where it switched, and do
  not switch back.
- **The Advisor runs in the session.** Under fallback the session should be Opus 5.5 at max effort. If
  it is another model, or the effort cannot be set, carry on and log `ADVISOR <model/effort> -
  fallback expects Opus 5.5 / Max` in the open items.
- **Principal agent.** Escalations go to `principal` on Fable and to `principal-opus` under fallback.
- **Say which ran.** The record and the report carry a `MODELS:` line.

The user is the site owner or the internal project team. Their prompt, plus anything they attached or pointed
to, **is** the service request. Stage 1's job is to turn it into the service brief, not to send
it back as a questionnaire.

**Router and department handoff.** Read any `CHAIN:`, `ROUTE:` and `MODELS:` lines that accompany
the request, including when this is the first department in a chain. If the request also carries a
`HANDOFF:` block, read the deliverable it points to and carry every inherited open item into your own
open items with its owner. Use the `ROUTE:` line as the starting point for track and work type. If an
inherited `REQUIRED INPUT` is something this department cannot work without, stop at Stage 1 and report
`blocked`; do not assume it. If the `CHAIN:` line names a sibling as a later step, do not branch to
that sibling; report `BRANCH: deferred to chain`.

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
  section per stage (template at the end).

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

## Principal and escalation

**One boss.** The Advisor (VP Service) plans and runs the job. The Principal
(Chief Operating Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The equipment, its state or the site constraints are unclear, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release review - every Standard-size job, before Stage 5 delivers.
6. The job involves energised work, a customer outage or a deviation from the manufacturer's procedure.

**Small size skips the Principal.** The Advisor does the release review itself, unless trigger 2, 4 or 6
fires. Trigger 6 is this skill's risk trigger: it applies at every size, and so does every stop-and-ask
condition.

**Escalation packet** - send this, not the full history, so the Principal works from fresh
context:

```
ESCALATION <n> - trigger <1-6>
QUESTION: <one sentence>
OPTIONS: <A / B / C, one line each>
EVIDENCE: <sources, results, file paths>
ADVISOR RECOMMENDS: <option + one-line reason>
```

**Ruling** - the Principal returns:

```
RULING <n>: <option chosen | other: ...> - <reason, one or two lines>
CONDITIONS: <anything the Advisor must do or check, if any>
```

The Advisor applies the ruling and logs it in the record. Wait for the ruling and apply its conditions
before dispatching any stage that depends on it. After any stage review or release review,
a material edit to reviewed content invalidates that review; send the changed content back to the same reviewer
and repeat any affected release review before Stage 5 delivers. If the Principal cannot run on Fable,
send the same packet to the fallback Principal (Opus 5.5 / Max). Only if neither can run does the
Advisor decide, mark it `PRINCIPAL NOT AVAILABLE - Advisor ruled`, and list it under DECISIONS
MADE FOR YOU. An Advisor ruling is never reported as a Principal review: the report line reads
`PRINCIPAL REVIEW: NOT REVIEWED - Principal not available`. If the question was trigger 4 or the risk
trigger, the Advisor may only choose the option that changes nothing, and the verdict is `blocked` until
the user decides.

## Mode

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

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

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
MODELS: <Fable | Fallback - Opus 5.5 / Max for Principal and Advisor (reason, from Stage n)> [- RAN FLAT when applicable]
DELIVERED: <deliverable and path, one line each>
HOW TO USE: <steps>
CHANGED: <what changed - change work only>
BRANCH: <not needed | inline | jrs:ehs stages x-y, verdict>
PRINCIPAL REVIEW: <not used (Small); Advisor release review: consistent / consistent with conditions / not consistent | n rulings; Advisor release review (Small): consistent / consistent with conditions / not consistent | n rulings; Principal release review: consistent / consistent with conditions / not consistent | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:field-service
Track: Startup | Service    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Work Order
Equipment and task:
Site conditions:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Job Plan
Branch: not needed | inline | jrs:ehs stages x-y -> <run folder>, verdict
Approach:
Parts, tools and people:
Scope of work:
Order:
Hazard analysis: <reference, date> | branched
Energy isolation: LOTO ref | arc-flash/shock boundary | PPE (or REQUIRED INPUT)
Risks:

## 3. Prepare log
- <step> - <status> - <plan changes, if any>

## 4. Review
| Criterion | Result | Evidence |
|---|---|---|

## Escalations
| # | Trigger | Question | Ruling | Conditions |
|---|---|---|---|---|

## 5. Open items
| # | Item | Type (TBD / REQUIRED INPUT / NOT RUN / discrepancy) | Owner |
|---|---|---|---|
```
