#!/usr/bin/env python3
"""jspace: concise, task-scoped state stored in a Markdown ledger.

note requires --task ID and applies all edits in one locked atomic transaction.
Open a task with --goal and --next. Record checkpoints with --check, --scope
and --evidence (legacy --verified and --by remain accepted). Question IDs are
monotonic. Invalid requests return 2 without committing ledger changes.

seam prints compact state; status and resume print the full ledger. These
commands are read-only and never inspect or update history. Without --task,
they read the legacy .jspace/WORKSPACE.md; explicit tasks never migrate it.
Task ledgers live in .jspace/tasks/<task>/WORKSPACE.md beneath the current directory.

ship FILE (or - for stdin) emits conservative advisory audience warnings.
Warnings return 0; input and filesystem failures return 2. No content is certified.
Standard library only; stores task state, not reasoning, drafts or execution logs.
"""

import argparse
from contextlib import contextmanager
import copy
import codecs
import os
import re
import sys
import tempfile
import time

LEDGER_DIR = ".jspace"
LEDGER = os.path.join(LEDGER_DIR, "WORKSPACE.md")
SECTIONS = ("Goal", "Core", "Verified", "Open", "Next")

class LedgerReadError(Exception):
    """The persisted ledger cannot be read without risking state loss."""

MARKERS = ["GRRR", "GAAAH", "PHEW", "I see meltdown", "DATA DATA", "I'M DROWNING"]


# ------------------------------------------------------------------------- ledger


def read_ledger():
    """Read canonical or legacy Markdown; reject shapes a rewrite would lose."""
    book = {k: [] for k in SECTIONS}
    if not os.path.exists(LEDGER):
        return book
    try:
        with open(LEDGER, encoding="utf-8-sig") as fh:
            text = fh.read()
    except (OSError, UnicodeError) as exc:
        raise LedgerReadError("%s (%s)" % (LEDGER, exc)) from exc
    current = None
    seen = set()
    metadata = False
    for line in text.split("\n"):
        if any(c in line for c in "\v\f\x1c\x1d\x1e\x85\u2028\u2029\x00"):
            raise LedgerReadError("unsupported line separator or NUL in ledger")
        head = line.strip()
        if not head:
            continue
        if head == "# J-Space Workspace Ledger" and not seen and not current:
            continue
        match = re.fullmatch(r"<!-- jspace:v1 next-question=(\d+) -->", head)
        if match and not seen and not metadata:
            book["_next_question"] = int(match.group(1))
            metadata = True
            continue
        if head.startswith("## "):
            current = head[3:]
            if current not in SECTIONS or current in seen:
                raise LedgerReadError("unknown or duplicate section: " + current)
            seen.add(current)
            continue
        if current is None:
            raise LedgerReadError("unexpected content outside sections")
        value = head[2:] if current not in ("Goal", "Next") and head.startswith("- ") else head
        value, problem = clean_scalar(value)
        if problem:
            raise LedgerReadError("invalid %s: %s" % (current, problem))
        book[current].append(value)
    if seen != set(SECTIONS) or any(len(book[k]) != 1 for k in ("Goal", "Next")):
        raise LedgerReadError("expected all five sections and one Goal/Next line")
    for key, prefix in (("Open", "?"), ("Verified", "\u2713")):
        ids = []
        for row in book[key]:
            match = re.match(r"^%s([0-9]+) " % re.escape(prefix), row)
            if not match or int(match.group(1)) < 1:
                raise LedgerReadError("invalid numbered entry in " + key)
            ids.append(int(match.group(1)))
        if len(ids) != len(set(ids)):
            raise LedgerReadError("duplicate IDs in " + key)
    minimum = next_number(book["Open"], "?")
    if metadata and book["_next_question"] < minimum:
        raise LedgerReadError("question counter precedes existing IDs")
    book.setdefault("_next_question", minimum)
    return book


def select_task(task):
    """No implicit import: an explicit task always selects its own directory."""
    global LEDGER_DIR, LEDGER
    if task is not None and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", task):
        raise ValueError("--task must be 1-64 ASCII letters, digits, underscores or hyphens; start with a letter or digit")
    if task and re.fullmatch(r"(?:con|prn|aux|nul|com[1-9]|lpt[1-9])", task, re.I):
        raise ValueError("--task must not be a reserved Windows device name")
    # Lowercase avoids task aliasing on case-insensitive filesystems.
    LEDGER_DIR = os.path.join(".jspace", "tasks", task.lower()) if task else ".jspace"
    LEDGER = os.path.join(LEDGER_DIR, "WORKSPACE.md")


