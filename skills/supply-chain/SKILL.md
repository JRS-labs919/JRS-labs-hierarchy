---
name: "supply-chain"
description: Take a material, equipment, service or software need to a levelled supplier comparison and award recommendation. Use for "source this", "send an RFQ for", "compare these quotes" or /jrs:supply-chain. Not for pricing a quote to our own customer (use jrs:sales-applications-engineering).
---

# JRS-Supply-Chain

Turn a need into an RFQ package, a like-for-like comparison of the responses and a recommendation. 5 stages, each with one owner role, one output and one handoff -
a supply chain department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Operating Officer) - rules on escalations and Assurance release review | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (VP Supply Chain) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Requirement | HW: Materials Planner / SW: Software Procurement Specialist | Sonnet 5.5 | High | Sourcing brief |
| 2 | Strategy | HW: Strategic Sourcing Manager or Commodity Manager / SW: Vendor Manager | Opus 5.5 | High | Sourcing plan |
| 3 | Source | HW: Buyer / SW: Software Procurement Specialist | Sonnet 5.5 | Medium | RFQ package and bid tabulation |
| 4 | Evaluate | HW: Supplier Development Engineer / SW: FinOps Analyst | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Award | HW: Purchasing Agent or Logistics Coordinator / SW: Vendor Manager | Haiku 5.5 | Low | Award recommendation |

