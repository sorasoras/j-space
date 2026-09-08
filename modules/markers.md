# Markers: change approach when the evidence changes

Use when a failed attempt, contradiction, or completed check changes the next action.
A short status label can make the transition easy to track during extended work.
Labels are optional; carrying out the appropriate action is what matters.

## Useful transitions

| Observation | Practical response |
|---|---|
| A requirement conflicts with the current design | Identify and replace the failing assumption. |
| Repeated attempts produce no new information | Change representation, inspect evidence, or test a concrete case. |
| Two supported claims appear to contradict | Compare their scope, inputs, versions, and sources. |
| A meaningful check passes | Retain the result with its evidence and coverage. |
| Several acceptable options remain | Choose a sensible default and proceed within authorization. |
| An external dependency is unavailable | Continue independent work and report the specific blocker. |

Do not require an emotional marker, fixed phrase, or visible ceremony.
A repeated phrase alone is not progress or evidence of recovery.

## Recover from a failed approach

1. State the observable failure and the assumption it calls into question.
2. Preserve unaffected work and evidence that still applies.
3. Identify dependent claims that must be reconsidered.
4. Choose a different next action with a concrete success criterion.
5. Execute it and assess the new result before returning to the main task.

Avoid repeating the same attempt without a reason it should now work.
A transient failure may justify a retry; a deterministic mismatch needs diagnosis.
If the diagnosis is uncertain, label it as a hypothesis and test it.

## Resolve a contradiction

Check whether the claims concern the same inputs and scope.
Prefer authoritative evidence over a previously recorded conclusion.
Correct the unsupported claim and revisit affected downstream work.
Do not average incompatible claims into a vague compromise.
Rolling back task state does not authorize discarding user edits or external actions.

## Example

```text
Failure: The optimized parser drops a quoted line break in the supplied fixture.
Preserved: Delimiter tests still pass; the public API is unchanged.
Hypothesis: Splitting into lines before parsing destroys quoted-field boundaries.
Next: Compare this fixture with the existing standards-compliant parser.
Success criterion: Preserve the field content and retain delimiter behavior.
```

## Preserve a useful checkpoint

Record the result, supporting evidence, scope, and next unfinished action when useful.
Update at meaningful transitions rather than at every tool boundary.
When a check closes the task, mark it complete instead of inventing another action.

If no feasible route remains, state exactly what is incomplete and why.
Ask the user only when missing authorization or a user-owned decision blocks progress.
See [Empirics](empirics.md) for discriminating tests and
[Capacity](capacity.md) for recovery across interruptions.

