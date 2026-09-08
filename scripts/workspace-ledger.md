# Task workspace ledger

The controller stores concise task state: Goal, Core, Verified, Open, Next. The conceptual ledger's Constraints and Decisions map to labelled Core entries, for example `--core "Constraint - use standard library only"` and `--core "Decision - keep each task in its own directory"`. There is no two-entry storage cap: all Core entries are retained and shown by `status` and `resume`; the first two are marked live and the rest parked. Keep evidence as a short observation or artifact reference. Do not store private reasoning, drafts, transcripts, or execution logs.

Run the controller from the task workspace. Every write requires an explicit `--task` ID. IDs contain 1–64 ASCII letters, digits, underscores or hyphens, starting with a letter or digit, and are normalized to lowercase. Windows device names such as `CON` and `NUL` are rejected on every platform. State lives at `.jspace/tasks/<task>/WORKSPACE.md`. Use a distinct ID for each independent task.

```powershell
python <skill-root>\scripts\jspace.py note --task controller-fixes --goal "Controller updates preserve task state" --next "Run regression tests"
python <skill-root>\scripts\jspace.py note --task controller-fixes --core "Ledger - one atomic task snapshot"
python <skill-root>\scripts\jspace.py note --task controller-fixes --open "Are concurrent updates retained?" --settled-by "Run concurrent subprocess writers"
python <skill-root>\scripts\jspace.py note --task controller-fixes --close 1 --check "Concurrent updates retained" --scope "16 local subprocess writers" --evidence "test_concurrent_process_writes passed" --next "Run integration checks"
python <skill-root>\scripts\jspace.py status --task controller-fixes
python <skill-root>\scripts\jspace.py seam --task controller-fixes
python <skill-root>\scripts\jspace.py resume --task controller-fixes
python <skill-root>\scripts\jspace.py ship draft.md
```

`--task` also works before the command. `status` and `resume` print the full task ledger; `seam` prints compact state. All three are read-only: they create no directories or locks and never write ledger/history files. Legacy history is ignored. The controller does not infer stalls or print premise, confidence, or sweep instructions.

A note is one transaction. Every requested edit must be valid or none of the ledger changes are written (exit 2). A failed write may leave the directory and stable lock sidecar, but never a partial ledger. Concurrent controller writers serialize the complete read/validate/replace operation with OS locks (`msvcrt` on Windows, `fcntl` on POSIX). Lock ownership is released on process exit; the sidecar must not be deleted while writers run. Manual editors must not race controller writes. Atomic replacement protects readers from partial content. These guarantees target local filesystems with normal OS locking semantics.

The Markdown file carries a versioned `next-question` counter in a comment. Keep that metadata: closed question IDs are never reused. Goal and Next each occupy one line; all five sections must be present exactly once. Unknown sections, extra Goal/Next lines, malformed IDs and unsupported Unicode line separators are rejected instead of being silently dropped. Core has two live entries; additional entries stay parked. Verified entries are numbered and append-only through the CLI. Closing a question requires a checkpoint in the same note.

## Compatibility

Without `--task`, `status`, `seam`, and `resume` inspect the old `.jspace/WORKSPACE.md`. Writes without a task are refused. An explicit task never falls back to or migrates that legacy file. For a new task, open a fresh ledger with explicit Goal and Next. Standard five-section legacy Markdown remains readable; malformed or ambiguous files require deliberate manual repair. Legacy files cannot recover IDs of questions already deleted before a counter existed. No inferred migration promises otherwise.

`--check "conclusion" --scope "coverage" --evidence "support"` is preferred. Scope and evidence must be supplied together. They record an explicit attestation, not a proof checked by the controller. The old `--check "conclusion" --by "verifier and coverage"` form remains accepted, and `--verified` is an alias for `--check`. Legacy `--by` is no longer gated by a vocabulary heuristic. If supplied together, structured scope/evidence take precedence over `--by`.

`ship` only offers conservative audience warnings for standalone state markers outside fenced or indented code. Ordinary math symbols, code operators, punctuation and claims are not classified as leaks. It returns 0 even when warning, and absence of warnings does not certify content. File/encoding errors return 2.

## Verification

```powershell
python -X utf8 -B -m unittest discover -s <skill-root>\scripts -p test_jspace.py -v
```

The tests use temporary workspaces, including subprocess concurrency, transactional rejection, mixed updates, ID persistence, schema preservation, task isolation, legacy reads, and filesystem snapshots around read-only commands.

Keep `.jspace/` out of version control unless explicitly requested. The ledger can also be maintained as five concise labelled lines in the conversation when no filesystem is available.

