#!/usr/bin/env python3
"""
Banned Feature Scanner

Pre-commit gate with two channels: the features a project bans, and the content rules that hold
for every file.

Usage:
    pre-commit run banned-feature-scan --all-files        # portable; pre-commit owns the interpreter

    # Direct invocation is needed only for --path. The interpreter name is OS-dependent:
    # `python3` on macOS/Linux, `python` on Windows. There is no portable bare name.
    python3 scripts/banned_feature_scan.py [--path PATH]

Exit codes:
    0 - No banned feature and no content-rule violation found
    1 - A violation found (blocks commit)

A project bans a feature by adding its patterns to BANNED_PATTERNS below (TEMPLATE_GUIDE.md,
Customizing the law).
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# ==============================================================================
# CUSTOMIZE THESE PATTERNS FOR YOUR PROJECT
# ==============================================================================

# The features this project bans, each a list of case-insensitive patterns. The template bans
# none; a project adds its own here and names them in CONSTITUTION.md.
BANNED_PATTERNS: dict[str, list[str]] = {}

# ==============================================================================
# CONTENT RULES - checked separately from BANNED_PATTERNS, on purpose
# ==============================================================================
#
# These run against every scanned file INCLUDING the ones in EXCLUDE_FILES. That exclusion list
# exempts the documents that legitimately *name* a banned feature. It must not exempt them from
# these rules, because AGENTS.md is on it and is precisely where the bare-`python` defect last
# landed. A rule added to BANNED_PATTERNS instead would be inert in the files it most needs to
# cover. The channel is defined by its SCOPE, every file, not by a topic.
#
# A rule carries `patterns` (regex), its own `allow` set of filenames and a `fix` string.
# Exemptions are per-rule and per-file, never whole-file.

HOME_PATH_RULE = "Absolute home-directory path (it names the person whose machine wrote it)"

CONTENT_RULES = {
    "Bare `python` invocation (macOS ships no unversioned `python`)": {
        # `python3 scripts/...` deliberately does NOT match: \s+ cannot cross the "3".
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
            "    write `python3` and state the Windows form beside it."
        ),
    },
    HOME_PATH_RULE: {
        # macOS, Linux and Windows home roots. A placeholder after the root (`/Users/<user>/`)
        # does not match, and a root inside a URL (`example.com/home/docs/`) is not a path.
        "patterns": [
            r"(?<![\w.-])/Users/(?!<)[^/\s`'\"]+/",
            r"(?<![\w.-])/home/(?!<)[^/\s`'\"]+/",
            r"\b[A-Za-z]:\\{1,2}Users\\{1,2}(?!<)[^\\\s`'\"]+\\",
        ],
        "allow": {
            # Holds the patterns themselves.
            "banned_feature_scan.py",
        },
        "fix": (
            "Write the path relative to the repository, under `~`, or with a placeholder after\n"
            "    the home root (`/Users/<user>/`): an absolute home path names the person whose\n"
            "    machine wrote it."
        ),
    },
    # Add project-specific content rules below this line
}

# Every text file git would commit is scanned, whatever its extension: a fixed list misses the next
# file type a project writes. A file is text when it holds no NUL byte and
# decodes as UTF-8.

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

# Directories whose JOB is to explain the rules, which necessarily means naming what the rules
# ban. Excluding them one filename at a time is whack-a-mole: the next knowledge entry that
# explains a rule breaks the build again.
#
# This applies to BANNED_PATTERNS ONLY. CONTENT_RULES still covers every file here, so the
# content rules keep policing the knowledge base. That separation is the entire reason the two
# channels exist.
EXCLUDE_BANNED_DIRS = {"knowledge"}

# Files to exclude from BANNED_PATTERNS: the law and the decisions name what they ban.
EXCLUDE_FILES = {
    "banned_feature_scan.py",
    "decision-log.md",
    "framework_decisions.md",
    "CONSTITUTION.md",
    "AGENTS.md",
    "TEMPLATE_GUIDE.md",
}


def candidate_files(root: Path) -> list[Path]:
    """Files git would actually commit: tracked, plus untracked-but-not-ignored.

    A gitignored file can never enter the repository, so scanning one blocks a
    commit over content that will never be committed. That is a false positive,
    and a baffling one: it names a file the author cannot fix by committing.

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


def is_text(filepath: Path) -> bool:
    """True for a file that holds no NUL byte and decodes as UTF-8; a binary file is not scanned."""
    try:
        data = filepath.read_bytes()
        data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return b"\0" not in data


def should_scan(filepath: Path) -> bool:
    """Determine if a file should be scanned for banned features."""
    if filepath.name in EXCLUDE_FILES:
        return False

    for part in filepath.parts:
        if part in EXCLUDE_DIRS or part in EXCLUDE_BANNED_DIRS:
            return False

    return True


def should_scan_content(filepath: Path) -> bool:
    """Like should_scan, but ignores EXCLUDE_FILES: see CONTENT_RULES."""
    for part in filepath.parts:
        if part in EXCLUDE_DIRS:
            return False

    return True


