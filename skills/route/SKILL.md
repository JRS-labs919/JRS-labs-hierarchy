---
name: route
description: Front door for the jrs department skills. Routes a business or engineering request to the one department skill and track (hardware, software or combined) that should handle it, and chains departments for work that crosses them, such as quote to order or idea to launch. Use when the user says "which team handles this", "run this through the departments", "take this from quote to delivery", or /jrs:route, or when a request clearly spans more than one department. Not for requests that name a department skill directly (use that skill).
---

# JRS-Route

Send a request to the right department skill, on the right track, loading as little as possible.
This skill decides and dispatches. It does no department work itself.

## Token rule

Every department skill costs a few thousand tokens to load. So:

1. Decide from the tables below. Do not open a department skill to find out whether it fits.
2. Load one department skill at a time, and only the one chosen.
3. In a chain, run each department **in this session**, one after the other. Do not run a department
   in a subagent: nested dispatch, Principal access and user prompts are not available in every
   environment, so the department could lose its review layer. Keep the conversation small another way:
   each department writes its deliverable to a file, and only its Stage 5 report and the HANDOFF block
   move forward.
4. Carry forward the handoff, not the history.

## Step 0 - Model check (once)

Read the model your own system prompt names. If it is a Fable model (any version), department skills
run their Principal and Advisor on Fable. If it is any other model - or Fable has run out - they run
on the fallback: Opus for both. Pass the result to every department as `MODELS: Fable` or
`MODELS: Fallback - <reason>`. State the model that is actually running; a department checks the line
against its own system prompt. If a Fable call fails partway through a chain, switch to the fallback
for the rest of the chain and do not switch back.

## Step 1 - Classify

Say these three things in one line before routing:

- **Track** - Hardware (a physical product, equipment, material or site), Software (an application,
  platform, subscription or data), or Combined (both).
- **Work** - new, or a change to something already released.
- **Reach** - one department, or a chain.

A department picks its own track from its own list. If it has no Combined track, it takes the half
that belongs to it and names the other half in its open items.

## Step 2 - Pick the department

Match on what the user wants to end up holding, not on keywords.

### Product

| Skill | Produces |
|---|---|
| `jrs:product-management` | an approved PRD and roadmap entry |
| `jrs:npi-program-management` | a gated program plan and launch-readiness record |
| `jrs:design-hw` | an industrial design intent package engineering can build to |
| `jrs:design-sw` | a reviewed UX/UI design spec developers can build from |

### Engineering

| Skill | Produces |
|---|---|
| `jrs:hardware-engineering` | a verified design package for a physical product, ready for release |
| `jrs:software-engineering` | working, tested code ready to ship |
| `jrs:platform-infrastructure` | a tested infrastructure or deployment change with a runbook and rollback |
| `jrs:data-ai` | a validated analysis, model or dashboard with its method stated |
| `jrs:systems-engineering` | baselined system requirements, architecture and interface definitions |
| `jrs:engineering-systems` | a tested configuration of an engineering tool (PLM, CAD, build tooling) with a rollout note |
| `jrs:technical-publications` | a reviewed manual, guide or reference |

### Operations

| Skill | Produces |
|---|---|
| `jrs:manufacturing` | a build package the floor can run - routing, work instructions, schedule and test plan |
| `jrs:supply-chain` | a levelled supplier comparison and award recommendation |
| `jrs:quality` | a quality record with a recommended disposition |
| `jrs:project-delivery` | a baselined project plan, running status and a closeout package |
| `jrs:field-service` | a job plan with procedure, safety steps and test sheets, then the service report |
| `jrs:remote-monitoring` | a triaged incident from connected equipment, with a response and a closed-out report |
| `jrs:ehs` | a hazard assessment with controls, or an incident report with corrective actions |

### Commercial

| Skill | Produces |
|---|---|
| `jrs:sales` | a qualified opportunity with an account strategy and customer-ready proposal draft |
| `jrs:sales-applications-engineering` | a compliant technical proposal with scope, clarifications and an estimate |
| `jrs:marketing` | reviewed, publish-ready marketing content with a claims register |
| `jrs:customer-success-support` | a diagnosed case with a resolution, a customer reply draft and a clean record |

### Finance, IT and Security

| Skill | Produces |
|---|---|
| `jrs:accounting` | a reviewed, posting-ready workpaper with the treatment stated |
| `jrs:fpa` | a checked financial model and a short recommendation with assumptions stated |
| `jrs:it` | a tested IT change or fix with a rollback and a user note |
| `jrs:security` | validated security findings with severities and a remediation plan |

People and Legal are not part of this plugin. If a request belongs there, say so and stop. If only part
of it does - contract meaning, liability, employment - route the business part and flag that part for
the user's Legal or People owner.

### Tie-breaks

When two departments fit, use this table before anything else.