@contextmanager
def ledger_lock():
    """OS advisory lock on a stable sidecar; released even after process death."""
    problem = ensure_dir()
    if problem:
        raise OSError(problem)
    with open(os.path.join(LEDGER_DIR, ".write.lock"), "a+b") as lock:
        if os.name == "nt":
            import msvcrt
            lock.seek(0, os.SEEK_END)
            if lock.tell() == 0:
                lock.write(b"\0")
                lock.flush()
            deadline = time.monotonic() + 30
            while True:
                try:
                    lock.seek(0)
                    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise OSError("timed out waiting for ledger lock")
                    time.sleep(0.05)
            try:
                yield
            finally:
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def ensure_dir():
    """Make the ledger directory. Returns an error string, or None on success."""
    try:
        os.makedirs(LEDGER_DIR, exist_ok=True)
    except OSError as exc:
        return "%s (%s)" % (LEDGER_DIR, exc.strerror or "cannot create")
    if not os.path.isdir(LEDGER_DIR):
        return "%s exists but is not a directory" % LEDGER_DIR
    return None


def atomic_write_text(path, text):
    """Replace a UTF-8 text file atomically. Returns an error string or None."""
    problem = ensure_dir()
    if problem:
        return problem
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=LEDGER_DIR, prefix=".jspace-", delete=False
        ) as fh:
            temp_path = fh.name
            fh.write(text)
        os.replace(temp_path, path)
    except OSError as exc:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        return "%s (%s)" % (path, exc.strerror or "cannot write")
    return None


def write_ledger(book):
    out = ["# J-Space Workspace Ledger",
           "<!-- jspace:v1 next-question=%d -->" % book.get("_next_question", next_number(book["Open"], "?")), ""]
    for name in SECTIONS:
        out.append("## " + name)
        rows = book[name]
        if name in ("Goal", "Next"):
            out.append(rows[0] if rows else "")
        else:
            out.extend("- " + r for r in rows)
        out.append("")
    return atomic_write_text(LEDGER, "\n".join(out).rstrip() + "\n")


def one(book, key):
    return book[key][0] if book[key] else ""


def declined(message, fix):
    print("NOT RECORDED: " + message)
    print("  " + fix)
    return 2


def clean_scalar(value):
    """Return a safe one-line scalar and an error, if any."""
    if value is None:
        return None, None
    if any(c in value for c in "\r\n\v\f\x1c\x1d\x1e\x85\u2028\u2029\x00"):
        return None, "must be one line"
    value = value.strip()
    if not value:
        return None, "must not be empty"
    return value, None


def next_number(rows, prefix):
    numbers = []
    pattern = re.compile(r"^%s(\d+)\b" % re.escape(prefix))
    for row in rows:
        match = pattern.match(row)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


# -------------------------------------------------------------------------- modes


def print_ledger(book):
    print("Goal:     " + (one(book, "Goal") or "(not set)"))
    core = book["Core"] or ["(empty)"]
    print("Core:     " + core[0])
    for extra in core[1:2]:
        print("          " + extra)
    if len(core) > 2:
        print("          (+%d more in the ledger — two live at a time)" % (len(core) - 2))
    verified = book["Verified"]
    print("Verified: " + (verified[-1] if verified else "(none yet)"))
    if len(verified) > 1:
        print("          (%d earlier, in the ledger)" % (len(verified) - 1))
    for row in book["Open"][:2]:
        print("Open:     " + row)
    print("Next:     " + (one(book, "Next") or "(not set)"))


def print_full_ledger(book):
    print("Goal: " + (one(book, "Goal") or "(not set)"))
    print("Core:")
    if book["Core"]:
        for index, row in enumerate(book["Core"]):
            state = "live" if index < 2 else "parked"
            print("  [%s] %s" % (state, row))
    else:
        print("  (empty)")
    print("Verified:")
    if book["Verified"]:
        for row in book["Verified"]:
            print("  " + row)
    else:
        print("  (none yet)")
    print("Open:")
    if book["Open"]:
        for row in book["Open"]:
            print("  " + row)
    else:
        print("  (none)")
    print("Next: " + (one(book, "Next") or "(not set)"))


