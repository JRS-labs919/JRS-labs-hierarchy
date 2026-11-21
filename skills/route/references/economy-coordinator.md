# Experimental economy coordinator

Load this only when the user explicitly requests the experimental or economy coordinator for a
Balanced chain of at least three departments.

This path attempts to keep long-chain coordination on one Sonnet coordinator while the main session
waits for a result. It is off by default because some Claude environments do not allow a subagent to
invoke skills or nested tier agents.

## Eligibility

- The user explicitly requested this experimental path.
- The route is a Balanced chain with at least three departments.
- No known Assurance condition, live/destructive action or required user gate exists.
- The chain order and expected deliverable are already clear.

## Probe before work

Dispatch `chain-coordinator` with `PROBE ONLY`. Continue only when it reports `available`, confirms it
can invoke JRS skills, confirms those skills retain tier-agent dispatch, and can write a ledger. Any
`no`, missing field or failed probe falls back to the normal main-session chain without penalty.

## Run

Create `jrs/chains/<yyyy-mm-dd>-<topic>.md` and send the coordinator:

```
ORIGINAL REQUEST: <unchanged>
CHAIN: <name and fixed department order>
RUN MODE: Balanced
USAGE BUDGET: <=6 tier-agent dispatches total
LEDGER: <path>
RETURN ON: user question | Assurance upgrade | flat department | blocked | budget overrun
```

The coordinator runs one department at a time and appends each compact report and handoff. If it
returns control, resume in the main session from the ledger; never rerun completed departments.
Report the coordinator probe/call in `MODELS:` and `USAGE:` separately from department tier-agent
counts.

