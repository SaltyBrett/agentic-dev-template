#!/usr/bin/env python3
"""
kb_frontmatter_scan.py — a knowledge entry's frontmatter must be valid YAML, and must be
spelled the way the freshness gate can actually read.

THE FAILURE THIS CLOSES
-----------------------
`kb_freshness_scan.py` parses frontmatter with two regexes, not a YAML parser:

    ^teaches:\\s*\\[([^\\]]*)\\]
    ^verified:\\s*(\\d{4}-\\d{2}-\\d{2})

Regexes do not validate. An entry whose frontmatter YAML is malformed still matches them, so the
freshness gate reports green on a file no YAML consumer can load. Demonstrated:

    name: pre-commit language: python interpreter portability   <- unquoted scalar, second colon

    yaml.safe_load                     -> ScannerError
    kb_freshness_scan.parse_frontmatter -> {'teaches': [...], 'verified': '2026-09-20'}

A gate that reports green on a file it cannot actually parse is worse than no gate, because the
green is what stops anyone looking.

WHAT IT CHECKS
--------------
Every `docs/orchestration/knowledge/*.md` entry except INDEX.md:

  1. the frontmatter block exists and is terminated
  2. it parses under `yaml.safe_load`
  3. it has a `teaches` key      (an empty list is legitimate — see below — but the key is required)
  4. it has a `verified` key
  5. `verified` is an unquoted, zero-padded ISO date
  6. the two parsers AGREE about what the file says
  7. the entry has a row in INDEX.md's Entries table, and every row there links an existing file

Check 6 is the durable one. Rather than enumerating known spelling divergences, it parses each file
BOTH ways — with `yaml.safe_load` and with the freshness gate's own `parse_frontmatter` — and fails
when the results differ. Any future divergence is caught without editing this file.

THE DISAGREEMENTS THAT MOTIVATE CHECK 6 (all measured, not assumed)
-------------------------------------------------------------------
    frontmatter line                 freshness-gate regex      yaml.safe_load
    ---------------------------------------------------------------------------------
    verified: 2026-09-20             '2026-09-20'              date(2026, 9, 20)      AGREE
    verified: "2026-09-20"           None -> "UNSTAMPED"       '2026-09-20'           DIFFER
    verified: 2026-09-20T10:00:00    '2026-09-20' (truncated)  datetime(...10:00)     DIFFER
    verified: 2026-9-20              None -> "UNSTAMPED"       '2026-9-20'            DIFFER
    teaches:\\n  - 2026-09-20-001      []  -> entry SKIPPED      ['2026-09-20-001']     DIFFER
    teaches: ["2026-09-20-001"]      ['"2026-09-20-001"']      ['2026-09-20-001']     DIFFER

The second row is the trap: quoting the date is the natural response to "make it valid YAML", it IS
valid YAML, and it makes the freshness gate read the entry as unstamped. The fifth is worse — a YAML
block list is idiomatic, parses correctly, and makes the entry vanish from the freshness gate while
still looking stamped to a human.

So this scanner does not enforce "valid YAML". It enforces the intersection: the one spelling both
gates read identically. Valid YAML that the freshness gate cannot see is still a defect here.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
`teaches: []` is NOT a failure. An entry that explains no ratified decision is legitimate, and
forcing a decision ID into one would manufacture a false link. It does mean the entry is invisible to
the freshness gate, which is a coverage fact rather than an error — `kb_freshness_scan.py --list`
reports those entries by name so the gate's reach is visible rather than implied.

Usage:  pre-commit run kb-frontmatter-scan --all-files   # portable; pre-commit provides pyyaml
        python3 scripts/kb_frontmatter_scan.py           # needs pyyaml in the ambient interpreter
        python3 scripts/kb_frontmatter_scan.py --self-test

Another repository consumes it as the `kb-frontmatter-scan` hook published by `.pre-commit-hooks.yaml`
(decision 2026-09-23-005); it then judges that repository's `docs/orchestration/knowledge/`.
Exit 0 = clean, 1 = violations found (blocks the commit), 2 = cannot run.
"""

import datetime
import pathlib
import re
import subprocess
import sys


def repo_root() -> pathlib.Path:
    """The repository under judgement: the git top level of the working directory.

    Not the script's parent. This module is also installed as a hook package through
    `.pre-commit-hooks.yaml` (decision 2026-09-23-005), where `__file__` sits inside pre-commit's
    virtualenv and the repository is the one the hook runs in. pre-commit runs every hook from
    that repository's root, and the documented direct invocations run from it too.
    """
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False)
    top = out.stdout.strip()
    return pathlib.Path(top) if out.returncode == 0 and top else pathlib.Path.cwd()


ROOT = repo_root()
KB = ROOT / "docs" / "orchestration" / "knowledge"
INDEX = KB / "INDEX.md"

# A row's file link: `[slug](slug.md)`. Read from the Entries section only — the header of
# INDEX.md quotes filenames in prose, and an unscoped scan would count those (2026-09-20-004).
INDEX_LINK = re.compile(r"\]\(([^)/\s]+\.md)\)")
ENTRIES_HEADING = re.compile(r"^##\s+Entries\s*$", re.IGNORECASE)

