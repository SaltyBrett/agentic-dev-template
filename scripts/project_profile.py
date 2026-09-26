#!/usr/bin/env python3
"""
project_profile.py — a project starts under GCC/Gov constraints or under none, mechanically.

THE PROBLEM THIS SOLVES
-----------------------
The GCC compliance regime — banned Direct Lake, Dataflows Gen2, DirectQuery, OLS,
mandatory Power BI Import mode, RLS + DAX masking — is the law of one kind of
engagement, not of every project. A purely commercial project inherits rules that
do not apply to it, and a governance document that states a rule nobody enforces
is the fossil `CONSTITUTION.md` §6.3 exists to prevent.

A note saying "ignore section 5 if commercial" would be exactly that fossil. So
the toggle is mechanical, and it fires once, at project birth.

HOW IT WORKS
------------
`.project-profile` holds one word: `gcc` or `commercial`. `new_project.py`
requires `--profile` and writes it. Two things then follow from that one value:

  1. **Documents are stripped.** Profile-specific prose is fenced:

         <!-- profile:gcc -->
         ...GCC-only law...
         <!-- /profile:gcc -->

     A commercial project keeps no `gcc` block, and vice versa. The rule is
     removed from the document, not annotated as inapplicable.

  2. **The scanner switches.** `banned_feature_scan.py` applies the GCC pattern
     set only under the `gcc` profile. The gate and the governance text always
     agree, because both read the same file.

THE TEMPLATE ITSELF HAS NO PROFILE
----------------------------------
No `.project-profile` means "this is the template", which keeps **every** profile's
blocks and applies the **union** of the rules — the strictest reading. That is
fail-closed, and it is why the template can still carry GCC law it does not impose
on every descendant.

An unknown value in `.project-profile` is an error, never a default. A toggle that
silently picks a side is not a toggle.

Usage:  pre-commit run project-profile --all-files
        python3 scripts/project_profile.py [--check | --self-test]
Exit 0 = clean, 1 = markers unbalanced or a foreign profile survived, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_FILE = ROOT / ".project-profile"

PROFILES = ("gcc", "commercial")

# `<!-- profile:gcc -->` … `<!-- /profile:gcc -->`. HTML comments so they vanish
# when the markdown renders, and so a reader of the raw file sees the boundary.
OPEN = re.compile(r"^\s*<!--\s*profile:([a-z0-9_-]+)\s*-->\s*$")
CLOSE = re.compile(r"^\s*<!--\s*/profile:([a-z0-9_-]+)\s*-->\s*$")

SCAN_SUFFIXES = {".md"}
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}

FIX = {
    "unknown-profile": (
        f"Profile names are {' or '.join(PROFILES)}. Fix the marker, or add the new\n"
        "    profile to PROFILES in scripts/project_profile.py."
    ),
    "unclosed": (
        "Every <!-- profile:X --> needs a matching <!-- /profile:X -->.\n"
        "    An unclosed block silently swallows the rest of the file when stripped."
    ),
    "unopened": "A closing marker with no opening marker above it.",
    "nested": (
        "Profile blocks do not nest. Close the first before opening the second —\n"
        "    nesting makes 'which profile owns this line' ambiguous."
    ),
    "foreign-profile": (
        "This project declares one profile in .project-profile, but a block for a\n"
        "    different profile survived initialization. Re-run the initializer, or\n"
        "    delete the block: the rule does not apply to this project and a document\n"
        "    stating a rule nobody enforces is the fossil CONSTITUTION §6.3 forbids."
    ),
}


def read_profile(root: Path = ROOT) -> str | None:
    """The project's profile, or None when this is the template itself."""
    path = root / ".project-profile"
    if not path.is_file():
        return None
    value = path.read_text(encoding="utf-8").strip().lower()
    if value not in PROFILES:
        raise ValueError(
            f".project-profile contains {value!r}; expected one of {', '.join(PROFILES)}"
        )
    return value


def gcc_active(root: Path = ROOT) -> bool:
    """True when GCC rules apply: the gcc profile, or the template (union of all)."""
    profile = read_profile(root)
    return profile in (None, "gcc")


def validate_markers(text: str) -> list[tuple[int, str, str]]:
    """Return (line_no, rule, detail) for each structural problem."""
    problems: list[tuple[int, str, str]] = []
    open_stack: list[tuple[int, str]] = []

    for line_no, line in enumerate(text.splitlines(), start=1):
        opened = OPEN.match(line)
        closed = CLOSE.match(line)
        if opened:
            name = opened.group(1)
            if name not in PROFILES:
                problems.append((line_no, "unknown-profile", f"unknown profile {name!r}"))
            if open_stack:
                problems.append(
                    (line_no, "nested", f"{name!r} opened inside {open_stack[-1][1]!r}")
                )
            open_stack.append((line_no, name))
        elif closed:
            name = closed.group(1)
            if not open_stack:
                problems.append((line_no, "unopened", f"closes {name!r}, which was never opened"))
            elif open_stack[-1][1] != name:
                problems.append(
                    (line_no, "unopened", f"closes {name!r}, but {open_stack[-1][1]!r} is open")
                )
                open_stack.pop()
            else:
                open_stack.pop()

    for line_no, name in open_stack:
        problems.append((line_no, "unclosed", f"{name!r} is never closed"))
    return problems