def scan_content(filepath: Path) -> list[dict]:
    """Scan a single file for content-rule violations."""
    violations = []
    try:
        lines = filepath.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as e:
        print(f"  WARNING: Could not scan {filepath}: {e}", file=sys.stderr)
        return violations

    for rule_name, rule in CONTENT_RULES.items():
        if filepath.name in rule["allow"]:
            continue
        for pattern in rule["patterns"]:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    violations.append({"file": str(filepath), "line": line_num, "feature": rule_name,
                                       "fix": rule["fix"], "content": line.strip()[:120]})
    return violations


def scan_file(filepath: Path, banned: dict[str, list[str]] | None = None) -> list[dict]:
    """Scan a single file for banned patterns."""
    violations = []
    try:
        lines = filepath.read_text(encoding="utf-8", errors="ignore").splitlines()
        for feature_name, patterns in (BANNED_PATTERNS if banned is None else banned).items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append({"file": str(filepath), "line": line_num, "feature": feature_name,
                                           "pattern": pattern, "content": line.strip()[:120]})
    except Exception as e:
        print(f"  WARNING: Could not scan {filepath}: {e}", file=sys.stderr)

    return violations


# ==============================================================================
# SELF-TEST - in-memory fixtures, run on every commit
# ==============================================================================

def run_self_test() -> int:
    print("\nContent Rules Self-Test")
    print("=" * 60)
    state = {"failures": 0, "total": 0}

    def check(label, ok, detail=""):
        state["total"] += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok:
            state["failures"] += 1
            if detail:
                print(f"        {detail}")

    py = CONTENT_RULES["Bare `python` invocation (macOS ships no unversioned `python`)"]
    pat = py["patterns"][0]
    check("the bare-python rule still discriminates",
          bool(re.search(pat, "python scripts/x.py")) and not re.search(pat, "python3 scripts/x.py"))

    # The defining property of this channel, pinned: EXCLUDE_FILES must not reach it.
    check("content rules bypass EXCLUDE_FILES",
          should_scan_content(Path("AGENTS.md")) and not should_scan(Path("AGENTS.md")),
          "AGENTS.md is in EXCLUDE_FILES and must still be content-scanned")

    # The knowledge base is exempt from BANNED_PATTERNS because its job is to explain
    # the rules. It must NOT thereby fall out of the content rules.
    kb = Path("docs/orchestration/" + "knowledge/reference_x.md")
    check("the knowledge base is exempt from banned patterns but NOT from content rules",
          should_scan_content(kb) and not should_scan(kb))

    home = CONTENT_RULES[HOME_PATH_RULE]["patterns"]

    def homed(text):
        return any(re.search(p, text) for p in home)

    check("an absolute home path is found on macOS, Linux and Windows",
          homed("a clone at /Users/someone/code/x") and homed("cd /home/someone/src")
          and homed(r"C:\Users\someone\code") and homed("'C:\\\\Users\\\\someone\\\\code'"))
    check("a placeholder after the home root passes", not homed("/Users/<user>/code/x") and not homed("/home/<user>/src"))
    check("a path under ~ or the repository passes", not homed("~/code/x") and not homed("../launch-probe/"))
    check("a home root inside a URL is not a path", not homed("https://example.com/home/docs/"))

    check("every rule carries patterns, a fix and an allow set",
          all("patterns" in r and "fix" in r and "allow" in r for r in CONTENT_RULES.values()))
    check("the template bans no feature of its own", BANNED_PATTERNS == {})

    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "model.json"
        f.write_text('{"mode": "Forbidden"}\n', encoding="utf-8")
        found = scan_file(f, {"A feature a project bans": [r"forbidden"]})
        check("a feature a project bans is found, case-insensitively, with its line",
              len(found) == 1 and found[0]["line"] == 1, str(found))
        check("a file with no banned feature passes", scan_file(f, {"Another": [r"absent"]}) == [])

        # Every text file is scanned, whatever its extension; a binary one is not.
        sh = Path(tmp) / "deploy.sh"
        sh.write_text("cd /Users/someone/src\n", encoding="utf-8")
        check("a file of any text type is scanned, as a shell script is",
              is_text(sh) and should_scan_content(Path("scripts/deploy.sh")) and should_scan(Path("src/main.rs"))
              and [v["feature"] for v in scan_content(sh)] == [HOME_PATH_RULE])
        blob = Path(tmp) / "image.gif"
        blob.write_bytes(b"GIF89a\x01\x00\x01\x00\x00\x00")   # valid UTF-8, so only the NUL bytes tell
        bad = Path(tmp) / "latin1.txt"
        bad.write_bytes("caf\xe9".encode("latin-1"))
        check("a binary file is skipped: a NUL byte, or bytes that are not UTF-8",
              not is_text(blob) and not is_text(bad) and is_text(f))

    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 1 if state["failures"] else 0


def main():
    parser = argparse.ArgumentParser(description="Scan for banned features and content-rule violations")
    parser.add_argument("--path", default=".", help="Root path to scan (default: current directory)")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()

    if args.self_test:
        sys.exit(run_self_test())

    root = Path(args.path).resolve()
    all_violations = []
    content_violations = []
    files_scanned = 0

    for filepath in sorted(candidate_files(root)):
        if not filepath.is_file() or not is_text(filepath):
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

    print("\nBanned Feature Scan Results")
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
