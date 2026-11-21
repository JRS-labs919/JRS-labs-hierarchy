# Assurance runtime

Read this only after Assurance is selected or required.

## Dispatch contract

Dispatch Stages 1–5 separately, in order, to the configured tier agent matching each row of the
department stage table. Do not combine stages. Each agent receives only its stage section, prior
handoff, applicable rules, inherited open items and record path. Wait for a stage before starting
work that depends on it.

The Advisor may perform integration and gating, but it does not replace an available independent
stage owner. If an agent is unavailable, run that stage in the session, label the fallback on
`MODELS:` and retain all evidence requirements.

## Assurance review

After Stage 4, send trigger 5 to the Principal using the escalation protocol. Stage 5 may deliver only
after a `consistent` or `consistent with conditions` ruling and completion of its conditions. A
`not consistent` ruling returns the affected work to the proper stage.

A material edit after any stage review or Principal review invalidates that review. Re-run the
affected review on the changed material; do not redo unrelated completed stages.

## Failure handling

- If the Fable Principal is unavailable or fails, use the Opus Principal for all later rulings in the
  run. Never claim a failed model ran and never redo completed work merely to change models.
- If neither Principal is available, the Advisor may make a provisional ruling only for triggers
  1–3 or 5 and must report `PRINCIPAL REVIEW: NOT REVIEWED - Principal not available`.
- For triggers 4 or 6 without a Principal or reachable user, make no change, return `blocked`, and
  name the qualified human role that must decide.
- Usage budgets never suppress these rules. Report any safety-required overrun explicitly.

