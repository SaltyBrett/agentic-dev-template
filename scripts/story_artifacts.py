#!/usr/bin/env python3
"""
story_artifacts.py — the agentic team's handoffs, judged: every story's artifacts in
docs/stories/<ID>/ held to docs/standards/team_standard_v1.0.md.

WHAT IT DOES
------------
The role map (§3) and the trigger list (§4) are read from the team standard itself, so a project
that extends them is judged by its own copy; a standard that cannot be read stops the gate, never
reads as nothing to check. For each folder under docs/stories/:
  story        the folder names a story the tracker holds, and each artifact's `story:` is it
  type         `brief.md` exists and names one of the role map's types
  frontmatter  each stage file's frontmatter parses with `story`, `stage` (its file's), `role`,
               `input`, `status` (pass, fail, needs-operator), `triggers` (a list), and the `model`
               and `effort` the role ran at, a model the ceiling's ranking places and one of its
               efforts
  stage        each file is a stage the type has (or `approvals.md`), security joining on its triggers
  order        every required earlier stage is present, and each input is the stage just before
  input-status the input a role started from has status pass
  age          each stage was last changed after its input was, read from git history: the commit
               that last changed it holds its input's last change and is not that commit, a file
               differing from HEAD belonging to the commit being made
  role        the role is one the map allows at that stage and the project's roster holds
  builder      the verifier and the reviewer are not the builder
  criteria     the brief numbers its acceptance criteria, and a passing verify checks each one
  commits      each commit the build lists exists
  trigger      each trigger named is in §4; once the story releases or is Done, each trigger hit
               (declared, or a build commit touching a stack profile trigger path, or the release
               itself) has an approval row with the Chair's words
  security     a story hitting an auth or crypto change or an external service passes a security
               stage before its release
  finding      once a story moves past its review or security stage, each finding there is answered
               in docs/code_review_log.md
  release      a release names its CI `run:`
  done         a story the tracker marks Done has its last stage present and passing

--self-test   in-memory fixtures for every rule; this gate's own functions held to the coding
              standard's production limits
Exit 0 clean (or no docs/stories/), 1 a violation, 2 cannot run (the standard unreadable, git failing,
a shallow clone, whose cut history would date every older stage to its boundary commit).

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It cannot judge whether a design is good or a check the right one; those are the roles' and the
Chair's. It runs no role: the `/story` skill does.
"""
from __future__ import annotations

import contextlib
import io
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import code_standard  # noqa: E402  — the review log's reader and the trigger paths are its
import session_closeout  # noqa: E402  — the tracker's one parse
import subagent_ceiling  # noqa: E402  — the ranking a recorded model and effort are read against

ROOT = code_standard.ROOT
STORIES = "docs/stories"
STANDARD = "docs/standards/team_standard_v1.0.md"
STAGES = ("brief", "design", "build", "verify", "review", "security", "docs", "release")
STATUSES = ("pass", "fail", "needs-operator")
OPTIONAL = {("game", "review"), ("media", "release")}
SECURITY_TRIGGERS = {"an auth or crypto change", "an external service"}
RELEASE_TRIGGER = "a deploy or release"
APPROVAL_COLUMNS = ["Trigger", "What was approved", "Chair's words", "Date"]

FIXES = {
    "story": "Name the folder for a story in sprint/story-tracker.md, and set each artifact's `story:` to it.",
    "type": "Write brief.md first, with `type:` one of the team standard's story types (§3).",
    "frontmatter": "Open the file with the frontmatter of the team standard §2.",
    "stage": "Keep only the stages the story's type has (§3), and approvals.md.",
    "order": "Write the stages in order, each `input:` the stage just before it.",
    "input-status": "A role starts only from an input that passed: fix the earlier stage first.",
    "age": "Remove every stage after a changed artifact in the commit that changes it, then run each again, "
           "committing each stage alone after its input.",
    "role": "Use a role the map allows at this stage, activated in .claude/agents/ by the team-selection skill.",
    "builder": "Give verify and review to a role other than the build's.",
    "criteria": "Number the brief's acceptance criteria, and check each in verify's `## Checks` table.",
    "commits": "List only commits this repository holds in build.md's `commits:`.",
    "trigger": "Ask the Chair, and record the approval in approvals.md before the release or Done.",
    "security": "Run the security stage before the release: the story hit an auth, crypto or external-service trigger.",
    "finding": "Log each finding in docs/code_review_log.md with the Chair's response before the story moves on.",
    "release": "Name the CI run observed green as `run:` in release.md.",
    "done": "Finish the story's last stage, passing, before the tracker marks it Done.",
}


class LawError(Exception):
    """The team standard cannot be read, or git fails: the gate cannot run. Exit 2."""


