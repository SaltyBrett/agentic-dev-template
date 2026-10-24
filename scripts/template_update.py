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
             2026-09-23-003 keeps the framework's decisions out of it, and the session's
             gitignored journal and working notes), `.project-profile`, the project's persona
             roster `.claude/agents/`, `.claude/settings.local.json` (one
             operator's), and the content folders the template ships empty (`docs/prd/`,
             `evidence/`, `infra/`, ...). A template change under one of these is named in one
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
             project is on), current (the project's copy) and other (the target). That
             includes `.claude/skills/`, `.claude/rules/` and `.claude/settings.json`: the
             template's, which a project may edit and extend (decision 2026-10-23-002); a
             skill or rule the project added is in neither release and never touched. And the
             persona library `personas/`, which a project activates from (decision 2026-10-23-003).
             A copy the project never edited takes the template's version outright.
             An edited copy takes the template's change where the two do not overlap.
             An overlap is a conflict: the file is left alone and named, and the run
             refuses to stamp until `--take` or `--keep` settles it. One path is the
             exception: `.gitignore`, where project and template both append at the end,
             is merged with `--union`, both sides' lines kept, the project's first, and
             the dry run names it `union` (decision 2026-10-23-007).

ADOPTION FROM v1.0.0 — judged by what the project holds, not by either release
-------------------------------------------------------------------------------
Decision 2026-10-23-005. A v1.0.0 project kept its personas in `docs/personas/` and synced
them, with one knowledge entry, from the retired `dev-resources`. Whenever the project still
holds them (`adoption_steps`):
  * every persona in `docs/personas/` is converted into an agent file in the roster
    `.claude/agents/` and the old file removed: the only write this script makes into the
    roster. A file that does not convert exactly, or a roster file already holding other text,
    is a conflict, left alone and named.
  * the sync's stamp `.resources-version` is removed; nothing reads it.
  * a knowledge entry declaring `source: dev-resources` is merged three-way like any other, the
    declaration being content; one that no release step writes loses the declaration and is
    the project's own.
The converter reads nothing from the sibling scripts: during adoption they are still the
project's v1.0.0 copies, and their persona lint knows only the old shape.

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
import importlib.util
import json
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

ROSTER = ".claude/agents/"
LIBRARY = "personas/"

# Project-owned: never written. Everything not listed here, in MERGE or in the adoption paths
# below is three-way merged.
KEEP = [
    "sprint/",
    ".project-profile",
    "docs/prd/", "docs/architecture/", "docs/executive/", "docs/research/",
    "docs/testing/", "docs/runbooks/", "evidence/", "infra/", "resources/branding/",
    # The template's hook-repository packaging, removed at birth (new_project.TEMPLATE_ONLY):
    # a project's pyproject.toml is its own, and a project is not a hook repository.
    "pyproject.toml", ".pre-commit-hooks.yaml",
    # The roster: the personas this project activated from the library or drafted itself
    # (decision 2026-10-23-003). A release ships the library in personas/ and never a roster.
    ROSTER,
    # One operator's Claude Code permissions (new_project.LOCAL_STATE): gitignored, so a release
    # should never hold it; kept in case one ever does, since it would carry personal grants.
    ".claude/settings.local.json",
    # The template's MIT license arrives at birth and is the project's from then on: a project
    # keeps it or replaces it with its own, and a release never rewrites a project's license
    # (decision 2026-09-25-002).
    "LICENSE",
]
# Adoption from v1.0.0 (decision 2026-10-23-005): what the retired dev-resources sync left in a
# project. Judged by the project's own files in adoption_steps, never by either release.
LEGACY_PERSONAS = "docs/personas/"   # the v1.0.0 registry, converted into the roster
RETIRED = [".resources-version"]     # the sync's stamp, which nothing reads any longer
KB_DIR = "docs/orchestration/knowledge/"
RESOURCE_KEY = re.compile(r"^source:\s*dev-resources\s*$")
MERGE = {
    "docs/orchestration/knowledge/INDEX.md": "index",
    "docs/governance/framework_decisions.md": "decisions",
}
SPECIAL = {VERSION_FILE}
# Merged with `git merge-file --union` where both sides changed one place: both sides' lines are
# kept, the project's first. Project and template both append at the end of this file, so a line
# merge conflicts every time; the one order that matters, a `!` line after the pattern it reverses,
# the template's exact paths never meet. Every other three-way path still conflicts (decision
# 2026-10-23-007).
UNION = {".gitignore"}

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
    if path in RETIRED or path.startswith(LEGACY_PERSONAS):
        return "adopt"
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
# Adoption from v1.0.0 — pure over the project's files (decision 2026-10-23-005)
# ==============================================================================

V1_KEYS = ["name", "slug", "description", "version"]
V1_SECTIONS = ["Expertise", "Insists on", "Invocation", "Changelog"]
V1_LISTS = {"Expertise": "expertise", "Insists on": "insists_on", "Changelog": "changelog"}
V1_LINE = re.compile(r"^([a-z_]+):\s*(.*)$")   # how v1.0.0's persona lint read the flat frontmatter
H2 = re.compile(r"^##\s+(.+?)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


class ConversionError(Exception):
    """A docs/personas/ file that would not convert without losing or changing something."""


def blank_trimmed(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


def v1_persona(stem: str, data: bytes) -> tuple[dict, str]:
    """(agent frontmatter values, Invocation) from a v1.0.0 persona, read as v1.0.0 read it: flat
    `key: value` lines, then a title and four H2 sections. Anything the agent-file shape has no
    place for is refused rather than dropped."""
    text = data.decode("utf-8").replace("\r\n", "\n")
    end = text.find("\n---\n", 3)
    if not text.startswith("---\n") or end == -1:
        raise ConversionError("no --- frontmatter block")
    keys: dict[str, str] = {}
    for line in text[4:end].splitlines():
        m = V1_LINE.match(line)
        if not m:
            if line.strip():
                raise ConversionError(f"frontmatter line {line!r} is not `key: value`")
            continue
        if m.group(1) in keys:
            raise ConversionError(f"frontmatter key `{m.group(1)}` appears twice")
        keys[m.group(1)] = m.group(2).strip()
    if set(keys) != set(V1_KEYS) or not all(keys.values()):
        raise ConversionError(f"frontmatter must hold exactly {V1_KEYS}, each non-empty; found {list(keys)}")
    if keys["slug"] != stem:
        raise ConversionError(f"`slug: {keys['slug']}` differs from the filename stem `{stem}`")
    if not re.fullmatch(r"[1-9]\d*", keys["version"]):
        raise ConversionError(f"`version: {keys['version']}` is not a positive integer")

    preamble: list[str] = []
    secs: list[tuple[str, list[str]]] = []
    fenced = False
    for line in text[end + 5:].splitlines():
        if FENCE.match(line):
            fenced = not fenced
        m = None if fenced else H2.match(line)
        if m:
            secs.append((m.group(1), []))
        else:
            (secs[-1][1] if secs else preamble).append(line)
    heads = [h for h, _ in secs]
    if heads != V1_SECTIONS:
        raise ConversionError(f"H2 headings must be exactly {V1_SECTIONS}, found {heads}")
    title = [ln for ln in preamble if ln.strip()]
    if len(title) > 1 or (title and not title[0].startswith("# ")):
        raise ConversionError("text before `## Expertise` other than the `# ` title has no place in an agent file")

    values: dict = {"name": stem, "description": keys["description"], "version": int(keys["version"])}
    invocation = ""
    for heading, lines in secs:
        lines = blank_trimmed(lines)
        if not lines:
            raise ConversionError(f"`## {heading}` is empty")
        if heading == "Invocation":
            invocation = "\n".join(lines)
            continue
        # A bullet wrapped onto the next line is one item, as Markdown reads it and as the hand
        # conversion joined the real one; a line after a blank one belongs to no bullet.
        items: list[str] = []
        joinable = False
        for ln in lines:
            s = ln.strip()
            if s.startswith("- "):
                items.append(s[2:].strip())
                joinable = True
            elif s and joinable:
                items[-1] += " " + s
            elif s:
                raise ConversionError(f"`## {heading}` holds {s!r} outside any `- ` bullet")
            else:
                joinable = False
        values[V1_LISTS[heading]] = items
    return values, invocation


def yaml_scalar(value: str, item: bool) -> str:
    """`value` plain when YAML reads it back unchanged where it sits, else double-quoted. A list item
    holding `: ` reads as a mapping unless quoted, the trap the hand conversion met (decision
    2026-10-22-005); a backtick cannot open a plain scalar; `yes` reads as a bool."""
    import yaml
    doc, want = (f"- {value}", [value]) if item else (f"k: {value}", {"k": value})
    try:
        if "\n" not in value and yaml.safe_load(doc) == want:
            return value
    except yaml.YAMLError:
        pass
    return json.dumps(value, ensure_ascii=False)   # JSON's string is YAML's double-quoted scalar


def agent_file(values: dict, invocation: str, scalar=yaml_scalar) -> bytes:
    """The agent file the library's shape prescribes, refused unless its frontmatter parses back
    to exactly `values`: Claude Code skips an agent file it cannot parse, without a word."""
    import yaml
    fm = [f"name: {scalar(values['name'], False)}", f"description: {scalar(values['description'], False)}",
          f"version: {values['version']}"]
    for key in ("expertise", "insists_on", "changelog"):
        fm += [f"{key}:"] + [f"  - {scalar(i, True)}" for i in values[key]]
    try:
        parsed = yaml.safe_load("\n".join(fm))
    except yaml.YAMLError as e:
        raise ConversionError(f"the frontmatter written would not parse: {e}") from None
    if parsed != values:
        raise ConversionError("the frontmatter written would not read back as the persona's values")
    return "\n".join(["---", *fm, "---", "", invocation, ""]).encode("utf-8")


def convert_persona(stem: str, data: bytes) -> bytes:
    return agent_file(*v1_persona(stem, data))


def frontmatter_end(lines: list[str]) -> int | None:
    """Index of the closing `---` of a frontmatter block opening on the first line, or None."""
    if not lines or lines[0].rstrip("\r\n") != "---":
        return None
    return next((i for i in range(1, len(lines)) if lines[i].rstrip("\r\n") == "---"), None)


def marked(data: bytes | None) -> bool:
    """A knowledge entry whose frontmatter declares `source: dev-resources`: synced by the retired sync."""
    lines = (data or b"").decode("utf-8", errors="replace").splitlines(keepends=True)
    end = frontmatter_end(lines)
    return end is not None and any(RESOURCE_KEY.match(ln.rstrip("\r\n")) for ln in lines[1:end])


def unmarked(data: bytes) -> bytes:
    """The entry without its `source: dev-resources` line; a mention in the body is prose and stays."""
    lines = data.decode("utf-8").splitlines(keepends=True)
    end = frontmatter_end(lines)
    if end is None:
        return data
    kept = [ln for i, ln in enumerate(lines) if not (0 < i < end and RESOURCE_KEY.match(ln.rstrip("\r\n")))]
    return "".join(kept).encode("utf-8")


def adoption_steps(files: dict[str, bytes], library: dict[str, bytes | None],
                   planned: set[str], keeps: set[str]) -> list[Step]:
    """The steps that settle what a v1.0.0 project holds from the retired sync.

    `files`: the project's tracked files under docs/personas/, the roster and the knowledge base,
    and each RETIRED path, with their bytes. `library`: slug -> the target release's library copy,
    or None. `planned`: the paths the release's own steps already settle."""
    steps: list[Step] = []
    for path in sorted(p for p in files if p.startswith(LEGACY_PERSONAS)):
        if path in keeps:
            steps.append(Step(path, "keep", notes=["kept by --keep; not converted"]))
            continue
        name = path[len(LEGACY_PERSONAS):]
        try:
            if "/" in name or not name.endswith(".md"):
                raise ConversionError("not a persona file; move it out of docs/personas/")
            stem = name[:-3]
            converted = convert_persona(stem, files[path])
        except ConversionError as e:
            steps.append(Step(path, "CONFLICT", notes=[f"cannot convert: {e}",
                              "fix it to the v1.0.0 persona shape or move it, then re-run; --keep leaves it as it is"]))
            continue
        target = ROSTER + name
        held = files.get(target)
        if held is not None and held != converted:
            steps.append(Step(path, "CONFLICT", notes=[f"{target} already holds other text; the roster is the "
                              "project's, so settle the two by hand, then re-run"]))
            continue
        lib = library.get(stem)
        where = ("the library holds the same text" if lib == converted
                 else "not in the library: the project's own" if lib is None
                 else "differs from the library copy: the suite's library rule judges it")
        if held is None:
            steps.append(Step(target, "convert", converted, notes=[f"from {path}; {where}"]))
        steps.append(Step(path, "delete", delete=True, notes=[f"converted into {target}"]))
    for path in RETIRED:
        if path in files:
            steps.append(Step(path, "keep", notes=["kept by --keep"]) if path in keeps else
                         Step(path, "retire", delete=True, notes=["the retired dev-resources sync's stamp; nothing reads it"]))
    for path in sorted(files):
        if path.startswith(KB_DIR) and path.endswith(".md") and path not in planned and marked(files[path]):
            steps.append(Step(path, "keep", notes=["kept by --keep"]) if path in keeps else
                         Step(path, "unmark", unmarked(files[path]),
                              notes=["synced from the retired dev-resources; the declaration goes and the entry is the project's own"]))
    return steps


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


def build_plan(frm: str, to: str, profile: str | None, takes: set[str], keeps: set[str]) -> tuple[list[Step], list[str]]:
    steps: list[Step] = []
    kept: list[str] = []
    for path in sorted(tree(frm) | tree(to)):
        cls = classify(path)
        if cls in ("special", "adopt"):
            continue
        base = normalized(prepared(path, blob(frm, path), profile))
        other = normalized(prepared(path, blob(to, path), profile))
        if base == other:
            continue
        step = plan_path(path, cls, current_bytes(path), base, other, takes, keeps)
        if step is not None and step.verdict == "not applied":
            kept.append(path)
        elif step is not None:
            steps.append(step)
    files = {p: b for p in tracked(LEGACY_PERSONAS, ROSTER, KB_DIR, *RETIRED) if (b := current_bytes(p)) is not None}
    library = {p[len(LEGACY_PERSONAS):-3]: normalized(prepared(p, blob(to, LIBRARY + p[len(LEGACY_PERSONAS):]), profile))
               for p in files if p.startswith(LEGACY_PERSONAS) and p.endswith(".md")}
    steps += adoption_steps(files, library, {s.path for s in steps}, keeps)
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
    if tracked(LEGACY_PERSONAS) and importlib.util.find_spec("yaml") is None:
        print(f"template_update: converting {LEGACY_PERSONAS} needs PyYAML in this python3: "
              "`python3 -m pip install pyyaml`, then re-run.", file=sys.stderr)
        return 2

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
        print(f"\n{len(conflicts)} CONFLICT(s): both the project and the template changed the same lines, "
              "or a persona would not convert.")
        for s in conflicts:
            print(f"  {s.path}: its note above" if classify(s.path) == "adopt"
                  else f"  git diff {REF_PREFIX}{frm} {REF_PREFIX}{args.to} -- {s.path}")
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
    legacy = ROOT / LEGACY_PERSONAS
    if legacy.is_dir() and not any(legacy.iterdir()):
        legacy.rmdir()
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

# A v1.0.0 persona and the agent file it converts to. Its description and two items hold `: `, one
# item opens with a backtick, one reads as a bool, one is wrapped onto a second line, and the
# Invocation holds a fenced `## ` line.
_V1 = ("---\nname: Fixture keeper\nslug: fixture-keeper\n"
       "description: Keeps the fixtures honest: every one proved against broken code\nversion: 2\n---\n\n"
       "# Fixture keeper\n\n## Expertise\n\n- Gate scripts and\n  their self-tests\n"
       "- Markdown state: index-first logs\n- `pre-commit` stages\n\n"
       "## Insists on\n\n- yes\n- A rule is a control only when a script enforces it\n\n"
       "## Invocation\n\nYou keep the fixtures honest.\n\n```\n## not a heading\n```\n\n"
       "## Changelog\n\n- 1 — 2026-09-21 — seeded\n- 2 — 2026-10-01 — reworded: tighter\n")
_AGENT = ("---\nname: fixture-keeper\n"
          "description: \"Keeps the fixtures honest: every one proved against broken code\"\nversion: 2\n"
          "expertise:\n  - Gate scripts and their self-tests\n  - \"Markdown state: index-first logs\"\n"
          "  - \"`pre-commit` stages\"\n"
          "insists_on:\n  - \"yes\"\n  - A rule is a control only when a script enforces it\n"
          "changelog:\n  - 1 — 2026-09-21 — seeded\n  - \"2 — 2026-10-01 — reworded: tighter\"\n"
          "---\n\nYou keep the fixtures honest.\n\n```\n## not a heading\n```\n")
_KB = (b"---\nname: x\nteaches: []\nverified: 2026-09-23\nsource: dev-resources\nmetadata:\n  type: reference\n---\n\n"
       b"Synced entries declare `source: dev-resources`.\nsource: dev-resources\n")
_KB_PLAIN = _KB.replace(b"verified: 2026-09-23\nsource: dev-resources\n", b"verified: 2026-09-23\n")


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

    want = {"scripts/x.py": "three-way", "AGENTS.md": "three-way", ".claude/agents/p.md": "keep",
            "docs/orchestration/knowledge/reference_x.md": "three-way", "docs/runbooks/new.md": "keep",
            "sprint/story-tracker.md": "keep", "sprint/handoffs/HANDOFF_S9.md": "keep",
            ".project-profile": "keep", "sprint/decision-log.md": "keep",
            "docs/governance/framework_decisions.md": "merge", "docs/governance/gate_suite_runbook.md": "three-way",
            "docs/orchestration/knowledge/INDEX.md": "merge", ".template-version": "special",
            "pyproject.toml": "keep", ".pre-commit-hooks.yaml": "keep", ".resources-version": "adopt",
            "docs/personas/x.md": "adopt"}
    bad = {p: classify(p) for p, w in want.items() if classify(p) != w}
    check("paths classify as keep, merge, three-way, special or adopt", not bad, str(bad))

    # Every Claude Code path the template ships, and the session's local banking, as decided by
    # decisions 2026-10-23-002 and 2026-10-23-005. `docs/personas/` is the v1.0.0 registry, which
    # adoption converts into the roster whatever either release holds there.
    decided = {".claude/agents/framework-maintainer.md": "keep", ".claude/settings.local.json": "keep",
               "personas/framework-maintainer.md": "three-way",
               ".claude/skills/closeout/SKILL.md": "three-way", ".claude/skills/new-one/notes.md": "three-way",
               ".claude/rules/gate-scripts.md": "three-way", ".claude/settings.json": "three-way",
               "sprint/recovery/journal.md": "keep", "sprint/recovery/WORKING_NOTES.md": "keep",
               "docs/personas/framework-maintainer.md": "adopt"}
    bad = {p: classify(p) for p, w in decided.items() if classify(p) != w}
    check("the Claude Code paths and the recovery files classify as decided", not bad, str(bad))

    # The writing profile merges three-way, so a development path a release adds reaches a project
    # beside its own lines; a project's custom voice is in neither release, so no step names it
    # (decisions 2026-10-24-016, 2026-10-24-017 and 2026-10-24-026).
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

    # The roster and the library are one path each, named in four places: the closeout gate reads
    # both, and the initializer, the sanitizer and this map each decide them. A rename that missed
    # one (TMPL-1.3 renamed the registry in three lists with no fixture) would leave a project
    # activating into a folder no gate reads, or a release writing over a project's roster.
    import session_closeout  # lazy: the state gate, whose PyYAML import is itself lazy
    import sanitize_template
    roster = session_closeout.PERSONAS.relative_to(session_closeout.ROOT).as_posix() + "/"
    library = session_closeout.LIBRARY.relative_to(session_closeout.ROOT).as_posix() + "/"
    check("the roster the gate reads is kept here and by the sanitizer, and cleared by the initializer at birth",
          roster == ROSTER and roster in KEEP and classify(roster + "p.md") == "keep"
          and roster in sanitize_template.NEVER_RESET and roster + "*.md" in new_project.CLEAR_GLOBS
          and roster not in new_project.NEVER_RESET,
          f"gate={roster} clear={new_project.CLEAR_GLOBS}")
    mutating = (set(new_project.FILL_FILES) | set(new_project.REGENERATE_FILES)
                | set(new_project.CLEAR_GLOBS) | set(new_project.TEMPLATE_ONLY))
    check("the library the gate reads is merged here, kept by the sanitizer, and in no list of the initializer",
          library == LIBRARY and classify(library + "p.md") == "three-way" and library in sanitize_template.NEVER_RESET
          and not any(m.startswith(library) for m in mutating | set(new_project.NEVER_RESET)),
          f"gate={library}")
    check("the initializer's local files are kept here, never carried by a release",
          all(classify(p) == "keep" for p in new_project.LOCAL_STATE),
          str({p: classify(p) for p in new_project.LOCAL_STATE}))
    merged_claude = [p for p in decided if p.startswith(".claude/") and decided[p] == "three-way"]
    check("what this map merges under .claude/ the initializer leaves as shipped",
          not any(p.startswith(m.split("*")[0]) for p in merged_claude for m in mutating),
          f"mutating={sorted(mutating)}")

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
          "base) or is the project's own (its decision log) — never by nothing",
          classify("docs/governance/framework_decisions.md") == "merge" and classify("sprint/decision-log.md") == "keep"
          and classify("docs/orchestration/knowledge/x.md") == "three-way" and set(never) <= {"merge", "keep", "three-way"},
          f"never={never}")

    # Adoption from v1.0.0 (decision 2026-10-23-005). A converter that raises is reported as a
    # failed fixture, never as a crash of the self-test.
    def attempt(text: str) -> bytes | str:
        try:
            return convert_persona("fixture-keeper", text.encode())
        except Exception as e:   # noqa: BLE001 — reported in the fixture's detail
            return f"{type(e).__name__}: {e}"

    out = attempt(_V1)
    check("convert: a v1.0.0 persona becomes the agent file, every item quoted only where YAML needs it",
          out == _AGENT.encode(), out.decode(errors="replace") if isinstance(out, bytes) else out)
    check("convert: the agent file written passes the state gate's persona lint",
          not session_closeout.lint_persona(_AGENT, "fixture-keeper"), str(session_closeout.lint_persona(_AGENT, "fixture-keeper")))
    check("convert: a CRLF checkout converts the same", attempt(_V1.replace("\n", "\r\n")) == _AGENT.encode())
    refused = {
        "slug differs from the filename": ("slug: fixture-keeper", "slug: other-keeper"),
        "a key the agent file has no place for": ("version: 2\n", "version: 2\nmodel: opus\n"),
        "a key missing": ("description: Keeps the fixtures honest: every one proved against broken code\n", ""),
        "a key twice": ("version: 2\n", "version: 2\nversion: 3\n"),
        "a version not an integer": ("version: 2\n", "version: 2.0\n"),
        "a frontmatter line not `key: value`": ("version: 2\n", "version: 2\n  - stray\n"),
        "a section renamed": ("## Insists on", "## Insists On"),
        "a section added": ("## Changelog", "## Notes\n\nlost?\n\n## Changelog"),
        "prose before the sections": ("# Fixture keeper\n", "# Fixture keeper\n\nAn introduction.\n"),
        "a line after a blank one in a list": ("- Gate scripts and\n  their self-tests\n", "- Gate scripts and\n\n  their self-tests\n"),
        "a line before any bullet": ("## Expertise\n\n", "## Expertise\n\nThese skills:\n\n"),
        "an empty Invocation": ("You keep the fixtures honest.\n\n```\n## not a heading\n```\n", ""),
        "a heading outside a fence": ("```\n## not a heading\n```", "## not a heading"),
        "no frontmatter": ("---\nname: Fixture keeper\n", "name: Fixture keeper\n"),
    }
    def refuses(fn) -> bool:
        """True only when `fn` raises ConversionError: a crash is not a refusal."""
        try:
            fn()
        except ConversionError:
            return True
        except Exception:   # noqa: BLE001 — any other exception is the converter failing, reported as such
            return False
        return False

    accepted = [label if old in _V1 else f"{label} (the fixture's text is not in _V1)"
                for label, (old, new) in refused.items()
                if old not in _V1 or not refuses(lambda: convert_persona("fixture-keeper", _V1.replace(old, new, 1).encode()))]
    check("convert: what the agent file cannot hold is refused, never dropped", not accepted, str(accepted))
    values = {"name": "fixture-keeper", "description": "d: e", "version": 1, "expertise": ["a: b"],
              "insists_on": ["yes"], "changelog": ["1 — 2026-09-21 — seeded"]}
    check("convert: frontmatter that would not parse, or would read back otherwise, is refused",
          refuses(lambda: agent_file(values, "p", scalar=lambda v, item: v))
          and refuses(lambda: agent_file(values, "p", scalar=lambda v, item: v if v == "yes" else yaml_scalar(v, item))))

    check("a knowledge entry declaring source: dev-resources in its frontmatter is marked; in the body, "
          "or with no frontmatter, it is not",
          marked(_KB) and marked(_KB.replace(b"\n", b"\r\n")) and not marked(_KB_PLAIN)
          and not marked(b"no frontmatter\nsource: dev-resources\n") and not marked(None))
    check("unmarking removes the frontmatter line alone; the body's mention stays",
          unmarked(_KB) == _KB_PLAIN and _KB_PLAIN.count(b"source: dev-resources") == 2, unmarked(_KB).decode())
    step = plan_path(KB_DIR + "reference_m.md", "three-way", _KB, _KB, _KB_PLAIN + b"amended\n", set(), set())
    check("a synced entry the template now ships takes the template's copy: the declaration is content, "
          "merged like any other line",
          step is not None and (step.verdict, step.write) == ("update", _KB_PLAIN + b"amended\n"), str(step))
    step = plan_path(ROSTER + "p.md", "keep", b"mine", b"a", b"b", set(), set())
    check("a template change under a project-owned path is not applied",
          step is not None and step.verdict == "not applied" and step.write is None, str(step))

    legacy, own, roster_copy = LEGACY_PERSONAS + "fixture-keeper.md", LEGACY_PERSONAS + "own.md", ROSTER + "fixture-keeper.md"
    files = {legacy: _V1.encode(), own: _V1.replace("fixture-keeper", "own").encode(), ".resources-version": b"main abc\n",
             KB_DIR + "reference_m.md": _KB, KB_DIR + "reference_t.md": _KB, KB_DIR + "reference_p.md": _KB_PLAIN}
    steps = adoption_steps(files, {"fixture-keeper": _AGENT.encode(), "own": None}, {KB_DIR + "reference_t.md"}, set())
    got = {(s.path, s.verdict) for s in steps}
    by = {s.path: s for s in steps}
    blank = Step("", "")

    def note(path: str) -> str:
        return " ".join(by.get(path, blank).notes)

    check("adopt: each persona converts into the roster and its old file goes; the stamp is retired; a marked "
          "entry no release step writes is unmarked; a planned or plain one is left",
          got == {(roster_copy, "convert"), (legacy, "delete"), (ROSTER + "own.md", "convert"), (own, "delete"),
                  (".resources-version", "retire"), (KB_DIR + "reference_m.md", "unmark")}
          and by[roster_copy].write == _AGENT.encode() and by[legacy].delete and by[".resources-version"].delete
          and by[KB_DIR + "reference_m.md"].write == _KB_PLAIN, str(sorted(got)))
    check("adopt: the note says whether the library holds the same text or the persona is the project's own",
          "same text" in note(roster_copy) and "project's own" in note(ROSTER + "own.md"),
          f"{note(roster_copy)} | {note(ROSTER + 'own.md')}")
    steps = adoption_steps({legacy: _V1.encode()}, {"fixture-keeper": b"other text"}, set(), set())
    check("adopt: a persona whose library copy differs is converted and named for the suite to judge",
          "differs" in steps[0].notes[0], str(steps[0].notes))
    steps = adoption_steps({legacy: _V1.encode(), roster_copy: _AGENT.encode()}, {}, set(), set())
    check("adopt: a roster already holding the converted text is not written again; the old file goes",
          [(s.path, s.verdict) for s in steps] == [(legacy, "delete")], str([(s.path, s.verdict) for s in steps]))
    steps = adoption_steps({legacy: _V1.encode(), roster_copy: b"the project's own text\n"}, {}, set(), set())
    check("adopt: a roster holding other text is a conflict: nothing written, nothing deleted",
          [(s.path, s.verdict, s.write, s.delete) for s in steps] == [(legacy, "CONFLICT", None, False)],
          str([(s.path, s.verdict) for s in steps]))
    files = {LEGACY_PERSONAS + "bad.md": b"no frontmatter\n", LEGACY_PERSONAS + "notes.txt": b"x\n",
             LEGACY_PERSONAS + "sub/x.md": _V1.encode(), ".resources-version": b"main abc\n", KB_DIR + "reference_m.md": _KB}
    steps = adoption_steps(files, {}, set(), set())
    check("adopt: a file that is no v1.0.0 persona is a conflict, left in place",
          {(s.path, s.verdict) for s in steps if s.path.startswith(LEGACY_PERSONAS)}
          == {(p, "CONFLICT") for p in files if p.startswith(LEGACY_PERSONAS)} and not any(s.delete for s in steps
          if s.path.startswith(LEGACY_PERSONAS)), str([(s.path, s.verdict) for s in steps]))
    steps = adoption_steps(files, {}, set(), set(files))
    check("adopt: --keep leaves a persona unconverted, the stamp and a marked entry as they are",
          {s.verdict for s in steps} == {"keep"} and not any(s.write or s.delete for s in steps),
          str([(s.path, s.verdict) for s in steps]))

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

    # .gitignore by union (decision 2026-10-23-007): the shape of every real adoption so far.
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
