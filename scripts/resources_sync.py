#!/usr/bin/env python3
"""
resources_sync.py — the persona registry and the resource knowledge entries are a cache of
`dev-resources`, refreshed by this script and grown only through it.

THE FAILURE THIS CLOSES
-----------------------
A persona written in one project stayed there. The template carried its registry to every project
at birth and at every release, and nothing travelled the other way, so each clone was only as good
as the registry it started with (decision 2026-09-23-002). The same held for reference knowledge
that belongs to no one project.

WHAT IT DOES
------------
Fetches `--source` at `--ref` into refs/resources/<ref> (outside refs/tags/, invisible to the
version gate), judges every owned path against that tree, writes what is behind, reports what is
ahead or unpublished, merges the INDEX rows the fetched tree carries, and stamps
.resources-version last — withheld on a conflict.

Owned paths: every docs/personas/*.md, and every docs/orchestration/knowledge/*.md whose
frontmatter declares `source: dev-resources`. Everything under that path in the fetched tree must
carry the declaration; an entry without it is refused (`unmarked`), because the declaration is how
the template updater knows to leave the file alone (template_update.resource_owned).

Verdicts, local copy against the fetched copy:
  add          fetched only                          written
  update       both, fetched at a higher version     written
  up-to-date   identical                             nothing
  ahead        both, local at a higher version       kept; --publish writes it to the clone
  unpublished  local only                            kept; --publish writes it to the clone
  CONFLICT     both differ and no version decides    kept, stamp withheld; --take <path> takes the
                                                     fetched copy, --publish sends the local one

--publish <clone> names a local checkout of dev-resources; with --apply, every ahead, unpublished
or conflicting file is written there for you to commit and push. That clone's own gates judge it
(the persona linter it consumes from this template), which is how the registry stays append-only
at its source. The session closeout refuses a persona this project holds that the fetched ref
lacks, so the sync runs at closeout, before the scaffold, never at cold start.

Usage:
    python3 scripts/resources_sync.py [--source <url>] [--ref main]             # dry run
    python3 scripts/resources_sync.py --apply
    python3 scripts/resources_sync.py --apply --publish ~/code/personal/dev-resources
    python3 scripts/resources_sync.py --self-test
Exit 0 = clean, 1 = a conflict, an unmarked entry or a refused run, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import template_update  # noqa: E402 — resource_owned and merge_index: one ownership rule, one INDEX merge

ROOT = Path(__file__).resolve().parents[1]

# ==============================================================================
# CUSTOMIZE FOR YOUR PROJECT — the repository personas and resource entries are synced from.
# Plain github.com; a machine that separates identities rewrites it to its host alias inside
# the directory its includeIf covers (reference_derived_project_start, reference_published_hooks).
# ==============================================================================
DEFAULT_SOURCE = "git@github.com:SaltyBrett/dev-resources.git"
DEFAULT_REF = "main"

REF_PREFIX = "refs/resources/"
STAMP = ".resources-version"
PERSONAS = "docs/personas/"
KB = "docs/orchestration/knowledge/"
INDEX = KB + "INDEX.md"
VERSION_KEY = re.compile(r"^version:\s*([1-9]\d*)\s*$", re.M)

WRITES = ("add", "update", "take")
PUBLISHES = ("ahead", "unpublished", "CONFLICT")
BLOCKS = ("CONFLICT", "unmarked")


# ==============================================================================
# Pure decisions — no git, no files, so the self-test covers them directly
# ==============================================================================

def frontmatter(data: bytes | None) -> str:
    if not data or not data.startswith(b"---"):
        return ""
    text = data.decode("utf-8", errors="replace")
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def version_of(data: bytes | None) -> int | None:
    m = VERSION_KEY.search(frontmatter(data))
    return int(m.group(1)) if m else None


def owned(path: str, local: bytes | None, fetched: bytes | None) -> bool:
    """Every persona; a knowledge entry that is a resource on either side. INDEX.md is merged."""
    if not path.endswith(".md") or path == INDEX:
        return False
    if path.startswith(PERSONAS):
        return True
    return path.startswith(KB) and (fetched is not None or template_update.resource_owned(local))


def verdict(local: bytes | None, fetched: bytes | None) -> str:
    if fetched is None:
        return "unpublished"
    if local is None:
        return "add"
    if local == fetched:
        return "up-to-date"
    lv, fv = version_of(local), version_of(fetched)
    if lv is not None and fv is not None and lv != fv:
        return "ahead" if lv > fv else "update"
    return "CONFLICT"


def judge(path: str, local: bytes | None, fetched: bytes | None, takes: set[str]) -> str:
    """The verdict for one owned path, including the two rules that sit above `verdict`."""
    if path.startswith(KB) and fetched is not None and not template_update.resource_owned(fetched):
        return "unmarked"
    if path in takes and fetched is not None:
        return "take"
    return verdict(local, fetched)


def parse_stamp(text: str | None) -> tuple[str, str] | None:
    """`<ref> <sha>` or None. The ref is what the closeout looks the registry up against."""
    parts = (text or "").split()
    return (parts[0], parts[1]) if len(parts) == 2 else None


# ==============================================================================
# Git and files
# ==============================================================================

@dataclass
class Step:
    path: str
    verdict: str
    write: bytes | None = None
    notes: list[str] = field(default_factory=list)


def git(*args: str, binary: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False, text=not binary)


def fetch(source: str, ref: str) -> str | None:
    r = git("fetch", "--no-tags", "--quiet", source, f"+{ref}:{REF_PREFIX}{ref}")
    return None if r.returncode == 0 else r.stderr.strip()


def ref_sha(ref: str) -> str:
    return git("rev-parse", f"{REF_PREFIX}{ref}").stdout.strip()


def tree(ref: str) -> set[str]:
    r = git("ls-tree", "-r", "--name-only", "-z", f"{REF_PREFIX}{ref}")
    if r.returncode:
        raise RuntimeError(f"cannot read {REF_PREFIX}{ref}: {r.stderr.strip()}")
    return {p for p in r.stdout.split("\0") if p}


def blob(ref: str, path: str) -> bytes | None:
    r = git("cat-file", "blob", f"{REF_PREFIX}{ref}:{path}", binary=True)
    return r.stdout if r.returncode == 0 else None


def local_bytes(path: str) -> bytes | None:
    p = ROOT / path
    return p.read_bytes() if p.is_file() else None


def local_paths() -> set[str]:
    out: set[str] = set()
    for d in (PERSONAS, KB):
        if (ROOT / d).is_dir():
            out.update(p.relative_to(ROOT).as_posix() for p in (ROOT / d).glob("*.md"))
    return out


def build_plan(ref: str, takes: set[str]) -> tuple[list[Step], Step | None]:
    fetched_paths = {p for p in tree(ref) if p.startswith((PERSONAS, KB))}
    steps: list[Step] = []
    for path in sorted(fetched_paths | local_paths()):
        local, fetched = local_bytes(path), blob(ref, path)
        if not owned(path, local, fetched):
            continue
        v = judge(path, local, fetched, takes)
        step = Step(path, v, fetched if v in WRITES else None)
        if v == "unmarked":
            step.notes.append("the fetched entry declares no `source: dev-resources`; add it there, or the "
                              "template updater would treat the synced copy as its own")
        steps.append(step)

    index_step: Step | None = None
    fetched_index, current_index = blob(ref, INDEX), local_bytes(INDEX)
    if fetched_index is not None and current_index is not None:
        text, actions = template_update.merge_index(current_index.decode("utf-8"), None, fetched_index.decode("utf-8"))
        if text != current_index.decode("utf-8"):
            index_step = Step(INDEX, "merge", text.encode("utf-8"), [f"{kind} {key}" for kind, key in actions])
    elif fetched_index is None and any(s.verdict == "add" and s.path.startswith(KB) for s in steps):
        index_step = Step(INDEX, "by-hand", notes=["the fetched tree carries no INDEX.md; add a row per new entry "
                                                   "or the frontmatter gate refuses the commit"])
    return steps, index_step


# ==============================================================================
# Main
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(description="Sync the persona registry and resource entries from dev-resources")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help=f"dev-resources: a URL or a local path (default {DEFAULT_SOURCE})")
    parser.add_argument("--ref", default=DEFAULT_REF, help=f"branch or tag to sync (default {DEFAULT_REF})")
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry run)")
    parser.add_argument("--publish", metavar="CLONE", help="A local checkout of dev-resources to write unpublished and ahead files into")
    parser.add_argument("--take", action="append", default=[], metavar="PATH", help="Resolve a conflict by taking the fetched copy")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    clone = Path(args.publish).expanduser() if args.publish else None
    if clone is not None and not (clone / ".git").exists():
        print(f"resources_sync: --publish {clone} is not a git checkout", file=sys.stderr)
        return 2

    err = fetch(args.source, args.ref)
    if err:
        print(f"resources_sync: cannot fetch {args.ref} from {args.source}:\n    {err}", file=sys.stderr)
        return 2
    sha = ref_sha(args.ref)
    steps, index_step = build_plan(args.ref, set(args.take))

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"\nResources Sync — {mode}")
    print("=" * 60)
    print(f"Source: {args.source} @ {args.ref} ({sha[:12]})")
    for s in steps + ([index_step] if index_step else []):
        print(f"  {s.verdict:<12}{s.path}")
        for n in s.notes:
            print(f"                {n}")
    to_publish = [s for s in steps if s.verdict in PUBLISHES]
    blocked = [s for s in steps if s.verdict in BLOCKS] + ([index_step] if index_step and index_step.verdict == "by-hand" else [])
    if to_publish:
        where = f"into {clone}" if clone else "with --publish <clone of dev-resources>"
        print(f"  publish     {len(to_publish)} file(s) {where}, then commit and push there")
    if not steps and not index_step:
        print("  nothing owned on either side")

    if not args.apply:
        print(f"\nDRY RUN — nothing written. Re-run with --apply{' --publish <clone>' if to_publish and not clone else ''}.")
        return 1 if blocked else 0

    for s in steps + ([index_step] if index_step and index_step.write is not None else []):
        if s.write is not None:
            p = ROOT / s.path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(s.write)
    if clone is not None:
        for s in to_publish:
            data = local_bytes(s.path)
            if data is not None:
                p = clone / s.path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
                print(f"  published   {s.path} -> {clone}")
        if to_publish:
            print(f"\nCommit and push in {clone}; its gates judge what arrived. Then re-run the sync here.")
    if blocked:
        print(f"\nBLOCKED: {len(blocked)} path(s) need a decision; the stamp is withheld. "
              "Take the fetched copy with --take <path>, or publish yours and re-run.")
        return 1
    if to_publish:
        print("\nWritten. The stamp is withheld until what is ahead or unpublished here is published and synced back.")
        return 1
    (ROOT / STAMP).write_text(f"{args.ref} {sha}\n", encoding="utf-8")
    print(f"\nPASSED: in step with {args.source} @ {args.ref}. {STAMP} reads `{args.ref} {sha[:12]}`.")
    return 0


# ==============================================================================
# SELF-TEST — pure fixtures; every verdict has a case
# ==============================================================================

_P1 = b"---\nname: A\nslug: a\ndescription: d\nversion: 1\n---\n\n# A\n\n## Invocation\n\nv1\n"
_P2 = _P1.replace(b"version: 1", b"version: 2").replace(b"v1\n", b"v2\n")
_P1_EDITED = _P1.replace(b"v1\n", b"v1 edited\n")
_R = b"---\nname: R\ndescription: r\nteaches: []\nverified: 2026-09-23\nsource: dev-resources\nmetadata:\n  type: reference\n---\n\ntext\n"
_R_EDITED = _R.replace(b"text\n", b"other text\n")
_K = _R.replace(b"source: dev-resources\n", b"")


def run_self_test() -> int:
    print("\nResources Sync Self-Test")
    print("=" * 60)
    failures = total = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    check("the version is read from the frontmatter, and only a positive integer",
          version_of(_P2) == 2 and version_of(_R) is None and version_of(_P1.replace(b"version: 1", b"version: 0")) is None)
    check("a persona is owned on either side", owned(PERSONAS + "a.md", _P1, None) and owned(PERSONAS + "a.md", None, _P1))
    check("a knowledge entry is owned when marked locally or present in the fetched tree",
          owned(KB + "r.md", _R, None) and owned(KB + "r.md", None, _R) and not owned(KB + "k.md", _K, None))
    check("INDEX.md and non-markdown are never owned", not owned(INDEX, _R, _R) and not owned(PERSONAS + "x.png", b"", b""))
    check("verdict: fetched only is add", verdict(None, _P1) == "add")
    check("verdict: local only is unpublished", verdict(_P1, None) == "unpublished")
    check("verdict: identical is up-to-date", verdict(_P1, _P1) == "up-to-date")
    check("verdict: a higher fetched version is update", verdict(_P1, _P2) == "update")
    check("verdict: a higher local version is ahead", verdict(_P2, _P1) == "ahead")
    check("verdict: same version, different text is a conflict — never a silent pick", verdict(_P1_EDITED, _P1) == "CONFLICT")
    check("verdict: an edited entry with no version is a conflict", verdict(_R_EDITED, _R) == "CONFLICT")
    check("judge: a fetched entry without the source declaration is refused as unmarked",
          judge(KB + "k.md", None, _K, set()) == "unmarked" and judge(KB + "r.md", None, _R, set()) == "add")
    check("judge: --take resolves a conflict by taking the fetched copy",
          judge(KB + "r.md", _R_EDITED, _R, {KB + "r.md"}) == "take" and judge(KB + "r.md", _R_EDITED, _R, set()) == "CONFLICT")
    check("judge: --take of a path the fetched tree lacks changes nothing", judge(PERSONAS + "a.md", _P1, None, {PERSONAS + "a.md"}) == "unpublished")
    check("the stamp is `<ref> <sha>` and anything else is unreadable",
          parse_stamp("main abc123\n") == ("main", "abc123") and parse_stamp("v1") is None and parse_stamp(None) is None)
    check("verdicts that write, publish and block are disjoint where they must be",
          not set(WRITES) & set(PUBLISHES) and "CONFLICT" in PUBLISHES and "CONFLICT" in BLOCKS and "unmarked" not in PUBLISHES)
    check("the ownership rule is the updater's, not a second copy",
          template_update.resource_owned(_R) and not template_update.resource_owned(_K))

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
