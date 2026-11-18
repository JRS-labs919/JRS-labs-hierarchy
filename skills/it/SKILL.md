---
name: "it"
description: Take an IT request, problem or system change to a tested change or fix with a rollback and a user note. Use for "set up access for", "this system isn't working", "configure the ERP to" or /jrs:it. Not for engineering tools such as PLM and CAD (use jrs:engineering-systems).
---

# JRS-IT

Turn a ticket into a configuration, script or fix that has been tested and can be undone. 5 stages, each with one owner role, one output and one handoff -
an IT department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Information Officer) - rules on escalations, final sign-off (Standard size) | Fable 5.2 | Max | Rulings and release sign-off |
| - | All | Advisor (IT Manager) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Request | Help Desk Technician | Sonnet 5.5 | Low | Ticket brief |
| 2 | Design | HW: ERP Administrator or OT/Plant Network Engineer / SW: Identity & Access Engineer | Opus 5.5 | High | Change plan |
| 3 | Implement | HW: MES Administrator / SW: SaaS Administrator or Systems Administrator | Sonnet 5.5 | Medium | Configuration, script or fix |
| 4 | Test | Network Engineer / Systems Administrator | Opus 5.5 | Medium | Pass/fail per criterion |
| 5 | Handover | Help Desk Technician | Haiku 5.5 | Low | Change record and user note |

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

The user is the employee or system owner. Their prompt, plus anything they attached or pointed
to, **is** the IT request. Stage 1's job is to turn it into the ticket brief, not to send
it back as a questionnaire.

## Keep it small

The point of the stages is to catch the expensive mistakes early: a change that locks people out or stops the plant,
access granted more widely than needed, a fix nobody can undo. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this fix the problem, or prove the fix is safe? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one user, one setting or one documented fix. Run all stages in the conversation: the problem, the cause, the change, a test, the note to the user. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/it/<slug>.md`, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - ERP, MES, plant-floor networks and the systems production depends on. Collect the system, the process it supports and the production window.
- **Software** - SaaS applications, identity, access and employee devices. Collect the user, role, application and who approves access.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - change-management process, access policy, naming standard or security policy -
   is followed and noted in the ticket brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them. This skill fills gaps only.
2. **Never invent facts.** Any hostname, account, license count, permission or setting the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Test it as the user.** A setting that was saved is not proof; a criterion passes when the task is performed with the affected account or a test transaction. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Live systems are opt-in.** Never change production, grant or remove access, reset credentials or delete data unless the user asks.
5. **Credentials never go in the record.** Refer to where a secret lives, not what it is.

## Principal and escalation

**One boss.** The Advisor (IT Manager) plans and runs the job. The Principal
(Chief Information Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. What the user needs to be able to do is unclear, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release sign-off - every Standard-size job, before Stage 5 delivers.
6. The change affects production availability, privileged access or company data leaving a system.

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
- **gated**: stop after Request and after Design for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- what the user needs to be able to do is unclear;
- the system, admin rights or the access approver is not available;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Request (Help Desk Technician)

Turn the request into a ticket brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Need or symptom** - what the user needs, or what is failing and since when.
- **Affected** - users, systems and business processes touched.
- **Done when** - 3 to 7 criteria, each checkable by performing the task or a test transaction. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - change window, access policy, licences, security policy, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: collect the system, the process it supports and the production window.
- Software track: collect the user, role, application and who approves access.
- Change work: before writing this, read the current configuration and recent changes and add **Must not break** -
  running business processes, existing access and integrations.

Handoff: the ticket brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Design (HW: ERP Administrator or OT/Plant Network Engineer / SW: Identity & Access Engineer)

Two short pieces of work. Settle the way back first.

### Security branch

Decide whether the change adds a new application, privileged access or a new path for data to leave, then branch:

| Situation | What to do |
|---|---|
| The change reuses an approved pattern | Skip. |
| A standard role is assigned to a standard user | No branch. Describe it in two or three lines and move on. |
| The change adds a new application, privileged access or a new path for data to leave | Run **jrs:security**. |

When branching, read the jrs:security skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the security findings - not
  every stage by reflex.

The branch returns the security findings and its own verdict. Record both, then continue. If
jrs:security is not installed, do it inline - list the data involved, who can reach it and the control - and log
`jrs:security NOT AVAILABLE` in the open items.

### Change plan

Keep it to what Stage 3 needs to start:

- **Approach** - standard configuration before customisation; least privilege. Change work: reuse what exists before adding anything new.
- **Rollback** - the exact steps to undo it.
- **Change list** - each setting, account, group or script this job touches. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - test environment or one user first, then everyone; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the security findings (if branched) plus the change plan.

## Stage 3 - Implement (HW: MES Administrator / SW: SaaS Administrator or Systems Administrator)

Make the configuration, script or fix in the order planned. Get the change for one user or one test case complete first, then widen it.

- Hardware track: stage the change outside production hours with a tested way back.
- Software track: grant the least access that does the job, through groups rather than individuals.
- Change work: stay inside the change list and match existing conventions.
- Work against the security findings when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the configuration, script or fix, in a usable state.

## Stage 4 - Test (Network Engineer / Systems Administrator)

Check what was produced against the ticket brief, by performing the task with the affected account or a test transaction.

1. Check every **Done when** criterion and record the evidence: test results, before-and-after settings, rollback test.
2. Hardware track: the business process runs end to end on a test transaction.
3. Software track: the user can do the task and cannot do what they should not.
4. Change work: check every **Must not break** item still holds.
5. If the branch ran, check the result against the security findings.
6. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Handover (Help Desk Technician)

Hand it over in a state the user can use immediately.

- Deliver the change, rollback steps and a note for the user, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:security stages x-y, verdict>
PRINCIPAL: <not used (Small) | n rulings, sign-off: approved / approved with conditions / rejected>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:it
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Request
Need or symptom:
Affected:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Design
Branch: not needed | inline | jrs:security stages x-y -> <run folder>, verdict
Approach:
Rollback:
Change list:
Order:
Risks:

## 3. Implement log
- <step> - <status> - <plan changes, if any>

## 4. Test
| Criterion | Result | Evidence |
|---|---|---|

## Escalations
| # | Trigger | Question | Ruling | Conditions |
|---|---|---|---|---|

## 5. Open items
| # | Item | Type (TBD / REQUIRED INPUT / NOT RUN / discrepancy) | Owner |
|---|---|---|---|
```
