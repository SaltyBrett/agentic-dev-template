#!/usr/bin/env python3
"""
sanitize_template.py — return the template to its pristine state.

WHAT THIS IS
------------
The initializer's machinery without the fill (decision 2026-09-23-003). `new_project.py`
regenerates the sprint documents, clears the handoff folder and fills the project tokens; this
script does the first two to the template itself and leaves every token, both profile blocks
and every framework file exactly as they are. The template carries its own build state — sprint
entries above S1, the `TMPL` epics, handoff pairs and their archive, the sprint-status archive,
and the name of the derived probe repository — and a project created from it inherits none of
that, but the template itself is not the pristine artifact the operator clones from until it is
gone. The build history is kept in the archive repository the decision names, not here.

WHAT --check JUDGES
-------------------
Exit 1 while any build state remains, each item named:
  * a sprint-status entry numbered above S1
  * a `TMPL-` story row in the tracker
  * a file in sprint/archive/ or sprint/handoffs/archive/
  * a handoff or kickoff in sprint/handoffs/
  * the probe repository's name in any text file git would commit, this script excepted,
    because the name has to be written somewhere for the check to exist

WHAT --apply DOES
-----------------
Regenerates sprint/sprint-status.md with the template's own S1 entry and sprint/story-tracker.md
with the initializer's skeleton (the `[EXAMPLE]` epic, statistics at zero, `{{DATE}}` kept),
removes every file under sprint/handoffs/, sprint/handoffs/archive/ and sprint/archive/, then
runs the suite. It writes no `.project-profile`, strips no profile block and fills no token.
`.resources-version` stays: it is the template's own sync state, not session state, and the
closeout's persona rule reads it. NEVER_RESET of the initializer holds here too, pinned by a
fixture: the framework decisions, the project's decision log, the knowledge base and the
personas are in no mutating list.

The sweep of session numbers, probe references and commit hashes out of the knowledge entries
and decision bodies is by hand; the decision says so, and --check proves only the probe name.

WHERE IT RUNS
-------------
Only in the template: the inverse of the initializer's refusal. `origin` must be the template's
own repository, or the run is refused. `--force` overrides, for a deliberate re-scaffold; the
self-test has no such condition, so the suite stays green in every derived project.

Usage:
    python3 scripts/sanitize_template.py --check
    python3 scripts/sanitize_template.py --apply
    python3 scripts/sanitize_template.py --self-test
    pre-commit run sanitize-template-check --hook-stage manual --all-files
Exit 0 = clean, 1 = refused, build state remains, or the suite failed, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import datetime
import fnmatch
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import new_project  # noqa: E402 — the skeleton, the token rules and the origin test
import session_closeout  # noqa: E402 — the state gate's own parsers

ROOT = Path(__file__).resolve().parents[1]
SELF = "scripts/sanitize_template.py"

# The derived probe repository of the archived lineage (decision 2026-09-22-002). Its name is
# build state everywhere but here.
PROBE_NAME = "template-probe"

STATUS = "sprint/sprint-status.md"
TRACKER = "sprint/story-tracker.md"
HANDOFFS = "sprint/handoffs"
HANDOFF_ARCHIVE = "sprint/handoffs/archive"
SPRINT_ARCHIVE = "sprint/archive"

# Regenerated from a skeleton, as the initializer does; the skeletons differ only in that the
# template's sprint-status entry is its own and the tracker keeps its `{{DATE}}` token.
REGENERATE_FILES = list(new_project.REGENERATE_FILES)

# Removed. The initializer's globs plus the sprint-status archive, which the initializer never
# sees because a project's cap has not fired at birth.
CLEAR_GLOBS = ["sprint/handoffs/*.md", "sprint/handoffs/archive/*.md", "sprint/archive/*.md"]

# Never written, never removed. The initializer's list, and the sync stamp on top of it.
NEVER_RESET = list(new_project.NEVER_RESET) + [".resources-version"]

TMPL_STORY = re.compile(r"^TMPL-\d+\.\d+$")


class Tree(NamedTuple):
    """A snapshot of what --check reads, so the rules are pure over text and names."""
    status: str | None
    tracker: str | None
    handoffs: list[str]          # file names directly in sprint/handoffs/
    handoff_archive: list[str]   # file names in sprint/handoffs/archive/
    sprint_archive: list[str]    # file names in sprint/archive/
    texts: dict[str, str]        # every text file git would commit, by path


# ==============================================================================
# Rules — pure functions
# ==============================================================================

def sessions_above_one(status_text: str) -> list[int]:
    """Every `## S<N> — date — title` heading with N above 1, in file order."""
    found: list[int] = []
    for head in session_closeout.status_headings(status_text):
        m = session_closeout.STATUS_ENTRY.match(f"## {head}")
        if m and int(m.group(1)) > 1:
            found.append(int(m.group(1)))
    return found


def tmpl_stories(tracker_text: str) -> list[str]:
    """Every table row whose Story ID cell is a `TMPL-` story, under any epic. A mention in
    prose is not a story."""
    found: list[str] = []
    for line in tracker_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and TMPL_STORY.fullmatch(cells[0]):
            found.append(cells[0])
    return found


def probe_mentions(rel: str, text: str, name: str = PROBE_NAME) -> list[int]:
    """Line numbers naming the probe repository. This script is the one file allowed to."""
    if rel == SELF:
        return []
    return [no for no, line in enumerate(text.splitlines(), 1) if name in line]


def violations(tree: Tree) -> list[tuple[str, str, str]]:
    """Every --check rule over a snapshot. Returns (rule, where, detail)."""
    v: list[tuple[str, str, str]] = []
    if tree.status is not None:
        for n in sessions_above_one(tree.status):
            v.append(("session", STATUS, f"entry S{n} is build history; the pristine template holds S1 alone"))
    if tree.tracker is not None:
        for sid in tmpl_stories(tree.tracker):
            v.append(("tmpl-story", TRACKER, f"{sid} is a story of the template's own build; the pristine tracker "
                                              "holds the [EXAMPLE] epic alone"))
    for name in sorted(tree.sprint_archive):
        v.append(("sprint-archive", f"{SPRINT_ARCHIVE}/{name}", "archived sprint-status entries are build history"))
    for name in sorted(tree.handoff_archive):
        v.append(("handoff-archive", f"{HANDOFF_ARCHIVE}/{name}", "archived pairs are build history"))
    for name in sorted(tree.handoffs):
        v.append(("pair", f"{HANDOFFS}/{name}", "a pair is session state; the pristine template starts at S1 with none"))
    for rel in sorted(tree.texts):
        for no in probe_mentions(rel, tree.texts[rel]):
            v.append(("probe", f"{rel}:{no}", f"names the probe repository; a citation that matters names the "
                                              "archive repository instead (decision 2026-09-23-003)"))
    return v


# ==============================================================================
# Skeletons and the plan — pure
# ==============================================================================

def status_skeleton(date: str) -> str:
    """The template's own sprint-status: one S1 entry, no history. The state gate numbers the
    session from the heading, and the closeout of the first maintenance session scaffolds S2."""
    return f"""# Sprint Status

