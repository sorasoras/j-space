# Deep reasoning: dependencies and supporting checks

Use when a conclusion depends on missing facts, several transformations, or cases.
The useful output is a supported result and an explanation suited to the reader.
Do not request or reconstruct private chain-of-thought as a verification method.

## Frame the problem

1. Identify the requested result and constraints from the actual request.
2. Note ambiguities that materially change the answer.
3. Use sensible defaults for routine choices; state important assumptions.
4. Identify the intermediate facts needed to support the conclusion.

For a small problem, solve it directly without a formal record.
For a larger problem, retain only dependencies needed for checking or resumption.

## Build a checkable result

- Separate sourced facts, derived conclusions, and provisional assumptions.
- Check an uncertain intermediate before treating it as established.
- Conditional work may proceed from a labeled assumption; preserve that condition.
- Keep quantities, units, domains, and case boundaries explicit.
- Look for omitted cases and premises stronger than the source supports.

A plausible explanation can be wrong even when it sounds orderly.
Verify the mathematical or factual relationship, not a report of when it occurred.

## Select an independent check

Choose a check that could expose the likely error:

- Arithmetic: recalculate independently or use a calculator.
- Algebra: substitute the result into the original equation and check the domain.
- Algorithms: compare small inputs with a simpler reference implementation.
- Factual chains: verify the key link against an appropriate primary source.
- Arguments: test a counterexample or inspect the strongest competing account.

Two paraphrases of the same assumption do not make independent checks.
Finite examples can refute a general claim; passing examples alone do not prove it.

## Structured and multilingual output

For constrained writing, outline the needed sections or anchor requirements first.
Check the finished artifact against those requirements, including language and format.
Translate terms consistently; preserve technical distinctions and quoted source text.
Language switching alone is not evidence of a reasoning failure.

## When the approach stalls

Identify the specific unresolved dependency or failing assumption.
Try a concrete example, a different representation, or a discriminating test.
Preserve supported results instead of restarting unrelated work.
If evidence cannot settle the question, state the resulting limit precisely.

## Delivery

Give the result with essential supporting steps, sources, and material assumptions.
A requested proof or calculation should be complete enough to check independently.
Omit process narration that does not help the reader assess or use the result.

See [Empirics](empirics.md) for experiments and [Markers](markers.md) for recovery.

