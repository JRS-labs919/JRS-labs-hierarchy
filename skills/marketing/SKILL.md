---
name: "marketing"
description: Take a product, launch or audience goal to reviewed, publish-ready marketing content with a claims register. Use for "write a brochure for", "launch plan for", "draft the web page" or /jrs:marketing. Not for manuals and technical documentation (use jrs:technical-publications).
---

# JRS-Marketing

Turn a marketing goal into content where the message is deliberate and every claim has a source. 5 stages, each with one owner role, one output and one handoff -
a marketing department with the meetings removed.

| # | Stage | Role | Model | Effort | Output (the handoff) |
|---|---|---|---|---|---|
| - | Escalations | Principal (Chief Revenue Officer) - rules on escalations, final sign-off (Standard size) | Fable 5.2 | Max | Rulings and release sign-off |
| - | All | Advisor (VP Marketing) - plans, gates, dispatches, integrates | Fable 5.2 | Medium | Gate decisions, integrated output |
| 1 | Brief | Product Marketing Manager | Opus 5.5 | High | Marketing brief |
| 2 | Messaging | HW: Technical Marketing Engineer / SW: Demand Generation Manager | Opus 5.5 | Medium | Messaging plan |
| 3 | Create | HW: Collateral Specialist / SW: Growth Marketer or SEO/Content Marketer | Sonnet 5.5 | Medium | Content draft |
| 4 | Review | Brand Manager | Opus 5.5 | High | Pass/fail per criterion |
| 5 | Launch | Marketing Operations | Haiku 5.5 | Low | Publish-ready content |

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

The user is the product or sales owner. Their prompt, plus anything they attached or pointed
to, **is** the marketing request. Stage 1's job is to turn it into the marketing brief, not to send
it back as a questionnaire.

## Keep it small

The point of the stages is to catch the expensive mistakes early: a claim the product cannot back up,
content aimed at nobody in particular, off-brand work that has to be redone. Anything beyond that is overhead, so apply one test
to every task you are about to add:

> Does this change what the audience understands or does, or prove a claim? If neither, skip it.

Size the job before starting and say which size you picked:

- **Small** - one email, one post or one page section. Run all stages in the conversation: audience and goal, the message, the draft, a claims check, the handoff. No record file.
- **Standard** - anything larger. Keep one record file, `jrs/marketing/<slug>.md`, with one
  section per stage (template at the end).

Pick the track too, because it changes who owns each stage and what counts as proof:

- **Hardware** - product literature, technical marketing and events. Collect the product facts, ratings and certifications from engineering sources.
- **Software** - web, campaigns, content and lifecycle messaging. Collect the audience, funnel stage, offer and how success is measured.
- **Combined** - a request with both. Run the two tracks side by side under one record and one report; where they depend on each other, name the dependency and its owner.

Say also whether the job is **new** or a **change** to something already released. A change adds
the Must not break list in Stage 1 and the boundary rule in Stage 3.

## Ground rules

1. **House rules outrank this skill.** Read `house-standards.md` in this skill's folder before
   Stage 1. Whatever it or the environment defines - brand guide, tone of voice, legal claims policy or template -
   is followed and noted in the marketing brief. Lines there still marked `REQUIRED INPUT` are not
   defined yet; ignore them. This skill fills gaps only.
2. **Never invent facts.** Any specification, statistic, customer name, quote, award or comparison the user did not supply and you cannot read from
   a source is `TBD` or `REQUIRED INPUT`, and goes in the open items. A default is fine when
   labelled as an assumption.
3. **Source every claim.** Good copy is not proof; a claim passes when the claims register names where it came from. A check that could not run is reported as `NOT RUN`
   with the reason.
4. **Nothing is published without being asked.** Never publish, send, schedule or post content, or use a customer's name, logo or quote without stated permission.
5. **No superlatives without evidence.** Words like best, fastest or only need a source or are cut.

## Principal and escalation

**One boss.** The Advisor (VP Marketing) plans and runs the job. The Principal
(Chief Revenue Officer) never plans, builds or dispatches; it only rules on what is escalated to it,
and its ruling is final.

Escalate to the Principal only when:

1. The audience or the goal is unclear enough that two different pieces would both fit, and guessing wrong wastes the work (the user is
   asked first if they are reachable; the Principal rules when they are not, or when the question
   is technical rather than a preference).
