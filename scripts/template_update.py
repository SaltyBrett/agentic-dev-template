#!/usr/bin/env python3
"""
template_update.py — take a project created from this template to a newer release.

WHAT THIS IS THE INVERSE OF
---------------------------
`new_project.py` runs once, at birth: it fills tokens, regenerates the sprint files,
clears the handoffs, strips the other profile and stamps `.template-version`. Nothing
then carried a later release into the project. The first derived project (TMPL-2.3)
was told to copy files by name in its kickoff — a checklist, which this repository
converts into a control (decision 2026-09-22-004).

WHO OWNS WHAT — three classes, decided by path (`classify`)
------------------------------------------------------------
  keep       Never written. `sprint/` (the project's decision log included, since decision
             2026-09-23-003 keeps the framework's decisions out of it), `.project-profile`,
             and the content folders the template ships empty (`docs/prd/`, `evidence/`,
             `infra/`, ...). A template change under one of these is named in one
             summary line and not applied.
  merge      Two tables merged by key, so project rows are never touched:
             `docs/orchestration/knowledge/INDEX.md` by slug, and
             `docs/governance/framework_decisions.md` by decision ID (index row and body).
             A framework decision the file lacks is inserted, because the framework's
             knowledge entries declare `teaches:` against it and the freshness gate
             refuses an unindexed ID; a row or body the project edited is reported and
             left. Nothing is ever removed from it. Before v11.0.0 the framework decisions
             were inserted into `sprint/decision-log.md`; a project that took an earlier
             release keeps those copies, and the freshness gate lets the framework file
             win the duplicate IDs.
  three-way  Everything else, through `git merge-file` over base (the release the
             project is on), current (the project's copy) and other (the target).
             A copy the project never edited takes the template's version outright.
             An edited copy takes the template's change where the two do not overlap.
             An overlap is a conflict: the file is left alone and named, and the run
             refuses to stamp until `--take` or `--keep` settles it.

Template markdown is stripped to the project's profile before it is compared or
written, because the initializer stripped it at birth; without that, every document
with a profile block would look project-edited. `.template-version` is stamped last,
so an incomplete run leaves the old stamp.

HOW THE RELEASES ARE READ
-------------------------
Both releases are fetched from `--source` into `refs/template/<version>` — outside
`refs/tags/`, so the version gate, which reads `git tag`, never sees them. They stay
after the run: `git diff refs/template/vOLD refs/template/vNEW -- <path>` shows what
a conflict is about.

THE UPDATER UPDATES ITSELF, SO RUN THE TARGET'S COPY
-----------------------------------------------------
The ownership map lives in this file and may change between releases. The run refuses
when the file being executed differs from the target release's copy, and prints the
two commands that fetch it. A target that predates the updater is accepted with a
note. First adoption in a project that predates it is the same two commands.

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
import kb_freshness_scan  # noqa: E402 — the decision-index heading and parser
import new_project        # noqa: E402 — the initializer's lists, cross-checked against this map
import project_profile    # noqa: E402 — profile stripping, exactly as at birth

ROOT = Path(__file__).resolve().parents[1]
SELF = "scripts/template_update.py"
VERSION_FILE = ".template-version"
REF_PREFIX = "refs/template/"
VERSION = re.compile(r"^v\d+\.\d+\.\d+$")

# Project-owned: never written. The decision log sits under sprint/ but is merged (MERGE
# is consulted first). Everything not listed here or in MERGE is three-way merged.
KEEP = [
    "sprint/",
    ".project-profile",
    "docs/prd/", "docs/architecture/", "docs/executive/", "docs/research/",
    "docs/testing/", "docs/runbooks/", "evidence/", "infra/", "resources/branding/",
    # The template's hook-repository packaging, removed at birth (new_project.TEMPLATE_ONLY):
    # a project's pyproject.toml is its own, and a project is not a hook repository.
    "pyproject.toml", ".pre-commit-hooks.yaml",
    # The persona registry is dev-resources' (decision 2026-09-23-007): only resources_sync.py
    # writes it. Resource knowledge entries are the sync's too, but they share a directory with
    # the template's own entries, so they are told apart by content: see resource_owned().
    "docs/personas/",
    # The sync's stamp is this project's own state, like .project-profile: the initializer
    # clears it at birth and the updater never writes it. Found by the first derived project to
    # take v7.1.0, which received the template's stamp as an `add`.
    ".resources-version",
    # The template's MIT license arrives at birth and is the project's from then on: a project
    # keeps it or replaces it with its own, and a release never rewrites a project's license
    # (decision 2026-09-25-002).
    "LICENSE",
]
RESOURCE_KEY = re.compile(r"^source:\s*dev-resources\s*$", re.M)


def resource_owned(data: bytes | None) -> bool:
    """A knowledge entry that declares `source: dev-resources` in its frontmatter belongs to the
    sync, and this script leaves it alone whichever side changed it."""
    if not data or not data.startswith(b"---"):
        return False
    text = data.decode("utf-8", errors="replace")
    end = text.find("\n---", 3)
    return end != -1 and bool(RESOURCE_KEY.search(text[3:end]))
MERGE = {
    "docs/orchestration/knowledge/INDEX.md": "index",
    "docs/governance/framework_decisions.md": "decisions",
}
SPECIAL = {VERSION_FILE}

ENTRIES_HEADING = re.compile(r"^##\s+Entries\s*$", re.IGNORECASE)
INDEX_ROW = re.compile(r"^\|\s*\[([^\]]+)\]\(")
SEPARATOR = re.compile(r"^\|[\s:|-]+\|\s*$")
BODY_HEADING = re.compile(r"^## Decision (\S+):")


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


def prepared(path: str, data: bytes | None, profile: str | None) -> bytes | None:
    """Template content as the initializer would have written it into this project."""
    if data is None or profile is None or not path.endswith(".md"):
        return data
    return project_profile.strip_profiles(data.decode("utf-8"), profile).encode("utf-8")


def normalized(data: bytes | None) -> bytes | None:
    """Blobs are LF; a checkout may be CRLF. Compare and merge on LF, as git commits."""
    return None if data is None else data.replace(b"\r\n", b"\n")


def three_way(current: bytes, base: bytes, other: bytes) -> tuple[bool, bytes]:
    """`git merge-file` on temp copies. Returns (clean, merged); merged carries markers when not clean."""
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, data in (("current", current), ("base", base), ("other", other)):
            p = Path(d) / name
            p.write_bytes(data)
            paths.append(str(p))
        r = subprocess.run(
            ["git", "merge-file", "-L", "project", "-L", "previous release", "-L", "template", *paths],
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


def decision_key(line: str) -> str | None:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    did = cells[0] if cells else ""
    if not did or did.lower() == "id" or set(did) <= set("-: ") or did.startswith("[EXAMPLE]"):
        return None
    return did


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


def decision_bodies(text: str | None) -> dict[str, str]:
    """{id: body}: from `## Decision <id>:` to the next H2, trailing rule and blanks dropped."""
    if text is None:
        return {}
    lines = text.splitlines()
    h2 = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    out: dict[str, str] = {}
    for n, i in enumerate(h2):
        m = BODY_HEADING.match(lines[i])
        if not m or m.group(1).startswith("[EXAMPLE]"):
            continue
        body = lines[i:(h2[n + 1] if n + 1 < len(h2) else len(lines))]
        while body and (not body[-1].strip() or body[-1].strip() == "---" or body[-1].startswith("<!--")):
            body.pop()
        out[m.group(1)] = "\n".join(body)
    return out


def merge_index(current: str, old: str | None, new: str) -> tuple[str, list]:
    return merge_rows(current, old, new, ENTRIES_HEADING, slug_key)


def merge_decisions(current: str, old: str | None, new: str) -> tuple[str, list]:
    """Index rows by ID, then bodies by ID. Missing bodies are appended, as the log grows."""
    text, actions = merge_rows(current, old, new, kb_freshness_scan.INDEX_HEADING, decision_key)
    cur_b, old_b, new_b = decision_bodies(text), decision_bodies(old), decision_bodies(new)
    appended: list[str] = []
    for did, body in new_b.items():
        if did not in cur_b:
            appended.append(body)
            actions.append(("append-body", did))
        elif cur_b[did] == body:
            continue
        elif cur_b[did] == old_b.get(did):
            text = text.replace(cur_b[did], body, 1)
            actions.append(("update-body", did))
        else:
            actions.append(("body-edited", did))
    if appended:
        text = text.rstrip("\n") + "\n" + "".join(f"\n---\n\n{b}\n" for b in appended)
    return text, actions


MERGERS = {"index": merge_index, "decisions": merge_decisions}


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


def build_plan(frm: str, to: str, profile: str | None, takes: set[str], keeps: set[str]) -> tuple[list[Step], list[str]]:
    steps: list[Step] = []
    kept: list[str] = []
    for path in sorted(tree(frm) | tree(to)):
        cls = classify(path)
        if cls == "special":
            continue
        base = normalized(prepared(path, blob(frm, path), profile))
        other = normalized(prepared(path, blob(to, path), profile))
        if base == other:
            continue
        current = current_bytes(path)
        if cls == "keep" or any(resource_owned(d) for d in (current, base, other)):
            kept.append(path)
            continue
        if path in takes and other is not None:
            steps.append(Step(path, "take", other))
            continue
        if path in keeps:
            steps.append(Step(path, "keep", notes=["kept by --keep"]))
            continue
        if cls == "merge":
            if current is None:
                steps.append(Step(path, "add", other))
                continue
            try:
                text, actions = MERGERS[MERGE[path]](
                    current.decode("utf-8"),
                    None if base is None else base.decode("utf-8"),
                    other.decode("utf-8") if other is not None else current.decode("utf-8"),
                )
            except MergeError as e:
                steps.append(Step(path, "CONFLICT", notes=[str(e)]))
                continue
            step = Step(path, "merge" if text != current.decode("utf-8") else "up-to-date",
                        text.encode("utf-8") if text != current.decode("utf-8") else None)
            for kind, key in actions:
                step.notes.append(f"{kind} {key}")
            steps.append(step)
            continue
        v, content = verdict(current, base, other)
        if v == "unchanged":
            continue
        if v == "merge":
            clean, merged = three_way(current, base, other)
            steps.append(Step(path, "merge", merged) if clean else Step(path, "CONFLICT"))
            continue
        steps.append(Step(path, v, content, delete=(v == "delete")))
    return steps, kept


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
        print("template_update: REFUSED — origin is the template itself. This runs in a derived project.")
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
    try:
        profile = project_profile.read_profile(ROOT)
    except ValueError as e:
        print(f"template_update: {e}", file=sys.stderr)
        return 2

    err = fetch(args.source, [frm, args.to])
    if err:
        print(f"template_update: cannot fetch {frm} and {args.to} from {args.source}:\n  {err}")
        return 1

    # The map is in this file. Run the target's copy, or the plan is the previous release's idea.
    target_self = blob(args.to, SELF)
    if target_self is None:
        print(f"note: {args.to} carries no updater; this copy's ownership map is used.")
    elif normalized(target_self) != normalized(Path(__file__).read_bytes()):
        print(f"template_update: REFUSED — this file differs from the updater in {args.to}.")
        print("  The ownership map may have changed. Run the target's copy:")
        print(f"    git show {REF_PREFIX}{args.to}:{SELF} > {SELF}")
        print("    python3 " + SELF + f" --source {args.source} --to {args.to}")
        return 1

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"\nTemplate Update — {mode}")
    print("=" * 60)
    print(f"Project: {ROOT.name}   {frm} -> {args.to}   profile: {profile or 'none (all blocks kept)'}")

    if args.apply and (dirty := dirty_paths()):
        print(f"\nREFUSED: the tree has {len(dirty)} uncommitted path(s). Commit or stash first, so "
              "`git diff` afterwards shows exactly what the update did.")
        return 1

    steps, kept = build_plan(frm, args.to, profile, set(args.take), set(args.keep))
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

_LOG_HEAD = ("# Architectural Decision Log\n\n## How to Use This Log\n\n- notes\n\n---\n\n## Decision Index\n\n"
             "| ID | Date | Title | Status |\n|----|------|-------|--------|\n")
_ROW1 = "| 2026-09-20-001 | 2026-09-20 | First | APPROVED |\n"
_ROW2 = "| 2026-09-22-002 | 2026-09-22 | Second | APPROVED |\n"
_EX = "| [EXAMPLE] 2025-01-15-001 | 2025-01-15 | Sample | APPROVED |\n"
_BODY1 = ("## Decision 2026-09-20-001: First\n\n**Date:** 2026-09-20\n\n### Context\n\n"
          "| a | 2026-09-20 | table in a body | x |\n|---|---|---|---|\n\ntext\n")
_BODY2 = "## Decision 2026-09-22-002: Second\n\n**Date:** 2026-09-22\n\nbody two\n"
_BODY_EX = "## Decision [EXAMPLE] 2025-01-15-001: Sample\n\nexample\n"
_LOG_OLD = _LOG_HEAD + _ROW1 + _EX + "\n---\n\n" + _BODY_EX + "\n---\n\n<!-- Add new decisions above -->\n\n---\n\n" + _BODY1
_LOG_NEW = _LOG_HEAD + _ROW2 + _ROW1 + _EX + "\n---\n\n" + _BODY_EX + "\n---\n\n<!-- Add new decisions above -->\n\n---\n\n" + _BODY1 + "\n---\n\n" + _BODY2
_PROJ_ROW = "| PROJ-1 | 2026-09-23 | The project's own | APPROVED |\n"
_PROJ_BODY = "## Decision PROJ-1: The project's own\n\nours\n"
_LOG_PROJECT = _LOG_HEAD + _PROJ_ROW + _ROW1 + "\n---\n\n" + _BODY1 + "\n---\n\n" + _PROJ_BODY

_DOC = "intro\n<!-- profile:gcc -->\ngcc law\n<!-- /profile:gcc -->\n<!-- profile:commercial -->\nnone\n<!-- /profile:commercial -->\ntail\n"


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

    want = {"scripts/x.py": "three-way", "AGENTS.md": "three-way", "docs/personas/p.md": "keep",
            "docs/orchestration/knowledge/reference_x.md": "three-way", "docs/runbooks/new.md": "keep",
            "sprint/story-tracker.md": "keep", "sprint/handoffs/HANDOFF_S9.md": "keep",
            ".project-profile": "keep", "sprint/decision-log.md": "keep",
            "docs/governance/framework_decisions.md": "merge", "docs/governance/gate_suite_runbook.md": "three-way",
            "docs/orchestration/knowledge/INDEX.md": "merge", ".template-version": "special",
            "pyproject.toml": "keep", ".pre-commit-hooks.yaml": "keep", ".resources-version": "keep"}
    bad = {p: classify(p) for p, w in want.items() if classify(p) != w}
    check("paths classify as keep, merge, three-way or special", not bad, str(bad))

    regen = [classify(p) for p in new_project.REGENERATE_FILES]
    cleared = [classify(g.split("*")[0]) for g in new_project.CLEAR_GLOBS]
    filled = [classify(p) for p in new_project.FILL_FILES]
    never = [classify(p) for p in new_project.NEVER_RESET]
    template_only = [classify(p) for p in new_project.TEMPLATE_ONLY]
    check("the map is the initializer's inverse: what it regenerates, clears or removes is kept",
          set(regen) == {"keep"} and set(cleared) == {"keep"} and set(template_only) == {"keep"},
          f"regen={regen} cleared={cleared} template_only={template_only}")
    check("what it fills is merged three-way, never overwritten — except the project's decision log, "
          "filled at birth and then the project's own (the framework's decisions no longer enter it)",
          all(classify(p) == "three-way" for p in new_project.FILL_FILES if p != "sprint/decision-log.md")
          and classify("sprint/decision-log.md") == "keep", f"filled={filled}")
    check("what it preserves at birth is carried by a release (the framework decisions and the knowledge "
          "base) or by the resources sync (the persona registry) — never by nothing",
          classify("docs/governance/framework_decisions.md") == "merge" and classify("sprint/decision-log.md") == "keep"
          and classify("docs/orchestration/knowledge/x.md") == "three-way" and classify("docs/personas/") == "keep",
          f"never={never}")
    marked = b"---\nname: x\nteaches: []\nverified: 2026-09-23\nsource: dev-resources\n---\n\nbody\n"
    check("a knowledge entry that declares source: dev-resources is the sync's; an ordinary one, or the "
          "declaration outside the frontmatter, is not",
          resource_owned(marked) and not resource_owned(marked.replace(b"source: dev-resources\n", b""))
          and not resource_owned(b"no frontmatter\nsource: dev-resources\n") and not resource_owned(None))

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
    base = prepared("d.md", _DOC.encode(), "commercial")
    other = prepared("d.md", _DOC.replace("gcc law", "gcc law, amended").encode(), "commercial")
    check("a template change inside the other profile's block is no change for this project",
          base == other and b"gcc" not in base and b"none\n" in base)
    check("non-markdown and a profile-less project are never stripped",
          prepared("x.py", b"<!-- profile:gcc -->", "commercial") == b"<!-- profile:gcc -->"
          and prepared("d.md", _DOC.encode(), None) == _DOC.encode())
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

    text, actions = merge_decisions(_LOG_PROJECT, _LOG_OLD, _LOG_NEW)
    ids = set(kb_freshness_scan.parse_index(text))
    check("decisions: a framework decision the log lacks gets its row and its body",
          ids == {"PROJ-1", "2026-09-20-001", "2026-09-22-002"} and "body two" in text
          and ("insert-row", "2026-09-22-002") in actions and ("append-body", "2026-09-22-002") in actions,
          f"ids={sorted(ids)} actions={actions}")
    check("decisions: the IDs this merge reads are the IDs the freshness gate reads",
          set(keyed(_LOG_NEW, kb_freshness_scan.INDEX_HEADING, decision_key)) == set(kb_freshness_scan.parse_index(_LOG_NEW)))
    # The project's copy carries no [EXAMPLE] row or body; one in the template's must not arrive.
    check("decisions: the [EXAMPLE] row and body are never inserted", "[EXAMPLE]" not in text)
    check("decisions: the project's own row and body survive, and a body's table stays in its body",
          "| PROJ-1 |" in text and "ours" in text and "table in a body" in decision_bodies(text)["2026-09-20-001"])
    again, actions2 = merge_decisions(text, _LOG_OLD, _LOG_NEW)
    check("decisions: re-running is a no-op", again == text and not actions2, str(actions2))
    amended_new = _LOG_NEW.replace("| 2026-09-20-001 | 2026-09-20 |", "| 2026-09-20-001 | 2026-09-20; amended 2026-09-23 |")
    text, actions = merge_decisions(_LOG_PROJECT, _LOG_OLD, amended_new)
    check("decisions: an amended index row is updated when the project's copy is unedited",
          "amended 2026-09-23" in text and ("update-row", "2026-09-20-001") in actions, str(actions))
    reworded = _LOG_NEW.replace("text\n", "text, corrected\n")
    text, actions = merge_decisions(_LOG_PROJECT, _LOG_OLD, reworded)
    check("decisions: a body the template corrected is replaced in place when unedited",
          "text, corrected" in text and ("update-body", "2026-09-20-001") in actions
          and text.count("## Decision 2026-09-20-001") == 1, str(actions))
    edited_body = _LOG_PROJECT.replace("text\n", "text, annotated by the project\n")
    text, actions = merge_decisions(edited_body, _LOG_OLD, reworded)
    check("decisions: a body the project annotated is reported and left alone",
          "annotated by the project" in text and ("body-edited", "2026-09-20-001") in actions, str(actions))
    bodies = decision_bodies(_LOG_NEW)
    check("decisions: a body ends at the next heading, without its trailing rule",
          bodies["2026-09-20-001"].endswith("text") and bodies["2026-09-22-002"].endswith("body two")
          and "[EXAMPLE]" not in bodies)

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
