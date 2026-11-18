---
name: "supply-chain"
description: Take a material, equipment, service or software need to a levelled supplier comparison and award recommendation. Use for "source this", "send an RFQ for", "compare these quotes" or /jrs:supply-chain. Not for pricing a quote to our own customer (use jrs:sales-applications-engineering).
---

# JRS-Supply-Chain

Turn a need into an RFQ package, a like-for-like comparison of the responses and a recommendation. 5 stages, each with one owner role, one output and one handoff -
a supply chain department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations, final sign-off (Standard size) | Fable 5.2 | Max | Rulings and release sign-off |
| - | All | Advisor (VP Supply Chain) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Requirement | HW: Materials Planner / SW: Software Procurement Specialist | Sonnet 5.5 | High | Sourcing brief |
| 2 | Strategy | HW: Strategic Sourcing Manager or Commodity Manager / SW: Vendor Manager | Opus 5.5 | High | Sourcing plan |
| 3 | Source | HW: Buyer / SW: Software Procurement Specialist | Sonnet 5.5 | Medium | RFQ package and bid tabulation |
| 4 | Evaluate | HW: Supplier Development Engineer / SW: FinOps Analyst | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Award | HW: Purchasing Agent or Logistics Coordinator / SW: Vendor Manager | Haiku 5.5 | Low | Award recommendation |

Each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-high`, `builder-medium`, `clerk`, `senior-high`.

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

The user is the internal requester (a project, engineering or manufacturing). Their prompt, plus anything they attached or pointed
to, **is** the purchase request. Stage 1's job is to turn it into the sourcing brief, not to send
it back as a questionnaire.

## Keep it small

The point of the stages is to catch the expensive mistakes early: comparing quotes that are not like for like,
missing an exclusion or a lead time, buying to a spec that was never confirmed. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change who we buy from or on what terms, or prove the comparison is fair? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one item, one or two suppliers, quotes already in hand. Run all stages in the conversation: the need, the suppliers, a side-by-side, a check for gaps, the recommendation. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/supply-chain/<slug>.md`, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - materials, components, equipment and freight. Collect the spec, quantity, need date, delivery point and approved suppliers.
- **Software** - cloud services, licenses and third-party tools. Collect the users, usage, term, data handled and current spend.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - approved supplier list, purchasing policy, approval limits or standard terms -
   is followed and noted in the sourcing brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them. This skill fills gaps only.
2. **Never invent facts.** Any price, lead time, quantity, rating, Incoterm or payment term the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Level it before comparing it.** The lowest number is not proof; a recommendation stands only when scope, exclusions and terms have been made comparable. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Nothing leaves the building without being asked.** Never send an RFQ, contact a supplier, commit spend or issue a purchase order unless the user asks.
5. **Quotes are quoted exactly.** A value missing from a supplier's quote is `REQUIRED INPUT` from that supplier, never estimated.

## Principal and escalation

**One boss.** The Advisor (VP Supply Chain) plans and runs the job. The Principal
(Chief Operating Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The spec, quantity or need date is unclear enough that suppliers would quote different things, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release sign-off - every Standard-size job, before Stage 5 delivers.
6. The recommendation is sole-source, exceeds an approval limit or is not the lowest compliant offer.

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
- **gated**: stop after Requirement and after Strategy for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the spec, quantity or need date is unclear enough that suppliers would quote different things;
- the spec or the supplier quotes cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Requirement (HW: Materials Planner / SW: Software Procurement Specialist)

Turn the request into a sourcing brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Need** - what, how many, to what spec, delivered where and when.
- **Evaluation basis** - what the award is judged on and the weighting if given.
- **Done when** - 3 to 7 criteria, each checkable by tracing a value to the quote or recomputing a total. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - budget, approved suppliers, lead time, terms, compliance, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: collect the spec, quantity, need date, delivery point and approved suppliers.
- Software track: collect the users, usage, term, data handled and current spend.
- Change work: before writing this, read the current supplier, contract, price and performance history and add **Must not break** -
  existing contracts, committed deliveries and qualified sources.

Handoff: the sourcing brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Strategy (HW: Strategic Sourcing Manager or Commodity Manager / SW: Vendor Manager)

Two short pieces of work. Settle who gets asked and on what basis first.

### Quality branch

Decide whether a supplier or part is new and has not been qualified, then branch:

| Situation | What to do |
|---|---|
| All bidders and parts are already qualified | Skip. |
| A qualified supplier offers a listed alternate | No branch. Describe it in two or three lines and move on. |
| A supplier or part is new and has not been qualified | Run **jrs:quality**. |

When branching, read the jrs:quality skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the qualification requirements - not
  every stage by reflex.

The branch returns the qualification requirements and its own verdict. Record both, then continue. If
jrs:quality is not installed, do it inline - list the certificates, tests and audits to request - and log
`jrs:quality NOT AVAILABLE` in the open items.

### Sourcing plan

Keep it to what Stage 3 needs to start:

- **Approach** - competitive where possible; sole-source needs a stated reason. Change work: reuse what exists before adding anything new.
- **Bidder list** - each supplier and why they are included.
- **Scope of supply** - the line items and services the RFQ covers. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - longest-lead and highest-value lines first; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the qualification requirements (if branched) plus the sourcing plan.

## Stage 3 - Source (HW: Buyer / SW: Software Procurement Specialist)

Build the RFQ package and tabulate the responses in the order planned. Get the RFQ scope and one supplier's tabulation complete first, then widen it.

- Hardware track: tabulate price, lead time, Incoterms, warranty, exceptions and validity for every bidder.
- Software track: tabulate unit price, term, usage tiers, renewal terms, support and exit terms.
- Change work: stay inside the scope of supply and match existing conventions.
- Work against the qualification requirements when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the RFQ package and bid tabulation, in a usable state.

## Stage 4 - Evaluate (HW: Supplier Development Engineer / SW: FinOps Analyst)

Check what was produced against the sourcing brief, by tracing every value to the quote and levelling scope, exclusions and terms.

1. Check every **Done when** criterion and record the evidence: quote page references, levelling adjustments, gaps per bidder.
2. Hardware track: every tabulated value traces to a page of the supplier's quote.
3. Software track: totals are recomputed from the supplier's stated rates and usage.
4. Change work: check every **Must not break** item still holds.
5. If the branch ran, check the result against the qualification requirements.
6. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Award (HW: Purchasing Agent or Logistics Coordinator / SW: Vendor Manager)

Hand it over in a state the user can use immediately.

- Deliver the RFQ package, bid tabulation and award recommendation, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:quality stages x-y, verdict>
PRINCIPAL: <not used (Small) | n rulings, sign-off: approved / approved with conditions / rejected>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.

## Record template (Standard size only)

```markdown
# <Name> - jrs:supply-chain
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Requirement
Need:
Evaluation basis:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Strategy
Branch: not needed | inline | jrs:quality stages x-y -> <run folder>, verdict
Approach:
Bidder list:
Scope of supply:
Order:
Risks:

## 3. Source log
- <step> - <status> - <plan changes, if any>

## 4. Evaluate
| Criterion | Result | Evidence |
|---|---|---|

## Escalations
| # | Trigger | Question | Ruling | Conditions |
|---|---|---|---|---|

## 5. Open items
| # | Item | Type (TBD / REQUIRED INPUT / NOT RUN / discrepancy) | Owner |
|---|---|---|---|
```
