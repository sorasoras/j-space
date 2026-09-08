# Broadcast: shared facts and consistency

Use when several sections, files, or subtasks depend on the same facts.
Keep an authoritative task record so changes propagate to every affected use.
For a single short answer, a separate record usually adds no value.

## Establish the shared facts

1. Identify recurring names, values, units, constraints, and definitions.
2. Record each once with its source and applicable scope.
3. Distinguish user decisions, observed facts, and provisional assumptions.
4. Point dependent work to that record instead of inventing local variants.

Keep as many entries as the task needs; group related entries for readability.
A shared record makes disagreement findable, but does not make an entry true.
Resolve conflicts against the user's request and relevant authoritative evidence.

## Reuse a result

Before repeating expensive work, check whether an existing result covers the need.
Reuse it when its inputs, version, assumptions, and scope still match.
Recheck when evidence is missing, stale, contradicted, or independently needed.
Agreement between copied results is not independent corroboration.

## Propagate a change

1. Update the canonical value and briefly record why it changed.
2. Identify dependents through references, search, or the task's artifact list.
3. Update affected sections, calculations, examples, and tests.
4. Invalidate conclusions that relied on the old value where necessary.
5. Search for stale uses and inspect legitimate exceptions before replacing them.

Do not assume editing the record automatically updates external artifacts.
Do not globally replace matching text without checking its meaning in context.

## Example

```text
Decision: Request timeout is 30 seconds; user approved this value.
Scope: HTTP client only; database timeout remains 10 seconds.
Dependents: Client configuration, settings help, timeout test.
Change check: Each dependent uses 30 seconds with consistent units.
```

## Delivery check

Compare shared names, numbers, units, and definitions across the deliverables.
Explain intentional differences where they could confuse the reader.
Report a consistency check only over artifacts actually inspected.
An audit may find no conflicts; do not manufacture one.

## Related workflows

- [Capacity](capacity.md): preserve shared state across interruptions.
- [Directed focus](directed-focus.md): apply a recurring constraint.
- [Empirics](empirics.md): resolve disputed facts with independent evidence.