@dataclass(frozen=True)
class Violation:
    rule: str
    where: str
    detail: str


@dataclass(frozen=True)
class Artifact:
    stage: str
    meta: dict
    body: str


@dataclass
class Context:
    role_map: dict[str, dict[str, list[str]]]
    triggers: list[str]
    roster: set[str]
    stories: dict[str, str]                       # story ID -> its tracker Status
    log_rows: list
    commit_paths: Callable[[str], list[str] | None]
    last_change: Callable[[str], str | None]      # `<ID>/<file>` -> its last commit, None: the commit being made
    contains: Callable[[str, str], bool]          # (a, b): commit a is in commit b's history


# ==============================================================================
# The law, read from the team standard
# ==============================================================================

def _section(text: str, heading: str) -> str:
    if heading not in text:
        raise LawError(f"{STANDARD} has no `{heading}` section")
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def read_role_map(text: str) -> dict[str, dict[str, list[str]]]:
    """§3's table: {type: {stage: [roles]}}, a stage the type lacks absent."""
    rows = [r for r in _section(text, "## 3. Story types and the role map").splitlines() if r.startswith("|")]
    if len(rows) < 3:
        raise LawError(f"{STANDARD} §3 holds no role map")
    header = [c.strip() for c in rows[0].strip("|").split("|")]
    if header != ["Type", *STAGES]:
        raise LawError(f"{STANDARD} §3's columns must be: Type, {', '.join(STAGES)}")
    out: dict[str, dict[str, list[str]]] = {}
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip("|").split("|")]
        out[cells[0]] = {stage: re.findall(r"`([a-z0-9-]+)`", cell) for stage, cell in zip(STAGES, cells[1:])
                         if re.findall(r"`([a-z0-9-]+)`", cell)}
    return out


def read_triggers(text: str) -> list[str]:
    """§4's first list: the triggers by name, a project's additions among them."""
    names, started = [], False
    for line in _section(text, "## 4. Review triggers").splitlines():
        if line.startswith("- "):
            names.append(line[2:].strip())
            started = True
        elif started and line.strip():
            break
    if not names:
        raise LawError(f"{STANDARD} §4 lists no trigger")
    return names


# ==============================================================================
# Reading a story's files
# ==============================================================================

def parse_artifact(stage: str, text: str) -> tuple[Artifact | None, str | None]:
    import yaml
    if not text.startswith("---\n") or "\n---" not in text[4:]:
        return None, "has no frontmatter"
    head, body = text[4:].split("\n---", 1)
    try:
        meta = yaml.safe_load(head)
    except yaml.YAMLError as e:
        return None, f"frontmatter does not parse: {e}"
    if not isinstance(meta, dict):
        return None, "frontmatter is not a mapping"
    missing = [k for k in ("story", "stage", "role", "input", "status", "model", "effort") if not isinstance(meta.get(k), str)]
    if missing or not isinstance(meta.get("triggers"), list):
        return None, f"frontmatter wants {', '.join(missing + ([] if isinstance(meta.get('triggers'), list) else ['triggers']))}"
    if meta["stage"] != stage or meta["status"] not in STATUSES:
        return None, f"`stage:` must be {stage} and `status:` one of {', '.join(STATUSES)}"
    if subagent_ceiling.family(meta["model"]) is None or meta["effort"] not in subagent_ceiling.EFFORTS:
        return None, (f"`model:` must be one the ranking places ({', '.join(subagent_ceiling.MODELS)}) and "
                      f"`effort:` one of {', '.join(subagent_ceiling.EFFORTS)}")
    return Artifact(stage, meta, body), None


def table_rows(body: str, heading: str) -> list[list[str]]:
    """The rows of the table under `heading`, its header and separator dropped."""
    if heading not in body:
        return []
    rows = [l for l in body.split(heading, 1)[1].split("\n## ", 1)[0].splitlines() if l.startswith("|")]
    return [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]


def criteria(brief: Artifact) -> list[int]:
    section = brief.body.split("## Acceptance criteria", 1)[-1].split("\n## ", 1)[0] if "## Acceptance criteria" in brief.body else ""
    return [int(m) for m in re.findall(r"^\s*(\d+)\.\s+\S", section, re.M)]


def approvals(text: str | None) -> set[str]:
    if not text:
        return set()
    rows = [l for l in text.splitlines() if l.startswith("|")]
    if not rows or [c.strip() for c in rows[0].strip("|").split("|")] != APPROVAL_COLUMNS:
        return set()
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]
    return {c[0] for c in cells if len(c) == 4 and c[2].lower() not in code_standard.NO_RESPONSE}


# ==============================================================================
# Judging one story
# ==============================================================================

