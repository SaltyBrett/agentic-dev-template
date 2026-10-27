#!/usr/bin/env python3
"""
issue_log.py — every issue reported, filed through one writer and held to its template.

WHAT IT DOES
------------
  --file              Files an issue: the next ID, its index row and its entry, from the template.
                      Each field comes from its flag; in a terminal, one not given is asked for, and
                      outside one the run is refused with the missing flags named. A person and an
                      agent file the same way; `--as human` or `--as agent` records which.
  --update <ID>       Changes an issue's fields the same way, its index row with them.
  --check             The gate, on every commit: each entry in the template's form; the index in
                      step with the entries; IDs one prefix, numbered from 1 with no gap; each
                      status borne out by the named stories' status in the tracker; every named
                      story and decision existing; every issue the code review log names held here.
  --report            Issues by status, kind, severity and reporter; the open ones by age, each with
                      its stories' status.
  --self-test         In-memory fixtures for every rule, and the law read from the standard.

The log is re-rendered whole by the writer, from one renderer, so the index cannot drift from the
entries it writes. The `[EXAMPLE]` entry is rendered by the same function: the template a reader
sees is the one the gate holds entries to.

THE LAW
-------
The fields, kinds, severities, statuses and sections are section 12 of
docs/standards/sprint_management_standard_v1.0.md; the self-test reads that section and fails when
the lists here differ from it. A project with no issue log has no issues and passes.

Usage:
    python3 scripts/issue_log.py --file [--title ... --by <name> --as human|agent --kind ... --severity ...
                                         --what ... --expected ... --steps ... --impact ...]
    python3 scripts/issue_log.py --update <ID> [--status ... --stories ... --decisions ... --resolved-by ...
                                                --resolution ... --severity ... --title ...]
    python3 scripts/issue_log.py --check | --report | --self-test
Exit 0 = clean, 1 = a violation or a refusal, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import collections
import datetime
import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import session_closeout  # noqa: E402 — the tracker's stories, the decision IDs and the section parser, one parse each

ROOT = Path(__file__).resolve().parents[1]
LOG = "sprint/issue-log.md"
TRACKER = "sprint/story-tracker.md"
REVIEW_LOG = "docs/code_review_log.md"
STANDARD = "docs/standards/sprint_management_standard_v1.0.md"

# The template's form: section 12 of the sprint management standard, which the self-test reads.
FIELDS = ("Title", "Reported", "Reporter", "Kind", "Severity", "Status", "Stories", "Decisions", "Resolved by")
KINDS = ("bug", "request", "risk")
SEVERITIES = ("critical", "high", "medium", "low")
STATUSES = ("Open", "Triaged", "In Progress", "Resolved", "Closed", "Won't fix")
SECTIONS = ("What happened", "Expected", "Steps to reproduce", "Impact", "Resolution")
BUG_ONLY = "Steps to reproduce"
RESOLVED = ("Resolved", "Closed")
DECLINED = "Won't fix"
REPORTER_KINDS = ("human", "agent")
INDEX_COLUMNS = ("ID", "Reported", "Title", "Kind", "Severity", "Status", "Stories")
NONE = "none"
EXAMPLE = session_closeout.EXAMPLE_MARK
INDEX_HEADING = "Issue Index"
CLOSING = "<!-- File issues with `python3 scripts/issue_log.py --file` or `/issue`; the writer keeps the index and the entries in step. -->"

ISSUE_ID = re.compile(r"\b[A-Z][A-Z0-9]*-ISS-\d+\b")
ISSUE_HEADING = re.compile(r"^Issue (\[EXAMPLE\] )?([A-Z][A-Z0-9]*-ISS-\d+)\s*$")
FIELD = re.compile(r"^\*\*([^*]+):\*\* ?(.*)$")
PREFIX_LINE = re.compile(r"^\*\*Prefix:\*\* ([A-Z][A-Z0-9]*)\s*$", re.M)   # written at birth, the project's story prefix
H3 = re.compile(r"^### (.+?)\s*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REPORTER = re.compile(r"^\S.* \((human|agent)\)$")
COMMIT = re.compile(r"^[0-9a-f]{7,40}$")
STORY = re.compile(r"^[A-Z][A-Z0-9]*-\d+\.\d+$")
DECISION = re.compile(r"^(?:[A-Z][A-Z0-9]*-)?\d{4}-\d{2}-\d{2}-\d{3}$")


class Issue(NamedTuple):
    id: str
    example: bool
    fields: dict[str, str]
    order: tuple[str, ...]          # the field names as written, in order
    sections: dict[str, str]
    section_order: tuple[str, ...]


class Cancelled(Exception):
    """The person at the terminal ended the prompts, Ctrl-D or Ctrl-C: nothing is written."""


class Log(NamedTuple):
    preamble: str
    index: dict[str, dict[str, str]]   # ID -> its row, by column
    issues: list[Issue]
    problems: list[str]                # what the parse itself could not read


def items(value: str) -> list[str]:
    """A list field's items; `none` lists nothing."""
    return [] if value.strip() == NONE else [v.strip() for v in value.split(",") if v.strip()]


def key(issue: Issue) -> str:
    """How the index names an issue: the example keeps its mark, so it never collides with a real ID."""
    return f"{EXAMPLE} {issue.id}" if issue.example else issue.id


def number(issue_id: str) -> int:
    return int(issue_id.rsplit("-", 1)[1])


def prefix(issue_id: str) -> str:
    return issue_id.split("-ISS-", 1)[0]


# ==============================================================================
# Parse and render
# ==============================================================================

