#!/usr/bin/env python3
"""
birth_probe.py — a project born from any commit of the template starts green.

THE FAILURE THIS CLOSES
-----------------------
From the S7 closeout push until the S8 closeout push, every project born from the template was
refused by its own first suite run while the template's CI stayed green. CI judges the template,
and several gates judge a project differently: the profile's stripped documents, the tracker the
initializer regenerates, the project's decisions beside the framework's, the roster. GitHub's "Use
this template" copies the default branch as it stands, not a release tag, so `main` must make a
healthy project at every push. The regression was found only because a proof happened to need a
birth. Decision 2026-10-23-017.

WHAT IT DOES
------------
Makes a scratch project from a committed revision of this repository, the way a project is made:

  1. the revision's tree, written out by `git archive`, so neither the working tree nor an
     uncommitted change reaches it;
  2. a fresh repository holding that tree as one "Initial commit", which is what GitHub's template
     flow gives a new project;
  3. that revision's own `scripts/new_project.py --apply`, with a profile.

The verdict is the initializer's: it ends by running the suite and refuses a birth that is not
green. With no `--profile`, each profile is born in turn. Git and the initializer run with every
`GIT_*` variable and `CLAUDE_PROJECT_DIR` removed: inside a commit hook git exports the index it is
committing, and a scratch `git add` would write to it, and a gate reading `CLAUDE_PROJECT_DIR`
would judge this repository instead of the birth. The scratch directory is removed when the run
ends.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It judges a birth, not an adoption: a project taken to a newer release through
`template_update.py` is heavier and is proved by hand at the release (TMPL-2.4). It refuses a
revision whose tree holds `.project-profile`, since a project is not a template; CI skips the step
there.

Usage:  python3 scripts/birth_probe.py [--rev <revision>] [--profile commercial|gcc]
        pre-commit run birth-probe-selftest --all-files
        python3 scripts/birth_probe.py --self-test
Exit 0 = every birth green, 1 = a birth refused, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import project_profile  # noqa: E402 — the profiles, their one home

INITIALIZER = "scripts/new_project.py"
PROFILE_FILE = ".project-profile"
# The initializer's tokens, every one filled; what they say does not matter to the verdict.
PROJECT_ARGS = ["--name", "Birth Probe", "--platform", "a scratch birth", "--scope", "prove the template births green",
                "--prefix", "PROBE"]
# A scratch commit needs an identity and no signing whatever the machine sets, and no hook a
# global hooks path would run.
IDENTITY = ["-c", "user.name=birth-probe", "-c", "user.email=birth-probe@example.invalid", "-c", "commit.gpgsign=false"]
DROP_ENV = ("CLAUDE_PROJECT_DIR",)

Runner = Callable[[list[str], Path, dict], int]


class CannotRun(Exception):
    """No scratch project could be made, so no birth was judged."""


def repo_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False)
    if out.returncode != 0 or not out.stdout.strip():
        raise CannotRun("not inside a git repository")
    return Path(out.stdout.strip())


def birth_env() -> dict:
    """The environment with nothing in it that names another repository."""
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k not in DROP_ENV}


def git(where: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=where, env=birth_env(), capture_output=True, check=False)


def resolve(source: Path, rev: str) -> tuple[str, str]:
    """(full hash, `<short> <subject>`) of the commit the revision names."""
    out = git(source, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if out.returncode != 0:
        raise CannotRun(f"`{rev}` names no commit in {source}")
    full = out.stdout.decode().strip()
    title = git(source, "log", "-1", "--format=%h %s", full).stdout.decode().strip()
    return full, title


def export(source: Path, commit: str, dest: Path) -> None:
    """The commit's tree, as committed, written into dest."""
    out = git(source, "archive", "--format=tar", commit)
    if out.returncode != 0:
        raise CannotRun(f"`git archive {commit[:7]}` failed: {out.stderr.decode().strip()}")
    with tarfile.open(fileobj=io.BytesIO(out.stdout), mode="r:") as tar:
        tar.extractall(dest, filter="data")


def initial_commit(tree: Path) -> None:
    """A fresh repository holding the tree as its one commit."""
    for args in (["init", "-q", "-b", "main"], ["add", "-A"],
                 [*IDENTITY, "commit", "-q", "--no-verify", "-m", "Initial commit"]):
        out = git(tree, *args)
        if out.returncode != 0:
            raise CannotRun(f"`git {' '.join(args)}` failed in the scratch repository: {out.stderr.decode().strip()}")