def mode_note(book, args):
    """Validate the entire note, then commit it as one transaction."""
    book = copy.deepcopy(book)
    changed = False
    refused = []
    invalid = set()

    for name, flag in (
        ("goal", "--goal"),
        ("core", "--core"),
        ("next", "--next"),
        ("check", "--check"),
        ("by", "--by"),
        ("scope", "--scope"),
        ("evidence", "--evidence"),
        ("open", "--open"),
        ("settled_by", "--settled-by"),
    ):
        value, problem = clean_scalar(getattr(args, name))
        if value is not None and not problem and name in ("goal", "next") and value.startswith("## "):
            problem = "must not begin with a ledger section heading ('## ')"
            value = None
        setattr(args, name, value)
        if problem:
            invalid.add(name)
            refused.append(("%s %s." % (flag, problem), "%s \"one-line value\"" % flag))

    if not (one(book, "Goal") or args.goal) or not (one(book, "Next") or args.next):
        refused.append(
            (
                "opening the ledger requires both Goal and Next.",
                'note --goal "what done means" --next "the first action"',
            )
        )
        for message, fix in refused:
            declined(message, fix)
        return 2

    if args.goal:
        book["Goal"] = [args.goal]
        changed = True

    if args.core:
        if "—" not in args.core and " - " not in args.core:
            refused.append(
                (
                    "a core entry without its defining fact is a mention, not a load.",
                    '--core "name — the one fact that makes it matter"',
                )
            )
        elif args.core_slot is None:
            if args.core not in book["Core"]:
                book["Core"].append(args.core)
                changed = True
        else:
            live = book["Core"][:2]
            parked = book["Core"][2:]
            idx = args.core_slot - 1
            if idx > len(live):
                refused.append(
                    (
                        "live core slot %d does not exist." % args.core_slot,
                        "use the next available slot or add the entry without --core-slot",
                    )
                )
            elif args.core in live and (idx >= len(live) or live[idx] != args.core):
                refused.append(
                    ("that core entry is already live.", "choose the slot that should actually change")
                )
            elif idx == len(live):
                live.append(args.core)
                book["Core"] = live + parked
                changed = True
            else:
                displaced = live[idx]
                live[idx] = args.core
                parked = [row for row in parked if row != args.core]
                if displaced != args.core:
                    parked.insert(0, displaced)
                book["Core"] = live + parked
                changed = changed or displaced != args.core
    elif args.core_slot is not None:
        refused.append(("--core-slot requires --core.", '--core "name — defining fact" --core-slot 1'))

    check_recorded = False
    if args.check:
        if args.scope and args.evidence:
            args.by = "scope: %s; evidence: %s" % (args.scope, args.evidence)
        if not args.by:
            refused.append(
                (
                    "a checkpoint with no record is not a checkpoint.",
                    '--check "what now holds" --by "what verified it"',
                )
            )
        else:
            num = next_number(book["Verified"], "✓")
            book["Verified"].append(
                "✓%02d %s — verified by: %s" % (num, args.check, args.by)
            )
            changed = True
            check_recorded = True
    else:
        if args.by and "check" not in invalid:
            refused.append(("--by requires --check.", '--check "what now holds" --by "verifier and coverage"'))

    if args.open:
        settle = args.settled_by or ""
        if not settle:
            refused.append(
                (
                    "an open question with nothing that would settle it cannot be closed.",
                    '--open "the question" --settled-by "the cheapest test that could refute it"',
                )
            )
        else:
            num = book.get("_next_question", next_number(book["Open"], "?"))
            book["_next_question"] = num + 1
            book["Open"].append("?%02d %s — settled by: %s" % (num, args.open, settle))
            changed = True
    elif args.settled_by and "open" not in invalid:
        refused.append(("--settled-by requires --open.", '--open "question" --settled-by "test"'))

    if args.close is not None:
        rows = book["Open"]
        idx = next((i for i, row in enumerate(rows)
                    if re.match(r"^\?0*%d " % args.close, row)), None)
        if idx is None:
            refused.append(
                ("no open question numbered %d." % args.close, "run `seam` to see the list")
            )
        elif not check_recorded:
            refused.append(
                (
                    "closing an open question requires a checkpoint in the same call.",
                    '--close %d --check "what now holds" --by "verifier and coverage"' % args.close,
                )
            )
        else:
            rows.pop(idx)
            changed = True

    if args.next:
        book["Next"] = [args.next]
        changed = True

    if bool(args.scope) != bool(args.evidence) or ((args.scope or args.evidence) and not args.check):
        refused.append(("--scope and --evidence require each other and --check.", "provide a checkpoint, scope and evidence"))
    if refused:
        for message, fix in refused:
            declined(message, fix)
        return 2
    if changed:
        problem = write_ledger(book)
        if problem:
            print("CANNOT: cannot write the ledger — " + problem)
            print("  free the path, or work without the file: keep the five lines in the")
            print("  conversation and restate them at each seam.")
            return 2
    print_ledger(book)
    return 0


