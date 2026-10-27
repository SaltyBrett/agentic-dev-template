#!/usr/bin/env python3
"""
session_closeout.py — a session ends with a verified handoff pair, and the pair lives one session.

WHAT IT CHECKS
--------------
--check     every commit
  * sprint/handoffs/ holds only HANDOFF_S<N>.md and KICKOFF_S<N>.md (plus archive/); at most two
    session numbers, consecutive; every number is a complete pair
  * each handoff and kickoff carries exactly the required H2 sections, in order, non-empty, with
    no unfilled {{TOKEN}}; wikilinks resolve; every decision ID cited is in a decision index
  * each kickoff names a persona in the roster and the version the roster holds, section 1 is the
    scaffold's line naming the agent, and every task cites a story ID present in
    sprint/story-tracker.md
  * each persona is an agent file, in the roster .claude/agents/<slug>.md or the library
    personas/<slug>.md, whose frontmatter parses as YAML (Claude Code skips the file silently
    otherwise) with name equal to the slug, description, an integer version, and expertise,
    insists_on and changelog as lists of strings; the body is the Invocation, the agent's prompt.
    Personas are append-only: a body that differs from the committed
    copy needs a higher version, the version never goes down, and the changelog carries an item
    for the current version
  * a roster persona the library also holds was activated from it by copy: a higher version than the library's is a fork, the same version with other
    text is drift, and both fail; a lower version is the library moving on, reported, never failed
  * sprint/sprint-status.md: newest entry headed `## S<N> - YYYY-MM-DD - title`; at most 10 entries
  * sprint/story-tracker.md Summary Statistics equal the counted rows ([EXAMPLE] epics skipped)
  * a story In Progress or Done whose listed dependency is not Done fails: the sprint standard's "never start a story whose dependencies are not Done"
  * in a project (a .template-version exists) whose tracker holds a non-example epic, an unfilled
    {{TOKEN}} in the tracker, sprint-status or the decision log fails; text quoted in inline or
    fenced code is the convention explaining itself, not a live placeholder. The template has no
    .template-version and is exempt. An [EXAMPLE] entry, numbered zero, stays in every log as its
    form
  * every [[slug]] in any text file git would commit resolves to docs/orchestration/knowledge/
    <slug>.md, with an allow set for the convention's own placeholders and the fixture slug
    the self-test uses; the handoff linter above proved it for handoffs alone
  * every unprefixed decision ID in those files outside sprint/ is in a decision index, a decision
    log's `**Deletes:**` line and an allow set of the fixtures' IDs excepted, so a deleted
    decision leaves no citation
  * no ID in that allow set is one an index holds, and no slug in the wikilink allow set names a
    knowledge entry: every check and the strip pass what the sets hold, so an invented name that
    became real would carry its citations into production unread
  * AGENTS.md is at most 32 KiB, the Codex project-doc cap
  * every .claude/rules/**/*.md is path-scoped judgement: its
    frontmatter parses with a `paths:` list, since Claude Code loads a rule without one, or whose
    YAML does not parse, in every session, a second brain beside AGENTS.md; at least one file git
    would commit matches it, or it never loads; and it repeats no sentence of AGENTS.md
--closeout  session end: archives every pair older than the session being closed, then verifies
            that the pair for the next session exists and passes every check above, and that the
            entry being closed is no longer an emergency checkpoint nor holds the initializer's
            `### Next`; on a pass clears the session journal and working
            notes (session_journal.py).
--verify    cold start: the verification of --closeout without the rotation, plus a clean tree.
            A fresh project — no pairs and sprint-status at S1 — passes.
--scaffold  writes the next session's HANDOFF/KICKOFF skeletons; they fail --check until filled
--self-test in-memory fixtures, run before the gate on every commit

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It cannot read prose, so it cannot prove a sentence in a handoff was not durable. The rotation is
the control for that: a fact left only in a handoff leaves the mandatory reads one session later.

Usage:  pre-commit run session-closeout-check --all-files
        pre-commit run session-closeout --hook-stage manual --all-files   (see CLOSEOUT_COMMAND)
        pre-commit run session-verify --hook-stage manual --all-files   (see VERIFY_COMMAND)
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
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_freshness_scan  # noqa: E402 — the decision-index parser, not its main()
import session_journal    # noqa: E402 — the closeout clears the journal and the working notes


def repo_root() -> Path:
    """The repository under judgement: the git top level of the working directory, where
    pre-commit runs every hook and the documented direct invocations run too. Outside a
    repository the working directory itself is judged, and the checks then fail on what is missing
    rather than pass on a tree that is not there.
    """
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False)
    top = out.stdout.strip()
    return Path(top) if out.returncode == 0 and top else Path.cwd()


ROOT = repo_root()
HANDOFFS = ROOT / "sprint" / "handoffs"
ARCHIVE = HANDOFFS / "archive"
PERSONAS = ROOT / ".claude" / "agents"   # the roster: the personas this project activated, one agent file each
LIBRARY = ROOT / "personas"              # the library the template ships, inactive
STATUS = ROOT / "sprint" / "sprint-status.md"
TRACKER = ROOT / "sprint" / "story-tracker.md"
LOG = ROOT / "sprint" / "decision-log.md"
# Every decision log the tree holds, read as one set, an ID in two refused.
DECISION_LOGS = {"sprint/decision-log.md": LOG}
KB = ROOT / "docs" / "orchestration" / "knowledge"
BRAIN = ROOT / "AGENTS.md"
RULES = ROOT / ".claude" / "rules"     # path-scoped judgement Claude Code loads beside a matching file
STAMP = ROOT / ".template-version"              # present in a project, absent in the template
# The three sprint documents the live-placeholder rule reads, by the path the report names.
SPRINT_FILES = {"sprint/story-tracker.md": TRACKER, "sprint/sprint-status.md": STATUS, "sprint/decision-log.md": LOG}

HANDOFF_NAME = re.compile(r"^HANDOFF_S(\d+)\.md$")
KICKOFF_NAME = re.compile(r"^KICKOFF_S(\d+)\.md$")
# The formats the gates read are written and read with a hyphen, and with nothing else.
SEP = " - "
STATUS_ENTRY = re.compile(r"^## S(\d+) - \d{4}-\d{2}-\d{2} - \S.*$")
STORY_ID = re.compile(r"\b([A-Z][A-Z0-9]*-\d+\.\d+)\b")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
TOKEN = re.compile(r"(?<!\$)\{\{\s*[^}]+?\s*\}\}")
INLINE_CODE = re.compile(r"`[^`\n]*`")
EXAMPLE_MARK = "[EXAMPLE]"
# Wikilinks that resolve to no entry and are not a defect: the convention's own placeholders
# (`[[slug]]`, `[[<slug>]]`, `[[other-slug]]`, `[[wikilink]]` in the documents that explain it,
# `[[{slug}]]` in this gate's own message) and the slugs the self-test fixtures use. Anything
# else that does not resolve blocks the commit, and so does a slug here that names an entry, since
# the strip and its checks would pass every link to it. Adding a fixture slug means adding it here.
WIKILINK_ALLOW = {"slug", "<slug>", "other-slug", "wikilink", "{slug}", "reference_nowhere", "reference_fixture"}
WIKILINK_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".toml"}
# A decision ID with no prefix. A project prefixes its own (`ACME-2026-09-24-001`), so a
# prefixed ID is a project's or an example and is not read by the citation rule.
DECISION_ID = re.compile(r"(?<![\w-])(\d{4}-\d{2}-\d{2}-\d{3})(?![\w-])")
# The one place a deleted decision's ID stands: a `**Deletes:**` line in a decision log.
DELETES_LINE = re.compile(r"^\*\*Deletes:\*\*")
# Decision IDs no index holds that are not a defect: the [EXAMPLE] row's and those the self-test
# fixtures invent. Anything else unindexed blocks the commit, and so does an ID here that an index
# holds, since every check and the strip pass what this set holds. Adding
# a fixture ID means adding it here, numbered 900 or above, a number no day's decisions reach.
DECISION_ALLOW = {"2025-01-15-001", "2026-01-02-003", "2026-01-02-004", "2026-01-01-999", "2026-09-21-099", "2026-10-21-001",
                  "2026-10-25-901", "2026-10-26-909",
                  # the authority gate's fixture decisions, dated as the rules they test need
                  "2026-10-22-902", "2026-10-23-910", "2026-10-24-901",
                  "2026-09-21-901",   # this gate's own fixture decision
                  "2026-09-20-901", "2026-09-20-903", "2026-09-20-904"}   # the freshness gate's
ALLOW_SETS_AT = "scripts/session_closeout.py"   # where a violation of the allow-set rule is fixed
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
PERSONA_KEYS = ["name", "description", "version", "expertise", "insists_on", "changelog"]
# Lists of strings. An unquoted item holding `: ` is a YAML mapping, not a string, so it fails.
PERSONA_LISTS = ("expertise", "insists_on", "changelog")
# A changelog item opens with the version it records: `2 - 2026-09-24 - what changed`.
CHANGELOG_ENTRY = re.compile(r"^(\d+) - ")


class Persona(NamedTuple):
    """What a kickoff checks against the roster: the Invocation (the agent's prompt), its version, and
    the versions it has held, any of which a kickoff written against it may name."""
    invocation: str
    version: str
    held: tuple[str, ...]
STATUSES = ("Not Started", "In Progress", "Blocked", "Done")
STARTED = ("In Progress", "Done")   # a story in one of these has begun, so its dependencies were due
MAX_STATUS_ENTRIES = 10
MAX_BRAIN_BYTES = 32 * 1024
MIN_SENTENCE_WORDS = 6   # shorter shared phrases ("run the gate suite") are vocabulary, not a restatement
NONE_MARKERS = {"none", "none."}
# `--all-files` is load-bearing: without it pre-commit stashes unstaged changes to tracked files
# before running the hook, and the gate then judges the last commit's sprint-status and tracker
# rather than the ones just edited. The hook takes no filenames,
# so the flag changes nothing but the stash.
CLOSEOUT_COMMAND = "pre-commit run session-closeout --hook-stage manual --all-files"
# The same flag for the cold start, for a sharper reason: under the stash an unstaged edit to a
# tracked file vanishes, so the dirty-tree rule passes a tree that is dirty.
VERIFY_COMMAND = "pre-commit run session-verify --hook-stage manual --all-files"


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
    title = f"# {kind}{SEP}S{n}"
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
        v.append(("persona", f"`**Persona:** {slug}` is not in the roster; activate it from personas/ with the "
                             f"team-selection skill, or draft .claude/agents/{slug}.md in the same commit"))
    else:
        # The agent file is the source and the start hook injects it, so section 1 names the agent
        # and nothing else.
        if norm(secs.get(KICKOFF_SECTIONS[0], "")) != norm(persona_line(slug)):
            v.append(("persona-agent", f"section 1 must be the scaffold's line naming the agent: "
                                       f"`{persona_line(slug)}`"))
        # A kickoff says which version it was written against, and the closeout keeps the last two
        # live, so one written before a bump names an older version.
        version, persona = field(text, "Persona version"), personas[slug]
        if version not in persona.held:
            v.append(("persona-version", f"`**Persona version:** {version}` must name a version {slug} has held "
                                         f"by the roster's changelog ({', '.join(persona.held) or 'none'}); the "
                                         f"scaffold writes the current one, {persona.version or 'none'}"))
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


def persona_line(slug: str) -> str:
    """A kickoff's section 1: the agent it names, and how the session comes to hold its prompt."""
    return (f"Run as the `{slug}` agent, `.claude/agents/{slug}.md`. The `SessionStart` hook injects its "
            f"prompt as context unless the session already runs as that agent (`claude --agent {slug}`).")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """(frontmatter source, body), or (None, '') when the file opens with no terminated block.
    Splits only; it parses nothing, so the session hook can read a body without PyYAML."""
    if not text.startswith("---\n"):
        return None, ""
    end = text.find("\n---", 3)
    if end == -1:
        return None, ""
    return text[4:end], text[end + 4:]


def persona_frontmatter(text: str) -> tuple[dict | None, str]:
    """(keys, body), or (None, '') when the frontmatter is absent, unterminated, or not a YAML
    mapping. Claude Code skips such an agent file without a word, so the linter must refuse it,
    and only a parser can say which it is (a regex read the old flat keys; lists are YAML).

    PyYAML is imported here rather than at the top: session_start.py imports this module for its
    parsers under whatever python3 the operator has, and only the persona rules need YAML."""
    import yaml
    fm, body = split_frontmatter(text)
    if fm is None:
        return None, ""
    try:
        keys = yaml.safe_load(fm)
    except yaml.YAMLError:
        return None, ""
    return (keys, body) if isinstance(keys, dict) else (None, "")


def positive_int(value: object) -> bool:
    return type(value) is int and value > 0   # `type`, not isinstance: YAML's `true` is a bool, an int subclass


def lint_persona(text: str, slug: str, previous: str | None = None) -> list:
    """`previous` is the committed copy (git HEAD), or None for a new persona.

    Personas are append-only: the Invocation, which is the agent file's
    body and so its prompt, is never changed in place. A change to it needs a higher `version:` and
    a changelog item for that version. A bump with no change to the body is allowed: expertise and
    insists_on may be enhanced too, and a bump that records nothing costs a line. The version never
    decreases. A committed copy with no valid `version:` gives no baseline, as a new file gives none,
    whatever its origin; the working copy is still held to every shape rule, so its repair passes.
    """
    v: list[tuple[str, str]] = []
    keys, body = persona_frontmatter(text)
    if keys is None:
        return [("frontmatter", "an agent file opens with a --- frontmatter block that parses as a YAML mapping; "
                                "Claude Code skips the file without a word otherwise")]
    for k in PERSONA_KEYS:
        if keys.get(k) in (None, "", []):
            v.append(("frontmatter", f"missing `{k}:`"))
    if keys.get("name") != slug:
        v.append(("name", f"`name: {slug}` must equal the filename stem, found {keys.get('name')!r}; "
                          "Claude Code knows an agent by its name, and hooks receive it as agent_type"))
    version = keys.get("version")
    if version is not None and not positive_int(version):
        v.append(("version", f"`version: {version}` must be a positive integer; the first release is 1"))
        version = None
    for k in PERSONA_LISTS:
        items = keys.get(k)
        if items not in (None, "", []) and not (isinstance(items, list) and all(isinstance(i, str) and i.strip() for i in items)):
            v.append(("list", f"`{k}:` must be a YAML list of strings; quote an item holding `: `, "
                              "which YAML reads as a mapping"))
    if not norm(body):
        v.append(("prompt", "the body is empty; it is the Invocation, the agent's prompt"))
    if version and isinstance(keys.get("changelog"), list):   # a missing or malformed list is reported above
        logged = {m.group(1) for m in (CHANGELOG_ENTRY.match(i) for i in keys["changelog"] if isinstance(i, str)) if m}
        if str(version) not in logged:
            v.append(("changelog", f"the changelog has no item for version {version}; append "
                                   f"`{version}{SEP}<date>{SEP}<what changed>`"))
    if previous is not None and version:
        prev_keys, prev_body = persona_frontmatter(previous)
        prev_version = (prev_keys or {}).get("version")
        if positive_int(prev_version):
            if version < prev_version:
                v.append(("version-order", f"`version: {version}` is below the committed {prev_version}; "
                                           "a version never goes down"))
            elif version == prev_version and norm(body) != norm(prev_body):
                v.append(("invocation-unbumped", f"the body (the Invocation) differs from the committed copy at "
                                                 f"version {prev_version}; a persona is append-only — bump "
                                                 "`version:` and add the changelog item, never edit in place"))
    return v


def persona_invocation(text: str) -> str:
    return split_frontmatter(text)[1].strip()


def persona_version(text: str) -> str:
    keys, _ = persona_frontmatter(text)
    version = (keys or {}).get("version")
    return str(version) if positive_int(version) else ""


def persona_of(text: str) -> Persona:
    return Persona(persona_invocation(text), persona_version(text), held_versions(text))


def held_versions(text: str) -> tuple[str, ...]:
    """The versions a persona has held: its own, and each its changelog records below it."""
    version = persona_version(text)
    if not version:
        return ()
    items = (persona_frontmatter(text)[0] or {}).get("changelog")
    logged = {m.group(1) for m in (CHANGELOG_ENTRY.match(i) for i in items if isinstance(i, str)) if m} if isinstance(items, list) else set()
    return tuple(sorted({version} | {v for v in logged if int(v) <= int(version)}, key=int))


def expand_braces(pattern: str) -> list[str]:
    """`src/*.{ts,tsx}` -> both patterns, innermost group first, as Claude Code expands `paths:`."""
    m = re.search(r"\{([^{}]*)\}", pattern)
    if not m:
        return [pattern]
    return [p for alt in m.group(1).split(",") for p in expand_braces(pattern[:m.start()] + alt + pattern[m.end():])]


def glob_regex(pattern: str) -> re.Pattern:
    """A brace-free `paths:` glob, relative to the project root: `**/` is any run of directories
    (none included), `**` anything, `*` and `?` stay within one path segment."""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        else:
            out.append({"*": "[^/]*", "?": "[^/]"}.get(pattern[i], re.escape(pattern[i])))
            i += 1
    return re.compile("".join(out) + r"\Z")


def words(text: str) -> str:
    """Lower-cased words, punctuation and markdown dropped, one space apart."""
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", text.lower()).split())


def sentences(text: str) -> set[str]:
    """Normalized sentences of MIN_SENTENCE_WORDS or more, split at sentence ends, list items,
    headings and blank lines."""
    chunks = re.split(r"(?<=[.!?])\s+|\n\s*\n|\n\s*(?:[-*>]|\d+\.|#+)\s", "\n" + text)
    return {w for w in map(words, chunks) if len(w.split()) >= MIN_SENTENCE_WORDS}


def restatements(text: str, brain: str) -> set[str]:
    """Sentences of one found whole inside the other, either way: a rule sentence that is a clause
    of AGENTS.md (observed in the live probe: equality alone let a copied clause through), or a
    sentence of AGENTS.md carried inside a longer rule sentence."""
    t, b = f" {words(text)} ", f" {words(brain)} "
    return {s for s in sentences(text) if f" {s} " in b} | {s for s in sentences(brain) if f" {s} " in t}


def lint_rule(text: str, files: list[str], brain: str) -> list:
    """A rule under .claude/rules/ against the files git would commit and the text of AGENTS.md."""
    v: list[tuple[str, str]] = []
    fm, body = split_frontmatter(text)
    paths = None
    if fm is not None:
        import yaml   # lazily, as persona_frontmatter does
        try:
            keys = yaml.safe_load(fm)
        except yaml.YAMLError:
            keys = None
        paths = keys.get("paths") if isinstance(keys, dict) else None
        if isinstance(paths, str):
            paths = [p.strip() for p in paths.split(",") if p.strip()]
    if not (isinstance(paths, list) and paths and all(isinstance(p, str) and p.strip() for p in paths)):
        v.append(("rule-paths", "a rule here opens with a --- block whose `paths:` parses as a list of globs; "
                                "Claude Code loads a rule without one, or whose YAML does not parse, in every "
                                "session, and always-loaded text belongs in AGENTS.md"))
    else:
        regs = [glob_regex(x) for p in paths for x in expand_braces(p)]
        if not any(r.match(f) for f in files for r in regs):
            v.append(("rule-dead", f"no file git would commit matches {paths}, so the rule never loads"))
    for s in sorted(restatements(body if fm is not None else text, brain)):
        v.append(("rule-restates", f"repeats a sentence of AGENTS.md: `{s[:90]}`; a fact has one home"))
    return v


# Reported beside a verdict, never a violation: the library moved on and the roster may follow.
NOTE_RULES = {"library-newer"}


def library_state(roster: str, library: str) -> tuple[str, str] | None:
    """One roster persona against its copy in the library. Activation is
    a copy, so the same version must be the same file. A higher roster version is a fork of a
    library persona, which a project writes as a persona of its own under its own slug instead; a
    lower one is the library moving on, reported for the team-selection skill to re-activate."""
    rv, lv = persona_version(roster), persona_version(library)
    if not (rv.isdigit() and lv.isdigit()):
        return None   # a malformed version is lint_persona's to report
    if int(rv) > int(lv):
        return ("library-fork", f"version {rv} here, {lv} in personas/; a library persona changes in the library — "
                                "write the variant as the project's own persona, under its own slug")
    if int(rv) == int(lv) and roster != library:   # .gitattributes checks out LF everywhere
        return ("library-drift", f"differs from personas/ at the same version {rv}; activation is a copy — "
                                 "activate it again from the library with the team-selection skill")
    if int(rv) < int(lv):
        return ("library-newer", f"the library holds version {lv}, the roster {rv}; activate it again with the "
                                 "team-selection skill to take the newer text")
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
        return [("status", "newest sprint-status entry must be headed `## S<N> - YYYY-MM-DD - title`")]
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


def unfinished_entry(text: str) -> list[tuple[str, str]]:
    """What the closeout refuses in the entry it closes: a heading still
    the emergency checkpoint's, whose Status says the closeout was not completed, or the
    initializer's `### Next`, which stands in for S1's kickoff only until S1 closes out. Passed,
    either closes the session on a record saying it is still open. Read at the closeout alone: at a
    cold start the emergency entry is the true record."""
    _, secs = sections(text)
    m = STATUS_ENTRY.match(f"## {secs[0][0]}") if secs else None
    if not m:
        return []   # the `status` rule reports an unreadable heading
    heading, body = secs[0]
    v: list[tuple[str, str]] = []
    if norm(heading.split(SEP, 2)[-1]).lower().startswith("emergency checkpoint"):
        v.append(("emergency-entry", f"S{m.group(1)}'s entry is still the emergency checkpoint. Rewrite its "
                                     "heading and Status for what the session did, then close out"))
    fenced = False
    for line in body.splitlines():
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced and norm(line) == "### Next":
            v.append(("next-section", f"S{m.group(1)}'s entry holds the initializer's `### Next`, which stands "
                                      "in for S1's kickoff only until S1 closes out. Remove it; the next "
                                      "session's tasks go in its kickoff"))
            break
    return v


def current_session(text: str, has_kickoff: Callable[[int], bool]) -> int | None:
    """The session at work, from sprint-status and the pairs: the newest entry, plus one when the
    next session's kickoff exists, as at a cold start before the session writes its own entry. The
    start hook and the doc-queue gate read this one rule."""
    newest = newest_session(text)
    if newest is None:
        return None
    return newest + 1 if has_kickoff(newest + 1) else newest


class Story(NamedTuple):
    """One row of a non-example epic: its ID, its Status cell, the story IDs its Dependencies
    cell lists (`—` lists none), and the row itself, which the authority gate reads for the
    decision and the document a story cites."""
    id: str
    status: str
    deps: tuple[str, ...]
    row: str = ""


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
            out.append(Story(cells[0], cells[2], deps, line))
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
    is what the rule asks of them."""
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
    """(line, what) for every unfilled {{TOKEN}}, read outside fenced blocks and inline code: a
    document that writes `{{PLACEHOLDER}}` in a code span is explaining the convention, and a GitHub
    Actions `${{ }}` is not a token. An [EXAMPLE] entry is no placeholder: numbered zero, it stays
    as the form each log is filled from."""
    found: list[tuple[int, str]] = []
    fenced = False
    for no, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        for m in TOKEN.finditer(INLINE_CODE.sub("", line)):
            found.append((no, f"unfilled token {m.group(0)}"))
    return found


def placeholder_violations(texts: dict[str, str], project: bool) -> list:
    """The sprint standard's section 11 rule, "no {{PLACEHOLDER}} content in a live sprint", over
    the three sprint documents keyed by path. It applies in a project (`project`: a
    .template-version exists) whose tracker holds a non-example epic: the template keeps every
    token it ships, and a fresh project fills the rest at its planning session. Returns (rule, where, detail)."""
    if not project or not real_epics(texts.get("sprint/story-tracker.md", "")):
        return []
    v: list[tuple[str, str, str]] = []
    for rel, text in texts.items():
        for no, what in live_placeholders(text):
            v.append(("live-placeholder", f"{rel}:{no}",
                      f"{what} in a live sprint; the tracker holds a real epic, so every placeholder "
                      "token is filled (sprint standard section 11)"))
    return v


# ==============================================================================
# Scaffolds — the agent never hand-types headings
# ==============================================================================

def handoff_skeleton(n: int, date: str) -> str:
    return f"""# Handoff{SEP}S{n}

**For session:** S{n}
**Written by:** S{n - 1}
**Written:** {date}

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S{n}.md`
- {{{{FILL: task-specific files, one per bullet, with why}}}}

## 2. Completed last session

- {{{{FILL: what was done, by story ID and file}}}}

## 3. In progress

- {{{{FILL: each In Progress story with its exact state, or None.}}}}

## 4. Decisions logged

- {{{{FILL: each decision ID the session logged, with its title, or None.}}}}

## 5. Blockers and open questions

- {{{{FILL: blockers and open questions, or None.}}}}

## 6. Verification observed

- {{{{FILL: which gates ran and their exit codes}}}}
"""


def kickoff_skeleton(n: int, slug: str, persona: Persona) -> str:
    return f"""# Kickoff{SEP}S{n}

**For session:** S{n}
**Persona:** {slug}
**Persona version:** {persona.version}

## 1. Persona

{persona_line(slug)}

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S{n}.md`, then the files it lists.
Run `{VERIFY_COMMAND}` and do no build work until it passes.

## 3. Tasks

- {{{{FILL: STORY-ID: what to do, in dependency order}}}}

## 4. Success criteria

- {{{{FILL: the executable checks that prove each task done}}}}

## 5. Closeout

Before ending: commit the `## S{n}{SEP}<date>{SEP}<title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S{n + 1}.
It writes and fills the pair for S{n + 1}, runs `{CLOSEOUT_COMMAND}`, commits
`checkpoint: closeout S{n}`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S{n + 1}.md`, whose contents go to the user as the next session's prompt.
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
    except kb_freshness_scan.DecisionIndexError as e:
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
        personas[p.stem] = persona_of(text)
    return personas, v


def library_findings() -> tuple[list, list]:
    """(violations, notes): every library persona linted as a roster persona is, append-only
    against its committed copy, then every roster persona the library holds against its copy."""
    v: list[tuple[str, str, str]] = []
    notes: list[tuple[str, str, str]] = []
    if not LIBRARY.is_dir():
        return v, notes
    library: dict[str, str] = {}
    for p in sorted(LIBRARY.glob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        for rule, detail in lint_persona(text, p.stem, committed_text(rel)):
            v.append((rule, rel, detail))
        library[p.stem] = text
    if PERSONAS.is_dir():
        for p in sorted(PERSONAS.glob("*.md")):
            if p.stem in library:
                state = library_state(p.read_text(encoding="utf-8"), library[p.stem])
                if state:
                    (notes if state[0] in NOTE_RULES else v).append((state[0], p.relative_to(ROOT).as_posix(), state[1]))
    return v, notes


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


def unindexed_citations(text: str, ids: set[str], allow: set[str] = DECISION_ALLOW,
                        log: bool = False) -> list[tuple[int, str]]:
    """(line, ID) for every unprefixed decision ID that no index holds and is not allowed. In a
    decision log, a `**Deletes:**` line is the record of the IDs a decision deleted and is not read.
    Pure over text, so the self-test needs no files."""
    found: list[tuple[int, str]] = []
    for no, line in enumerate(text.splitlines(), 1):
        if log and DELETES_LINE.match(line):
            continue
        found.extend((no, did) for did in DECISION_ID.findall(line) if did not in ids and did not in allow)
    return found


def tree_citation_violations(ids: set[str]) -> list:
    """The citation rule over the files the wikilink rule reads, outside `sprint/`, where the records
    keep the IDs of their day."""
    v: list[tuple[str, str, str]] = []
    for rel in committed_files():
        path = ROOT / rel
        if rel.startswith("sprint/") or path.suffix not in WIKILINK_SUFFIXES or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for no, did in unindexed_citations(text, ids, log=rel in DECISION_LOGS):
            v.append(("decision-citation", f"{rel}:{no}",
                      f"{did} is in no decision index: cite the decision that holds the rule now, or "
                      "(an ID a fixture invents) add it to DECISION_ALLOW"))
    return v


def allow_set_violations(ids: set[str], kb_slugs: set[str], decisions: set[str] = DECISION_ALLOW,
                         slugs: set[str] = WIKILINK_ALLOW) -> list:
    """An invented name that became real: an allow-set decision ID an index holds, or an allow-set
    slug naming a knowledge entry. Every citation check and the strip pass what the allow sets hold,
    so each citation of it would go unread into production."""
    v = [("allow-set", ALLOW_SETS_AT, f"{did} is a real decision and in DECISION_ALLOW: move the fixtures "
          "citing it to an invented ID numbered 900 or above, and that ID into the set") for did in sorted(decisions & ids)]
    v += [("allow-set", ALLOW_SETS_AT, f"[[{slug}]] is a knowledge entry and in WIKILINK_ALLOW: move the fixtures "
           "linking it to a slug no entry has, and that slug into the set") for slug in sorted(slugs & kb_slugs)]
    return v


def folder_names() -> list[str]:
    if not HANDOFFS.is_dir():
        return []
    return sorted(p.name for p in HANDOFFS.iterdir() if p.name != "archive" and not p.name.startswith("."))


def check_all() -> tuple[list, dict[int, set[str]], int | None, list]:
    """Every --check rule over the real tree. Returns (violations, pair numbers, newest session,
    notes), the notes reported beside the verdict and never counted in it."""
    v: list[tuple[str, str, str]] = []
    ids, log_v = decision_ids()
    v.extend(log_v)
    kb_slugs = {p.stem for p in KB.glob("*.md")} if KB.is_dir() else set()
    personas, persona_v = load_personas()
    v.extend(persona_v)
    library_v, notes = library_findings()
    v.extend(library_v)

    story_ids: set[str] = set()
    if TRACKER.is_file():
        tracker_text = TRACKER.read_text(encoding="utf-8")
        computed, declared, story_ids = tracker_counts(tracker_text)
        for rule, detail in tracker_violations(computed, declared) + dependency_violations(tracker_stories(tracker_text)):
            v.append((rule, "sprint/story-tracker.md", detail))
        texts = {rel: p.read_text(encoding="utf-8") for rel, p in SPRINT_FILES.items() if p.is_file()}
        v.extend(placeholder_violations(texts, STAMP.is_file()))

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
    if not log_v:   # with an index unread, every citation would read as dangling
        v.extend(tree_citation_violations(ids))
    v.extend(allow_set_violations(ids, kb_slugs))

    current: int | None = None
    if STATUS.is_file():
        text = STATUS.read_text(encoding="utf-8")
        current = newest_session(text)
        if current is None:
            v.append(("status", "sprint/sprint-status.md",
                      "newest entry must be headed `## S<N> - YYYY-MM-DD - title`"))
        count = len(status_headings(text))
        if count > MAX_STATUS_ENTRIES:
            v.append(("status-cap", "sprint/sprint-status.md",
                      f"{count} entries; keep at most {MAX_STATUS_ENTRIES} — move the oldest to "
                      "sprint/archive/sprint-status_<year>.md"))

    if RULES.is_dir():
        files = committed_files()
        brain = BRAIN.read_text(encoding="utf-8") if BRAIN.is_file() else ""
        for p in sorted(RULES.rglob("*.md")):
            for rule, detail in lint_rule(p.read_text(encoding="utf-8"), files, brain):
                v.append((rule, p.relative_to(ROOT).as_posix(), detail))

    if BRAIN.is_file():
        size = BRAIN.stat().st_size
        if size > MAX_BRAIN_BYTES:
            v.append(("brain-cap", "AGENTS.md",
                      f"{size} bytes; the Codex project-doc cap is {MAX_BRAIN_BYTES}. Move procedure "
                      "to docs/standards/ and keep only nouns and non-inferable constraints here"))
    return v, nums, current, notes


def report(title: str, violations: list, notes: list | None = None) -> int:
    print(f"\n{title}")
    print("=" * 60)
    for rule, where, detail in notes or []:
        print(f"  note  {where} ({rule}): {detail}")
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
    v, _, _, notes = check_all()
    return report("Session State Gate", v, notes)


def cmd_closeout() -> int:
    v, nums, current, notes = check_all()
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
    if STATUS.is_file():
        for rule, detail in unfinished_entry(STATUS.read_text(encoding="utf-8")):
            v.append((rule, "sprint/sprint-status.md", detail))
    rc = report(f"Session Closeout (closing S{current})" if current else "Session Closeout", v, notes)
    if rc == 0:
        for rel in session_journal.clear(ROOT):
            print(f"cleared   {rel}")
        print(f"\nCommit as `checkpoint: closeout S{current}`. The next session starts from "
              f"KICKOFF_S{current + 1}.md.")
    return rc


def cmd_verify() -> int:
    v, nums, current, notes = check_all()
    for rule, detail in verify_state(current, set(nums)):
        v.append((rule, "sprint/handoffs/", detail))
    dirty = git_dirty()
    if dirty:
        v.append(("dirty-tree", "git status", f"{len(dirty)} uncommitted path(s); the previous session "
                                              "must have committed its closeout"))
    rc = report("Session Verify (previous session closed out)", v, notes)
    if rc == 0 and current is not None:
        nxt = current + 1 if nums else current
        print(f"\nThis is S{nxt}. Add `## S{nxt}{SEP}<date>{SEP}<title>` to sprint-status at the first checkpoint.")
    return rc


def cmd_scaffold(slug: str | None) -> int:
    if not STATUS.is_file():
        print("session_closeout: no sprint/sprint-status.md", file=sys.stderr)
        return 2
    current = newest_session(STATUS.read_text(encoding="utf-8"))
    if current is None:
        print("session_closeout: newest sprint-status entry must be `## S<N> - YYYY-MM-DD - title` "
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

_IDS = {"2026-09-21-901"}
_KB = {"reference_fixture"}
_INVOCATION = "You are a senior platform engineer. You enforce rules with scripts."
_PERSONAS = {"framework-maintainer": Persona(_INVOCATION, "1", ("1",))}
_STORIES = {"ACME-1.2", "ACME-1.3"}


def _good_handoff() -> str:
    t = handoff_skeleton(2, "2026-09-21")
    t = t.replace("- {{FILL: task-specific files, one per bullet, with why}}",
                  "- [[reference_fixture]] — the gate this session extends")
    t = t.replace("- {{FILL: what was done, by story ID and file}}", "- ACME-1.2 shipped `scripts/session_closeout.py`")
    t = t.replace("- {{FILL: which gates ran and their exit codes}}", "- `pre-commit run --all-files` exit 0")
    t = t.replace("- {{FILL: each In Progress story with its exact state, or None.}}", "- None.")
    t = t.replace("- {{FILL: blockers and open questions, or None.}}", "- None.")
    return t.replace("- {{FILL: each decision ID the session logged, with its title, or None.}}", "- 2026-09-21-901 closeout gate")


def _good_kickoff() -> str:
    t = kickoff_skeleton(2, "framework-maintainer", _PERSONAS["framework-maintainer"])
    t = t.replace("- {{FILL: STORY-ID: what to do, in dependency order}}", "- ACME-1.3 write the persona seeds")
    return t.replace("- {{FILL: the executable checks that prove each task done}}", "- self-test exit 0")


_GOOD_PERSONA = ("---\nname: framework-maintainer\ndescription: builds gates\nversion: 1\n"
                 "expertise:\n  - gates\ninsists_on:\n  - proof\nchangelog:\n  - 1 - 2026-09-21 - seeded\n---\n\n"
                 f"{_INVOCATION}\n")
_BUMPED_PERSONA = (_GOOD_PERSONA.replace("version: 1", "version: 2")
                   .replace("enforce rules with scripts", "enforce rules with fixtures")
                   .replace("  - 1 - 2026-09-21 - seeded\n", "  - 1 - 2026-09-21 - seeded\n  - 2 - 2026-09-24 - fixtures\n"))
# The pre-005 shape: sections in the body, flat keys. It must fail as an agent file.
_OLD_SHAPE = ("---\nname: Framework maintainer\nslug: framework-maintainer\ndescription: builds gates\nversion: 1\n---\n\n"
              "# Framework maintainer\n\n## Expertise\n\n- gates\n\n## Insists on\n\n- proof\n\n"
              f"## Invocation\n\n{_INVOCATION}\n\n## Changelog\n\n- 1 - 2026-09-21 - seeded\n")

_TRACKER = ("# Story Tracker\n\n## Summary Statistics\n\n| Metric | Count |\n|---|---|\n"
            "| **Total Stories** | 2 |\n| **Not Started** | 1 |\n| **In Progress** | 0 |\n"
            "| **Blocked** | 0 |\n| **Completed** | 1 |\n\n"
            "## Epic: INFRA-1 - Setup [EXAMPLE]\n\n| Story ID | Title | Status | D | S | P |\n|---|---|---|---|---|---|\n"
            "| INFRA-1.1 | x | Not Started | — | — | — |\n\n"
            "## Epic: ACME-1 - Closeout\n\n| Story ID | Title | Status | D | S | P |\n|---|---|---|---|---|---|\n"
            "| ACME-1.1 | a | Done | — | — | — |\n| ACME-1.2 | b | Not Started | — | — | — |\n")

_STATUS = "# Sprint Status\n\n**Current Phase:** x\n\n---\n\n## S3 - 2026-09-21 - closeout\n\ntext\n\n## S2 - 2026-09-20 - older\n\ntext\n"

# Dependencies in every shape the rule must tell apart. The example epic's row is In Progress on a
# story that exists nowhere, so a variant that judged example rows fails the passing case.
_DEPS = ("## Epic: INFRA-1 - Setup [EXAMPLE]\n\n| Story ID | Title | Status | Dependencies | S | P |\n|---|---|---|---|---|---|\n"
         "| INFRA-1.2 | x | In Progress | INFRA-1.1 | — | — |\n\n"
         "## Epic: ACME-1 - Closeout\n\n| Story ID | Title | Status | Dependencies | S | P |\n|---|---|---|---|---|---|\n"
         "| ACME-1.1 | a | Done | — | — | — |\n"
         "| ACME-1.2 | b | In Progress | ACME-1.1 | — | — |\n"
         "| ACME-1.3 | c | Not Started | ACME-1.2 | — | — |\n"
         "| ACME-1.4 | d | Blocked | ACME-1.3 | — | — |\n"
         "| ACME-1.5 | e | Done | ACME-1.1, ACME-1.6 | — | — |\n"
         "| ACME-1.6 | f | Done | — | — | — |\n")

_EXAMPLE_EPIC = ("## Epic: INFRA-1 - Setup [EXAMPLE]\n\n| Story ID | Title | Status | D | S | P |\n|---|---|---|---|---|---|\n"
                 "| INFRA-1.1 | x | Not Started | — | — | — |\n\n")
_LOG = ("# Log\n\n## Decision Index\n\n| ID | Date | Title | Status |\n|---|---|---|---|\n"
        "| 2026-09-21-901 | 2026-09-21 | closeout | APPROVED |\n")
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
    expect("an unfilled scaffold fails on its tokens, section 4's as no decision ID too",
           lint_handoff(handoff_skeleton(2, "2026-09-21"), 2, _IDS, _KB), "unfilled-token", "decision-id")
    # A section the scaffold pre-filled with `- None.` passed unwritten: the S6 probe's closeout
    # found section 4 saying None beside the decision its session had logged.
    _, scaffold = sections(handoff_skeleton(2, "2026-09-21"))
    check("the scaffold leaves every handoff section after the first read as a token to fill",
          all(TOKEN.search(body) for head, body in scaffold if head != HANDOFF_SECTIONS[0]),
          str([head for head, body in scaffold if not TOKEN.search(body)]))
    expect("a missing section fails", lint_handoff(h.replace("## 3. In progress\n\n- None.\n", ""), 2, _IDS, _KB),
           "sections")
    expect("an extra section is refused — durable content has no home here",
           lint_handoff(h + "\n## 7. Rules to remember\n\n- never do X\n", 2, _IDS, _KB), "sections")
    expect("filename and For-session must agree", lint_handoff(h, 3, _IDS, _KB),
           "title", "for-session", "written-by")
    expect("an unindexed decision ID fails",
           lint_handoff(h.replace("2026-09-21-901 closeout gate", "2026-09-21-099 phantom"), 2, _IDS, _KB),
           "decision-id")
    expect("an unresolved wikilink fails",
           lint_handoff(h.replace("[[reference_fixture]]", "[[reference_nowhere]]"), 2, _IDS, _KB),
           "wikilink")
    expect("an empty section fails",
           lint_handoff(h.replace("- `pre-commit run --all-files` exit 0", ""), 2, _IDS, _KB), "empty-section")

    k = _good_kickoff()
    expect("a filled kickoff passes", lint_kickoff(k, 2, _PERSONAS, _STORIES))
    expect("an unregistered persona fails",
           lint_kickoff(k.replace("**Persona:** framework-maintainer", "**Persona:** wizard"), 2, _PERSONAS, _STORIES),
           "persona")
    line = persona_line("framework-maintainer")
    check("the scaffold's section 1 names the agent file and is nothing but that line",
          line in k and ".claude/agents/framework-maintainer.md" in line and _INVOCATION not in k)
    expect("a section 1 copying the agent's prompt instead of naming the agent fails",
           lint_kickoff(k.replace(line, _INVOCATION), 2, _PERSONAS, _STORIES), "persona-agent")
    expect("a section 1 naming another agent's file fails",
           lint_kickoff(k.replace(".claude/agents/framework-maintainer.md", ".claude/agents/wizard.md"), 2, _PERSONAS, _STORIES),
           "persona-agent")
    expect("a section 1 with text added to the line fails — the persona lives in the agent file",
           lint_kickoff(k.replace(line, line + " Be brief."), 2, _PERSONAS, _STORIES), "persona-agent")
    expect("a task citing an unknown story fails",
           lint_kickoff(k.replace("ACME-1.3 write", "ACME-9.9 write"), 2, _PERSONAS, _STORIES), "task-story")
    expect("a task citing no story fails",
           lint_kickoff(k.replace("- ACME-1.3 write the persona seeds", "- write the persona seeds"), 2, _PERSONAS, _STORIES),
           "task-story")
    expect("a closeout section without the command fails",
           lint_kickoff(k.replace("session-closeout", "session-close"), 2, _PERSONAS, _STORIES), "closeout")
    expect("a kickoff naming a version above the roster's fails",
           lint_kickoff(k.replace("**Persona version:** 1", "**Persona version:** 2"), 2, _PERSONAS, _STORIES),
           "persona-version")
    bumped = {"framework-maintainer": Persona(_INVOCATION, "2", ("1", "2"))}
    expect("a kickoff written against a version the persona held before passes", lint_kickoff(k, 2, bumped, _STORIES))
    expect("a kickoff naming the roster's current version passes",
           lint_kickoff(k.replace("**Persona version:** 1", "**Persona version:** 2"), 2, bumped, _STORIES))
    skipped = {"framework-maintainer": Persona(_INVOCATION, "3", ("1", "3"))}
    expect("a kickoff naming a version the changelog never held fails",
           lint_kickoff(k.replace("**Persona version:** 1", "**Persona version:** 2"), 2, skipped, _STORIES),
           "persona-version")
    expect("a kickoff that names no persona version fails",
           lint_kickoff(k.replace("**Persona version:** 1\n", ""), 2, _PERSONAS, _STORIES), "persona-version")

    expect("a well-formed agent file passes", lint_persona(_GOOD_PERSONA, "framework-maintainer"))
    ahead = _BUMPED_PERSONA.replace("  - 2 - 2026-09-24 - fixtures\n", "  - 2 - 2026-09-24 - fixtures\n  - 3 - 2026-09-25 - later\n")
    unlogged = _BUMPED_PERSONA.replace("  - 2 - 2026-09-24 - fixtures\n", "")
    held = [held_versions(x) for x in (_GOOD_PERSONA, _BUMPED_PERSONA, ahead, unlogged, _GOOD_PERSONA.replace("version: 1", "version: x"))]
    check("the versions held are the persona's own and each its changelog records below it, none without a version",
          held == [("1",), ("1", "2"), ("1", "2"), ("1", "2"), ()], str(held))
    record = persona_of(_BUMPED_PERSONA)
    check("the roster's record of a persona carries its prompt, its version and every version it has held",
          record.version == "2" and record.held == ("1", "2") and "enforce rules with fixtures" in record.invocation, str(record))
    expect("an agent whose name differs from its filename fails", lint_persona(_GOOD_PERSONA, "other"), "name")
    expect("an agent file with an empty body fails — the body is the prompt",
           lint_persona(_GOOD_PERSONA.split("---\n\n")[0] + "---\n\n", "framework-maintainer"), "prompt")
    expect("the pre-005 persona shape fails as an agent file",
           lint_persona(_OLD_SHAPE, "framework-maintainer"), "name", "frontmatter")
    expect("a file with no frontmatter fails", lint_persona(_INVOCATION + "\n", "framework-maintainer"), "frontmatter")
    expect("a frontmatter that does not parse fails — Claude Code would skip the file silently",
           lint_persona(_GOOD_PERSONA.replace("description: builds gates", "description: [unclosed"),
                        "framework-maintainer"), "frontmatter")
    expect("an unquoted list item holding `: ` is a mapping, not a string, and fails",
           lint_persona(_GOOD_PERSONA.replace("  - gates\n", "  - gates: and hooks\n"), "framework-maintainer"), "list")
    expect("a missing list fails", lint_persona(_GOOD_PERSONA.replace("insists_on:\n  - proof\n", ""),
                                               "framework-maintainer"), "frontmatter")
    check("the Invocation is the body, whole, without the frontmatter",
          persona_invocation(_GOOD_PERSONA) == _INVOCATION)
    check("the version is read from the frontmatter", persona_version(_GOOD_PERSONA) == "1")
    expect("an agent file without version: fails",
           lint_persona(_GOOD_PERSONA.replace("version: 1\n", ""), "framework-maintainer"), "frontmatter")
    expect("a version that is not a positive integer fails",
           lint_persona(_GOOD_PERSONA.replace("version: 1", "version: 1.1"), "framework-maintainer"), "version")
    expect("YAML's `true` is not a version, though Python counts a bool as an int",
           lint_persona(_GOOD_PERSONA.replace("version: 1", "version: true"), "framework-maintainer"), "version")
    expect("a version with no changelog item fails",
           lint_persona(_GOOD_PERSONA.replace("version: 1", "version: 2"), "framework-maintainer"), "changelog")
    probe = ("import sys; sys.modules['yaml'] = None; sys.path.insert(0, sys.argv[1]); import session_closeout as c; "
             "print(c.persona_invocation(sys.argv[2]) == sys.argv[3])")
    out = subprocess.run([sys.executable, "-I", "-c", probe, str(Path(__file__).resolve().parent), _GOOD_PERSONA, _INVOCATION],
                         capture_output=True, text=True, check=False)
    check("the module loads and reads a prompt with no PyYAML — the session hook imports it under any python3",
          out.returncode == 0 and out.stdout.strip() == "True", (out.stdout + out.stderr).strip()[-300:])
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
    expect("an expertise edit at the same version passes — the rule guards the prompt",
           lint_persona(_GOOD_PERSONA.replace("  - gates\n", "  - gates and hooks\n"), "framework-maintainer", _GOOD_PERSONA))
    expect("a committed copy with no valid version gives no baseline, so the commit repairing it passes",
           lint_persona(_GOOD_PERSONA, "framework-maintainer", _GOOD_PERSONA.replace("version: 1\n", "")))
    files = ["docs/orchestration/knowledge/INDEX.md", "docs/orchestration/" + "knowledge/reference_a.md",
             "scripts/x.py", "README.md", "src/app.tsx"]
    brain = ("# Brain\n\n- **Verify before done:** give yourself an executable check and iterate until it passes.\n"
             "- Never guess.\n- **Plan, then build:** settle a plan with the user before a change\n")
    rule = "---\npaths:\n  - \"docs/orchestration/knowledge/**\"\n---\n\n# Entries\n\n- One fact per file, with its row in the index.\n"
    expect("rules: a path-scoped rule that matches a tracked file and restates nothing passes", lint_rule(rule, files, brain))
    expect("rules: no frontmatter fails — Claude Code would load the rule in every session",
           lint_rule("# Entries\n\n- One fact per file, with its row in the index.\n", files, brain), "rule-paths")
    expect("rules: YAML that does not parse fails — Claude Code would load the rule unscoped",
           lint_rule(rule.replace('  - "docs', '  - [docs'), files, brain), "rule-paths")
    expect("rules: a frontmatter without paths: fails",
           lint_rule(rule.replace('paths:\n  - "docs/orchestration/knowledge/**"\n', "name: x\n"), files, brain), "rule-paths")
    expect("rules: paths as a comma-separated string is read as Claude Code reads it",
           lint_rule(rule.replace('paths:\n  - "docs/orchestration/knowledge/**"', 'paths: "nowhere/**, scripts/*.py"'), files, brain))
    expect("rules: globs that match no tracked file fail — the rule never loads",
           lint_rule(rule.replace("knowledge/**", "knowlege/**"), files, brain), "rule-dead")
    expect("rules: a rule matched only through a brace group passes",
           lint_rule(rule.replace("docs/orchestration/knowledge/**", "src/*.{ts,tsx}"), files, brain))
    expect("rules: a sentence of AGENTS.md repeated in a rule fails",
           lint_rule(rule + "- Verify before done: give yourself an executable check and iterate until it passes.\n", files, brain),
           "rule-restates")
    expect("rules: a clause of an AGENTS.md sentence copied into a rule fails (the live probe's miss)",
           lint_rule(rule + "- Verify before done: give yourself an executable check.\n", files, brain), "rule-restates")
    expect("rules: an AGENTS.md sentence carried inside a longer rule sentence fails",
           lint_rule(rule + "- In short, plan, then build: settle a plan with the user before a change, always.\n",
                     files, brain), "rule-restates")
    expect("rules: a short sentence both share is vocabulary, not a restatement",
           lint_rule(rule + "- Never guess.\n", files, brain))
    expect("rules: list items are sentences even with no punctuation on either side",
           lint_rule(rule + "- one two three\n- eta theta iota kappa lambda mu\n", files,
                     brain + "- alpha beta gamma delta epsilon zeta\n- eta theta iota kappa lambda mu\n"), "rule-restates")
    expect("rules: an unpunctuated list item repeated is found — list items are sentences",
           lint_rule(rule.replace("in the index.", "in the index") + "- Plan, then build: settle a plan with the user "
                     "before a change\n", files, brain), "rule-restates")
    check("globs: `**` crosses directories and `**/` may match none; `*` and `?` stay in one segment",
          bool(glob_regex("docs/**").match("docs/a/b/c.md") and glob_regex("**/*.py").match("a.py")
               and glob_regex("**/*.py").match("x/y/a.py") and glob_regex("*.md").match("README.md")
               and glob_regex("scripts/?.py").match("scripts/a.py"))
          and not glob_regex("*.md").match("docs/README.md") and not glob_regex("scripts/?.py").match("scripts/ab.py")
          and not glob_regex("a?b").match("a/b") and not glob_regex("scripts/*.py").match("scripts/x.pyc"))
    check("globs: brace groups expand and multiply",
          sorted(expand_braces("src/*.{ts,tsx}")) == ["src/*.ts", "src/*.tsx"] and len(expand_braces("{a,b}/{c,d}/x")) == 4)

    def state(roster: str, library: str) -> str:
        return (library_state(roster, library) or ("",))[0]
    check("library: a roster copy equal to the library passes", state(_GOOD_PERSONA, _GOOD_PERSONA) == "")
    check("library: a roster version above the library's is a fork and fails",
          state(_BUMPED_PERSONA, _GOOD_PERSONA) == "library-fork" and "library-fork" not in NOTE_RULES)
    check("library: the same version with other text is drift and fails, frontmatter included",
          state(_GOOD_PERSONA.replace("enforce rules with scripts", "enforce rules with prose"), _GOOD_PERSONA) == "library-drift"
          and state(_GOOD_PERSONA.replace("  - gates\n", "  - gates and hooks\n"), _GOOD_PERSONA) == "library-drift"
          and "library-drift" not in NOTE_RULES)
    check("library: a roster behind the library is reported as a note, never a violation",
          state(_GOOD_PERSONA, _BUMPED_PERSONA) == "library-newer" and "library-newer" in NOTE_RULES)
    check("library: a malformed version is left to the persona lint",
          state(_GOOD_PERSONA.replace("version: 1\n", ""), _GOOD_PERSONA) == "")

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
    check("current session: the newest entry, plus one while the next kickoff exists, none when unreadable",
          current_session(_STATUS, lambda n: n == 4) == 4 and current_session(_STATUS, lambda n: False) == 3
          and current_session("# Sprint Status\n\n## Notes\n", lambda n: True) is None)
    expect("closeout: a fresh project must still produce S2", verify_state(1, set(), closing=True), "not-closed")
    expect("verify: an empty folder past S1 fails", verify_state(2, set()), "no-pair")
    expect("verify: an unheaded sprint-status fails", verify_state(None, {2}), "status")
    expect("verify: a pair that should be archived fails", verify_state(3, {2, 3, 4}), "stale-pair")

    check("newest sprint-status session is read from the first H2", newest_session(_STATUS) == 3)
    check("a legacy heading yields no session",
          newest_session(_STATUS.replace("## S3 - 2026-09-21 - closeout", "## Session 3 Update")) is None)

    # The entry a closeout closes
    emergency = _STATUS.replace("- closeout", "- emergency checkpoint")
    nxt = "\n### Next\n\nS1 has no incoming kickoff, so this stands in for it.\n\n1. Run `/project-launch`.\n"
    expect("closeout: a written entry passes", unfinished_entry(_STATUS))
    expect("closeout: an entry still headed emergency checkpoint fails", unfinished_entry(emergency), "emergency-entry")
    expect("closeout: the heading in another case, with a suffix, still fails",
           unfinished_entry(_STATUS.replace("- closeout", "- Emergency  Checkpoint: launch paused")), "emergency-entry")
    expect("closeout: a title that only mentions one passes",
           unfinished_entry(_STATUS.replace("- closeout", "- The launch, after an emergency checkpoint")))
    expect("closeout: the initializer's `### Next` in the entry fails",
           unfinished_entry(_STATUS.replace("closeout\n\ntext\n", "closeout\n\ntext\n" + nxt, 1)), "next-section")
    expect("closeout: both together fail as both",
           unfinished_entry(emergency.replace("checkpoint\n\ntext\n", "checkpoint\n\ntext\n" + nxt, 1)),
           "emergency-entry", "next-section")
    expect("closeout: `### Next` inside fenced code, or a `### Next steps`, passes",
           unfinished_entry(_STATUS.replace("closeout\n\ntext\n", "closeout\n\ntext\n\n```\n### Next\n```\n\n### Next steps\n", 1)))
    expect("closeout: an older entry is not the one being closed",
           unfinished_entry(_STATUS.replace("- older\n\ntext\n", "- emergency checkpoint\n\ntext\n" + nxt)))
    expect("closeout: an unreadable heading is the status rule's, not this one's",
           unfinished_entry("# Sprint Status\n\n## Notes\n" + nxt))

    # The formats the gates read, with a hyphen alone:
    # each U+2014 form a project kept before the cut is refused, never read.
    check("formats: an entry headed in the U+2014 form is unread",
          newest_session(_STATUS.replace("## S3 - 2026-09-21 -", "## S3 \u2014 2026-09-21 \u2014")) is None)
    check("formats: an entry heading with another dash is unread",
          newest_session(_STATUS.replace("## S3 - 2026-09-21 -", "## S3 \u2013 2026-09-21 \u2013")) is None)
    expect("formats: a title holding a hyphen is read whole, not split at it",
           unfinished_entry(_STATUS.replace("- closeout", "- The launch - emergency checkpoint drill")))
    skeletons = handoff_skeleton(4, "2026-09-21") + kickoff_skeleton(4, "framework-maintainer", _PERSONAS["framework-maintainer"])
    check("formats: the scaffold writes the hyphen form and no U+2014",
          skeletons.startswith("# Handoff - S4\n") and "\n# Kickoff - S4\n" in skeletons and "\u2014" not in skeletons)
    expect("formats: a pair titled in the U+2014 form fails",
           lint_handoff(h.replace("# Handoff - S2", "# Handoff \u2014 S2", 1), 2, _IDS, _KB), "title")
    expect("formats: a pair titled with another separator fails",
           lint_handoff(h.replace("# Handoff - S2", "# Handoff: S2", 1), 2, _IDS, _KB), "title")
    dashed_persona = _GOOD_PERSONA.replace("  - 1 - 2026-09-21 - seeded", "  - 1 \u2014 2026-09-21 \u2014 seeded")
    expect("formats: a changelog item in the U+2014 form records no version",
           lint_persona(dashed_persona, "framework-maintainer"), "changelog")
    expect("formats: a changelog item with no separator records nothing",
           lint_persona(_GOOD_PERSONA.replace("  - 1 - 2026-09-21 - seeded", "  - 1 seeded"), "framework-maintainer"),
           "changelog")
    check("formats: a roster in the U+2014 form is drift from the library in the hyphen form",
          state(dashed_persona, _GOOD_PERSONA) == "library-drift")

    computed, declared, ids = tracker_counts(_TRACKER)
    expect("tracker: matching statistics pass; the [EXAMPLE] epic is skipped",
           tracker_violations(computed, declared))
    check("tracker: story IDs exclude the example epic", ids == {"ACME-1.1", "ACME-1.2"}, str(sorted(ids)))
    c2, d2, _ = tracker_counts(_TRACKER.replace("| **Completed** | 1 |", "| **Completed** | 0 |"))
    expect("tracker: a stale statistic fails", tracker_violations(c2, d2), "stats")
    c3, d3, _ = tracker_counts(_TRACKER.replace("| ACME-1.2 | b | Not Started", "| ACME-1.2 | b | Started"))
    expect("tracker: an unknown status value fails", tracker_violations(c3, d3), "status-value", "stats")

    stories = tracker_stories(_DEPS)
    by_id = {s.id: s for s in stories}
    check("dependencies: rows parse with every ID their Dependencies cell lists, and `—` lists none",
          len(stories) == 6 and by_id["ACME-1.5"].deps == ("ACME-1.1", "ACME-1.6") and by_id["ACME-1.1"].deps == (),
          str(stories))
    expect("dependencies: started stories on Done dependencies pass; waiting stories and the example epic "
           "are not judged", dependency_violations(stories))
    expect("dependencies: a Done story whose dependency is Not Started fails",
           dependency_violations(tracker_stories(_DEPS.replace("| Done | ACME-1.1, ACME-1.6 |", "| Done | ACME-1.1, ACME-1.3 |"))),
           "dependency-order")
    expect("dependencies: a Done story whose dependency is only In Progress fails",
           dependency_violations(tracker_stories(_DEPS.replace("| Done | ACME-1.1, ACME-1.6 |", "| Done | ACME-1.2 |"))),
           "dependency-order")
    found = dependency_violations(tracker_stories(_DEPS.replace("| c | Not Started | ACME-1.2 |", "| c | In Progress | ACME-1.2 |")))
    check("dependencies: an In Progress story whose dependency is In Progress fails, and only it — the "
          "Blocked story behind it is waiting", len(found) == 1 and found[0][0] == "dependency-order"
          and "ACME-1.3" in found[0][1], str(found))
    found = dependency_violations(tracker_stories(_DEPS.replace("| Done | ACME-1.1, ACME-1.6 |", "| Done | ACME-9.9 |")))
    check("dependencies: a started story naming a dependency that is no story fails and says so",
          _rules(found) == {"dependency-order"} and "not a story" in found[0][1], str(found))

    expect("placeholders: the template, with no .template-version, keeps every shape it ships", placeholder_violations(_LIVE, False))
    expect("placeholders: a fresh project with only the example epic passes",
           placeholder_violations(_live(tracker=_TRACKER.split("## Epic: ACME-1")[0]), True))
    expect("placeholders: once a real epic exists, the example epic stays beside it and passes",
           placeholder_violations(_LIVE, True))
    clean = _TRACKER.replace(_EXAMPLE_EPIC, "")
    expect("placeholders: the same project with the example epic removed passes",
           placeholder_violations(_live(tracker=clean), True))
    found = placeholder_violations(_live(tracker=clean, status=_STATUS.replace("**Current Phase:** x", "**Last Updated:** {{DATE}}"),
                                         log=_LOG + "\n**Owner:** {{PROJECT_NAME}}\n"), True)
    check("placeholders: an unfilled token in sprint-status or the decision log fails, each named",
          sorted(w.split(":")[0] for _, w, _ in found) == ["sprint/decision-log.md", "sprint/sprint-status.md"]
          and all(r == "live-placeholder" for r, *_ in found), str(found))
    expect("placeholders: the example decision's index row and its heading stay and pass",
           placeholder_violations(_live(tracker=clean, log=_LOG + "| [EXAMPLE] ACME-2025-01-15-000 | 2025-01-15 | Sample | APPROVED |\n"
                                                              "\n## Decision [EXAMPLE] ACME-2025-01-15-000: Sample\n\nexample\n"), True))
    quoted = _STATUS + ("replace every `{{PLACEHOLDER}}` value and remove the `[EXAMPLE]` rows\n"
                        "| a row about `[EXAMPLE]` rows | `{{DATE}}` |\n")
    expect("placeholders: a token or marker quoted in inline code explains the convention and passes",
           placeholder_violations(_live(tracker=clean, status=quoted), True))
    expect("placeholders: a fenced block is quoted too",
           placeholder_violations(_live(tracker=clean, status=_STATUS + "```\n{{DATE}}\n| [EXAMPLE] |\n```\n"), True))
    expect("placeholders: a GitHub Actions expression is not a token",
           placeholder_violations(_live(tracker=clean, status=_STATUS + "run: ${{ secrets.TOKEN }}\n"), True))

    # These fixtures live in a file the tree pass scans, so every literal here is an allowed slug;
    # the dangling cases vary the allow argument instead.
    doc = "see [[reference_fixture]] and, with a label, [[reference_fixture|the gate]]\n"
    check("tree wikilinks: links that resolve pass, labelled or not", dangling_wikilinks(doc, _KB, set()) == [])
    check("tree wikilinks: a dangling link is found with its line",
          dangling_wikilinks("x\n" + doc + "then [[reference_nowhere]]\n", _KB, set()) == [(3, "reference_nowhere")])
    check("tree wikilinks: the convention's own placeholders and the fixture slug are allowed",
          dangling_wikilinks("`[[slug]]` → `[[<slug>]]`; [[other-slug]]; `[[wikilink]]`; [[reference_nowhere]]\n", _KB) == [])
    check("tree wikilinks: a padded link resolves once stripped, as the handoff linter reads it",
          dangling_wikilinks("[[ reference_fixture ]]\n", _KB, set()) == []
          and dangling_wikilinks("[[ reference_nowhere ]]\n", _KB, set()) == [(1, "reference_nowhere")])
    check("tree wikilinks: the allow set is exact — a near miss in it still leaves the link dangling",
          dangling_wikilinks("[[slug]]\n", _KB, {"slugs"}) == [(1, "slug")])
    check("tree wikilinks: an empty allow set makes the placeholders dangling, so the set is load-bearing",
          [s for _, s in dangling_wikilinks("[[slug]] [[reference_nowhere]]\n", _KB, set())] == ["slug", "reference_nowhere"])

    # A citation of a decision no index holds
    cited = "Why: decisions 2026-09-21-901 and 2026-01-02-003.\n"
    check("citations: an unprefixed ID no index holds is found, an indexed one passes",
          unindexed_citations(cited, _IDS, set()) == [(1, "2026-01-02-003")])
    check("citations: a prefixed ID is a project's or an example and is not read",
          unindexed_citations("ACME-2026-01-02-003 and PROJ-2026-01-02-003\n", _IDS, set()) == [])
    check("citations: an ID inside a longer token is not one",
          unindexed_citations("x2026-01-02-003 2026-01-02-0031 2026-01-02-003a\n", _IDS, set()) == [])
    check("citations: a log's `**Deletes:**` line is the record and is not read; elsewhere in the log it is",
          unindexed_citations("**Deletes:** 2026-01-02-003\n", _IDS, set(), log=True) == []
          and unindexed_citations("**Amends:** 2026-01-02-003\n", _IDS, set(), log=True) == [(1, "2026-01-02-003")])
    check("citations: a `**Deletes:**` line outside a decision log is read",
          unindexed_citations("**Deletes:** 2026-01-02-003\n", _IDS, set()) == [(1, "2026-01-02-003")])
    check("citations: the allow set is exact, and the fixtures' IDs are in it",
          unindexed_citations(cited, _IDS, {"2026-01-02-004"}) == [(1, "2026-01-02-003")]
          and unindexed_citations(cited, _IDS) == [])

    # An invented name that became real
    def named(found: list) -> list[str]:
        return [d.split(" ")[0] for rule, _, d in found if rule == "allow-set"]
    check("allow sets: invented names no index and no entry holds pass",
          allow_set_violations(_IDS, _KB, {"2026-01-02-003"}, {"reference_nowhere"}) == [])
    check("allow sets: an allow-set decision ID an index holds is refused, the invented one beside it not",
          named(allow_set_violations(_IDS, set(), {"2026-09-21-901", "2026-01-02-003"}, set())) == ["2026-09-21-901"])
    check("allow sets: an allow-set slug naming a knowledge entry is refused, the placeholder beside it not",
          named(allow_set_violations(set(), _KB, set(), {"reference_fixture", "slug"})) == ["[[reference_fixture]]"])
    check("allow sets: by default the gate's own sets are judged, which hold the fixture index's ID and entry",
          named(allow_set_violations(_IDS, _KB)) == ["2026-09-21-901", "[[reference_fixture]]"])

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
    if "--scaffold" in argv:
        slug = argv[argv.index("--persona") + 1] if "--persona" in argv and argv.index("--persona") + 1 < len(argv) else None
        return cmd_scaffold(slug)
    print(__doc__.split("Usage:")[1] if "Usage:" in __doc__ else "see --help", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