def parse_body(issue_id: str, example: bool, body: str) -> Issue:
    fields: dict[str, str] = {}
    order: list[str] = []
    sections: dict[str, list[str]] = {}
    current = None
    for line in body.splitlines():
        if (m := H3.match(line)):
            current = m.group(1)
            sections[current] = []
        elif current is None:
            if (m := FIELD.match(line)):
                fields[m.group(1)] = m.group(2).strip()
                order.append(m.group(1))
        elif line.strip() != "---" and not line.startswith("<!--"):
            sections[current].append(line)
    return Issue(issue_id, example, fields, tuple(order), {k: "\n".join(v).strip() for k, v in sections.items()},
                 tuple(sections))


def parse_index(body: str) -> tuple[dict[str, dict[str, str]], list[str]]:
    rows: dict[str, dict[str, str]] = {}
    problems: list[str] = []
    for line in body.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if len(cells) != len(INDEX_COLUMNS) or cells[0] in ("ID",) or set(cells[0]) <= set("-: "):
            continue
        name = " ".join(cells[0].split())
        if name in rows:
            problems.append(f"the index holds {name} twice")
        rows[name] = dict(zip(INDEX_COLUMNS, cells))
    return rows, problems


def parse(text: str) -> Log:
    preamble, secs = session_closeout.sections(text)
    index: dict[str, dict[str, str]] = {}
    issues: list[Issue] = []
    problems: list[str] = []
    seen_index = False
    for heading, body in secs:
        if heading == INDEX_HEADING:
            seen_index = True
            index, problems = parse_index(body)
        elif (m := ISSUE_HEADING.match(heading)):
            issues.append(parse_body(m.group(2), bool(m.group(1)), body))
        else:
            problems.append(f"`## {heading}` is neither the index nor an issue")
    if not seen_index:
        problems.append(f"no `## {INDEX_HEADING}` section")
    return Log(preamble, index, issues, problems)


def render_entry(issue: Issue) -> str:
    head = f"## Issue {EXAMPLE + ' ' if issue.example else ''}{issue.id}\n\n"
    fields = "".join(f"**{name}:** {issue.fields.get(name, NONE)}\n" for name in FIELDS)
    wanted = [s for s in SECTIONS if s != BUG_ONLY or issue.fields.get("Kind") == "bug"]
    body = "".join(f"\n### {s}\n\n{issue.sections.get(s) or NONE}\n" for s in wanted)
    return head + fields + body


def index_row(issue: Issue) -> str:
    cells = [key(issue)] + [issue.fields.get(c, "") for c in INDEX_COLUMNS[1:]]
    return "| " + " | ".join(cells) + " |"


def render(preamble: str, issues: list[Issue]) -> str:
    table = ("| " + " | ".join(INDEX_COLUMNS) + " |\n|" + "|".join("-" * (len(c) + 2) for c in INDEX_COLUMNS) + "|\n"
             + "".join(index_row(i) + "\n" for i in issues))
    entries = "".join(render_entry(i) + "\n---\n\n" for i in issues)
    return f"{preamble.rstrip()}\n\n## {INDEX_HEADING}\n\n{table}\n---\n\n{entries}{CLOSING}\n"


PREAMBLE = f"""# Issue Log

**Purpose:** Every issue reported against the project, from filing to resolution

> **GOVERNED BY** `{STANDARD}` section 12: the fields, the statuses and their links.
>
> **READ SELECTIVELY (index-first).** Read the **{INDEX_HEADING}**, then only the entries the task
> needs. File through the writer, which allocates the ID and keeps the index and the entries in step:
> `python3 scripts/issue_log.py --file`, run by a person in a terminal or by an agent through the
> `/issue` skill. `--update <ID>` changes an issue; `--report` reports. The `[EXAMPLE]` entry shows
> the template every entry follows, and the `issue-log` gate refuses one that departs from it.

---"""

# Numbered zero, so the first real issue is 1 and never takes the example's ID, whatever the
# project's prefix.
EXAMPLE_ISSUE = Issue(
    id="ACME-ISS-0", example=True,
    fields={"Title": "The nightly export drops rows with no region", "Reported": "2025-01-15",
            "Reporter": "Chair (human)", "Kind": "bug", "Severity": "high", "Status": "Resolved",
            "Stories": "ACME-2.3", "Decisions": NONE, "Resolved by": "1a2b3c4"},
    order=FIELDS,
    sections={"What happened": "The nightly export wrote 9,812 of 10,000 rows. The 188 missing rows had no region.",
              "Expected": "Every row exported, a missing region written as an empty field.",
              "Steps to reproduce": "1. Load a table holding a row with no region.\n2. Run the export.\n"
                                    "3. Count the rows in the file.",
              "Impact": "The downstream totals undercount by about 2% each night.",
              "Resolution": "ACME-2.3 writes a missing region as an empty field and adds a test holding one."},
    section_order=SECTIONS)


def skeleton(story_prefix: str | None = None) -> str:
    """The log a project is born with, its story prefix recorded for the writer, or the template's,
    with no prefix: the example alone either way."""
    head = PREAMBLE.replace("\n\n> **GOVERNED BY**", f"\n**Prefix:** {story_prefix}\n\n> **GOVERNED BY**", 1) if story_prefix else PREAMBLE
    return render(head, [EXAMPLE_ISSUE])


def log_prefix(log: Log) -> str | None:
    m = PREFIX_LINE.search(log.preamble)
    return m.group(1) if m else None


# ==============================================================================
# Rules — pure
# ==============================================================================

