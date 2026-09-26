#!/usr/bin/env python3
"""
kb_freshness_scan.py — no mandatory-read document may teach a stale or superseded decision.

THE FAILURE THIS CLOSES
-----------------------
On the project this pattern came from, an amendment sweep was missed SIX times. Every miss had the
same shape: the decision body, the canonical source and the live system were all updated correctly,
and the **teaching document** was left stale.

That shape is the dangerous one, because teaching documents are what the next agent reads INSTEAD of
the source. The worst instance told agents that a value two ratified decisions REQUIRED was "legacy,
retained only until parity proves it has no remaining consumer." It had five live consumers.

**A sweep that stops at code and decision bodies is not a sweep.**

Root cause, once measured: nothing linked a decision to the documents teaching it, and amendment
dates were not machine-readable. Neither a human nor a script could answer *"which decisions changed
since this document was written?"*

WHAT IT CHECKS
--------------
Every `docs/orchestration/knowledge/*.md` entry declares in its YAML frontmatter:

    teaches:  [2026-07-30-001]     # decisions this entry EXPLAINS (not every ID it mentions)
    verified: 2026-07-31           # when it was last confirmed against them

FAIL when a taught decision changed after the entry was last verified:

    effective_change_date(D) = max(
        D's "; amended <date>" in the decision-log Date cell,
        the Date of any decision recorded as superseding/amending D,
    )

Supersession dates are taken from the SUPERSEDING decision, so historical rows need no backfill.

Decision IDs are read LITERALLY from the first column of the decision-log index table, so this works
with any ID convention (`DEC-041`, `2026-07-30-001`, `ADR-7`, …). Rows marked `[EXAMPLE]` are skipped.

TWO LOGS, READ AS ONE
---------------------
The template's own decisions live in `docs/governance/framework_decisions.md`; a project's live in
`sprint/decision-log.md` (decision 2026-09-23-003). Both carry a Decision Index and both are read,
as one set: an entry may teach an ID from either. A log that exists without a locatable index still
fails loudly. On a duplicate ID the framework file's row wins — it is the maintained copy, and a
project that took a release before the split may still carry framework rows in its own log.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It flags staleness RISK, not wrongness — it cannot read prose. It says "this entry may now be wrong,
go re-verify", which is the signal that was missing. A green scan means nothing has changed SINCE
SOMEONE LAST LOOKED, not that the entry is correct.

**Clearing a failure means re-reading the decision AND the canonical source, correcting the entry,
then bumping `verified:`. Bumping the date alone re-creates the exact fossil this exists to catch.**

SCOPE
-----
Decisions are read from the **Decision Index section only** — the heading, then the contiguous run of
`|` lines beneath it. Decision bodies legitimately contain tables, and scanning the whole file
absorbed one as a phantom decision. If the index cannot be located the scan FAILS; an unreadable
index is never zero decisions. `--self-test` proves that boundary on every commit.

Usage:  pre-commit run kb-freshness-scan --all-files        # portable; pre-commit owns the interpreter
        python3 scripts/kb_freshness_scan.py [--list]       # direct: `python3` on macOS/Linux,
        python3 scripts/kb_freshness_scan.py --self-test    # `python` on Windows — no portable
                                                            # bare name exists (see
                                                            # knowledge/reference_precommit_interpreter.md)
Exit 0 = clean, 1 = stale/unstamped/unknown/unreadable index (blocks the commit).
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
KB = ROOT / "docs" / "orchestration" / "knowledge"
LOG = ROOT / "sprint" / "decision-log.md"
FRAMEWORK = ROOT / "docs" / "governance" / "framework_decisions.md"
# Read in this order; a later log's row wins a duplicate ID, so the framework file is authoritative.
LOGS = {"sprint/decision-log.md": LOG, "docs/governance/framework_decisions.md": FRAMEWORK}

ISO = re.compile(r"(\d{4}-\d{2}-\d{2})")
AMENDED = re.compile(r"amended\s+(\d{4}-\d{2}-\d{2})")

# The index is a SCOPED REGION, not "every table row in the file". Decision bodies legitimately
# contain tables, and one of them was silently absorbed as a phantom decision. The boundary is read
# from the file's actual structure: the heading, then the contiguous run of `|` lines beneath it,
# ending at the first horizontal rule, the next heading, or the end of the table — whichever is
# first. Anything below that is a decision body and is not the index.
INDEX_HEADING = re.compile(r"^#{2,3}\s+Decision Index\s*$", re.IGNORECASE)
SECTION_BREAK = re.compile(r"^(?:-{3,}\s*$|#{1,6}\s)")


class DecisionIndexNotFound(Exception):
    """The Decision Index table could not be located. NEVER treat this as zero decisions."""


def index_rows(text):
    """Return the raw `|` lines of the Decision Index table.

    Raises DecisionIndexNotFound rather than returning [] — an index that cannot be located must
    fail loudly. Returning empty would make every `teaches:` report UNKNOWN, or, if nothing is
    stamped, make the gate report green while checking nothing at all.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if INDEX_HEADING.match(line):
            start = i + 1
            break
    if start is None:
        raise DecisionIndexNotFound(
            "no '## Decision Index' heading found. The freshness gate reads decisions from that "
            "section only; if the heading was renamed, restore it or update INDEX_HEADING here."
        )

    rows = []
    for line in lines[start:]:
        if SECTION_BREAK.match(line):
            break
        if line.startswith("|"):
            rows.append(line)
        elif rows:
            break  # the table ended; everything after it is body, not index
    if not rows:
        raise DecisionIndexNotFound(
            "'Decision Index' heading found, but no table rows beneath it."
        )
    return rows


