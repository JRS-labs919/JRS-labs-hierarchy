---
name: "systems-engineering"
description: Take a product or project that joins hardware and software to a baselined set of system requirements, architecture and interface definitions. Use for "define the interfaces", "how do these fit together", "system architecture for" or /jrs:systems-engineering. Not for detailed hardware design (use jrs:hardware-engineering).
---

# JRS-Systems-Engineering

Turn a combined hardware-software need into requirements, an architecture and interfaces every team builds to. 5 stages, each with one owner role, one output and one handoff -
a systems engineering group with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Technology Officer) - rules on escalations, final sign-off (Standard size) | Fable 5.2 | Max | Rulings and release sign-off |
| - | All | Advisor (Chief Systems Engineer) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Requirements | Requirements Engineer | Opus 5.5 | High | System requirements |
| 2 | Architecture | Systems Architect | Opus 5.5 | High | Architecture plan |
| 3 | Define | Systems Engineer / Solutions Architect | Sonnet 5.5 | Medium | Interface definitions |
| 4 | Verify | Integration Test Engineer | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Baseline | Systems Engineer | Sonnet 5.5 | Low | System baseline |

Each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-low`, `builder-medium`, `senior-high`.

Send one packet per stage, not the conversation:

```
ROLE: <title from the table>
STAGE: <n - name>, with that stage's section of this skill
INPUT: <the handoff from the stage before; the record path if Standard size>
RULES: <the ground rules of this skill>
RETURN: <that stage's handoff, plus OPEN ITEMS>
```

The Advisor does not hand off its own row (planning, gates, integration). The Principal is never
dispatched for work - only consulted through the escalation protocol below. If the tier agents
are not available in this environment, the Advisor runs that stage itself and logs
`<role> model/effort NOT SET - ran in session` in the open items.

### Fable fallback

Fable usage can run out, so every job checks the model once at the start and keeps working either way.

| Role | Fable available | Fallback (no Fable) |
|---|---|---|
| Principal | Fable 5.2 / Max | Opus 5.5 / Max |
| Advisor | Fable 5.2 / Medium | Opus 5.5 / Max |
| Stages 1-5 | as in the table above | unchanged |

- **Check at the start.** Run on Fable when the session is on Fable 5.2. Use the fallback when the
  session is on any other model, or when the user says to.
  If the request arrives from the router with a `MODELS:` line, use that and skip the check.
- **Switch mid-job only on failure.** If a Fable call fails for usage or availability partway
  through, switch to the fallback for the rest of the job, log the stage where it switched, and do
  not switch back.
- **The Advisor runs in the session.** Under fallback the session should be Opus 5.5 at max effort. If
  it is another model, or the effort cannot be set, carry on and log `ADVISOR <model/effort> -
  fallback expects Opus 5.5 / Max` in the open items.
- **Principal agent.** Escalations go to `principal` on Fable and to `principal-opus` under fallback.
- **Say which ran.** The record and the report carry a `MODELS:` line.

The user is the program or product owner. Their prompt, plus anything they attached or pointed
to, **is** the system request. Stage 1's job is to turn it into the system requirements, not to send
it back as a questionnaire.

## Keep it small

The point of the stages is to catch the expensive mistakes early: two teams building to different versions of an interface,
a requirement owned by nobody, integration problems found at the end. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change an interface, an allocation or a verification? If not, skip it.

Size the job before starting and say which size you picked:

- **Small** - one interface between two existing components. Run all stages in the conversation: the requirement, the two sides, the interface definition, a trace check, the handoff. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/systems-engineering/<slug>.md`, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **New system** - no baseline exists. Collect stakeholder needs, operating modes and external interfaces.
- **Baselined system** - a controlled baseline already exists. Read the baseline and list what the change touches.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - requirements tool, interface control template or configuration process -
   is followed and noted in the system requirements. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them. This skill fills gaps only.
