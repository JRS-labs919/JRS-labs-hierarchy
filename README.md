# JRS for Claude

[![Validate Claude plugin](https://github.com/JRS-labs919/JRS-labs-hierarchy/actions/workflows/validate.yml/badge.svg)](https://github.com/JRS-labs919/JRS-labs-hierarchy/actions/workflows/validate.yml)

JRS is a Claude Code plugin that routes company work through the department that owns it. It includes a front-door router, 26 department skills, and eight tiered agents. Each department follows a five-stage pipeline with one owner, one output, and one handoff per stage.

## Install

With Claude Code 2.1.292 or newer, install directly from this GitHub repository:

```sh
claude plugin install jrs --marketplace JRS-labs919/JRS-labs-hierarchy
```

On an older Claude Code release, add the marketplace and install the plugin in two steps:

```sh
claude plugin marketplace add JRS-labs919/JRS-labs-hierarchy
claude plugin install jrs@jrs-labs919-plugins
```

Start a new Claude Code session, then use:

- `/jrs:route` when you are not sure which department owns the work, or the request crosses departments.
- `/jrs:<department>` to go straight to one department, such as `/jrs:supply-chain`.

To try a local clone without installing it:

```sh
claude --plugin-dir .
```

## Standalone Claude skills

The [`packages/standalone`](packages/standalone) directory contains the same 27 workflows as individual `.skill` files for Claude.ai. Install `jrs-route.skill` first, then only the departments you need.

Do not install the standalone skills and the plugin in the same environment: their triggers overlap. The plugin is the richer option for Claude Code because it also includes shared agents and per-department house-standard files.

## Customize before relying on it

Each department has a `house-standards.md` file beside its `SKILL.md`. Replace the `REQUIRED INPUT` lines with your company’s actual titles, rules, systems, approval limits, and record locations. Lines left as `REQUIRED INPUT` are ignored.

See [INSTALL-AND-CUSTOMISE.md](INSTALL-AND-CUSTOMISE.md) for the full setup guide.

## Included skills

| Skill | Department | Principal | Advisor |
|---|---|---|---|
| `jrs:route` | Router | — | — |
| `jrs:product-management` | Product Management | Chief Product Officer | VP Product |
| `jrs:npi-program-management` | NPI & Program Management | Chief Product Officer | Director, PMO |
| `jrs:design-hw` | Industrial Design | Chief Product Officer | Head of Design |
| `jrs:design-sw` | UX/UI Design | Chief Product Officer | Head of Design |
| `jrs:hardware-engineering` | Hardware Engineering | Chief Technology Officer | VP Hardware Engineering |
| `jrs:software-engineering` | Software Engineering | Chief Technology Officer | VP Software Engineering |
| `jrs:platform-infrastructure` | Platform & Infrastructure | Chief Technology Officer | VP Platform |
| `jrs:data-ai` | Data & AI | Chief Technology Officer | Head of Data |
| `jrs:systems-engineering` | Systems Engineering | Chief Technology Officer | Chief Systems Engineer |
| `jrs:engineering-systems` | Engineering Systems | Chief Technology Officer | Manager, Engineering Systems |
| `jrs:technical-publications` | Technical Publications | Chief Technology Officer | Technical Publications Manager |
| `jrs:manufacturing` | Manufacturing | Chief Operating Officer | Plant Manager |
| `jrs:supply-chain` | Supply Chain | Chief Operating Officer | VP Supply Chain |
| `jrs:quality` | Quality | Chief Operating Officer | VP Quality |
| `jrs:project-delivery` | Project Delivery | Chief Operating Officer | Director, Project Management |
| `jrs:field-service` | Field Service & Commissioning | Chief Operating Officer | VP Service |
| `jrs:remote-monitoring` | Remote Monitoring / NOC | Chief Operating Officer | VP Service |
| `jrs:ehs` | Environment, Health & Safety | Chief Operating Officer | EHS Manager |
| `jrs:sales` | Sales | Chief Revenue Officer | VP Sales |
| `jrs:sales-applications-engineering` | Sales & Applications Engineering | Chief Revenue Officer | Director, Applications Engineering |
| `jrs:marketing` | Marketing | Chief Revenue Officer | VP Marketing |
| `jrs:customer-success-support` | Customer Success & Support | Chief Revenue Officer | VP Customer Experience |
| `jrs:accounting` | Accounting | Chief Financial Officer | Controller |
| `jrs:fpa` | Financial Planning & Analysis | Chief Financial Officer | FP&A Manager |
| `jrs:it` | Information Technology | Chief Information Officer | IT Manager |
| `jrs:security` | Security | Chief Information Security Officer | Security Manager |

## How loading works

- Claude always sees each skill and agent name and description.
- A full skill body loads only when that skill is used.
- A department reads its own `house-standards.md`; the other department bodies stay unloaded.
- Cross-department work is routed one department at a time to keep context focused.

## Models

The agents use the aliases `fable`, `opus`, `sonnet`, and `haiku`, so Claude Code resolves them to the model versions available in the user’s environment. The workflows include an Opus fallback for the Principal when Fable is unavailable.

After installing, use `/agents` to confirm the agent models and effort levels available to your account.

## Validation

Run the official Claude Code validator before publishing a change:

```sh
claude plugin validate --strict .
```

The GitHub Actions workflow runs the same check on every push and pull request.

## Limits

- Test each department with a small request before using it on live work.
- JRS produces drafts, recommendations, and work products. It does not send, post, release, deploy, or commit unless the user explicitly asks.
- People and Legal departments are deliberately not included.