def index_decisions(text):
    """The rows of one log's Decision Index, {id: {'date','amended','status','_text'}}, before
    decision-to-decision changes are resolved. Raises DecisionIndexNotFound as index_rows does."""
    decs = {}
    for line in index_rows(text):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        did, datecell, title, status = cells[0], cells[1], cells[2], cells[-1]
        if not did or did.lower() in ("id", "---") or set(did) <= set("-: "):
            continue
        if did.startswith("[EXAMPLE]"):          # template placeholder rows are not decisions
            continue
        if not ISO.search(datecell):             # an index row always carries a date
            continue
        decs[did] = {
            "date": ISO.search(datecell).group(1),
            "amended": AMENDED.search(datecell).group(1) if AMENDED.search(datecell) else None,
            "status": status,
            "_text": f"{status} || {title}",
        }
    return decs


def resolve_changes(decs):
    """Resolve decision-to-decision content changes across the set. Any verb counts: a decision
    whose content was replaced, amended, corrected, retired or superseded BY another changed on
    that other's date. Resolved over the union, so a row in one log may name an ID in the other."""
    ids = sorted(decs, key=len, reverse=True)
    verb = re.compile(r"(?:supersed\w*|amend\w*|correct\w*|retir\w*|replac\w*)[^|]{0,80}?\bby\s+", re.I)
    for did, d in decs.items():
        d["changed_by"] = None
        for m in verb.finditer(d["_text"]):
            tail = d["_text"][m.end():m.end() + 40]
            for other in ids:
                if other != did and tail.startswith(other):
                    d["changed_by"] = other
                    break
            if d["changed_by"]:
                break
    return decs


def parse_index(text):
    """Parse one decision-log text. IDs are taken literally from column 1, so any ID convention
    works. Returns {id: {'date','amended','changed_by','status'}}."""
    return resolve_changes(index_decisions(text))


def parse_logs(texts):
    """Every log's Decision Index as one set, from {label: text} in reading order: a later log's
    row wins a duplicate ID. A log whose index cannot be located raises, naming the label — one
    unreadable index is never "the other log's decisions only"."""
    decs = {}
    for label, text in texts.items():
        try:
            decs.update(index_decisions(text))
        except DecisionIndexNotFound as e:
            raise DecisionIndexNotFound(f"{label}: {e}") from e
    return resolve_changes(decs)


def log_texts():
    """{label: text} for every decision log that exists, in LOGS order."""
    return {label: path.read_text(encoding="utf-8") for label, path in LOGS.items() if path.is_file()}


def load_decisions():
    return parse_logs(log_texts())


def effective_change_date(did, decs):
    d = decs.get(did)
    if not d:
        return None, None
    cands = []
    if d["amended"]:
        cands.append((d["amended"], "amended"))
    if d["changed_by"] and decs.get(d["changed_by"], {}).get("date"):
        cands.append((decs[d["changed_by"]]["date"], f"changed by {d['changed_by']}"))
    return max(cands) if cands else (None, None)


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = text[3:end]
    teaches = re.search(r"^teaches:\s*\[([^\]]*)\]", fm, re.M)
    verified = re.search(r"^verified:\s*(\d{4}-\d{2}-\d{2})", fm, re.M)
    return {
        "teaches": [t.strip() for t in teaches.group(1).split(",") if t.strip()] if teaches else [],
        "verified": verified.group(1) if verified else None,
    }


# ==============================================================================
# SELF-TEST — the parser proves itself on every commit
# ==============================================================================
#
# Fixtures are in-memory, so this costs milliseconds and needs no files on disk.
# It exists because the phantom-decision bug was a PARSER bug: the gate stayed
# green while silently reading the wrong region. A parser that guards a file
# nobody re-reads has to demonstrate its own boundary, not assert it in prose.

