---
name: "quality"
description: Take a product, process, supplier or release that must be shown to conform to a quality record with a clear disposition. Use for "write the inspection plan", "does this conform", "open an NCR" or /jrs:quality. Not for writing and running software tests (use jrs:software-engineering).
---

# JRS-Quality

Turn a conformance question into a plan, findings and a disposition that stands up to an audit. 5 stages, each with one owner role, one output and one handoff -
a quality department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations, final sign-off (Standard size) | Fable 5.2 | Max | Rulings and release sign-off |
| - | All | Advisor (VP Quality) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Define | HW: Quality Engineer / SW: Software Quality Manager | Opus 5.5 | High | Quality brief |
| 2 | Plan | HW: Certification Engineer or Supplier Quality Engineer / SW: Release Assurance Analyst | Opus 5.5 | High | Inspection and test plan |
| 3 | Inspect | HW: QC Inspector or Quality Technician / SW: Release Assurance Analyst | Sonnet 5.5 | Medium | Findings log |
| 4 | Disposition | QMS Manager / ISO Auditor | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Record | CAPA Coordinator | Haiku 5.5 | Low | Quality record |

Each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-medium`, `clerk`, `senior-high`.

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

The user is the internal requester (manufacturing, engineering, supply chain or a project). Their prompt, plus anything they attached or pointed
to, **is** the quality request. Stage 1's job is to turn it into the quality brief, not to send
it back as a questionnaire.

## Keep it small

The point of the stages is to catch the expensive mistakes early: accepting something that does not conform,
inspecting to the wrong revision or standard, a corrective action that treats the symptom. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change the disposition, or provide evidence for it? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one characteristic, one document or one nonconformance. Run all stages in the conversation: the requirement, the method, the finding, the disposition, the record. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/quality/<slug>.md`, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - parts, assemblies, suppliers and certifications. Collect the drawing revision, spec, standard and acceptance limits.
- **Software** - release readiness and process compliance. Collect the release criteria, test results and open defects.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - quality manual, inspection standard, sampling plan or certification scheme -
   is followed and noted in the quality brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them. This skill fills gaps only.
2. **Never invent facts.** Any measurement, tolerance, test result, certificate number or standard clause the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Evidence or it did not happen.** A statement that something was checked is not proof; a criterion passes on a recorded value, document or test result. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Quality reports, it does not waive.** Never accept, release, rework or scrap on the user's behalf, or close a nonconformance, unless the user asks.
5. **Cite the requirement.** Every finding names the drawing, spec or standard clause and its revision or edition.

## Principal and escalation

**One boss.** The Advisor (VP Quality) plans and runs the job. The Principal
(Chief Operating Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The requirement or the acceptance limit is unclear, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release sign-off - every Standard-size job, before Stage 5 delivers.
6. The disposition is use-as-is, a concession or a waiver of a requirement.

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

Handoff: the inspection and test plan.

## Stage 3 - Inspect (HW: QC Inspector or Quality Technician / SW: Release Assurance Analyst)

Carry out the checks and log the findings in the order planned. Get the critical characteristics complete first, then widen it.

- Hardware track: record each characteristic's requirement, measured or observed value, and method.
- Software track: record each release criterion, its evidence and any waiver.
- Change work: stay inside the characteristic list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the findings log, in a usable state.

## Stage 4 - Disposition (QMS Manager / ISO Auditor)

Check what was produced against the quality brief, by judging each finding against its cited requirement.

1. Check every **Done when** criterion and record the evidence: recorded values, documents, photos, test results, waivers.
2. Hardware track: each finding cites the requirement clause and the evidence.
3. Software track: each criterion has a result or a signed waiver; open defects are listed by severity.
4. Change work: check every **Must not break** item still holds.
5. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Record (CAPA Coordinator)

Hand it over in a state the user can use immediately.

- Deliver the quality record (plan, findings, disposition, corrective actions), in the form the user asked for or house rules require.
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
# <Name> - jrs:quality
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Define
Subject:
Requirements:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Plan
Approach:
Method:
Characteristic list:
Order:
Risks:

## 3. Inspect log
- <step> - <status> - <plan changes, if any>

## 4. Disposition
| Criterion | Result | Evidence |
|---|---|---|

## Escalations
| # | Trigger | Question | Ruling | Conditions |
|---|---|---|---|---|

## 5. Open items
| # | Item | Type (TBD / REQUIRED INPUT / NOT RUN / discrepancy) | Owner |
|---|---|---|---|
```
