#!/usr/bin/env python3
"""
template_update.py — take a project created from this template to a newer release.

WHAT THIS IS THE INVERSE OF
---------------------------
`new_project.py` runs once, at birth: it fills tokens, regenerates the sprint files,
clears the handoffs and stamps `.template-version`, the mark of a project. Nothing
then carried a later release into the project but a kickoff listing the files to copy
by name: a checklist, which this repository converts into a control.

WHO OWNS WHAT — three classes, decided by path (`classify`)
------------------------------------------------------------
  keep       Never written. `sprint/` (the project's decision log included, and the session's
             gitignored journal and working notes), the project's persona roster `.claude/agents/`, `.claude/settings.local.json` (one
             operator's), and the content folders the template ships empty (`docs/prd/`,
             `evidence/`, `infra/`, ...). A template change under one of these is named in one
             summary line and not applied.
  merge      `docs/orchestration/knowledge/INDEX.md`, merged by slug so the project's rows are
             never touched: a row the release adds is inserted, one it changed is updated
             and one it dropped is removed, each only where the project's copy still
             equals the previous release's; an edited row is reported and left.
  three-way  Everything else, through `git merge-file` over base (the release the
             project is on), current (the project's copy) and other (the target). That
             includes `.claude/skills/`, `.claude/rules/` and `.claude/settings.json`: the
             template's, which a project may edit and extend; a
             skill or rule the project added is in neither release and never touched. And the
             persona library `personas/`, which a project activates from.
             A copy the project never edited takes the template's version outright.
             An edited copy takes the template's change where the two do not overlap.
             An overlap is a conflict: the file is left alone and named, and the run
             refuses to stamp until `--take` or `--keep` settles it. One path is the
             exception: `.gitignore`, where project and template both append at the end,
             is merged with `--union`, both sides' lines kept, the project's first, and
             the dry run names it `union`.

`.template-version` is stamped last, so an incomplete run leaves the old stamp.

HOW THE RELEASES ARE READ
-------------------------
Both releases are fetched from `--source` into `refs/template/<version>` — outside
`refs/tags/`, so they never mix with the project's own tags. They stay
after the run: `git diff refs/template/vOLD refs/template/vNEW -- <path>` shows what
a conflict is about.

THE UPDATER UPDATES ITSELF, SO RUN THE TARGET'S COPY
-----------------------------------------------------
The ownership map lives in this file and may change between releases. The run refuses
when the file being executed differs from the target release's copy, and prints the
two commands that fetch it; a target that carries no updater has no map, and `target_refusal`
refuses it.

Usage:
    python3 scripts/template_update.py --source <url-or-path> --to vX.Y.Z           # dry run
    python3 scripts/template_update.py --source <url-or-path> --to vX.Y.Z --apply   # write; then the suite runs
        ... --take <path>    resolve a conflict with the template's copy (repeatable)
        ... --keep <path>    resolve a conflict with the project's copy  (repeatable)
    python3 scripts/template_update.py --self-test
Exit 0 = clean, 1 = refused, a conflict, or the suite failed, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import new_project        # noqa: E402 — the initializer's lists, cross-checked against this map

ROOT = Path(__file__).resolve().parents[1]
SELF = "scripts/template_update.py"
VERSION_FILE = ".template-version"
REF_PREFIX = "refs/template/"
VERSION = re.compile(r"^v\d+\.\d+\.\d+$")

ROSTER = ".claude/agents/"
LIBRARY = "personas/"

# Project-owned: never written. Everything not listed here or in MERGE is three-way merged.
KEEP = [
    "sprint/",
    "docs/prd/", "docs/architecture/", "docs/executive/", "docs/research/",
    "docs/testing/", "docs/runbooks/", "evidence/", "infra/", "resources/branding/",
    # The roster: the personas this project activated from the library or drafted itself. A release ships the library in personas/ and never a roster.
    ROSTER,
    # One operator's Claude Code permissions (new_project.LOCAL_STATE): gitignored, so a release
    # should never hold it; kept in case one ever does, since it would carry personal grants.
    ".claude/settings.local.json",
    # The template's MIT license arrives at birth and is the project's from then on: a project
    # keeps it or replaces it with its own, and a release never rewrites a project's license.
    "LICENSE",
    # The project's front page, written at birth for its users; the template's README is an
    # adopter's, and a release never writes over the project's.
    # new_project.README, spelled out: this file runs in a project beside the older release's
    # initializer, which may not name it.
    "README.md",
]
MERGE = {
    "docs/orchestration/knowledge/INDEX.md": "index",
}
SPECIAL = {VERSION_FILE}
# Merged with `git merge-file --union` where both sides changed one place: both sides' lines are
# kept, the project's first. Project and template both append at the end of this file, so a line
# merge conflicts every time; the one order that matters, a `!` line after the pattern it reverses,
# the template's exact paths never meet. Every other three-way path still conflicts.
UNION = {".gitignore"}

ENTRIES_HEADING = re.compile(r"^##\s+Entries\s*$", re.IGNORECASE)
INDEX_ROW = re.compile(r"^\|\s*\[([^\]]+)\]\(")
SEPARATOR = re.compile(r"^\|[\s:|-]+\|\s*$")


class MergeError(Exception):
    """A table this script must merge has lost its structure."""


# ==============================================================================
# Pure decisions — no git, no files, so the self-test covers them directly
# ==============================================================================

def classify(path: str) -> str:
    if path in SPECIAL:
        return "special"
    if path in MERGE:
        return "merge"
    for prefix in KEEP:
        if path == prefix or path.startswith(prefix):
            return "keep"
    return "three-way"


def verdict(current: bytes | None, base: bytes | None, other: bytes | None) -> tuple[str, bytes | None]:
    """What happens to one three-way path. Returns (verdict, bytes to write or None)."""
    if base == other:
        return "unchanged", None                # the template did not change it
    if other is None:                           # the template removed it
        if current is None:
            return "unchanged", None
        return ("delete", None) if current == base else ("template-removed", None)
    if current is None:
        return ("add", other) if base is None else ("project-removed", None)
    if current == other:
        return "up-to-date", None
    if current == base:
        return "update", other
    return "merge", None                        # both sides changed; git merge-file decides


def normalized(data: bytes | None) -> bytes | None:
    """Blobs are LF; a checkout may be CRLF. Compare and merge on LF, as git commits."""
    return None if data is None else data.replace(b"\r\n", b"\n")


def three_way(current: bytes, base: bytes, other: bytes, union: bool = False) -> tuple[bool, bytes]:
    """`git merge-file` on temp copies. Returns (clean, merged); merged carries markers when not clean.
    With `union`, an overlap keeps both sides' lines, the project's first, and is never a conflict."""
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, data in (("current", current), ("base", base), ("other", other)):
            p = Path(d) / name
            p.write_bytes(data)
            paths.append(str(p))
        r = subprocess.run(
            ["git", "merge-file", *(["--union"] if union else []),
             "-L", "project", "-L", "previous release", "-L", "template", *paths],
            capture_output=True, check=False,
        )
        merged = Path(paths[0]).read_bytes()
    if r.returncode < 0 or r.returncode > 127:
        raise RuntimeError(f"git merge-file failed: {r.stderr.decode(errors='replace').strip()}")
    return r.returncode == 0, merged


def table(text: str, heading: re.Pattern) -> tuple[list[str], int, int]:
    """(lines, first data row index, end index) of the table under `heading`."""
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if heading.match(ln)), None)
    if start is None:
        raise MergeError(f"no heading matching {heading.pattern!r}")
    sep = next((i for i in range(start + 1, len(lines)) if SEPARATOR.match(lines[i])), None)
    if sep is None:
        raise MergeError(f"no table beneath {heading.pattern!r}")
    end = sep + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    return lines, sep + 1, end


def keyed(text: str | None, heading: re.Pattern, key_of) -> dict[str, str]:
    if text is None:
        return {}
    lines, first, end = table(text, heading)
    return {k: ln for ln in lines[first:end] if (k := key_of(ln))}


def slug_key(line: str) -> str | None:
    m = INDEX_ROW.match(line)
    return m.group(1) if m else None


def merge_rows(current: str, old: str | None, new: str, heading: re.Pattern, key_of) -> tuple[str, list]:
    """Merge one keyed table. Rows the template never had belong to the project and are untouched.

    A template row the project lacks is inserted at the top of the table. A row the template
    changed is updated only if the project's copy still equals the previous release's; an edited
    row is reported. A row for a key the template dropped is removed on the same condition.
    """
    lines, first, end = table(current, heading)
    cur = {k: ln for ln in lines[first:end] if (k := key_of(ln))}
    old_rows = keyed(old, heading, key_of)
    new_rows = keyed(new, heading, key_of)
    actions: list[tuple[str, str]] = []
    inserts: list[str] = []
    for key, row in new_rows.items():
        if key not in cur:
            inserts.append(row)
            actions.append(("insert-row", key))
        elif cur[key] == row:
            continue
        elif cur[key] == old_rows.get(key):
            lines[lines.index(cur[key])] = row
            actions.append(("update-row", key))
        else:
            actions.append(("row-edited", key))
    for key, row in old_rows.items():
        if key in new_rows or key not in cur:
            continue
        if cur[key] == row:
            lines.remove(row)
            actions.append(("remove-row", key))
        else:
            actions.append(("row-edited", key))
    lines[first:first] = inserts
    return "\n".join(lines) + ("\n" if current.endswith("\n") else ""), actions


def merge_index(current: str, old: str | None, new: str) -> tuple[str, list]:
    return merge_rows(current, old, new, ENTRIES_HEADING, slug_key)


MERGERS = {"index": merge_index}


# ==============================================================================
# The plan over a real project
# ==============================================================================

@dataclass
class Step:
    path: str
    verdict: str
    write: bytes | None = None
    delete: bool = False
    notes: list[str] = field(default_factory=list)


def git(*args: str, binary: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False, text=not binary)


def fetch(source: str, versions: list[str]) -> str | None:
    r = git("fetch", "--no-tags", "--quiet", source, *[f"+refs/tags/{v}:{REF_PREFIX}{v}" for v in versions])
    return None if r.returncode == 0 else r.stderr.strip()


def tree(version: str) -> set[str]:
    r = git("ls-tree", "-r", "--name-only", "-z", f"{REF_PREFIX}{version}")
    if r.returncode:
        raise RuntimeError(f"cannot read {REF_PREFIX}{version}: {r.stderr.strip()}")
    return {p for p in r.stdout.split("\0") if p}


def blob(version: str, path: str) -> bytes | None:
    r = git("cat-file", "blob", f"{REF_PREFIX}{version}:{path}", binary=True)
    return r.stdout if r.returncode == 0 else None


def current_bytes(path: str) -> bytes | None:
    p = ROOT / path
    return normalized(p.read_bytes()) if p.is_file() else None


def plan_path(path: str, cls: str, current: bytes | None, base: bytes | None, other: bytes | None,
              takes: set[str], keeps: set[str]) -> Step | None:
    """One path the template changed between the releases: its step, or None when nothing is to be
    done. A project-owned path comes back as `not applied`."""
    if cls == "keep":
        return Step(path, "not applied")
    if path in takes and other is not None:
        return Step(path, "take", other)
    if path in keeps:
        return Step(path, "keep", notes=["kept by --keep"])
    if cls == "merge":
        if current is None:
            return Step(path, "add", other)
        try:
            text, actions = MERGERS[MERGE[path]](
                current.decode("utf-8"),
                None if base is None else base.decode("utf-8"),
                other.decode("utf-8") if other is not None else current.decode("utf-8"),
            )
        except MergeError as e:
            return Step(path, "CONFLICT", notes=[str(e)])
        changed = text != current.decode("utf-8")
        return Step(path, "merge" if changed else "up-to-date", text.encode("utf-8") if changed else None,
                    notes=[f"{kind} {key}" for kind, key in actions])
    v, content = verdict(current, base, other)
    if v == "unchanged":
        return None
    if v == "merge":
        if path in UNION:
            _, merged = three_way(current, base, other, union=True)
            return Step(path, "union", merged, notes=[
                "both sides' lines kept where both changed one place, the project's first: read it in `git diff`"])
        clean, merged = three_way(current, base, other)
        return Step(path, "merge", merged) if clean else Step(path, "CONFLICT")
    return Step(path, v, content, delete=(v == "delete"))


def tracked(*prefixes: str) -> list[str]:
    return [p for p in git("ls-files", "-z", "--", *prefixes).stdout.split("\0") if p]


def build_plan(frm: str, to: str, takes: set[str], keeps: set[str]) -> tuple[list[Step], list[str]]:
    steps: list[Step] = []
    kept: list[str] = []
    for path in sorted(tree(frm) | tree(to)):
        cls = classify(path)
        if cls == "special":
            continue
        base = normalized(blob(frm, path))
        other = normalized(blob(to, path))
        if base == other:
            continue
        step = plan_path(path, cls, current_bytes(path), base, other, takes, keeps)
        if step is not None and step.verdict == "not applied":
            kept.append(path)
        elif step is not None:
            steps.append(step)
    return steps, kept


def target_refusal(target_self: bytes | None, running: bytes, to: str, source: str) -> list[str]:
    """Why the run must stop before planning, as the lines to print, or [] to go on. The map lives
    in this file, so only the target's own copy may plan its release; a target that carries no
    updater has no map to apply."""
    if target_self is None:
        return [f"template_update: REFUSED - {to} carries no {SELF}, so it has no ownership map to apply."]
    if normalized(target_self) != normalized(running):
        return [f"template_update: REFUSED - this file differs from the updater in {to}.",
                "  The ownership map may have changed. Run the target's copy:",
                f"    git show {REF_PREFIX}{to}:{SELF} > {SELF}",
                f"    python3 {SELF} --source {source} --to {to}"]
    return []


def dirty_paths() -> list[str]:
    out = git("status", "--porcelain").stdout.splitlines()
    return [ln[3:] for ln in out if ln.strip() and ln[3:] != SELF]


def main() -> int:
    parser = argparse.ArgumentParser(description="Take a derived project to a newer template release")
    parser.add_argument("--source", help="The template repository: a URL or a local path")
    parser.add_argument("--to", metavar="vX.Y.Z", help="The release to take")
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry run)")
    parser.add_argument("--take", action="append", default=[], metavar="PATH",
                        help="Resolve a conflict by taking the template's copy")
    parser.add_argument("--keep", action="append", default=[], metavar="PATH",
                        help="Resolve a conflict by keeping the project's copy")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if not args.source or not args.to:
        print("template_update: --source and --to are required (or use --self-test)", file=sys.stderr)
        return 2
    if not VERSION.match(args.to):
        print(f"template_update: --to must be vMAJOR.MINOR.PATCH, got {args.to!r}", file=sys.stderr)
        return 2
    if new_project.is_template_repo(new_project.origin_url()):
        print("template_update: REFUSED — origin is the template's own repository. This runs in a derived project.")
        return 1
    stamp = ROOT / VERSION_FILE
    if not stamp.is_file():
        print(f"template_update: no {VERSION_FILE}. Write the release this project was created from "
              "to it, then re-run.", file=sys.stderr)
        return 2
    frm = stamp.read_text(encoding="utf-8").strip()
    if not VERSION.match(frm):
        print(f"template_update: {VERSION_FILE} holds {frm!r}, not vMAJOR.MINOR.PATCH", file=sys.stderr)
        return 2
    if frm == args.to:
        print(f"template_update: already on {frm}.")
        return 0
    err = fetch(args.source, [frm, args.to])
    if err:
        print(f"template_update: cannot fetch {frm} and {args.to} from {args.source}:\n  {err}")
        return 1

    # The map is in this file. Run the target's copy, or the plan is the previous release's idea.
    refusal = target_refusal(blob(args.to, SELF), Path(__file__).read_bytes(), args.to, args.source)
    if refusal:
        print("\n".join(refusal))
        return 1

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"\nTemplate Update — {mode}")
    print("=" * 60)
    print(f"Project: {ROOT.name}   {frm} -> {args.to}")

    if args.apply and (dirty := dirty_paths()):
        print(f"\nREFUSED: the tree has {len(dirty)} uncommitted path(s). Commit or stash first, so "
              "`git diff` afterwards shows exactly what the update did.")
        return 1

    steps, kept = build_plan(frm, args.to, set(args.take), set(args.keep))
    conflicts = [s for s in steps if s.verdict == "CONFLICT"]
    for s in steps:
        print(f"  {s.verdict:<12}{s.path}")
        for n in s.notes:
            print(f"  {'':<12}  {n}")
    if kept:
        print(f"  {'not applied':<12}{len(kept)} template change(s) under project-owned paths: "
              + ", ".join(kept))
    if conflicts:
        print(f"\n{len(conflicts)} CONFLICT(s): both the project and the template changed the same lines.")
        for s in conflicts:
            print(f"  git diff {REF_PREFIX}{frm} {REF_PREFIX}{args.to} -- {s.path}")
        print("  Edit the file and re-run with --keep <path>, or take the template's copy with --take <path>.")
    print(f"  {'stamp':<12}{VERSION_FILE}  ({args.to})" + ("" if not conflicts else "  — withheld until resolved"))

    if not args.apply:
        print("\nDRY RUN — nothing written. Re-run with --apply.")
        return 1 if conflicts else 0

    for s in steps:
        p = ROOT / s.path
        if s.delete:
            p.unlink()
        elif s.write is not None:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(s.write)
    if conflicts:
        print("\nApplied what merges cleanly; the conflicted files are untouched and the stamp is withheld.")
        return 1
    stamp.write_text(args.to + "\n", encoding="utf-8")

    print("\nRunning the gate suite to prove the project is green on the new release...")
    result = subprocess.run(["pre-commit", "run", "--all-files"], cwd=ROOT, check=False)
    if result.returncode != 0:
        print(f"\nBLOCKED: the suite did not pass on {args.to}. Fix before committing; the stamp is written.")
        return 1
    print(f"\nPASSED: on {args.to} and every gate is green. Review with `git diff`, then commit.")
    return 0


# ==============================================================================
# SELF-TEST — in-memory fixtures, run on every commit
# ==============================================================================

_INDEX = ("# Knowledge Base — Index\n\nprose mentioning [x](x.md)\n\n## Entries\n\n"
          "| Slug | Summary | Type |\n|------|---------|------|\n"
          "| [reference_b](reference_b.md) | B, as shipped | reference |\n"
          "| [reference_a](reference_a.md) | A | reference |\n"
          "<!-- Add one row per knowledge entry above this line, newest first -->\n")
_INDEX_NEW = _INDEX.replace("| [reference_b](reference_b.md) | B, as shipped | reference |\n",
                            "| [reference_c](reference_c.md) | C, new | reference |\n"
                            "| [reference_b](reference_b.md) | B, reworded | reference |\n")
_PROJECT_INDEX = _INDEX.replace("| [reference_b]", "| [project_x](project_x.md) | the project's own | project |\n| [reference_b]")


def run_self_test() -> int:
    print("\nTemplate Update Self-Test")
    print("=" * 60)
    failures = total = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    entry = "docs/orchestration/" + "knowledge/reference_x.md"   # built, so no entry's path is spelled
    want = {"scripts/x.py": "three-way", "AGENTS.md": "three-way", ".claude/agents/p.md": "keep",
            entry: "three-way", "docs/runbooks/new.md": "keep",
            "sprint/story-tracker.md": "keep", "sprint/handoffs/HANDOFF_S9.md": "keep",
            "sprint/decision-log.md": "keep", "docs/governance/gate_suite_runbook.md": "three-way",
            "docs/orchestration/knowledge/INDEX.md": "merge", ".template-version": "special",
            "docs/other/x.md": "three-way", "LICENSE": "keep"}
    bad = {p: classify(p) for p, w in want.items() if classify(p) != w}
    check("paths classify as keep, merge, three-way or special", not bad, str(bad))

    # Every Claude Code path the template ships, and the session's local banking.
    decided = {".claude/agents/framework-maintainer.md": "keep", ".claude/settings.local.json": "keep",
               "personas/framework-maintainer.md": "three-way",
               ".claude/skills/closeout/SKILL.md": "three-way", ".claude/skills/new-one/notes.md": "three-way",
               ".claude/rules/gate-scripts.md": "three-way", ".claude/settings.json": "three-way",
               "sprint/recovery/journal.md": "keep", "sprint/recovery/WORKING_NOTES.md": "keep"}
    bad = {p: classify(p) for p, w in decided.items() if classify(p) != w}
    check("the Claude Code paths and the recovery files classify as decided", not bad, str(bad))
    # The four classes are the whole map: the adoption class for projects born before the cut is
    # gone, and a path it held is an ordinary one.
    classes = {classify(p) for p in [*want, *decided]}
    check("no fifth class: every path is keep, merge, three-way or special",
          classes == {"keep", "merge", "three-way", "special"}, str(sorted(classes)))

    # The writing profile merges three-way, so a development path a release adds reaches a project
    # beside its own lines; a project's custom voice is in neither release, so no step names it.
    profile = (b'rules:\n  - paths:\n      - "AGENTS.md"\n      - "sprint/**"\n    voice: technical\n'
               b'    audience: development\ndefault: technical\nallow: []\n')
    ours = profile.replace(b"allow: []", b'allow: ["Amazon S3"]')
    theirs = profile.replace(b'      - "sprint/**"\n', b'      - "sprint/**"\n      - "docs/new/**"\n')
    step = plan_path("writing-profile.yaml", classify("writing-profile.yaml"), ours, profile, theirs, set(), set())
    check("the writing profile merges three-way: the release's new path and the project's allow line both kept",
          step is not None and step.verdict == "merge" and b'"docs/new/**"' in (step.write or b"")
          and b"Amazon S3" in (step.write or b""), str(step))
    voice = "docs/standards/voices/chair.md"
    check("a project's custom voice, in neither release, is left alone",
          classify(voice) == "three-way" and plan_path(voice, classify(voice), b"mine", None, None, set(), set()) is None)

    # The roster and the library are one path each, named in three places a project holds: the
    # closeout gate reads both, and the initializer and this map each decide them. A rename that
    # missed one would leave a project activating into a folder no gate reads, or a release writing
    # over a project's roster.
    import session_closeout  # lazy: the state gate, whose PyYAML import is itself lazy
    roster = session_closeout.PERSONAS.relative_to(session_closeout.ROOT).as_posix() + "/"
    library = session_closeout.LIBRARY.relative_to(session_closeout.ROOT).as_posix() + "/"
    check("the roster the gate reads is kept here and cleared by the initializer at birth",
          roster == ROSTER and roster in KEEP and classify(roster + "p.md") == "keep"
          and roster + "*.md" in new_project.CLEAR_GLOBS
          and roster not in new_project.NEVER_RESET,
          f"gate={roster} clear={new_project.CLEAR_GLOBS}")
    mutating = (set(new_project.FILL_FILES) | set(new_project.REGENERATE_FILES) | set(new_project.BIRTH_FILES)
                | set(new_project.CLEAR_GLOBS))
    check("the library the gate reads is merged here and in no list of the initializer",
          library == LIBRARY and classify(library + "p.md") == "three-way"
          and not any(m.startswith(library) for m in mutating | set(new_project.NEVER_RESET)),
          f"gate={library}")
    check("the initializer's local files are kept here, never carried by a release",
          all(classify(p) == "keep" for p in new_project.LOCAL_STATE),
          str({p: classify(p) for p in new_project.LOCAL_STATE}))
    merged_claude = [p for p in decided if p.startswith(".claude/") and decided[p] == "three-way"]
    check("what this map merges under .claude/ the initializer leaves as shipped",
          not any(p.startswith(m.split("*")[0]) for p in merged_claude for m in mutating),
          f"mutating={sorted(mutating)}")

    regen = [classify(p) for p in new_project.REGENERATE_FILES + new_project.BIRTH_FILES]
    cleared = [classify(g.split("*")[0]) for g in new_project.CLEAR_GLOBS]
    filled = [classify(p) for p in new_project.FILL_FILES]
    never = [classify(p) for p in new_project.NEVER_RESET]
    check("the map is the initializer's inverse: what it regenerates or clears is kept",
          set(regen) == {"keep"} and set(cleared) == {"keep"}, f"regen={regen} cleared={cleared}")
    check("what it fills is merged three-way, never overwritten — except the project's decision log, "
          "filled at birth and then the project's own (the framework's decisions no longer enter it)",
          all(classify(p) == "three-way" for p in new_project.FILL_FILES if p != "sprint/decision-log.md")
          and classify("sprint/decision-log.md") == "keep", f"filled={filled}")
    check("what it preserves at birth is carried by a release (the knowledge base) or is the project's own (its "
          "decision log), never by nothing",
          classify("sprint/decision-log.md") == "keep" and classify(entry) == "three-way"
          and set(never) <= {"merge", "keep", "three-way"},
          f"never={never}")

    step = plan_path(ROSTER + "p.md", "keep", b"mine", b"a", b"b", set(), set())
    check("a template change under a project-owned path is not applied",
          step is not None and step.verdict == "not applied" and step.write is None, str(step))

    # A target release is planned only by its own updater.
    check("a target that carries no updater is refused, naming it",
          any("carries no" in ln for ln in target_refusal(None, b"map", "v9.0.0", "src")))
    check("a target whose updater differs is refused, with the two commands that fetch it",
          len(target_refusal(b"other map", b"map", "v9.0.0", "src")) == 4)
    check("the target's own copy goes on, a CRLF checkout included",
          target_refusal(b"a\r\nb\r\n", b"a\nb\n", "v9.0.0", "src") == [])

    check("verdict: a path the template did not change is untouched, even if the project edited it",
          verdict(b"mine", b"a", b"a") == ("unchanged", None))
    check("verdict: a new template file is added", verdict(None, None, b"new") == ("add", b"new"))
    check("verdict: an unedited copy takes the template's version",
          verdict(b"a", b"a", b"b") == ("update", b"b"))
    check("verdict: a copy already on the target is up to date", verdict(b"b", b"a", b"b") == ("up-to-date", None))
    check("verdict: a file the template removed goes only if unedited",
          verdict(b"a", b"a", None) == ("delete", None) and verdict(b"mine", b"a", None) == ("template-removed", None))
    check("verdict: a file the project deleted is not brought back",
          verdict(None, b"a", b"b") == ("project-removed", None))
    check("verdict: edits on both sides go to the merge", verdict(b"mine", b"a", b"b") == ("merge", None))

    clean, merged = three_way(b"PROJECT\nb\nc\n", b"a\nb\nc\n", b"a\nb\nTEMPLATE\n")
    check("three-way: non-overlapping edits merge, keeping both",
          clean and merged == b"PROJECT\nb\nTEMPLATE\n", merged.decode(errors="replace"))
    clean, merged = three_way(b"a\nPROJECT\nc\n", b"a\nb\nc\n", b"a\nTEMPLATE\nc\n")
    check("three-way: the same line changed on both sides is a conflict, not a silent pick",
          not clean and b"<<<<<<<" in merged and b"PROJECT" in merged and b"TEMPLATE" in merged)

    # .gitignore by union: a project and a release both append at the end.
    gi_base = b"# ignores\n*.pyc\n"
    gi_project = gi_base + b"node_modules/\n.venv/\n"
    gi_template = gi_base + b"sprint/recovery/journal.md\n.claude/settings.local.json\n"
    step = plan_path(".gitignore", classify(".gitignore"), gi_project, gi_base, gi_template, set(), set())
    check("union: .gitignore appended at the end on both sides keeps both blocks, the project's first, named `union`",
          step is not None and step.verdict == "union"
          and step.write == gi_base + b"node_modules/\n.venv/\nsprint/recovery/journal.md\n.claude/settings.local.json\n",
          str(step))
    step = plan_path(".gitignore", "three-way", b"a\n.env*\nz\n", b"a\n.env\nz\n", b"a\n.env.local\nz\n", set(), set())
    check("union: the same line changed on both sides is kept twice, never a conflict or a pick",
          step is not None and step.verdict == "union" and step.write == b"a\n.env*\n.env.local\nz\n", str(step))
    step = plan_path("AGENTS.md", "three-way", gi_project, gi_base, gi_template, set(), set())
    check("union: any other path changed at the same place on both sides still conflicts",
          step is not None and step.verdict == "CONFLICT" and step.write is None, str(step))
    step = plan_path(".gitignore", "three-way", gi_base, gi_base, gi_template, set(), set())
    check("union: an unedited .gitignore takes the template's copy, as any path does",
          step is not None and step.verdict == "update" and step.write == gi_template, str(step))
    check("union: .gitignore is three-way, and the union set holds it alone",
          classify(".gitignore") == "three-way" and UNION == {".gitignore"})
    check("CRLF checkouts compare as LF", normalized(b"a\r\nb\r\n") == b"a\nb\n")

    text, actions = merge_index(_PROJECT_INDEX, _INDEX, _INDEX_NEW)
    rows = [ln for ln in text.splitlines() if ln.startswith("| [")]
    check("index: a missing entry's row is inserted at the top; the project's row survives",
          rows[0].startswith("| [reference_c]") and any("project_x" in r for r in rows)
          and ("insert-row", "reference_c") in actions, "\n".join(rows))
    check("index: an unedited row the template reworded is updated in place",
          "B, reworded" in text and "B, as shipped" not in text and ("update-row", "reference_b") in actions)
    edited = _PROJECT_INDEX.replace("B, as shipped", "B, edited by the project")
    text, actions = merge_index(edited, _INDEX, _INDEX_NEW)
    check("index: an edited row is reported and left alone",
          "B, edited by the project" in text and ("row-edited", "reference_b") in actions, str(actions))
    text, actions = merge_index(_INDEX_NEW, _INDEX_NEW, _INDEX)
    check("index: a row for an entry the template dropped is removed when unedited",
          "reference_c" not in text and ("remove-row", "reference_c") in actions, str(actions))
    check("index: the prose link above the table is never read as a row", slug_key("prose mentioning [x](x.md)") is None)
    try:
        merge_index("# Index\n\nno table here\n", _INDEX, _INDEX_NEW)
        check("index: a missing Entries table is refused, never treated as empty", False)
    except MergeError:
        check("index: a missing Entries table is refused, never treated as empty", True)


    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