_HEAD = "# Architectural Decision Log\n\n## Decision Index\n\n| ID | Date | Title | Status |\n|----|------|-------|--------|\n"
_ROW = "| 2026-09-20-001 | 2026-09-20 | A real decision | APPROVED |\n"

SELF_TEST_CASES = [
    (
        "index rows are parsed",
        _HEAD + _ROW + "\n---\n",
        {"2026-09-20-001"},
    ),
    (
        "a table inside a decision BODY is not an index row",
        _HEAD + _ROW + "\n---\n\n## Decision 2026-09-20-001: A real decision\n\n### Context\n\n"
        "| frontmatter line | regex | yaml | |\n|---|---|---|---|\n"
        "| `verified: 2026-09-20` | `'2026-09-20'` | date | agree |\n",
        {"2026-09-20-001"},
    ),
    (
        "a |-prefixed body line that is not a table is not an index row",
        # Shaped to LOOK like an index row to the cell parser — second cell carries a date — so it
        # discriminates. A fixture the broken parser also passes gives false confidence.
        _HEAD + _ROW + "\n---\n\n## Decision 2026-09-20-001: A real decision\n\n"
        "| note | 2026-09-20 | pipe-prefixed prose, not an index row | see above |\n",
        {"2026-09-20-001"},
    ),
    (
        "[EXAMPLE] rows are skipped",
        _HEAD + _ROW + "| [EXAMPLE] 2025-01-15-001 | 2025-01-15 | Sample | APPROVED |\n\n---\n",
        {"2026-09-20-001"},
    ),
    (
        "supersession is resolved to the superseding decision",
        _HEAD
        + "| 2026-09-20-003 | 2026-09-20 | Old | SUPERSEDED (scope) by 2026-09-20-004 |\n"
        + "| 2026-09-20-004 | 2026-09-21 | New | APPROVED |\n\n---\n",
        {"2026-09-20-003", "2026-09-20-004"},
    ),
    (
        "an index with zero data rows parses to zero decisions",
        _HEAD + "\n---\n\n## Decision 2026-09-20-001: orphaned body\n",
        set(),
    ),
    (
        "a missing index heading RAISES, never returns empty",
        "# Architectural Decision Log\n\n## Decisions\n\n| ID | Date | Title | Status |\n"
        "|----|------|-------|--------|\n" + _ROW,
        DecisionIndexNotFound,
    ),
    (
        "a heading with no table beneath it RAISES",
        "# Architectural Decision Log\n\n## Decision Index\n\nNone recorded yet.\n\n---\n",
        DecisionIndexNotFound,
    ),
]


def run_self_test():
    print("\nKB Freshness Parser Self-Test")
    print("=" * 60)
    failures = 0
    for label, text, expected in SELF_TEST_CASES:
        try:
            got = parse_index(text)
        except DecisionIndexNotFound:
            got = DecisionIndexNotFound
        except Exception as e:  # a parser crash is a failure, not an error to propagate
            print(f"  FAIL  {label}\n        raised {type(e).__name__}: {e}")
            failures += 1
            continue

        if expected is DecisionIndexNotFound:
            ok = got is DecisionIndexNotFound
            detail = "raised" if ok else f"returned {sorted(got)}"
        elif got is DecisionIndexNotFound:
            ok, detail = False, "raised DecisionIndexNotFound"
        else:
            ok = set(got) == expected
            detail = f"got {sorted(got)}, expected {sorted(expected)}"

        if ok:
            print(f"  ok    {label}")
        else:
            print(f"  FAIL  {label}\n        {detail}")
            failures += 1

    extra = 0

    def check(label, ok, detail=""):
        nonlocal failures, extra
        extra += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok:
            if detail:
                print(f"        {detail}")
            failures += 1

    # The supersession case also asserts the resolved link, not just the ID set.
    decs = parse_index(SELF_TEST_CASES[4][1])
    check("supersession link resolves to the superseding decision",
          decs["2026-09-20-003"].get("changed_by") == "2026-09-20-004",
          f"changed_by={decs['2026-09-20-003'].get('changed_by')!r}")

    # Two logs read as one (decision 2026-09-23-003): the project's, then the framework's.
    project = _HEAD + "| PROJ-2026-09-24-001 | 2026-09-24 | The project's own | APPROVED |\n" + "| [EXAMPLE] 2025-01-15-001 | 2025-01-15 | Sample | APPROVED |\n\n---\n"
    framework = _HEAD + _ROW + "\n---\n"
    both = parse_logs({"project": project, "framework": framework})
    check("two logs read as one set", set(both) == {"PROJ-2026-09-24-001", "2026-09-20-001"}, str(sorted(both)))
    check("a project log with the example row only contributes nothing, and is not an error",
          set(parse_logs({"project": _HEAD + "| [EXAMPLE] 2025-01-15-001 | 2025-01-15 | Sample | APPROVED |\n\n---\n",
                          "framework": framework})) == {"2026-09-20-001"})
    stale_copy = _HEAD + _ROW.replace("| 2026-09-20 |", "| 2026-09-19 |") + "\n---\n"
    dup = parse_logs({"project": stale_copy, "framework": framework})
    check("a duplicate ID takes the later log's row — the framework file wins over a copy left in the project's log",
          dup["2026-09-20-001"]["date"] == "2026-09-20", str(dup))
    try:
        parse_logs({"project": project, "framework": "# Log\n\n## Decisions\n\n" + _ROW})
        check("an index missing from either log RAISES, naming the log", False)
    except DecisionIndexNotFound as e:
        check("an index missing from either log RAISES, naming the log", str(e).startswith("framework:"), str(e))
    cross = parse_logs({"project": _HEAD + "| PROJ-1 | 2026-09-24 | Retires the framework rule | SUPERSEDED (scope) by 2026-09-20-001 |\n\n---\n",
                        "framework": framework})
    check("a change recorded in one log against an ID in the other resolves across the union",
          cross["PROJ-1"]["changed_by"] == "2026-09-20-001", str(cross["PROJ-1"]))

    total = len(SELF_TEST_CASES) + extra
    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} parser checks")
    return 1 if failures else 0


