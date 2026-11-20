---
name: "product-management"
description: Take a product idea, customer request or market gap to an approved PRD and roadmap entry. Use for "write a PRD", "should we build this", "add this to the roadmap" or /jrs:product-management. Not for detailed engineering design (use jrs:hardware-engineering or jrs:software-engineering).
---

# JRS-Product-Management

Turn a product request into a PRD engineering can build from and a roadmap entry leadership can approve. 5 stages, each with one owner role, one output and one handoff -
a product management team with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Product Officer) - rules on escalations, final release review (Standard size) | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (VP Product) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Brief | HW: Hardware Product Manager / SW: Software Product Manager | Opus 5.5 | High | Product brief |
| 2 | Define | HW: Product Line Manager / SW: Technical PM | Opus 5.5 | High | Requirements plan |
| 3 | Write | Product Owner | Sonnet 5.5 | Medium | PRD draft |
| 4 | Verify | Portfolio Manager | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Release | Product Operations Analyst | Haiku 5.5 | Low | PRD and roadmap entry |

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

The user is the requester (sales, a customer, engineering or leadership). Their prompt, plus anything they attached or pointed
to, **is** the product request. Stage 1's job is to turn it into the product brief, not to send
it back as a questionnaire.

**Router and department handoff.** Read any `CHAIN:`, `ROUTE:` and `MODELS:` lines that accompany
the request, including when this is the first department in a chain. If the request also carries a
`HANDOFF:` block, read the deliverable it points to and carry every inherited open item into your own
open items with its owner. Use the `ROUTE:` line as the starting point for track and work type. If an
inherited `REQUIRED INPUT` is something this department cannot work without, stop at Stage 1 and report
`blocked`; do not assume it. If the `CHAIN:` line names a sibling as a later step, do not branch to
that sibling; report `BRANCH: deferred to chain`.

## Keep it small

The point of the stages is to catch the expensive mistakes early: solving a problem no customer has,
a requirement nobody can test, scope that keeps growing after the commit. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change what gets built, or prove a customer needs it? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one feature, option or variant on an existing product, expressible in under a page. Run all stages in the conversation: a five-line brief, a prioritised requirement list, a check against the brief, the handoff. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/product-management/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - a physical product, option or variant. Collect the ratings, standards, certifications and target cost the request names.
- **Software** - an application, platform feature or service. Collect the users, workflows, integrations and data the request names.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - product template, roadmap format, pricing policy or brand standard -
   is followed and noted in the product brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any market size, price, cost, rating, date or customer quote the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Trace it before calling it done.** A requirement that sounds right is not proof; each one traces to the request, a source or a labelled assumption. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Do not commit the company.** Never state a price, launch date or roadmap commitment as approved unless the user says it is.
5. **Requirements say what, not how.** Leave the design to engineering unless the user fixed it.
6. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
   approve. Neither the Advisor nor the Principal stamps, certifies, attests, dispositions, accepts a risk or
   signs off safety - whatever the request asks for. A Principal review means "consistent with the Stage 1
   criteria and the evidence", and nothing more.

## Principal and escalation

**One boss.** The Advisor (VP Product) plans and runs the job. The Principal
(Chief Product Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The target customer or the problem is unclear enough that two different products would both fit, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release review - every Standard-size job, before Stage 5 delivers.
6. The request conflicts with an existing roadmap commitment or needs a price outside current policy.

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
- **gated**: stop after Brief and after Define for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the target customer or the problem is unclear enough that two different products would both fit;
- a source the request depends on (customer spec, market data, existing PRD) cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Brief (HW: Hardware Product Manager / SW: Software Product Manager)

Turn the request into a product brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Problem and customer** - who has the problem, how they handle it today, and the evidence it is real.
- **Outcome** - what the customer can do once this ships, and how success is measured.
- **Done when** - 3 to 7 criteria, each checkable by reading the PRD against the request. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - target cost or price, standards and certifications, dependencies, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: collect the ratings, standards, certifications and target cost the request names.
- Software track: collect the users, workflows, integrations and data the request names.
- Change work: before writing this, read the current PRD, spec and roadmap entry and add **Must not break** -
  requirements, interfaces and customer commitments this must keep.

Handoff: the product brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Define (HW: Product Line Manager / SW: Technical PM)

Two short pieces of work. Settle the must-have versus later split first.

### Design branch

Decide whether the request needs a new form factor or interface concept settled before requirements can be written, then branch:

| Situation | What to do |
|---|---|
| No new form factor or interface is involved | Skip. |
| A small change to an existing enclosure or screen | No branch. Describe it in two or three lines and move on. |
| The request needs a new form factor or interface concept settled before requirements can be written | Run **jrs:design-hw (Hardware) or jrs:design-sw (Software)**. |

When branching, read the the jrs:design-hw or jrs:design-sw skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the design concept - not
  every stage by reflex.

The branch returns the design concept and its own verdict. Record both, then continue. If
the jrs:design-hw or jrs:design-sw is not installed, do it inline - describe the concept in one short paragraph - and log
`the jrs:design-hw or jrs:design-sw NOT AVAILABLE` in the open items.

### Requirements plan

Keep it to what Stage 3 needs to start:

- **Approach** - the smallest product that delivers the outcome. Change work: reuse what exists before adding anything new.
- **Priorities** - must / should / later for each requirement, with the reason.
- **Requirement list** - the sections and requirements the PRD will contain. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - must-haves first; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the design concept (if branched) plus the requirements plan.

## Stage 3 - Write (Product Owner)

Write the PRD in the order planned. Get the must-have requirements complete first, then widen it.

- Hardware track: write requirements as measurable specs with units and the governing standard.
- Software track: write requirements as user stories with acceptance criteria.
- Change work: stay inside the requirement list and match existing conventions.
- Work against the design concept when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the PRD draft, in a usable state.

## Stage 4 - Verify (Portfolio Manager)

Check what was produced against the product brief, by reading it line by line against the brief and its sources.

1. Check every **Done when** criterion and record the evidence: the source or assumption behind each requirement, gaps, conflicts.
2. Hardware track: every spec has a unit, a value or `TBD`, and a verification method.
3. Software track: every story has acceptance criteria a tester could run.
4. Change work: check every **Must not break** item still holds.
5. If the branch ran, check the result against the design concept.
6. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Release (Product Operations Analyst)

Hand it over in a state the user can use immediately.

- Deliver the PRD and a roadmap entry, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | the jrs:design-hw or jrs:design-sw stages x-y, verdict>
PRINCIPAL REVIEW: <not used (Small) | n rulings, release review: consistent / consistent with conditions / not consistent | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:product-management
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Brief
Problem and customer:
Outcome:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Define
Branch: not needed | inline | the jrs:design-hw or jrs:design-sw stages x-y -> <run folder>, verdict
Approach:
Priorities:
Requirement list:
Order:
Risks:

## 3. Write log
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
