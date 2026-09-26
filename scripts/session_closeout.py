#!/usr/bin/env python3
"""
session_closeout.py — a session ends with a verified handoff pair, and the pair lives one session.

THE FAILURE THIS CLOSES
-----------------------
The session end protocol was five prose steps. Nothing verified that a handoff was written, that
sprint-status was updated, that learnings were flushed, or that the next session had a prompt. One
session decided the kickoff prompt "is not a repo artifact" and handed it over in chat. Handoffs
also accreted rules and constraints, becoming a second knowledge base that nothing indexed and no
gate watched. Decision 2026-09-21-001.

WHAT IT CHECKS
--------------
--check     every commit
  * sprint/handoffs/ holds only HANDOFF_S<N>.md and KICKOFF_S<N>.md (plus archive/); at most two
    session numbers, consecutive; every number is a complete pair
  * each handoff and kickoff carries exactly the required H2 sections, in order, non-empty, with
    no unfilled {{TOKEN}}; wikilinks resolve; every decision ID cited is in a decision index — the
    project's (sprint/decision-log.md) or the framework's (docs/governance/framework_decisions.md)
  * each kickoff names a registered persona and the version it copied, copies its Invocation
    block verbatim, and every task cites a story ID present in sprint/story-tracker.md
  * each docs/personas/<slug>.md has the required frontmatter (name, description, an integer
    version) and exactly the four sections; personas are append-only (decision 2026-09-23-002):
    an Invocation that differs from the committed copy needs a higher version, the version never
    goes down, and the Changelog carries a bullet for the current version
  * sprint/sprint-status.md: newest entry headed `## S<N> — YYYY-MM-DD — title`; at most 10 entries
  * sprint/story-tracker.md Summary Statistics equal the counted rows ([EXAMPLE] epics skipped)
  * a story In Progress or Done whose listed dependency is not Done fails (TMPL-5.5, decision
    2026-09-24-001): the sprint standard's "never start a story whose dependencies are not Done"
  * in a project (a .project-profile exists) whose tracker holds a non-example epic, an [EXAMPLE]
    row or heading, or an unfilled {{TOKEN}}, in the tracker, sprint-status or the decision log
    fails; text quoted in inline or fenced code is the convention explaining itself, not a live
    placeholder. The template has no profile and is exempt; a fresh project keeps the shipped
    example epic until its first real one
  * every [[slug]] in any text file git would commit resolves to docs/orchestration/knowledge/
    <slug>.md, with an allow set for the convention's own placeholders and the fixture slug
    the self-test uses (TMPL-5.2); the handoff linter above proved it for handoffs alone
  * AGENTS.md is at most 32 KiB, the Codex project-doc cap
--closeout  session end: archives every pair older than the session being closed, then verifies
            that the pair for the next session exists and passes every check above; refuses a
            persona this project holds that dev-resources lacks at the synced ref, or holds at a
            lower version — the registry grows only through resources_sync.py --publish
            (decision 2026-09-23-007). A project that has never synced (no .resources-version)
            is not held to it.
--verify    cold start: the verification of --closeout without the rotation, plus a clean tree.
            A fresh project — no pairs and sprint-status at S1 — passes.
--scaffold  writes the next session's HANDOFF/KICKOFF skeletons; they fail --check until filled
--personas  the persona rule of --check alone, for a repository that holds a registry and no
            sprint state — `dev-resources` consumes it as the `persona-lint` hook published by
            `.pre-commit-hooks.yaml` (decision 2026-09-23-005)
--self-test in-memory fixtures, run before the gate on every commit

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It cannot read prose, so it cannot prove a sentence in a handoff was not durable. The rotation is
the control for that: a fact left only in a handoff leaves the mandatory reads one session later.

Usage:  pre-commit run session-closeout-check --all-files
        pre-commit run session-closeout --hook-stage manual --all-files   (see CLOSEOUT_COMMAND)
        pre-commit run session-verify --hook-stage manual
        python3 scripts/session_closeout.py --scaffold --persona <slug>
        python3 scripts/session_closeout.py --self-test
Exit 0 = clean, 1 = violations (blocks the commit or the session), 2 = cannot run.
"""

from __future__ import annotations

import datetime
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_freshness_scan  # noqa: E402 — the decision-index parser, not its main()


def repo_root() -> Path:
    """The repository under judgement: the git top level of the working directory.

    Not the script's parent. This module is also installed as a hook package through
    `.pre-commit-hooks.yaml` (decision 2026-09-23-005), where `__file__` sits inside pre-commit's
    virtualenv and the repository is the one the hook runs in. pre-commit runs every hook from
    that repository's root, and the documented direct invocations run from it too. Outside a
    repository the working directory itself is judged, and the checks then fail on what is missing
    rather than pass on a tree that is not there.
    """
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False)
    top = out.stdout.strip()
    return Path(top) if out.returncode == 0 and top else Path.cwd()


ROOT = repo_root()
HANDOFFS = ROOT / "sprint" / "handoffs"
ARCHIVE = HANDOFFS / "archive"
PERSONAS = ROOT / "docs" / "personas"
STATUS = ROOT / "sprint" / "sprint-status.md"
TRACKER = ROOT / "sprint" / "story-tracker.md"
LOG = ROOT / "sprint" / "decision-log.md"
# The template's decisions live beside the project's (decision 2026-09-23-003); a handoff may cite
# an ID from either, read as one set in this order, the framework file winning a duplicate.
DECISION_LOGS = {"sprint/decision-log.md": LOG, "docs/governance/framework_decisions.md": ROOT / "docs" / "governance" / "framework_decisions.md"}
KB = ROOT / "docs" / "orchestration" / "knowledge"
BRAIN = ROOT / "AGENTS.md"
PROFILE = ROOT / ".project-profile"             # present in a project, absent in the template
RESOURCES_STAMP = ROOT / ".resources-version"   # `<ref> <sha>`, written by resources_sync.py
# The three sprint documents the live-placeholder rule reads, by the path the report names.
SPRINT_FILES = {"sprint/story-tracker.md": TRACKER, "sprint/sprint-status.md": STATUS, "sprint/decision-log.md": LOG}
RESOURCES_REF_PREFIX = "refs/resources/"

HANDOFF_NAME = re.compile(r"^HANDOFF_S(\d+)\.md$")
KICKOFF_NAME = re.compile(r"^KICKOFF_S(\d+)\.md$")
STATUS_ENTRY = re.compile(r"^## S(\d+) — \d{4}-\d{2}-\d{2} — \S.*$")
STORY_ID = re.compile(r"\b([A-Z][A-Z0-9]*-\d+\.\d+)\b")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
TOKEN = re.compile(r"(?<!\$)\{\{\s*[^}]+?\s*\}\}")
INLINE_CODE = re.compile(r"`[^`\n]*`")
EXAMPLE_MARK = "[EXAMPLE]"
# Wikilinks that resolve to no entry and are not a defect: the convention's own placeholders
# (`[[slug]]`, `[[<slug>]]`, `[[other-slug]]`, `[[wikilink]]` in the documents that explain it,
# `[[{slug}]]` in this gate's own message) and the slug the self-test fixtures use. Anything
# else that does not resolve blocks the commit. Adding a fixture slug means adding it here.
WIKILINK_ALLOW = {"slug", "<slug>", "other-slug", "wikilink", "{slug}", "reference_nowhere"}
WIKILINK_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".toml"}
H2 = re.compile(r"^## (.+?)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")

