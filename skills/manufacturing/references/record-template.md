# manufacturing Standard record template

```markdown
# <Name> - jrs:manufacturing
Track: New build | Running process    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Advisor <model>; tier agents <models/count or not used>; Principal <model or not used>
Usage: Lean | Balanced | Assurance - <tier-agent dispatches; Principal calls; budget status>

## 1. Order Review
What and how many:
Readiness inputs:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Process Plan
Branch: not needed | inline | jrs:quality stages x-y -> <run folder>, verdict
Approach:
Inspection and test points:
Operation list:
Order:
Risks:

## 3. Prepare log
- <step> - <status> - <plan changes, if any>

## 4. Readiness
| Criterion | Result | Evidence |
|---|---|---|

## Escalations
| # | Trigger | Question | Ruling | Conditions |
|---|---|---|---|---|

## 5. Open items
| # | Item | Type (TBD / REQUIRED INPUT / NOT RUN / discrepancy) | Owner |
|---|---|---|---|
```
