#!/usr/bin/env python3
"""
session_journal.py — the uncommitted interval is banked without the model's cooperation.

WHAT IT DOES
------------
A Claude Code PostToolUse and PostToolUseFailure hook on Edit, Write and Bash
(`.claude/settings.json`). Each event appends one line to `sprint/recovery/journal.md`: UTC time,
short session id, tool, the exit code for Bash, then the file or the command. This module also
owns the working notes, `sprint/recovery/WORKING_NOTES.md`, and their fixed shape (Plan, Open
decisions, Half-done): `session_stop.py` demands them, `session_start.py` re-injects both files
after compaction, and the session closeout gate clears both when it passes.

Both files are gitignored, for two reasons. The journal records raw commands, which can carry a
secret or a banned name into a public history. And an ignored file is outside pre-commit's stash,
so an append that lands while the suite runs cannot collide with the stash and its restore: the
writer is safe beside the suite by construction, not by timing. Concurrent writers (parallel tool
calls) are kept whole by one os.write of one line on an O_APPEND descriptor, under an exclusive
flock where the platform has one.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It records what a tool did, never why; the why is the notes' job, and only the agent can write it.
A failure to write is reported on stderr and exit 1, which Claude Code shows as a non-blocking
hook error: the tool already ran, and a journal must never be the reason its result is lost.

Usage:  (hook)  python3 scripts/session_journal.py            # event JSON on stdin
        python3 scripts/session_journal.py --clear            # reset both files
        pre-commit run session-journal-selftest --all-files
        python3 scripts/session_journal.py --self-test
Exit 0 = written (or nothing to write), 1 = could not write / self-test failed.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import fcntl  # POSIX only; on Windows the O_APPEND write alone keeps a line whole
except ImportError:  # pragma: no cover - exercised on Windows only
    fcntl = None

JOURNAL_REL = "sprint/recovery/journal.md"
NOTES_REL = "sprint/recovery/WORKING_NOTES.md"
JOURNAL_HEADER = ("# Session journal\n\n"
                  "Written by `scripts/session_journal.py`, one line per Edit, Write or Bash event. "
                  "Gitignored; cleared by the session closeout.\n\n")
NOTES_SECTIONS = ["Plan", "Open decisions", "Half-done"]
NOTES_INTRO = ("Kept by the agent while work is uncommitted; the Stop hook refuses a turn that leaves "
               "them older than the newest uncommitted change. Gitignored; cleared by the session closeout.")
MAX_COMMAND = 240     # characters of a Bash command kept in its line
MAX_LINE = 1000       # bytes; far under PIPE_BUF, so one write is one record on every POSIX system
TOOLS = ("Edit", "Write", "Bash")
EXIT_LINE = re.compile(r"^Exit code (\d+)")
LINE = re.compile(r"^- \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z [0-9a-z-]{1,8} \S.*$")


def project_root(event: dict | None = None) -> Path:
    """The project Claude Code started in: CLAUDE_PROJECT_DIR when the hook runs, else the git top
    level of the event's cwd or the working directory, else that directory itself."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    start = Path((event or {}).get("cwd") or os.getcwd())
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=start, capture_output=True,
                         text=True, check=False)
    top = out.stdout.strip()
    return Path(top) if out.returncode == 0 and top else start


def notes_skeleton() -> str:
    body = "".join(f"## {s}\n\n-\n\n" for s in NOTES_SECTIONS)
    return f"# Working notes\n\n{NOTES_INTRO}\n\n{body}".rstrip("\n") + "\n"


def notes_sections(text: str) -> list[tuple[str, str]]:
    """The H2 sections of the notes, in order, with their bodies stripped."""
    out: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        if line.startswith("## "):
            out.append((line[3:].strip(), []))
        elif out:
            out[-1][1].append(line)
    return [(h, "\n".join(b).strip()) for h, b in out]


def notes_shape(text: str) -> list[str]:
    """Problems with the notes' shape: exactly the three sections, in order. Empty means it holds."""
    heads = [h for h, _ in notes_sections(text)]
    if heads == NOTES_SECTIONS:
        return []
    return [f"sections are {heads or 'none'}; the shape is {NOTES_SECTIONS}"]


def notes_blank(text: str) -> bool:
    """True when every section is empty or a lone `-`: nothing an unfinished session left."""
    return all(body in ("", "-") for _, body in notes_sections(text))


def short_session(event: dict) -> str:
    sid = str(event.get("session_id") or "")
    return (re.sub(r"[^0-9a-z-]", "", sid.lower())[:8]) or "-"


def rel_path(path: str, root: Path) -> str:
    try:
        return Path(path).resolve().relative_to(root.resolve()).as_posix()
    except (ValueError, OSError):
        return path


