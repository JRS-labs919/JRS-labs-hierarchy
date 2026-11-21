---
name: "software-engineering"
description: Take a feature request, bug or change to working, tested code ready to ship. Use for "build this feature", "fix this bug", "add an endpoint for" or /jrs:software-engineering. Not for deployment and infrastructure changes (use jrs:platform-infrastructure).
---

# JRS-Software-Engineering

Turn a request into code that passes its tests and is ready for review and release. 5 stages, each with one owner role, one output and one handoff -
a software engineering team with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Technology Officer) - rules on escalations and Assurance release review | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (VP Software Engineering) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Spec | Tech Lead | Opus 5.5 | High | Technical brief |
| 2 | Design | Software Architect / Staff Engineer | Opus 5.5 | High | Technical plan |
| 3 | Build | Software Engineer (Frontend / Backend / Mobile) | Sonnet 5.5 | Medium | Working code and tests |
| 4 | Test | SDET / QA Engineer | Opus 5.5 | Medium | Pass/fail per criterion |
| 5 | Ship | Software Engineer | Sonnet 5.5 | Low | Change ready to merge |

In Assurance, each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-low`, `builder-medium`, `senior-high`, `senior-medium`.

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

The point of the stages is to catch the expensive mistakes early: building the wrong behaviour,
a change that breaks something it did not mean to touch, code that was never actually run. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change what the code does, or prove that it works? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - a change to one or two files with no schema or interface change. Run all stages in the conversation: the behaviour in a few lines, the approach, the change, a run of the tests, the handoff. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/software-engineering/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage; load its reference only when needed.

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Application** - frontend, backend or mobile product code. Read the existing module, its tests and its conventions.
- **Integrations** - APIs and connections to other systems. Read the contract of the system on the other side.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - coding standard, branching model, review rule or test policy -
   is followed and noted in the technical brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any API field, endpoint, schema, credential or performance figure the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Run it before calling it done.** Code that reads correctly is not proof; a criterion passes on test output, a run log or a reproduced fix. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Nothing irreversible without being asked.** Never push to a protected branch, run a migration, delete data or change production unless the user asks.
5. **Secrets stay out of code.** Never write a key, token or password into a file, log or commit.
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
6. The change touches authentication, authorisation, secrets, payments, personal data or a safety-related function.

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
- **gated**: stop after Spec and after Design for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the expected behaviour is unclear enough that two different implementations would both fit;
- the repository, a dependency or a required credential is not available;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Spec (Tech Lead)

Turn the request into a technical brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Behaviour** - what the code must do, in observable terms.
- **Interfaces** - inputs, outputs, APIs and data touched.
- **Done when** - 3 to 7 criteria, each checkable by a test or a run. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - language and framework, performance, compatibility, security, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Application track: read the existing module, its tests and its conventions.
- Integrations track: read the contract of the system on the other side.
- Change work: before writing this, read the code, tests and recent history of the area and add **Must not break** -
  public interfaces, existing tests and behaviour callers rely on.

Handoff: the technical brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Design (Software Architect / Staff Engineer)

Two short pieces of work. Settle the interface or data-model decision first.

### UI branch

Decide whether a user interface has to be created or reworked, then branch:

| Situation | What to do |
|---|---|
| There is no user interface | Skip. |
| One field, label or button on an existing screen | No branch. Describe it in two or three lines and move on. |
| A user interface has to be created or reworked | Run **jrs:design-sw**. |

When branching, read the jrs:design-sw skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the design spec - not
  every stage by reflex.

The branch returns the design spec and its own verdict. Record both, then continue. If
jrs:design-sw is not installed, do it inline - describe the screen and its states in a few lines - and log
`jrs:design-sw NOT AVAILABLE` in the open items.

### Technical plan

Keep it to what Stage 3 needs to start:

- **Approach** - the smallest change that delivers the behaviour, following existing patterns. Change work: reuse what exists before adding anything new.
- **Tests** - the tests that will prove each criterion.
- **Change list** - the files and modules this job touches. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - the thinnest end-to-end slice first; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the design spec (if branched) plus the technical plan.

## Stage 3 - Build (Software Engineer (Frontend / Backend / Mobile))

Write the code and tests in the order planned. Get one end-to-end slice complete first, then widen it.

- Application track: write the test alongside the change.
- Integrations track: code against the published contract; never guess a field or endpoint.
- Change work: stay inside the change list and match existing conventions.
- Work against the design spec when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the working code and tests, in a usable state.

## Stage 4 - Test (SDET / QA Engineer)

Check what was produced against the technical brief, by running the tests and the code.

1. Check every **Done when** criterion and record the evidence: test output, run logs, before-and-after behaviour.
2. Application track: the acceptance tests ran and passed, with output shown.
3. Integrations track: the integration is exercised against a real or recorded response.
4. Change work: check every **Must not break** item still holds.
5. If the branch ran, check the result against the design spec.
6. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. In Assurance mode, send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Ship (Software Engineer)

Hand it over in a state the user can use immediately.

- Deliver the code change with tests and a change summary, in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:design-sw stages x-y, verdict>
PRINCIPAL REVIEW: <not used; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Principal release review: consistent / consistent with conditions / not consistent (Assurance) | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Never omit `VERDICT:`, `MODELS:`, `USAGE:` or `PRINCIPAL REVIEW:`. Leave out any other line that has nothing to say.

## Standard record

For Standard work, read `references/record-template.md` immediately before creating the record. Do not load it for Small work.
