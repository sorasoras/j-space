# Shorthand: compact, readable task notes

Use when a durable task record needs to be easier to scan or resume.
Compress facts and decision summaries without losing their scope or provenance.
Short tasks do not need a special notation or a separate note.

## Keep useful information

1. Retain the goal, binding constraints, decisions, evidence, and unfinished work.
2. Remove repeated narrative and details that can be recovered from linked artifacts.
3. Preserve units, quantifiers, exceptions, and version information when relevant.
4. Define a local abbreviation at first use if its meaning is not obvious.
5. Prefer ordinary words when notation would make recovery harder.

There is no fixed word count per entry.
The record should be understandable from its text and referenced evidence.
Do not request, expose, or reconstruct private chain-of-thought.

## Label consequential claims

| Label | Meaning |
|---|---|
| Observed | Directly supported by a cited source, artifact, or test result. |
| Inferred | Follows from stated evidence and assumptions. |
| Assumed | Provisional premise for conditional work. |
| Open | Unresolved question affecting the task. |
| Refuted | Rejected by identified contrary evidence. |
| Superseded | Replaced after a change; old scope may still matter. |

Labels are optional aids, not decorations required on every sentence.
A label does not strengthen the underlying evidence.
An assumption may be explored without silently promoting it to fact.

## Example

```text
Observed: Import tests pass for comma/tab delimiters (local run, current revision).
Open: Quoted multiline field fails in supplied fixture.
Decision: Reuse the existing parser; preserve exported signatures.
Next: Verify multiline content and rerun affected delimiter cases.
```

This records the state needed to continue without reproducing the exploration.
Include a test command or result location when later verification needs it.
Avoid copying full logs, credentials, or unrelated personal information.

## Check clarity when needed

At a handoff or when an entry is ambiguous, read it without relying on unstated context.
Resolve an undefined name, missing unit, or unclear reference against the source.
If the evidence cannot be recovered, keep the entry's uncertainty visible.
Do not treat a fluent expansion of an unsupported note as validation.

## Fit the recipient

Use plain, complete language for user-facing conclusions and progress updates.
Keep domain notation, formulas, code, and quoted text when they help the reader.
Tool arguments must follow their schemas and execution semantics.
Neither a universal prose-only rule nor an audit at every tool call is needed.

See [Capacity](capacity.md) for what to persist and
[Broadcast](broadcast.md) for consistent definitions across artifacts.

