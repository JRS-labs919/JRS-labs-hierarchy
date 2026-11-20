---
name: "design-sw"
description: Take a software product need to a reviewed UX/UI design spec developers can build from. Use for "design this screen", "fix this flow", "make this easier to use" or /jrs:design-sw. Not for physical product form (use jrs:design-hw).
---

# JRS-Design-SW

Turn a software need into flows, screens and copy that a developer can build without guessing. 5 stages, each with one owner role, one output and one handoff -
a product design team with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Product Officer) - rules on escalations, final release review (Standard size) | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (Head of Design) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Brief | UX Researcher | Opus 5.5 | High | Design brief |
| 2 | Structure | UX Designer | Opus 5.5 | High | Flow and structure plan |
| 3 | Design | UI Designer / Design Systems Designer | Sonnet 5.5 | Medium | Screen designs |
| 4 | Review | UX Researcher | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Handoff | UX Writer | Sonnet 5.5 | Low | Design spec |

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

The user is the product owner. Their prompt, plus anything they attached or pointed
to, **is** the design request. Stage 1's job is to turn it into the design brief, not to send
it back as a questionnaire.

**Router and department handoff.** Read any `CHAIN:`, `ROUTE:` and `MODELS:` lines that accompany
the request, including when this is the first department in a chain. If the request also carries a
`HANDOFF:` block, read the deliverable it points to and carry every inherited open item into your own
open items with its owner. Use the `ROUTE:` line as the starting point for track and work type. If an
inherited `REQUIRED INPUT` is something this department cannot work without, stop at Stage 1 and report
`blocked`; do not assume it. If the `CHAIN:` line names a sibling as a later step, do not branch to
that sibling; report `BRANCH: deferred to chain`.

## Keep it small

The point of the stages is to catch the expensive mistakes early: designing screens before the task is understood,
a flow with a dead end or missing state, a one-off component the design system already had. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change what the user can do or understand? If not, skip it.

Size the job before starting and say which size you picked:

- **Small** - one screen or one component change. Run all stages in the conversation: a short brief, the flow in a few lines, the screen described or drawn, a quick heuristic check, the handoff. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/design-sw/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **New interface** - no existing screens to match. List the users, their top tasks and the data each task needs.
- **Existing interface** - the product already has screens and a design system. Read the current screens and reuse the existing components.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - design system, accessibility standard or brand guide -
   is followed and noted in the design brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any user finding, metric, copy string or data field the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Walk the task before calling it done.** A polished screen is not proof; each criterion is checked by walking the task, including empty, error and loading states. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Do not design away a safeguard.** Never remove a confirmation, permission check or warning to shorten a flow unless the user asks.
5. **Accessibility is a criterion, not a polish step.** Contrast, keyboard path and labels are checked in Review every time.
6. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
   approve. Neither the Advisor nor the Principal stamps, certifies, attests, dispositions, accepts a risk or
   signs off safety - whatever the request asks for. A Principal review means "consistent with the Stage 1
   criteria and the evidence", and nothing more.

## Principal and escalation

**One boss.** The Advisor (Head of Design) plans and runs the job. The Principal
(Chief Product Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The user or the task is unclear enough that two different flows would both fit, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release review - every Standard-size job, before Stage 5 delivers.
6. The design changes a safety-critical, destructive or consent screen - alarms, emergency stop, delete, payment or permissions.

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

The Advisor applies the ruling and logs it in the record. If the Principal cannot run on Fable,
send the same packet to the fallback Principal (Opus 5.5 / Max). Only if neither can run does the
Advisor decide, mark it `PRINCIPAL NOT AVAILABLE - Advisor ruled`, and list it under DECISIONS
MADE FOR YOU. An Advisor ruling is never reported as a Principal review: the report line reads
`PRINCIPAL REVIEW: NOT REVIEWED - Principal not available`. If the question was trigger 4 or the risk
trigger, the Advisor may only choose the option that changes nothing, and the verdict is `blocked` until
the user decides.

## Mode

- **autonomous** (default): show each stage's output briefly and keep going. Decisions made on
  the user's behalf are listed in the final report so they can overturn any of them.
- **gated**: stop after Brief and after Structure for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the user or the task is unclear enough that two different flows would both fit;
- the existing screens or design system cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Brief (UX Researcher)

Turn the request into a design brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Users and tasks** - who uses it and the tasks they must complete.
- **Content and data** - what each task needs to show and capture.
- **Done when** - 3 to 7 criteria, each checkable by walking the task through the design. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - platform, design system, accessibility level, technical limits, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- New interface track: list the users, their top tasks and the data each task needs.
- Existing interface track: read the current screens and reuse the existing components.
- Change work: before writing this, read the current screens, components and usage feedback and add **Must not break** -
  existing flows, component behaviour and anything users already rely on.

Handoff: the design brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Structure (UX Designer)

One short piece of work. Settle the flow before any screen first.

### Structure plan

Keep it to what Stage 3 needs to start:

- **Approach** - the shortest flow that completes the task. Change work: reuse what exists before adding anything new.
- **States** - empty, loading, error and success for every screen.
- **Screen list** - the screens and components this job creates or changes. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - the main path first, then edge states; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the structure plan.

## Stage 3 - Design (UI Designer / Design Systems Designer)

Design the screens in the order planned. Get the main path complete first, then widen it.

- New interface track: define tokens and components before screens.
- Existing interface track: use existing components; a new one needs a reason.
- Change work: stay inside the screen list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the screen designs, in a usable state.

## Stage 4 - Review (UX Researcher)

Check what was produced against the design brief, by walking each task and running a heuristic and accessibility pass.

1. Check every **Done when** criterion and record the evidence: task walk-through, heuristic findings, contrast and keyboard checks.
2. New interface track: every task in the brief can be completed start to finish.
3. Existing interface track: nothing else on the touched screens changed without being listed.
4. Change work: check every **Must not break** item still holds.
5. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Handoff (UX Writer)

Hand it over in a state the user can use immediately.

- Deliver the design spec (flows, screens, states, copy), in the form the user asked for or house rules require.
- Say how to use it, in as few steps as it takes.
- Change work: say what changed and where.
- List what is still open.

Report bottom line first, in this shape:

```
VERDICT: <done | done with open items | blocked> - <n>/<n> criteria passed
MODELS: <Fable | Fallback - Opus 5.5 / Max for Principal and Advisor (reason, from Stage n)> [- RAN FLAT when applicable]
DELIVERED: <deliverable and path, one line each>
HOW TO USE: <steps>
CHANGED: <what changed - change work only>
PRINCIPAL REVIEW: <not used (Small) | n rulings, release review: consistent / consistent with conditions / not consistent | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:design-sw
Track: New interface | Existing interface    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Brief
Users and tasks:
Content and data:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Structure
Approach:
States:
Screen list:
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
