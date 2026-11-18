---
name: "route"
description: Front door for the jrs department skills. Routes a business or engineering request - product, engineering, operations, commercial, finance, IT or security - to the one department skill and track (hardware, software or combined) that should handle it, and chains departments for work that crosses them, such as quote to order or idea to launch. Use when the user says "which team handles this", "run this through the departments", "take this from quote to delivery", or /jrs:route, or when a request clearly spans more than one department. Not needed when the user names a department skill directly.
---

# JRS-Route

Send a request to the right department skill, on the right track, loading as little as possible.
This skill decides and dispatches. It does no department work itself.

## Token rule

Every department skill costs a few thousand tokens to load. So:

1. Decide from the table below. Do not open a department skill to find out whether it fits.
2. Load one department skill at a time, and only the one chosen.
3. In a chain, run each department in a subagent when the environment has them, so its skill body
   and working notes stay out of this conversation and only its Stage 5 report comes back.
4. Carry forward the handoff, not the history.

## Step 0 - Model check (once)

Check once whether this session is on Fable 5.2. If it is, department skills run their Principal and
Advisor on Fable. If it is not - or Fable has run out - they run on the fallback: Opus 5.5 / Max for
both. Pass the result to every department as a `MODELS: Fable` or `MODELS: Fallback - <reason>` line so
none of them repeats the check. If a Fable call fails partway through a chain, switch to the fallback
for the rest of the chain and do not switch back.

## Step 1 - Classify

Say these three things in one line before routing:

- **Track** - Hardware (a physical product, equipment, material or site), Software (an application,
  platform, subscription or data), or Combined (both).
- **Work** - new, or a change to something already released.
- **Reach** - one department, or a chain.

## Step 2 - Pick the department

Match on what the user wants to end up holding (the Output column), not on keywords.

### Product

| Skill | Starts from | Produces |
|---|---|---|
| `jrs:product-management` | a product idea, customer request or market gap | an approved PRD and roadmap entry |
| `jrs:npi-program-management` | an approved product or release scope | a gated program plan and launch-readiness record |
| `jrs:design-hw` | a physical product need | an industrial design intent package engineering can build to |
| `jrs:design-sw` | a software product need | a reviewed UX/UI design spec developers can build from |

### Engineering

| Skill | Starts from | Produces |
|---|---|---|
| `jrs:hardware-engineering` | a requirement, spec or change request for a physical product | a verified design package ready for release |
| `jrs:software-engineering` | a feature request, bug or change | working, tested code ready to ship |
| `jrs:platform-infrastructure` | an infrastructure, deployment or connectivity need | a tested change with a runbook and rollback |
| `jrs:data-ai` | a question, dataset or prediction need | a validated analysis, model or dashboard with its method stated |
| `jrs:systems-engineering` | a product or project that joins hardware and software | a baselined set of system requirements, architecture and interface definitions |
| `jrs:engineering-systems` | a need to set up or change an engineering tool, schema or workflow | a tested configuration with a rollout note |
| `jrs:technical-publications` | a product, feature or procedure that needs documenting | a reviewed manual, guide or reference |

### Operations

| Skill | Starts from | Produces |
|---|---|---|
| `jrs:manufacturing` | a released design or a production order | a build package the floor can run - routing, work instructions, schedule and test plan |
| `jrs:supply-chain` | a material, equipment, service or software need | a levelled supplier comparison and award recommendation |
| `jrs:quality` | a product, process, supplier or release that must be shown to conform | a quality record with a clear disposition |
| `jrs:project-delivery` | an awarded order, contract or statement of work | a baselined project plan, running status and a closeout package |
| `jrs:field-service` | a service call, startup or maintenance request | a job plan with procedure, safety steps and test sheets, then the service report |
| `jrs:remote-monitoring` | an alarm, trend or customer report from connected equipment | a triaged incident with a response and a closed-out report |
| `jrs:ehs` | a task, site, incident or regulatory question | a hazard assessment with controls, or an incident report with corrective actions |

### Commercial

