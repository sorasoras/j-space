# J-Space

A practical agent skill for preserving task state, evidence, and constraints across long-running work.

J-Space uses a lightweight workspace metaphor. It does not claim consciousness, access to model activations, or proven performance gains from self-induction. Simple questions and routine edits bypass the workflow.

## What it provides

- Direct, focused, and persistent workflows selected by task needs.
- Nine optional modules for task state, consistency, verification, uncertainty, and recovery.
- A standard-library Python ledger controller with task isolation, atomic updates, and write locking.
- Read-only inspection and structured verification records with scope and evidence.
- Research context and an optional comparative evaluation protocol.

Start with [SKILL.md](SKILL.md). Controller details are in [workspace-ledger.md](scripts/workspace-ledger.md).

## Install

Clone the repository into your agent's skill directory, using `j-space` as the folder name. For ZCode:

```sh
git clone https://github.com/sorasoras/j-space.git ~/.zcode/skills/j-space
```

Authenticate with GitHub first when the repository is private. If that directory already exists, preserve it before replacing it; do not clone over an installed copy. Other compatible agents can use their own skill directories.

The skill itself does not require Python. The optional controller requires Python 3.10 or newer and has no third-party dependencies.

## Controller example

Run from the task's working directory. Replace `<skill-root>` with the installed repository path:

```sh
python <skill-root>/scripts/jspace.py note --task csv-import --goal "Preserve quoted line breaks" --next "Inspect parser fixtures"
python <skill-root>/scripts/jspace.py note --task csv-import --check "Parser tests pass" --scope "Local parser cases" --evidence "Test command passed"
python <skill-root>/scripts/jspace.py resume --task csv-import
```

Writes require an explicit task identifier and store state under `.jspace/tasks/<task-id>/WORKSPACE.md`. `status`, `seam`, and `resume` do not modify state. Legacy no-task ledgers remain readable without automatic migration.

Store concise facts and evidence references, not credentials, unnecessary personal data, or private reasoning. Keep task state out of source control unless intentionally shared.

## Validate

```sh
python -B scripts/verify_suite.py
python -B -m unittest discover -s scripts -p test_jspace.py -v
```

The regression suite covers concurrent writers, malformed-input rejection, mixed updates, persistent question IDs, task isolation, and read-only inspection. CI runs on Windows and Linux. Package checks and controller tests do not establish model-performance improvements; see the [evaluation protocol](references/induction-playbook.md).

## Layout

- `SKILL.md`: entry point and workflow routing.
- `modules/`: optional focused guidance.
- `references/`: research qualifications, evaluation protocol, and examples.
- `scripts/`: controller, regression tests, and package validation.