HANDOFF_SECTIONS = [
    "1. Mandatory reads",
    "2. Completed last session",
    "3. In progress",
    "4. Decisions logged",
    "5. Blockers and open questions",
    "6. Verification observed",
]
KICKOFF_SECTIONS = ["1. Persona", "2. Cold start", "3. Tasks", "4. Success criteria", "5. Closeout"]
PERSONA_SECTIONS = ["Expertise", "Insists on", "Invocation", "Changelog"]
PERSONA_KEYS = ["name", "description", "version"]
# A changelog bullet opens with the version it records: `- 2 — 2026-09-24 — what changed`.
CHANGELOG_ENTRY = re.compile(r"^(\d+)\s+—")


class Persona(NamedTuple):
    """What a kickoff copies from the registry: the Invocation block and the version it is at."""
    invocation: str
    version: str
STATUSES = ("Not Started", "In Progress", "Blocked", "Done")
STARTED = ("In Progress", "Done")   # a story in one of these has begun, so its dependencies were due
MAX_STATUS_ENTRIES = 10
MAX_BRAIN_BYTES = 32 * 1024
NONE_MARKERS = {"none", "none."}
# `--all-files` is load-bearing: without it pre-commit stashes unstaged changes to tracked files
# before running the hook, and the gate then judges the last commit's sprint-status and tracker
# rather than the ones just edited ([[reference_precommit_stash]]). The hook takes no filenames,
# so the flag changes nothing but the stash.
CLOSEOUT_COMMAND = "pre-commit run session-closeout --hook-stage manual --all-files"


# ==============================================================================
# Markdown helpers
# ==============================================================================

def sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split on H2 headings outside fenced code. Returns (preamble, [(heading, body), ...])."""
    pre: list[str] = []
    out: list[tuple[str, str]] = []
    cur: str | None = None
    buf: list[str] = []
    fenced = False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
        m = None if fenced else H2.match(line)
        if m:
            if cur is None:
                pre = buf
            else:
                out.append((cur, "\n".join(buf)))
            cur, buf = m.group(1), []
        else:
            buf.append(line)
    if cur is None:
        pre = buf
    else:
        out.append((cur, "\n".join(buf)))
    return "\n".join(pre), out


def field(text: str, label: str) -> str | None:
    m = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$", text, re.M)
    return m.group(1) if m else None


def norm(s: str) -> str:
    return " ".join(s.split())


def bullets(body: str) -> list[str]:
    return [ln.strip()[2:].strip() for ln in body.splitlines() if ln.strip().startswith("- ")]


def only_bullets(body: str) -> bool:
    return all(ln.strip().startswith("- ") for ln in body.splitlines() if ln.strip())


# ==============================================================================
# Linters — pure functions over text, so the self-test needs no files
# ==============================================================================

def lint_common(text: str, kind: str, n: int, required: list[str]) -> tuple[list, dict]:
    v: list[tuple[str, str]] = []
    title = f"# {kind} — S{n}"
    first = next((ln for ln in text.splitlines() if ln.strip()), "").strip()
    if first != title:
        v.append(("title", f"first line must be `{title}`, found `{first}`"))
    fs = field(text, "For session")
    if fs != f"S{n}":
        v.append(("for-session", f"`**For session:** S{n}` expected, found {fs!r}"))
    tok = TOKEN.search(text)
    if tok:
        v.append(("unfilled-token", f"unfilled token {tok.group(0)} — a scaffold is not a handoff"))
    _, secs = sections(text)
    heads = [h for h, _ in secs]
    if heads != required:
        v.append((
            "sections",
            f"H2 headings must be exactly {required}, in order; found {heads}. "
            "There is no section for durable content by design: rules go to the knowledge base, "
            "decisions to the log, work to the tracker — and the handoff links to them.",
        ))
    for h, b in secs:
        if h in required and not norm(b):
            v.append(("empty-section", f"section `{h}` is empty; write `- None.` if there is nothing"))
    return v, dict(secs)


def lint_handoff(text: str, n: int, decision_ids: set[str], kb_slugs: set[str]) -> list:
    v, secs = lint_common(text, "Handoff", n, HANDOFF_SECTIONS)
    wb = field(text, "Written by")
    if wb != f"S{n - 1}":
        v.append(("written-by", f"`**Written by:** S{n - 1}` expected, found {wb!r}"))
    for slug in WIKILINK.findall(text):
        if slug.strip() not in kb_slugs:
            v.append(("wikilink", f"[[{slug}]] has no docs/orchestration/knowledge/{slug.strip()}.md"))
    body = secs.get(HANDOFF_SECTIONS[3], "")
    if norm(body) and not only_bullets(body):
        v.append(("decision-id", "section 4 lists decision IDs, one `- ` bullet each (or `- None.`)"))
    for b in bullets(body):
        if b.lower() in NONE_MARKERS:
            continue
        head = b.split()[0].rstrip(":,") if b.split() else ""
        if head not in decision_ids:
            v.append(("decision-id", f"`{head}` is not in the decision-log index"))
    return v


def lint_kickoff(text: str, n: int, personas: dict[str, Persona], story_ids: set[str]) -> list:
    v, secs = lint_common(text, "Kickoff", n, KICKOFF_SECTIONS)
    slug = field(text, "Persona")
    if slug not in personas:
        v.append(("persona", f"`**Persona:** {slug}` is not registered; add docs/personas/{slug}.md "
                             "in the same commit — a persona is written when a task first needs it"))
    else:
        if norm(secs.get(KICKOFF_SECTIONS[0], "")) != norm(personas[slug].invocation):
            v.append(("persona-copy", f"section 1 must copy the Invocation block of docs/personas/{slug}.md "
                                      "verbatim; the registry is the source and the kickoff is a copy"))
        version = field(text, "Persona version")
        if version != personas[slug].version:
            v.append(("persona-version", f"`**Persona version:** {version}` must name the registry's "
                                         f"`version: {personas[slug].version}` for {slug}; the scaffold "
                                         "writes it — a kickoff says which persona version it was written against"))
    cold = secs.get(KICKOFF_SECTIONS[1], "")
    for must in ("AGENTS.md", f"HANDOFF_S{n}.md"):
        if must not in cold:
            v.append(("cold-start", f"section 2 must direct the reader to `{must}`"))
    tasks = bullets(secs.get(KICKOFF_SECTIONS[2], ""))
    if not tasks:
        v.append(("tasks", "section 3 needs at least one `- ` task"))
    for t in tasks:
        ids = STORY_ID.findall(t)
        if not ids:
            v.append(("task-story", f"task `{t[:60]}` cites no story ID; work lives in the tracker"))
        for sid in ids:
            if sid not in story_ids:
                v.append(("task-story", f"`{sid}` is not a story in sprint/story-tracker.md"))
    if "session-closeout" not in secs.get(KICKOFF_SECTIONS[4], ""):
        v.append(("closeout", f"section 5 must name the closeout command: `{CLOSEOUT_COMMAND}`"))
    return v


def persona_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """(keys, body_after_frontmatter) or (None, '') when the block is absent/unterminated."""
    if not text.startswith("---"):
        return None, ""
    end = text.find("\n---", 3)
    if end == -1:
        return None, ""
    fm = text[3:end]
    keys = {m.group(1): m.group(2).strip() for m in re.finditer(r"^([a-z_]+):\s*(.*)$", fm, re.M)}
    return keys, text[end + 4:]


def lint_persona(text: str, slug: str, previous: str | None = None) -> list:
    """`previous` is the committed copy (git HEAD), or None for a new persona.

    Personas are append-only (decision 2026-09-23-002): an Invocation is never changed in place.
    A change to it needs a higher `version:` and a Changelog bullet for that version. A bump with
    no Invocation change is allowed: Expertise and Insists on may be enhanced too, and a bump
    that records nothing costs a line. The version never decreases.
    """
    v: list[tuple[str, str]] = []
    keys, body = persona_frontmatter(text)
    if keys is None:
        return [("frontmatter", "persona needs a --- frontmatter block with name:, slug:, description:, version:")]
    for k in PERSONA_KEYS:
        if not keys.get(k):
            v.append(("frontmatter", f"missing `{k}:`"))
    if keys.get("slug") != slug:
        v.append(("slug", f"`slug: {slug}` must equal the filename stem, found {keys.get('slug')!r}"))
    version = keys.get("version", "")
    if version and not re.fullmatch(r"[1-9]\d*", version):
        v.append(("version", f"`version: {version}` must be a positive integer; the first release is 1"))
        version = ""
    _, secs = sections(body)
    heads = [h for h, _ in secs]
    if heads != PERSONA_SECTIONS:
        v.append(("sections", f"H2 headings must be exactly {PERSONA_SECTIONS}, found {heads}"))
    for h, b in secs:
        if not norm(b):
            v.append(("empty-section", f"section `{h}` is empty"))
    if version:
        logged = {m.group(1) for m in map(CHANGELOG_ENTRY.match, bullets(dict(secs).get("Changelog", ""))) if m}
        if version not in logged:
            v.append(("changelog", f"the Changelog has no bullet for version {version}; append "
                                   f"`- {version} — <date> — <what changed>`"))
    if previous is not None and version:
        prev_keys, prev_body = persona_frontmatter(previous)
        prev_version = (prev_keys or {}).get("version", "")
        if re.fullmatch(r"[1-9]\d*", prev_version):
            if int(version) < int(prev_version):
                v.append(("version-order", f"`version: {version}` is below the committed {prev_version}; "
                                           "a version never goes down"))
            elif int(version) == int(prev_version) and norm(dict(sections(body)[1]).get("Invocation", "")) \
                    != norm(dict(sections(prev_body)[1]).get("Invocation", "")):
                v.append(("invocation-unbumped", f"the Invocation differs from the committed copy at version "
                                                 f"{prev_version}; a persona is append-only — bump `version:` "
                                                 "and add the Changelog bullet, never edit in place"))
    return v


def persona_invocation(text: str) -> str:
    _, body = persona_frontmatter(text)
    return dict(sections(body)[1]).get("Invocation", "")


def persona_version(text: str) -> str:
    keys, _ = persona_frontmatter(text)
    return (keys or {}).get("version", "")


def published_state(local: str, published: str | None) -> tuple[str, str] | None:
    """The closeout rule for one persona against its copy in dev-resources at the synced ref:
    absent there, or behind the local version, is unpublished. Behind locally is the sync's
    business, not the closeout's."""
    if published is None:
        return ("unpublished", "not in dev-resources at the synced ref; run `python3 scripts/resources_sync.py "
                               "--apply --publish <clone>`, commit and push there, then sync again")
    lv, pv = persona_version(local), persona_version(published)
    if lv.isdigit() and pv.isdigit() and int(lv) > int(pv):
        return ("unpublished", f"version {lv} here, {pv} published; publish the enhancement before closing")
    return None