| Skill | Starts from | Produces |
|---|---|---|
| `jrs:sales` | a lead, account or opportunity | a qualified opportunity with an account strategy and customer-ready proposal draft |
| `jrs:sales-applications-engineering` | a customer RFQ, spec or technical inquiry | a compliant technical proposal with scope, clarifications and an estimate |
| `jrs:marketing` | a product, launch or audience goal | reviewed, publish-ready marketing content with a claims register |
| `jrs:customer-success-support` | a customer issue, question or account-health concern | a diagnosed case with a resolution, a customer reply draft and a clean record |

### Finance

| Skill | Starts from | Produces |
|---|---|---|
| `jrs:accounting` | a transaction, close task or accounting question | a reviewed, posting-ready workpaper with the treatment stated |
| `jrs:fpa` | a business question, plan or pricing decision | a checked financial model and a short recommendation with assumptions stated |

### IT

| Skill | Starts from | Produces |
|---|---|---|
| `jrs:it` | an IT request, problem or system change | a tested change or fix with a rollback and a user note |

### Security

| Skill | Starts from | Produces |
|---|---|---|
| `jrs:security` | a system, product, change or control that needs a security view | validated findings with severities and a remediation plan |

People and Legal are not part of this plugin. If a request belongs there, say so and stop.

Two candidates: pick the one whose output the user asked for, and name the runner-up in one line.
Ask the user only when the two outputs are materially different and nothing in the request settles it.

## Step 3 - Run

**One department.** Invoke the chosen skill with the user's request unchanged, plus the Step 0 and Step 1 lines.
That skill owns everything from there, including its own Principal and Advisor.

**A chain.** Use a named flow when one fits; go only as far along it as the user asked.

| Flow | Departments, in order |
|---|---|
| Quote to order | `jrs:sales` -> `jrs:sales-applications-engineering` -> `jrs:supply-chain` (only when a bought-out price is missing) |
| Order to delivery | `jrs:project-delivery` -> `jrs:manufacturing` -> `jrs:quality` -> `jrs:field-service` |
| Idea to launch | `jrs:product-management` -> `jrs:design-hw` or `jrs:design-sw` -> `jrs:systems-engineering` (Combined only) -> `jrs:hardware-engineering` or `jrs:software-engineering` -> `jrs:npi-program-management` |
| Issue to resolution | `jrs:customer-success-support` -> `jrs:remote-monitoring` (connected equipment) -> `jrs:field-service` (only when someone must go to site) |

Chain rules:

1. Each department runs to its own Stage 5 report before the next one starts.
2. The next department receives the previous deliverable and its OPEN ITEMS as input - nothing else.
3. A `blocked` verdict stops the chain. Report where it stopped and why.
4. Skip a department whose output already exists; say that you skipped it.
5. Combined track: hardware and software departments at the same step may run side by side; their
   interfaces are settled by `jrs:systems-engineering`.
6. A department skill that branches to a sibling does so itself. Do not pre-load the sibling.

## Ground rules

1. **The department skill governs the work.** This skill adds no rules to it and removes none.
2. **Never invent facts.** A value missing between departments stays `TBD` or `REQUIRED INPUT` and
   travels with the handoff.
3. **Nothing leaves without being asked.** Routing never sends, posts, releases, deploys or commits.

## Report (chains only)

A single department reports in its own shape. For a chain, report bottom line first:

```
VERDICT: <done | done with open items | blocked at <department>>
ROUTE: <track> / <new | change> / <flow name or custom chain>
MODELS: <Fable | Fallback - Opus 5.5 / Max for Principal and Advisor (reason, from department n)>
DEPARTMENTS: <skill - verdict - deliverable and path, one line each>
SKIPPED: <department - reason>
DECISIONS MADE FOR YOU: <routing choices and assumptions to confirm or overturn>
OPEN ITEMS: <merged TBD, REQUIRED INPUT, NOT RUN, discrepancies, tagged by department>
NEXT: <at most three follow-ups worth doing, if any>
```

Leave out any line that has nothing to say.