def stages_of(kind: str, ctx: Context, present: set[str]) -> list[str]:
    """The type's stages in order, security among them where the story has one."""
    have = ctx.role_map[kind]
    return [s for s in STAGES if s in have or (s == "security" and s in present)]


def judge_order(sid: str, kind: str, arts: dict[str, Artifact], ctx: Context) -> list[Violation]:
    seq = stages_of(kind, ctx, set(arts))
    v = []
    for i, stage in enumerate(seq):
        if stage not in arts:
            continue
        missing = [s for s in seq[:i] if s not in arts and (kind, s) not in OPTIONAL]
        before = [s for s in seq[:i] if s in arts]
        expected = f"{before[-1]}.md" if before else "none"
        if missing:
            v.append(Violation("order", f"{sid}/{stage}.md", f"written before {', '.join(missing)}"))
        elif arts[stage].meta["input"] != expected:
            v.append(Violation("order", f"{sid}/{stage}.md", f"input {arts[stage].meta['input']!r}, not {expected!r}"))
        elif before and arts[before[-1]].meta["status"] != "pass":
            v.append(Violation("input-status", f"{sid}/{stage}.md", f"started from {expected}, whose status is "
                                                                    f"{arts[before[-1]].meta['status']}"))
    return v


def later(stage: str | None, source: str | None, contains: Callable[[str, str], bool]) -> bool:
    """Whether a stage's last change came after its input's; None is the commit being made."""
    if source is None:
        return False          # the input changes in this commit: nothing beside or before it is newer
    return stage is None or (stage != source and contains(source, stage))


def judge_age(sid: str, arts: dict[str, Artifact], ctx: Context) -> list[Violation]:
    """A stage vouches for its input as it was: one older than its input's last change is stale."""
    v = []
    for stage, art in arts.items():
        source = art.meta["input"].removesuffix(".md")
        if source in arts and not later(ctx.last_change(f"{sid}/{stage}.md"), ctx.last_change(f"{sid}/{source}.md"),
                                        ctx.contains):
            v.append(Violation("age", f"{sid}/{stage}.md", f"was not changed after {source}.md's last change, "
                                                           f"so it vouches for an older {source}"))
    return v


def judge_roles(sid: str, kind: str, arts: dict[str, Artifact], ctx: Context) -> list[Violation]:
    v = []
    for stage, art in arts.items():
        allowed = ctx.role_map[kind].get(stage, ["security-engineer"] if stage == "security" else [])
        role = art.meta["role"]
        if role not in allowed:
            v.append(Violation("role", f"{sid}/{stage}.md", f"{role} is not a {kind} {stage} role ({', '.join(allowed)})"))
        elif role not in ctx.roster:
            v.append(Violation("role", f"{sid}/{stage}.md", f"{role} is not in the roster"))
    builder = arts.get("build")
    for stage in ("verify", "review"):
        if builder and stage in arts and arts[stage].meta["role"] == builder.meta["role"]:
            v.append(Violation("builder", f"{sid}/{stage}.md", f"{builder.meta['role']} built it and cannot {stage} it"))
    return v


def judge_criteria(sid: str, arts: dict[str, Artifact]) -> list[Violation]:
    numbers = criteria(arts["brief"])
    if not numbers:
        return [Violation("criteria", f"{sid}/brief.md", "names no numbered acceptance criteria")]
    verify = arts.get("verify")
    if not verify or verify.meta["status"] != "pass":
        return []
    passed = {int(r[0]) for r in table_rows(verify.body, "## Checks") if len(r) >= 3 and r[0].isdigit()
              and r[2].lower() == "pass"}
    unchecked = [n for n in numbers if n not in passed]
    return [Violation("criteria", f"{sid}/verify.md", f"passes with criteria {unchecked} not checked and passing")] if unchecked else []


def hit_triggers(sid: str, arts: dict[str, Artifact], ctx: Context) -> tuple[set[str], list[Violation]]:
    hit: set[str] = set()
    v = []
    for art in arts.values():
        for name in art.meta["triggers"]:
            hit.add(name)
            if name not in ctx.triggers:
                v.append(Violation("trigger", f"{sid}/{art.stage}.md", f"{name!r} is no trigger of §4"))
    for sha in (arts["build"].meta.get("commits") or []) if "build" in arts else []:
        paths = ctx.commit_paths(str(sha))
        if paths is None:
            v.append(Violation("commits", f"{sid}/build.md", f"commit {sha} is not in this repository"))
            continue
        hit |= {name for name, globs in code_standard.TRIGGER_PATHS.items() if any(code_standard.matches(p, globs) for p in paths)}
    if "release" in arts:
        hit.add(RELEASE_TRIGGER)
    return hit, v


