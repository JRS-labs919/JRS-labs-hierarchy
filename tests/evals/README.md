# JRS runtime evaluations

`cases.json` is the small, stable release suite. It measures routing and usage behavior instead of
searching prompt source text alone.

Run every prompt through `/jrs:route`, except E07 which uses `/jrs:onboard`. Use fictional inputs and
a fresh session for each case. Save one JSON object per result in an array:

```json
{
  "id": "E01",
  "selected_skill": "jrs:quick-draft",
  "department": "jrs:sales",
  "mode": "Lean",
  "tier_dispatches": 0,
  "principal_calls": 0,
  "final_output": "the complete final response",
  "notes": "optional observed issue"
}
```

Then run:

```sh
python3 scripts/evaluate_results.py path/to/results.json
```

The evaluator checks selected skill, department, mode, dispatch budgets and mandatory report labels.
It does not claim to assess the quality of the deliverable. Include transcripts, created artifacts,
the result JSON and environment/model details in any retest zip so a release reviewer can inspect
failures rather than only a pass count.