2. Sources conflict and the conflict cannot be resolved from evidence.
3. A criterion has failed Stage 4 twice (the re-scope point in Stage 4).
4. The next step is destructive or irreversible.
5. Release sign-off - every Standard-size job, before Stage 5 delivers.
6. Content names a competitor, makes a comparative claim or uses a customer reference.

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
- **gated**: stop after Brief and after Messaging for a yes/no. Use when the user asks
  to approve as you go.

In either mode, stop and ask - one short round, all questions together - only when:

- the audience or the goal is unclear enough that two different pieces would both fit;
- the product facts or brand assets cannot be opened;
- the next step is destructive, irreversible, or needs a credential you do not have.

## Stage 1 - Brief (Product Marketing Manager)

Turn the request into a marketing brief. Take everything from the prompt and attachments
first; fill the rest with labelled assumptions or `TBD`.

- **Audience and goal** - who it is for and what they should do next.
- **Offer and proof** - what we are saying and the facts that support it.
- **Done when** - 3 to 7 criteria, each checkable by reading the content against the brief and the claims register. These are what
  Stage 4 tests.
- **In scope / Out of scope** - out of scope matters most; it stops the work growing.
- **Constraints** - brand, channel format, length, legal claims policy, house rules adopted, deadline if given.
- **Assumptions and TBD** - everything you filled in or could not.

- Hardware track: collect the product facts, ratings and certifications from engineering sources.
- Software track: collect the audience, funnel stage, offer and how success is measured.
- Change work: before writing this, read the current content and its performance and add **Must not break** -
  approved claims, brand elements and live links.

Handoff: the marketing brief. Autonomous mode shows it and continues; gated mode waits.

## Stage 2 - Messaging (HW: Technical Marketing Engineer / SW: Demand Generation Manager)

One short piece of work. Settle the single message first.

### Messaging plan

Keep it to what Stage 3 needs to start:

- **Approach** - one audience, one message, one action. Change work: reuse what exists before adding anything new.
- **Claims register** - each claim with its source; unsourced claims are `REQUIRED INPUT`.
- **Asset list** - the pieces this job creates or changes. Change work: this list is the boundary; work
  outside it needs a reason.
- **Order** - the primary asset first, then derivatives; smallest complete version first.
- **Risks** - only the ones that would change the plan.

Handoff: the messaging plan.

## Stage 3 - Create (HW: Collateral Specialist / SW: Growth Marketer or SEO/Content Marketer)

Create the content in the order planned. Get the primary asset complete first, then widen it.

- Hardware track: lead with the application and the proof; specs appear exactly as sourced.
- Software track: lead with the reader's problem and one clear action.
- Change work: stay inside the asset list and match existing conventions.
- If a step shows the plan was wrong, fix the plan in the record, then continue. Do not quietly
  drift from it.
- If independent pieces can run in parallel and the environment has subagents, dispatch them
  with separate write paths. Otherwise work in sequence. Do not parallelise for its own sake.

Handoff: the content draft, in a usable state.

## Stage 4 - Review (Brand Manager)

Check what was produced against the marketing brief, by checking each claim against the register and the content against the brand guide.

1. Check every **Done when** criterion and record the evidence: claims register, brand checks, link checks.
2. Hardware track: every rating, certification and comparison is in the claims register with its source.
3. Software track: every feature, number and customer reference is in the claims register with its source.
4. Change work: check every **Must not break** item still holds.
5. Anything that fails goes back to Stage 3. After two failed rounds on the same criterion, stop
   fixing and re-scope it with the user.

Handoff: a pass/fail line per criterion, with evidence, and any `NOT RUN`. Standard size:
send the Principal a trigger-5 escalation packet with this evidence before Stage 5.

## Stage 5 - Launch (Marketing Operations)

Hand it over in a state the user can use immediately.

- Deliver the content and its claims register, in the form the user asked for or house rules require.
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
# <Name> - jrs:marketing
Track: Hardware | Software | Combined    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Fable | Fallback - <reason>, from Stage <n>

## 1. Brief
Audience and goal:
Offer and proof:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Messaging
Approach:
Claims register:
Asset list:
Order:
Risks:

## 3. Create log
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