| The request is about | Goes to | Not to |
|---|---|---|
| a customer's RFQ or spec that we must quote | `jrs:sales-applications-engineering` | `jrs:supply-chain` |
| an RFQ we send to suppliers | `jrs:supply-chain` | `jrs:sales-applications-engineering` |
| an alarm or trend from connected equipment, whoever reported it | `jrs:remote-monitoring` | `jrs:customer-success-support` |
| a customer complaint, question or account concern with no alarm data | `jrs:customer-success-support` | `jrs:remote-monitoring` |
| an injury, near miss, spill or exposure | `jrs:ehs` | `jrs:remote-monitoring`, `jrs:field-service` |
| a procedure a technician follows on site | `jrs:field-service` | `jrs:technical-publications` |
| an instruction the production floor follows | `jrs:manufacturing` | `jrs:technical-publications` |
| a manual or guide the customer reads | `jrs:technical-publications` | `jrs:field-service`, `jrs:manufacturing` |
| how a product looks, feels and is used | `jrs:design-hw` | `jrs:hardware-engineering` |
| sizing, calculation, drawings or a BOM change for a product | `jrs:hardware-engineering` | `jrs:design-hw`, `jrs:engineering-systems` |
| the PLM, CAD or BOM tool itself - schema, workflow, attributes | `jrs:engineering-systems` | `jrs:hardware-engineering`, `jrs:it` |
| product conformity to a drawing, spec, standard or directive | `jrs:quality` | `jrs:security` |
| a security standard, control or threat | `jrs:security` | `jrs:quality` |
| a forecast, budget, margin or price model | `jrs:fpa` | `jrs:data-ai` |
| planning a release or launch | `jrs:npi-program-management` | `jrs:software-engineering`, `jrs:platform-infrastructure` |

Still two candidates: pick the one whose output the user asked for, and name the runner-up in one line.
Ask the user only when the two outputs are materially different and nothing in the request settles it.

## Step 3 - Run

**One department.** Invoke the chosen skill with the user's request unchanged, plus the Step 0 and
Step 1 lines. That skill owns everything from there, including its own Principal and Advisor.

**A chain.** Use a named flow when one fits; go only as far along it as the user asked.

| Flow | Departments, in order |
|---|---|
| Quote to order | `jrs:sales` -> `jrs:sales-applications-engineering` -> `jrs:supply-chain` (only when a bought-out price is missing) |
| Order to delivery | `jrs:project-delivery` -> `jrs:manufacturing` -> `jrs:quality` -> `jrs:field-service` |
| Idea to launch | `jrs:product-management` -> `jrs:design-hw` or `jrs:design-sw` -> `jrs:systems-engineering` (Combined only) -> `jrs:hardware-engineering` or `jrs:software-engineering` -> `jrs:npi-program-management` |
| Issue to resolution | `jrs:customer-success-support` or `jrs:remote-monitoring` (see tie-breaks) -> `jrs:field-service` (only when someone must go to site) |
| Nonconformance to corrective action | `jrs:quality` -> the department that owns the cause (`jrs:hardware-engineering`, `jrs:software-engineering`, `jrs:manufacturing` or `jrs:supply-chain`) -> `jrs:quality` (check the fix worked) |
| Engineering change | `jrs:hardware-engineering` -> `jrs:engineering-systems` (only when the tool or workflow must change) -> `jrs:manufacturing` -> `jrs:technical-publications` |
| Security incident | `jrs:remote-monitoring` or `jrs:it` -> `jrs:security` -> `jrs:platform-infrastructure` (only when a change is needed) |
| Release to market | `jrs:technical-publications` -> `jrs:marketing` |

### The handoff block

Every department after the first receives the user's original request plus this block, and nothing else:

```
HANDOFF:
FROM: <previous department skill> - <its verdict>
DELIVERABLE: <path, or the text if it is short>
OPEN ITEMS: <its TBD, REQUIRED INPUT, NOT RUN and discrepancies, each with an owner>
CHAIN: <flow name> - step <n> of <m>; later steps: <skills still to run>
ROUTE: <track> / <new | change>
MODELS: <Fable | Fallback - reason>
```

The first department gets the user's original request plus the `CHAIN:`, `ROUTE:` and `MODELS:`
lines. Every department reads those lines even when there is no `HANDOFF:` block yet.

### Chain rules

1. Each department runs to its own Stage 5 report before the next one starts.
2. A `blocked` verdict stops the chain. Report where it stopped and why.
3. `done with open items` continues - unless an open item is a `REQUIRED INPUT` the next department
   cannot work without. Then stop before dispatching it, and ask the user for that input.
4. Skip a department only when an existing output satisfies that exact flow step; say that you
   skipped it. Do not skip an intentional repeat with a different purpose, such as the final
   `jrs:quality` effectiveness check in the nonconformance flow.
5. A department does not branch to a sibling that is a later step of the chain; the `CHAIN:` line tells
   it which those are. It may still branch to a sibling outside the chain, and does that itself. Do not
   pre-load the sibling.
6. Combined track: run the hardware and software departments of the same step one after the other,
   hardware first. Their interfaces are settled by `jrs:systems-engineering`; if that step was skipped,
   say so in the open items. The step's verdict is the worse of the two.
7. Size is each department's call. A department in a chain keeps its own Principal review.

## Ground rules

1. **The department skill governs the work.** This skill adds no rules to it and removes none.
2. **Never invent facts.** A value missing between departments stays `TBD` or `REQUIRED INPUT` and
   travels with the handoff.
3. **Nothing leaves without being asked.** Routing never sends, posts, releases, deploys or commits.
4. **Drafts, not approvals.** A chain's output is a set of drafts for named, qualified people to approve.
   A `done` verdict is not an approval, a release or a safety sign-off.

## Report (chains only)

A single department reports in its own shape. For a chain, report bottom line first:

```
VERDICT: <done | done with open items | blocked at <department>>
ROUTE: <track> / <new | change> / <flow name or custom chain>
MODELS: <Fable | Fallback - Opus for Principal and Advisor (reason, from department n)>
DEPARTMENTS: <skill - verdict - deliverable and path - its PRINCIPAL REVIEW line, one line each>
SKIPPED: <department - reason>
DECISIONS MADE FOR YOU: <routing choices and assumptions to confirm or overturn>
OPEN ITEMS: <merged TBD, REQUIRED INPUT, NOT RUN, discrepancies, tagged by department>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.
