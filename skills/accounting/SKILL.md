---
name: "accounting"
description: Take a transaction, close task or accounting question to a reviewed, posting-ready workpaper with the treatment stated. Use for "reconcile this account", "how do we account for", "prepare the journal entry" or /jrs:accounting. Not for forecasts, budgets and pricing analysis (use jrs:fpa).
---

# JRS-Accounting

Turn an accounting question into entries and schedules that tie out, with the policy behind them on the page. 5 stages, each with one owner role, one output and one handoff -
an accounting department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Financial Officer) - rules on escalations, final sign-off (Standard size) | Fable 5.2 | Max | Rulings and release sign-off |
| - | All | Advisor (Controller) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Intake | HW: AP/AR Specialist / SW: Billing Specialist | Sonnet 5.5 | Medium | Accounting brief |
| 2 | Treatment | HW: Cost Accountant / SW: Revenue Accountant | Opus 5.5 | High | Treatment memo |
| 3 | Prepare | HW: Inventory Accountant / SW: Billing Specialist | Sonnet 5.5 | Medium | Entries and schedules |
| 4 | Review | Tax Manager / second accountant | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Close | AP/AR Specialist | Haiku 5.5 | Low | Posting-ready workpaper |

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

The user is the finance owner. Their prompt, plus anything they attached or pointed
to, **is** the accounting request. Stage 1's job is to turn it into the accounting brief, not to send
it back as a questionnaire.

## Keep it small

The point of the stages is to catch the expensive mistakes early: the wrong treatment applied consistently,
a schedule that does not tie to the ledger, an entry in the wrong period. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change a number, a period or a treatment, or prove the numbers tie? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one reconciliation or one entry with clear support. Run all stages in the conversation: the item, the treatment, the entry, a tie-out, the handoff. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/accounting/<slug>.md`, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - product cost, inventory, work in progress and project accounting. Collect the cost records, quantities, bills of material and the period.
- **Software** - subscription revenue, deferred revenue and billing. Collect the contract, term, billing schedule and what was delivered when.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - accounting policy, chart of accounts, close calendar or approval matrix -
   is followed and noted in the accounting brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them. This skill fills gaps only.
2. **Never invent facts.** Any amount, rate, date, account or contract term the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Tie it out.** An entry that balances is not proof; a criterion passes when the schedule ties to the ledger and to source documents. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Prepare, never post.** Never post an entry, release a payment, issue an invoice or file a return unless the user asks.
5. **State the policy.** Each treatment names the policy or standard it follows; if the policy is unknown it is `REQUIRED INPUT`.
6. **This is preparation, not professional advice.** Tax and audit conclusions belong to the qualified owner.

## Principal and escalation

**One boss.** The Advisor (Controller) plans and runs the job. The Principal
(Chief Financial Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The transaction's facts are unclear enough that two different treatments would both fit, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release sign-off - every Standard-size job, before Stage 5 delivers.
6. The treatment is a judgement call, a change in policy or material to the period.

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
- **gated**: stop after Intake and after Treatment for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the transaction's facts are unclear enough that two different treatments would both fit;
- the ledger, contract or supporting documents cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Intake (HW: AP/AR Specialist / SW: Billing Specialist)

Turn the request into an accounting brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Item and period** - what happened, the amounts and the period it belongs to.
- **Support** - the documents that evidence it.
- **Done when** - 3 to 7 criteria, each checkable by tie-out to the ledger or a source document. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - policy, period cut-off, materiality, approval limits, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: collect the cost records, quantities, bills of material and the period.
- Software track: collect the contract, term, billing schedule and what was delivered when.
- Change work: before writing this, read the prior-period workpaper and treatment and add **Must not break** -
  closed periods, prior treatments and approved balances.

Handoff: the accounting brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Treatment (HW: Cost Accountant / SW: Revenue Accountant)

One short piece of work. Settle the treatment first.

### Treatment memo

Keep it to what Stage 3 needs to start:

- **Approach** - follow existing policy; a departure is named and escalated. Change work: reuse what exists before adding anything new.
- **Policy basis** - the policy or standard applied and why it fits.
- **Account list** - the accounts and periods this job touches. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - the largest amounts first; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the treatment memo.

## Stage 3 - Prepare (HW: Inventory Accountant / SW: Billing Specialist)

Prepare the entries and schedules in the order planned. Get the largest item, end to end complete first, then widen it.

- Hardware track: show the cost build-up and the basis for every allocation.
- Software track: show the recognition schedule by period and the contract terms that drive it.
- Change work: stay inside the account list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the entries and schedules, in a usable state.

## Stage 4 - Review (Tax Manager / second accountant)

Check what was produced against the accounting brief, by recomputing and tying every schedule to the ledger and source documents.

1. Check every **Done when** criterion and record the evidence: tie-out totals, recomputations, document references.
2. Hardware track: quantities and values tie to the sub-ledger and the ledger.
3. Software track: the schedule ties to the contract value and to billings.
4. Change work: check every **Must not break** item still holds.
5. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Close (AP/AR Specialist)

Hand it over in a state the user can use immediately.

- Deliver the workpaper (treatment, entries, schedules, tie-out), in the form the user asked for or house rules require.
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
# <Name> - jrs:accounting
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Intake
Item and period:
Support:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Treatment
Approach:
Policy basis:
Account list:
Order:
Risks:

## 3. Prepare log
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