def judge_triggers(sid: str, arts: dict[str, Artifact], ctx: Context, approved: set[str]) -> list[Violation]:
    hit, v = hit_triggers(sid, arts, ctx)
    closing = "release" in arts or ctx.stories.get(sid) == "Done"
    if closing:
        v += [Violation("trigger", f"{sid}/approvals.md", f"{name!r} was hit and the Chair has not approved it")
              for name in sorted(hit - approved)]
    if "release" in arts and hit & SECURITY_TRIGGERS and arts.get("security", None) is None:
        v.append(Violation("security", f"{sid}/release.md", f"released past {sorted(hit & SECURITY_TRIGGERS)} with no security stage"))
    return v


def judge_findings(sid: str, kind: str, arts: dict[str, Artifact], ctx: Context) -> list[Violation]:
    seq = stages_of(kind, ctx, set(arts))
    v = []
    for stage in ("review", "security"):
        later = [s for s in seq[seq.index(stage) + 1:] if s in arts] if stage in seq else []
        if stage not in arts or not (later or ctx.stories.get(sid) == "Done"):
            continue
        for row in table_rows(arts[stage].body, "## Findings"):
            m = re.match(r"`?([a-z_-]+)`?\s+(\d+)", row[1]) if len(row) >= 2 else None
            finding = code_standard.Finding(m.group(1), row[0].strip("` "), int(m.group(2)), "") if m else None
            if finding is None or not code_standard.logged(finding, ctx.log_rows):
                v.append(Violation("finding", f"{sid}/{stage}.md", f"{row[:2]} has no answer from the Chair in the log"))
    return v


def judge_close(sid: str, kind: str, arts: dict[str, Artifact], ctx: Context) -> list[Violation]:
    v = []
    if "release" in arts and not arts["release"].meta.get("run"):
        v.append(Violation("release", f"{sid}/release.md", "names no CI `run:`"))
    if ctx.stories.get(sid) == "Done":
        last = [s for s in stages_of(kind, ctx, set(arts)) if (kind, s) not in OPTIONAL][-1]
        if last not in arts or arts[last].meta["status"] != "pass":
            v.append(Violation("done", sid, f"the tracker marks it Done and its {last} stage is not passing"))
    return v


def read_story(sid: str, files: dict[str, str], ctx: Context) -> tuple[str | None, dict[str, Artifact], list[Violation]]:
    """(the story's type, its parsed artifacts, what stopped the reading)."""
    v = [] if sid in ctx.stories else [Violation("story", sid, "no story in the tracker has this ID")]
    arts: dict[str, Artifact] = {}
    for name, text in sorted(files.items()):
        stage = name.removesuffix(".md")
        if name == "approvals.md":
            continue
        if stage not in STAGES:
            v.append(Violation("stage", f"{sid}/{name}", "is no stage of the team standard"))
            continue
        art, problem = parse_artifact(stage, text)
        if problem:
            v.append(Violation("frontmatter", f"{sid}/{name}", problem))
        elif art.meta["story"] != sid:
            v.append(Violation("story", f"{sid}/{name}", f"names story {art.meta['story']}"))
        else:
            arts[stage] = art
    kind = arts["brief"].meta.get("type") if "brief" in arts else None
    if kind not in ctx.role_map:
        v.append(Violation("type", f"{sid}/brief.md", f"type {kind!r} is not one of {', '.join(ctx.role_map)}"))
        return None, arts, v
    v += [Violation("stage", f"{sid}/{s}.md", f"a {kind} story has no {s} stage") for s in arts
          if s not in ctx.role_map[kind] and s != "security"]
    return kind, arts, v


def judge_story(sid: str, files: dict[str, str], ctx: Context) -> list[Violation]:
    kind, arts, v = read_story(sid, files, ctx)
    if kind is None or v:
        return v
    return (judge_order(sid, kind, arts, ctx) + judge_age(sid, arts, ctx) + judge_roles(sid, kind, arts, ctx)
            + judge_criteria(sid, arts)
            + judge_triggers(sid, arts, ctx, approvals(files.get("approvals.md"))) + judge_findings(sid, kind, arts, ctx)
            + judge_close(sid, kind, arts, ctx))


# ==============================================================================
# The real tree
# ==============================================================================

def commit_paths(sha: str) -> list[str] | None:
    ok = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"], cwd=ROOT,
                        capture_output=True, text=True, check=False)
    if ok.returncode != 0:
        return None
    out = subprocess.run(["git", "show", "--name-only", "--format=", sha], cwd=ROOT, capture_output=True, text=True, check=False)
    return [l for l in out.stdout.splitlines() if l.strip()]


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise LawError(f"`git {' '.join(args)}` failed: {out.stderr.strip()}")
    return out.stdout