# ==============================================================================
# Folder, status and tracker state — pure over names/text
# ==============================================================================

def folder_state(names: list[str]) -> tuple[dict[int, set[str]], list]:
    v: list[tuple[str, str]] = []
    nums: dict[int, set[str]] = {}
    for name in names:
        m = HANDOFF_NAME.match(name) or KICKOFF_NAME.match(name)
        if not m:
            v.append(("stray", f"{name}: only HANDOFF_S<N>.md and KICKOFF_S<N>.md belong in "
                               "sprint/handoffs/; older material goes in archive/"))
            continue
        nums.setdefault(int(m.group(1)), set()).add(name.split("_", 1)[0])
    for n, kinds in sorted(nums.items()):
        if kinds != {"HANDOFF", "KICKOFF"}:
            v.append(("incomplete-pair", f"S{n} has only {sorted(kinds)}; a session's handoff and "
                                         "kickoff are written together"))
    if len(nums) > 2:
        v.append(("too-many", f"{len(nums)} session numbers present ({sorted(nums)}); at most two — "
                              f"run `{CLOSEOUT_COMMAND}` to archive older pairs"))
    elif len(nums) == 2:
        a, b = sorted(nums)
        if b != a + 1:
            v.append(("gap", f"S{a} and S{b} are not consecutive"))
    return nums, v


def rotation_plan(numbers: set[int], current: int) -> list[int]:
    """Session numbers to archive at the closeout of `current`: everything older than it."""
    return sorted(n for n in numbers if n < current)


def verify_state(current: int | None, numbers: set[int], closing: bool = False) -> list:
    """`closing` is the closeout itself: the next pair is required even on a fresh project.
    Without it (a cold-start verify) session 1 may start with no incoming pair."""
    v: list[tuple[str, str]] = []
    if current is None:
        return [("status", "newest sprint-status entry must be headed `## S<N> — YYYY-MM-DD — title`")]
    if not numbers and not closing:
        if current == 1:
            return v  # a fresh project: session 1 starts with no incoming pair
        return [("no-pair", f"sprint-status says S{current} but sprint/handoffs/ holds no pair")]
    if current + 1 not in numbers:
        v.append(("not-closed", f"S{current} did not close out: HANDOFF_S{current + 1}.md and "
                                f"KICKOFF_S{current + 1}.md are missing. Run --scaffold, fill both, "
                                f"then `{CLOSEOUT_COMMAND}`"))
    extra = [n for n in sorted(numbers) if n not in (current, current + 1)]
    if extra:
        v.append(("stale-pair", f"S{extra} should be in archive/ (session being closed is S{current})"))
    return v


def status_headings(text: str) -> list[str]:
    _, secs = sections(text)
    return [h for h, _ in secs]


def newest_session(text: str) -> int | None:
    heads = status_headings(text)
    m = STATUS_ENTRY.match(f"## {heads[0]}") if heads else None
    return int(m.group(1)) if m else None


class Story(NamedTuple):
    """One row of a non-example epic: its ID, its Status cell, and the story IDs its Dependencies
    cell lists (`—` lists none)."""
    id: str
    status: str
    deps: tuple[str, ...]


def real_epics(text: str) -> list[str]:
    """The `## Epic:` headings that are not marked [EXAMPLE], in file order."""
    _, secs = sections(text)
    return [h for h, _ in secs if h.startswith("Epic:") and EXAMPLE_MARK not in h]


def tracker_stories(text: str) -> list[Story]:
    """Every story row under a non-example epic. The statistics, the kickoff's story IDs and the
    dependency rule all read this one parse, so they cannot disagree about what a row is."""
    out: list[Story] = []
    _, secs = sections(text)
    for h, b in secs:
        if not h.startswith("Epic:") or EXAMPLE_MARK in h:
            continue
        for line in b.splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or not STORY_ID.fullmatch(cells[0]):
                continue
            deps = tuple(STORY_ID.findall(cells[3])) if len(cells) > 3 else ()
            out.append(Story(cells[0], cells[2], deps))
    return out


