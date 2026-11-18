---
name: "design-hw"
description: Take a physical product need to an industrial design intent package engineering can build to. Use for "design the enclosure", "what should this product look like", "improve the operator interface" or /jrs:design-hw. Not for software screens and flows (use jrs:design-sw).
---

# JRS-Design-HW

Turn a product need into a design intent package: form, layout, colour-material-finish and operator interface. 5 stages, each with one owner role, one output and one handoff -
an industrial design studio with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Product Officer) - rules on escalations, final sign-off (Standard size) | Fable 5.2 | Max | Rulings and release sign-off |
| - | All | Advisor (Head of Design) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Brief | Industrial Designer | Opus 5.5 | High | Design brief |
| 2 | Concept | Industrial Designer | Opus 5.5 | High | Concept direction |
| 3 | Design | Industrial Designer | Sonnet 5.5 | Medium | Design intent draft |
| 4 | Review | Human Factors Engineer | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Handoff | Industrial Designer | Sonnet 5.5 | Low | Design intent package |

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

The user is the product owner. Their prompt, plus anything they attached or pointed
to, **is** the design request. Stage 1's job is to turn it into the design brief, not to send
it back as a questionnaire.

## Keep it small

The point of the stages is to catch the expensive mistakes early: a form that cannot be manufactured or serviced,
an operator interface that invites a wrong action, a concept chosen before the constraints were known. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change what the user sees, touches or services? If not, skip it.

Size the job before starting and say which size you picked:

- **Small** - one panel, label set or door layout on an existing product. Run all stages in the conversation: a short brief, one concept in words, a layout description, an ergonomics check, the handoff. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/design-hw/<slug>.md`, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **New product** - no existing form to respect. Collect envelope, access, environment and brand constraints before any concept.
- **Refresh** - an existing product family sets the language. Read the existing product's design language and what users complain about.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - brand guide, CMF library, labelling standard or product family language -
   is followed and noted in the design brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them. This skill fills gaps only.
2. **Never invent facts.** Any dimension, clearance, colour code, material or finish the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Check it against a person using it.** A good-looking concept is not proof; each criterion is checked against reach, sight line, access or the brand guide. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Safety markings are not styling.** Never remove, shrink or relocate a warning label, guard or interlock indication for appearance.

## Principal and escalation

**One boss.** The Advisor (Head of Design) plans and runs the job. The Principal
(Chief Product Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The product's users or environment are unclear enough that two different forms would both fit, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release sign-off - every Standard-size job, before Stage 5 delivers.

**Small size skips the Principal.** The Advisor signs off itself, unless trigger 2 or 4 fires.

**Escalation packet** - send this, not the full history, so the Principal works from fresh
context:

```
ESCALATION <n> - trigger <1-5>
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
- **gated**: stop after Brief and after Concept for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the product's users or environment are unclear enough that two different forms would both fit;
- the envelope, existing drawings or brand guide cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Brief (Industrial Designer)

Turn the request into a design brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Users and tasks** - who operates, installs and services it, and what they do.
- **Envelope and environment** - size limits, mounting, indoor or outdoor, access sides.
- **Done when** - 3 to 7 criteria, each checkable by reading the package against the brief. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - envelope, manufacturing process, tooling, brand, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- New product track: collect envelope, access, environment and brand constraints before any concept.
- Refresh track: read the existing product's design language and what users complain about.
- Change work: before writing this, read the current design files, drawings and field feedback and add **Must not break** -
  mounting points, tooling, certified labels and the family look.

Handoff: the design brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Concept (Industrial Designer)

One short piece of work. Settle the layout that the constraints allow first.

### Concept plan

Keep it to what Stage 3 needs to start:

- **Approach** - one direction chosen from at most three, with the reason. Change work: reuse what exists before adding anything new.
- **CMF** - colour, material and finish intent, each sourced or `TBD`.
- **Surface list** - the panels, doors, labels and controls this job touches. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - overall form first, then operator interface, then detail; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the concept plan.

## Stage 3 - Design (Industrial Designer)

Develop the design in the order planned. Get the overall form and layout complete first, then widen it.

- New product track: describe form, layout and CMF precisely enough to model; dimensions are `TBD` unless sourced.
- Refresh track: stay inside the family's form language and existing tooling where possible.
- Change work: stay inside the surface list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the design intent draft, in a usable state.

## Stage 4 - Review (Human Factors Engineer)

Check what was produced against the design brief, by walking each user task through the design.

1. Check every **Done when** criterion and record the evidence: task walk-through notes, ergonomic references, brand-guide checks.
2. New product track: reach, clearance, labelling and service access are checked against the brief.
3. Refresh track: the result still reads as the same family and no tooling change is unlisted.
4. Change work: check every **Must not break** item still holds.
5. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Handoff (Industrial Designer)

Hand it over in a state the user can use immediately.

- Deliver the design intent package (form, layout, CMF, labels, open dimensions), in the form the user asked for or house rules require.
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
# <Name> - jrs:design-hw
Track: New product | Refresh    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Brief
Users and tasks:
Envelope and environment:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Concept
Approach:
CMF:
Surface list:
Order:
Risks:

## 3. Design log
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
