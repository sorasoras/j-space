# Capacity: task state and resumption

Use when decisions or evidence must survive stages, files, or interruptions.
Prefer an existing tracker that already carries the necessary state.
Direct work needs no ledger; Focused work may need only a brief note.
Persistent work benefits from a compact, task-scoped record.

## Record what will be needed again

```text
Goal: Requested outcome and observable completion criteria.
Constraints: Scope, compatibility, authorization, and relevant limits.
Decisions: Current choices and concise reasons.
Verified: Results with evidence references and coverage.
Open: Unresolved questions or explicitly provisional assumptions.
Next: First unfinished action, or complete when nothing remains.
```

Use only fields that help the task; a ledger is not a transcript.
Store facts, decision summaries, and evidence pointers, not private reasoning.
Keep credentials and unnecessary personal data out of the record.
Use a distinct task identity; do not overwrite another task's state.

## Manage a large task

1. Split work into bounded subtasks with clear completion criteria.
2. Keep shared constraints accessible to each subtask.
3. Summarize a completed subtask as result, evidence, scope, and remaining work.
4. Retain source references needed to verify or revise that summary.
5. Prioritize unfinished work by dependencies and consequences.

There is no universal limit on the number of ideas or entries.
Serialize work when dependencies require it; parallelize independent work when useful.
Compress stale detail while preserving decisions and access to supporting evidence.

## Update at meaningful changes

Record a consequential decision, completed phase, changed assumption, or failure.
Prepare a checkpoint before interruption when recovery would otherwise be costly.
Routine tool calls and ledger inspection need no accompanying write.
Mark corrected claims as superseded when their history matters for recovery.
A recorded pass remains limited to its tested inputs and version.

## Resume

1. Read the task record and recover the original requested outcome.
2. Inspect current artifacts and the evidence needed for the next decision.
3. Reconcile changed files, external state, and later user instructions.
4. Retain supported results; recheck only missing, stale, or disputed evidence.
5. Continue at the first unfinished action and update state if it changed.

A note saying an action was planned does not establish that it happened.
A note saying a test passed does not establish that changed code still passes.
If persistence is unavailable, use the conversation or task tracker.
The optional controller's interface is documented in [SKILL.md](../SKILL.md).

## Related workflows

- [Broadcast](broadcast.md): maintain facts shared across artifacts.
- [Markers](markers.md): recover after a failed approach.
- [Examples](../references/exemplars.md): see a resume and security scenario.