def profiles_present(text: str) -> set[str]:
    return {m.group(1) for line in text.splitlines() if (m := OPEN.match(line))}


def strip_profiles(text: str, keep: str | None) -> str:
    """Remove blocks belonging to a profile other than `keep`.

    `keep=None` keeps everything, which is the template's own state. The markers
    themselves are removed from kept blocks so a derived project reads cleanly.
    """
    out: list[str] = []
    dropping = False
    for line in text.splitlines(keepends=True):
        opened = OPEN.match(line.rstrip("\n"))
        closed = CLOSE.match(line.rstrip("\n"))
        if opened:
            if keep is not None and opened.group(1) != keep:
                dropping = True
            continue  # the marker line itself never survives
        if closed:
            dropping = False
            continue
        if not dropping:
            out.append(line)
    return "".join(out)


def markdown_files(root: Path) -> list[Path]:
    return [
        p for p in sorted(root.rglob("*"))
        if p.is_file() and p.suffix in SCAN_SUFFIXES and not (set(p.parts) & SKIP_DIRS)
    ]


def check() -> int:
    try:
        profile = read_profile()
    except ValueError as exc:
        print(f"project_profile: BLOCKED — {exc}")
        print("  A toggle that silently picks a side is not a toggle.")
        return 1

    violations: list[tuple[str, int, str, str]] = []
    for path in markdown_files(ROOT):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, rule, detail in validate_markers(text):
            violations.append((str(path.relative_to(ROOT)), line_no, rule, detail))
        if profile is not None:
            for name in profiles_present(text) - {profile}:
                violations.append(
                    (str(path.relative_to(ROOT)), 1, "foreign-profile",
                     f"carries a {name!r} block, but this project is {profile!r}")
                )

    label = profile or "template (no .project-profile — all profiles kept, union enforced)"
    print("\nProject Profile Gate")
    print("=" * 60)
    print(f"Profile:    {label}")
    print(f"Files:      {len(markdown_files(ROOT))}")
    print(f"Violations: {len(violations)}")

    if violations:
        print("\n" + "!" * 60)
        print("BLOCKED: profile markers are not sound\n")
        for rel, line_no, rule, detail in violations:
            print(f"  {rel}:{line_no}")
            print(f"    Rule:   {rule}")
            print(f"    Detail: {detail}")
            print(f"    Fix:    {FIX[rule]}")
            print()
        return 1

    print(f"\nPASSED: markers balanced; GCC rules {'apply' if gcc_active() else 'do NOT apply'}")
    return 0


# ==============================================================================
# SELF-TEST — in-memory fixtures, run on every commit
# ==============================================================================

_DOC = """intro
<!-- profile:gcc -->
gcc only
<!-- /profile:gcc -->
middle
<!-- profile:commercial -->
commercial only
<!-- /profile:commercial -->
tail
"""


def run_self_test() -> int:
    print("\nProject Profile Self-Test")
    print("=" * 60)
    failures = 0

    def check_case(label, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"  ok    {label}")
        else:
            print(f"  FAIL  {label}")
            if detail:
                print(f"        {detail}")
            failures += 1

    gcc = strip_profiles(_DOC, "gcc")
    com = strip_profiles(_DOC, "commercial")
    tmpl = strip_profiles(_DOC, None)

    check_case("gcc keeps gcc and drops commercial",
               "gcc only" in gcc and "commercial only" not in gcc, gcc)
    check_case("commercial keeps commercial and drops gcc",
               "commercial only" in com and "gcc only" not in com, com)
    check_case("the template keeps both", "gcc only" in tmpl and "commercial only" in tmpl)
    check_case("shared prose survives every profile",
               all("intro" in t and "middle" in t and "tail" in t for t in (gcc, com, tmpl)))
    check_case("marker lines never survive",
               not any("profile:" in t for t in (gcc, com, tmpl)), gcc)

    check_case("a sound document has no problems", validate_markers(_DOC) == [])
    check_case("an unclosed block is caught",
               any(r == "unclosed" for _, r, _ in validate_markers("<!-- profile:gcc -->\nx\n")))
    check_case("a stray close is caught",
               any(r == "unopened" for _, r, _ in validate_markers("<!-- /profile:gcc -->\n")))
    check_case("nesting is caught",
               any(r == "nested" for _, r, _ in
                   validate_markers("<!-- profile:gcc -->\n<!-- profile:commercial -->\nx\n"
                                    "<!-- /profile:commercial -->\n<!-- /profile:gcc -->\n")))
    check_case("an unknown profile name is caught",
               any(r == "unknown-profile" for _, r, _ in
                   validate_markers("<!-- profile:classified -->\nx\n<!-- /profile:classified -->\n")))

    # An unclosed block would swallow the rest of the file when stripped. That is why
    # the balance check is a gate and not a nicety.
    swallowed = strip_profiles("keep\n<!-- profile:gcc -->\nlost\n", "commercial")
    check_case("an unclosed block demonstrably swallows the tail",
               "lost" not in swallowed and "keep" in swallowed, swallowed)

    check_case("every marker rule has a fix string",
               set(FIX) >= {"unknown-profile", "unclosed", "unopened", "nested", "foreign-profile"})

    total = 12
    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and report the project profile")
    parser.add_argument("--check", action="store_true", help="Validate markers (default)")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