def main():
    if "--self-test" in sys.argv:
        return run_self_test()

    stamped_entries = [
        p for p in sorted(KB.glob("*.md"))
        if p.name != "INDEX.md" and (parse_frontmatter(p) or {}).get("teaches")
    ]
    texts = log_texts()
    if not texts:
        where = " or ".join(LOGS)
        if stamped_entries:
            print(f"kb_freshness_scan: no decision log at {where}, but "
                  f"{len(stamped_entries)} entrie(s) declare `teaches:` and cannot be checked:")
            for p in stamped_entries:
                print(f"  UNCHECKABLE: {p.name}")
            print("\nRestore the decision logs, or clear `teaches:` on entries that teach nothing.")
            return 1
        print(f"kb_freshness_scan: no decision log at {where} — nothing to check.")
        return 0

    try:
        decs = parse_logs(texts)
    except DecisionIndexNotFound as e:
        print("kb_freshness_scan: BLOCKED — cannot read a decision index")
        print(f"  {e}")
        print("\nAn unreadable index is not zero decisions. Every `teaches:` would report UNKNOWN, "
              "or, with nothing stamped, the gate would report green while checking nothing.")
        return 1
    stale, unstamped, unknown = [], [], []

    for path in sorted(KB.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        fm = parse_frontmatter(path)
        if not fm or not fm["teaches"]:
            continue
        if not fm["verified"]:
            unstamped.append(path.name)
            continue
        for did in fm["teaches"]:
            if did not in decs:
                unknown.append((path.name, did))
                continue
            changed, why = effective_change_date(did, decs)
            if changed and changed > fm["verified"]:
                stale.append((path.name, did, why, changed, fm["verified"]))

    if "--list" in sys.argv:
        entries = [p for p in sorted(KB.glob("*.md")) if p.name != "INDEX.md"]
        uncovered = [p.name for p in entries if not (parse_frontmatter(p) or {}).get("teaches")]
        stamped = len(entries) - len(uncovered)
        print(f"decisions indexed: {len(decs)}   kb entries: {len(entries)}   stamped: {stamped}")
        # Coverage is reported, never enforced. An entry that explains no ratified decision is
        # legitimate; forcing an ID into it would manufacture a false link. But a green scan must
        # not read as full coverage when it is a fraction of it, so name the gap.
        if uncovered:
            verb = "carries" if len(uncovered) == 1 else "carry"
            print(f"\ngate reach: {stamped}/{len(entries)} entries checkable "
                  f"({len(uncovered)} {verb} `teaches: []` and cannot go stale by this gate)")
            for name in uncovered:
                print(f"  UNCOVERED: {name}")
            print("  (informational, not a failure — verify these by reading, not by scanning)")
        else:
            print(f"\ngate reach: {stamped}/{len(entries)} entries checkable")

    ok = True
    for name, did, why, changed, verified in stale:
        print(f"STALE: {name} teaches {did} ({why} {changed}) but was last verified {verified}")
        ok = False
    for name in unstamped:
        print(f"UNSTAMPED: {name} declares teaches: but has no verified: date")
        ok = False
    for name, did in unknown:
        print(f"UNKNOWN: {name} teaches {did}, which is in neither decision index ({', '.join(texts)})")
        ok = False

    if not ok:
        print("\nRe-verify the entry against the decision AND canonical source, correct it, then bump "
              "`verified:`. Never bump the date alone — that is how the fossil survives.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