def _value_problem(name: str, value: str) -> str | None:
    """Why a field's value is outside the template's, or None."""
    allowed = {"Kind": KINDS, "Severity": SEVERITIES, "Status": STATUSES}
    patterns = {"Reported": DATE, "Reporter": REPORTER}
    lists = {"Stories": STORY, "Decisions": DECISION}
    if name in allowed and value not in allowed[name]:
        return f"{name} is {value!r}, not one of {', '.join(allowed[name])}"
    if name in patterns and not patterns[name].match(value):
        return f"{name} is {value!r}; the template's form is " + ("YYYY-MM-DD" if name == "Reported" else "a name, then (human) or (agent)")
    if name in lists and any(not lists[name].match(v) for v in items(value)):
        return f"{name} is {value!r}: its items are IDs, comma-separated, or `none`"
    if name == "Resolved by" and value != NONE and not COMMIT.match(value):
        return f"Resolved by is {value!r}, not a commit hash or `none`"
    if name == "Title" and (not value or value == NONE):
        return "Title is empty"
    return None


def entry_problems(issue: Issue) -> list[str]:
    """Where an entry departs from the template's form."""
    problems = []
    if issue.order != FIELDS:
        problems.append(f"its fields are {list(issue.order)}; the template's are {list(FIELDS)}, in that order")
    problems += [p for name in FIELDS if name in issue.fields and (p := _value_problem(name, issue.fields[name]))]
    wanted = tuple(s for s in SECTIONS if s != BUG_ONLY or issue.fields.get("Kind") == "bug")
    if issue.section_order != wanted:
        problems.append(f"its sections are {list(issue.section_order)}; a {issue.fields.get('Kind', '?')}'s are {list(wanted)}")
    empty = [s for s in wanted if s != "Resolution" and issue.sections.get(s, NONE) in ("", NONE)]
    if empty:
        problems.append(f"{', '.join(empty)} holds no text")
    return problems


def bears_out(issue: Issue, stories: dict[str, str]) -> str | None:
    """Why the issue's status is not what its links and the tracker bear out, or None."""
    f = issue.fields
    status, named, decisions = f.get("Status"), items(f.get("Stories", NONE)), items(f.get("Decisions", NONE))
    states = [stories[s] for s in named if s in stories]
    started = any(s in ("In Progress", "Done") for s in states)
    done = all(s == "Done" for s in states)
    closing = status in RESOLVED or status == DECLINED
    if (f.get("Resolved by", NONE) != NONE) != (status in RESOLVED):
        return f"{status} with Resolved by {f.get('Resolved by')!r}: a commit is named once Resolved or Closed, and only then"
    if (issue.sections.get("Resolution", NONE) != NONE) != closing:
        return f"{status} with Resolution {'written' if not closing else 'none'}: it is written once Resolved, Closed or Won't fix, and only then"
    rule = {"Open": (not named and not decisions, "Open names no story and no decision"),
            "Triaged": ((named or decisions) and not started, "Triaged names a story or a decision, none of its stories started"),
            "In Progress": (started and not done, "In Progress has a named story In Progress or Done, not every one Done"),
            "Resolved": ((named or decisions) and done, "Resolved has every named story Done"),
            "Closed": ((named or decisions) and done, "Closed has every named story Done"),
            DECLINED: ("In Progress" not in states, "Won't fix has no named story In Progress")}
    holds, law = rule.get(status, (True, ""))
    return None if holds else f"{status}, but its stories are {dict(zip(named, states)) or 'none'}: {law}"


def link_problems(issue: Issue, stories: dict[str, str], decisions: set[str] | None) -> list[str]:
    problems = [f"names {s}, no story in the tracker" for s in items(issue.fields.get("Stories", NONE)) if s not in stories]
    if decisions is not None:
        problems += [f"names {d}, no decision in either log" for d in items(issue.fields.get("Decisions", NONE))
                     if d not in decisions]
    return problems


def index_problems(index: dict[str, dict[str, str]], issues: list[Issue]) -> list[str]:
    problems = []
    entries = {key(i): i for i in issues}
    problems += [f"the index names {k}, which has no entry" for k in index if k not in entries]
    problems += [f"{k} has no index row" for k in entries if k not in index]
    for k in index.keys() & entries.keys():
        diff = [c for c in INDEX_COLUMNS[1:] if index[k].get(c) != entries[k].fields.get(c)]
        if diff:
            problems.append(f"{k}'s index row disagrees with its entry on {', '.join(diff)}")
    return problems


def sequence_problems(issues: list[Issue]) -> list[str]:
    real = [i.id for i in issues if not i.example]
    problems = []
    dupes = [k for k, n in collections.Counter(real).items() if n > 1]
    if dupes:
        problems.append(f"{', '.join(dupes)} filed more than once")
    prefixes = {prefix(k) for k in real}
    if len(prefixes) > 1:
        problems.append(f"IDs under {len(prefixes)} prefixes, {', '.join(sorted(prefixes))}; a log has one")
    numbers = sorted(number(k) for k in set(real))
    if numbers != list(range(1, len(numbers) + 1)):
        problems.append(f"IDs numbered {numbers}, not 1 to {len(numbers)}: an issue is never deleted, Won't fix closes it")
    return problems


def review_problems(review_text: str | None, held: set[str]) -> list[str]:
    """Every issue the code review log names is held in the issue log."""
    if not review_text:
        return []
    named = sorted(set(ISSUE_ID.findall(review_text)) - held)
    return [f"{REVIEW_LOG} names {k}, which the issue log does not hold" for k in named]


def judge(log: Log, stories: dict[str, str], decisions: set[str] | None, review_text: str | None) -> list[str]:
    """Every rule over one parsed log; the example is held to the form alone."""
    problems = list(log.problems)
    recorded = log_prefix(log)
    problems += [f"{i.id} is not under the log's prefix, {recorded}" for i in log.issues
                 if recorded and not i.example and prefix(i.id) != recorded]
    for issue in log.issues:
        here = entry_problems(issue)
        if not issue.example:
            here += link_problems(issue, stories, decisions)
            here += [p for p in [bears_out(issue, stories)] if p and not link_problems(issue, stories, None)]
        problems += [f"{issue.id}: {p}" for p in here]
    problems += index_problems(log.index, log.issues) + sequence_problems(log.issues)
    return problems + review_problems(review_text, {i.id for i in log.issues if not i.example})