def one_line(text: str, limit: int) -> str:
    flat = " ".join(str(text).split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"


def journal_line(event: dict, root: Path, now: datetime.datetime) -> str | None:
    """The line for one hook event, or None for an event this journal does not record."""
    tool = event.get("tool_name")
    if tool not in TOOLS:
        return None
    stamp = now.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    who = short_session(event)
    agent = f" [{one_line(event['agent_type'], 40)}]" if event.get("agent_type") else ""
    tin = event.get("tool_input") or {}
    if tool == "Bash":
        if event.get("hook_event_name") == "PostToolUseFailure":
            if event.get("is_interrupt"):
                status = "interrupted"
            else:
                m = EXIT_LINE.match(str(event.get("error") or ""))
                status = f"exit={m.group(1)}" if m else "failed"
        else:
            status = "exit=0"
        what = f"{status} {one_line(tin.get('command', ''), MAX_COMMAND)}"
    else:
        failed = " failed" if event.get("hook_event_name") == "PostToolUseFailure" else ""
        what = f"{rel_path(str(tin.get('file_path', '?')), root)}{failed}"
    line = f"- {stamp} {who}{agent} {tool} {what}"
    return line.encode("utf-8")[:MAX_LINE].decode("utf-8", errors="ignore")


def note_line(event: dict, text: str, now: datetime.datetime) -> str:
    """A line the session hooks write themselves (`start S3 (startup)`, `compact S3`)."""
    stamp = now.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"- {stamp} {short_session(event)} {one_line(text, 200)}"


def append(path: Path, line: str) -> None:
    """Append one record. The header goes in under the same lock when the file is empty, so two
    first writers cannot both write it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        if fcntl is not None:
            fcntl.flock(fd, fcntl.LOCK_EX)
        data = (line.rstrip("\n") + "\n").encode("utf-8")
        if os.fstat(fd).st_size == 0:
            data = JOURNAL_HEADER.encode("utf-8") + data
        os.write(fd, data)
    finally:
        os.close(fd)  # closing releases the flock


def clear(root: Path) -> list[str]:
    """Reset the journal to its header and the notes to the empty shape. Returns what it reset."""
    done = []
    for rel, text in ((JOURNAL_REL, JOURNAL_HEADER), (NOTES_REL, notes_skeleton())):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        done.append(rel)
    return done


def journal_records(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if ln.startswith("- ")]


# ==============================================================================
# Self-test
# ==============================================================================

def _stress_worker(args: tuple[str, int, int]) -> None:
    path, worker, count = args
    for i in range(count):
        append(Path(path), f"- 2026-10-22T00:00:00Z w{worker:02d} Bash exit=0 record {worker}-{i} " + "x" * 300)


def run_self_test() -> int:
    # A commit hook in a linked worktree exports GIT_DIR, and git run in a scratch directory with it
    # set acts on the real repository: `git init` made it bare. The
    # self-test's git sees none of the hook's.
    for name in [k for k in os.environ if k.startswith("GIT_")]:
        os.environ.pop(name)
    print("\nSession Journal Self-Test")
    print("=" * 60)
    failures = total = 0

    def check_(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    root = Path("/repo")
    now = datetime.datetime(2026, 10, 22, 20, 31, 5, tzinfo=datetime.timezone.utc)
    ev = {"session_id": "1A2B3C4D-ffff", "hook_event_name": "PostToolUse"}
    line = journal_line({**ev, "tool_name": "Edit", "tool_input": {"file_path": "/repo/sprint/sprint-status.md"}}, root, now)
    check_("an Edit records the time, the short session id, the tool and the path relative to the project",
           line == "- 2026-10-22T20:31:05Z 1a2b3c4d Edit sprint/sprint-status.md", str(line))
    line = journal_line({**ev, "tool_name": "Bash", "tool_input": {"command": "pre-commit run\n  --all-files"}}, root, now)
    check_("a Bash success records exit=0 and the command on one line",
           line == "- 2026-10-22T20:31:05Z 1a2b3c4d Bash exit=0 pre-commit run --all-files", str(line))
    fail = {**ev, "hook_event_name": "PostToolUseFailure", "tool_name": "Bash", "tool_input": {"command": "false"},
            "error": "Exit code 1\nboom"}
    check_("a Bash failure records the exit code from the error's first line",
           (journal_line(fail, root, now) or "").endswith(" Bash exit=1 false"), str(journal_line(fail, root, now)))
    check_("an interrupted Bash call is recorded as interrupted, not as an exit code",
           " Bash interrupted " in (journal_line({**fail, "is_interrupt": True}, root, now) or ""))
    check_("a failure with no exit-code line is recorded as failed",
           " Bash failed " in (journal_line({**fail, "error": "could not start shell"}, root, now) or ""))
    check_("a subagent's event names the agent",
           " 1a2b3c4d [Explore] Edit " in (journal_line({**ev, "agent_type": "Explore", "tool_name": "Edit",
                                                          "tool_input": {"file_path": "/repo/x"}}, root, now) or ""))
    check_("a path outside the project stays absolute",
           (journal_line({**ev, "tool_name": "Write", "tool_input": {"file_path": "/tmp/x.md"}}, root, now) or "").endswith(" Write /tmp/x.md"))
    check_("a tool this journal does not record writes nothing",
           journal_line({**ev, "tool_name": "Read", "tool_input": {"file_path": "/repo/x"}}, root, now) is None)
    long_cmd = journal_line({**ev, "tool_name": "Bash", "tool_input": {"command": "echo " + "y" * 5000}}, root, now) or ""
    check_("a long command is cut, so a line stays one bounded record",
           len(long_cmd.encode()) <= MAX_LINE and long_cmd.endswith("…") and LINE.match(long_cmd), str(len(long_cmd)))

    sk = notes_skeleton()
    check_("the notes skeleton has exactly the three sections, in order, and reads as blank",
           notes_shape(sk) == [] and notes_blank(sk), str(notes_sections(sk)))
    filled = sk.replace("## Plan\n\n-", "## Plan\n\n- finish ACME-1.2")
    check_("notes with content are not blank and keep their shape", not notes_blank(filled) and notes_shape(filled) == [])
    check_("notes missing a section fail the shape", notes_shape(sk.replace("## Half-done", "## Later")) != [])
    swapped = sk.replace("## Plan", "## TMP").replace("## Open decisions", "## Plan").replace("## TMP", "## Open decisions")
    check_("notes with sections out of order fail the shape", notes_shape(swapped) != [])
    check_("notes with an extra section fail the shape", notes_shape(sk + "\n## Ideas\n\n- x\n") != [])

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "sprint" / "recovery" / "journal.md"
        append(path, "- 2026-10-22T00:00:00Z a Edit x")
        append(path, "- 2026-10-22T00:00:01Z a Edit y")
        text = path.read_text(encoding="utf-8")
        check_("the first append writes the header once, then one record per call",
               text.count("# Session journal") == 1 and journal_records(text) == ["- 2026-10-22T00:00:00Z a Edit x",
                                                                                 "- 2026-10-22T00:00:01Z a Edit y"], text)
        done = clear(Path(tmp))
        check_("clear resets the journal to its header and the notes to the blank shape",
               done == [JOURNAL_REL, NOTES_REL] and journal_records(path.read_text(encoding="utf-8")) == []
               and notes_blank((Path(tmp) / NOTES_REL).read_text(encoding="utf-8")))

        stress = Path(tmp) / "stress.md"
        import multiprocessing
        workers, count = 8, 60
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            pool.map(_stress_worker, [(str(stress), w, count) for w in range(workers)])
        text = stress.read_text(encoding="utf-8")
        records = journal_records(text)
        whole = [r for r in records if re.fullmatch(r"- \S+ w\d\d Bash exit=0 record \d+-\d+ x{300}", r)]
        seen = {r.split(" record ")[1].split(" ")[0] for r in whole}
        check_(f"{workers} processes appending {count} lines each leave every line whole, none lost, one header",
               len(records) == workers * count and len(whole) == len(records) and len(seen) == workers * count
               and text.count("# Session journal") == 1 and text.count("\n") == text.count("\n- ") + JOURNAL_HEADER.count("\n"),
               f"records={len(records)} whole={len(whole)} distinct={len(seen)} headers={text.count('# Session journal')}")

    ignored = subprocess.run(["git", "check-ignore", "-q", "--no-index", JOURNAL_REL],
                             cwd=project_root(), capture_output=True, check=False).returncode == 0 and \
        subprocess.run(["git", "check-ignore", "-q", "--no-index", NOTES_REL],
                       cwd=project_root(), capture_output=True, check=False).returncode == 0
    check_("the repository's .gitignore covers both files (the stash and the scanners never see them)", ignored)

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        return run_self_test()
    if "--clear" in sys.argv[1:]:
        for rel in clear(project_root()):
            print(f"cleared   {rel}")
        return 0
    try:
        event = json.load(sys.stdin)
        root = project_root(event)
        line = journal_line(event, root, datetime.datetime.now(datetime.timezone.utc))
        if line:
            append(root / JOURNAL_REL, line)
        return 0
    except Exception as exc:  # noqa: BLE001 — any failure is reported, never raised into the hook runner
        print(f"session_journal: could not write the journal: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
