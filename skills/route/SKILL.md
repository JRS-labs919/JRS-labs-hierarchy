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

## Step 0 - Model context (once)

Read the model named by the current system prompt and pass it as
`MODELS: Advisor <actual session model>; Principal path <Fable | Opus fallback>`. The Advisor stays on
the session model in Lean and Balanced; do not require Opus merely because the session is not Fable.
Use the Fable Principal when the session is on Fable and it is available; otherwise use the Opus
Principal. If a Fable Principal call fails partway through a chain, use Opus for later Principal calls
and do not redo completed work.

## Step 0.5 - Usage mode and budget

Honor an explicit user choice of **Lean**, **Balanced** or **Assurance**, subject to mandatory upgrades:

- **Lean** - only one department, Small, low-risk, reversible, no live-system action, and no release,
  disposition, compliance or safety decision. Target at most one tier-agent dispatch.
- **Balanced** - default for ordinary work and chains. Target at most two tier-agent dispatches per
  department. A Balanced chain targets at most six tier-agent dispatches total: intermediate
  departments use one bundled worker, and the final department gets an independent review.
- **Assurance** - when the user asks for the full process, or for safety, regulatory, security or
  legal-impact work; live or production changes; destructive or irreversible steps; final release,
  disposition or risk decisions; or a department trigger 4 or 6. It keeps the full five-stage
  dispatch and Principal release review.

Use `RUN MODE: <mode> - <one-line reason>` and
`USAGE BUDGET: <tier-agent target for this department; chain target/used when applicable>`. The router
may assign Lean to an eligible intermediate department in a Balanced chain. Once a department starts,
its mode may upgrade but never downgrade. Safety and required Principal calls can exceed the target;
non-safety extra calls require the user to agree first when they are reachable.

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
In that case, do not choose from an assumption: ask one short either/or question and stop before
dispatch. Two common required-clarification cases are:

- An unnamed audience for a startup or operating procedure: ask whether it is for a technician on
  site (`jrs:field-service`) or a customer-facing manual (`jrs:technical-publications`).
- An ambiguous "BOM structure": ask whether it means the product's BOM
  (`jrs:hardware-engineering`) or the BOM schema/workflow in the tool
  (`jrs:engineering-systems`).

When routing product conformity to a law, regulation or directive, also flag applicability and legal
interpretation for the user's Legal owner. Quality owns the conformance evidence; Legal is not part of
this plugin.

## Step 3 - Run

**One department.** Invoke the chosen skill with the user's request unchanged, plus the Step 0,
Step 0.5 and Step 1 lines. That skill owns everything from there, including its own Principal and
Advisor.

**A chain.** Use a named flow when one fits; go only as far along it as the user asked. If the user
states an order (for example, "brochure, then manual"), that order wins and becomes a custom chain.
Do not reverse it to match a named flow unless the user confirms the change.

| Flow | Departments, in order |
|---|---|
| Quote to order | `jrs:sales` -> `jrs:sales-applications-engineering` (scope and preliminary estimate) -> `jrs:supply-chain` (only when a bought-out price is missing) -> `jrs:sales-applications-engineering` (final priced quote, only when supply chain ran) |
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
MODELS: <Advisor actual session model; Principal path Fable | Opus fallback>
RUN MODE: <Lean | Balanced | Assurance> - <reason or upgrade>
USAGE BUDGET: <department tier-agent target; chain target/used when applicable>
USAGE SO FAR: <tier-agent dispatches and Principal calls from completed departments>
```

The first department gets the user's original request plus the `CHAIN:`, `ROUTE:`, `MODELS:`,
`RUN MODE:`, `USAGE BUDGET:` and `USAGE SO FAR: 0 tier-agent dispatches; 0 Principal calls` lines.
Every department reads those lines even when there is no `HANDOFF:` block yet.

### Chain rules

1. Each department runs to its own Stage 5 report before the next one starts.
2. A `blocked` verdict stops the chain. Report where it stopped and why.
3. `done with open items` continues - unless an open item is a `REQUIRED INPUT` the next department
   cannot work without. Then stop before dispatching it, and ask the user for that input.
4. Skip a department only when an existing output satisfies that exact flow step; say that you
   skipped it. Do not skip an intentional repeat with a different purpose, such as the final
   `jrs:quality` effectiveness check in the nonconformance flow or the final
   `jrs:sales-applications-engineering` pricing pass after supply chain.
5. A department does not branch to a sibling that is a later step of the chain; the `CHAIN:` line tells
   it which those are. It may still branch to a sibling outside the chain, and does that itself. Do not
   pre-load the sibling.
6. Combined track: run the hardware and software departments of the same step one after the other,
   hardware first. Their interfaces are settled by `jrs:systems-engineering`; if that step was skipped,
   say so in the open items. The step's verdict is the worse of the two.
7. Size is each department's call. A department in a chain keeps its own mode-specific review
   contract and upgrades itself when it finds an Assurance condition.
8. A Balanced chain targets at most six tier-agent dispatches: one bundled dispatch for each
   intermediate department and at most two for the final department. Use Lean for an eligible
   intermediate step. Before exceeding six for a non-safety reason, ask the user whether to continue
   in Balanced or upgrade to Assurance. Required safety and Principal calls always run.
9. Add each department's `USAGE:` counts to `USAGE SO FAR:` in the next handoff and aggregate them in
   the chain report.

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
MODELS: <Advisor session model; tier models/count by department; Principal model or not used>
USAGE: <mode by department; total tier-agent dispatches; total Principal calls; budget status>
DEPARTMENTS: <skill - verdict - deliverable and path - its PRINCIPAL REVIEW line, one line each>
SKIPPED: <department - reason>
DECISIONS MADE FOR YOU: <routing choices and assumptions to confirm or overturn>
OPEN ITEMS: <merged TBD, REQUIRED INPUT, NOT RUN, discrepancies, tagged by department>
NEXT: <at most three follow-ups worth doing, if any>
```

Never omit `VERDICT:`, `ROUTE:`, `MODELS:` or `USAGE:`. Leave out any other line that has nothing to
say.