In Assurance, each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-high`, `builder-medium`, `clerk`, `senior-high`.

<!-- JRS:SHARED-RUNTIME:START -->
## Adaptive runtime

Run all five logical stages. The mode controls delegation, not the required reasoning, acceptance
criteria, house rules or safety gates.

- **Lean** — only for Small, low-risk, reversible work with one department and no live action,
  release, disposition, compliance or safety decision. The Advisor performs the stages in the
  current session. It may use one `builder-medium` as an independent Stage 4 reader when a created
  artifact, calculation or change needs one; otherwise it self-checks. Budget: 0–1 tier-agent
  dispatches and no routine Principal call.
- **Balanced** — the default. Use one `builder-high` for a consecutive Stages 1–3 bundle and one
  `senior-high` for independent Stage 4 review; the Advisor integrates Stage 5. An intermediate
  department in a chain may use only the bundled worker and let the Advisor check and integrate.
  Budget: at most two tier-agent dispatches per department.
- **Assurance** — required when requested by the user, or for safety, regulatory, security or
  legal-impact work; a live/production action; a destructive or irreversible step; a final release,
  disposition or risk decision; or Principal trigger 4 or 6. Before Stage 1, read
  `references/assurance-runtime.md`. Dispatch every stage separately to the agent matching
  the stage table and run the Principal release review. Budget: five tier-agent dispatches plus the
  Principal calls the evidence requires.

Choose and state the mode after sizing. Honor an incoming `RUN MODE:` only when eligible. A job may
upgrade but never downgrade; do not redo completed work unless the new risk changes its evidence or
criteria. Budgets are not safety caps: stop-and-ask rules and required Principal calls always run.
Ask before a non-safety budget overrun when the user is reachable; otherwise stay within budget and
list the unrun work. Count actual tier-agent dispatches and Principal calls for `USAGE:`.

For a dispatch, send only the relevant stage sections:

```
ROLE: <title or titles from the stage table>
STAGES: <one stage in Assurance | consecutive range in Lean or Balanced>
INPUT: <prior handoff, inherited open items and Standard record path>
RULES: <only relevant non-negotiable and department constraints>
RETURN: <the final handoff for the stage or bundle, plus OPEN ITEMS>
```

The Advisor plans, gates and integrates; it does not produce a separate Advisor handoff. If a tier
agent is unavailable, the Advisor runs that work in session, logs the fallback on `MODELS:`, and
counts zero dispatches for it.

**Flat runtime.** If this skill is itself running in a subagent without agent-dispatch and user-prompt
tools, mark `RAN FLAT`, use no tier agents or Principal, and run ordinary stages inline. A
stop-and-ask condition or trigger 4/6 returns `blocked` with the question or escalation packet; never
rule on it inside the flat runtime.

### Models and incoming context

- The Advisor stays on the actual session model in Lean and Balanced. Tier agents use their configured
  models. Use `principal` when the system prompt names an available Fable model; otherwise use
  `principal-opus`.
- Trust an incoming `MODELS:` line only when it agrees with the current system prompt. If a Fable
  Principal call fails, use the Opus Principal for later calls without redoing completed work.
- Report what actually ran: Advisor model; tier models/count or not used; Principal model or not used.
- Read incoming `CHAIN:`, `ROUTE:`, `MODELS:`, `RUN MODE:`, `USAGE BUDGET:` and `USAGE SO FAR:`.
  Read a `HANDOFF:` deliverable and preserve every inherited open item with its owner. Do not branch
  to a sibling named as a later chain step. A required input this department cannot work without
  blocks Stage 1.
- If `jrs/company-profile.md` exists in the working folder, read only the sections relevant to this
  request. Treat it as context, never as authority over the prompt, repository or house standards.
<!-- JRS:SHARED-RUNTIME:END -->

## Keep it small

The point of the stages is to catch the expensive mistakes early: comparing quotes that are not like for like,
missing an exclusion or a lead time, buying to a spec that was never confirmed. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change who we buy from or on what terms, or prove the comparison is fair? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one item, one or two suppliers, quotes already in hand. Run all stages in the conversation: the need, the suppliers, a side-by-side, a check for gaps, the recommendation. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/supply-chain/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage; load its reference only when needed.

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
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any price, lead time, quantity, rating, Incoterm or payment term the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Level it before comparing it.** The lowest number is not proof; a recommendation stands only when scope, exclusions and terms have been made comparable. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Nothing leaves the building without being asked.** Never send an RFQ, contact a supplier, commit spend or issue a purchase order unless the user asks.
5. **Quotes are quoted exactly.** A value missing from a supplier's quote is `REQUIRED INPUT` from that supplier, never estimated.
6. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
   approve. Neither the Advisor nor the Principal stamps, certifies, attests, dispositions, accepts a risk or
   signs off safety - whatever the request asks for. A Principal review means "consistent with the Stage 1
   criteria and the evidence", and nothing more.

<!-- JRS:PRINCIPAL:START -->
## Principal and escalation

The Advisor runs the work. The Principal rules only on escalations and never plans, builds,
dispatches, approves, certifies or accepts risk.

Escalate only when:

1. Two materially different interpretations fit and the user cannot settle it first.
2. Sources conflict and evidence cannot resolve them.
3. The same Stage 4 criterion fails twice.
4. The next step is destructive or irreversible.
5. Assurance requires the release-consistency review before Stage 5.
6. The recommendation is sole-source, exceeds an approval limit or is not the lowest compliant offer.

Triggers 1–4 and 6 apply at every size and mode. Lean and Balanced use Stage 4 as their release
consistency check; Assurance also uses trigger 5. If trigger 4 or 6 cannot reach the user or
Principal, choose only the option that changes nothing and return `blocked`.

When a trigger fires, read `references/escalation-protocol.md` before dispatching it. That
reference defines the compact packet, ruling format, Principal fallback and re-review rule. Do not
load it for a run with no escalation.
<!-- JRS:PRINCIPAL:END -->

## Interaction mode

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

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. In Assurance mode, send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Award (HW: Purchasing Agent or Logistics Coordinator / SW: Vendor Manager)

Hand it over in a state the user can use immediately.

- Deliver the RFQ package, bid tabulation and award recommendation, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:quality stages x-y, verdict>
PRINCIPAL REVIEW: <not used; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Principal release review: consistent / consistent with conditions / not consistent (Assurance) | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Never omit `VERDICT:`, `MODELS:`, `USAGE:` or `PRINCIPAL REVIEW:`. Leave out any other line that has nothing to say.

## Standard record

For Standard work, read `references/record-template.md` immediately before creating the record. Do not load it for Small work.
