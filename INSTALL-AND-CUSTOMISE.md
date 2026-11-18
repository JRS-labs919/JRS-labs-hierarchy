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

## Make it yours

- Each skill follows your company's own standards first (Ground rule 1). In the plugin, fill in each
  department's `house-standards.md`; lines left as `REQUIRED INPUT` are ignored.
- Role titles are generic. Replace them with yours in the role tables, or in house-standards.md.
- People and Legal are deliberately not included.

## Models

| Role | Fable available | Fallback (no Fable, or usage ran out) |
|---|---|---|
| Principal | Fable 5.2 / Max | Opus 5.5 / Max |
| Advisor | Fable 5.2 / Medium | Opus 5.5 / Max |
| Stage roles | Opus 5.5, Sonnet 5.5 or Haiku 5.5, per the skill's table | unchanged |

The model is checked once at the start; a Fable failure mid-job switches to the fallback for the rest
of the job. Every report shows a `MODELS:` line. If your environment cannot set a model per role, the
skill runs that stage in the session and says so.

## Skills

| Skill | Department | Principal | Advisor |
|---|---|---|---|
| `jrs-route` | Router - picks the department and chains them | - | - |
| `jrs-product-management` | Product Management | Chief Product Officer | VP Product |
| `jrs-npi-program-management` | NPI & Program Management | Chief Product Officer | Director, PMO |
| `jrs-design-hw` | Design - Industrial Design | Chief Product Officer | Head of Design |
| `jrs-design-sw` | Design - UX/UI | Chief Product Officer | Head of Design |
| `jrs-hardware-engineering` | Hardware Engineering | Chief Technology Officer | VP Hardware Engineering |
| `jrs-software-engineering` | Software Engineering | Chief Technology Officer | VP Software Engineering |
| `jrs-platform-infrastructure` | Platform & Infrastructure | Chief Technology Officer | VP Platform |
| `jrs-data-ai` | Data & AI | Chief Technology Officer | Head of Data |
| `jrs-systems-engineering` | Systems Engineering | Chief Technology Officer | Chief Systems Engineer |
| `jrs-engineering-systems` | Engineering Systems | Chief Technology Officer | Manager, Engineering Systems |
| `jrs-technical-publications` | Technical Publications | Chief Technology Officer | Technical Publications Manager |
| `jrs-manufacturing` | Manufacturing | Chief Operating Officer | Plant Manager |
| `jrs-supply-chain` | Supply Chain | Chief Operating Officer | VP Supply Chain |
| `jrs-quality` | Quality | Chief Operating Officer | VP Quality |
| `jrs-project-delivery` | Project Delivery | Chief Operating Officer | Director, Project Management |
| `jrs-field-service` | Field Service & Commissioning | Chief Operating Officer | VP Service |
| `jrs-remote-monitoring` | Remote Monitoring / NOC | Chief Operating Officer | VP Service |
| `jrs-ehs` | Environment, Health & Safety | Chief Operating Officer | EHS Manager |
| `jrs-sales` | Sales | Chief Revenue Officer | VP Sales |
| `jrs-sales-applications-engineering` | Sales & Applications Engineering | Chief Revenue Officer | Director, Applications Engineering |
| `jrs-marketing` | Marketing | Chief Revenue Officer | VP Marketing |
| `jrs-customer-success-support` | Customer Success & Support | Chief Revenue Officer | VP Customer Experience |
| `jrs-accounting` | Accounting | Chief Financial Officer | Controller |
| `jrs-fpa` | Financial Planning & Analysis | Chief Financial Officer | FP&A Manager |
| `jrs-it` | Information Technology | Chief Information Officer | IT Manager |
| `jrs-security` | Security | Chief Information Security Officer | Security Manager |

## Known limits

- Not tested on live work in your environment; run one small request per department you rely on.
- Plugin agent fields `model` aliases (`fable`, `opus`, `sonnet`, `haiku`) and `effort` should be
  confirmed after install (for example with `/agents` in Claude Code).
- Every skill produces drafts and recommendations. It never sends, posts, releases, deploys or
  commits anything unless the user asks.
