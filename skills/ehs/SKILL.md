---
name: "ehs"
description: Take a task, site, incident or regulatory question to a hazard assessment with controls, or an incident report with corrective actions. Use for "write the JHA for", "is this safe to do", "investigate this incident" or /jrs:ehs. Not for the step-by-step work procedure (use jrs:field-service).
---

# JRS-EHS

Turn a task or an incident into identified hazards, controls that match them and a record that would satisfy an inspector. 5 stages, each with one owner role, one output and one handoff -
an EHS department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations, final release review (Standard size) | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (EHS Manager) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Scope | Safety Coordinator | Opus 5.5 | Medium | Assessment brief |
| 2 | Assess | Industrial Hygienist / Safety Coordinator | Opus 5.5 | High | Hazard assessment |
| 3 | Control | Safety Coordinator | Sonnet 5.5 | Medium | Controls and documents |
| 4 | Compliance | Safety Professional (second reader) / Environmental Compliance Specialist (environmental questions) | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Issue | Safety Coordinator | Haiku 5.5 | Low | Draft assessment or report for the named qualified person |

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

The user is the work owner (a supervisor, project or site lead). Their prompt, plus anything they attached or pointed
to, **is** the safety request. Stage 1's job is to turn it into the assessment brief, not to send
it back as a questionnaire.

**Router and department handoff.** Read any `CHAIN:`, `ROUTE:` and `MODELS:` lines that accompany
the request, including when this is the first department in a chain. If the request also carries a
`HANDOFF:` block, read the deliverable it points to and carry every inherited open item into your own
open items with its owner. Use the `ROUTE:` line as the starting point for track and work type. If an
inherited `REQUIRED INPUT` is something this department cannot work without, stop at Stage 1 and report
`blocked`; do not assume it. If the `CHAIN:` line names a sibling as a later step, do not branch to
that sibling; report `BRANCH: deferred to chain`.

## Keep it small

The point of the stages is to catch the expensive mistakes early: a hazard nobody listed,
a control that relies on people being careful, a regulatory requirement quoted from memory. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this identify a hazard, control it, or prove compliance? If none, skip it.

Size the job before starting and say which size you picked:

- **Small** - one routine task with a standing assessment to update. Run all stages in the conversation: the task steps, the hazards, the controls, a regulation check, the handoff. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/ehs/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage (template at the end).

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

## Principal and escalation

**One boss.** The Advisor (EHS Manager) plans and runs the job. The Principal
(Chief Operating Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The task, location or jurisdiction is unclear, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release review - every Standard-size job, before Stage 5 delivers.
6. The assessment finds a risk that cannot be controlled to an acceptable level, or a reportable event.

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

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Issue (Safety Coordinator)

Hand it over in a state the user can use immediately.

- Deliver the hazard assessment or incident report, marked as a draft for the qualified person, in the form the user asked for or house rules require.
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
# <Name> - jrs:ehs
Track: Planned work | Incident    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Scope
Activity:
Applicable rules:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Assess
Approach:
Risk rating:
Hazard list:
Order:
Risks:

## 3. Control log
Per hazard: control | stop-work | permit | competence | emergency/rescue
Approver / permit issuer / risk acceptor:
Incident: notifications and deadlines | evidence held | root-cause method
- <step> - <status> - <plan changes, if any>

## 4. Compliance
| Criterion | Result | Evidence |
|---|---|---|

## Escalations
| # | Trigger | Question | Ruling | Conditions |
|---|---|---|---|---|

## 5. Open items
| # | Item | Type (TBD / REQUIRED INPUT / NOT RUN / discrepancy) | Owner |
|---|---|---|---|
```
