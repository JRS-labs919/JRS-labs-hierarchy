# JRS for Claude

[![Validate Claude plugin](https://github.com/JRS-labs919/JRS-labs-hierarchy/actions/workflows/validate.yml/badge.svg)](https://github.com/JRS-labs919/JRS-labs-hierarchy/actions/workflows/validate.yml)

JRS turns Claude into your own pocket-sized company—with you in the CEO chair. Claude gets 26
departments, a front-desk router, four low-usage support skills, eight specialist agents and an
optional experimental chain coordinator. A small draft can stay at one desk; consequential work can
still call the full boardroom. You set the direction; your AI company gets to work.

## Install JRS (plugin + all skills)

Install the **JRS plugin once**. It already includes the router, all 26 department skills, four
support skills, nine shared agents, and the department house-standard files. Do not install the standalone copies too;
their triggers overlap with the plugin.

### Claude, Claude Desktop, or Cowork

1. Open **Customize** and select **Plugins**.
2. Select **Add**, then **Add marketplace**.
3. Choose **Add from a repository** and enter `JRS-labs919/JRS-labs-hierarchy`.
4. Open **JRS Department Skills** from that marketplace and select **Add**.
5. Start a new chat or task, then use `/jrs:route` or a department command such as
   `/jrs:marketing`.

> [!IMPORTANT]
> Pasting the GitHub URL into a Claude Code chat does not install JRS. It only gives that session a
> clone of the source repository. Add the marketplace through **Customize > Plugins**, or use the
> Claude Code command below.

### Claude Code terminal

With Claude Code 2.1.292 or newer, install directly from this GitHub repository:

```sh
claude plugin install jrs --marketplace JRS-labs919/JRS-labs-hierarchy
```

On an older Claude Code release, add the marketplace and install the plugin in two steps:

```sh
claude plugin marketplace add JRS-labs919/JRS-labs-hierarchy
claude plugin install jrs@jrs-labs919-plugins
```

Start a new Claude Code session (or run `/reload-plugins`), then use:

- `/jrs:route` when you are not sure which department owns the work, or the request crosses departments.
- `/jrs:<department>` to go straight to one department, such as `/jrs:supply-chain`.

To try a local clone without installing it:

```sh
claude --plugin-dir .
```

### Update JRS

First check the installed version:

```sh
claude plugin list
```

- **Installed through Customize in Claude, Claude Desktop, or Cowork:** this is an account-synced
  install (shown as `jrs@synced` in Claude Code). Manage it in **Customize > Plugins** on claude.ai;
  the Claude Code update command cannot update an account-synced copy. Refresh or re-add the
  `JRS-labs919/JRS-labs-hierarchy` marketplace there, update or re-add **JRS Department Skills**, and
  start a new session.
- **Installed from a Claude Code marketplace:** refresh the marketplace, update the fully qualified
  plugin, and restart Claude Code:

  ```sh
  claude plugin marketplace update jrs-labs919-plugins
  claude plugin update jrs@jrs-labs919-plugins
  ```

If `jrs-labs919-plugins` is not listed by `claude plugin marketplace list`, add the marketplace first
using the install instructions above. Do not keep the account-synced copy and a local marketplace copy
enabled together; overlapping JRS versions can route unpredictably.

## Standalone skills (optional alternative)

The [`packages/standalone`](packages/standalone) directory contains all 31 current workflows as
individual `.skill` files. They include their references and editable house standards, but not the
plugin's shared agents. Use these when you want selected departments instead of the complete plugin.
Install `jrs-route.skill`, the support skills you want and only the departments you need.

Do not install the standalone skills and the plugin in the same account or environment: their
triggers overlap. The plugin is the complete JRS experience because it also includes shared agents
and per-department house-standard files.

## Customize before relying on it

Each department has a `house-standards.md` file beside its `SKILL.md`. Replace the `REQUIRED INPUT` lines with your company’s actual titles, rules, systems, approval limits, and record locations. Lines left as `REQUIRED INPUT` are ignored.

Run `/jrs:onboard` once in a company or project workspace to create `jrs/company-profile.md`. It
stores reusable context such as the offering, customer, tool names, terminology and output style—never
credentials. Departments read only the relevant sections when that file exists.

See [INSTALL-AND-CUSTOMISE.md](INSTALL-AND-CUSTOMISE.md) for the full setup guide.

## Included skills

| Skill | Department | Principal | Advisor |
|---|---|---|---|
| `jrs:route` | Router | — | — |
| `jrs:onboard` | Company context setup | — | — |
| `jrs:quick-draft` | Lean single-draft fast path | — | — |
| `jrs:quick-review` | Lean single-artifact review | — | — |
| `jrs:quick-analysis` | Lean bounded comparison or calculation | — | — |
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
- `/jrs:route` sends eligible one-department Lean drafts, reviews and analyses to compact task skills
  instead of loading the full department body.
- A department reads its own `house-standards.md`; the other department bodies stay unloaded.
- Assurance mechanics, escalation protocol and Standard record templates load only when their
  condition occurs. Small Lean work does not pay for them.
- Cross-department work is routed one department at a time, in the main session, so each department keeps its tier agents and its Principal. Only a short `HANDOFF:` block moves between them.

## Usage modes

JRS chooses the lightest mode that fits the consequence of the work. You can request a mode in the
prompt, such as `Run this in Lean mode` or `Run the full Assurance process`.

| Mode | Best for | Usage target |
|---|---|---|
| **Lean** | Small, low-risk, reversible work | 0-1 tier-agent dispatch |
| **Balanced** | Ordinary work and most chains; the default | Up to 2 tier-agent dispatches per department; 6 per chain |
| **Assurance** | Safety, regulatory, security, legal-impact, live, destructive, release or disposition work | Full five-stage dispatch plus required Principal review |

A request automatically upgrades to Assurance when trigger 4 or the department risk trigger fires.
Usage budgets never suppress a safety gate, blocking question or required Principal call. Every final
report includes a `USAGE:` line with the actual mode and dispatch count.

## Optional economy coordinator

Long Balanced chains normally stay in the main session because that is the reliable way to preserve
department agents, user questions and Principal access. A user may explicitly request the
**experimental economy coordinator** for a chain of at least three departments. JRS probes the
runtime first and uses it only when nested skill and agent dispatch are genuinely available. It is
never used for Assurance, and any failed probe falls back to the normal chain.

## Models

The agents use the aliases `fable`, `opus`, `sonnet`, and `haiku`, so Claude Code resolves them to the
model versions available in the user's environment. In Lean and Balanced, the Advisor stays on the
current session model. Configured tier agents handle only the bundled worker and review calls. A
Principal uses Fable when the session is on Fable and it is available, otherwise the Opus fallback;
it is called only when the evidence or Assurance mode requires it. The report states what actually ran
on its `MODELS:` line.

After installing, use `/agents` to confirm the agent models and effort levels available to your account.
The optional coordinator uses Sonnet / Medium only after explicit opt-in and a successful capability
probe.

## Validation

Run the official Claude Code validator before publishing a change:

```sh
claude plugin validate --strict .
python3 scripts/check_release.py
python3 scripts/check_usage_modes.py
python3 scripts/sync_department_contract.py
python3 scripts/check_prompt_budgets.py
python3 scripts/evaluate_results.py
python3 scripts/build_standalone.py
```

The GitHub Actions workflow runs the full validation suite on every push and pull request.

`tests/routing-prompts.md` lists prompts with the department each should route to. Run them through
`/jrs:route` (routing only) after any change to the router or to a skill description.
`tests/usage-mode-prompts.md` covers mode selection, budgets, upgrades and model behavior.
`tests/evals/cases.json` is the runtime release suite. Capture results using
`tests/evals/README.md`, then check them with `python3 scripts/evaluate_results.py <results.json>`.

## Limits

- Test each department with a small request before using it on live work.
- JRS produces drafts, recommendations, and work products. It does not send, post, release, deploy, or commit unless the user explicitly asks.
- People and Legal departments are deliberately not included.
- Every output is a draft for a named, qualified person to approve. A Principal review means "consistent with the criteria and the evidence"; it is never an approval, a stamp or a safety sign-off.
- If a department cannot reach tier agents, a Principal or the user from inside a subagent, it says
  `RAN FLAT` on its report and stops as `blocked` on any risk question.
- Dispatch targets are contractual, but exact token savings depend on the selected session model,
  prompt, attachments and Claude environment. Use the `USAGE:` line to compare runs.