def run_initializer(cmd: list[str], tree: Path, env: dict) -> int:
    return subprocess.run(cmd, cwd=tree, env=env, check=False).returncode


def probe(source: Path, rev: str, profiles: list[str], run: Runner = run_initializer) -> int:
    """Born once per profile from the revision; 0 when every birth is green, 1 otherwise."""
    commit, title = resolve(source, rev)
    refused = []
    for profile in profiles:
        with tempfile.TemporaryDirectory(prefix="birth-probe-") as tmp:
            tree = Path(tmp) / "project"
            tree.mkdir()
            export(source, commit, tree)
            if (tree / PROFILE_FILE).exists():
                raise CannotRun(f"{title} holds `{PROFILE_FILE}`: it is a project, and only the template gives birth")
            initial_commit(tree)
            print(f"\n=== Birth probe: {title}, profile `{profile}` ===", flush=True)
            # Unbuffered, so the initializer's own lines keep their place beside the suite's in a log.
            rc = run([sys.executable, INITIALIZER, *PROJECT_ARGS, "--profile", profile, "--apply"], tree,
                     {**birth_env(), "PYTHONUNBUFFERED": "1"})
        print(f"=== {'GREEN' if rc == 0 else f'REFUSED (initializer exit {rc})'}: profile `{profile}` ===", flush=True)
        if rc != 0:
            refused.append(profile)
    if refused:
        print(f"\nBirth probe: BLOCKED — a project born from {title} is refused under {', '.join(refused)}.\n"
              "    The initializer's suite output above names each failing gate. Fix the template so a\n"
              "    birth starts green; a gate that judges a project differently is proved on a birth.")
        return 1
    print(f"\nBirth probe: PASSED — a project born from {title} starts green under {', '.join(profiles)}.")
    return 0


# ==============================================================================
# SELF-TEST — a stub initializer in a scratch template, every rule against a passing and a failing case
# ==============================================================================

# Writes what it saw to $BIRTH_PROBE_FIXTURE_OUT and exits with the code its tree holds.
_STUB = '''import os, subprocess, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
count = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
seen = {"root": str(root), "commits": count, "argv": sys.argv[1:], "untracked": (root / "untracked.txt").exists(),
        "env": sorted(k for k in os.environ if k.startswith("GIT_") or k == "CLAUDE_PROJECT_DIR")}
with open(os.environ["BIRTH_PROBE_FIXTURE_OUT"], "a", encoding="utf-8") as f:
    f.write(repr(seen) + "\\n")
sys.exit(int((root / "verdict.txt").read_text()))
'''


def _commit(repo: Path, verdict: str, message: str) -> str:
    (repo / "verdict.txt").write_text(verdict, encoding="utf-8")
    for args in (["add", "-A"], [*IDENTITY, "commit", "-q", "--no-verify", "-m", message]):
        subprocess.run(["git", *args], cwd=repo, env=birth_env(), check=True, capture_output=True)
    return git(repo, "rev-parse", "HEAD").stdout.decode().strip()


def _seen(path: Path) -> list[dict]:
    import ast
    return [ast.literal_eval(line) for line in path.read_text(encoding="utf-8").splitlines()] if path.is_file() else []


