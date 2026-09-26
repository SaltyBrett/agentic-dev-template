#!/usr/bin/env python3
"""
Banned Feature Scanner

Pre-commit gate that scans project files for banned features.
Prevents GCC-incompatible services from entering the codebase.

Usage:
    pre-commit run banned-feature-scan --all-files        # portable; pre-commit owns the interpreter

    # Direct invocation is needed only for --path. The interpreter name is OS-dependent:
    # `python3` on macOS/Linux, `python` on Windows. There is no portable bare name
    # (see docs/orchestration/knowledge/reference_precommit_interpreter.md).
    python3 scripts/banned_feature_scan.py [--path PATH]

Exit codes:
    0 - No banned features found
    1 - Banned features detected (blocks commit)

Customize the BANNED_PATTERNS dict below for your project.
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import project_profile  # noqa: E402 — shared profile resolution

# ==============================================================================
# CUSTOMIZE THESE PATTERNS FOR YOUR PROJECT
# ==============================================================================

# GCC-only. Applied when `.project-profile` says `gcc`, and in the template itself
# (no profile = the union of every profile, the strictest reading). A commercial
# project does not carry this law in its docs and does not get it enforced here —
# the gate and CONSTITUTION.md read the same file, so they cannot disagree.
# See scripts/project_profile.py and [[reference_project_profiles]].
GCC_BANNED_PATTERNS = {
    # GCC-Incompatible Fabric Features (non-negotiable for Azure GCC projects)
    "Direct Lake": [
        r"DirectLake",
        r"direct[\s_-]?lake",
        r"\"mode\":\s*\"DirectLake\"",
    ],
    "Fabric Dataflows Gen2": [
        r"Dataflow\s*Gen\s*2",
        r"dataflows?\s*gen\s*2",
        r"DataflowGen2",
    ],
    "Shortcuts (as critical dependency)": [
        r"\"type\":\s*\"Shortcut\"",
        r"create\s+shortcut",
        r"OneLakeShortcut",
    ],
    "DirectQuery (over non-GCC structures)": [
        r"\"mode\":\s*\"DirectQuery\"",
        r"directQuery.*mode",
    ],
    "Object-Level Security (OLS)": [
        r"objectLevelSecurity",
        r"OLS\s*=\s*true",
        r"\"ols\"",
    ],
}

# Applied on every profile. Add project-specific banned patterns here.
ALWAYS_BANNED_PATTERNS: dict[str, list[str]] = {}


def active_banned_patterns() -> dict:
    """The pattern set this project actually enforces."""
    patterns = dict(ALWAYS_BANNED_PATTERNS)
    if project_profile.gcc_active():
        patterns.update(GCC_BANNED_PATTERNS)
    return patterns

# ==============================================================================
# CONTENT RULES — checked separately from BANNED_PATTERNS, on purpose
# ==============================================================================
#
# These run against every scanned file INCLUDING the ones in EXCLUDE_FILES.
# That exclusion list exempts governance docs that legitimately *name* banned
# Fabric features. It must not exempt them from these rules, because AGENTS.md
# and AGENT_COLDSTART_CHECKLIST.md are on it and are precisely where the
# bare-`python` defect last landed. A rule added to BANNED_PATTERNS instead
# would have been inert in the two files it most needed to cover.
#
# Formerly PORTABILITY_RULES. Renamed when the provenance rule below joined it:
# "no employer identifier" is not a portability concern, and filing it under a
# name that says otherwise misleads the next reader. The channel is defined by
# its SCOPE — every file, no exceptions — not by a topic.
#
# A rule carries EITHER `patterns` (regex) or `hashes` (see below), plus its own
# `allow` set of filenames and a `fix` string. Exemptions are per-rule and
# per-file, never whole-file.

# --- Why the provenance rule matches hashes rather than names -----------------
# An identifier this repository must never contain cannot be written into this
# repository in order to be banned. Listing it in plaintext would put the very
# string in `scripts/banned_feature_scan.py`, and force the scanner to exempt
# itself — defeating the rule to state it.
#
# So identifiers are stored as SHA-256 of their normalized form. Text is
# lowercased, stripped to alphanumerics and re-joined, so a name written
# "Widget Corp", "widget-corp" or "WIDGETCORP" reduces to one hash.
#
# Examples here are deliberately fictional. This comment first used a real
# identifier while explaining that real identifiers must never be written here,
# and the rule below caught it on the next run. Keep the examples fake.
#
# HONEST LIMIT: a hash is non-disclosure, not secrecy. It is unsalted — a salt
# stored beside it protects nothing — so anyone who already guesses a name can
# confirm it. The goal is that the name is not *published* by the control, not
# that it is unknowable.
#
# Add one:  python3 scripts/banned_feature_scan.py --add-identifier "Name"

N_GRAM_MAX = 3


def normalize_words(text: str) -> list[str]:
    """Lowercase, split on anything non-alphanumeric."""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).split()


def identifier_hash(value: str) -> str:
    """SHA-256 of a normalized identifier, joined without separators."""
    return hashlib.sha256("".join(normalize_words(value)).encode()).hexdigest()


def line_hashes(line: str) -> set[str]:
    """Hashes of every 1..N word run in a line, concatenated without separators.

    The n-gram sweep is what catches a multi-word identifier written with any
    spacing or punctuation: "Widget Corp" and "widget-corp" both reach "widgetcorp".
    """
    words = normalize_words(line)
    found = set()
    for size in range(1, N_GRAM_MAX + 1):
        for start in range(len(words) - size + 1):
            found.add(hashlib.sha256("".join(words[start:start + size]).encode()).hexdigest())
    return found


CONTENT_RULES = {
    "Bare `python` invocation (macOS ships no unversioned `python`)": {
        # `python3 scripts/…` deliberately does NOT match: \s+ cannot cross the "3".
        "patterns": [r"\bpython\s+\.?/?scripts/"],
        "allow": {
            # `entry:` lines resolve inside pre-commit's own virtualenv, which
            # always contains `python`. This is the one correct use.
            ".pre-commit-config.yaml",
            # Quotes the broken pattern in order to teach it.
            "reference_precommit_interpreter.md",
            # Holds the pattern itself.
            "banned_feature_scan.py",
        },
        "fix": (
            "Run gates through pre-commit, which provisions its own interpreter:\n"
            "      pre-commit run <hook-id> --all-files\n"
            "    Where a real interpreter is unavoidable (ad-hoc flags, md_to_docx.py),\n"
            "    write `python3` and state the Windows form beside it.\n"
            "    See docs/orchestration/knowledge/reference_precommit_interpreter.md"
        ),
    },
    "Employer identifier in the personal lineage": {
        # Decision 2026-09-19-001 split this template from employer brand and
        # program content. That split was procedural until now. No `allow` set:
        # there is no file in this repository where such a name belongs.
        "hashes": {
            "807e166a67e4bd8145d99fe4e5ec97ae4f4acb75798d1cb4a06e31c6e328b42e",
        },
        "allow": set(),
        "fix": (
            "Remove the employer product, program, platform or brand name from this\n"
            "    line. The personal lineage carries the governance machinery only —\n"
            "    decision 2026-09-19-001. If the work genuinely belongs to the employer\n"
            "    repository, it goes there, not here.\n"
            "    Add another identifier: python3 scripts/banned_feature_scan.py --add-identifier \"Name\""
        ),
    },
    # Add project-specific content rules below this line
}

# File extensions to scan
SCAN_EXTENSIONS = {".sql", ".json", ".py", ".ps1", ".yaml", ".yml", ".dax", ".pq", ".md"}

# Directories to exclude from scanning
EXCLUDE_DIRS = {
    "archive",
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".env",
}

# Directories whose JOB is to explain the rules, which necessarily means naming what
# the rules ban. Excluding them one filename at a time is whack-a-mouse: the next
# knowledge entry that explains a rule breaks the build again.
#
# This applies to BANNED_PATTERNS ONLY. CONTENT_RULES still covers every file here,
# so the provenance and portability rules keep policing the knowledge base. That
# separation is the entire reason the two channels exist (decision 2026-09-20-002).
EXCLUDE_BANNED_DIRS = {"knowledge"}

# Files to exclude from scanning (standards/docs that MENTION banned features)
EXCLUDE_FILES = {
    "banned_feature_scan.py",
    # Decision bodies explain why a feature is banned, so they name it.
    "decision-log.md",
    "framework_decisions.md",
    # Explains which features are GCC-only, so it necessarily names them. Still
    # covered by CONTENT_RULES, which EXCLUDE_FILES does not reach.
    "project_profile.py",
    "CONSTITUTION.md",
    "AGENTS.md",
    "AGENT_COLDSTART_CHECKLIST.md",
    "doc_control_standard.md",
    "TEMPLATE_GUIDE.md",
}


def candidate_files(root: Path) -> list[Path]:
    """Files git would actually commit: tracked, plus untracked-but-not-ignored.

    A gitignored file can never enter the repository, so scanning one blocks a
    commit over content that will never be committed. That is a false positive,
    and a baffling one — it names a file the author cannot fix by committing.
    Found when `.claude/settings.local.json`, which the global gitignore covers,
    failed the provenance rule.

    Falls back to a filesystem walk outside a git repository.
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root, capture_output=True, text=True, check=False,
        )
        if out.returncode == 0:
            return [root / line for line in out.stdout.splitlines() if line.strip()]
    except OSError:  # pragma: no cover - git absent
        pass
    return [p for p in root.rglob("*") if p.is_file()]


