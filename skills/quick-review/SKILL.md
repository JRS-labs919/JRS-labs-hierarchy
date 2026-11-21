---
name: "quick-review"
description: Review one supplied artifact against a short checklist without loading a full department workflow. Used by jrs:route for Lean document, copy, calculation or configuration reviews, or directly with /jrs:quick-review. Not a compliance review, approval, certification, disposition or release sign-off.
---

# JRS-Quick-Review

Give one artifact a bounded, evidence-based review with no ceremonial process.

## Eligibility

Use only for a Small, reversible, single-department review where findings do not approve, certify,
release, disposition or accept risk. Exclude safety, legal interpretation, regulatory compliance,
security findings, production readiness and destructive/live actions. Route excluded work to the full
department in Assurance. Route a large or multi-artifact review to the full department in Balanced.

Read `DEPARTMENT:` from the router. If absent, read
`references/department-map.md` and choose from the requested review outcome. Ask one
either/or question only if the outcome leaves two materially different departments.

## Run

1. **Frame** — identify the artifact, intended audience/use and supplied criteria. When no checklist
   was supplied, propose 3–7 observable criteria and label them as the reviewer's working checklist.
2. **Context** — read only relevant company-profile sections and the chosen department's
   `house-standards.md`. An unresolved approval, safety, legal or regulatory requirement makes the
   request ineligible for this fast path.
3. **Review** — inspect the actual artifact. Report findings as `blocking`, `important` or `minor`,
   each with location, evidence and the smallest corrective action. Do not manufacture issues to fill
   categories.
4. **Verify** — ensure every criterion has `pass`, `fail` or `not checked` with a reason. Do not edit
   the artifact unless the user requested edits. Use no agent by default; one `builder-medium`
   independent read is permitted for an eligible artifact where a second reader materially helps.

## Report

```
VERDICT: <done | done with open items | routed to full department> - <n>/<n> criteria passed
DEPARTMENT: <jrs:department>
USAGE: Lean fast path - <0-1 tier-agent dispatches>; 0 Principal calls; <budget status>
REVIEWED: <artifact and path>
FINDINGS: <count by severity and location>
PRINCIPAL REVIEW: not used - findings are not approval or sign-off
NOT CHECKED: <criterion and reason>
OPEN ITEMS: <missing evidence or owner>
NEXT: <at most one useful follow-up>
```