**Current Phase:** Template maintenance
**Current Focus:** The pristine template; its build history is in the archive repository
**Last Updated:** {date}
**Updated By:** S1

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (setup, update cadence, sprint boundaries).
>
> **READ SELECTIVELY (index-first).** Read the header (Current Phase/Focus) and the newest session
> update first; older updates are context, not required reading. Keep the last 10 updates visible and
> archive older ones — `scripts/session_closeout.py --check` enforces the cap. Markdown only (never JSON).
> Every entry is headed `## S<N> — YYYY-MM-DD — <title>`; the gate reads the session number from it.

---

## S1 — {date} — Pristine template

**Status:** The template at its pristine start (decision 2026-09-23-003). Its build history, the
sprint entries, handoff pairs and `TMPL` epics of the sessions that built it, lives in the archive
repository that decision names. Nothing here is a project's state: the initializer regenerates
this file and the tracker at a project's birth.

### Done

1. `scripts/sanitize_template.py --apply`; its `--check` exit 0 and the suite green.

### Blockers

- None.

---

<!-- Add new session updates ABOVE this line, newest first, headed `## S<N> — YYYY-MM-DD — title` -->
<!-- Each entry: Done (by story ID), Blockers. Next-session tasks live in the kickoff, not here. -->
<!-- Keep the last 10 entries visible; move older ones to sprint/archive/ (the gate enforces the cap) -->
"""


def tracker_skeleton() -> str:
    """The initializer's tracker with its tokens kept: `{{DATE}}` is filled at a project's birth,
    not here, and the ID example falls back to the skeleton's own."""
    return new_project.story_tracker_skeleton({"DATE": "{{DATE}}", "PREFIX": ""})