def should_scan(filepath: Path) -> bool:
    """Determine if a file should be scanned."""
    if filepath.suffix.lower() not in SCAN_EXTENSIONS:
        return False

    if filepath.name in EXCLUDE_FILES:
        return False

    for part in filepath.parts:
        if part in EXCLUDE_DIRS or part in EXCLUDE_BANNED_DIRS:
            return False

    return True


def should_scan_content(filepath: Path) -> bool:
    """Like should_scan, but ignores EXCLUDE_FILES — see CONTENT_RULES."""
    if filepath.suffix.lower() not in SCAN_EXTENSIONS:
        return False

    for part in filepath.parts:
        if part in EXCLUDE_DIRS:
            return False

    return True


def scan_content(filepath: Path) -> list[dict]:
    """Scan a single file for content-rule violations (regex or hashed identifier)."""
    violations = []
    try:
        lines = filepath.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as e:
        print(f"  WARNING: Could not scan {filepath}: {e}", file=sys.stderr)
        return violations

    def record(line_num: int, line: str, rule_name: str, rule: dict) -> None:
        violations.append(
            {
                "file": str(filepath),
                "line": line_num,
                "feature": rule_name,
                "fix": rule["fix"],
                "content": line.strip()[:120],
            }
        )

    for rule_name, rule in CONTENT_RULES.items():
        if filepath.name in rule["allow"]:
            continue

        for pattern in rule.get("patterns", []):
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    record(line_num, line, rule_name, rule)

        wanted = rule.get("hashes")
        if wanted:
            for line_num, line in enumerate(lines, 1):
                if line_hashes(line) & wanted:
                    record(line_num, line, rule_name, rule)

    return violations


