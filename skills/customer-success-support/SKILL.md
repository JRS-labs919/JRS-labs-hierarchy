---
name: "customer-success-support"
description: Take a customer issue, question or account-health concern to a diagnosed case with a resolution, a customer reply draft and a clean record. Use for "answer this support ticket", "is this covered by warranty", "customer is reporting" or /jrs:customer-success-support. Not for planning an on-site visit (use jrs:field-service).
---

# JRS-Customer-Success-Support

Turn a customer's report into a diagnosis, a fix or next step, and a reply that is accurate and promises only what is approved. 5 stages, each with one owner role, one output and one handoff -
a customer support organisation with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Revenue Officer) - rules on escalations, final release review (Standard size) | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (VP Customer Experience) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Intake | HW: Order Customer Service Rep / SW: Support Engineer (Tier 1) | Sonnet 5.5 | Low | Case brief |
| 2 | Diagnose | HW: Technical Support Engineer / SW: Support Engineer (Tier 2-3) | Opus 5.5 | High | Diagnosis and resolution plan |
| 3 | Resolve | HW: RMA Coordinator or Warranty Administrator / SW: Customer Success Manager or Onboarding Specialist | Sonnet 5.5 | Medium | Resolution and reply draft |
| 4 | Verify | HW: Technical Support Engineer / SW: Support Engineer (Tier 3) | Opus 5.5 | Medium | Pass/fail per criterion |
| 5 | Close | Support Operations Analyst | Haiku 5.5 | Low | Case record and knowledge note |

Each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-low`, `builder-medium`, `clerk`, `senior-high`, `senior-medium`.

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

The user is the customer, through whoever owns the case. Their prompt, plus anything they attached or pointed
to, **is** the case. Stage 1's job is to turn it into the case brief, not to send
it back as a questionnaire.

**Router and department handoff.** Read any `CHAIN:`, `ROUTE:` and `MODELS:` lines that accompany
the request, including when this is the first department in a chain. If the request also carries a
`HANDOFF:` block, read the deliverable it points to and carry every inherited open item into your own
open items with its owner. Use the `ROUTE:` line as the starting point for track and work type. If an
inherited `REQUIRED INPUT` is something this department cannot work without, stop at Stage 1 and report
`blocked`; do not assume it. If the `CHAIN:` line names a sibling as a later step, do not branch to
that sibling; report `BRANCH: deferred to chain`.

## Keep it small

The point of the stages is to catch the expensive mistakes early: answering a different problem than the one reported,
promising coverage or a credit that is not approved, closing a case the customer still has. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this move the customer toward a fix, or prove the fix worked? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one question with a documented answer. Run all stages in the conversation: what they reported, the cause, the answer, a check against the docs, the reply. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/customer-success-support/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - equipment faults, warranty claims, returns and order issues. Collect the model, serial, install date, symptoms and what has been tried.
- **Software** - product issues, how-to questions, onboarding and account health. Collect the account, version, steps to reproduce and the impact.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - support playbook, severity scale, warranty terms, service-level agreement or tone guide -
   is followed and noted in the case brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any warranty term, part number, fix version, credit amount or date the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Reproduce it or cite it.** A confident answer is not proof; a resolution passes when it was reproduced or matches a cited document for that model or version. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Replies are drafts.** Never send a reply, approve a return, warranty claim or credit, or promise a date unless the user asks.
5. **Safety advice comes only from the manual.** Do not improvise a hands-on step for electrical or mechanical equipment.
6. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
   approve. Neither the Advisor nor the Principal stamps, certifies, attests, dispositions, accepts a risk or
   signs off safety - whatever the request asks for. A Principal review means "consistent with the Stage 1
   criteria and the evidence", and nothing more.

## Principal and escalation

**One boss.** The Advisor (VP Customer Experience) plans and runs the job. The Principal
(Chief Revenue Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. What the customer is actually experiencing is unclear, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release review - every Standard-size job, before Stage 5 delivers.
6. The resolution needs a warranty exception, credit or replacement outside policy, or involves a safety event.

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
- **gated**: stop after Intake and after Diagnose for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- what the customer is actually experiencing is unclear;
- the case history, product documentation or warranty terms cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Intake (HW: Order Customer Service Rep / SW: Support Engineer (Tier 1))

Turn the report into a case brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Reported problem** - in the customer's words, with product, version or serial.
- **Impact and urgency** - what is down or blocked, and for whom.
- **Done when** - 3 to 7 criteria, each checkable by reproduction or a cited document. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - service level, warranty terms, policy limits, customer environment, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: collect the model, serial, install date, symptoms and what has been tried.
- Software track: collect the account, version, steps to reproduce and the impact.
- Change work: before writing this, read the case history and earlier replies and add **Must not break** -
  commitments already made to this customer.

Handoff: the case brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Diagnose (HW: Technical Support Engineer / SW: Support Engineer (Tier 2-3))

Two short pieces of work. Settle the most likely cause and how to confirm it first.

### Site visit branch

Decide whether the resolution needs someone on site, then branch:

| Situation | What to do |
|---|---|
| The case is resolved remotely | Skip. |
| The customer's own technician can do a documented check | No branch. Describe it in two or three lines and move on. |
| The resolution needs someone on site | Run **jrs:field-service**. |

When branching, read the jrs:field-service skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the job plan - not
  every stage by reflex.

The branch returns the job plan and its own verdict. Record both, then continue. If
jrs:field-service is not installed, do it inline - write a dispatch request with symptoms, serial and likely parts - and log
`jrs:field-service NOT AVAILABLE` in the open items.

### Diagnosis and resolution plan

Keep it to what Stage 3 needs to start:

- **Approach** - confirm the cause before prescribing the fix. Change work: reuse what exists before adding anything new.
- **Evidence** - what supports the diagnosis and what would disprove it.
- **Action list** - each step for the customer and each step for us. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - restore service first, then root cause; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the job plan (if branched) plus the diagnosis and resolution plan.

## Stage 3 - Resolve (HW: RMA Coordinator or Warranty Administrator / SW: Customer Success Manager or Onboarding Specialist)

Write the resolution and the reply draft in the order planned. Get the step that restores service complete first, then widen it.

- Hardware track: give safe checks first; warranty and return decisions cite the terms that apply.
- Software track: reproduce before answering where possible; give the workaround and the fix separately.
- Change work: stay inside the action list and match existing conventions.
- Work against the job plan when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the resolution and reply draft, in a usable state.

## Stage 4 - Verify (HW: Technical Support Engineer / SW: Support Engineer (Tier 3))

Check what was produced against the case brief, by reproducing the fix or matching it to the documentation.

1. Check every **Done when** criterion and record the evidence: reproduction notes, document references, policy checks.
2. Hardware track: the diagnosis fits every reported symptom and each instruction matches the manual.
3. Software track: the steps were reproduced or match the documentation for the customer's version.
4. Change work: check every **Must not break** item still holds.
5. If the branch ran, check the result against the job plan.
6. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Close (Support Operations Analyst)

Hand it over in a state the user can use immediately.

- Deliver the reply draft, resolution steps and case record, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:field-service stages x-y, verdict>
PRINCIPAL REVIEW: <not used (Small) | n rulings, release review: consistent / consistent with conditions / not consistent | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:customer-success-support
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Intake
Reported problem:
Impact and urgency:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Diagnose
Branch: not needed | inline | jrs:field-service stages x-y -> <run folder>, verdict
Approach:
Evidence:
Action list:
Order:
Risks:

## 3. Resolve log
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