def last_changes() -> dict[str, str]:
    """`<ID>/<file>` -> the commit that last changed it. A file differing from HEAD, staged, modified
    or untracked, is left out: it belongs to the commit being made."""
    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        raise LawError("a shallow clone cuts the history a stage's age is read from: run `git fetch --unshallow`")
    prefix, commits, sha = f"{STORIES}/", {}, ""
    for line in git("-c", "core.quotePath=false", "log", "--format=commit %H", "--name-only", "--", STORIES).splitlines():
        if line.startswith("commit "):
            sha = line.removeprefix("commit ")
        elif line.startswith(prefix):
            commits.setdefault(line.removeprefix(prefix), sha)
    for path in git("diff", "--name-only", "-z", "HEAD", "--", STORIES).split("\0"):
        commits.pop(path.removeprefix(prefix), None)
    return commits


def contains(ancestor: str, commit: str) -> bool:
    out = subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, commit], cwd=ROOT,
                         capture_output=True, text=True, check=False)
    if out.returncode > 1:
        raise LawError(f"`git merge-base --is-ancestor {ancestor} {commit}` failed: {out.stderr.strip()}")
    return out.returncode == 0


def context() -> Context:
    law = ROOT / STANDARD
    if not law.is_file():
        raise LawError(f"{STANDARD} is missing")
    text = law.read_text(encoding="utf-8")
    tracker = (ROOT / "sprint" / "story-tracker.md").read_text(encoding="utf-8")
    roster = {p.stem for p in (ROOT / ".claude" / "agents").glob("*.md")}
    log = ROOT / code_standard.LOG_FILE
    rows, _ = code_standard.parse_log(log.read_text(encoding="utf-8") if log.is_file() else None)
    return Context(read_role_map(text), read_triggers(text), roster,
                   {s.id: s.status for s in session_closeout.tracker_stories(tracker)}, rows, commit_paths,
                   last_changes().get, contains)


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    folders = sorted(p for p in (ROOT / STORIES).glob("*") if p.is_dir()) if (ROOT / STORIES).is_dir() else []
    if not folders:
        print(f"Story Artifacts Gate: no stories under {STORIES}; nothing to judge.")
        return 0
    try:
        ctx = context()
    except LawError as e:
        print(f"story_artifacts: cannot run: {e}", file=sys.stderr)
        return 2
    v = []
    for folder in folders:
        files = {p.name: p.read_text(encoding="utf-8") for p in folder.glob("*.md")}
        v += judge_story(folder.name, files, ctx)
    print(f"\nStory Artifacts Gate ({len(folders)} stories)")
    print("=" * 60)
    if not v:
        print("PASSED")
        return 0
    print(f"BLOCKED: {len(v)} violation(s)\n")
    for x in v:
        print(f"  {x.where}\n    Rule:   {x.rule}\n    Detail: {x.detail}\n    Fix:    {FIXES.get(x.rule, '')}\n")
    return 1


# ==============================================================================
# SELF-TEST — every rule against a passing and a failing fixture, in memory
# ==============================================================================

ROSTER = {"product-manager", "solution-architect", "software-engineer", "qa-engineer", "code-reviewer",
          "security-engineer", "technical-writer", "devops-engineer"}


def _art(stage: str, role: str, input_: str, extra: str = "", body: str = "") -> str:
    """A passing artifact; a fixture that needs another status edits it in."""
    return (f"---\nstory: ACME-5.1\nstage: {stage}\nrole: {role}\ninput: {input_}\nstatus: pass\ntriggers: []\n"
            f"model: sonnet\neffort: high\n{extra}---\n\n{body}")


def _story(release: bool = True) -> dict[str, str]:
    """A whole software story, every rule kept."""
    s = {
        "brief.md": _art("brief", "product-manager", "none", extra="type: software\n",
                         body="## Acceptance criteria\n\n1. It doubles.\n2. It is typed.\n"),
        "design.md": _art("design", "solution-architect", "brief.md"),
        "build.md": _art("build", "software-engineer", "design.md", extra="commits: [abc1234]\n"),
        "verify.md": _art("verify", "qa-engineer", "build.md",
                          body="## Checks\n\n| Criterion | Check | Result |\n|---|---|---|\n| 1 | test_double | pass |\n| 2 | mypy | pass |\n"),
        "review.md": _art("review", "code-reviewer", "verify.md",
                          body="## Findings\n\n| Where | Finding | Severity | Fix |\n|---|---|---|---|\n"
                               "| `pipeline/a.py:double` | naming 1 — a vague name | minor | rename |\n"),
        "security.md": _art("security", "security-engineer", "review.md", body="## Findings\n\nNone.\n"),
        "docs.md": _art("docs", "technical-writer", "security.md"),
        "approvals.md": "| Trigger | What was approved | Chair's words | Date |\n|---|---|---|---|\n"
                        "| a deploy or release | ship it | go | 2026-10-24 |\n",
    }
    if release:
        s["release.md"] = _art("release", "devops-engineer", "docs.md", extra="run: 123\n")
    return s