# ==============================================================================
# The writer — pure over text
# ==============================================================================

def next_id(issues: list[Issue], tracker_prefixes: list[str], given: str | None, recorded: str | None = None) -> str:
    """The next ID, its prefix the first of: the one given, the one the log records, the log's own
    issues', the tracker's stories'."""
    real = [i.id for i in issues if not i.example]
    pfx = (given or recorded or (prefix(real[0]) if real else None)
           or (collections.Counter(tracker_prefixes).most_common(1) or [(None,)])[0][0])
    if not pfx:
        raise ValueError("no prefix: the log, its issues and the tracker name none, so give --prefix")
    return f"{pfx}-ISS-{max((number(k) for k in real), default=0) + 1}"


def file_issue(text: str, values: dict[str, str], issue_id: str) -> str:
    fields = {"Title": values["title"], "Reported": values["date"], "Reporter": f"{values['by']} ({values['as']})",
              "Kind": values["kind"], "Severity": values["severity"], "Status": "Open", "Stories": NONE,
              "Decisions": NONE, "Resolved by": NONE}
    sections = {"What happened": values["what"], "Expected": values["expected"], "Impact": values["impact"],
                "Resolution": NONE, **({BUG_ONLY: values["steps"]} if values["kind"] == "bug" else {})}
    issue = Issue(issue_id, False, fields, FIELDS, sections,
                  tuple(s for s in SECTIONS if s in sections))
    log = parse(text)
    return render(log.preamble, log.issues + [issue])


UPDATABLE = {"title": "Title", "severity": "Severity", "status": "Status", "stories": "Stories",
             "decisions": "Decisions", "resolved_by": "Resolved by"}


def update_issue(text: str, issue_id: str, changes: dict[str, str]) -> str:
    log = parse(text)
    found = [i for i in log.issues if i.id == issue_id and not i.example]
    if not found:
        raise ValueError(f"the log holds no {issue_id}")
    old = found[0]
    fields = {**old.fields, **{UPDATABLE[k]: v for k, v in changes.items() if k in UPDATABLE}}
    sections = {**old.sections, **({"Resolution": changes["resolution"]} if "resolution" in changes else {})}
    new = old._replace(fields=fields, sections=sections)
    return render(log.preamble, [new if i is old else i for i in log.issues])


# ==============================================================================
# The tree
# ==============================================================================

def read(rel: str) -> str | None:
    path = ROOT / rel
    return path.read_text(encoding="utf-8") if path.is_file() else None


def tracker_statuses(text: str | None) -> dict[str, str]:
    return {s.id: s.status for s in session_closeout.tracker_stories(text or "")}


def known_decisions() -> set[str] | None:
    ids, problems = session_closeout.decision_ids()
    return None if problems else ids


def cmd_check() -> int:
    text = read(LOG)
    review = read(REVIEW_LOG)
    print("\nIssue Log Gate")
    print("=" * 60)
    if text is None:
        problems = review_problems(review, set())
        if not problems:
            print(f"PASSED: no {LOG}, so no issues")
            return 0
    else:
        problems = judge(parse(text), tracker_statuses(read(TRACKER)), known_decisions(), review)
    if not problems:
        print(f"PASSED: {LOG} in its template's form and in step with the tracker")
        return 0
    print(f"BLOCKED: {len(problems)} violation(s)\n")
    for p in problems:
        print(f"  {p}")
    print(f"\n  The form, the statuses and their rules: {STANDARD} section 12. Change an issue through "
          "`python3 scripts/issue_log.py --update <ID>`, which writes the index row with it.")
    return 1


def report_lines(log: Log, stories: dict[str, str], today: datetime.date) -> list[str]:
    real = [i for i in log.issues if not i.example]
    out = [f"{len(real)} issue(s)"]
    for name, key in (("status", "Status"), ("kind", "Kind"), ("severity", "Severity")):
        counts = collections.Counter(i.fields.get(key) for i in real)
        out.append(f"  by {name}: " + (", ".join(f"{k} {n}" for k, n in counts.most_common()) or "none"))
    by = collections.Counter(REPORTER.match(i.fields.get("Reporter", "")).group(1) if REPORTER.match(i.fields.get("Reporter", ""))
                             else "?" for i in real)
    out.append("  by reporter: " + (", ".join(f"{k} {n}" for k, n in by.most_common()) or "none"))
    open_ = sorted((i for i in real if i.fields.get("Status") not in (*RESOLVED, DECLINED)), key=lambda i: i.fields.get("Reported", ""))
    out.append(f"\nOpen, oldest first ({len(open_)}):")
    for i in open_:
        age = (today - datetime.date.fromisoformat(i.fields["Reported"])).days if DATE.match(i.fields.get("Reported", "")) else "?"
        out.append(f"  {i.id}  {age} day(s)  {i.fields.get('Severity')}  {i.fields.get('Kind')}  {i.fields.get('Status')}  "
                   f"{i.fields.get('Title')}")
        out += [f"      {s}: {stories.get(s, 'not in the tracker')}" for s in items(i.fields.get("Stories", NONE))]
    return out


def cmd_report() -> int:
    text = read(LOG)
    if text is None:
        print(f"No {LOG}: no issues.")
        return 0
    print("\n".join(["\nIssue Log Report", "=" * 60, *report_lines(parse(text), tracker_statuses(read(TRACKER)), datetime.date.today())]))
    return 0


