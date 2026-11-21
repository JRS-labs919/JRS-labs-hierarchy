---
name: "quick-analysis"
description: Perform one bounded, low-risk comparison or calculation from supplied data without loading a full department workflow. Used by jrs:route for Lean summaries, estimates and option comparisons, or directly with /jrs:quick-analysis. Not for forecasts, regulated calculations, safety limits, formal financial decisions or production changes.
---

# JRS-Quick-Analysis

Answer one bounded question from supplied, readable inputs and expose the evidence behind the answer.

## Eligibility

Use only for Small, reversible, single-department analysis with one decision question and no safety
limit, regulated method, accounting posting, formal forecast/budget, security risk rating, release,
disposition or live action. Route ineligible work to the full department in Balanced or Assurance.

Read `DEPARTMENT:` from the router. If absent, read
`references/department-map.md` and choose based on the requested decision or deliverable.
Ask one either/or question only when two outcomes are materially different.

## Run

1. **Question** — restate the decision question, inputs, requested output and 2–5 pass criteria.
2. **Context** — read only relevant company-profile sections and the selected department's
   `house-standards.md`. A missing required method, limit or approval boundary makes this fast path
   ineligible.
3. **Analyze** — show the source of every input, units, transformations and material assumptions.
   Missing values remain `TBD`; do not silently substitute industry averages. Keep sensitivity work
   to variables that could change the conclusion.
4. **Check** — reproduce arithmetic or run an appropriate lightweight check. Compare units and totals.
   Use no agent by default; one `builder-medium` independent check is allowed when it materially
   reduces error and the job remains eligible.
5. **Conclude** — answer the bounded question and distinguish evidence from recommendation. Never
   present the result as approval, professional advice or authority to act.

## Report

```
VERDICT: <done | done with open items | routed to full department> - <n>/<n> criteria passed
DEPARTMENT: <jrs:department>
USAGE: Lean fast path - <0-1 tier-agent dispatches>; 0 Principal calls; <budget status>
ANSWER: <one-line result>
EVIDENCE: <sources, formula or check>
PRINCIPAL REVIEW: not used - analysis is not approval or authority to act
ASSUMPTIONS: <material assumptions>
OPEN ITEMS: <TBD, missing method or source>
NEXT: <at most one useful follow-up>
```