LAST = {f"ACME-5.1/{s}.md": f"c{i}" for i, s in enumerate(STAGES, 1)}    # each stage committed alone, in order


def _linear(a: str, b: str) -> bool:
    """A history with no branch: commit c<j> is in the history of every c<i> with i >= j."""
    return int(a[1:]) <= int(b[1:])


def _ctx(status: str = "In Progress", paths: list[str] | None = None, logged: bool = True,
         changes: dict[str, str | None] | None = None) -> Context:
    text = (ROOT / STANDARD).read_text(encoding="utf-8")
    log = (code_standard.HEADER + "| 2026-10-24 | ACME-5.1 | `pipeline/a.py:double` | naming 1 — vague | code-reviewer | none | acknowledged |\n")
    rows, _ = code_standard.parse_log(log if logged else code_standard.HEADER)
    return Context(read_role_map(text), read_triggers(text), set(ROSTER), {"ACME-5.1": status}, rows,
                   lambda sha: (paths or ["pipeline/a.py"]) if sha == "abc1234" else None,
                   {**LAST, **(changes or {})}.get, _linear)


def _rules(v: list[Violation]) -> set[str]:
    return {x.rule for x in v}


def _edit(story: dict[str, str], name: str, old: str, new: str) -> dict[str, str]:
    assert old in story[name], f"fixture edit missing in {name}: {old!r}"
    return dict(story, **{name: story[name].replace(old, new, 1)})


def _t_law(check) -> None:
    text = (ROOT / STANDARD).read_text(encoding="utf-8")
    rm, trig = read_role_map(text), read_triggers(text)
    check("the role map holds the five story types", set(rm) == {"software", "data", "document", "game", "media"}, str(set(rm)))
    check("a stage a type lacks is absent: a document story has no security stage", "security" not in rm["document"])
    check("the code reviewer reviews software", rm["software"]["review"] == ["code-reviewer"])
    check("§4 lists the eleven triggers", len(trig) == 11 and RELEASE_TRIGGER in trig, str(trig))
    head, rest = text.split("## 3. Story types and the role map", 1)
    tableless = head + "## 3. Story types and the role map\n\nTo be written.\n\n## " + rest.split("\n## ", 1)[1]
    listless = text.split("## 4. Review triggers")[0] + "## 4. Review triggers\n\nNone.\n"
    for broken, reader, label in ((tableless, read_role_map, "a role-map section with no table"),
                                  (listless, read_triggers, "a triggers section with no list")):
        try:
            reader(broken)
            check(f"{label} raises, never reads as empty", False)
        except LawError:
            check(f"{label} raises, never reads as empty", True)


def _t_story(check) -> None:
    check("a whole software story passes", not judge_story("ACME-5.1", _story(), _ctx()), str(judge_story("ACME-5.1", _story(), _ctx())))
    unknown = {k: v.replace("story: ACME-5.1", "story: ACME-9.9") for k, v in _story().items()}
    check("a folder no tracker story names fails, its artifacts naming it alike", "story" in _rules(judge_story("ACME-9.9", unknown, _ctx())))
    check("an artifact naming another story fails",
          "story" in _rules(judge_story("ACME-5.1", _edit(_story(), "design.md", "story: ACME-5.1", "story: ACME-5.2"), _ctx())))
    check("a story with no brief fails its type", "type" in _rules(judge_story("ACME-5.1", {k: v for k, v in _story().items() if k != "brief.md"}, _ctx())))
    check("an unknown type fails", "type" in _rules(judge_story("ACME-5.1", _edit(_story(), "brief.md", "type: software", "type: poem"), _ctx())))
    check("an unparsable frontmatter fails", "frontmatter" in _rules(judge_story("ACME-5.1", _edit(_story(), "docs.md", "status: pass", "status: [x"), _ctx())))
    check("a file whose `stage:` is not its name fails",
          "frontmatter" in _rules(judge_story("ACME-5.1", _edit(_story(), "docs.md", "stage: docs", "stage: build"), _ctx())))
    for old, new, label in (("model: sonnet\n", "", "a stage that records no model fails"),
                            ("effort: high\n", "", "a stage that records no effort fails"),
                            ("model: sonnet", "model: gpt-5", "a stage whose model the ranking cannot place fails"),
                            ("effort: high", "effort: extreme", "a stage whose effort is no level fails")):
        v = judge_story("ACME-5.1", _edit(_story(), "docs.md", old, new), _ctx())
        check(label, [(x.rule, x.where) for x in v] == [("frontmatter", "ACME-5.1/docs.md")], str(v))
    check("a full model ID is recorded as well as an alias",
          not judge_story("ACME-5.1", _edit(_story(), "docs.md", "model: sonnet", "model: claude-opus-5-5"), _ctx()))
    check("a file that is no stage fails", "stage" in _rules(judge_story("ACME-5.1", dict(_story(), **{"notes.md": "x"}), _ctx())))
    doc = _edit(_story(), "brief.md", "type: software", "type: document")
    check("a stage the type lacks fails: a document story has no docs stage", "stage" in _rules(judge_story("ACME-5.1", doc, _ctx())))