ASKED = {"title": "Title, one line", "by": "Reporter's name", "as": "Reporter: human or agent",
         "kind": "Kind: bug, request or risk", "severity": "Severity: critical, high, medium or low",
         "what": "What happened", "expected": "What was expected", "steps": "Steps to reproduce",
         "impact": "Its impact"}
CHOICES = {"as": REPORTER_KINDS, "kind": KINDS, "severity": SEVERITIES}


def gather(given: dict[str, str | None], ask: Callable[[str], str] | None) -> tuple[dict[str, str], list[str]]:
    """Each field from its flag, else asked for when there is a terminal; what is still missing."""
    values: dict[str, str] = {}
    for key in ASKED:
        if key == "steps" and values.get("kind") != "bug":
            continue
        value = given.get(key)
        try:
            while ask is not None and (not value or (key in CHOICES and value not in CHOICES[key])):
                value = ask(f"{ASKED[key]}: ").strip()
        except (EOFError, KeyboardInterrupt) as e:
            raise Cancelled from e
        if value:
            values[key] = value
    missing = [k for k in ASKED if k not in values and not (k == "steps" and values.get("kind") != "bug")]
    missing += [f"{k} ({values[k]!r} is not one of {', '.join(CHOICES[k])})" for k in CHOICES if k in values and values[k] not in CHOICES[k]]
    return values, missing


def write_checked(text: str, stories: dict[str, str]) -> list[str]:
    """What the gate would refuse in the log the writer is about to write, beside what it held already."""
    return judge(parse(text), stories, known_decisions(), read(REVIEW_LOG))


def cmd_file(args: argparse.Namespace) -> int:
    ask = input if sys.stdin.isatty() else None
    try:
        values, missing = gather({k: getattr(args, k) for k in ASKED}, ask)
    except Cancelled:
        print("\nissue_log: cancelled; nothing written.")
        return 1
    if missing:
        print(f"issue_log: REFUSED — missing {', '.join(missing)}. Give each as a flag "
              f"(--{' --'.join(m.split(' ')[0] for m in missing)}), or run it in a terminal to be asked.")
        return 1
    text = read(LOG) or skeleton()
    tracker = read(TRACKER) or ""
    try:
        log = parse(text)
        issue_id = next_id(log.issues, [s.id.split("-")[0] for s in session_closeout.tracker_stories(tracker)], args.prefix,
                           log_prefix(log))
    except ValueError as e:
        print(f"issue_log: REFUSED — {e}")
        return 1
    new = file_issue(text, {**values, "date": datetime.date.today().isoformat()}, issue_id)
    problems = [p for p in write_checked(new, tracker_statuses(tracker)) if p.startswith(issue_id)]
    if problems:
        return _refused(problems)
    (ROOT / LOG).write_text(new, encoding="utf-8")
    print(f"issue_log: filed {issue_id}, Open. Commit it: `checkpoint: issue {issue_id} filed`.")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    text = read(LOG)
    if text is None:
        print(f"issue_log: REFUSED — there is no {LOG}")
        return 1
    changes = {k: v for k in (*UPDATABLE, "resolution") if (v := getattr(args, k, None)) is not None}
    try:
        new = update_issue(text, args.update, changes)
    except ValueError as e:
        print(f"issue_log: REFUSED — {e}")
        return 1
    problems = [p for p in write_checked(new, tracker_statuses(read(TRACKER))) if p.startswith(args.update)]
    if problems:
        return _refused(problems)
    (ROOT / LOG).write_text(new, encoding="utf-8")
    print(f"issue_log: {args.update} updated: {', '.join(f'{k} {v!r}' for k, v in changes.items())}.")
    return 0


def _refused(problems: list[str]) -> int:
    print("issue_log: REFUSED — the entry would break the log's rules; nothing written:")
    for p in problems:
        print(f"  {p}")
    return 1


# ==============================================================================
# SELF-TEST — in-memory fixtures, run on every commit
# ==============================================================================

def table_after(text: str, header: str) -> list[list[str]]:
    """The body rows of the markdown table whose header row is `header`."""
    if header not in text:
        return []
    rows = []
    for line in text.split(header, 1)[1].splitlines()[1:]:
        if not line.startswith("|"):
            break
        if not set(line) <= set("|-: "):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def law_lists(standard: str) -> dict[str, tuple[str, ...]]:
    """The lists section 12 of the standard states: its field table, the values of Kind, Severity and
    Status, its status table and its sections, so the gate cannot drift from its law."""
    section = standard.split("## 12. Issues", 1)[-1].split("\n## ", 1)[0]
    fields = table_after(section, "| Field | Values |")
    values = {r[0]: tuple(re.findall(r"`([^`]+)`", r[1])) for r in fields}
    order_line = section.split("The sections, in order:", 1)[-1].split(".", 1)[0]
    return {"fields": tuple(r[0] for r in fields), "kinds": values.get("Kind", ()), "severities": values.get("Severity", ()),
            "statuses": values.get("Status", ()), "sections": tuple(re.findall(r"`([^`]+)`", order_line)),
            "status table": tuple(r[0] for r in table_after(section, "| Status | Holds when |"))}


def _issue(n: int = 1, kind: str = "request", **fields: str) -> Issue:
    base = {"Title": "A title", "Reported": "2026-10-01", "Reporter": "Chair (human)", "Kind": kind, "Severity": "high",
            "Status": "Open", "Stories": NONE, "Decisions": NONE, "Resolved by": NONE}
    base.update({k.replace("_", " "): v for k, v in fields.items()})
    resolution = base.pop("Resolution", NONE)
    sections = {"What happened": "Something.", "Expected": "Something else.", "Impact": "Some.", "Resolution": resolution,
                **({BUG_ONLY: "1. Do it."} if kind == "bug" else {})}
    return Issue(f"ACME-ISS-{n}", False, base, FIELDS, sections, tuple(s for s in SECTIONS if s in sections))


