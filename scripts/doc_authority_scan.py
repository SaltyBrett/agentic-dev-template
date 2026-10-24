#!/usr/bin/env python3
"""
doc_authority_scan.py — a decision that changes an authoritative document is recorded in it or
queued for it, and nothing else passes.

THE FAILURE THIS CLOSES
-----------------------
Updates, design changes and reversals land in the decision log and the knowledge base, and the
documents that are the source of truth for a scope (the PRD, the architecture, the runbooks, the
standards) are never brought up to date. The document-control standard said "update the documents
and the changelog table", and nothing enforced it. The knowledge base escaped this because
`teaches:` and `verified:` are gated, yet even that gate cannot see a MISSING update: a new
decision names no entry. Decision 2026-10-22-002.

WHAT IT CHECKS
--------------
An authority is any markdown file git would commit whose YAML frontmatter carries `authority:`.
The frontmatter is the registry; there is no list to keep beside it.

    ---
    authority: <the scope this document is the source of truth for>
    implements: [<decision-id>, ...]
    verified: <YYYY-MM-DD>
    ---
    ...
    ## Version log

    | Version | Date | Decision | Summary | Commit |
    |---------|------|----------|---------|--------|
    | 2 | 2026-10-25 | 2026-10-24-001 | fact: `MAX_ROWS` is 12 | pending |
    | 1 | 2026-10-23 | 2026-10-22-002 | Marked as the authority (TMPL-2.3) | 1a2b3c4 |

  frontmatter  the block parses as YAML: `authority:` a non-empty string, `implements:` a list of
               decision IDs, `verified:` an unquoted ISO date
  scope        no two authorities claim one scope
  unknown-id   every ID `implements:` or a row cites is in a decision index
  stale        `verified:` predates a change to a decision the document implements, computed as
               kb_freshness_scan computes it for a knowledge entry
  no-log       the last H2 is `## Version log`, holding a table with at least one row
  log-header   its columns are Version, Date, Decision, Summary, Commit, in that order
  row          each row: a version (`3`, `2.1`), an ISO date, one or more decision IDs, a summary,
               and `pending` or a commit hash
  order        newest first: versions strictly descending, dates never rising
  unmarked     a row's summary opens `fact:` and holds the fact itself (a code span or a number:
               a value, a name, a path, a count), or cites a tracker story whose row cites the
               row's decision. Inline, a session records facts; a structural change is a story
  no-affects   every decision dated AFFECTS_FROM or later has a body with an `**Affects:**` line:
               each document it changes as a code span of its path, or `none`. Older decisions
               read as none
  unrecorded   for each decision whose `**Affects:**` names an authority, the authority's version
               log holds a row citing the decision, or the tracker holds a story citing the
               decision and the path that is not Done. Those two outcomes, and nothing else
  commit       a stored hash is a prefix of the first commit, following renames but never a
               copy, whose copy of the document holds that version
  index        a decision index that cannot be located is never zero decisions

In a project whose tracker holds a real epic, the approval gate (decision 2026-10-23-008), each
document read as decision 2026-10-23-014 defines it:
  approval     the PRD in `docs/prd/` and the architecture in `docs/architecture/` each stand
               approved, one document with the `authority:` line and a version-log row, its status
               `approved`, or `draft` while reopened for revision, when the newest row stands; or an
               APPROVED decision of the project's own log carries `**Skips:**` naming it
  prd-version  an architecture with `status: approved` has the PRD's newest version as `prd:`, quoted
  skips        a `**Skips:**` line names only the stages of `/project-launch`

In a project, what the template wrote is judged in the template: a row citing only framework
decisions is not held to `unmarked` or `commit`, since the story it cites is in the template's
tracker and the commit in the template's history, the project's squashed at birth; and a framework
decision is not held to `no-affects` or `unrecorded`, since the story that queues it is the
template's too. The project's own rows and decisions are judged in full (decision 2026-10-23-015).

--stamp            fills each `pending` row whose first commit exists with that commit's hash
--history <doc>    prints each row's stored commit beside the one git derives
--list             the registry and the gate's reach
--queue            the `doc-queue` gate, a manual hook the SessionStart hook runs at cold start
                   (decision 2026-10-23-016). The technical writer's queue is every story not Done
                   whose row carries a `Queued: S<N>` note, written bare by the session N that queued
                   a change for the writer; in a code span it is the convention quoted, not a note.
                   The session at work is session_closeout's rule over sprint-status and the pairs.
  queue-note       the note names one session, as `Queued: S9`, once
  queue-shape      a queued story names exactly one authority in a code span, the document the
                   drain rewrites, and cites an indexed decision, which the drain's row cites
  queue-future     the note names no session after the one at work
  overdue          the story is drained by S<N+1>: at a later session it fails
  session          the newest sprint-status entry is readable, so a session is known

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It cannot read prose. A row citing a decision says the document was brought up to date, not that
it was brought up to date correctly, and a path named outside a code span in `**Affects:**` is not
read. Nor can it see who wrote a row: a story citation is the evidence that a change went through
the queue, and `fact:` is the author's declaration that the change is a fact. How long a story may
wait in the queue is `--queue`'s, which drains nothing: the doc-drain skill does, one document per
run, and leaves its change for the main session to review.

Usage:  pre-commit run doc-authority-scan --all-files        # portable; pre-commit provides pyyaml
        pre-commit run doc-queue --hook-stage manual --all-files --verbose
        python3 scripts/doc_authority_scan.py [--list]
        python3 scripts/doc_authority_scan.py --stamp
        python3 scripts/doc_authority_scan.py --history <doc>
        python3 scripts/doc_authority_scan.py --self-test
Exit 0 = clean, 1 = violations (blocks the commit), 2 = cannot run.
"""

from __future__ import annotations

import datetime
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_freshness_scan  # noqa: E402 — the decision-index parser and the change-date rule
import session_closeout  # noqa: E402 — the repository root, the markdown helpers, the tracker's one parse

try:
    import yaml
