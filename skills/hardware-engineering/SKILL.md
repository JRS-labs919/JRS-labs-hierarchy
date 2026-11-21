---
name: "hardware-engineering"
description: Take a requirement, spec or change request for a physical product to a verified design package ready for release. Use for "design this", "size this", "run the calc for" or /jrs:hardware-engineering. Not for application code (use jrs:software-engineering).
---

# JRS-Hardware-Engineering

Turn a requirement into drawings, calculations and a BOM that have been checked before release. 5 stages, each with one owner role, one output and one handoff -
a hardware engineering department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Technology Officer) - rules on escalations and Assurance release review | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (VP Hardware Engineering) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Design Basis | Principal Engineer (Mechanical / Electrical / Controls) | Opus 5.5 | High | Design basis |
| 2 | Plan | Senior Engineer of the lead discipline | Opus 5.5 | High | Design plan |
| 3 | Design | Design Engineer / CAD Designer / Firmware Engineer | Sonnet 5.5 | Medium | Design package draft |
| 4 | Verify | Test Engineer / Validation Engineer | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Release | Drafter | Haiku 5.5 | Low | Release package |

In Assurance, each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-medium`, `clerk`, `senior-high`.

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

The point of the stages is to catch the expensive mistakes early: designing to the wrong rating or standard,
a calculation built on an unsourced input, a change that breaks fit, form or function elsewhere. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change the design, or prove it meets the requirement? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one calculation, one part selection or a single-drawing change. Run all stages in the conversation: the inputs and standard, the method, the result, an independent check, the handoff. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/hardware-engineering/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage; load its reference only when needed.

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Mechanical** - structure, enclosure, thermal or layout. Collect loads, envelope, environment and the governing standard.
- **Electrical** - power, protection, grounding or wiring. Collect voltage, current, fault duty, ratings and the governing code.
- **Controls & Embedded** - control logic, PLC, firmware or PCB. Collect the I/O list, sequences, interlocks and fail-safe states.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - drawing standard, part numbering scheme, design guide or approved-parts list -
   is followed and noted in the design basis. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any rating, dimension, load, tolerance, setting or part number the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Check it by a second route.** The designer re-reading their own work is not proof; a result is verified by an independent calculation, a test or a cited source. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Safety functions are never traded away.** Removing or weakening a protection, interlock, clearance or
   safety or rating margin is never done because the user asks alone. It always fires trigger 6, and the
   skill only drafts the change request and the risk-assessment inputs for the responsible engineer and the
   safety owner to decide (each named by the user, or `REQUIRED INPUT`).
5. **Cite the standard and clause.** A requirement taken from a code names the edition; if the edition is unknown it is `REQUIRED INPUT`.
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
6. A design decision affects safety, a certification or a rating margin.

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
- **gated**: stop after Design Basis and after Plan for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the governing standard, rating or duty is unclear enough that two different designs would both fit;
- the spec, existing drawings or source datasheets cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Design Basis (Principal Engineer (Mechanical / Electrical / Controls))

Turn the request into a design basis. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Requirements** - ratings, duty, environment and interfaces, each with its source.
- **Standards** - the codes and standards that govern, with edition and the clauses relied on, on every
  track. A standard or edition that is not known stays `REQUIRED INPUT`; do not assume one.
- **Done when** - 3 to 7 criteria, each checkable by calculation, test or drawing review. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - standards, approved parts, cost target, manufacturing process, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Mechanical track: collect loads, envelope, environment and the governing standard.
- Electrical track: collect voltage, current, fault duty, ratings and the governing code.
- Controls & Embedded track: collect the I/O list, sequences, interlocks and fail-safe states.
- Change work: before writing this, read the released drawings, BOM and change history and add **Must not break** -
  fit, form, function, certifications and interfaces other parts depend on.

Handoff: the design basis. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Plan (Senior Engineer of the lead discipline)

Two short pieces of work. Settle the architecture and the governing calculation first.

### Systems branch

Decide whether the design has a software, firmware or communications interface that is not yet defined, then branch:

| Situation | What to do |
|---|---|
| The design has no software or communications interface | Skip. |
| The interface is an existing, documented signal list | No branch. Describe it in two or three lines and move on. |
| The design has a software, firmware or communications interface that is not yet defined | Run **jrs:systems-engineering**. |

When branching, read the jrs:systems-engineering skill and follow it as written. Give it:

- the Stage 1 output as its input, so it does not rediscover what is already decided;
- the same mode (autonomous or gated);
- the **narrowest stage range that answers the need**, ending at the interface definition - not
  every stage by reflex.

The branch returns the interface definition and its own verdict. Record both, then continue. If
jrs:systems-engineering is not installed, do it inline - list each signal with direction, type and owner - and log
`jrs:systems-engineering NOT AVAILABLE` in the open items.

### Design plan

Keep it to what Stage 3 needs to start:

- **Approach** - the simplest design that meets the basis, using approved parts first. Change work: reuse what exists before adding anything new.
- **Calculation list** - each calc, its method and the inputs it needs. Include tolerance stack or fit,
  thermal, fatigue or margin, and manufacturability checks where they apply.
- **Hazards and failure modes** - every track: list how the design can fail or be misused, the effect and
  the mitigation. Any method will do (FMEA is one example). A hazard with no mitigation is an open item and
  fires trigger 6.
- **Document list** - the drawings, BOM lines and calcs this job creates or changes. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - governing calculation first, then layout, then detail; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the interface definition (if branched) plus the design plan.

## Stage 3 - Design (Design Engineer / CAD Designer / Firmware Engineer)

Produce the design in the order planned. Get the governing calculation and the top-level drawing complete first, then widen it.

- Mechanical track: state each calculation's method, inputs and source; model geometry only from sourced dimensions.
- Electrical track: show every rating and its source on the one-line, schedule or calc.
- Controls & Embedded track: write the sequence of operations before any logic.
- Change work: stay inside the document list and match existing conventions.
- Work against the interface definition when the branch ran.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the design package draft, in a usable state.

## Stage 4 - Verify (Test Engineer / Validation Engineer)

Check what was produced against the design basis, by independent calculation, test or design review.

1. Check every **Done when** criterion and record the evidence: check calcs, test results, review comments, source citations.
2. Calculation checks are re-derived independently - by a different method or a script shown in the
   record, not by repeating the same arithmetic.
3. Physical tests cannot be run here. A criterion that needs one is reported `NOT RUN - test plan
   provided`, and the test plan (method, set-up, acceptance limits) is the deliverable. Results the user
   supplies are checked against it.
4. Every track: each requirement taken from a standard is matched to the clause cited, edition stated.
   A standard or edition that is not known stays `REQUIRED INPUT`.
5. Every listed hazard has a mitigation and a verification; one missing either fails.
6. Mechanical track: each result is re-derived or cross-checked by a second method.
7. Electrical track: ratings, protection settings and conductor sizes are checked against the code clause cited.
8. Controls & Embedded track: every interlock and fail-safe state is tested or traced.
9. Change work: check every **Must not break** item still holds.
10. If the branch ran, check the result against the interface definition.
11. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
    fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. A pass means the package is
ready for a qualified engineer's approval, not that it is approved or released. In Assurance mode, send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Release (Drafter)

Hand it over in a state the user can use immediately.

- Deliver the design package (drawings, calcs, BOM, open items), in the form the user asked for or house rules require.
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
BRANCH: <not needed | inline | jrs:systems-engineering stages x-y, verdict>
PRINCIPAL REVIEW: <not used; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Principal release review: consistent / consistent with conditions / not consistent (Assurance) | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Never omit `VERDICT:`, `MODELS:`, `USAGE:` or `PRINCIPAL REVIEW:`. Leave out any other line that has nothing to say.

## Standard record

For Standard work, read `references/record-template.md` immediately before creating the record. Do not load it for Small work.
