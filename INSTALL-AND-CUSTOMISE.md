# JRS department skills

Turn Claude into your own pocket-sized company, with you as CEO: a front-door router plus 26
departments, each with a five-stage team led by a Principal, an Advisor and one owner per stage.
Hardware and software work are tracks inside each department.

## Two ways to install - pick one

- **Plugin** (recommended): it includes the router, every department, eight agents that carry each
  role's model and effort, and a `house-standards.md` per department. In Claude, Claude Desktop, or
  Cowork, open **Customize > Plugins > Add > Add marketplace**, choose **Add from a repository**,
  enter `JRS-labs919/JRS-labs-hierarchy`, then add **JRS Department Skills**. In a Claude Code
  terminal, run `claude plugin install jrs --marketplace JRS-labs919/JRS-labs-hierarchy`.
  Invoke it as `/jrs:route` or `/jrs:<department>`.
- **Standalone skills** (`packages/standalone/*.skill`): use these only when you want selected
  departments instead of the complete plugin. Start with `jrs-route.skill`, then add only the
  departments you need.

Do not install both: their triggers overlap.

Pasting the repository URL into a Claude Code chat only clones the source for that session. It does
not install the plugin or activate its skills.

## Update an existing plugin

Run `claude plugin list` to see how JRS is installed.

- If it appears as `jrs@synced`, it came from the Claude account. Update it from **Customize >
  Plugins** on claude.ai, not from the Claude Code terminal. Refresh or re-add the
  `JRS-labs919/JRS-labs-hierarchy` marketplace, update or re-add **JRS Department Skills**, and start
  a new session.
- If it appears as `jrs@jrs-labs919-plugins`, run:

  ```sh
  claude plugin marketplace update jrs-labs919-plugins
  claude plugin update jrs@jrs-labs919-plugins
  ```

  Then restart Claude Code. If that marketplace is missing, add it again using the install command
  above.

Do not keep two JRS plugin copies enabled together. A local `--plugin-dir` test can temporarily load a
release checkout, but an older account-synced copy may still be visible on disk and cause confusion.

## Make it yours

- Each skill follows your company's own standards first (Ground rule 1). In the plugin, fill in each
  department's `house-standards.md`; lines left as `REQUIRED INPUT` are ignored.
- Role titles are generic. Replace them with yours in the role tables, or in house-standards.md.
- People and Legal are deliberately not included.

## Models

| Role | Model behavior |
|---|---|
| Advisor | Stays on the current session model in Lean and Balanced |
| Principal | Fable when the session is on Fable and it is available; otherwise Opus fallback; only when invoked |
| Balanced worker | Sonnet / High for the bundled build, then Opus / High for independent review |
| Assurance stages | Opus, Sonnet or Haiku per the department stage table |

Every report shows a `MODELS:` line naming what actually ran. If the environment cannot set a tier
model, the Advisor runs that work in the session, records the fallback and reports zero tier-agent
dispatches for it.

## Usage modes

- **Lean:** Small, low-risk and reversible; zero or one tier-agent dispatch.
- **Balanced:** ordinary default; at most two tier-agent dispatches per department and a target of six
  for a chain.
- **Assurance:** the full five-stage process for high-consequence work or when the user asks for it.

The mode can upgrade but cannot downgrade after a department starts. Trigger 4, trigger 6 and every
required safety or Principal call run even when they exceed the usage target. Ask for a mode in the
request, or let JRS choose. The final `USAGE:` line shows what happened.

## Skills

| Skill | Department | Principal | Advisor |
|---|---|---|---|
| `jrs:route` | Router - picks the department and chains them | - | - |
| `jrs:product-management` | Product Management | Chief Product Officer | VP Product |
| `jrs:npi-program-management` | NPI & Program Management | Chief Product Officer | Director, PMO |
| `jrs:design-hw` | Design - Industrial Design | Chief Product Officer | Head of Design |
| `jrs:design-sw` | Design - UX/UI | Chief Product Officer | Head of Design |
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

## Known limits

- Not tested on live work in your environment; run one small request per department you rely on.
- Plugin agent fields `model` aliases (`fable`, `opus`, `sonnet`, `haiku`) and `effort` should be
  confirmed after install (for example with `/agents` in Claude Code).
- Runtime token savings depend on the chosen session model and inputs; compare the `USAGE:` dispatch
  counts during initial testing.
- Every skill produces drafts and recommendations. It never sends, posts, releases, deploys or
  commits anything unless the user asks.