def _t_order(check) -> None:
    s = _edit({k: v for k, v in _story().items() if k != "design.md"}, "build.md", "input: design.md", "input: brief.md")
    check("a build written before its design fails, though its input names the stage before it",
          "order" in _rules(judge_story("ACME-5.1", s, _ctx())))
    check("an input that is not the stage just before fails",
          "order" in _rules(judge_story("ACME-5.1", _edit(_story(), "verify.md", "input: build.md", "input: design.md"), _ctx())))
    check("a role that started from a failed input fails",
          "input-status" in _rules(judge_story("ACME-5.1", _edit(_story(), "build.md", "status: pass", "status: fail"), _ctx())))
    game = _edit(_edit(_story(), "brief.md", "type: software", "type: game"), "brief.md", "role: product-manager", "role: game-producer")
    game = {k: v for k, v in game.items() if k not in ("review.md", "security.md", "docs.md")}
    game = _edit(game, "release.md", "input: docs.md", "input: verify.md")
    ctx = _ctx()
    ctx.roster |= {"game-producer", "game-designer", "game-engine-developer", "game-qa-tester"}
    game = _edit(_edit(_edit(game, "design.md", "role: solution-architect", "role: game-designer"),
                       "build.md", "role: software-engineer", "role: game-engine-developer"), "verify.md", "role: qa-engineer", "role: game-qa-tester")
    check("a game story may skip its optional review", not judge_story("ACME-5.1", game, ctx), str(judge_story("ACME-5.1", game, ctx)))


def _t_age(check) -> None:
    def only_age_at(v: list[Violation], where: str) -> bool:
        return [(x.rule, x.where) for x in v] == [("age", f"ACME-5.1/{where}")]

    v = judge_story("ACME-5.1", _story(), _ctx(changes={"ACME-5.1/build.md": "c9"}))
    check("a verify older than a rebuilt build fails, on its own rule alone", only_age_at(v, "verify.md"), str(v))
    v = judge_story("ACME-5.1", _story(), _ctx(changes={"ACME-5.1/verify.md": "c3"}))
    check("a stage committed in one commit with its input fails", only_age_at(v, "verify.md"), str(v))
    now = {"ACME-5.1/docs.md": None}
    v = judge_story("ACME-5.1", _story(release=False), _ctx(changes=now))
    check("a stage in the commit being made, over a committed input, passes", not v, str(v))
    v = judge_story("ACME-5.1", _story(), _ctx(changes={**now, "ACME-5.1/release.md": None}))
    check("a stage and its input both in the commit being made fail", only_age_at(v, "release.md"), str(v))
    kept = {k: s for k, s in _story(release=False).items() if k in ("brief.md", "design.md", "build.md", "approvals.md")}
    v = judge_story("ACME-5.1", kept, _ctx(changes={"ACME-5.1/build.md": None}))
    check("a rebuild that removes every stage after it passes", not v, str(v))
    ctx = _ctx(changes={f"ACME-5.1/{s}.md": f"c{i}" for i, s in enumerate(STAGES[2:], 9)})
    ctx.contains = lambda a, b: a == b or (a != "c9" and _linear(a, b))     # c9, the build, on a branch alone
    v = judge_story("ACME-5.1", _story(), ctx)
    check("a stage made on a branch that never saw its input's last change fails", only_age_at(v, "verify.md"), str(v))


def _t_roles(check) -> None:
    check("a role the map does not allow at the stage fails",
          "role" in _rules(judge_story("ACME-5.1", _edit(_story(), "design.md", "role: solution-architect", "role: qa-engineer"), _ctx())))
    ctx = _ctx()
    ctx.roster.discard("technical-writer")
    check("a role the roster lacks fails", "role" in _rules(judge_story("ACME-5.1", _story(), ctx)))
    ctx = _ctx()
    ctx.role_map["software"]["verify"].append("software-engineer")
    s = _edit(_story(), "verify.md", "role: qa-engineer", "role: software-engineer")
    check("the builder verifying its own work fails, even where the map allows the role", "builder" in _rules(judge_story("ACME-5.1", s, ctx)))