def _log(*issues: Issue) -> str:
    return render(PREAMBLE, [EXAMPLE_ISSUE, *issues])


def _t_form(check) -> None:
    check("the shipped log, the example alone, passes every rule", judge(parse(skeleton()), {}, set(), None) == [],
          str(judge(parse(skeleton()), {}, set(), None)))
    text = _log(_issue(1), _issue(2, kind="bug"))
    check("a log the writer renders parses back to the same log", render(parse(text).preamble, parse(text).issues) == text)
    ok = _issue(1)
    check("an entry in the template's form passes", entry_problems(ok) == [], str(entry_problems(ok)))
    bad_cases = {
        "a field out of order": ok._replace(order=("Reported", "Title", *FIELDS[2:])),
        "a field missing": ok._replace(order=FIELDS[:-1], fields={k: v for k, v in ok.fields.items() if k != "Resolved by"}),
        "a kind outside bug, request and risk": _issue(1, kind="question"),
        "a severity outside the four": _issue(1, Severity="urgent"),
        "a status outside the six": _issue(1, Status="Done"),
        "a date not YYYY-MM-DD": _issue(1, Reported="25 Oct 2026"),
        "a reporter not marked human or agent": _issue(1, Reporter="Chair"),
        "a story list holding no ID": _issue(1, Stories="the export story"),
        "a decision list holding no ID": _issue(1, Decisions="the big one"),
        "a resolving commit that is no hash": _issue(1, Resolved_by="yesterday"),
        "an empty title": _issue(1, Title=""),
        "a bug with no steps to reproduce": _issue(1, kind="bug")._replace(section_order=("What happened", "Expected", "Impact", "Resolution")),
        "a request with steps to reproduce": ok._replace(section_order=SECTIONS),
        "an empty What happened": ok._replace(sections={**ok.sections, "What happened": NONE}),
    }
    for label, issue in bad_cases.items():
        check(f"{label} is refused", len(entry_problems(issue)) >= 1, str(entry_problems(issue)))


STATUS_CASES = [   # label, issue, the stories' status in the tracker, whether it holds
    ("Open, naming nothing", _issue(1), {}, True),
    ("Open, naming a story", _issue(1, Stories="ACME-1.1"), {"ACME-1.1": "Not Started"}, False),
    ("Triaged, its story not started", _issue(1, Status="Triaged", Stories="ACME-1.1"), {"ACME-1.1": "Not Started"}, True),
    ("Triaged, its story blocked", _issue(1, Status="Triaged", Stories="ACME-1.1"), {"ACME-1.1": "Blocked"}, True),
    ("Triaged by a decision alone", _issue(1, Status="Triaged", Decisions="2026-01-02-004"), {}, True),
    ("Triaged, naming nothing", _issue(1, Status="Triaged"), {}, False),
    ("Triaged, its story in progress", _issue(1, Status="Triaged", Stories="ACME-1.1"), {"ACME-1.1": "In Progress"}, False),
    ("In Progress, a story in progress", _issue(1, Status="In Progress", Stories="ACME-1.1, ACME-1.2"),
     {"ACME-1.1": "In Progress", "ACME-1.2": "Not Started"}, True),
    ("In Progress, one story done and one not", _issue(1, Status="In Progress", Stories="ACME-1.1, ACME-1.2"),
     {"ACME-1.1": "Done", "ACME-1.2": "Not Started"}, True),
    ("In Progress, every story done", _issue(1, Status="In Progress", Stories="ACME-1.1"), {"ACME-1.1": "Done"}, False),
    ("In Progress, no story started", _issue(1, Status="In Progress", Stories="ACME-1.1"), {"ACME-1.1": "Not Started"}, False),
    ("Resolved, every story done, its commit and resolution written",
     _issue(1, Status="Resolved", Stories="ACME-1.1", Resolved_by="1a2b3c4", Resolution="Fixed."), {"ACME-1.1": "Done"}, True),
    ("Closed, as Resolved", _issue(1, Status="Closed", Stories="ACME-1.1", Resolved_by="1a2b3c4", Resolution="Fixed."),
     {"ACME-1.1": "Done"}, True),
    ("Resolved, a story still in progress",
     _issue(1, Status="Resolved", Stories="ACME-1.1", Resolved_by="1a2b3c4", Resolution="Fixed."), {"ACME-1.1": "In Progress"}, False),
    ("Resolved, no commit named", _issue(1, Status="Resolved", Stories="ACME-1.1", Resolution="Fixed."), {"ACME-1.1": "Done"}, False),
    ("Resolved, no resolution written", _issue(1, Status="Resolved", Stories="ACME-1.1", Resolved_by="1a2b3c4"),
     {"ACME-1.1": "Done"}, False),
    ("Closed, naming nothing", _issue(1, Status="Closed", Resolved_by="1a2b3c4", Resolution="Fixed."), {}, False),
    ("In Progress, a commit already named", _issue(1, Status="In Progress", Stories="ACME-1.1", Resolved_by="1a2b3c4"),
     {"ACME-1.1": "In Progress"}, False),
    ("Triaged, a resolution already written", _issue(1, Status="Triaged", Stories="ACME-1.1", Resolution="Fixed."),
     {"ACME-1.1": "Not Started"}, False),
    ("Won't fix, its reason written", _issue(1, Status="Won't fix", Resolution="Out of scope."), {}, True),
    ("Won't fix, no reason", _issue(1, Status="Won't fix"), {}, False),
    ("Won't fix, its story in progress", _issue(1, Status="Won't fix", Stories="ACME-1.1", Resolution="Out of scope."),
     {"ACME-1.1": "In Progress"}, False),
]


