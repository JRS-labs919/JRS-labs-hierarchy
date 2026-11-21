---
name: "technical-publications"
description: Take a product, feature or procedure that needs documenting to a reviewed manual, guide or reference. Use for "write the manual for", "document this procedure", "write the API docs" or /jrs:technical-publications. Not for marketing collateral and brochures (use jrs:marketing).
---

# JRS-Technical-Publications

Turn engineering sources into documentation where every instruction and value can be traced. 5 stages, each with one owner role, one output and one handoff -
a technical publications team with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Technology Officer) - rules on escalations and Assurance release review | Fable 5.2 | Max | Rulings and release review |
| - | All | Advisor (Technical Publications Manager) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Brief | HW: Technical Writer / SW: Documentation Engineer | Opus 5.5 | Medium | Document brief |
| 2 | Source | HW: Technical Writer / SW: Documentation Engineer | Opus 5.5 | High | Outline and fact sheet |
| 3 | Write | HW: Technical Writer / SW: Documentation Engineer | Sonnet 5.5 | Medium | Draft |
| 4 | Review | HW: Technical Writer (second reader) / SW: Developer Advocate | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Publish | HW: Technical Writer / SW: Documentation Engineer | Haiku 5.5 | Low | Published document |

In Assurance, each delegated role is dispatched to the plugin's tier agent that matches its row: Opus 5.5 rows
to `senior-high` or `senior-medium`, Sonnet 5.5 rows to `builder-high`, `builder-medium` or
`builder-low`, Haiku 5.5 rows to `clerk`, and escalations to `principal`. This skill uses `builder-medium`, `clerk`, `senior-high`, `senior-medium`.

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

The point of the stages is to catch the expensive mistakes early: an instruction that is wrong or out of order,
a value copied from the wrong revision, a document written for the wrong reader. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this help the reader do the task, or prove the content is right? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one procedure, one page or one endpoint. Run all stages in the conversation: the reader and task, the sources, the text, a check against the sources, the handoff. No record file.
  If a Small job needs a file, use the path the user requested; otherwise keep the deliverable in the
  conversation. The department date-and-topic path below is for Standard records only.
- **Standard** - anything larger. Keep one record file, `jrs/technical-publications/<yyyy-mm-dd>-<topic>.md` under the working folder, with one
  section per stage; load its reference only when needed.

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - installation, operation, maintenance and safety manuals. Collect the drawings, datasheets and procedures at their current revision.
- **Software** - user guides, API reference and release notes. Collect the spec, the code or the running product.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - style guide, template, terminology list or safety-notice standard -
   is followed and noted in the document brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them - with one exception. If the job depends on a safety, legal, regulatory or
   approval-limit standard and that line is still `REQUIRED INPUT`, the gap is a **blocking** open item:
   do not fill it with a default or with general practice. This skill fills gaps only.
2. **Never invent facts.** Any rating, torque, setting, step, parameter or version the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Check every fact against its source.** Clear prose is not proof; a criterion passes when each value and step is matched to a cited source. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Safety text is never softened.** Never remove, reword or reorder a warning, caution or lockout step unless the source changed.
5. **Drafts, not approvals.** Everything this skill produces is a draft for a named, qualified human to
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
6. The document adds, changes or removes a safety warning, limit, rating or operating step that could hurt someone if wrong.

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
- **gated**: stop after Brief and after Source for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the reader or the task is unclear enough that two different documents would both fit;
- the engineering sources at the current revision cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Brief (HW: Technical Writer / SW: Documentation Engineer)

Turn the request into a document brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Reader and task** - who reads it and what they need to do.
- **Sources** - the documents, revisions or systems the content comes from.
- **Done when** - 3 to 7 criteria, each checkable by matching the text to its source. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - template, length, format, languages, regulatory content, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: collect the drawings, datasheets and procedures at their current revision.
- Software track: collect the spec, the code or the running product.
- Change work: before writing this, read the current document and its revision history and add **Must not break** -
  approved safety text, document numbers and cross-references.

Handoff: the document brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Source (HW: Technical Writer / SW: Documentation Engineer)

One short piece of work. Settle the outline first.

### Outline and fact sheet

Keep it to what Stage 3 needs to start:

- **Approach** - the shortest document that lets the reader complete the task. Change work: reuse what exists before adding anything new.
- **Fact sheet** - every value and step with its source; missing ones are `REQUIRED INPUT`.
- **Section list** - the sections this job writes or changes. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - procedures first, then reference, then front matter; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the outline and fact sheet.

## Stage 3 - Write (HW: Technical Writer / SW: Documentation Engineer)

Write the document in the order planned. Get the core procedure complete first, then widen it.

- Hardware track: write steps in the order they are performed, one action per step, warnings before the step.
- Software track: show a working example for each task.
- Change work: stay inside the section list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the draft, in a usable state.

## Stage 4 - Review (HW: Technical Writer (second reader) / SW: Developer Advocate)

Check what was produced against the document brief, by matching every fact to the fact sheet and walking each procedure.

1. Check every **Done when** criterion and record the evidence: source and revision per fact, procedure walk-through notes.
2. Hardware track: every value and step matches the cited source and revision.
3. Software track: every example was run or matches the current spec.
4. Change work: check every **Must not break** item still holds.
5. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. In Assurance mode, send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Publish (HW: Technical Writer / SW: Documentation Engineer)

Hand it over in a state the user can use immediately.

- Deliver the document with its source register, in the form the user asked for or house rules require.
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
PRINCIPAL REVIEW: <not used; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Stage 4 release check: consistent / consistent with conditions / not consistent (Lean/Balanced) | n rulings; Principal release review: consistent / consistent with conditions / not consistent (Assurance) | NOT REVIEWED - Principal not available>
DECISIONS MADE FOR YOU: <assumptions and provisional choices to confirm or overturn>
OPEN ITEMS: <TBD, REQUIRED INPUT, NOT RUN, discrepancies>
NEXT: <at most three follow-ups worth doing, if any>
```

Never omit `VERDICT:`, `MODELS:`, `USAGE:` or `PRINCIPAL REVIEW:`. Leave out any other line that has nothing to say.

## Standard record

For Standard work, read `references/record-template.md` immediately before creating the record. Do not load it for Small work.