try:
    import yaml
except ModuleNotFoundError:
    print(
        "kb_frontmatter_scan: PyYAML is not installed in this interpreter.\n"
        "    This gate is normally run through pre-commit, which provisions it via\n"
        "    `additional_dependencies: [pyyaml]`:\n"
        "        pre-commit run kb-frontmatter-scan --all-files\n"
        "    To run it directly instead: python3 -m pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kb_freshness_scan  # noqa: E402  — imported for its parser, not its main()

# ==============================================================================
# FIXES — printed with each violation. A gate that says only "blocked" invites a
# bypass; one that names the correct spelling does not.
# ==============================================================================

FIXES = {
    "no-frontmatter": (
        "Give the entry a YAML frontmatter block: three dashes, the keys, three dashes,\n"
        "    as the very first lines of the file. See knowledge/INDEX.md for the template."
    ),
    "invalid-yaml": (
        "Make the block parse. The usual cause is an unquoted scalar containing a colon —\n"
        "    wrap the value in single quotes: name: 'a: b'. Check with:\n"
        "        python3 -c \"import yaml,sys;yaml.safe_load(open(sys.argv[1]).read().split('---')[1])\" <file>"
    ),
    "missing-teaches": (
        "Add a teaches: key listing the decision IDs this entry EXPLAINS, inline:\n"
        "        teaches: [2026-09-20-001]\n"
        "    An empty list is legitimate if the entry explains no ratified decision:\n"
        "        teaches: []"
    ),
    "missing-verified": (
        "Add a verified: date — when the entry was last confirmed against what it teaches:\n"
        "        verified: 2026-09-20\n"
        "    Set it from the file's last commit date, never today, unless you just re-verified it."
    ),
    "bad-verified": (
        "Write verified: as an unquoted, zero-padded ISO date — verified: 2026-09-20\n"
        "    NOT quoted (\"2026-09-20\"), NOT a timestamp, NOT 2026-9-20. Those are valid YAML\n"
        "    but the freshness gate's regex reads them as missing, marking the entry UNSTAMPED."
    ),
    "parsers-disagree": (
        "Respell the key so both gates read it identically. teaches: must be an INLINE list\n"
        "    (teaches: [id, id]) — a YAML block list parses fine but is invisible to the\n"
        "    freshness gate, which silently skips the entry. IDs and dates go unquoted."
    ),
    "unindexed": (
        "Add a row to the Entries table in knowledge/INDEX.md:\n"
        "        | [<slug>](<slug>.md) | <one-line summary> | <type> |\n"
        "    An entry nobody can find from the index is a fact nobody re-reads."
    ),
    "dangling-row": (
        "The INDEX row links a file that does not exist. Restore the file or remove the row;\n"
        "    never leave a pointer to nothing."
    ),
    "no-entries-section": (
        "knowledge/INDEX.md must carry a `## Entries` heading with the table beneath it.\n"
        "    The index cross-check reads that section only; an unlocatable section fails loudly."
    ),
}


def index_links(index_text: str) -> set[str] | None:
    """Filenames linked from the Entries table, or None when the section cannot be located."""
    found = in_entries = False
    linked: set[str] = set()
    for line in index_text.splitlines():
        if line.startswith("## "):
            found = found or bool(ENTRIES_HEADING.match(line))
            in_entries = bool(ENTRIES_HEADING.match(line))
            continue
        if found and in_entries and line.startswith("|"):
            linked.update(INDEX_LINK.findall(line))
    return linked if found else None


def index_violations(index_text: str | None, entry_names: set[str]) -> list[tuple[str, str]]:
    """(rule, detail) pairs: every entry indexed, every row's file present, section locatable."""
    if index_text is None:
        return [("no-entries-section", "INDEX.md is missing")] if entry_names else []
    linked = index_links(index_text)
    if linked is None:
        return [("no-entries-section", "no `## Entries` heading found")]
    out: list[tuple[str, str]] = []
    for name in sorted(entry_names - linked):
        out.append(("unindexed", f"{name} has no row in INDEX.md"))
    for name in sorted(linked - entry_names):
        out.append(("dangling-row", f"INDEX.md links {name}, which does not exist"))
    return out


def key_line(raw_fm: str, key: str, default: int) -> int:
    """File line number of `key:` inside the frontmatter, or `default`."""
    for offset, line in enumerate(raw_fm.splitlines()):
        if re.match(rf"^{re.escape(key)}\s*:", line):
            return offset + 1
    return default


def yaml_view(value) -> str:
    """Normalize a YAML value to the string the freshness regex would have to produce to agree."""
    if type(value) is datetime.date:
        return value.isoformat()
    if value is None:
        return None
    return str(value)


def scan_entry(path: pathlib.Path) -> list[dict]:
    violations = []

    def add(line, rule, detail):
        violations.append(
            {"file": str(path), "line": line, "rule": rule, "detail": detail, "fix": FIXES[rule]}
        )

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        add(1, "no-frontmatter", "file does not begin with a --- frontmatter block")
        return violations
    end = text.find("\n---", 3)
    if end == -1:
        add(1, "no-frontmatter", "frontmatter block is never terminated by a closing ---")
        return violations

    raw_fm = text[3:end]

    try:
        data = yaml.safe_load(raw_fm)
    except yaml.YAMLError as e:
        line = 1
        mark = getattr(e, "problem_mark", None)
        if mark is not None:
            line = mark.line + 1
        problem = getattr(e, "problem", None) or str(e).splitlines()[0]
        add(line, "invalid-yaml", f"{type(e).__name__}: {problem}")
        return violations

    if not isinstance(data, dict):
        add(1, "invalid-yaml", f"frontmatter parsed as {type(data).__name__}, expected a mapping")
        return violations

    if "teaches" not in data:
        add(1, "missing-teaches", "no teaches: key")
    if "verified" not in data:
        add(1, "missing-verified", "no verified: key")

    if "verified" in data and type(data["verified"]) is not datetime.date:
        v = data["verified"]
        add(
            key_line(raw_fm, "verified", 1),
            "bad-verified",
            f"parsed as {type(v).__name__} ({v!r}), expected an unquoted ISO date",
        )

    # Cross-check: what does the freshness gate actually see?
    seen = kb_freshness_scan.parse_frontmatter(path) or {"teaches": [], "verified": None}
    if "teaches" in data:
        truth = [str(t) for t in data["teaches"]] if isinstance(data["teaches"], list) else data["teaches"]
        if truth != seen["teaches"]:
            add(
                key_line(raw_fm, "teaches", 1),
                "parsers-disagree",
                f"yaml reads teaches={truth!r}, freshness gate reads {seen['teaches']!r}",
            )
    if "verified" in data:
        truth = yaml_view(data["verified"])
        if truth != seen["verified"]:
            add(
                key_line(raw_fm, "verified", 1),
                "parsers-disagree",
                f"yaml reads verified={truth!r}, freshness gate reads {seen['verified']!r}",
            )

    return violations


# ==============================================================================
# SELF-TEST — the index cross-check proves its own boundary
# ==============================================================================

_INDEX = ("# Knowledge Base — Index\n\nSee `scripts/kb_freshness_scan.py` and `reference_ghost.md` in prose.\n\n"
          "## Entries\n\n| Slug | Summary | Type |\n|---|---|---|\n"
          "| [reference_a](reference_a.md) | a | reference |\n"
          "| [reference_b](reference_b.md) | b | reference |\n")


def run_self_test() -> int:
    print("\nKB Index Cross-Check Self-Test")
    print("=" * 60)
    failures = total = 0

    def expect(label: str, found: list, *rules: str) -> None:
        nonlocal failures, total
        total += 1
        got = sorted(r for r, _ in found)
        ok = got == sorted(rules)
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok:
            print(f"        rules={got} expected={sorted(rules)}")
            failures += 1

    expect("every entry indexed and every row resolvable passes",
           index_violations(_INDEX, {"reference_a.md", "reference_b.md"}))
    expect("a filename quoted in the header prose is not an index row (scoped to Entries)",
           index_violations(_INDEX, {"reference_a.md", "reference_b.md", "reference_ghost.md"}), "unindexed")
    expect("an entry with no row fails",
           index_violations(_INDEX, {"reference_a.md", "reference_b.md", "reference_c.md"}), "unindexed")
    expect("a row whose file is gone fails", index_violations(_INDEX, {"reference_a.md"}), "dangling-row")
    expect("a missing Entries heading fails loudly, never as zero rows",
           index_violations(_INDEX.replace("## Entries", "## Items"), {"reference_a.md"}), "no-entries-section")
    expect("a missing INDEX.md with entries present fails", index_violations(None, {"reference_a.md"}),
           "no-entries-section")
    expect("a missing INDEX.md with no entries is nothing to check", index_violations(None, set()))

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return run_self_test()
    if not KB.is_dir():
        print(f"kb_frontmatter_scan: no knowledge base at {KB} — nothing to check.")
        return 0

    entries = [p for p in sorted(KB.glob("*.md")) if p.name != "INDEX.md"]
    violations = []
    for path in entries:
        violations.extend(scan_entry(path))

    index_text = INDEX.read_text(encoding="utf-8") if INDEX.is_file() else None
    for rule, detail in index_violations(index_text, {p.name for p in entries}):
        violations.append({"file": str(INDEX), "line": 1, "rule": rule, "detail": detail, "fix": FIXES[rule]})

    print("\nKB Frontmatter Scan Results")
    print("=" * 60)
    print(f"Entries scanned: {len(entries)}")
    print(f"Violations found: {len(violations)}")

    if violations:
        print("\n" + "!" * 60)
        print("BLOCKED: Knowledge-entry frontmatter is unreadable or unreadable-as-intended\n")
        for v in violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    Rule:    {v['rule']}")
            print(f"    Detail:  {v['detail']}")
            print(f"    Fix:     {v['fix']}")
            print()
        return 1

    print("\nPASSED: All frontmatter parses, and both gates read it identically")
    return 0


if __name__ == "__main__":
    sys.exit(main())