def tracker_counts(text: str) -> tuple[dict[str, int], dict[str, int], set[str]]:
    stories = tracker_stories(text)
    computed: dict[str, int] = {}
    for s in stories:
        computed[s.status] = computed.get(s.status, 0) + 1
    ids = {s.id for s in stories}
    _, secs = sections(text)
    declared: dict[str, int] = {}
    for line in dict(secs).get("Summary Statistics", "").splitlines():
        m = re.match(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(\d+)\s*\|", line)
        if m:
            declared[m.group(1)] = int(m.group(2))
    return computed, declared, ids


def dangling_wikilinks(text: str, kb_slugs: set[str], allow: set[str] = WIKILINK_ALLOW) -> list[tuple[int, str]]:
    """(line, slug) for every `[[slug]]` that resolves to no knowledge entry and is not allowed.

    Pure over text, so the self-test needs no files. The handoff linter applies the same regex
    without the allow set: a handoff links real entries or nothing.
    """
    found: list[tuple[int, str]] = []
    for no, line in enumerate(text.splitlines(), 1):
        for raw in WIKILINK.findall(line):
            slug = raw.strip()
            if slug not in kb_slugs and slug not in allow:
                found.append((no, slug))
    return found


def tracker_violations(computed: dict[str, int], declared: dict[str, int]) -> list:
    v: list[tuple[str, str]] = []
    for s in computed:
        if s not in STATUSES:
            v.append(("status-value", f"`{s}` is not a status; use one of {STATUSES}"))
    want = {
        "Total Stories": sum(computed.values()),
        "Not Started": computed.get("Not Started", 0),
        "In Progress": computed.get("In Progress", 0),
        "Blocked": computed.get("Blocked", 0),
        "Completed": computed.get("Done", 0),
    }
    for k, n in want.items():
        if declared.get(k) != n:
            v.append(("stats", f"Summary Statistics says {k} = {declared.get(k)}; the rows count {n}"))
    return v


def dependency_violations(stories: list[Story]) -> list:
    """The sprint standard's §7 rule, "never start a story whose dependencies are not Done",
    judged on the tracker after the fact: a story In Progress or Done whose listed dependency is
    anything but Done, or is no story at all. Not Started and Blocked stories are waiting, which
    is what the rule asks of them (TMPL-5.5, decision 2026-09-24-001)."""
    status = {s.id: s.status for s in stories}
    v: list[tuple[str, str]] = []
    for s in stories:
        if s.status not in STARTED:
            continue
        for dep in s.deps:
            if status.get(dep) == "Done":
                continue
            found = f"is {status[dep]}" if dep in status else "is not a story in the tracker"
            v.append(("dependency-order", f"{s.id} is {s.status} but its dependency {dep} {found}; a story "
                                          "starts only when every dependency is Done (sprint standard §7) — "
                                          "finish the dependency, or fix the row that names it"))
    return v


def live_placeholders(text: str) -> list[tuple[int, str]]:
    """(line, what) for every [EXAMPLE] table row or heading and every unfilled {{TOKEN}}, read
    outside fenced blocks and inline code: a document that writes `[EXAMPLE]` or `{{PLACEHOLDER}}`
    in code spans is explaining the convention, and a GitHub Actions `${{ }}` is not a token."""
    found: list[tuple[int, str]] = []
    fenced = False
    for no, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        bare = INLINE_CODE.sub("", line)
        if EXAMPLE_MARK in bare and bare.lstrip().startswith(("|", "#")):
            found.append((no, f"{EXAMPLE_MARK} {'heading' if bare.lstrip().startswith('#') else 'row'}"))
        for m in TOKEN.finditer(bare):
            found.append((no, f"unfilled token {m.group(0)}"))
    return found


def placeholder_violations(texts: dict[str, str], project: bool) -> list:
    """The sprint standard's §11 rule, "no [EXAMPLE] or {{PLACEHOLDER}} content in a live
    sprint", over the three sprint documents keyed by path. It applies in a project (`project`:
    a .project-profile exists) whose tracker holds a non-example epic: the template keeps every
    shape it ships, and a fresh project keeps the shipped example epic until its planning session
    writes the first real one (TMPL-5.5, decision 2026-09-24-001). Returns (rule, where, detail)."""
    if not project or not real_epics(texts.get("sprint/story-tracker.md", "")):
        return []
    v: list[tuple[str, str, str]] = []
    for rel, text in texts.items():
        for no, what in live_placeholders(text):
            v.append(("live-placeholder", f"{rel}:{no}",
                      f"{what} in a live sprint; the tracker holds a real epic, so the shipped example "
                      "rows and every placeholder token go (sprint standard §5.2, §11)"))
    return v


# ==============================================================================
# Scaffolds — the agent never hand-types headings
# ==============================================================================

def handoff_skeleton(n: int, date: str) -> str:
    return f"""# Handoff — S{n}

**For session:** S{n}
**Written by:** S{n - 1}
**Written:** {date}

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S{n}.md`
- {{{{FILL: task-specific files, one per bullet, with why}}}}

## 2. Completed last session

- {{{{FILL: what was done, by story ID and file}}}}

## 3. In progress

- None.

## 4. Decisions logged

- None.

## 5. Blockers and open questions

- None.

## 6. Verification observed

- {{{{FILL: which gates ran and their exit codes}}}}
"""


def kickoff_skeleton(n: int, slug: str, persona: Persona) -> str:
    return f"""# Kickoff — S{n}

**For session:** S{n}
**Persona:** {slug}
**Persona version:** {persona.version}

## 1. Persona

{persona.invocation.strip()}

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S{n}.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual` and do no build work until it passes.

## 3. Tasks

- {{{{FILL: STORY-ID — what to do, in dependency order}}}}

## 4. Success criteria

- {{{{FILL: the executable checks that prove each task done}}}}

## 5. Closeout

Before ending: add a `## S{n} — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
flush durable learnings to `docs/orchestration/knowledge/` with an INDEX row, log decisions, update
the tracker, sync the registry (`python3 scripts/resources_sync.py --apply`, publishing what it
reports), then run `python3 scripts/session_closeout.py --scaffold --persona <slug>`, fill both
files for S{n + 1}, run `{CLOSEOUT_COMMAND}`, commit `checkpoint: closeout S{n}`, push, confirm
the `gates` run on GitHub is green, and hand the user the contents of `KICKOFF_S{n + 1}.md` as the
next session's prompt.
"""


# ==============================================================================
# Real-tree checks
# ==============================================================================

def decision_ids() -> tuple[set[str], list]:
    """Every indexed decision ID across both logs; an index missing from a log that exists is a
    violation, never an empty set."""
    texts = {rel: p.read_text(encoding="utf-8") for rel, p in DECISION_LOGS.items() if p.is_file()}
    if not texts:
        return set(), []
    try:
        return set(kb_freshness_scan.parse_logs(texts)), []
    except kb_freshness_scan.DecisionIndexNotFound as e:
        return set(), [("decision-log", "", f"cannot read the decision index: {e}")]


def committed_text(rel: str) -> str | None:
    """The file as committed at HEAD, or None when it is new or there is no HEAD."""
    out = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, text=True, check=False)
    return out.stdout if out.returncode == 0 else None