def mode_ship(text):
    """Conservative advisory hints; never certify or block delivery."""
    findings = []
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or line.startswith(("    ", "	")):
            continue
        if stripped.upper() in {m.upper() for m in MARKERS}:
            findings.append("line %d: possible state marker; review its audience" % number)
    if findings:
        print("WARNING: heuristic suggestions only; these may be intentional.")
        for finding in findings[:7]:
            print("- " + finding)
    else:
        print("No heuristic warnings. This is not verification of the content.")
    return 0


def read_outgoing(path):
    """Read outgoing text without silently accepting an unknown or binary encoding."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return None, "%s (%s)" % (path, exc.strerror or "unreadable")
    try:
        if data.startswith(codecs.BOM_UTF8):
            text = data.decode("utf-8-sig")
        elif data.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
            text = data.decode("utf-32")
        elif data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
            text = data.decode("utf-16")
        else:
            text = data.decode("utf-8")
            if "\x00" in text:
                raise UnicodeError("NUL bytes suggest an unsupported encoding")
    except UnicodeError as exc:
        return None, "%s (cannot decode safely: %s)" % (path, exc)
    return text, None


def configure_streams():
    """Keep controller output deterministic on Windows consoles and redirected streams."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


# --------------------------------------------------------------------------- main


def main(argv=None):
    """Parse the subcommand and run it. Returns the process exit code."""
    configure_streams()
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("seam", help="read-only ledger observation")
    sub.add_parser("status", help="read-only full task state")
    sub.add_parser("resume", help="read-only full task state after a gap")

    n = sub.add_parser("note", help="record something in the ledger")
    n.add_argument("--goal")
    n.add_argument("--core")
    n.add_argument("--core-slot", dest="core_slot", type=int, choices=(1, 2))
    n.add_argument("--next")
    n.add_argument("--check", "--verified", dest="check", help="checkpoint conclusion (legacy --verified alias)")
    n.add_argument("--scope", help="what the verification covers")
    n.add_argument("--evidence", help="test, observation or artifact supporting the conclusion")
    n.add_argument("--by")
    n.add_argument("--open")
    n.add_argument("--settled-by", dest="settled_by")
    n.add_argument("--close", type=int)

    s = sub.add_parser("ship", help="register check on anything about to leave")
    s.add_argument("file", help="path, or - for stdin")

    p.add_argument("--task", help="explicit task ID; required for note")
    for command_parser in sub.choices.values():
        command_parser.add_argument("--task", default=argparse.SUPPRESS)
    args = p.parse_args(argv)
    try:
        select_task(args.task)
    except ValueError as exc:
        p.error(str(exc))
    if args.cmd == "note" and not args.task:
        p.error("note requires --task; the legacy ledger is read-only")

    if args.cmd == "ship":
        if args.file == "-":
            return mode_ship(sys.stdin.read())
        text, problem = read_outgoing(args.file)
        if problem:
            print("CANNOT: " + problem + ".")
            print("  pass a readable file, or - to read stdin")
            return 2
        return mode_ship(text)

    try:
        if args.cmd == "note":
            with ledger_lock():
                return mode_note(read_ledger(), args)
        book = read_ledger()
    except (LedgerReadError, OSError) as exc:
        print("CANNOT: ledger was unreadable — %s." % exc)
        print("  inspect and repair the selected ledger before recording more state")
        return 2
    if args.cmd == "seam":
        print_ledger(book)
    else:
        print_full_ledger(book)
    return 0


if __name__ == "__main__":
    sys.exit(main())
