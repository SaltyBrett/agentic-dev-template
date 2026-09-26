#!/usr/bin/env python3
"""
template_version.py — the template's version is checked against its tags, not remembered.

THE GAP THIS CLOSES
-------------------
`new_project.py` stamps `.template-version` into every project it initializes, from a
constant in its own source. Nothing compared that constant to the actual tag. Tag
`v1.1.0` and forget to bump it, and every project created afterwards is labelled
`v1.0.0` — silently, with no error. That is the last hand-maintained value in this
repository and the same convention-instead-of-control shape as the rest of the audit.

WHAT IT CHECKS, ON EVERY COMMIT
-------------------------------
For every tag in the repository:

  1. the tag name is `vMAJOR.MINOR.PATCH`
  2. the commit the tag points at carries `TEMPLATE_VERSION = "<that tag>"`
  3. the tag's annotation names the bump type — MAJOR, MINOR or PATCH

Check 3 exempts the earliest tag, and not as a special case: a bump is defined
relative to a predecessor, and the first release has none.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
**It cannot stamp the commit being made.** At pre-commit time `git describe` reports
the *previous* commit, so any value written now would be stale by one. The version is
therefore set by an explicit release step and verified afterwards, rather than guessed
at during a commit.

**Between releases the constant names the last release.** A project created from an
untagged `main` is stamped with the previous version even though it carries newer
content. Tag before creating a project if the distinction matters. This is stated
rather than papered over; see [[reference_template_versioning]].

CUTTING A RELEASE
-----------------
    python3 scripts/template_version.py --release v1.1.0
    git add -A && git commit -m "release: v1.1.0"
    git tag -a v1.1.0 -m "MINOR: <what changed>"

`--release` rewrites the constant and prints those two commands. Doing it in the other
order tags a commit whose constant is wrong, and check 2 fails on your next commit.

Usage:  pre-commit run template-version --all-files
        python3 scripts/template_version.py [--check | --release vX.Y.Z | --self-test]
Exit 0 = clean, 1 = a tag and its commit disagree, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "scripts" / "new_project.py"

SEMVER = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
CONSTANT = re.compile(r'^TEMPLATE_VERSION\s*=\s*"([^"]*)"', re.MULTILINE)
BUMP_TYPE = re.compile(r"\b(MAJOR|MINOR|PATCH)\b")

FIX = {
    "bad-tag-name": (
        "Tags are vMAJOR.MINOR.PATCH — v1.1.0, not v1.1, 1.1.0 or release-2.\n"
        "    Retag: git tag -d <bad> && git tag -a v1.1.0 -m 'MINOR: ...'"
    ),
    "constant-mismatch": (
        "The tagged commit's TEMPLATE_VERSION does not match its tag, so projects\n"
        "    created from it are stamped with the wrong version. Cut releases with:\n"
        "        python3 scripts/template_version.py --release vX.Y.Z\n"
        "    then commit, THEN tag. Tagging first tags a commit with a stale constant."
    ),
    "no-bump-type": (
        "A tag annotation must name the bump it represents — MAJOR, MINOR or PATCH —\n"
        "    so the reason survives the decision. See knowledge/reference_template_versioning.md\n"
        "    Re-annotate: git tag -f -a <tag> -m 'MINOR: <what changed>'"
    ),
    "lightweight-tag": (
        "This tag has no annotation object, so it can carry no bump type. Locally: retag with\n"
        "    git tag -f -a <tag> -m 'MINOR: <what changed>'. On GitHub Actions the tag was\n"
        "    annotated when pushed and actions/checkout replaced it with a lightweight one;\n"
        "    the workflow restores it with `git fetch --force --tags origin` after checkout."
    ),
}


def git(*args: str) -> tuple[int, str]:
    try:
        out = subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
        )
        return out.returncode, out.stdout.strip()
    except OSError:  # pragma: no cover - git absent
        return 1, ""


def parse_constant(text: str) -> str | None:
    match = CONSTANT.search(text)
    return match.group(1) if match else None


def set_constant(text: str, version: str) -> str:
    return CONSTANT.sub(f'TEMPLATE_VERSION = "{version}"', text, count=1)


def is_valid_version(name: str) -> bool:
    return bool(SEMVER.match(name))


def names_bump_type(annotation: str) -> bool:
    return bool(BUMP_TYPE.search(annotation or ""))


def sort_key(name: str) -> tuple[int, int, int]:
    match = SEMVER.match(name)
    return tuple(int(g) for g in match.groups()) if match else (0, 0, 0)


TAG_FORMAT = "%(refname:short)|%(objecttype)|%(contents:subject)"


def parse_tag_rows(raw: str) -> list[tuple[str, str, str]]:
    """(name, objecttype, annotation subject) per tag, from `git tag -l --format=TAG_FORMAT`."""
    rows = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 2) + ["", ""]
        rows.append((parts[0], parts[1], parts[2]))
    return rows


def judge(name: str, objecttype: str, annotation: str, earliest: str | None,
          stamped: str | None) -> list[tuple[str, str]]:
    """The rules for one tag, as (rule, detail). `stamped` is None when the tagged
    commit predates the version-carrying file, which is not a violation.

    A lightweight tag is judged on its own, and never also as `no-bump-type`: for a
    lightweight tag `%(contents:subject)` is the COMMIT subject, so the bump-type rule
    would print the commit message as if it were an annotation that forgot the bump.
    That is exactly what the first tag-push run on GitHub did, and the diagnostic sent
    the reader to re-annotate a tag that was annotated all along.
    """
    if not is_valid_version(name):
        return [("bad-tag-name", f"{name!r} is not vMAJOR.MINOR.PATCH")]
    out: list[tuple[str, str]] = []
    if stamped is not None and stamped != name:
        out.append(("constant-mismatch", f"tag {name} points at a commit stamped {stamped!r}"))
    if name == earliest:
        return out  # no predecessor, so no bump to name and no annotation required
    if objecttype != "tag":
        out.append(("lightweight-tag",
                    f"tag {name} is a lightweight tag (points straight at a {objecttype})"))
    elif not names_bump_type(annotation):
        out.append(("no-bump-type",
                    f"annotation does not name MAJOR, MINOR or PATCH: {annotation!r}"))
    return out


def check() -> int:
    code, raw = git("tag", "-l", f"--format={TAG_FORMAT}")
    if code != 0:
        print("template_version: not a git repository — skipping.")
        return 0
    tags = parse_tag_rows(raw)
    if not tags:
        # A project created from this template has no tags. Nothing to verify, and
        # policing a derived project's versioning is not this gate's business.
        print("template_version: no tags in this repository — skipping.")
        return 0

    valid = [t for t, _, _ in tags if is_valid_version(t)]
    earliest = min(valid, key=sort_key) if valid else None

    violations: list[tuple[str, str, str]] = []
    for name, objecttype, annotation in tags:
        stamped = None
        if is_valid_version(name):
            code, blob = git("show", f"{name}:{VERSION_FILE.relative_to(ROOT)}")
            if code == 0:  # else the tag predates the version-carrying file
                stamped = parse_constant(blob)
        for rule, detail in judge(name, objecttype, annotation, earliest, stamped):
            violations.append((name, rule, detail))

    print("\nTemplate Version Gate")
    print("=" * 60)
    print(f"Tags checked: {len(tags)}")
    print(f"Violations:   {len(violations)}")

    if violations:
        print("\n" + "!" * 60)
        print("BLOCKED: a tag and the commit it points at disagree\n")
        for name, rule, detail in violations:
            print(f"  tag {name}")
            print(f"    Rule:   {rule}")
            print(f"    Detail: {detail}")
            print(f"    Fix:    {FIX[rule]}")
            print()
        return 1

    current = parse_constant(VERSION_FILE.read_text(encoding="utf-8"))
    code, described = git("describe", "--tags", "--always")
    ahead = code == 0 and described != current
    print(f"\nPASSED: every tag matches the commit it points at (current: {current})")
    if ahead:
        print(f"  note: main is ahead of the last release ({described}).")
        print("        Projects created now are stamped "
              f"{current} but carry newer content. Tag first if that matters.")
    return 0


def release(version: str) -> int:
    if not is_valid_version(version):
        print(f"template_version: {version!r} is not vMAJOR.MINOR.PATCH", file=sys.stderr)
        return 2
    text = VERSION_FILE.read_text(encoding="utf-8")
    current = parse_constant(text)
    if current == version:
        print(f"template_version: already at {version}; nothing to rewrite.")
    else:
        VERSION_FILE.write_text(set_constant(text, version), encoding="utf-8")
        print(f"template_version: {current} -> {version} in {VERSION_FILE.relative_to(ROOT)}")
    print("\nNow, in this order — tagging before committing tags a stale constant:")
    print("    git add -A && git commit -m \"release: " + version + "\"")
    print("    git tag -a " + version + " -m \"<MAJOR|MINOR|PATCH>: <what changed>\"")
    print("\nWhich bump: docs/orchestration/knowledge/reference_template_versioning.md")
    return 0


# ==============================================================================
# SELF-TEST — in-memory fixtures, run on every commit
# ==============================================================================

def run_self_test() -> int:
    print("\nTemplate Version Gate Self-Test")
    print("=" * 60)
    failures = 0

    def check_case(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        if ok:
            print(f"  ok    {label}")
        else:
            print(f"  FAIL  {label}")
            if detail:
                print(f"        {detail}")
            failures += 1

    good = ["v1.0.0", "v0.1.0", "v12.3.45"]
    bad = ["v1.0", "1.0.0", "release-2", "v1.0.0-rc1", "v1.0.0.0", ""]
    check_case("semver tag names accepted", all(is_valid_version(v) for v in good))
    check_case("non-semver tag names rejected",
               not any(is_valid_version(v) for v in bad),
               f"accepted {[v for v in bad if is_valid_version(v)]}")

    src = 'x = 1\nTEMPLATE_VERSION = "v1.0.0"\ny = 2\n'
    check_case("the constant is read out of source", parse_constant(src) == "v1.0.0")
    check_case("source with no constant reads as None", parse_constant("x = 1\n") is None)

    rewritten = set_constant(src, "v1.1.0")
    check_case("the constant is rewritten in place",
               parse_constant(rewritten) == "v1.1.0" and rewritten.count("TEMPLATE_VERSION") == 1,
               rewritten)

    check_case("a bump type is detected in an annotation",
               names_bump_type("MINOR: added the initializer")
               and names_bump_type("PATCH: fix the scissors bug")
               and not names_bump_type("First tagged template release."))

    check_case("versions sort numerically, not as strings",
               min(["v1.0.0", "v0.9.0", "v10.0.0"], key=sort_key) == "v0.9.0"
               and max(["v1.0.0", "v0.9.0", "v10.0.0"], key=sort_key) == "v10.0.0")

    # The earliest tag is exempt from the bump-type rule because a bump is defined
    # relative to a predecessor. This is semantics, not a carve-out.
    tags = ["v1.1.0", "v1.0.0", "v2.0.0"]
    check_case("the earliest tag is the one exempt from naming a bump",
               min(tags, key=sort_key) == "v1.0.0")

    rows = parse_tag_rows("v1.0.0|tag|First release.\nv1.1.0|commit|release: v1.1.0\n\n")
    check_case("tag rows carry name, object type and subject",
               rows == [("v1.0.0", "tag", "First release."),
                        ("v1.1.0", "commit", "release: v1.1.0")], str(rows))

    # What actions/checkout produces on a tag push: the tag object is gone, the
    # ref points at the commit, and `%(contents:subject)` is the commit subject.
    rules = [r for r, _ in judge("v1.1.0", "commit", "release: v1.1.0", "v1.0.0", "v1.1.0")]
    check_case("a lightweight tag is named as such, not as a missing bump type",
               rules == ["lightweight-tag"], str(rules))
    rules = [r for r, _ in judge("v1.1.0", "tag", "release: v1.1.0", "v1.0.0", "v1.1.0")]
    check_case("an annotated tag without a bump type is still no-bump-type",
               rules == ["no-bump-type"], str(rules))
    check_case("an annotated tag naming its bump on the right commit is clean",
               judge("v1.1.0", "tag", "MINOR: x", "v1.0.0", "v1.1.0") == [])
    rules = [r for r, _ in judge("v1.1.0", "tag", "MINOR: x", "v1.0.0", "v1.0.0")]
    check_case("a tag on a commit stamped with another version is constant-mismatch",
               rules == ["constant-mismatch"], str(rules))
    # A bump is named relative to a predecessor; the earliest tag has none, so it
    # needs neither a bump type nor the annotation object that would carry one.
    check_case("the earliest tag needs neither a bump type nor an annotation",
               judge("v1.0.0", "tag", "First.", "v1.0.0", "v1.0.0") == []
               and judge("v1.0.0", "commit", "First.", "v1.0.0", "v1.0.0") == [])
    check_case("a tag older than the version file is compared against nothing",
               judge("v0.1.0", "tag", "MINOR: x", "v0.1.0", None) == [])

    total = 15
    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the template version against its tags")
    parser.add_argument("--check", action="store_true", help="Verify tags (default)")
    parser.add_argument("--release", metavar="vX.Y.Z", help="Set the constant for a release")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.release:
        return release(args.release)
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