def scan_file(filepath: Path) -> list[dict]:
    """Scan a single file for banned patterns."""
    violations = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()

        for feature_name, patterns in active_banned_patterns().items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append(
                            {
                                "file": str(filepath),
                                "line": line_num,
                                "feature": feature_name,
                                "pattern": pattern,
                                "content": line.strip()[:120],
                            }
                        )
    except Exception as e:
        print(f"  WARNING: Could not scan {filepath}: {e}", file=sys.stderr)

    return violations


# ==============================================================================
# SELF-TEST — in-memory fixtures, run on every commit
# ==============================================================================

def run_self_test() -> int:
    print("\nContent Rules Self-Test")
    print("=" * 60)
    failures = 0

    def check(label, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"  ok    {label}")
        else:
            print(f"  FAIL  {label}")
            if detail:
                print(f"        {detail}")
            failures += 1

    py = CONTENT_RULES["Bare `python` invocation (macOS ships no unversioned `python`)"]
    pat = py["patterns"][0]
    check("the bare-python rule still discriminates",
          bool(re.search(pat, "python scripts/x.py")) and not re.search(pat, "python3 scripts/x.py"))

    # Every spelling of an identifier must reach one hash, or the rule is bypassed
    # by typing the name differently — which is exactly what someone does by accident.
    variants = ["Widget Corp", "widget-corp", "WIDGETCORP", "Widget  Corp"]
    hashes = {identifier_hash(v) for v in variants}
    check("identifier spellings collapse to one hash", len(hashes) == 1, f"{len(hashes)} distinct")

    target = identifier_hash("Widget Corp")
    check("a multi-word identifier is found in prose",
          target in line_hashes("our Widget Corp deployment"))
    check("punctuation between the words does not hide it",
          target in line_hashes("the widget-corp instance"))
    check("an unrelated line does not match",
          target not in line_hashes("a perfectly ordinary sentence about widgets"))

    check("n-grams cover up to N_GRAM_MAX words",
          identifier_hash("one two three") in line_hashes("x one two three y")
          and identifier_hash("one two three four") not in line_hashes("x one two three four y"))

    emp = CONTENT_RULES["Employer identifier in the personal lineage"]
    check("the provenance rule has an EMPTY allow set", emp["allow"] == set(),
          "there is no file in this repo where such a name belongs")
    check("the provenance rule stores hashes, not names",
          "hashes" in emp and "patterns" not in emp
          and all(re.fullmatch(r"[0-9a-f]{64}", h) for h in emp["hashes"]))

    # The defining property of this channel, pinned: EXCLUDE_FILES must not reach it.
    check("content rules bypass EXCLUDE_FILES",
          should_scan_content(Path("AGENTS.md")) and not should_scan(Path("AGENTS.md")),
          "AGENTS.md is in EXCLUDE_FILES and must still be content-scanned")

    # The knowledge base is exempt from BANNED_PATTERNS because its job is to explain
    # the rules. It must NOT thereby fall out of the provenance and portability rules.
    kb = Path("docs/orchestration/knowledge/reference_project_profiles.md")
    check("the knowledge base is exempt from banned patterns but NOT from content rules",
          should_scan_content(kb) and not should_scan(kb))

    check("every rule carries a fix and an allow set",
          all("fix" in r and "allow" in r for r in CONTENT_RULES.values()))

    total = 11
    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description="Scan for banned features in project files")
    parser.add_argument("--path", default=".", help="Root path to scan (default: current directory)")
    parser.add_argument(
        "--add-identifier", metavar="NAME",
        help="Print the hash for an employer identifier, to paste into CONTENT_RULES",
    )
    parser.add_argument(
        "--self-test", action="store_true", help="Run in-memory fixtures and exit",
    )
    args = parser.parse_args()

    if args.self_test:
        sys.exit(run_self_test())

    if args.add_identifier:
        digest = identifier_hash(args.add_identifier)
        words = normalize_words(args.add_identifier)

        # A single common word makes a denylist that blocks innocuous prose. Measure it
        # against the repository rather than guessing: the author should see the cost
        # before pasting the hash, not after the next commit is refused.
        root = Path(args.path).resolve()
        collisions = []
        for filepath in candidate_files(root):
            if not filepath.is_file() or not should_scan_content(filepath.relative_to(root)):
                continue
            for line_num, line in enumerate(
                filepath.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
            ):
                if digest in line_hashes(line):
                    collisions.append(f"{filepath.relative_to(root)}:{line_num}")

        print(f'\nAdd this line to CONTENT_RULES["Employer identifier in the personal lineage"]["hashes"]:\n')
        print(f'            "{digest}",\n')
        print("The name itself is deliberately not written to any file.")

        if collisions:
            print(f"\n  WARNING: this would already block {len(collisions)} existing line(s):")
            for hit in collisions[:5]:
                print(f"    {hit}")
            if len(collisions) > 5:
                print(f"    ... and {len(collisions) - 5} more")
            print("  A single common word makes a denylist that blocks ordinary prose.")
            print("  Prefer the fuller form — 'Acme Core' rather than 'Core'.")
        elif len(words) == 1 and len(words[0]) <= 5:
            print(f"\n  NOTE: {args.add_identifier!r} is one short word. It collides with nothing here")
            print("  today, but a short common word is the shape that causes false positives later.")
        else:
            print("\n  No collisions in this repository.")
        sys.exit(0)

    root = Path(args.path).resolve()
    all_violations = []
    content_violations = []
    files_scanned = 0

    for filepath in sorted(candidate_files(root)):
        if not filepath.is_file():
            continue
        rel = filepath.relative_to(root)
        scan_banned = should_scan(rel)
        scan_port = should_scan_content(rel)
        if not (scan_banned or scan_port):
            continue
        files_scanned += 1
        if scan_banned:
            all_violations.extend(scan_file(filepath))
        if scan_port:
            content_violations.extend(scan_content(filepath))

    # Report results
    print(f"\nBanned Feature Scan Results")
    print(f"{'=' * 60}")
    print(f"Files scanned: {files_scanned}")
    print(f"Violations found: {len(all_violations) + len(content_violations)}")

    if all_violations:
        print(f"\n{'!' * 60}")
        print("BLOCKED: Banned features detected\n")
        for v in all_violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    Feature: {v['feature']}")
            print(f"    Content: {v['content']}")
            print()

    if content_violations:
        print(f"\n{'!' * 60}")
        print("BLOCKED: Content rule violations\n")
        for v in content_violations:
            print(f"  {v['file']}:{v['line']}")
            print(f"    Rule:    {v['feature']}")
            print(f"    Content: {v['content']}")
            print(f"    Fix:     {v['fix']}")
            print()

    if all_violations or content_violations:
        sys.exit(1)

    print("\nPASSED: No banned features found")
    sys.exit(0)


if __name__ == "__main__":
    main()