def load_personas() -> tuple[dict[str, Persona], list]:
    personas: dict[str, Persona] = {}
    v: list[tuple[str, str, str]] = []
    if not PERSONAS.is_dir():
        return personas, v
    for p in sorted(PERSONAS.glob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        for rule, detail in lint_persona(text, p.stem, committed_text(rel)):
            v.append((rule, rel, detail))
        personas[p.stem] = Persona(persona_invocation(text), persona_version(text))
    return personas, v


def unpublished_personas() -> list:
    """Every local persona against refs/resources/<ref>, where <ref> is the stamp's. No stamp: the
    project has never synced, and nothing is checked."""
    if not RESOURCES_STAMP.is_file():
        return []
    parts = RESOURCES_STAMP.read_text(encoding="utf-8").split()
    if len(parts) != 2:
        return [("resources-stamp", ".resources-version", "must read `<ref> <sha>`; re-run resources_sync.py --apply")]
    ref = f"{RESOURCES_REF_PREFIX}{parts[0]}"
    if subprocess.run(["git", "rev-parse", "--verify", "-q", ref], cwd=ROOT, capture_output=True, check=False).returncode:
        return [("resources-ref", ".resources-version", f"{ref} is not fetched in this clone; run resources_sync.py first")]
    v: list[tuple[str, str, str]] = []
    if PERSONAS.is_dir():
        for p in sorted(PERSONAS.glob("*.md")):
            rel = p.relative_to(ROOT).as_posix()
            out = subprocess.run(["git", "cat-file", "blob", f"{ref}:{rel}"], cwd=ROOT, capture_output=True, text=True, check=False)
            state = published_state(p.read_text(encoding="utf-8"), out.stdout if out.returncode == 0 else None)
            if state:
                v.append((state[0], rel, state[1]))
    return v


def committed_files() -> list[str]:
    """Paths git would commit, relative to ROOT: tracked plus untracked-and-not-ignored.

    The same list the banned-feature scan judges, so a scratch file in the tree is judged and an
    ignored one is not. Outside a repository, every file under ROOT.
    """
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, capture_output=True, text=True, check=False)
    if out.returncode == 0:
        return out.stdout.splitlines()
    return [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]


def tree_wikilink_violations(kb_slugs: set[str]) -> list:
    """The wikilink rule over every text file git would commit, except the handoffs the handoff
    linter judges without an allow set (a dangling link there would otherwise report twice)."""
    v: list[tuple[str, str, str]] = []
    for rel in committed_files():
        path = ROOT / rel
        if path.suffix not in WIKILINK_SUFFIXES or not path.is_file():
            continue
        if path.parent == HANDOFFS and HANDOFF_NAME.match(path.name):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for no, slug in dangling_wikilinks(text, kb_slugs):
            v.append(("wikilink", f"{rel}:{no}",
                      f"[[{slug}]] has no docs/orchestration/knowledge/{slug}.md — write the entry "
                      "with an INDEX row, fix the slug, or (a fixture or the convention's own text) "
                      "add it to WIKILINK_ALLOW"))
    return v


def folder_names() -> list[str]:
    if not HANDOFFS.is_dir():
        return []
    return sorted(p.name for p in HANDOFFS.iterdir() if p.name != "archive" and not p.name.startswith("."))


def check_all() -> tuple[list, dict[int, set[str]], int | None]:
    """Every --check rule over the real tree. Returns (violations, pair numbers, newest session)."""
    v: list[tuple[str, str, str]] = []
    ids, log_v = decision_ids()
    v.extend(log_v)
    kb_slugs = {p.stem for p in KB.glob("*.md")} if KB.is_dir() else set()
    personas, persona_v = load_personas()
    v.extend(persona_v)

    story_ids: set[str] = set()
    if TRACKER.is_file():
        tracker_text = TRACKER.read_text(encoding="utf-8")
        computed, declared, story_ids = tracker_counts(tracker_text)
        for rule, detail in tracker_violations(computed, declared) + dependency_violations(tracker_stories(tracker_text)):
            v.append((rule, "sprint/story-tracker.md", detail))
        texts = {rel: p.read_text(encoding="utf-8") for rel, p in SPRINT_FILES.items() if p.is_file()}
        v.extend(placeholder_violations(texts, PROFILE.is_file()))

    names = folder_names()
    nums, folder_v = folder_state(names)
    for rule, detail in folder_v:
        v.append((rule, "sprint/handoffs/", detail))
    for name in names:
        path = HANDOFFS / name
        text = path.read_text(encoding="utf-8")
        m = HANDOFF_NAME.match(name)
        if m:
            found = lint_handoff(text, int(m.group(1)), ids, kb_slugs)
        else:
            m = KICKOFF_NAME.match(name)
            found = lint_kickoff(text, int(m.group(1)), personas, story_ids) if m else []
        for rule, detail in found:
            v.append((rule, f"sprint/handoffs/{name}", detail))

    v.extend(tree_wikilink_violations(kb_slugs))

    current: int | None = None
    if STATUS.is_file():
        text = STATUS.read_text(encoding="utf-8")
        current = newest_session(text)
        if current is None:
            v.append(("status", "sprint/sprint-status.md",
                      "newest entry must be headed `## S<N> — YYYY-MM-DD — title`"))
        count = len(status_headings(text))
        if count > MAX_STATUS_ENTRIES:
            v.append(("status-cap", "sprint/sprint-status.md",
                      f"{count} entries; keep at most {MAX_STATUS_ENTRIES} — move the oldest to "
                      "sprint/archive/sprint-status_<year>.md"))

    if BRAIN.is_file():
        size = BRAIN.stat().st_size
        if size > MAX_BRAIN_BYTES:
            v.append(("brain-cap", "AGENTS.md",
                      f"{size} bytes; the Codex project-doc cap is {MAX_BRAIN_BYTES}. Move procedure "
                      "to docs/standards/ and keep only nouns and non-inferable constraints here"))
    return v, nums, current


def report(title: str, violations: list) -> int:
    print(f"\n{title}")
    print("=" * 60)
    if not violations:
        print("PASSED")
        return 0
    print(f"BLOCKED: {len(violations)} violation(s)\n")
    for rule, where, detail in violations:
        print(f"  {where}\n    Rule:   {rule}\n    Detail: {detail}\n")
    return 1


def git_dirty() -> list[str]:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True,
                         text=True, check=False)
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def cmd_check() -> int:
    v, _, _ = check_all()
    return report("Session State Gate", v)


def cmd_personas() -> int:
    personas, v = load_personas()
    where = PERSONAS.relative_to(ROOT) if PERSONAS.is_dir() else "no docs/personas/"
    return report(f"Persona Registry Lint ({len(personas)} persona(s); {where})", v)


def cmd_closeout() -> int:
    v, nums, current = check_all()
    if current is not None:
        ARCHIVE.mkdir(exist_ok=True)
        for n in rotation_plan(set(nums), current):
            for name in (f"HANDOFF_S{n}.md", f"KICKOFF_S{n}.md"):
                src = HANDOFFS / name
                if src.is_file():
                    src.rename(ARCHIVE / name)
                    print(f"archived  sprint/handoffs/{name} -> archive/")
        v = [x for x in v if x[0] not in ("too-many", "gap")]  # the rotation just cleared these
        nums = {n: k for n, k in nums.items() if n >= current}
    for rule, detail in verify_state(current, set(nums), closing=True):
        v.append((rule, "sprint/handoffs/", detail))
    v.extend(unpublished_personas())
    rc = report(f"Session Closeout (closing S{current})" if current else "Session Closeout", v)
    if rc == 0:
        print(f"\nCommit as `checkpoint: closeout S{current}`. The next session starts from "
              f"KICKOFF_S{current + 1}.md.")
    return rc


def cmd_verify() -> int:
    v, nums, current = check_all()
    for rule, detail in verify_state(current, set(nums)):
        v.append((rule, "sprint/handoffs/", detail))
    dirty = git_dirty()
    if dirty:
        v.append(("dirty-tree", "git status", f"{len(dirty)} uncommitted path(s); the previous session "
                                              "must have committed its closeout"))
    rc = report("Session Verify (previous session closed out)", v)
    if rc == 0 and current is not None:
        nxt = current + 1 if nums else current
        print(f"\nThis is S{nxt}. Add `## S{nxt} — <date> — <title>` to sprint-status at the first checkpoint.")
    return rc


