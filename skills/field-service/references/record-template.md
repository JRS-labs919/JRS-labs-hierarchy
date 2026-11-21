# field-service Standard record template

```markdown
# <Name> - jrs:field-service
Track: Startup | Service    Work: new | change    Size: Standard    Mode: autonomous | gated
Models: Advisor <model>; tier agents <models/count or not used>; Principal <model or not used>
Usage: Lean | Balanced | Assurance - <tier-agent dispatches; Principal calls; budget status>

## 1. Work Order
Equipment and task:
Site conditions:
Done when:
- [ ] AC1
In scope:
Out of scope:
Must not break: (change work)
Constraints / house rules adopted:
Assumptions and TBD:

## 2. Job Plan
Branch: not needed | inline | jrs:ehs stages x-y -> <run folder>, verdict
Approach:
Parts, tools and people:
Scope of work:
Order:
Hazard analysis: <reference, date> | branched
Energy isolation: LOTO ref | arc-flash/shock boundary | PPE (or REQUIRED INPUT)
Risks:

## 3. Prepare log
- <step> - <status> - <plan changes, if any>

## 4. Review
| Criterion | Result | Evidence |
|---|---|---|

## Escalations
| # | Trigger | Question | Ruling | Conditions |
|---|---|---|---|---|

## 5. Open items
| # | Item | Type (TBD / REQUIRED INPUT / NOT RUN / discrepancy) | Owner |
|---|---|---|---|
```