def _t_criteria(check) -> None:
    check("a brief with no numbered criteria fails",
          "criteria" in _rules(judge_story("ACME-5.1", _edit(_story(), "brief.md", "1. It doubles.\n2. It is typed.", "It doubles."), _ctx())))
    check("a passing verify missing a criterion fails",
          "criteria" in _rules(judge_story("ACME-5.1", _edit(_story(), "verify.md", "| 2 | mypy | pass |\n", ""), _ctx())))
    check("a passing verify whose check failed fails",
          "criteria" in _rules(judge_story("ACME-5.1", _edit(_story(), "verify.md", "| 2 | mypy | pass |", "| 2 | mypy | fail |"), _ctx())))


def _t_triggers(check) -> None:
    s = _edit(_story(), "approvals.md", "| a deploy or release | ship it | go | 2026-10-24 |\n", "")
    check("a release the Chair has not approved fails", "trigger" in _rules(judge_story("ACME-5.1", s, _ctx())))
    s = _edit(_story(), "build.md", "triggers: []", "triggers: [a cost]")
    check("a declared trigger unapproved at release fails", "trigger" in _rules(judge_story("ACME-5.1", s, _ctx())))
    check("a trigger named outside §4 fails, before any release",
          "trigger" in _rules(judge_story("ACME-5.1", _edit(_story(release=False), "build.md", "triggers: []", "triggers: [vibes]"), _ctx())))
    check("a build commit touching a manifest hits a new dependency",
          "trigger" in _rules(judge_story("ACME-5.1", _story(), _ctx(paths=["requirements.txt"]))))
    check("a build commit touching the writing profile hits a gate or CI change",
          "trigger" in _rules(judge_story("ACME-5.1", _story(), _ctx(paths=["writing-profile.yaml"]))))
    s = _edit(_story(release=False), "build.md", "triggers: []", "triggers: [a cost]")
    check("a hit trigger before the release waits, not yet a violation", not judge_story("ACME-5.1", s, _ctx()))
    check("a commit the repository lacks fails", "commits" in _rules(judge_story("ACME-5.1", _edit(_story(), "build.md", "abc1234", "fff0000"), _ctx())))
    s = {k: v for k, v in _edit(_story(), "build.md", "triggers: []", "triggers: [an external service]").items() if k != "security.md"}
    s = _edit(s, "docs.md", "input: security.md", "input: review.md")
    s = _edit(s, "approvals.md", "| a deploy", "| an external service | the API | yes | 2026-10-24 |\n| a deploy")
    check("a release past an external service with no security stage fails", "security" in _rules(judge_story("ACME-5.1", s, _ctx())))


def _t_findings(check) -> None:
    check("a review finding unanswered once the story moves on fails", "finding" in _rules(judge_story("ACME-5.1", _story(), _ctx(logged=False))))
    s = {k: v for k, v in _story(release=False).items() if k not in ("security.md", "docs.md")}
    check("a review finding unanswered before the story moves on waits", not judge_story("ACME-5.1", s, _ctx(logged=False)))


def _t_close(check) -> None:
    check("a release with no CI run fails", "release" in _rules(judge_story("ACME-5.1", _edit(_story(), "release.md", "run: 123\n", ""), _ctx())))
    check("a story marked Done without its release fails", "done" in _rules(judge_story("ACME-5.1", _story(release=False), _ctx(status="Done"))))
    check("a story marked Done with its release passes", not judge_story("ACME-5.1", _story(), _ctx(status="Done")))


def _t_own_limits(check) -> None:
    own = code_standard.measure_python(Path(__file__).read_text(encoding="utf-8"))
    over = [f"{f.name} ({f.complexity}c/{f.code_lines}l/{f.parameters}p)" for f in own
            if code_standard.judge_function("", f, "production")]
    check("this gate's own functions meet the coding standard's production limits", not over, ", ".join(over))


def run_self_test() -> int:
    print("\nStory Artifacts Self-Test")
    print("=" * 60)
    check, state = code_standard._check_factory()
    for group in (_t_law, _t_story, _t_order, _t_age, _t_roles, _t_criteria, _t_triggers, _t_findings, _t_close, _t_own_limits):
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                group(check)
        except Exception as e:   # a crash is a failed fixture, never a crashed self-test
            check(f"{group.__name__} ran without raising", False, f"{type(e).__name__}: {e}")
    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 0 if not state["failures"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
