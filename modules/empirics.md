# Empirics: resolve uncertainty with evidence

Use when an uncertain claim can be tested, measured, or checked against a source.
Choose the smallest useful check that could expose the suspected error.
Use more extensive testing when consequences or unresolved uncertainty justify it.

## Define the question

1. State the unknown and why it changes the next action.
2. Identify plausible alternatives without treating the list as exhaustive.
3. Choose an observation that distinguishes them.
4. Specify inputs, expected outcomes, and the check's limitations.

Do not force every question into a finite candidate set.
Sampling a continuous or large space requires an explicit coverage limitation.
When direct evidence is unavailable, report the uncertainty instead of inventing a test.

## Choose independent evidence

- Code: compare against a simple reference with different implementation assumptions.
- Mathematics: use substitution, exhaustive small cases, or a counterexample.
- Factual work: consult a primary source with the relevant date and scope.
- UI behavior: exercise the user's path and inspect the observable result.

A reference can be wrong. Check its specification and basic cases separately.
Shared libraries, copied formulas, or copied sources can create correlated errors.
State important shared assumptions rather than calling such agreement independent.

## Run and inspect

1. Reproduce the relevant failure when feasible.
2. Run targeted normal, boundary, and failure cases.
3. Add randomized or exhaustive cases when they can reveal a plausible missed error.
4. Record actual outputs and distinguish failure, timeout, and unavailable tooling.
5. Inspect a mismatch before changing either the candidate or the expected result.

For randomized checks, retain the seed or failing input needed to reproduce a failure.
Do not modify expected results merely to make the candidate pass.
A useful passing result is legitimate; a test need not uncover a defect.

## Recover from a mismatch

Reduce the input until the disagreement is understandable.
Check whether the candidate, reference, specification, or environment is at fault.
Revise the unsupported assumption and rerun affected checks.
Preserve a meaningful regression case when it protects against recurrence.

## Record the scope

```text
Result: Candidate matched independent enumeration for all inputs of length 0–6.
Evidence: Test command, implementation version, and reproducible result location.
Limit: Larger inputs and performance limits were not covered by this comparison.
Next: Establish the general invariant or narrow the claim to tested behavior.
```

Testing examples is not a proof of universal correctness.
A failed command is not evidence that the intended behavior was exercised.
Summarize what the evidence permits the next stage to rely on.
Stop expanding checks once requirements are met and no material concern remains.

See [Deep reasoning](deep-reasoning.md) for general arguments and
[Self-monitoring](self-monitoring.md) for claim calibration and completion.

