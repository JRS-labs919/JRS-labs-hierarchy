---
name: "project-delivery"
description: Take an awarded order, contract or statement of work to a baselined project plan, running status and a closeout package. Use for "kick off this project", "build the project schedule", "write the status report" or /jrs:project-delivery. Not for internal product programs (use jrs:npi-program-management).
---

# JRS-Project-Delivery

Turn an awarded scope into a plan with dates, owners and risks, and keep it honest until closeout. 5 stages, each with one owner role, one output and one handoff -
a project management office with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations, final release review (Standard size) | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (Director, Project Management) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Kickoff | HW: Project Manager / SW: Implementation Manager | Opus 5.5 | High | Project brief |
| 2 | Plan | HW: Project Engineer or Scheduler / SW: Technical Project Manager | Opus 5.5 | High | Baseline plan |
| 3 | Execute | HW: Project Coordinator / SW: Implementation Consultant | Sonnet 5.5 | Medium | Status, logs and change requests |
| 4 | Verify | HW: Site Manager / SW: Implementation Manager | Opus 5.5 | Medium | Pass/fail per criterion |
| 5 | Closeout | Project Coordinator | Haiku 5.5 | Low | Closeout package |

Each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-medium`, `clerk`, `senior-high`, `senior-medium`.

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

The user is the project sponsor (account owner or end customer). Their prompt, plus anything they attached or pointed
to, **is** the project request. Stage 1's job is to turn it into the project brief, not to send
it back as a questionnaire.

**Router and department handoff.** Read any `CHAIN:`, `ROUTE:` and `MODELS:` lines that accompany
the request, including when this is the first department in a chain. If the request also carries a
`HANDOFF:` block, read the deliverable it points to and carry every inherited open item into your own
open items with its owner. Use the `ROUTE:` line as the starting point for track and work type. If an
inherited `REQUIRED INPUT` is something this department cannot work without, stop at Stage 1 and report
`blocked`; do not assume it. If the `CHAIN:` line names a sibling as a later step, do not branch to
that sibling; report `BRANCH: deferred to chain`.

## Keep it small

The point of the stages is to catch the expensive mistakes early: a scope gap found after the baseline,
a milestone date with no path to it, a change done without a change order. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change scope, date, cost or risk, or prove where the project stands? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one status report, one schedule update or one change request. Run all stages in the conversation: the current scope and dates, what moved, the update, a check against the contract, the handoff. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/project-delivery/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - equipment supply, submittals, delivery, installation and startup. Read the contract scope, equipment list, required dates and submittal requirements.
- **Software** - configuration, integration, data migration, training and go-live. Read the statement of work, environments, integrations and acceptance criteria.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - project template, schedule tool, change-order process or reporting cadence -
   is followed and noted in the project brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any date, duration, cost, quantity or contractual term the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Tie it to the contract.** A reported percent-complete is not proof; a milestone passes on a delivered item, a signed acceptance or a dated record. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Do not commit on the customer's side of the line.** Never accept a scope change, agree a date or send anything to the customer unless the user asks.
5. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
   approve. Neither the Advisor nor the Principal stamps, certifies, attests, dispositions, accepts a risk or
   signs off safety - whatever the request asks for. A Principal review means "consistent with the Stage 1
   criteria and the evidence", and nothing more.

## Principal and escalation

**One boss.** The Advisor (Director, Project Management) plans and runs the job. The Principal
(Chief Operating Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The contracted scope or a required date is unclear, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release review - every Standard-size job, before Stage 5 delivers.
6. A change affects contract price, a contractual date or liquidated damages.

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
- **gated**: stop after Kickoff and after Plan for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the contracted scope or a required date is unclear;
- the contract, purchase order or current schedule cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Kickoff (HW: Project Manager / SW: Implementation Manager)

Turn the request into a project brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Scope and deliverables** - what is owed, taken from the contract.
- **Dates and milestones** - contract dates, and which are firm.
- **Done when** - 3 to 7 criteria, each checkable by a delivered item or a dated record. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - contract terms, budget, resources, site access, lead times, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: read the contract scope, equipment list, required dates and submittal requirements.
- Software track: read the statement of work, environments, integrations and acceptance criteria.
- Change work: before writing this, read the current schedule, logs and approved changes and add **Must not break** -
  baseline dates, approved change orders and commitments made to the customer.

Handoff: the project brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Plan (HW: Project Engineer or Scheduler / SW: Technical Project Manager)

Two short pieces of work. Settle the critical path to the first contract milestone first.

### Startup branch

Decide whether site startup or commissioning has to be planned as part of the project, then branch:

| Situation | What to do |
|---|---|
| The project has no site work | Skip. |
| A single supervised energisation with an existing procedure | No branch. Describe it in two or three lines and move on. |
| Site startup or commissioning has to be planned as part of the project | Run **jrs:field-service**. |

When branching, read the jrs:field-service skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the job plan - not
  every stage by reflex.

The branch returns the job plan and its own verdict. Record both, then continue. If
jrs:field-service is not installed, do it inline - list the site activities, prerequisites and durations - and log
`jrs:field-service NOT AVAILABLE` in the open items.

### Baseline plan

Keep it to what Stage 3 needs to start:

- **Approach** - plan to the contract; anything beyond it is a change. Change work: reuse what exists before adding anything new.
- **Risk register** - the few risks that threaten a date or the margin, with an owner.
- **Deliverable list** - every contract deliverable with owner and date. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - long-lead and customer-dependent items first; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the job plan (if branched) plus the baseline plan.

## Stage 3 - Execute (HW: Project Coordinator / SW: Implementation Consultant)

Run the plan and keep the logs in the order planned. Get the schedule to the first milestone complete first, then widen it.

- Hardware track: track submittals, long-lead items, deliveries and site dates in one register.
- Software track: track configuration, integrations, test cycles and cutover in one plan.
- Change work: stay inside the deliverable list and match existing conventions.
- Work against the job plan when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the status, logs and change requests, in a usable state.

## Stage 4 - Verify (HW: Site Manager / SW: Implementation Manager)

Check what was produced against the project brief, by comparing each milestone to the contract and to evidence.

1. Check every **Done when** criterion and record the evidence: delivery records, acceptance sign-offs, dated logs.
2. Hardware track: each milestone ties to a contract date and has evidence of its real status.
3. Software track: each acceptance criterion in the statement of work has a result.
4. Change work: check every **Must not break** item still holds.
5. If the branch ran, check the result against the job plan.
6. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Closeout (Project Coordinator)

Hand it over in a state the user can use immediately.

- Deliver the plan, status report or closeout package, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:field-service stages x-y, verdict>
PRINCIPAL REVIEW: <not used (Small); Advisor release review: consistent / consistent with conditions / not consistent | n rulings; Advisor release review (Small): consistent / consistent with conditions / not consistent | n rulings; Principal release review: consistent / consistent with conditions / not consistent | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:project-delivery
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Kickoff
Scope and deliverables:
Dates and milestones:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Plan
Branch: not needed | inline | jrs:field-service stages x-y -> <run folder>, verdict
Approach:
Risk register:
Deliverable list:
Order:
Risks:

## 3. Execute log
- <step> - <status> - <plan changes, if any>

## 4. Verify
| Criterion | Result | Evidence |
|---|---|---|

## Escalations
| # | Trigger | Question | Ruling | Conditions |
|---|---|---|---|---|

## 5. Open items
| # | Item | Type (TBD / REQUIRED INPUT / NOT RUN / discrepancy) | Owner |
|---|---|---|---|
```
