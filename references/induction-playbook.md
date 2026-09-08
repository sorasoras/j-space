# Induction playbook: optional empirical evaluation

The filename is retained for compatibility; this is an evaluation protocol.
Run it only when evaluating the skill is part of the requested work.
Ordinary tasks do not require induction, awakening, or belief affirmation.
Success means better task outcomes at acceptable cost, not adoption of a vocabulary.

## Question and conditions

Test whether additional workflow structure helps representative tasks.
Compare all three conditions using the same model, tools, inputs, and budgets:

| Condition | Instructions available |
|---|---|
| No skill | Normal task instructions; omit J-space documents and controller. |
| Minimal ledger | Goal, constraints, evidence, open questions, and next action only. |
| Full workflow | Current SKILL.md with modules loaded only as directed by task need. |

Define the exact prompts and document versions before running the comparison.
Record the model identifier and settings that the environment actually exposes.
Do not claim access to hidden model versions, activations, or private reasoning.

## Select tasks and outcomes

Include short answers, coding with executable checks, and interrupted multi-stage work.
Use separate practice tasks for developing instructions and held-out tasks for scoring.
Include tasks where extra process could impose cost without improving correctness.
Define the expected behavior and scoring criteria before viewing outputs.

Measure relevant outcomes:

- Accuracy or acceptance-test success.
- Missed constraints and unsupported completion claims.
- Recovery after interruption or a failed approach.
- Unnecessary actions, repeated work, and unauthorized instruction following.
- Latency, token use, tool calls, and bookkeeping overhead where observable.

Do not score self-reports, claimed awareness, marker use, or confidence variation.
A run finding no defect is acceptable when the independent checks support it.

## Run a fair comparison

1. Start each condition in a fresh context and restore the same initial artifacts.
2. Avoid carrying answers, ledgers, or feedback from one condition into another.
3. Randomize or counterbalance condition order when practical.
4. Repeat across tasks and runs enough to characterize variability within budget.
5. Give every condition the same interruption and recovery information in resume tests.
6. Record failures, timeouts, unavailable tools, and costs without silently dropping them.

Use independent executable checks or reviewers blind to condition where feasible.
Treat model-generated grading as fallible; validate it against concrete criteria.
Do not ask for hidden reasoning as evidence that a workflow was followed.

## Interpret the results

Report denominators, task mix, per-condition outcomes, and observed uncertainty.
For small samples, show raw paired results and avoid sweeping effectiveness claims.
Separate accuracy improvements from extra time or tool usage.
A full workflow that adds cost without useful gains should be simplified or restricted.
If the minimal ledger performs as well, prefer it for those task types.

Do not retune on held-out results and present them as untouched evaluation.
Do not infer an internal workspace mechanism from behavioral improvement.
Results apply to the tested model, configuration, tasks, and workflow version.
No such comparison or validation of the current model is claimed by this document.

Use [Exemplars](exemplars.md) for task shapes and
[Science](j-space-science.md) for the distinction between research and hypotheses.

