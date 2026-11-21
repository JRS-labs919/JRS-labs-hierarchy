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

In Assurance, each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-medium`, `clerk`, `senior-high`.

## Adaptive usage

Complete all five logical stages in every mode. The mode changes who performs consecutive stages and
how many tier agents are dispatched; it never removes a ground rule, acceptance criterion or safety
gate.

- **Lean** - only for Small, low-risk, reversible work that touches no live system and makes no
  release, disposition, compliance or safety decision. The Advisor runs Stages 1-3 and Stage 5 in the
  session. It may dispatch one `builder-medium` as the independent Stage 4 reader when the work
  creates a file, calculation or change; otherwise the Advisor performs Stage 4. Target: at most one
  tier-agent dispatch and no routine Principal call.
- **Balanced** - the default. Dispatch one `builder-high` for a consecutive Stages 1-3 bundle and one
  `senior-high` for Stage 4; the Advisor integrates Stage 5 in the session. An intermediate department
  in a Balanced chain may use one `builder-high` for Stages 1-3 and let the Advisor perform the
  independent Stage 4 check and integrate Stage 5. Target: at most two tier-agent dispatches per department.
- **Assurance** - use when the user asks for it, or for safety, regulatory, security or legal-impact
  work; a live or production change; a destructive or irreversible step; a final release,
  disposition or risk decision; or whenever trigger 4 or 6 fires. Dispatch every stage separately to
  the table agent and run the Principal release review. Target: five tier-agent dispatches plus the
  Principal calls the evidence requires.

Choose the mode after sizing and say it before Stage 1. Honor an incoming `RUN MODE:` as the
starting mode only when the job is eligible; an explicit Lean or Balanced request never overrides a
mandatory Assurance upgrade. Once this department starts, its mode may upgrade but never downgrade. In a Balanced chain the router
may assign Lean to an eligible intermediate department before it begins. Small work that grows becomes
Balanced; any Assurance condition upgrades it
immediately, without waiting for permission. Do not redo a completed stage after an upgrade unless the
new risk changes its evidence or acceptance criteria.

The targets are usage budgets, not safety caps. A stop-and-ask rule or Principal trigger always runs
even when it exceeds a target. Before exceeding the target for a non-safety reason, ask the user if
reachable; otherwise stay within the target and report the unrun work under `OPEN ITEMS`. Count every
tier-agent dispatch and Principal call for the final `USAGE:` line.

Send one packet for the listed stage or consecutive bundle, not the conversation:

```
ROLE: <title or titles from the table>
STAGES: <one stage in Assurance | consecutive range in Lean or Balanced>, with only those sections
INPUT: <the prior handoff, inherited open items and record path if Standard>
RULES: <only the non-negotiable ground rules and department constraints relevant to this work>
RETURN: <the final handoff for the listed stage or bundle, plus OPEN ITEMS>
```

The Advisor plans, gates and integrates; it does not create a separate handoff for its own row. The
Principal is consulted only through the escalation protocol below. If a required tier agent is not
available, the Advisor runs that work in the session and logs `<role> model/effort NOT SET - ran in
session`; it still counts that fallback accurately on `USAGE:` as zero tier-agent dispatches.

**Running inside a subagent.** If you have no tool to dispatch agents and none to ask the user, you are
running flat: no tier agents, no Principal, and the user cannot be reached. Say so on the report's
`MODELS:` line (`- RAN FLAT`). Run the stages yourself. But when a stop-and-ask condition, trigger 4 or
the risk trigger (trigger 6) applies, stop there and return `blocked`, with the questions or the
escalation packet for your caller to act on. Do not rule on it yourself.

### Model policy

- **Advisor stays in the session.** Lean and Balanced never require a switch to Opus merely because
  the session is not on Fable. Use the current session model and report it.
- **Tier agents keep their configured models.** Assurance follows the stage table. Lean and Balanced
  use the bundled-agent choices in Adaptive usage.
- **Principal path.** Use `principal` when the system prompt names a Fable model and Fable is
  available; otherwise use `principal-opus`. A Principal is not called merely to prove that the mode
  is working.
- **Incoming model context.** If the request carries a `MODELS:` line, use it only when it agrees with
  the model named by the current system prompt. Log a mismatch instead of pretending a model ran.
- **Failure partway through.** If a Fable Principal call fails for usage or availability, switch the
  Principal path to Opus for the rest of the job and do not switch back. Do not redo completed work.
- **Say what ran.** The record and report name the Advisor session model, the tier models actually
  dispatched and the Principal model, or `not used`.


The user is the requester (sales, a customer, engineering or leadership). Their prompt, plus anything they attached or pointed
to, **is** the product request. Stage 1's job is to turn it into the product brief, not to send
it back as a questionnaire.

**Router and department handoff.** Read any `CHAIN:`, `ROUTE:`, `MODELS:`, `RUN MODE:`, `USAGE BUDGET:` and `USAGE SO FAR:` lines that accompany
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
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
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
5. Assurance release review - before Stage 5 delivers. Lean and Balanced use Stage 4 as the release consistency check unless another trigger upgrades the job.
6. The request conflicts with an existing roadmap commitment or needs a price outside current policy.

**Release review by mode.** Lean and Balanced use Stage 4 as the release consistency check. Assurance
sends the Principal a trigger-5 release-review packet before Stage 5. Principal triggers 1-4 and 6
remain available in every mode and at every size. Trigger 6 is this skill's risk trigger: it applies at
every size, and so does every stop-and-ask condition.

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

## Interaction mode

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

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. In Assurance mode, send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Release (Product Operations Analyst)

Hand it over in a state the user can use immediately.

- Deliver the PRD and a roadmap entry, in the form the user asked for or house rules require.
- Say how to use it, in as few steps as it takes.
- Change work: say what changed and where.
- List what is still open.

Report bottom line first, in this shape. The final response must contain
this literal fenced report block with the exact uppercase labels; do not replace it with prose or bold headings:

```
VERDICT: <done | done with open items | blocked> - <n>/<n> criteria passed
MODELS: <Advisor session model; tier agents models/count or not used; Principal model or not used> [- RAN FLAT when applicable]
USAGE: <Lean | Balanced | Assurance> - <n tier-agent dispatches; n Principal calls; budget met | exceeded for safety: reason>
DELIVERED: <deliverable and path, one line each>
HOW TO USE: <steps>
CHANGED: <what changed - change work only>
BRANCH: <not needed | inline | the jrs:design-hw or jrs:design-sw stages x-y, verdict>
PRINCIPAL REVIEW: <not used; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Principal release review: consistent / consistent with conditions / not consistent (Assurance) | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Never omit `VERDICT:`, `MODELS:`, `USAGE:` or `PRINCIPAL REVIEW:`. Leave out any other line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:product-management
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Advisor <model>; tier agents <models/count or not used>; Principal <model or not used>
Usage: Lean | Balanced | Assurance - <tier-agent dispatches; Principal calls; budget status>

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