def cmd_scaffold(slug: str | None) -> int:
    if not STATUS.is_file():
        print("session_closeout: no sprint/sprint-status.md", file=sys.stderr)
        return 2
    current = newest_session(STATUS.read_text(encoding="utf-8"))
    if current is None:
        print("session_closeout: newest sprint-status entry must be `## S<N> — YYYY-MM-DD — title` "
              "before a pair can be scaffolded", file=sys.stderr)
        return 1
    personas, _ = load_personas()
    if slug is None or slug not in personas:
        print(f"session_closeout: --persona <slug> is required; registered: {sorted(personas) or 'none'}",
              file=sys.stderr)
        return 2
    n = current + 1
    HANDOFFS.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    for name, text in ((f"HANDOFF_S{n}.md", handoff_skeleton(n, today)),
                       (f"KICKOFF_S{n}.md", kickoff_skeleton(n, slug, personas[slug]))):
        path = HANDOFFS / name
        if path.exists():
            print(f"exists    sprint/handoffs/{name} (left untouched)")
            continue
        path.write_text(text, encoding="utf-8")
        print(f"wrote     sprint/handoffs/{name}")
    print(f"\nFill every {{{{FILL}}}} token; --check refuses the pair until none remain.")
    return 0


# ==============================================================================
# SELF-TEST — pure fixtures; every rule has a passing and a failing case
# ==============================================================================

_IDS = {"2026-09-21-001"}
_KB = {"reference_session_closeout"}
_INVOCATION = "You are a senior platform engineer. You enforce rules with scripts."
_PERSONAS = {"framework-maintainer": Persona(_INVOCATION, "1")}
_STORIES = {"TMPL-1.2", "TMPL-1.3"}


def _good_handoff() -> str:
    t = handoff_skeleton(2, "2026-09-21")
    t = t.replace("- {{FILL: task-specific files, one per bullet, with why}}",
                  "- [[reference_session_closeout]] — the gate this session extends")
    t = t.replace("- {{FILL: what was done, by story ID and file}}", "- TMPL-1.2 shipped `scripts/session_closeout.py`")
    t = t.replace("- {{FILL: which gates ran and their exit codes}}", "- `pre-commit run --all-files` exit 0")
    return t.replace("## 4. Decisions logged\n\n- None.", "## 4. Decisions logged\n\n- 2026-09-21-001 closeout gate")


def _good_kickoff() -> str:
    t = kickoff_skeleton(2, "framework-maintainer", _PERSONAS["framework-maintainer"])
    t = t.replace("- {{FILL: STORY-ID — what to do, in dependency order}}", "- TMPL-1.3 write the persona seeds")
    return t.replace("- {{FILL: the executable checks that prove each task done}}", "- self-test exit 0")


_GOOD_PERSONA = ("---\nname: Framework maintainer\nslug: framework-maintainer\ndescription: builds gates\nversion: 1\n---\n\n"
                 "# Framework maintainer\n\n## Expertise\n\n- gates\n\n## Insists on\n\n- proof\n\n"
                 f"## Invocation\n\n{_INVOCATION}\n\n## Changelog\n\n- 1 — 2026-09-21 — seeded\n")
_BUMPED_PERSONA = (_GOOD_PERSONA.replace("version: 1", "version: 2")
                   .replace("enforce rules with scripts", "enforce rules with fixtures")
                   .replace("- 1 — 2026-09-21 — seeded\n", "- 1 — 2026-09-21 — seeded\n- 2 — 2026-09-24 — fixtures\n"))

_TRACKER = ("# Story Tracker\n\n## Summary Statistics\n\n| Metric | Count |\n|---|---|\n"
            "| **Total Stories** | 2 |\n| **Not Started** | 1 |\n| **In Progress** | 0 |\n"
            "| **Blocked** | 0 |\n| **Completed** | 1 |\n\n"
            "## Epic: INFRA-1 — Setup [EXAMPLE]\n\n| Story ID | Title | Status | D | S | P |\n|---|---|---|---|---|---|\n"
            "| INFRA-1.1 | x | Not Started | — | — | — |\n\n"
            "## Epic: TMPL-1 — Closeout\n\n| Story ID | Title | Status | D | S | P |\n|---|---|---|---|---|---|\n"
            "| TMPL-1.1 | a | Done | — | — | — |\n| TMPL-1.2 | b | Not Started | — | — | — |\n")

_STATUS = "# Sprint Status\n\n**Current Phase:** x\n\n---\n\n## S3 — 2026-09-21 — closeout\n\ntext\n\n## S2 — 2026-09-20 — older\n\ntext\n"

# Dependencies in every shape the rule must tell apart. The example epic's row is In Progress on a
# story that exists nowhere, so a variant that judged example rows fails the passing case.
_DEPS = ("## Epic: INFRA-1 — Setup [EXAMPLE]\n\n| Story ID | Title | Status | Dependencies | S | P |\n|---|---|---|---|---|---|\n"
         "| INFRA-1.2 | x | In Progress | INFRA-1.1 | — | — |\n\n"
         "## Epic: TMPL-1 — Closeout\n\n| Story ID | Title | Status | Dependencies | S | P |\n|---|---|---|---|---|---|\n"
         "| TMPL-1.1 | a | Done | — | — | — |\n"
         "| TMPL-1.2 | b | In Progress | TMPL-1.1 | — | — |\n"
         "| TMPL-1.3 | c | Not Started | TMPL-1.2 | — | — |\n"
         "| TMPL-1.4 | d | Blocked | TMPL-1.3 | — | — |\n"
         "| TMPL-1.5 | e | Done | TMPL-1.1, TMPL-1.6 | — | — |\n"
         "| TMPL-1.6 | f | Done | — | — | — |\n")

_EXAMPLE_EPIC = ("## Epic: INFRA-1 — Setup [EXAMPLE]\n\n| Story ID | Title | Status | D | S | P |\n|---|---|---|---|---|---|\n"
                 "| INFRA-1.1 | x | Not Started | — | — | — |\n\n")
_LOG = ("# Log\n\n## Decision Index\n\n| ID | Date | Title | Status |\n|---|---|---|---|\n"
        "| 2026-09-21-001 | 2026-09-21 | closeout | APPROVED |\n")
_LIVE = {"sprint/story-tracker.md": _TRACKER, "sprint/sprint-status.md": _STATUS, "sprint/decision-log.md": _LOG}


def _live(**over: str) -> dict[str, str]:
    """The three sprint documents with one or more replaced: tracker=, status=, log=."""
    keys = {"tracker": "sprint/story-tracker.md", "status": "sprint/sprint-status.md", "log": "sprint/decision-log.md"}
    return {**_LIVE, **{keys[k]: t for k, t in over.items()}}


def _rules(found: list) -> set[str]:
    return {r for r, *_ in found}


