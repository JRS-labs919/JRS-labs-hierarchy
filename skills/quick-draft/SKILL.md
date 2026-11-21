---
name: "quick-draft"
description: Create one small, low-risk business draft without loading a full department workflow. Used by jrs:route for Lean emails, briefs, summaries, outlines and internal content, or directly with /jrs:quick-draft. Not for publishing, regulated claims, contracts, safety instructions or release decisions.
---

# JRS-Quick-Draft

Produce one usable draft with the smallest safe workflow. This is a Lean single-department fast path,
not a miniature five-agent chain.

## Eligibility

Use this skill only when the work is Small, reversible, limited to one draft, and has no live send or
publish action, legal interpretation, regulated claim, safety instruction, security-sensitive detail,
formal approval, disposition, release or risk decision. If any condition fails, return the request to
the named full department in Balanced or Assurance mode before drafting.

Read `DEPARTMENT:` from the router. If absent, read
`references/department-map.md`, choose one department from the requested deliverable and
state it. If two materially different departments remain, ask one either/or question.

## Run

1. **Frame** — state the audience, purpose, format, source facts and 2–5 checkable criteria in no more
   than six lines. Use labelled assumptions for noncritical gaps; never invent names, numbers, claims
   or commitments.
2. **Context** — read only relevant sections of `jrs/company-profile.md` when it exists, then the
   selected department's `house-standards.md` when that department is installed and readable. Ignore
   `REQUIRED INPUT` lines unless a
   missing approval, legal, regulatory or safety rule makes the draft ineligible.
3. **Draft** — create the smallest complete artifact in the requested location or in the response.
   Do not send, publish, post or approve it.
4. **Check** — verify every criterion, source-sensitive statement, requested tone and obvious spelling
   or formatting issue. Use no agent by default. One `builder-medium` independent read is allowed only
   when the artifact has enough consequence to justify it but still meets fast-path eligibility.

## Report

```
VERDICT: <done | done with open items | routed to full department>
DEPARTMENT: <jrs:department>
USAGE: Lean fast path - <0-1 tier-agent dispatches>; 0 Principal calls; <budget status>
DELIVERED: <artifact and path>
CHECKED: <criteria result>
PRINCIPAL REVIEW: not used - fast path cannot approve, release or accept risk
DECISIONS MADE FOR YOU: <labelled assumptions>
OPEN ITEMS: <TBD, REQUIRED INPUT or source-sensitive claims>
NEXT: <at most one useful follow-up>
```