def _t_status(check) -> None:
    for label, issue, stories, holds in STATUS_CASES:
        got = bears_out(issue, stories)
        check(f"{label} {'holds' if holds else 'is refused'}", (got is None) == holds, str(got))


def _t_links(check) -> None:
    lost = _issue(1, Status="In Progress", Stories="ACME-9.9")   # a status no absent story bears out
    found = judge(parse(_log(lost)), {}, {"2026-01-02-004"}, None)
    check("a story the tracker lacks is named, and its status is not judged as well",
          len(found) == 1 and "ACME-9.9" in found[0], str(found))
    found = judge(parse(_log(_issue(1, Status="Triaged", Decisions="2026-01-01-999"))), {}, {"2026-01-02-004"}, None)
    check("a decision neither log indexes is named", len(found) == 1 and "2026-01-01-999" in found[0], str(found))
    found = judge(parse(_log(_issue(1, Status="Triaged", Decisions="2026-01-01-999"))), {}, None, None)
    check("an unreadable decision index judges no decision link", found == [], str(found))
    text = _log(_issue(1))
    check("a code review log naming a held issue passes", review_problems("| x | acknowledged, ACME-ISS-1 |", {"ACME-ISS-1"}) == [])
    for label, review in (("an issue the log does not hold", "| x | acknowledged, ACME-ISS-7 |"),
                          ("the example's ID", f"| x | acknowledged, {EXAMPLE_ISSUE.id} |")):
        found = judge(parse(_log() if "example" in label else text), {}, set(), review)
        check(f"a code review log naming {label} is refused", len(found) == 1 and REVIEW_LOG in found[0], str(found))


def _t_index(check) -> None:
    text = _log(_issue(1), _issue(2))
    for label, edit, said in (("a row missing", lambda t: t.replace(index_row(_issue(2)) + "\n", ""), "has no index row"),
                              ("a row with no entry", lambda t: t.replace(index_row(_issue(2)), index_row(_issue(2)) + "\n"
                                                                          + index_row(_issue(3))), "which has no entry"),
                              ("a row disagreeing with its entry", lambda t: t.replace(index_row(_issue(2)),
                                                                                       index_row(_issue(2, Severity="low"))), "disagrees"),
                              ("a row twice", lambda t: t.replace(index_row(_issue(2)), index_row(_issue(2)) + "\n"
                                                                  + index_row(_issue(2))), "twice"),
                              ("a heading that is neither", lambda t: t + "\n## Notes\n\ntext\n", "neither"),
                              ("no index", lambda t: t.replace(f"## {INDEX_HEADING}\n", ""), f"no `## {INDEX_HEADING}`")):
        found = judge(parse(edit(text)), {}, set(), None)
        check(f"{label} is refused, by its own rule", any(said in p for p in found), str(found))
    for label, issues in (("a gap in the numbers", (_issue(1), _issue(3))), ("an ID filed twice", (_issue(1), _issue(1))),
                          ("two prefixes", (_issue(1), _issue(2)._replace(id="OTHER-ISS-2")))):
        found = sequence_problems([EXAMPLE_ISSUE, *issues])
        check(f"{label} is refused", len(found) >= 1, str(found))
    check("the example is outside the sequence: a log of issues 1 and 2 beside it passes",
          sequence_problems([EXAMPLE_ISSUE, _issue(1), _issue(2)]) == [])