2. **Never invent facts.** Any signal, protocol, data format, timing, rating or tolerance the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Trace it both ways.** An interface document that reads well is not proof; a criterion passes on a complete trace or an integration test result. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **A baseline changes only on purpose.** Never alter a baselined requirement or interface without logging the change and who it affects.

## Principal and escalation

**One boss.** The Advisor (Chief Systems Engineer) plans and runs the job. The Principal
(Chief Technology Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The system boundary is unclear enough that two different architectures would both fit, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release sign-off - every Standard-size job, before Stage 5 delivers.
6. Hardware and software owners disagree on an interface or an allocation.

**Small size skips the Principal.** The Advisor signs off itself, unless trigger 2 or 4 fires.

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

The Advisor applies the ruling and logs it in the record. If the Principal cannot run on Fable,
send the same packet to the fallback Principal (Opus 5.5 / Max). Only if neither can run does the
Advisor decide, mark it `PRINCIPAL NOT AVAILABLE - Advisor ruled`, and list it under DECISIONS
MADE FOR YOU.

## Mode

- **autonomous** (default): show each stage's output briefly and keep going. Decisions made on
  the user's behalf are listed in the final report so they can overturn any of them.
- **gated**: stop after Requirements and after Architecture for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the system boundary is unclear enough that two different architectures would both fit;
- the requirements, existing interface documents or baseline cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Requirements (Requirements Engineer)

Turn the request into system requirements. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Needs and modes** - what the system must do in each operating mode.
- **Boundary** - what is inside the system and every external interface.
- **Done when** - 3 to 7 criteria, each checkable by trace or integration test. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - standards, existing components, protocols, safety, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- New system track: collect stakeholder needs, operating modes and external interfaces.
- Baselined system track: read the baseline and list what the change touches.
- Change work: before writing this, read the baseline, interface documents and change log and add **Must not break** -
  baselined interfaces and requirements other teams have built to.

Handoff: the system requirements. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Architecture (Systems Architect)

One short piece of work. Settle the system boundary and the split between hardware and software first.

### Architecture plan

Keep it to what Stage 3 needs to start:

- **Approach** - the fewest components and interfaces that meet the requirements. Change work: reuse what exists before adding anything new.
- **Allocation** - each requirement assigned to one component and owner.
- **Interface list** - every interface this job defines or changes. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - external interfaces first, then internal; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the architecture plan.

## Stage 3 - Define (Systems Engineer / Solutions Architect)

Write the interface definitions and allocations in the order planned. Get the external interfaces complete first, then widen it.

- New system track: allocate every requirement to exactly one owner.
- Baselined system track: change only the listed items and update the trace.
- Change work: stay inside the interface list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the interface definitions, in a usable state.

## Stage 4 - Verify (Integration Test Engineer)

Check what was produced against the system requirements, by two-way tracing and integration test review.

1. Check every **Done when** criterion and record the evidence: trace matrix, integration results, open interface issues.
2. New system track: every requirement traces down to an owner and up to a need.
3. Baselined system track: the trace is still complete and no untouched interface changed.
4. Change work: check every **Must not break** item still holds.
5. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Baseline (Systems Engineer)

Hand it over in a state the user can use immediately.

- Deliver the baseline (requirements, architecture, interface definitions, trace), in the form the user asked for or house rules require.
- Say how to use it, in as few steps as it takes.
- Change work: say what changed and where.
- List what is still open.

Report bottom line first, in this shape:

```
VERDICT: <done | done with open items | blocked> - <n>/<n> criteria passed
MODELS: <Fable | Fallback - Opus 5.5 / Max for Principal and Advisor (reason, from Stage n)>
DELIVERED: <deliverable and path, one line each>
HOW TO USE: <steps>
CHANGED: <what changed - change work only>
PRINCIPAL: <not used (Small) | n rulings, sign-off: approved / approved with conditions / rejected>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:systems-engineering
Track: New system | Baselined system    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Requirements
Needs and modes:
Boundary:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Architecture
Approach:
Allocation:
Interface list:
Order:
Risks:

## 3. Define log
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