def plan(paths: list[str]) -> list[tuple[str, str]]:
    """(action, path) over a list of committed paths: `regen` for the two sprint documents,
    `remove` for every path a clear glob matches, nothing else. Pure, so a fixture can prove
    the plan never reaches a NEVER_RESET path, a profile file or a filled file."""
    out: list[tuple[str, str]] = [("regen", rel) for rel in REGENERATE_FILES]
    for rel in sorted(paths):
        if any(fnmatch.fnmatchcase(rel, pattern) for pattern in CLEAR_GLOBS):
            out.append(("remove", rel))
    return out


# ==============================================================================
# The real tree
# ==============================================================================

def committed_files() -> list[str]:
    """Paths git would commit: tracked plus untracked-and-not-ignored, as the state gate and
    the banned-feature scan read them."""
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        return [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    return out.stdout.splitlines()


def text_of(rel: str) -> str | None:
    """The file's text, or None for a binary (a NUL byte) or a missing file."""
    path = ROOT / rel
    if not path.is_file():
        return None
    data = path.read_bytes()
    if b"\0" in data:
        return None
    return data.decode("utf-8", errors="ignore")


def names_in(rel_dir: str) -> list[str]:
    d = ROOT / rel_dir
    if not d.is_dir():
        return []
    return sorted(p.name for p in d.iterdir() if p.is_file() and not p.name.startswith("."))


def read_tree() -> tuple[Tree, list[str]]:
    paths = committed_files()
    texts = {rel: t for rel in paths if (t := text_of(rel)) is not None}
    return Tree(
        status=text_of(STATUS),
        tracker=text_of(TRACKER),
        handoffs=names_in(HANDOFFS),
        handoff_archive=names_in(HANDOFF_ARCHIVE),
        sprint_archive=names_in(SPRINT_ARCHIVE),
        texts=texts,
    ), paths


def refused(force: bool) -> bool:
    """The inverse of the initializer's refusal: run only where origin is the template."""
    url = new_project.origin_url()
    if new_project.is_template_repo(url) or force:
        return False
    print(f"sanitize_template: REFUSED — origin is not the template ({url or 'no origin'}).")
    print("  This script resets the template's own sprint state and nothing else's.")
    print("  A project starts clean through scripts/new_project.py instead.")
    print("  Use --force only if you are deliberately re-scaffolding a copy of the template.")
    return True


def report(title: str, v: list[tuple[str, str, str]]) -> int:
    print(f"\n{title}")
    print("=" * 60)
    if not v:
        print("PASSED: no build state remains")
        return 0
    print(f"BLOCKED: {len(v)} item(s) of build state\n")
    for rule, where, detail in v:
        print(f"  {where}\n    Rule:   {rule}\n    Detail: {detail}\n")
    return 1


def cmd_check() -> int:
    tree, _ = read_tree()
    return report("Sanitize Template Check", violations(tree))


def cmd_apply(apply: bool) -> int:
    _, paths = read_tree()
    date = datetime.date.today().isoformat()
    mode = "APPLY" if apply else "DRY RUN"
    print(f"\nSanitize Template — {mode}")
    print("=" * 60)
    skeletons = {STATUS: status_skeleton(date), TRACKER: tracker_skeleton()}
    for action, rel in plan(paths):
        print(f"  {action:8} {rel}")
        if not apply:
            continue
        if action == "regen":
            (ROOT / rel).write_text(skeletons[rel], encoding="utf-8")
        else:
            (ROOT / rel).unlink()
    print(f"\n  kept: {', '.join(NEVER_RESET)}")
    print("        every {{TOKEN}}, both profile blocks; no .project-profile is written")
    if not apply:
        print("\nDRY RUN — nothing written. Re-run with --apply.")
        return 0
    print("\nRunning the gate suite to prove the sanitized tree is green...")
    result = subprocess.run(["pre-commit", "run", "--all-files"], cwd=ROOT, check=False)
    if result.returncode != 0:
        print("\nBLOCKED: the suite did not pass.")
        return 1
    print("\nPASSED: sanitized and every gate is green. Run --check to name what the sweep left.")
    return 0


# ==============================================================================
# SELF-TEST — in-memory fixtures, run on every commit
# ==============================================================================

_CLEAN = Tree(status=status_skeleton("2026-09-24"), tracker=tracker_skeleton(),
              handoffs=[], handoff_archive=[], sprint_archive=[],
              texts={"README.md": "# A template\n", SELF: f'PROBE_NAME = "{PROBE_NAME}"\n'})
_HISTORY = ("# Sprint Status\n\n---\n\n## S12 — 2026-09-24 — later\n\ntext\n\n"
            "## S11 — 2026-09-24 — earlier\n\ntext\n\n## S1 — 2026-09-21 — first\n\ntext\n")
_TMPL_ROW = "| TMPL-4.2 | sanitizer | Not Started | — | — | 2026-09-23-003 |\n"


def _rules(found: list) -> list[str]:
    return sorted(r for r, *_ in found)


def run_self_test() -> int:
    print("\nSanitize Template Self-Test")
    print("=" * 60)
    failures = total = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    check("a pristine tree passes", violations(_CLEAN) == [], str(violations(_CLEAN)))

    found = violations(_CLEAN._replace(status=_HISTORY))
    check("every sprint-status entry above S1 is named; S1 is not",
          _rules(found) == ["session", "session"] and "S12" in found[0][2] and "S11" in found[1][2], str(found))

    found = violations(_CLEAN._replace(tracker=_CLEAN.tracker + "\n## Epic: TMPL-4 — Pristine\n\n" + _TMPL_ROW))
    check("a TMPL- story row is named, under any epic", _rules(found) == ["tmpl-story"] and "TMPL-4.2" in found[0][2],
          str(found))
    found = violations(_CLEAN._replace(tracker=_CLEAN.tracker + "\nThe template's own evolution used TMPL-4.2.\n"))
    check("a TMPL- mention in prose is not a story row", found == [], str(found))

    found = violations(_CLEAN._replace(sprint_archive=["sprint-status_2026.md"]))
    check("a file in sprint/archive/ is named", _rules(found) == ["sprint-archive"]
          and found[0][1] == "sprint/archive/sprint-status_2026.md", str(found))
    found = violations(_CLEAN._replace(handoff_archive=["HANDOFF_S2.md", "KICKOFF_S2.md"]))
    check("every file in sprint/handoffs/archive/ is named", _rules(found) == ["handoff-archive"] * 2, str(found))
    found = violations(_CLEAN._replace(handoffs=["HANDOFF_S13.md", "KICKOFF_S13.md"]))
    check("a pair in sprint/handoffs/ is named, both files", _rules(found) == ["pair", "pair"]
          and {w for _, w, _ in found} == {"sprint/handoffs/HANDOFF_S13.md", "sprint/handoffs/KICKOFF_S13.md"}, str(found))

    texts = {**_CLEAN.texts, "docs/x.md": f"a\nproved on `{PROBE_NAME}` twice\n"}
    found = violations(_CLEAN._replace(texts=texts))
    check("the probe's name in a text file is named by file and line",
          _rules(found) == ["probe"] and found[0][1] == "docs/x.md:2", str(found))
    check("this script is the one file allowed to hold the name",
          probe_mentions(SELF, f"x {PROBE_NAME}\n") == [] and probe_mentions("scripts/other.py", f"x {PROBE_NAME}\n") == [1])

    status = status_skeleton("2026-09-24")
    check("the regenerated sprint-status is S1 alone, headed as the gate reads it",
          session_closeout.newest_session(status) == 1 and len(session_closeout.status_headings(status)) == 1
          and sessions_above_one(status) == [])
    _, unknown = new_project.remaining_tokens(status)
    check("the regenerated sprint-status carries no unfilled token", not unknown, str(sorted(unknown)))

    tracker = tracker_skeleton()
    computed, declared, ids = session_closeout.tracker_counts(tracker)
    check("the regenerated tracker holds the example epic alone and reconciles at zero",
          not ids and not session_closeout.tracker_violations(computed, declared)
          and "[EXAMPLE]" in tracker and tmpl_stories(tracker) == [], f"ids={sorted(ids)}")
    check("the regenerated tracker keeps its {{DATE}} token, which the initializer fills at a project's birth",
          "**Last Updated:** {{DATE}}" in tracker)

    paths = ["AGENTS.md", "CONSTITUTION.md", ".resources-version", "sprint/decision-log.md",
             "docs/governance/framework_decisions.md", "docs/orchestration/knowledge/INDEX.md",
             "docs/personas/framework-maintainer.md", "sprint/recovery/README.md",
             "sprint/handoffs/HANDOFF_S13.md", "sprint/handoffs/KICKOFF_S13.md",
             "sprint/handoffs/archive/HANDOFF_S2.md", "sprint/archive/sprint-status_2026.md"]
    planned = plan(paths)
    removed = sorted(rel for a, rel in planned if a == "remove")
    check("the plan regenerates the two sprint documents and removes the pairs and both archives",
          [rel for a, rel in planned if a == "regen"] == [STATUS, TRACKER]
          and removed == ["sprint/archive/sprint-status_2026.md", "sprint/handoffs/HANDOFF_S13.md",
                          "sprint/handoffs/KICKOFF_S13.md", "sprint/handoffs/archive/HANDOFF_S2.md"], str(planned))
    touched = {rel for _, rel in planned}
    check("the plan reaches no NEVER_RESET path: the framework decisions, the log, the knowledge base, "
          "the personas, the sync stamp",
          not any(rel.startswith(p.rstrip("/")) for rel in touched for p in NEVER_RESET), str(sorted(touched)))
    check("without the fill: no filled file, no profile file, no template-only file is touched",
          not touched & (set(new_project.FILL_FILES) | set(new_project.TEMPLATE_ONLY) | {".project-profile", ".template-version"}),
          str(sorted(touched)))
    check("the clear globs are the initializer's plus the sprint-status archive",
          set(new_project.CLEAR_GLOBS) - {".resources-version"} < set(CLEAR_GLOBS)
          and "sprint/archive/*.md" in CLEAR_GLOBS)

    accepted = [u for u, is_tmpl in [("git@github.com-personal:SaltyBrett/agentic-dev-template.git", True),
                                      ("/Users/x/code/agentic-dev-template", True),
                                      ("git@github.com:SaltyBrett/my-real-project.git", False),
                                      ("git@github.com:SaltyBrett/agentic-dev-template-archive.git", False),
                                      (None, False)]
                if new_project.is_template_repo(u) is not is_tmpl]
    check("the refusal is the initializer's inverse: the template's origin runs, a project's is refused",
          not accepted, f"misjudged {accepted}")

    check("the sanitized snapshot passes as a whole",
          violations(Tree(status, tracker, [], [], [], {SELF: f'"{PROBE_NAME}"', "AGENTS.md": "# brain\n"})) == [])

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Return the template to its pristine state")
    parser.add_argument("--check", action="store_true", help="Exit 1 while build state remains, each item named")
    parser.add_argument("--apply", action="store_true", help="Write the reset and run the suite (default: dry run)")
    parser.add_argument("--force", action="store_true", help="Override the not-the-template refusal")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if refused(args.force):
        return 1
    if args.check:
        return cmd_check()
    return cmd_apply(args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