def run_self_test() -> int:
    print("\nBirth Probe Self-Test")
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

    def quiet(*args: object) -> tuple[int | str, list[dict]]:
        out.unlink(missing_ok=True)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rc: int | str = probe(*args)  # type: ignore[arg-type]
        except CannotRun as e:
            rc = f"cannot run: {e}"
        except Exception as e:  # a crash is a failed fixture, never a crashed self-test
            rc = f"crash: {type(e).__name__}: {e}"
        return rc, _seen(out)

    saved = dict(os.environ)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp).resolve()
        out = tmp_path / "seen.txt"
        os.environ["BIRTH_PROBE_FIXTURE_OUT"] = str(out)
        src = tmp_path / "template"
        (src / "scripts").mkdir(parents=True)
        (src / INITIALIZER).write_text(_STUB, encoding="utf-8")
        subprocess.run(["git", "init", "-q", "-b", "main", str(src)], env=birth_env(), check=True)
        green = _commit(src, "0", "green")
        red = _commit(src, "1", "red")
        one = [project_profile.PROFILES[0]]

        try:
            rc, seen = quiet(src, green, one)
            check("a revision whose initializer passes is a green birth", rc == 0, str(rc))
            first = seen[0] if seen else {}
            check("the birth is a fresh repository holding the revision as its one commit",
                  first.get("commits") == "1", str(seen))
            check("the initializer runs with --apply and the profile asked for",
                  "--apply" in first.get("argv", []) and first.get("argv", [])[-3:-1] == ["--profile", one[0]], str(seen))

            rc, seen = quiet(src, red, one)
            check("a revision whose initializer refuses the birth fails the probe", rc == 1, str(rc))
            rc, _ = quiet(src, "HEAD", one)
            check("HEAD is the revision unless one is named", rc == 1, str(rc))

            (src / "verdict.txt").write_text("0", encoding="utf-8")
            (src / "untracked.txt").write_text("x", encoding="utf-8")
            rc, seen = quiet(src, "HEAD", one)
            check("the committed tree is born, never the working tree or an untracked file",
                  rc == 1 and seen and seen[0].get("untracked") is False, f"rc={rc} {seen}")
            (src / "untracked.txt").unlink()
            subprocess.run(["git", "checkout", "-q", "--", "verdict.txt"], cwd=src, env=birth_env(), check=True)

            index = (src / ".git" / "index").read_bytes()
            os.environ.update(GIT_INDEX_FILE=str(src / ".git" / "index"), CLAUDE_PROJECT_DIR=str(src))
            rc, seen = quiet(src, green, one)
            for k in ("GIT_INDEX_FILE", "CLAUDE_PROJECT_DIR"):
                os.environ.pop(k, None)
            check("inside a commit hook the source's index is untouched and the birth sees no variable naming it",
                  rc == 0 and (src / ".git" / "index").read_bytes() == index and seen and seen[0].get("env") == [],
                  f"rc={rc} {seen}")
            status = git(src, "status", "--porcelain").stdout.decode().strip()
            check("the source repository is left as it was", status == "", status)
            check("the scratch directory is removed when the run ends",
                  bool(seen) and not Path(seen[0]["root"]).exists(), str(seen))

            rc, seen = quiet(src, green, list(project_profile.PROFILES))
            check("with no profile named, each is born in turn",
                  rc == 0 and [s["argv"][-2] for s in seen] == list(project_profile.PROFILES), f"rc={rc} {seen}")
            check("the command line's default is every profile, and a named one alone",
                  profiles_of(parse([])) == list(project_profile.PROFILES)
                  and profiles_of(parse(["--profile", "gcc"])) == ["gcc"], str(profiles_of(parse([]))))

            (src / PROFILE_FILE).write_text("commercial\n", encoding="utf-8")
            project = _commit(src, "0", "a project")
            rc, seen = quiet(src, project, one)
            check("a revision holding `.project-profile` is refused, and nothing is born",
                  isinstance(rc, str) and rc.startswith("cannot run") and PROFILE_FILE in rc and not seen, f"rc={rc} {seen}")
            rc, _ = quiet(src, "no-such-revision", one)
            check("a revision that names no commit cannot run", isinstance(rc, str) and rc.startswith("cannot run"), str(rc))
        finally:
            os.environ.clear()
            os.environ.update(saved)

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def parse(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Birth a scratch project from a committed revision")
    parser.add_argument("--rev", default="HEAD", help="the revision to birth from (default: HEAD)")
    parser.add_argument("--profile", action="append", choices=project_profile.PROFILES,
                        help="the profile to birth under; repeatable (default: each in turn)")
    parser.add_argument("--self-test", action="store_true", help="run the fixtures and exit")
    return parser.parse_args(argv)


def profiles_of(args: argparse.Namespace) -> list[str]:
    return args.profile or list(project_profile.PROFILES)


def main(argv: list[str]) -> int:
    args = parse(argv)
    if args.self_test:
        return run_self_test()
    try:
        return probe(repo_root(), args.rev, profiles_of(args))
    except CannotRun as e:
        print(f"birth_probe: cannot run: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