def run_self_test() -> int:
    print("\nSession Closeout Self-Test")
    print("=" * 60)
    failures = total = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    def expect(label: str, found: list, *rules: str) -> None:
        got = _rules(found)
        want = set(rules)
        check(label, got == want, f"rules={sorted(got)} expected={sorted(want)}")

    h = _good_handoff()
    expect("a filled handoff passes", lint_handoff(h, 2, _IDS, _KB))
    expect("an unfilled scaffold fails on its tokens",
           lint_handoff(handoff_skeleton(2, "2026-09-21"), 2, _IDS, _KB), "unfilled-token")
    expect("a missing section fails", lint_handoff(h.replace("## 3. In progress\n\n- None.\n", ""), 2, _IDS, _KB),
           "sections")
    expect("an extra section is refused — durable content has no home here",
           lint_handoff(h + "\n## 7. Rules to remember\n\n- never do X\n", 2, _IDS, _KB), "sections")
    expect("filename and For-session must agree", lint_handoff(h, 3, _IDS, _KB),
           "title", "for-session", "written-by")
    expect("an unindexed decision ID fails",
           lint_handoff(h.replace("2026-09-21-001 closeout gate", "2026-09-21-099 phantom"), 2, _IDS, _KB),
           "decision-id")
    expect("an unresolved wikilink fails",
           lint_handoff(h.replace("[[reference_session_closeout]]", "[[reference_nowhere]]"), 2, _IDS, _KB),
           "wikilink")
    expect("an empty section fails",
           lint_handoff(h.replace("- `pre-commit run --all-files` exit 0", ""), 2, _IDS, _KB), "empty-section")

    k = _good_kickoff()
    expect("a filled kickoff passes", lint_kickoff(k, 2, _PERSONAS, _STORIES))
    expect("an unregistered persona fails",
           lint_kickoff(k.replace("**Persona:** framework-maintainer", "**Persona:** wizard"), 2, _PERSONAS, _STORIES),
           "persona")
    expect("a persona copy that drifts from the registry fails",
           lint_kickoff(k.replace("enforce rules with scripts", "enforce rules with prose"), 2, _PERSONAS, _STORIES),
           "persona-copy")
    expect("a task citing an unknown story fails",
           lint_kickoff(k.replace("TMPL-1.3 write", "TMPL-9.9 write"), 2, _PERSONAS, _STORIES), "task-story")
    expect("a task citing no story fails",
           lint_kickoff(k.replace("- TMPL-1.3 write the persona seeds", "- write the persona seeds"), 2, _PERSONAS, _STORIES),
           "task-story")
    expect("a closeout section without the command fails",
           lint_kickoff(k.replace("session-closeout", "session-close"), 2, _PERSONAS, _STORIES), "closeout")
    expect("a kickoff naming a persona version the registry is not at fails",
           lint_kickoff(k.replace("**Persona version:** 1", "**Persona version:** 2"), 2, _PERSONAS, _STORIES),
           "persona-version")
    expect("a kickoff that names no persona version fails",
           lint_kickoff(k.replace("**Persona version:** 1\n", ""), 2, _PERSONAS, _STORIES), "persona-version")

    expect("a well-formed persona passes", lint_persona(_GOOD_PERSONA, "framework-maintainer"))
    expect("a persona whose slug differs from its filename fails", lint_persona(_GOOD_PERSONA, "other"), "slug")
    expect("a persona missing its Invocation fails (and, cut there, its Changelog with it)",
           lint_persona(_GOOD_PERSONA.split("## Invocation")[0], "framework-maintainer"), "sections", "changelog")
    check("the invocation block is extracted whole, without the Changelog after it",
          norm(persona_invocation(_GOOD_PERSONA)) == norm(_INVOCATION))
    check("the version is read from the frontmatter", persona_version(_GOOD_PERSONA) == "1")
    expect("a persona without version: fails",
           lint_persona(_GOOD_PERSONA.replace("version: 1\n", ""), "framework-maintainer"), "frontmatter")
    expect("a version that is not a positive integer fails",
           lint_persona(_GOOD_PERSONA.replace("version: 1", "version: 1.1"), "framework-maintainer"), "version")
    expect("a version with no Changelog bullet fails",
           lint_persona(_GOOD_PERSONA.replace("version: 1", "version: 2"), "framework-maintainer"), "changelog")
    expect("unchanged against the committed copy passes",
           lint_persona(_GOOD_PERSONA, "framework-maintainer", _GOOD_PERSONA))
    expect("an Invocation change with a bump and its bullet passes",
           lint_persona(_BUMPED_PERSONA, "framework-maintainer", _GOOD_PERSONA))
    expect("an Invocation change without a bump fails — personas are append-only",
           lint_persona(_GOOD_PERSONA.replace("enforce rules with scripts", "enforce rules with prose"),
                        "framework-maintainer", _GOOD_PERSONA), "invocation-unbumped")
    expect("a version below the committed one fails",
           lint_persona(_GOOD_PERSONA, "framework-maintainer", _BUMPED_PERSONA), "version-order")
    expect("a bump with no Invocation change is allowed",
           lint_persona(_BUMPED_PERSONA.replace("enforce rules with fixtures", "enforce rules with scripts"),
                        "framework-maintainer", _GOOD_PERSONA))
    expect("a committed copy from before the version rule constrains nothing",
           lint_persona(_GOOD_PERSONA, "framework-maintainer", _GOOD_PERSONA.replace("version: 1\n", "")))
    check("closeout: a persona dev-resources lacks is unpublished",
          (published_state(_GOOD_PERSONA, None) or ("",))[0] == "unpublished")
    check("closeout: a local version above the published one is unpublished",
          (published_state(_BUMPED_PERSONA, _GOOD_PERSONA) or ("",))[0] == "unpublished")
    check("closeout: published at the same version passes; behind locally is the sync's business, not a violation",
          published_state(_GOOD_PERSONA, _GOOD_PERSONA) is None and published_state(_GOOD_PERSONA, _BUMPED_PERSONA) is None)

    _, v = folder_state(["HANDOFF_S3.md", "KICKOFF_S3.md", "HANDOFF_S4.md", "KICKOFF_S4.md"])
    expect("two consecutive complete pairs pass", v)
    _, v = folder_state(["HANDOFF_S3.md", "KICKOFF_S3.md", "notes.md"])
    expect("a stray file fails", v, "stray")
    _, v = folder_state(["HANDOFF_S3.md"])
    expect("a handoff without its kickoff fails", v, "incomplete-pair")
    _, v = folder_state([f"{k}_S{n}.md" for n in (2, 3, 4) for k in ("HANDOFF", "KICKOFF")])
    expect("three session numbers fail", v, "too-many")
    _, v = folder_state([f"{k}_S{n}.md" for n in (2, 4) for k in ("HANDOFF", "KICKOFF")])
    expect("non-consecutive numbers fail", v, "gap")

    check("rotation archives everything older than the closing session",
          rotation_plan({1, 2, 3}, 3) == [1, 2] and rotation_plan({3, 4}, 3) == [])

    expect("verify: the produced pair present passes", verify_state(3, {3, 4}))
    expect("verify: only the produced pair passes", verify_state(3, {4}))
    expect("verify: no produced pair fails", verify_state(3, {3}), "not-closed")
    expect("verify: a fresh project passes", verify_state(1, set()))
    expect("closeout: a fresh project must still produce S2", verify_state(1, set(), closing=True), "not-closed")
    expect("verify: an empty folder past S1 fails", verify_state(2, set()), "no-pair")
    expect("verify: an unheaded sprint-status fails", verify_state(None, {2}), "status")
    expect("verify: a pair that should be archived fails", verify_state(3, {2, 3, 4}), "stale-pair")

    check("newest sprint-status session is read from the first H2", newest_session(_STATUS) == 3)
    check("a legacy heading yields no session",
          newest_session(_STATUS.replace("## S3 — 2026-09-21 — closeout", "## Session 3 Update")) is None)

    computed, declared, ids = tracker_counts(_TRACKER)
    expect("tracker: matching statistics pass; the [EXAMPLE] epic is skipped",
           tracker_violations(computed, declared))
    check("tracker: story IDs exclude the example epic", ids == {"TMPL-1.1", "TMPL-1.2"}, str(sorted(ids)))
    c2, d2, _ = tracker_counts(_TRACKER.replace("| **Completed** | 1 |", "| **Completed** | 0 |"))
    expect("tracker: a stale statistic fails", tracker_violations(c2, d2), "stats")
    c3, d3, _ = tracker_counts(_TRACKER.replace("| TMPL-1.2 | b | Not Started", "| TMPL-1.2 | b | Started"))
    expect("tracker: an unknown status value fails", tracker_violations(c3, d3), "status-value", "stats")

    stories = tracker_stories(_DEPS)
    by_id = {s.id: s for s in stories}
    check("dependencies: rows parse with every ID their Dependencies cell lists, and `—` lists none",
          len(stories) == 6 and by_id["TMPL-1.5"].deps == ("TMPL-1.1", "TMPL-1.6") and by_id["TMPL-1.1"].deps == (),
          str(stories))
    expect("dependencies: started stories on Done dependencies pass; waiting stories and the example epic "
           "are not judged", dependency_violations(stories))
    expect("dependencies: a Done story whose dependency is Not Started fails",
           dependency_violations(tracker_stories(_DEPS.replace("| Done | TMPL-1.1, TMPL-1.6 |", "| Done | TMPL-1.1, TMPL-1.3 |"))),
           "dependency-order")
    expect("dependencies: a Done story whose dependency is only In Progress fails",
           dependency_violations(tracker_stories(_DEPS.replace("| Done | TMPL-1.1, TMPL-1.6 |", "| Done | TMPL-1.2 |"))),
           "dependency-order")
    found = dependency_violations(tracker_stories(_DEPS.replace("| c | Not Started | TMPL-1.2 |", "| c | In Progress | TMPL-1.2 |")))
    check("dependencies: an In Progress story whose dependency is In Progress fails, and only it — the "
          "Blocked story behind it is waiting", len(found) == 1 and found[0][0] == "dependency-order"
          and "TMPL-1.3" in found[0][1], str(found))
    found = dependency_violations(tracker_stories(_DEPS.replace("| Done | TMPL-1.1, TMPL-1.6 |", "| Done | TMPL-9.9 |")))
    check("dependencies: a started story naming a dependency that is no story fails and says so",
          _rules(found) == {"dependency-order"} and "not a story" in found[0][1], str(found))

    expect("placeholders: the template — no profile — keeps every shape it ships", placeholder_violations(_LIVE, False))
    expect("placeholders: a fresh project with only the example epic passes",
           placeholder_violations(_live(tracker=_TRACKER.split("## Epic: TMPL-1")[0]), True))
    found = placeholder_violations(_LIVE, True)
    check("placeholders: once a real epic exists, the example epic's heading fails, named by file and line",
          [(r, w) for r, w, _ in found] == [("live-placeholder", "sprint/story-tracker.md:13")], str(found))
    clean = _TRACKER.replace(_EXAMPLE_EPIC, "")
    expect("placeholders: the same project with the example epic removed passes",
           placeholder_violations(_live(tracker=clean), True))
    found = placeholder_violations(_live(tracker=clean, status=_STATUS.replace("**Current Phase:** x", "**Last Updated:** {{DATE}}"),
                                         log=_LOG + "\n**Owner:** {{PROJECT_NAME}}\n"), True)
    check("placeholders: an unfilled token in sprint-status or the decision log fails, each named",
          sorted(w.split(":")[0] for _, w, _ in found) == ["sprint/decision-log.md", "sprint/sprint-status.md"]
          and all(r == "live-placeholder" for r, *_ in found), str(found))
    found = placeholder_violations(_live(tracker=clean, log=_LOG + "| [EXAMPLE] 2025-01-15-001 | 2025-01-15 | Sample | APPROVED |\n"
                                                                   "\n## Decision [EXAMPLE] 2025-01-15-001: Sample\n\nexample\n"), True)
    check("placeholders: the example decision's index row and its heading both fail",
          len(found) == 2 and {r for r, *_ in found} == {"live-placeholder"}, str(found))
    quoted = _STATUS + ("replace every `{{PLACEHOLDER}}` value and remove the `[EXAMPLE]` rows\n"
                        "| a row about `[EXAMPLE]` rows | `{{DATE}}` |\n")
    expect("placeholders: a token or marker quoted in inline code explains the convention and passes",
           placeholder_violations(_live(tracker=clean, status=quoted), True))
    expect("placeholders: a fenced block is quoted too",
           placeholder_violations(_live(tracker=clean, status=_STATUS + "```\n{{DATE}}\n| [EXAMPLE] |\n```\n"), True))
    expect("placeholders: a GitHub Actions expression is not a token",
           placeholder_violations(_live(tracker=clean, status=_STATUS + "run: ${{ secrets.TOKEN }}\n"), True))
    expect("placeholders: the marker in prose is a mention, not a row — only rows and headings are examples",
           placeholder_violations(_live(tracker=clean, status=_STATUS + "the [EXAMPLE] epic was removed in S2\n"), True))

    # These fixtures live in a file the tree pass scans, so every literal here is an allowed slug;
    # the dangling cases vary the allow argument instead.
    doc = "see [[reference_session_closeout]] and, with a label, [[reference_session_closeout|the gate]]\n"
    check("tree wikilinks: links that resolve pass, labelled or not", dangling_wikilinks(doc, _KB, set()) == [])
    check("tree wikilinks: a dangling link is found with its line",
          dangling_wikilinks("x\n" + doc + "then [[reference_nowhere]]\n", _KB, set()) == [(3, "reference_nowhere")])
    check("tree wikilinks: the convention's own placeholders and the fixture slug are allowed",
          dangling_wikilinks("`[[slug]]` → `[[<slug>]]`; [[other-slug]]; `[[wikilink]]`; [[reference_nowhere]]\n", _KB) == [])
    check("tree wikilinks: a padded link resolves once stripped, as the handoff linter reads it",
          dangling_wikilinks("[[ reference_session_closeout ]]\n", _KB, set()) == []
          and dangling_wikilinks("[[ reference_nowhere ]]\n", _KB, set()) == [(1, "reference_nowhere")])
    check("tree wikilinks: the allow set is exact — a near miss in it still leaves the link dangling",
          dangling_wikilinks("[[slug]]\n", _KB, {"slugs"}) == [(1, "slug")])
    check("tree wikilinks: an empty allow set makes the placeholders dangling, so the set is load-bearing",
          [s for _, s in dangling_wikilinks("[[slug]] [[reference_nowhere]]\n", _KB, set())] == ["slug", "reference_nowhere"])

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    if "--check" in argv:
        return cmd_check()
    if "--closeout" in argv:
        return cmd_closeout()
    if "--verify" in argv:
        return cmd_verify()
    if "--personas" in argv:
        return cmd_personas()
    if "--scaffold" in argv:
        slug = argv[argv.index("--persona") + 1] if "--persona" in argv and argv.index("--persona") + 1 < len(argv) else None
        return cmd_scaffold(slug)
    print(__doc__.split("Usage:")[1] if "Usage:" in __doc__ else "see --help", file=sys.stderr)
    return 2


def cli() -> int:
    """Console-script entry (pyproject.toml): the same main, over the process arguments."""
    return main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(cli())
