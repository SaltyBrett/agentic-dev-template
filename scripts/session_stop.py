#!/usr/bin/env python3
"""
session_stop.py — a turn does not end with sprint state uncommitted or the plan unwritten.

THE FAILURE THIS CLOSES
-----------------------
Checkpoint discipline was a sentence: update the tracker, the decision log and sprint-status after
each work unit, and commit. Nothing checked it between commits, so the interval a compaction or a
dead session could take was as long as the agent let it grow, and the plan behind uncommitted work
lived only in the conversation. Decision 2026-10-22-001.

WHAT IT CHECKS
--------------
A Claude Code Stop hook (`.claude/settings.json`), run when the agent finishes a turn.

  sprint-uncommitted  a tracked file under sprint/ is modified, staged or not
  notes-stale         work is uncommitted and the working notes are older than the newest of it
  notes-shape         the working notes no longer have exactly Plan, Open decisions, Half-done

The working notes and the journal are excluded from "uncommitted work" by path as well as by
.gitignore, so the rule does not depend on the ignore file. A new, untracked file under sprint/
(a scaffolded pair being filled) is uncommitted work but not a modified tracked file: the notes
must cover it, the commit can wait for the closeout gate.

WHAT IT DECIDES
---------------
  allow, silently   nothing holds; not a git repository; plan mode, where nothing can be written
  block             the first stop of a turn with a violation: the reasons go back to the agent
  allow, and say so a stop that is already a continuation from this hook (`stop_hook_active`):
                    the user sees what is still unbanked. The hook asks once and never wedges a
                    session; an agent with a reason it cannot commit says so, and the user hears it

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It is not enforcement: it guides the agent within a turn. The commit gates and CI enforce. It
cannot judge whether the notes are good, only that they are newer than the work.

Usage:  (hook)  python3 scripts/session_stop.py        # event JSON on stdin
        pre-commit run session-stop-selftest --all-files
        python3 scripts/session_stop.py --self-test
Exit 0 always as a hook (the decision is the JSON on stdout); the self-test exits 1 on a failure.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import session_journal as journal  # noqa: E402 — the notes path and shape

BANKING_FILES = {journal.NOTES_REL, journal.JOURNAL_REL}


def changes(root: Path) -> list[tuple[str, str]] | None:
    """(XY, path) for every uncommitted path, or None outside a git repository. Untracked files are
    listed one by one: under `normal` a wholly untracked directory is one entry whose mtime is the
    directory's, not the newest file's, and the notes file would hide inside it."""
    out = subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
                         cwd=root, capture_output=True, check=False)
    if out.returncode != 0:
        return None
    tokens = out.stdout.decode("utf-8", errors="replace").split("\0")
    entries, i = [], 0
    while i < len(tokens):
        tok = tokens[i]
        if len(tok) > 3:
            xy, path = tok[:2], tok[3:]
            entries.append((xy, path))
            if xy[0] in "RC":
                i += 1  # the rename's source path follows; the destination is the one that exists
        i += 1
    return entries


def mtime(path: Path) -> int | None:
    try:
        return path.stat().st_mtime_ns
    except OSError:
        return None  # a deletion has no time; the tracked-file rule still sees it


def violations(root: Path, entries: list[tuple[str, str]]) -> list[tuple[str, str]]:
    work = [(xy, p) for xy, p in entries if p.rstrip("/") not in BANKING_FILES]
    v = [("sprint-uncommitted", f"`{p}` is modified and uncommitted") for xy, p in work
         if xy != "??" and p.startswith("sprint/")]
    if not work:
        return v
    notes_path = root / journal.NOTES_REL
    if not notes_path.is_file():
        return v + [("notes-stale", f"there is uncommitted work and no `{journal.NOTES_REL}`")]
    shape = journal.notes_shape(notes_path.read_text(encoding="utf-8"))
    if shape:
        v.append(("notes-shape", f"`{journal.NOTES_REL}`: {shape[0]}"))
    times = [(t, p) for _, p in work if (t := mtime(root / p)) is not None]
    if times:
        newest, which = max(times)
        notes_time = mtime(notes_path) or 0
        if notes_time < newest:
            v.append(("notes-stale", f"`{journal.NOTES_REL}` is older than the newest uncommitted change, `{which}`"))
    return v


def decide(event: dict, root: Path) -> dict | None:
    """The JSON to print, or None to allow silently."""
    if event.get("permission_mode") == "plan":
        return None
    entries = changes(root)
    if entries is None:
        return None
    v = violations(root, entries)
    if not v:
        return None
    if event.get("stop_hook_active"):
        items = "; ".join(d for _, d in v)
        return {"systemMessage": f"Stop hook (scripts/session_stop.py): the turn ended with work unbanked "
                                 f"after one request to bank it: {items}."}
    lines = ["Checkpoint discipline (`AGENTS.md`, How I work), checked by the Stop hook `scripts/session_stop.py`:"]
    rules = {r for r, _ in v}
    for _, d in v:
        lines.append(f"- {d}.")
    if "sprint-uncommitted" in rules:
        lines.append("Commit the sprint files (`checkpoint: …`) before ending the turn, or say why they cannot be "
                     "committed yet.")
    if rules & {"notes-stale", "notes-shape"}:
        lines.append(f"Update `{journal.NOTES_REL}` (Plan, Open decisions, Half-done) so the uncommitted work "
                     "survives compaction.")
    return {"decision": "block", "reason": "\n".join(lines)}


# ==============================================================================
# Self-test
# ==============================================================================

def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid",
                    "-c", "commit.gpgsign=false", *args], cwd=root, check=True, capture_output=True)


def _touch(path: Path, t: int) -> None:
    os.utime(path, ns=(t, t))


def run_self_test() -> int:
    print("\nSession Stop Self-Test")
    print("=" * 60)
    failures = total = 0

    def check_(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    def rules(root: Path) -> list[str]:
        return sorted(r for r, _ in violations(root, changes(root) or []))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve() / "repo"
        (root / "sprint" / "recovery").mkdir(parents=True)
        (root / ".gitignore").write_text(f"{journal.NOTES_REL}\n{journal.JOURNAL_REL}\n", encoding="utf-8")
        status = root / "sprint" / "sprint-status.md"
        status.write_text("# Sprint Status\n", encoding="utf-8")
        (root / "README.md").write_text("readme\n", encoding="utf-8")
        _git(root, "init", "-q")
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "init")
        notes = root / journal.NOTES_REL
        notes.write_text(journal.notes_skeleton(), encoding="utf-8")
        base = 1_800_000_000_000_000_000

        check_("a clean tree passes, notes or not", rules(root) == [], str(rules(root)))
        check_("a clean tree is allowed silently", decide({}, root) is None)

        status.write_text("# Sprint Status\n\n## S9 — 2026-10-22 — x\n", encoding="utf-8")
        _touch(status, base)
        _touch(notes, base + 10)
        check_("a modified tracked sprint file fails, even with fresh notes", rules(root) == ["sprint-uncommitted"],
               str(rules(root)))
        _git(root, "add", "sprint/sprint-status.md")
        check_("staging it is not enough: it is still uncommitted", rules(root) == ["sprint-uncommitted"])
        out = decide({"stop_hook_active": False}, root) or {}
        check_("the first stop blocks, naming the file and asking for a checkpoint commit",
               out.get("decision") == "block" and "sprint/sprint-status.md" in out.get("reason", "")
               and "checkpoint" in out.get("reason", ""), str(out))
        out = decide({"stop_hook_active": True}, root) or {}
        check_("a stop that is already a continuation is allowed, and the user is told what is unbanked",
               "decision" not in out and "sprint/sprint-status.md" in out.get("systemMessage", ""), str(out))
        check_("plan mode is allowed silently: nothing can be committed there",
               decide({"permission_mode": "plan"}, root) is None)
        _git(root, "commit", "-q", "-m", "checkpoint: s")
        check_("once committed, the turn is allowed", decide({}, root) is None and rules(root) == [])

        (root / "README.md").write_text("edited\n", encoding="utf-8")
        _touch(root / "README.md", base + 100)
        _touch(notes, base + 50)
        check_("uncommitted work newer than the notes fails as stale notes", rules(root) == ["notes-stale"],
               str(violations(root, changes(root) or [])))
        _touch(notes, base + 200)
        check_("notes written after the work pass", rules(root) == [])
        notes.write_text(journal.notes_skeleton().replace("## Half-done", "## Someday"), encoding="utf-8")
        _touch(notes, base + 300)
        check_("notes that lost a section fail the shape", rules(root) == ["notes-shape"])
        notes.unlink()
        check_("uncommitted work with no notes file fails", rules(root) == ["notes-stale"])
        notes.write_text(journal.notes_skeleton(), encoding="utf-8")
        _touch(notes, base + 400)

        pair = root / "sprint" / "handoffs" / "KICKOFF_S10.md"
        pair.parent.mkdir()
        pair.write_text("# Kickoff — S10\n", encoding="utf-8")
        _touch(pair, base + 500)
        check_("a new untracked sprint file is not a modified tracked one; the notes must still cover it",
               rules(root) == ["notes-stale"], str(rules(root)))
        _touch(notes, base + 600)
        check_("…and once the notes are newer it passes", rules(root) == [])

        (root / ".gitignore").write_text("", encoding="utf-8")
        _git(root, "add", ".gitignore")
        _git(root, "commit", "-q", "-m", "drop ignores")
        _touch(pair, base + 700)
        _touch(notes, base + 650)
        check_("the notes never count as the newest change, even when nothing ignores them",
               "notes-stale" in rules(root), str(violations(root, changes(root) or [])))

        outside = Path(tmp).resolve() / "plain"
        outside.mkdir()
        check_("outside a git repository the turn is allowed silently", decide({}, outside) is None)

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        return run_self_test()
    try:
        event = json.load(sys.stdin)
        out = decide(event, journal.project_root(event))
        if out:
            print(json.dumps(out))
    except Exception as exc:  # noqa: BLE001 — a broken hook must not trap the agent in its turn
        print(f"session_stop: could not check the turn: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