except ModuleNotFoundError:
    print(
        "doc_authority_scan: PyYAML is not installed in this interpreter.\n"
        "    This gate is normally run through pre-commit, which provisions it via\n"
        "    `additional_dependencies: [pyyaml]`:\n"
        "        pre-commit run doc-authority-scan --all-files\n"
        "    To run it directly instead: python3 -m pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)

ROOT = session_closeout.ROOT
TRACKER = session_closeout.TRACKER
PROFILE = session_closeout.PROFILE           # present in a project, absent in the template
LOGS = session_closeout.DECISION_LOGS        # the project's log, then the framework's
FRAMEWORK_LOG = "docs/governance/framework_decisions.md"

# The date of decision 2026-10-22-002, which made `**Affects:**` part of every decision body from
# itself forward. A fixed law, not a maintained value: older decisions read as `none`.
AFFECTS_FROM = "2026-10-22"
AFFECTS = "**Affects:**"
LOG_HEADING = "Version log"
LOG_COLUMNS = ["Version", "Date", "Decision", "Summary", "Commit"]
PENDING = "pending"
FACT = "fact:"
STAMP_LEN = 7

# A top-level `authority:` key in the frontmatter source. Only a candidate: the block is then
# parsed, and one that claims authority and does not parse is a violation, never skipped.
CLAIM = re.compile(r"^authority\s*:", re.M)
VERSION = re.compile(r"^\d+(?:\.\d+)*$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HASH = re.compile(r"^[0-9a-f]{7,40}$")
CODE_SPAN = re.compile(r"`([^`\n]+)`")
NUMBER = re.compile(r"\b\d+(?:\.\d+)?\b")
SEPARATOR = re.compile(r"^:?-+:?$")
CELL_SPLIT = re.compile(r"(?<!\\)\|")
DECISION_HEADING = re.compile(r"^Decision (.+?):\s")
FIELD = re.compile(r"^\*\*[^*]+:\*\*")
STORY_ID = session_closeout.STORY_ID
H2 = session_closeout.H2
FENCE = session_closeout.FENCE

FIXES = {
    "frontmatter": "Give the document a frontmatter block that parses: `authority: <scope>`,\n"
                   "    `implements: [<decision-id>, ...]` (`[]` when none), `verified: YYYY-MM-DD` unquoted.",
    "scope": "One document is the authority for a scope. Supersede the other (remove its `authority:`\n"
             "    and say where the scope now lives), or narrow one of the two scopes.",
    "unknown-id": "Cite a decision indexed in `sprint/decision-log.md` or\n"
                  "    `docs/governance/framework_decisions.md`, by its ID exactly.",
    "stale": "Re-read the decision and correct the document, add a version-log row for the change,\n"
             "    then move `verified:`. Never the date alone.",
    "no-log": "End the document with `## Version log` and its table, newest row first:\n"
              "    | Version | Date | Decision | Summary | Commit |",
    "log-header": "The version log's columns are exactly: | Version | Date | Decision | Summary | Commit |",
    "row": "Each row: a version (`3`, `2.1`), a YYYY-MM-DD date, the decision IDs it records\n"
           "    (comma-separated), a summary, and `pending` or the commit hash (`--stamp` fills it).",
    "order": "Newest row first: each version lower than the one above it, each date no later.",
    "unmarked": "Open the summary with `fact:` and state the fact itself (a value, name or path in\n"
                "    backticks, or a count); or, for a structural change, cite the tracker story that\n"
                "    queued it, whose row cites the row's decision.",
    "no-affects": "Add `**Affects:**` to the decision's header block: each document it changes as a\n"
                  "    code span of its path, with the sections and the nature of the change, or `none`.",
    "unrecorded": "Record the change in the document, a version-log row citing the decision; or queue\n"
                  "    it, a tracker story that is not Done whose row cites the decision and the path.",
    "commit": "Set the row's Commit to `pending` and run `python3 scripts/doc_authority_scan.py\n"
              "    --stamp` once the row is committed; `--history <doc>` prints the derived commit.",
    "index": "Restore the `## Decision Index` heading and its table in the log named.",
    "queue-note": "Write the note bare on the story's row, once, naming the session that queued it:\n"
                  "    `Queued: S9`. Quoted in a code span it is the convention, not a note.",
    "queue-shape": "A queued story names the one authority it changes, its path in a code span, and the\n"
                   "    decision it records. Split a story that changes two documents; one drain is one document.",
    "queue-future": "Name the session that queued the change, this one or earlier.",
    "overdue": "Drain the document with the doc-drain skill (`/doc-drain <path>`): every queued change to\n"
               "    it in one pass, its version-log row, the stories Done. A change no longer wanted is\n"
               "    descoped by a decision, never left waiting.",
    "session": "Head the newest sprint-status entry `## S<N> — YYYY-MM-DD — <title>`.",
    "approval": "Approve the document by `docs/templates/README.md`: `status: approved`, the `authority:`\n"
                "    line for the project's scope, its first version-log row citing the approval decision.\n"
                "    Or log the Chair's skip: a decision in `sprint/decision-log.md` headed `**Skips:** prd`\n"
                "    or `**Skips:** architecture`, its reason in the body. One approved document per folder.",
    "prd-version": "Revise the architecture against the PRD's newest version and approve it again, its\n"
                   "    `prd:` the quoted version it is built from (decision 2026-10-23-008).",
    "skips": "`**Skips:**` names the stages passed over, `prd`, `architecture` or both, comma-separated.",
}

# The approval gate (decision 2026-10-23-008): in a project, a real epic needs an approved PRD and an
# approved architecture, read as decision 2026-10-23-014 defines them, or a logged skip of either.
STAGES = {"prd": ("docs/prd/", "PRD"), "architecture": ("docs/architecture/", "architecture")}
# Every stage of `/project-launch` may be skipped; only the two above are held by the gate.
LAUNCH_STAGES = ("intake", "team", "prd", "architecture", "planning")
SKIPS = "**Skips:**"
APPROVED = "approved"
# A document reopened for revision keeps its authority and its rows, and its last approved version
# stands until it is approved again (decision 2026-10-23-020, amended).
REOPENED = "draft"
PROJECT_LOG = "sprint/decision-log.md"

# The writer's queue (decision 2026-10-23-016): a bare note on an open story's row.
QUEUE_NOTE = "Queued:"
QUEUED = re.compile(r"Queued:\s*S(\d+)\b")
INLINE_CODE = session_closeout.INLINE_CODE
DRAIN = "/doc-drain"


class Row(NamedTuple):
    """One version-log row, read from a line that parsed cleanly."""
    version: str
    date: str
    decisions: tuple[str, ...]
    summary: str
    commit: str
    line: int          # 1-based, in the document


class Authority(NamedTuple):
    path: str
    scope: str
    implements: tuple[str, ...]
    verified: str      # ISO, or "" when the frontmatter's date did not parse
    rows: tuple[Row, ...]


class Queued(NamedTuple):
    """One story in the writer's queue: queued in `session`, for `document`."""
    story: str
    session: int
    document: str


class HistoryUnavailable(Exception):
    """Git cannot give the document's full history. A stored hash is then unverifiable, never verified."""


# ==============================================================================
# Readers — pure functions over text, so the self-test needs no files
# ==============================================================================

def cells(line: str) -> list[str]:
    return [c.strip() for c in CELL_SPLIT.split(line.strip().strip("|"))]


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(p) for p in version.split("."))


def valid_date(value: str) -> bool:
    if not ISO_DATE.match(value):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def version_log(text: str) -> tuple[list[Row], list[tuple[str, int, str]]]:
    """The rows of the document's `## Version log`, and the problems found, as (rule, line, message).

    The section must be the last H2 outside fenced code, and the table the first beneath it. A row
    with a malformed cell is reported and left out, so the rules that read rows judge only real ones.
    """
    lines = text.splitlines()
    heads: list[tuple[int, str]] = []
    fenced = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            fenced = not fenced
            continue
        m = None if fenced else H2.match(line)
        if m:
            heads.append((i, m.group(1)))
    if not heads or heads[-1][1] != LOG_HEADING:
        at = next((i + 1 for i, h in heads if h == LOG_HEADING), 0)
        msg = "`## Version log` is not the document's last section" if at else "no `## Version log` section"
        return [], [("no-log", at, msg)]

    table: list[tuple[int, str]] = []
    for i in range(heads[-1][0] + 1, len(lines)):
        if lines[i].startswith("|"):
            table.append((i + 1, lines[i]))
        elif table:
            break
    if len(table) < 3:
        return [], [("no-log", heads[-1][0] + 1, "the version log holds no rows")]
    head_line, head = table[0]
    if cells(head) != LOG_COLUMNS or not all(SEPARATOR.match(c) for c in cells(table[1][1])):
        return [], [("log-header", head_line, f"the columns read {cells(head)}")]

    rows: list[Row] = []
    problems: list[tuple[str, int, str]] = []
    for no, line in table[2:]:
        c = cells(line)
        if len(c) != len(LOG_COLUMNS):
            problems.append(("row", no, f"the row has {len(c)} cells; the log has {len(LOG_COLUMNS)} columns"))
            continue
        version, date, decision, summary, commit = c
        ids = tuple(d.strip().strip("`") for d in decision.split(",") if d.strip().strip("`"))
        bad = []
        if not VERSION.match(version):
            bad.append(f"version `{version}` is not a number like `3` or `2.1`")
        if not valid_date(date):
            bad.append(f"date `{date}` is not YYYY-MM-DD")
        if not ids or any(d in ("—", "-") for d in ids):
            bad.append("it cites no decision")
        if not summary:
            bad.append("the summary is empty")
        if commit != PENDING and not HASH.match(commit):
            bad.append(f"commit `{commit}` is neither `{PENDING}` nor a hash")
        if bad:
            problems.append(("row", no, "; ".join(bad)))
            continue
        rows.append(Row(version, date, ids, summary, commit, no))

    for above, below in zip(rows, rows[1:]):
        if version_key(below.version) >= version_key(above.version):
            problems.append(("order", below.line, f"version {below.version} sits below {above.version}"))
        if below.date > above.date:
            problems.append(("order", below.line, f"date {below.date} sits below {above.date}"))
    return rows, problems


def read_authority(path: str, text: str) -> tuple[Authority | None, list]:
    """(the authority, violations), or (None, []) when the frontmatter claims no authority."""
    src, _ = session_closeout.split_frontmatter(text)
    if src is None or not CLAIM.search(src):
        return None, []
    try:
        keys = yaml.safe_load(src)
    except yaml.YAMLError as e:
        first = str(e).splitlines()[0] if str(e) else type(e).__name__
        return None, [("frontmatter", path, f"the frontmatter claims authority and does not parse as YAML: {first}")]
    if not isinstance(keys, dict):
        return None, [("frontmatter", path, "the frontmatter is not a YAML mapping")]

    v: list[tuple[str, str, str]] = []
    scope = keys.get("authority")
    if not isinstance(scope, str) or not scope.strip():
        v.append(("frontmatter", path, "`authority:` must name the scope, a non-empty string"))
        scope = ""
    implements = keys.get("implements")
    if not isinstance(implements, list) or not all(isinstance(i, str) and i.strip() for i in implements):
        v.append(("frontmatter", path, "`implements:` must be a list of decision IDs, `[]` when none"))
        implements = []
    verified = keys.get("verified")
    if type(verified) is not datetime.date:   # `type`, not isinstance: a datetime is a date subclass
        v.append(("frontmatter", path, "`verified:` must be an unquoted ISO date, as `verified: 2026-10-23`"))
        verified = None

    rows, problems = version_log(text)
    v += [(rule, f"{path}:{line}" if line else path, msg) for rule, line, msg in problems]
    return Authority(path, scope.strip(), tuple(i.strip() for i in implements),
                     verified.isoformat() if verified else "", tuple(rows)), v


def decision_bodies(text: str) -> dict[str, str]:
    """{decision ID: body} for every `## Decision <ID>: <title>` outside fenced code; [EXAMPLE]
    bodies are the convention's illustration, not decisions."""
    _, secs = session_closeout.sections(text)
    out: dict[str, str] = {}
    for heading, body in secs:
        m = DECISION_HEADING.match(heading)
        if m and not m.group(1).startswith(session_closeout.EXAMPLE_MARK):
            out[m.group(1)] = body
    return out


def header_field(body: str, label: str) -> str | None:
    """A `**Field:**` value, its continuation lines joined, or None when the body has no line.
    A continuation runs until a blank line, a heading or the next `**Field:**`."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(label):
            value = [line[len(label):].strip()]
            for more in lines[i + 1:]:
                if not more.strip() or FIELD.match(more) or more.startswith("#"):
                    break
                value.append(more.strip())
            return " ".join(value).strip()
    return None


def affects(body: str) -> str | None:
    return header_field(body, AFFECTS)


def cites(text: str, did: str) -> bool:
    return re.search(rf"(?<![\w-]){re.escape(did)}(?![\w-])", text) is not None


def marked(row: Row, stories: dict[str, session_closeout.Story]) -> bool:
    """A fact, declared and stated; or a change made by the story that queued it."""
    if row.summary.startswith(FACT):
        rest = row.summary[len(FACT):]
        return bool(CODE_SPAN.search(rest) or NUMBER.search(rest))
    for sid in STORY_ID.findall(row.summary):
        story = stories.get(sid)
        if story and any(cites(story.row, d) for d in row.decisions):
            return True
    return False


def judge(docs: dict[str, str], logs: dict[str, str], tracker: str, project: bool,
          history: Callable[[str], dict[str, str]]) -> tuple[list, dict]:
    """Every rule of the gate over in-memory text: {path: document}, {log label: log}, the
    tracker, whether this is a project, and history(path) -> {version: full commit hash}.
    Returns (violations as (rule, where, message), the reach for --list)."""
    try:
        decs = kb_freshness_scan.parse_logs(logs)
    except kb_freshness_scan.DecisionIndexNotFound as e:
        return [("index", "", str(e))], {}
    framework_ids = set(kb_freshness_scan.index_decisions(logs[FRAMEWORK_LOG])) if FRAMEWORK_LOG in logs else set()
    bodies: dict[str, str] = {}
    for text in logs.values():            # in LOGS order, so the framework file wins a duplicate
        bodies.update(decision_bodies(text))
    stories = {s.id: s for s in session_closeout.tracker_stories(tracker)}

    v: list[tuple[str, str, str]] = []
    auths: list[Authority] = []
    for path, text in sorted(docs.items()):
        a, found = read_authority(path, text)
        v += found
        if a:
            auths.append(a)

    claimed: dict[str, list[str]] = {}
    for a in auths:
        if a.scope:
            claimed.setdefault(" ".join(a.scope.casefold().split()), []).append(a.path)
    for scope, paths in claimed.items():
        if len(paths) > 1:
            v.append(("scope", ", ".join(paths), f"each claims the scope `{scope}`"))

    reach = {"authorities": [], "foreign": 0, "pending": 0}
    for a in auths:
        for did in a.implements:
            if did not in decs:
                v.append(("unknown-id", a.path, f"`implements:` names {did}, which is in neither decision index"))
            elif a.verified:
                changed, why = kb_freshness_scan.effective_change_date(did, decs)
                if changed and changed > a.verified:
                    v.append(("stale", a.path, f"implements {did} ({why} {changed}) but was last verified {a.verified}"))
        for r in a.rows:
            where = f"{a.path}:{r.line}"
            # The template's row in a project: its story and its commit are the template's.
            foreign = project and all(d in framework_ids for d in r.decisions)
            for did in r.decisions:
                if did not in decs:
                    v.append(("unknown-id", where, f"version {r.version} cites {did}, which is in neither decision index"))
            if not foreign and not marked(r, stories):
                v.append(("unmarked", where, f"version {r.version} is neither `{FACT}` with its fact nor a story's change"))
            if r.commit == PENDING:
                reach["pending"] += 1
            elif foreign:
                reach["foreign"] += 1     # the template's row, verified in the template
            else:
                first = history(a.path).get(r.version)
                if not first or not first.startswith(r.commit):
                    derived = first[:STAMP_LEN] if first else "none: the row is not committed"
                    v.append(("commit", where, f"version {r.version} stores {r.commit}; the commit that introduced it is {derived}"))
        reach["authorities"].append(a)

    paths = {a.path for a in auths}
    recorded = {(a.path, d) for a in auths for r in a.rows for d in r.decisions}
    reach.update(due=0, by_row=0, by_story=0)
    for did in sorted(decs):
        if decs[did]["date"] < AFFECTS_FROM or (project and did in framework_ids):
            continue          # older than the rule, or the template's, judged where its queue lives
        reach["due"] += 1
        body = bodies.get(did)
        value = affects(body) if body is not None else None
        if not value:
            v.append(("no-affects", did, "the decision has no body" if body is None else "the body has no `**Affects:**` value"))
            continue
        for p in sorted({s.strip() for s in CODE_SPAN.findall(value)} & paths):
            if (p, did) in recorded:
                reach["by_row"] += 1
            elif any(s.status != "Done" and cites(s.row, did) and p in s.row for s in stories.values()):
                reach["by_story"] += 1
            else:
                v.append(("unrecorded", f"{did} -> {p}", "no version-log row cites the decision and no open story queues it"))
    return v, reach


def judge_approval(docs: dict[str, str], logs: dict[str, str], tracker: str, project: bool) -> list:
    """The approval gate over in-memory text. In a project whose tracker holds a real epic, each of
    the PRD and the architecture stands approved, one document in its folder with the `authority:`
    line and a version-log row, `status: approved`, or `status: draft` while reopened for revision,
    when its newest row is the version that stands; or its skip is logged: an APPROVED decision of
    the project's own log whose header carries `**Skips:**` naming it. An architecture with
    `status: approved` is built from the PRD's newest version. Returns (rule, where, message)."""
    epics = session_closeout.real_epics(tracker)
    if not project or not epics:
        return []      # the template, or a project still before its planning session
    try:
        decs = kb_freshness_scan.parse_logs(logs)
    except kb_freshness_scan.DecisionIndexNotFound as e:
        return [("index", "", str(e))]
    v: list[tuple[str, str, str]] = []
    skipped: set[str] = set()
    for did, body in decision_bodies(logs.get(PROJECT_LOG, "")).items():
        value = header_field(body, SKIPS)
        if value is None:
            continue
        names = [w.strip().casefold() for w in value.split(",") if w.strip()]
        if not names or any(n not in LAUNCH_STAGES for n in names):
            v.append(("skips", did, f"`{SKIPS} {value}` names other than the launch stages, {', '.join(LAUNCH_STAGES)}"))
        if decs.get(did, {}).get("status", "").upper().startswith("APPROVED"):
            skipped.update(n for n in names if n in STAGES)

    approved: dict[str, list[tuple[str, dict, Authority]]] = {s: [] for s in STAGES}
    for path, text in sorted(docs.items()):
        stage = next((s for s, (folder, _) in STAGES.items() if path.startswith(folder)), None)
        src, _ = session_closeout.split_frontmatter(text)
        try:
            keys = yaml.safe_load(src) if stage and src else None
        except yaml.YAMLError:
            keys = None    # a claimed authority that does not parse is the `frontmatter` rule's
        status = keys.get("status") if isinstance(keys, dict) else None
        if status not in (APPROVED, REOPENED):
            continue
        a, _ = read_authority(path, text)
        if a is None:
            if status == APPROVED:
                v.append(("approval", path, "`status: approved`, but the document claims no authority"))
            continue      # a first draft claims nothing and stands for nothing
        if a.rows:        # with no row it was never approved; `no-log` is the authority gate's
            approved[stage].append((path, keys, a))

    epic = epics[0].removeprefix("Epic:").strip()
    for stage, (folder, label) in STAGES.items():
        found = approved[stage]
        if len(found) > 1:
            v.append(("approval", ", ".join(p for p, _, _ in found), f"{folder} holds {len(found)} approved documents; "
                                                                      f"the project has one {label}"))
        elif not found and stage not in skipped:
            v.append(("approval", folder, f"the tracker holds a real epic ({epic}), and {folder} holds no approved "
                                          f"{label} nor does an APPROVED decision log its skip"))
    if len(approved["architecture"]) == 1 and len(approved["prd"]) == 1:
        path, keys, _ = approved["architecture"][0]
        prd_path, _, prd = approved["prd"][0]
        newest = prd.rows[0].version
        if keys.get("status") == APPROVED and keys.get("prd") != newest:
            v.append(("prd-version", path, f"`prd:` reads {keys.get('prd')!r}, and the approved PRD {prd_path} is at "
                                           f"version {newest!r}"))
    return v


def check_tree(docs: dict[str, str], logs: dict[str, str], tracker: str, project: bool,
               history: Callable[[str], dict[str, str]]) -> tuple[list, dict]:
    """Every rule a commit is held to: the authority gate, then the approval gate."""
    v, reach = judge(docs, logs, tracker, project, history)
    return v + [x for x in judge_approval(docs, logs, tracker, project) if x not in v], reach


def judge_queue(docs: dict[str, str], logs: dict[str, str], tracker: str,
                current: int | None) -> tuple[list, list[Queued]]:
    """The doc-queue rules over in-memory text and the session at work. Returns (violations as
    (rule, where, message), the queue). A Done story is drained and an [EXAMPLE] one is no story."""
    if current is None:
        return [("session", "sprint/sprint-status.md", "the newest entry is not headed `## S<N> — YYYY-MM-DD — <title>`, "
                 "so no session is known")], []
    try:
        ids = set(kb_freshness_scan.parse_logs(logs))
    except kb_freshness_scan.DecisionIndexNotFound as e:
        return [("index", "", str(e))], []
    authorities = {path for path, text in docs.items() if read_authority(path, text)[0]}
    v: list[tuple[str, str, str]] = []
    queue: list[Queued] = []
    for s in session_closeout.tracker_stories(tracker):
        bare = INLINE_CODE.sub("", s.row)
        if s.status == "Done" or QUEUE_NOTE not in bare:
            continue
        notes = QUEUED.findall(bare)
        if len(notes) != 1 or bare.count(QUEUE_NOTE) != 1:
            v.append(("queue-note", s.id, f"the row carries `{QUEUE_NOTE}` {bare.count(QUEUE_NOTE)} time(s), "
                                          f"{len(notes)} naming a session"))
            continue
        n = int(notes[0])
        named = sorted({p.strip() for p in CODE_SPAN.findall(s.row)} & authorities)
        if len(named) != 1:
            v.append(("queue-shape", s.id, f"names {len(named)} authorities ({', '.join(named) or 'none'}); "
                                           "a queued story names the one document the drain rewrites"))
        if not any(cites(s.row, d) for d in ids):
            v.append(("queue-shape", s.id, "cites no indexed decision, which the drain's version-log row must cite"))
        if n > current:
            v.append(("queue-future", s.id, f"`Queued: S{n}` names a session after this one, S{current}"))
        elif current > n + 1:
            v.append(("overdue", s.id, f"queued in S{n} for {', '.join(named) or 'no document'}, due by S{n + 1}; "
                                       f"this is S{current}"))
        if len(named) == 1:
            queue.append(Queued(s.id, n, named[0]))
    return v, queue


def stamps_for(a: Authority, first: dict[str, str], foreign: Callable[[Row], bool]) -> dict[int, str]:
    """{line: short hash} for each pending row whose first commit exists and which is this repository's."""
    return {r.line: first[r.version][:STAMP_LEN] for r in a.rows
            if r.commit == PENDING and r.version in first and not foreign(r)}


def stamp_text(text: str, stamps: dict[int, str]) -> str:
    """The document with the Commit cell of each row at a stamped line set to its hash."""
    lines = text.split("\n")
    for line, short in stamps.items():
        lines[line - 1] = re.sub(rf"\|\s*{PENDING}\s*\|\s*$", f"| {short} |", lines[line - 1])
    return "\n".join(lines)


# ==============================================================================
# Git — the one impure part, kept to two parsers the self-test can feed
# ==============================================================================

def log_commits(out: str, path: str) -> list[tuple[str, str]]:
    """[(full hash, path at that commit)], newest first, from
    `git log --follow --format=%x00%H --name-only -- <path>`."""
    commits = []
    for chunk in out.split("\x00")[1:]:
        lines = [ln for ln in chunk.splitlines() if ln.strip()]
        if lines:
            commits.append((lines[0], lines[1] if len(lines) > 1 else path))
    return commits


def renames_only(commits: list[tuple[str, str]], exists: Callable[[str, str], bool]) -> list[tuple[str, str]]:
    """The history cut at the first copy. `git log --follow` sets find-copies-harder, so a
    document made by copying another (a PRD from its template) would inherit that one's rows: where
    the path changes, the older path surviving in the commit that brought the newer one is a copy."""
    kept = commits[:1]
    for (newer, path), (older, was) in zip(commits, commits[1:]):
        if was != path and exists(newer, was):
            break
        kept.append((older, was))
    return kept


def batch_blobs(out: bytes) -> list[str | None]:
    """Each object's text from `git cat-file --batch` output, in input order; None where missing."""
    found: list[str | None] = []
    i = 0
    while i < len(out):
        nl = out.index(b"\n", i)
        header = out[i:nl].decode("utf-8", errors="replace")
        i = nl + 1
        if header.endswith((" missing", " ambiguous")):
            found.append(None)
            continue
        _, kind, size = header.rsplit(" ", 2)
        n = int(size)
        found.append(out[i:i + n].decode("utf-8", errors="replace") if kind == "blob" else None)
        i += n + 1
    return found


def git(*args: str, data: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, input=data, capture_output=True, check=False)


def first_commits(path: str) -> dict[str, str]:
    """{version: full hash of the first commit whose copy of the document holds it}, following
    renames. A document never committed has none. Raises HistoryUnavailable on a shallow clone,
    whose history ends early and would derive the wrong commit for every older row."""
    shallow = git("rev-parse", "--is-shallow-repository")
    if shallow.returncode != 0:
        raise HistoryUnavailable(shallow.stderr.decode(errors="replace").strip() or "not a git repository")
    if shallow.stdout.strip() == b"true":
        raise HistoryUnavailable("this clone is shallow; run `git fetch --unshallow`")
    out = git("log", "--follow", "--format=%x00%H", "--name-only", "--", path)
    if out.returncode != 0:
        raise HistoryUnavailable(out.stderr.decode(errors="replace").strip())
    commits = renames_only(log_commits(out.stdout.decode("utf-8", errors="replace"), path),
                           lambda h, p: git("cat-file", "-e", f"{h}:{p}").returncode == 0)
    if not commits:
        return {}
    blobs = batch_blobs(git("cat-file", "--batch", data="".join(f"{h}:{p}\n" for h, p in commits).encode()).stdout)
    seen: dict[str, str] = {}
    for (h, _), text in zip(reversed(commits), reversed(blobs)):
        if text is not None:
            for r in version_log(text)[0]:
                seen.setdefault(r.version, h)
    return seen


def gather() -> tuple[dict[str, str], dict[str, str], str, bool]:
    """Every markdown file git would commit that opens with frontmatter, the decision logs that
    exist, the tracker, and whether this is a project."""
    docs: dict[str, str] = {}
    for rel in session_closeout.committed_files():
        p = ROOT / rel
        if rel.endswith(".md") and p.is_file():
            text = p.read_text(encoding="utf-8", errors="replace")
            if text.startswith("---\n"):
                docs[rel] = text
    logs = {label: p.read_text(encoding="utf-8") for label, p in LOGS.items() if p.is_file()}
    tracker = TRACKER.read_text(encoding="utf-8") if TRACKER.is_file() else ""
    return docs, logs, tracker, PROFILE.is_file()


def cached(fn: Callable[[str], dict[str, str]]) -> Callable[[str], dict[str, str]]:
    memo: dict[str, dict[str, str]] = {}
    return lambda path: memo[path] if path in memo else memo.setdefault(path, fn(path))


def foreign_rule(logs: dict[str, str], project: bool) -> Callable[[Row], bool]:
    framework_ids = set(kb_freshness_scan.index_decisions(logs[FRAMEWORK_LOG])) if FRAMEWORK_LOG in logs else set()
    return lambda r: project and all(d in framework_ids for d in r.decisions)


# ==============================================================================
# Commands
# ==============================================================================

def cmd_check(listing: bool) -> int:
    docs, logs, tracker, project = gather()
    try:
        v, reach = check_tree(docs, logs, tracker, project, cached(first_commits))
    except HistoryUnavailable as e:
        print(f"doc_authority_scan: cannot verify a stored commit: {e}", file=sys.stderr)
        return 2
    if listing and reach:
        auths = reach["authorities"]
        print(f"authorities: {len(auths)} (the frontmatter is the registry)")
        for a in auths:
            newest = a.rows[0] if a.rows else None
            state = f"version {newest.version} of {newest.date}" if newest else "no readable version"
            print(f"  {a.path} — `{a.scope}` — {state}, {len(a.rows)} row(s)")
        print(f"rows pending a stamp: {reach['pending']}; template rows verified in the template: {reach['foreign']}")
        print(f"decisions dated {AFFECTS_FROM} or later: {reach['due']}; an authority they name recorded by a row: "
              f"{reach['by_row']}, queued by an open story: {reach['by_story']}")
    if not v:
        return 0
    print(f"doc_authority_scan: BLOCKED — {len(v)} violation(s)")
    for rule, where, msg in v:
        print(f"  [{rule}] {where}: {msg}")
    print("\nHow to fix:")
    for rule in dict.fromkeys(r for r, _, _ in v):
        print(f"  {rule}: {FIXES[rule]}")
    return 1


def cmd_stamp() -> int:
    docs, logs, _, project = gather()
    foreign = foreign_rule(logs, project)
    history = cached(first_commits)
    try:
        for path, text in sorted(docs.items()):
            a, _ = read_authority(path, text)
            if not a or not any(r.commit == PENDING for r in a.rows):
                continue
            stamps = stamps_for(a, history(path), foreign)
            if stamps:
                (ROOT / path).write_text(stamp_text(text, stamps), encoding="utf-8")
            for r in a.rows:
                if r.line in stamps:
                    print(f"stamped {path} version {r.version}: {stamps[r.line]}")
                elif r.commit == PENDING:
                    print(f"left {path} version {r.version} pending: "
                          f"{'a template row' if foreign(r) else 'not committed yet'}")
    except HistoryUnavailable as e:
        print(f"doc_authority_scan: cannot derive a commit: {e}", file=sys.stderr)
        return 2
    return 0


def cmd_queue() -> int:
    docs, logs, tracker, _ = gather()
    status = session_closeout.STATUS
    current = session_closeout.current_session(status.read_text(encoding="utf-8") if status.is_file() else "",
                                               lambda n: (session_closeout.HANDOFFS / f"KICKOFF_S{n}.md").is_file())
    v, queue = judge_queue(docs, logs, tracker, current)
    if current is not None:
        print(f"doc_queue: S{current}; " + (f"{len(queue)} story(ies) queued for the technical writer"
                                             if queue else "nothing queued for the technical writer"))
    for q in queue:
        print(f"  queued {q.story} (Queued: S{q.session}, due by S{q.session + 1}): `{q.document}`; "
              f"drain with `{DRAIN} {q.document}`")
    if not v:
        return 0
    print(f"doc_queue: BLOCKED — {len(v)} violation(s)")
    for rule, where, msg in v:
        print(f"  [{rule}] {where}: {msg}")
    print("\nHow to fix:")
    for rule in dict.fromkeys(r for r, _, _ in v):
        print(f"  {rule}: {FIXES[rule]}")
    return 1


def cmd_history(path: str) -> int:
    p = ROOT / path
    a, _ = read_authority(path, p.read_text(encoding="utf-8")) if p.is_file() else (None, [])
    if not a:
        print(f"doc_authority_scan: {path} is not an authority (no `authority:` frontmatter that parses)", file=sys.stderr)
        return 2
    try:
        first = first_commits(path)
    except HistoryUnavailable as e:
        print(f"doc_authority_scan: cannot derive a commit: {e}", file=sys.stderr)
        return 2
    print(f"{'version':<9}{'stored':<11}derived")
    for r in a.rows:
        derived = first[r.version][:STAMP_LEN] if r.version in first else "none: not committed"
        print(f"{r.version:<9}{r.commit:<11}{derived}")
    return 0


# ==============================================================================
# SELF-TEST — every rule against a passing and a failing fixture, in memory
# ==============================================================================

_FW = (
    "# Framework decisions\n\n## Decision Index\n\n| ID | Date | Title | Status |\n|---|---|---|---|\n"
    "| 2026-10-24-001 | 2026-10-24; amended 2026-10-26 | Amended later | APPROVED |\n"
    "| 2026-10-23-010 | 2026-10-23 | Changes the document | APPROVED |\n"
    "| 2026-10-22-002 | 2026-10-22 | The gate | APPROVED |\n"
    "| 2026-10-21-001 | 2026-10-21 | Older than the rule | APPROVED |\n\n---\n\n"
    "## Decision 2026-10-21-001: Older than the rule\n\n**Date:** 2026-10-21\n\n"
    "It changed `docs/a.md` and carries no Affects line.\n\n---\n\n"
    "## Decision 2026-10-22-002: The gate\n\n**Date:** 2026-10-22\n**Affects:** none\n\n---\n\n"
    "## Decision 2026-10-23-010: Changes the document\n\n**Date:** 2026-10-23\n"
    "**Affects:** `docs/b.md` §2, a path no authority holds,\n`docs/a.md` §3, rewritten\n**Builds:** TMPL-9.1\n\n---\n\n"
    "## Decision 2026-10-24-001: Amended later\n\n**Date:** 2026-10-24\n**Affects:** none\n\n---\n"
)
_PROJ = (
    "# Log\n\n## Decision Index\n\n| ID | Date | Title | Status |\n|---|---|---|---|\n"
    "| ACME-2026-10-25-001 | 2026-10-25 | The project's own | APPROVED |\n"
    "| [EXAMPLE] 2025-01-15-001 | 2025-01-15 | Sample | APPROVED |\n\n---\n\n"
    "## Decision [EXAMPLE] 2025-01-15-001: Sample\n\nNo Affects line.\n\n---\n\n"
    "## Decision ACME-2026-10-25-001: The project's own\n\n**Affects:** none\n\n---\n"
)
_TRACK = (
    "# Story Tracker\n\n## Epic: TMPL-9 — Documents\n\n"
    "| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |\n|---|---|---|---|---|---|\n"
    "| TMPL-9.1 | Restructure `docs/a.md` | Done | — | — | 2026-10-23-010 |\n"
    "| TMPL-9.2 | Something else | Not Started | — | — | 2026-10-22-002 |\n\n"
    "## Epic: INFRA-1 — Setup [EXAMPLE]\n\n| Story ID | Title | Status | D | S | P |\n|---|---|---|---|---|---|\n"
    "| INFRA-1.1 | Queue `docs/a.md` | Not Started | — | — | 2026-10-23-010 |\n"
)
_FM = "authority: the a scope\nimplements: [2026-10-24-001]\nverified: 2026-10-27\n"
_HEADER = "| Version | Date | Decision | Summary | Commit |\n|---|---|---|---|---|\n"
_ROW2 = "| 2 | 2026-10-24 | 2026-10-23-010 | Restructured §3 (TMPL-9.1) | pending |\n"
_ROW1 = "| 1 | 2026-10-22 | 2026-10-22-002 | fact: marked the authority for `the a scope` | abc1234 |\n"
_HIST = {"docs/a.md": {"1": "abc1234" + "0" * 33}}


def _doc(fm: str = _FM, rows: str = _ROW2 + _ROW1, header: str = _HEADER, tail: str = "",
         log: str = "## Version log") -> str:
    return f"---\n{fm}---\n\n# A\n\nBody.\n\n{log}\n\n{header}{rows}{tail}"


def _run(docs: dict | None = None, fw: str = _FW, proj: str = _PROJ, tracker: str = _TRACK,
         project: bool = False, hist: dict | None = None) -> list:
    docs = {"docs/a.md": _doc(), "docs/kb.md": "---\nname: an entry\n---\n\nNo log.\n"} if docs is None else docs
    hist = _HIST if hist is None else hist
    logs = {"sprint/decision-log.md": proj, FRAMEWORK_LOG: fw}
    try:
        return judge(docs, logs, tracker, project, lambda p: hist.get(p, {}))[0]
    except Exception as e:  # a crash is a failed fixture, never a crashed self-test
        return [("crash", "", f"{type(e).__name__}: {e}")]


def run_self_test() -> int:
    print("\nDocument Authority Self-Test")
    print("=" * 60)
    failures = total = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok:
            failures += 1
            if detail:
                print(f"        {detail}")

    def expect(label: str, found: list, *rules: str) -> None:
        got = {r for r, _, _ in found}
        check(label, got == set(rules), f"expected {sorted(rules)}, got {found}")

    def doc(**kw: str) -> dict:
        return {"docs/a.md": _doc(**kw)}

    # The registry
    expect("a clean authority passes", _run())
    expect("a file whose frontmatter claims no authority is not judged, a value holding `authority:` included",
           _run({"docs/n.md": "---\nname: x\ndescription: 'the authority: a word here'\n---\n\nNo log.\n"}))
    expect("frontmatter that claims authority and does not parse fails", _run(doc(fm="authority: a: b\nimplements: []\nverified: 2026-10-27\n")), "frontmatter")
    expect("a quoted `verified:` fails", _run(doc(fm=_FM.replace("2026-10-27", '"2026-10-27"'))), "frontmatter")
    expect("a `verified:` with a time fails", _run(doc(fm=_FM.replace("2026-10-27", "2026-10-27T10:00:00"))), "frontmatter")
    expect("`implements:` as a bare string fails", _run(doc(fm=_FM.replace("[2026-10-24-001]", "2026-10-24-001"))), "frontmatter")
    expect("an empty scope fails", _run(doc(fm=_FM.replace("the a scope", '""'))), "frontmatter")
    expect("two documents claiming one scope fail, however spelled",
           _run({"docs/a.md": _doc(), "docs/c.md": _doc(fm=_FM.replace("the a scope", "The A  scope"))},
                hist={"docs/a.md": _HIST["docs/a.md"], "docs/c.md": _HIST["docs/a.md"]}), "scope")
    expect("`implements:` naming an unindexed decision fails", _run(doc(fm=_FM.replace("2026-10-24-001", "2026-01-01-999"))), "unknown-id")
    expect("a row citing an unindexed decision fails", _run(doc(rows=_ROW2 + _ROW1.replace("2026-10-22-002", "2026-01-01-999"))), "unknown-id")
    expect("`verified:` before an amendment of a decision implemented fails", _run(doc(fm=_FM.replace("2026-10-27", "2026-10-25"))), "stale")

    # The version log
    expect("no version log fails, and the decision naming the document is unrecorded", _run(doc(log="## Notes", header="", rows="")), "no-log", "unrecorded")
    expect("a version log that is not the last section fails", _run(doc(tail="\n## Appendix\n\nMore.\n")), "no-log", "unrecorded")
    expect("a version log inside a fenced block is not the section",
           _run(doc(log="```\n## Version log\n", tail="```\n")), "no-log", "unrecorded")
    expect("a version log with no rows fails", _run(doc(rows="")), "no-log", "unrecorded")
    expect("columns other than the five fail", _run(doc(header="| Version | Date | Summary | Commit |\n|---|---|---|---|\n")), "log-header", "unrecorded")
    expect("a version that is no number fails", _run(doc(rows=_ROW2 + _ROW1.replace("| 1 |", "| v1 |"))), "row")
    expect("a date that is no date fails", _run(doc(rows=_ROW2 + _ROW1.replace("2026-10-22 | 2026", "2026-13-01 | 2026"))), "row")
    expect("a row citing no decision fails", _run(doc(rows=_ROW2 + _ROW1.replace("| 2026-10-22-002 |", "| — |"))), "row")
    expect("an empty summary fails", _run(doc(rows=_ROW2 + "| 1 | 2026-10-22 | 2026-10-22-002 |  | abc1234 |\n")), "row")
    expect("a commit that is neither pending nor a hash fails", _run(doc(rows=_ROW2 + _ROW1.replace("abc1234", "abc"))), "row")
    expect("a row with four cells fails", _run(doc(rows=_ROW2 + "| 1 | 2026-10-22 | 2026-10-22-002 | abc1234 |\n")), "row")
    expect("versions rising down the table fail", _run(doc(rows=_ROW1 + _ROW2)), "order")
    expect("a repeated version fails", _run(doc(rows=_ROW2 + _ROW1.replace("| 1 |", "| 2 |").replace("abc1234", "pending"))), "order")
    expect("a date rising down the table fails", _run(doc(rows=_ROW2.replace("2026-10-24", "2026-10-20") + _ROW1)), "order")

    # The fact marker
    expect("a summary with neither marker nor story fails", _run(doc(rows=_ROW2 + _ROW1.replace("fact: marked", "Marked"))), "unmarked")
    expect("`fact:` with no fact stated fails", _run(doc(rows=_ROW2 + _ROW1.replace("for `the a scope`", "for the scope"))), "unmarked")
    expect("`fact:` with a count passes", _run(doc(rows=_ROW2 + _ROW1.replace("for `the a scope`", "with 3 sections"))))
    expect("a story citation whose story cites another decision fails", _run(doc(rows=_ROW2.replace("TMPL-9.1", "TMPL-9.2") + _ROW1)), "unmarked")
    expect("a citation of a story absent from the tracker fails", _run(doc(rows=_ROW2.replace("TMPL-9.1", "TMPL-9.7") + _ROW1)), "unmarked")
    expect("a story in an [EXAMPLE] epic is no citation", _run(doc(rows=_ROW2.replace("TMPL-9.1", "INFRA-1.1") + _ROW1)), "unmarked")

    # Affects
    expect("a decision on or after the cutoff with no Affects line fails",
           _run(fw=_FW.replace("**Date:** 2026-10-22\n**Affects:** none\n", "**Date:** 2026-10-22\n")), "no-affects")
    expect("an Affects line with no value fails", _run(fw=_FW.replace("**Date:** 2026-10-24\n**Affects:** none", "**Date:** 2026-10-24\n**Affects:**")), "no-affects")
    expect("an indexed decision with no body fails",
           _run(fw=_FW.replace("## Decision 2026-10-24-001: Amended later\n\n**Date:** 2026-10-24\n**Affects:** none\n\n---\n", "")), "no-affects")
    expect("a project decision on or after the cutoff with no Affects line fails",
           _run(proj=_PROJ.replace("**Affects:** none", "No line.")), "no-affects")
    expect("a decision older than the cutoff reads as none, whatever its body names",
           _run(fw=_FW.replace("It changed `docs/a.md` and carries no Affects line.", "**Affects:** `docs/a.md`")))
    expect("an authority named on the Affects continuation line with no row and no story is unrecorded",
           _run(doc(rows=_ROW1), tracker=_TRACK.replace("TMPL-9.1 | Restructure `docs/a.md`", "TMPL-9.1 | Restructure")), "unrecorded")
    expect("a story Done queues nothing, nor one in an [EXAMPLE] epic", _run(doc(rows=_ROW1)), "unrecorded")
    expect("an open story citing the decision and the document queues the change",
           _run(doc(rows=_ROW1), tracker=_TRACK.replace("| Done |", "| Not Started |")))
    expect("an open story citing the decision but not the document queues nothing",
           _run(doc(rows=_ROW1), tracker=_TRACK.replace("| Done |", "| Not Started |").replace("Restructure `docs/a.md`", "Restructure")), "unrecorded")
    expect("an open story citing the document under another decision queues nothing",
           _run(doc(rows=_ROW1), tracker=_TRACK.replace("Something else", "Edit `docs/a.md`")), "unrecorded")
    check("a decision ID inside a prefixed project ID is not cited", not cites("| ACME-2026-10-25-001 |", "2026-10-25-001")
          and cites("| 2026-10-25-001 |", "2026-10-25-001"))

    # Commits
    expect("a stored hash that is not the commit that introduced the row fails", _run(hist={"docs/a.md": {"1": "fff" + "0" * 37}}), "commit")
    expect("a stored hash on a row never committed fails", _run(hist={}), "commit")
    expect("in a project, a row citing only framework decisions is the template's", _run(project=True, hist={}))
    expect("in a project, a row citing the project's decision is verified",
           _run(doc(rows=_ROW2 + _ROW1.replace("2026-10-22-002", "ACME-2026-10-25-001")), project=True, hist={}), "commit")

    # The template's rows and decisions in a project (decision 2026-10-23-015)
    born = "# Story Tracker\n\n## Epic: INFRA-1" + _TRACK.split("## Epic: INFRA-1")[1]   # a project's: no TMPL story
    own = "| 3 | 2026-10-26 | {} | Restructured again | pending |\n"
    proj_names = _PROJ.replace("## Decision ACME-2026-10-25-001: The project's own\n\n**Affects:** none",
                               "## Decision ACME-2026-10-25-001: The project's own\n\n**Affects:** `docs/a.md` §4")
    expect("in a project, the template's row citing a story only the template's tracker holds passes",
           _run(project=True, hist={}, tracker=born))
    expect("in a project, a framework decision queued only by the template's story passes",
           _run(doc(rows=_ROW1), project=True, hist={}, tracker=born))
    expect("in a project, the project's own row is still held to its marker",
           _run(doc(rows=own.format("ACME-2026-10-25-001") + _ROW2 + _ROW1), project=True, hist={}, tracker=born), "unmarked")
    expect("in a project, a row citing a framework and a project decision is the project's",
           _run(doc(rows=own.format("2026-10-23-010, ACME-2026-10-25-001") + _ROW2 + _ROW1), project=True, hist={},
                tracker=born), "unmarked")
    expect("in a project, the project's own decision naming an authority is still held to its record",
           _run(proj=proj_names, project=True, hist={}, tracker=born), "unrecorded")
    expect("in a project, the project's own decision with no Affects line still fails",
           _run(proj=_PROJ.replace("**Affects:** none", "No line."), project=True, hist={}, tracker=born), "no-affects")
    expect("in the template, the same decision queued by no open story is unrecorded", _run(doc(rows=_ROW1), tracker=born), "unrecorded")
    expect("an unreadable decision index fails, never reads as none", _run(fw=_FW.replace("## Decision Index", "## Decisions")), "index")

    # The writer's queue (decision 2026-10-23-016)
    def queue(row: str, current: int | None = 9, docs: dict | None = None, epic: str = "TMPL-9 — Documents",
              fw: str = _FW) -> tuple[list, list]:
        tracker = (f"# Story Tracker\n\n## Epic: {epic}\n\n| Story ID | Title | Status | Dependencies | Required Standards "
                   f"| PRD Ref |\n|---|---|---|---|---|---|\n{row}\n")
        try:
            return judge_queue({"docs/a.md": _doc()} if docs is None else docs,
                               {"sprint/decision-log.md": _PROJ, FRAMEWORK_LOG: fw}, tracker, current)
        except Exception as e:  # a crash is a failed fixture, never a crashed self-test
            return [("crash", "", f"{type(e).__name__}: {e}")], []

    queued = "| TMPL-9.3 | Rewrite `docs/a.md` §3, Queued: S8 | Not Started | — | — | 2026-10-23-010 |"
    found, q = queue(queued)
    expect("a story queued in the session before this one is due, and passes", found)
    check("the queue names the story, its session and its document", q == [Queued("TMPL-9.3", 8, "docs/a.md")], str(q))
    expect("a story queued in this session passes", queue(queued.replace("S8", "S9"))[0])
    expect("a story older than one session fails", queue(queued.replace("S8", "S7"))[0], "overdue")
    expect("a Blocked story is still open, and fails when overdue",
           queue(queued.replace("S8", "S7").replace("Not Started", "Blocked"))[0], "overdue")
    found, q = queue(queued.replace("S8", "S2").replace("Not Started", "Done"))
    expect("a Done story is drained, whatever its note says", found)
    check("a drained story leaves the queue", q == [], str(q))
    expect("a note naming a session after this one fails", queue(queued.replace("S8", "S12"))[0], "queue-future")
    expect("a note naming no session fails", queue(queued.replace("Queued: S8", "Queued: soon"))[0], "queue-note")
    expect("two notes on one row fail", queue(queued.replace("Queued: S8", "Queued: S8, Queued: S9"))[0], "queue-note")
    found, q = queue(queued.replace("Queued: S8", "the `Queued: S2` convention"))
    expect("a note quoted in a code span is the convention, not a note", found)
    check("a quoted note queues nothing", q == [], str(q))
    expect("a queued story naming no authority fails", queue(queued.replace("`docs/a.md`", "`docs/b.md`"))[0], "queue-shape")
    two = {"docs/a.md": _doc(), "docs/c.md": _doc(fm=_FM.replace("the a scope", "the c scope"))}
    expect("a queued story naming two authorities fails",
           queue(queued.replace("`docs/a.md`", "`docs/a.md` and `docs/c.md`"), docs=two)[0], "queue-shape")
    expect("a queued story citing no indexed decision fails", queue(queued.replace("2026-10-23-010", "—"))[0], "queue-shape")
    expect("a story in an [EXAMPLE] epic is not judged",
           queue(queued.replace("TMPL-9.3", "INFRA-1.4").replace("S8", "S1"), epic="INFRA-1 — Setup [EXAMPLE]")[0])
    expect("with no session known the gate fails, never passes on nothing", queue(queued, current=None)[0], "session")
    expect("an unreadable decision index fails the queue too", queue(queued, fw=_FW.replace("## Decision Index", "## Decisions"))[0], "index")

    # The approval gate (decisions 2026-10-23-008 and 2026-10-23-014)
    prd = ("---\nauthority: product requirements — Acme\nimplements: []\nverified: 2026-10-27\nstatus: approved\n"
           f"template: '1.0'\n---\n\n# PRD\n\n## Version log\n\n{_HEADER}"
           "| 1.1 | 2026-10-26 | ACME-2026-10-25-001 | fact: `FR-2` added | pending |\n"
           "| 1.0 | 2026-10-25 | ACME-2026-10-25-001 | fact: approved, made from `docs/templates/prd.md` 1.0 | pending |\n")
    arch = (prd.replace("product requirements", "architecture").replace("template: '1.0'\n", "template: '1.0'\nprd: '1.1'\n")
            .split("| 1.1 |")[0] + "| 1.0 | 2026-10-26 | ACME-2026-10-25-001 | fact: approved, built from PRD 1.1 | pending |\n")
    both = {"docs/prd/prd.md": prd, "docs/architecture/architecture.md": arch}

    def approval(docs: dict | None = None, proj: str = _PROJ, tracker: str = _TRACK, project: bool = True,
                 fw: str = _FW) -> list:
        try:
            return judge_approval(both if docs is None else docs, {"sprint/decision-log.md": proj, FRAMEWORK_LOG: fw},
                                  tracker, project)
        except Exception as e:  # a crash is a failed fixture, never a crashed self-test
            return [("crash", "", f"{type(e).__name__}: {e}")]

    def skipping(stages: str, status: str = "APPROVED") -> str:
        return (_PROJ.replace("| [EXAMPLE] 2025-01-15-001", f"| ACME-2026-10-26-001 | 2026-10-26 | Skip | {status} |\n"
                              "| [EXAMPLE] 2025-01-15-001")
                + f"\n## Decision ACME-2026-10-26-001: Skip\n\n**Skips:** {stages}\n**Affects:** none\n\n---\n")

    only_arch, only_prd = {"docs/architecture/architecture.md": arch}, {"docs/prd/prd.md": prd}
    expect("an approved PRD and an architecture built from its newest version pass", approval())
    expect("a real epic with no PRD fails", approval(only_arch), "approval")
    expect("a real epic with no architecture fails", approval(only_prd), "approval")
    expect("a PRD still a draft is no approval",
           approval({**only_arch, "docs/prd/prd.md": "---\nstatus: draft\ntemplate: '1.0'\n---\n\n# PRD\n"}), "approval")
    expect("a PRD reopened for revision, its authority and rows kept, stands at its last approved version",
           approval({**only_arch, "docs/prd/prd.md": prd.replace("status: approved", "status: draft")}))
    expect("an architecture reopened for revision is not held to the PRD's newest version",
           approval({**only_prd, "docs/architecture/architecture.md":
                     arch.replace("status: approved", "status: draft").replace("prd: '1.1'", "prd: '1.0'")}))
    expect("a document that claims the authority with no row was never approved",
           approval({**only_arch, "docs/prd/prd.md": prd.replace("status: approved", "status: draft").split("| 1.1 |")[0]}),
           "approval")
    expect("a status other than approved or draft stands for nothing",
           approval({**only_arch, "docs/prd/prd.md": prd.replace("status: approved", "status: final")}), "approval")
    found = approval({**only_arch, "docs/prd/prd.md": "---\nstatus: approved\ntemplate: '1.0'\n---\n\n# PRD\n"})
    check("`status: approved` without the authority line fails, naming the document",
          {r for r, _, _ in found} == {"approval"} and any(w == "docs/prd/prd.md" for _, w, _ in found), str(found))
    expect("an approved PRD outside `docs/prd/` is not the project's PRD", approval({**only_arch, "docs/other/prd.md": prd}), "approval")
    expect("two approved PRDs fail", approval({**both, "docs/prd/two.md": prd.replace("— Acme", "— Acme two")}), "approval")
    expect("an architecture built from an older PRD version fails",
           approval({**only_prd, "docs/architecture/architecture.md": arch.replace("prd: '1.1'", "prd: '1.0'")}), "prd-version")
    expect("an unquoted `prd:` is a number, never the version",
           approval({**only_prd, "docs/architecture/architecture.md": arch.replace("prd: '1.1'", "prd: 1.1")}), "prd-version")
    expect("a logged skip of the PRD passes without one, and the architecture's `prd:` is not read",
           approval({"docs/architecture/architecture.md": arch.replace("prd: '1.1'", "prd: '9.9'")}, proj=skipping("prd")))
    expect("a logged skip of the architecture passes without one", approval(only_prd, proj=skipping("architecture")))
    expect("one decision may skip both", approval({}, proj=skipping("prd, architecture")))
    expect("a skip whose decision is not APPROVED counts for nothing", approval(only_prd, proj=skipping("architecture", "PROPOSED")),
           "approval")
    expect("a skip naming no launch stage fails", approval(proj=skipping("everything")), "skips")
    expect("a skip of a stage the gate does not hold passes, and approves nothing",
           approval(only_prd, proj=skipping("team")), "approval")
    expect("a skip of the ungated stages beside approved documents passes", approval(proj=skipping("intake, planning")))
    expect("a skip in the framework's log counts for nothing",
           approval(only_prd, fw=_FW.replace("| 2026-10-24-001 |", "| 2026-10-26-009 | 2026-10-26 | Skip | APPROVED |\n| 2026-10-24-001 |")
                    + "\n## Decision 2026-10-26-009: Skip\n\n**Skips:** architecture\n**Affects:** none\n"), "approval")
    expect("the template is not judged", approval({}, project=False))
    expect("a project before its first real epic is not judged", approval({}, tracker=born))
    expect("an unreadable decision index fails the approval too", approval(proj=_PROJ.replace("## Decision Index", "## Decisions")),
           "index")
    logs = {"sprint/decision-log.md": _PROJ, FRAMEWORK_LOG: _FW}
    expect("the commit's check runs the approval gate beside the authority rules",
           check_tree({"docs/a.md": _doc()}, logs, _TRACK, True, lambda p: {})[0], "approval")
    expect("and the authority rules beside it",
           check_tree({"docs/a.md": _doc(rows=own.format("ACME-2026-10-25-001") + _ROW2 + _ROW1), **both}, logs, _TRACK, True,
                      lambda p: {})[0], "unmarked")

    # --stamp and the git readers
    try:
        stamp_checks(check)
    except Exception as e:  # a crash is a failed fixture, never a crashed self-test
        check("the --stamp and git-reader fixtures run", False, f"{type(e).__name__}: {e}")

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def stamp_checks(check: Callable[..., None]) -> None:
    auth, _ = read_authority("docs/a.md", _doc(rows=_ROW2 + _ROW1.replace("abc1234", "pending")))
    first = {"1": "abc1234" + "0" * 33, "2": "def5678" + "0" * 33}
    stamps = stamps_for(auth, first, lambda r: False)
    check("--stamp fills every pending row whose commit exists", sorted(stamps.values()) == ["abc1234", "def5678"], str(stamps))
    check("--stamp leaves a row whose version no commit holds", stamps_for(auth, {"1": first["1"]}, lambda r: False) == {auth.rows[1].line: "abc1234"})
    check("--stamp leaves the template's rows in a project", stamps_for(auth, first, lambda r: True) == {})
    stamped = stamp_text(_doc(rows=_ROW2 + _ROW1.replace("abc1234", "pending")), stamps)
    restamped, _ = read_authority("docs/a.md", stamped)
    check("a stamped row reads back with its hash, and the document is otherwise unchanged",
          [r.commit for r in restamped.rows] == ["def5678", "abc1234"]
          and stamped.replace("def5678", "pending").replace("abc1234", "pending") == _doc(rows=_ROW2 + _ROW1.replace("abc1234", "pending")))
    log = "\x00aaa\n\ndocs/new.md\n\x00bbb\n\ndocs/old.md\n"
    check("the git log reader follows a rename", log_commits(log, "docs/new.md") == [("aaa", "docs/new.md"), ("bbb", "docs/old.md")])
    moved = [("ccc", "docs/new.md"), ("aaa", "docs/new.md"), ("bbb", "docs/old.md"), ("ddd", "docs/old.md")]
    check("a rename is followed past: the old path is gone from the commit that brought the new",
          renames_only(moved, lambda h, p: False) == moved)
    check("a copy is not: a document made from a template never inherits the template's rows",
          renames_only(moved, lambda h, p: (h, p) == ("aaa", "docs/old.md")) == moved[:2])
    batch = b"1111 blob 5\nhello\nbbb:docs/old.md missing\n"
    check("the cat-file reader keeps each object in order and a missing one as None", batch_blobs(batch) == ["hello", None])


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    if "--stamp" in argv:
        return cmd_stamp()
    if "--queue" in argv:
        return cmd_queue()
    if "--history" in argv:
        i = argv.index("--history")
        if i + 1 >= len(argv):
            print("usage: doc_authority_scan.py --history <doc>", file=sys.stderr)
            return 2
        return cmd_history(argv[i + 1])
    return cmd_check("--list" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