def _t_writer(check) -> None:
    values = {"title": "Rows dropped", "by": "qa-engineer", "as": "agent", "kind": "bug", "severity": "high",
              "what": "Rows went missing.", "expected": "Every row.", "steps": "1. Export.", "impact": "Totals undercount.",
              "date": "2026-10-25"}
    check("the next ID follows the log's own prefix and highest number",
          next_id([EXAMPLE_ISSUE, _issue(1), _issue(2)], ["TMPL"], None) == "ACME-ISS-3")
    check("the first ID takes the tracker's story prefix, the example's not counted",
          next_id([EXAMPLE_ISSUE], ["PFX", "PFX", "X"], None) == "PFX-ISS-1")
    check("a given prefix wins", next_id([EXAMPLE_ISSUE], ["TMPL"], "ACME", "PROBE") == "ACME-ISS-1")
    check("the example is numbered zero, so the first issue under its own prefix is 1, never the example's ID",
          number(EXAMPLE_ISSUE.id) == 0
          and next_id([EXAMPLE_ISSUE], [], prefix(EXAMPLE_ISSUE.id)) == f"{prefix(EXAMPLE_ISSUE.id)}-ISS-1")
    check("the prefix the log records comes next, ahead of the tracker's",
          next_id([EXAMPLE_ISSUE], ["TMPL"], None, "PROBE") == "PROBE-ISS-1")
    born = parse(skeleton("PROBE"))
    check("a log born with a prefix records it, and still passes as the example alone",
          log_prefix(born) == "PROBE" and judge(born, {}, set(), None) == [] and log_prefix(parse(skeleton())) is None,
          str(judge(born, {}, set(), None)))
    found = judge(parse(render(born.preamble, [EXAMPLE_ISSUE, _issue(1)])), {}, set(), None)
    check("an issue under another prefix than the log records is refused", any("prefix" in p for p in found), str(found))
    try:
        next_id([EXAMPLE_ISSUE], [], None)
        check("no prefix anywhere is refused", False)
    except ValueError:
        check("no prefix anywhere is refused", True)
    new = file_issue(skeleton(), values, "ACME-ISS-1")
    issue = [i for i in parse(new).issues if not i.example][0]
    check("a filed bug is Open, its reporter marked an agent, its steps kept, and the log passes every rule",
          issue.fields["Status"] == "Open" and issue.fields["Reporter"] == "qa-engineer (agent)"
          and issue.sections.get(BUG_ONLY) == "1. Export." and judge(parse(new), {}, set(), None) == [],
          str(judge(parse(new), {}, set(), None)))
    request = file_issue(skeleton(), {**values, "kind": "request", "as": "human"}, "ACME-ISS-1")
    check("a filed request carries no steps to reproduce",
          BUG_ONLY not in [i for i in parse(request).issues if not i.example][0].section_order)
    moved = update_issue(new, "ACME-ISS-1", {"status": "Triaged", "stories": "ACME-1.1"})
    log = parse(moved)
    check("an update rewrites the entry and its index row together",
          log.index["ACME-ISS-1"]["Status"] == "Triaged" and log.index["ACME-ISS-1"]["Stories"] == "ACME-1.1"
          and index_problems(log.index, log.issues) == [], str(log.index.get("ACME-ISS-1")))
    try:
        update_issue(new, "ACME-ISS-9", {"status": "Triaged"})
        check("an update to an issue the log lacks is refused", False)
    except ValueError:
        check("an update to an issue the log lacks is refused", True)
    got, missing = gather({k: values.get(k) for k in ASKED}, None)
    check("every field given as a flag leaves nothing missing", not missing and got["kind"] == "bug", str(missing))
    got, missing = gather({"title": "x", "kind": "request"}, None)
    check("outside a terminal, each missing field is named, a request's steps not among them",
          sorted(missing) == sorted(["by", "as", "severity", "what", "expected", "impact"]), str(missing))
    answers = iter(["Ada", "person", "human", "maybe", "bug", "high", "Rows went missing.", "Every row.", "1. Export.", "Totals."])
    got, missing = gather({"title": "x"}, lambda prompt: next(answers))
    check("in a terminal each missing field is asked for, a choice asked again until it is one of the allowed",
          not missing and got["as"] == "human" and got["kind"] == "bug" and got["steps"] == "1. Export.", str(got))
    def ctrl_d(prompt: str) -> str:
        raise EOFError
    try:
        gather({"title": "x"}, ctrl_d)
        check("Ctrl-D at a prompt cancels the filing, never a traceback", False)
    except Cancelled:
        check("Ctrl-D at a prompt cancels the filing, never a traceback", True)
    got, missing = gather({**{k: values.get(k) for k in ASKED}, "kind": "question"}, None)
    check("a flag outside the allowed values is refused, never written", any("kind" in m for m in missing), str(missing))


def _t_report(check) -> None:
    log = parse(_log(_issue(1, kind="bug", Status="In Progress", Stories="ACME-1.1", Reporter="qa (agent)"),
                     _issue(2, Status="Won't fix", Resolution="No.")))
    lines = report_lines(log, {"ACME-1.1": "In Progress"}, datetime.date(2026, 10, 25))
    text = "\n".join(lines)
    check("the report counts by status and reporter, the example not counted, and lists the open issue by age with "
          "its story", lines[0] == "2 issue(s)" and "In Progress 1" in text and "agent 1, human 1" in text
          and "ACME-ISS-1  24 day(s)" in text and "ACME-1.1: In Progress" in text and "ACME-ISS-2  " not in text, text)


def _t_law(check) -> None:
    path = ROOT / STANDARD
    if not path.is_file():
        check("the standard's section 12 is read in the template", True)   # a project may not carry it
        return
    law = law_lists(path.read_text(encoding="utf-8"))
    for name, mine in (("fields", FIELDS), ("kinds", KINDS), ("severities", SEVERITIES), ("statuses", STATUSES),
                       ("sections", SECTIONS), ("status table", STATUSES)):
        check(f"the {name} are the standard's section 12", law[name] == mine, f"standard {law[name]}, gate {mine}")


def run_self_test() -> int:
    print("\nIssue Log Self-Test")
    print("=" * 60)
    state = {"failures": 0, "total": 0}

    def check(label: str, ok: bool, detail: str = "") -> None:
        state["total"] += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok:
            state["failures"] += 1
            if detail:
                print(f"        {detail}")

    for group in (_t_form, _t_status, _t_links, _t_index, _t_writer, _t_report, _t_law):
        try:
            group(check)
        except Exception as e:   # noqa: BLE001  — a crash is a failure of the group, never of the run
            check(f"{group.__name__} ran without raising", False, f"{type(e).__name__}: {e}")
    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 1 if state["failures"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="File, update, check and report the issue log")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--file", action="store_true", help="File a new issue")
    mode.add_argument("--update", metavar="ID", help="Change an issue's fields")
    mode.add_argument("--check", action="store_true", help="The gate")
    mode.add_argument("--report", action="store_true", help="Counts, and the open issues by age")
    mode.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    for flag in ("title", "by", "kind", "severity", "what", "expected", "steps", "impact", "prefix",
                 "status", "stories", "decisions", "resolved-by", "resolution"):
        parser.add_argument(f"--{flag}")
    parser.add_argument("--as", dest="as_", choices=REPORTER_KINDS, help="Who files it: a human or an agent")
    args = parser.parse_args()
    setattr(args, "as", args.as_)
    if args.self_test:
        return run_self_test()
    if args.check:
        return cmd_check()
    if args.report:
        return cmd_report()
    if args.file:
        return cmd_file(args)
    return cmd_update(args)


if __name__ == "__main__":
    raise SystemExit(main())
