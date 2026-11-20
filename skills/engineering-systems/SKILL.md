---
name: "engineering-systems"
description: Take a need to set up or change an engineering tool, schema or workflow to a tested configuration with a rollout note. Use for "set up the PLM category", "add this attribute", "fix the ECO workflow" or /jrs:engineering-systems. Not for corporate IT, ERP and user accounts (use jrs:it).
---

# JRS-Engineering-Systems

Turn a tooling need into a configuration, schema or script that has been tried in a safe place first. 5 stages, each with one owner role, one output and one handoff -
an engineering systems group with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Technology Officer) - rules on escalations, final release review (Standard size) | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (Manager, Engineering Systems) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Request | HW: Configuration Manager / SW: Developer Productivity Engineer | Opus 5.5 | High | Change brief |
| 2 | Design | HW: PLM Administrator / SW: Engineering Tools Developer | Opus 5.5 | High | Configuration plan |
| 3 | Configure | HW: CAD Administrator or BOM Analyst / SW: Engineering Tools Developer | Sonnet 5.5 | Medium | Configuration, import file or script |
| 4 | Verify | HW: Configuration Manager / SW: Source Control Administrator | Opus 5.5 | Medium | Pass/fail per criterion |
| 5 | Release | HW: Document Control Specialist / SW: Source Control Administrator | Haiku 5.5 | Low | Released change and rollout note |

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

The user is the engineering user or team lead. Their prompt, plus anything they attached or pointed
to, **is** the systems request. Stage 1's job is to turn it into the change brief, not to send
it back as a questionnaire.

**Router and department handoff.** Read any `CHAIN:`, `ROUTE:` and `MODELS:` lines that accompany
the request, including when this is the first department in a chain. If the request also carries a
`HANDOFF:` block, read the deliverable it points to and carry every inherited open item into your own
open items with its owner. Use the `ROUTE:` line as the starting point for track and work type. If an
inherited `REQUIRED INPUT` is something this department cannot work without, stop at Stage 1 and report
`blocked`; do not assume it. If the `CHAIN:` line names a sibling as a later step, do not branch to
that sibling; report `BRANCH: deferred to chain`.

## Keep it small

The point of the stages is to catch the expensive mistakes early: a schema change that cannot be undone,
an import that corrupts released data, a tool nobody was told how to use. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change how engineers work, or prove the change is safe? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one attribute, one view, one naming rule or one short script. Run all stages in the conversation: the change in a few lines, the affected records, the config, a test on a sample, the handoff. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/engineering-systems/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - PLM, item and BOM data, document control and CAD standards. Read the current schema, categories, lifecycle and who has which access.
- **Software** - build tooling, repositories, templates and automation for engineers. Read the current repository layout, pipelines and conventions.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - numbering scheme, lifecycle and revision rules, naming convention or access policy -
   is followed and noted in the change brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any attribute name, list value, part number, revision or permission the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Try it on a sample and read it back.** A config that looks right is not proof; a criterion passes when a sample record or run shows the expected result. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Released data is not edited in bulk without being asked.** Never run an import, bulk update, permission change or deletion against the live system unless the user asks.
5. **Work within the access you have.** If a step needs rights you lack, hand over the exact request for the system owner instead of working around it.
6. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
   approve. Neither the Advisor nor the Principal stamps, certifies, attests, dispositions, accepts a risk or
   signs off safety - whatever the request asks for. A Principal review means "consistent with the Stage 1
   criteria and the evidence", and nothing more.

## Principal and escalation

**One boss.** The Advisor (Manager, Engineering Systems) plans and runs the job. The Principal
(Chief Technology Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The intended behaviour is unclear enough that two different configurations would both fit, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release review - every Standard-size job, before Stage 5 delivers.
6. The change alters released records, revision rules or who can approve.

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
- **gated**: stop after Request and after Design for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the intended behaviour is unclear enough that two different configurations would both fit;
- the system, the current schema or the needed permission is not available;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Request (HW: Configuration Manager / SW: Developer Productivity Engineer)

Turn the request into a change brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Need** - what users cannot do today and what they must be able to do.
- **Affected data** - the records, categories, repositories or users the change touches.
- **Done when** - 3 to 7 criteria, each checkable by a read-back or a run. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - system limits, access, existing conventions, downstream integrations, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: read the current schema, categories, lifecycle and who has which access.
- Software track: read the current repository layout, pipelines and conventions.
- Change work: before writing this, read the current configuration, schema and any import history and add **Must not break** -
  released records, numbering, revision history and integrations that read this data.

Handoff: the change brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Design (HW: PLM Administrator / SW: Engineering Tools Developer)

Two short pieces of work. Settle the data model or workflow change and its undo first.

### IT branch

Decide whether the change needs single sign-on, an integration to a business system or new infrastructure, then branch:

| Situation | What to do |
|---|---|
| The change stays inside the engineering tool | Skip. |
| An existing integration is reused unchanged | No branch. Describe it in two or three lines and move on. |
| The change needs single sign-on, an integration to a business system or new infrastructure | Run **jrs:it**. |

When branching, read the jrs:it skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the IT change plan - not
  every stage by reflex.

The branch returns the IT change plan and its own verdict. Record both, then continue. If
jrs:it is not installed, do it inline - list what IT must provide and who to ask - and log
`jrs:it NOT AVAILABLE` in the open items.

### Configuration plan

Keep it to what Stage 3 needs to start:

- **Approach** - the smallest configuration change that meets the need, using standard features first. Change work: reuse what exists before adding anything new.
- **Undo** - how the change is reversed and what cannot be reversed.
- **Change list** - each setting, field, file or script this job creates or changes. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - sample first, then the full set; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the IT change plan (if branched) plus the configuration plan.

## Stage 3 - Configure (HW: CAD Administrator or BOM Analyst / SW: Engineering Tools Developer)

Prepare the configuration in the order planned. Get the change on one sample complete first, then widen it.

- Hardware track: prepare import files and config as reviewable files before anything is applied.
- Software track: keep tools small, documented and versioned with the code they serve.
- Change work: stay inside the change list and match existing conventions.
- Work against the IT change plan when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the configuration, import file or script, in a usable state.

## Stage 4 - Verify (HW: Configuration Manager / SW: Source Control Administrator)

Check what was produced against the change brief, by applying it to a sample or sandbox and reading the result back.

1. Check every **Done when** criterion and record the evidence: sample records, run output, before-and-after values.
2. Hardware track: the change is tried on a sample or sandbox and the records are read back.
3. Software track: the tool runs on a real example and its output is checked.
4. Change work: check every **Must not break** item still holds.
5. If the branch ran, check the result against the IT change plan.
6. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Release (HW: Document Control Specialist / SW: Source Control Administrator)

Hand it over in a state the user can use immediately.

- Deliver the configuration, import file or script with a rollout note, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:it stages x-y, verdict>
PRINCIPAL REVIEW: <not used (Small); Advisor release review: consistent / consistent with conditions / not consistent | n rulings; Advisor release review (Small): consistent / consistent with conditions / not consistent | n rulings; Principal release review: consistent / consistent with conditions / not consistent | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:engineering-systems
Track: Hardware | Software    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Request
Need:
Affected data:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Design
Branch: not needed | inline | jrs:it stages x-y -> <run folder>, verdict
Approach:
Undo:
Change list:
Order:
Risks:

## 3. Configure log
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
