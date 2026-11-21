# Escalation protocol

Send a compact packet, not the conversation:

```
ESCALATION <n> - trigger <1-6>
QUESTION: <one sentence>
OPTIONS: <A / B / C, one line each>
EVIDENCE: <sources, results and file paths>
ADVISOR RECOMMENDS: <option and one-line reason>
```

The Principal returns:

```
RULING <n>: <option chosen | other: ...> - <one- or two-line reason>
CONDITIONS: <required checks or changes, if any>
```

Wait for the ruling before dependent work. Apply and record every condition. A material edit to the
reviewed content invalidates the ruling and requires re-review of the affected material.

Use `principal` when an available Fable model is named by the current system prompt; otherwise use
`principal-opus`. If the Fable call fails, use Opus for later calls and do not redo completed work.
If neither runs, an Advisor ruling is provisional and is never reported as a Principal review. For
trigger 4 or 6, the only permitted fallback is no change and a `blocked` verdict until the user or a
qualified human decides.

For trigger 5, the permitted rulings are `consistent`, `consistent with conditions`, or
`not consistent`, judged only against Stage 1 criteria and recorded evidence. This is not approval,
certification, disposition, risk acceptance or safety sign-off.

