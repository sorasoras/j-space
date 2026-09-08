# Directed focus: maintain task constraints

Use when repetitive work can lose an important requirement.
Examples include compatibility, target language, naming, tone, and scope limits.
Translate the requirement into an observable check on the work.

## Choose the constraint

1. Read the relevant instruction and preserve its actual meaning.
2. State the required behavior in concrete terms.
3. Identify where that behavior could be lost during this task.
4. Choose a proportionate check at those points or before delivery.

Keep all binding constraints; do not impose a fixed number of active items.
Group a long list by phase or artifact so each check remains manageable.
Use a task note only when the constraint needs to survive later stages.

## Make the constraint actionable

```text
Requirement: Preserve the existing public API.
Apply: Change internal parsing without renaming exported functions.
Check: Compare exported signatures and run the relevant compatibility tests.
```

A slogan such as "compatibility" is less useful than a checkable requirement.
Repeating the slogan does not demonstrate that the output complies.

## Work through a long stretch

- Apply the constraint where the work is produced.
- Review at a phase change or a point where mistakes would propagate.
- After a user correction, identify and revise affected earlier work.
- Before delivery, inspect the resulting artifact against the requirement.

Do not interrupt every tool call to restate the constraint.
If it is repeatedly missed, improve the checklist, test, or task decomposition.

## Handle exclusions accurately

Prefer a concrete positive instruction when it improves execution:
"Use public API data" can clarify how to satisfy "do not query private tables."
Retain the original prohibition when it defines a security or scope boundary.
Do not weaken exclusions, reinterpret them as preferences, or drop them from checks.
A negative instruction is valid even without a convenient positive equivalent.

## Repair a missed constraint

1. Identify the affected output and the observable discrepancy.
2. Correct that output and any dependent work.
3. Run a targeted check that would catch the same mistake.
4. Record the correction only if it matters for continuation or handoff.

For writing tasks, inspect language, terminology, length, and required structure.
For calculations, check units and the relevant numerical result independently.
For code, prefer existing lint, type, or behavior checks where applicable.

See [Broadcast](broadcast.md) for shared constraints across artifacts and
[Capacity](capacity.md) for preserving them across interruptions.

