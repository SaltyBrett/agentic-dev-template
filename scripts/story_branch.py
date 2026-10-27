#!/usr/bin/env python3
"""
story_branch.py — the team's branch and merge workflow: each story on its own branch and worktree,
merged by a squashed pull request once CI is green, the shared records on the integration branch.

THE RULES
---------
Protected branches are `main` and `release/*`; the integration branch is `main`.
  - On a protected branch a commit changes only the shared records (RECORDS), and elsewhere only
    fills a version-log row's `pending` cell with its commit's hash: a stamp can name only a commit
    the branch holds, and a squash merge gives the story's work a new one, so `finish` stamps after
    the merge. A `release: vX.Y.Z` commit may also change the version constant's file; a
    repository's first commit, and a project's birth commit (the one that adds
    `.template-version`), anything.
  - On `story/<ID>` the story is In Progress, and no commit changes the records the integration
    branch alone writes (SHARED): the tracker, sprint-status, the handoffs and the issue log.
  - On `update/vX.Y.Z`, a template update, anything. No other branch is the team's.
  - A merge commit carries both sides, so the commit hook passes it and the push and provenance
    checks judge it against its first parent.

COMMANDS
--------
  start <ID>           On the integration branch, clean and current: the story set In Progress, the
                       statistics recounted, committed and pushed; `story/<ID>` made in its own
                       worktree, `.worktrees/<ID>`, which git ignores.
  finish <ID>          The integration branch merged into the story branch (never rebased, so nothing
                       is force-pushed), the suite run, the branch pushed, its pull request opened and
                       its CI watched; squash-merged once green; on the integration branch the story
                       set Done and its version-log rows stamped, committed and pushed; the
                       worktree and the branch removed.
  --policy <msgfile>   The commit-msg hook: the rules over the staged change.
  --push               The pre-push hook: each commit pushed to a protected branch is records, a
                       release, a birth or a repository's first commit. Story work reaches a
                       protected branch only as a merged pull request, which GitHub makes, so a push
                       from a clone never carries it. CI runs the same hook over the push's range
                       (`pre-commit run --hook-stage pre-push --from-ref ... --to-ref ...`), where a
                       merged pull request's commit does arrive, and asks GitHub, with the run's
                       token, which pull request each other commit came from.
  --self-test          In-memory fixtures for every rule.

Usage:
    python3 scripts/story_branch.py start <ID> | finish <ID>
    python3 scripts/story_branch.py --self-test
Exit 0 = clean, 1 = refused or a violation, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import session_closeout  # noqa: E402 — the tracker's stories, one parse with the state gate's
import issue_log        # noqa: E402 — the issue log's parse and its one writer, so the issues move with their story

PROTECTED = re.compile(r"^(main|release/[\w.-]+)$")
STORY_BRANCH = re.compile(r"^story/([A-Z][A-Z0-9]*-\d+\.\d+)$")
UPDATE_BRANCH = re.compile(r"^update/v\d+\.\d+\.\d+$")
RELEASE_SUBJECT = re.compile(r"^release: v\d+\.\d+\.\d+$")

# What a protected branch takes: the session's records, the decisions and learnings, the planning.
RECORDS = ("sprint/", "docs/orchestration/knowledge/", "docs/prd/", "docs/architecture/", ".claude/agents/")
# What the integration branch alone writes, so parallel story branches never collide on it.
SHARED = ("sprint/story-tracker.md", "sprint/sprint-status.md", "sprint/handoffs/", "sprint/archive/",
          "sprint/issue-log.md")
VERSION_FILE = "scripts/new_project.py"     # the constant `template_version.py --release` rewrites
BIRTH_MARK = ".template-version"
WORKTREES = ".worktrees"
TRACKER = "sprint/story-tracker.md"
SUITE = ["pre-commit", "run", "--all-files"]
STAMPER = "scripts/doc_authority_scan.py"
STATISTICS = {"Total Stories": None, "Not Started": "Not Started", "In Progress": "In Progress",
              "Blocked": "Blocked", "Completed": "Done"}


STAMPING = re.compile(r"^(.*)\| pending \|\s*$")
STAMPED = re.compile(r"^(.*)\| [0-9a-f]{7,40} \|\s*$")


class Change(NamedTuple):
    """What a rule reads of one commit, or of the change being committed."""
    subject: str
    paths: tuple[str, ...]
    added: tuple[str, ...]
    parents: int                       # 0 for a repository's first commit, 2 or more for a merge
    stamped: tuple[str, ...] = ()      # paths whose change only fills `pending` version-log cells


class Refused(Exception):
    """A command's precondition does not hold: nothing more is done."""


def under(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path == p or (p.endswith("/") and path.startswith(p)) for p in prefixes)


# ==============================================================================
# Rules — pure
# ==============================================================================

def protected_problems(change: Change) -> list[str]:
    """Why a change may not land on a protected branch; [] when it may."""
    if change.parents == 0 or BIRTH_MARK in change.added:
        return []
    allowed = RECORDS + ((VERSION_FILE,) if RELEASE_SUBJECT.match(change.subject) else ())
    outside = [p for p in change.paths if not under(p, allowed) and p not in change.stamped]
    if not outside:
        return []
    more = f" and {len(outside) - 4} more" if len(outside) > 4 else ""
    return [f"{change.subject!r} changes {', '.join(outside[:4])}{more} on a protected branch, which takes only the "
            "shared records: build it on story/<ID>, `python3 scripts/story_branch.py start <ID>`"]


def stamp_only(diff: str) -> bool:
    """True when a file's `-U0` diff only fills `pending` version-log cells with a hash, the rest of
    each row unchanged."""
    removed = [ln[1:] for ln in diff.splitlines() if ln.startswith("-") and not ln.startswith("---")]
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    if not removed or len(removed) != len(added):
        return False
    for old, new in zip(removed, added):
        before, after = STAMPING.match(old), STAMPED.match(new)
        if not before or not after or before.group(1) != after.group(1):
            return False
    return True


def branch_problems(branch: str | None, change: Change, stories: dict[str, str], merging: bool) -> list[str]:
    """The commit hook's rule for the branch being committed to; [] when the commit may be made."""
    if merging or branch is None:
        return []
    if PROTECTED.match(branch):
        return protected_problems(change)
    if UPDATE_BRANCH.match(branch):
        return []
    m = STORY_BRANCH.match(branch)
    if not m:
        return [f"`{branch}` is no branch of the team's: story/<ID>, update/vX.Y.Z, or main and release/* "
                "for the records"]
    sid = m.group(1)
    problems = []
    if stories.get(sid) != "In Progress":
        problems.append(f"{sid} is {stories.get(sid, 'no story in the tracker')}, not In Progress: "
                        f"`python3 scripts/story_branch.py start {sid}` starts it")
    shared = [p for p in change.paths if under(p, SHARED)]
    if shared:
        problems.append(f"changes {', '.join(shared)}, which the integration branch alone writes")
    return problems


def provenance_problems(commits: list[tuple[str, Change]], merged_pr: Callable[[str], bool]) -> list[str]:
    """Each commit on a protected branch is records, a release, a birth, a repository's first
    commit, or a merged pull request's own commit."""
    out = []
    for sha, change in commits:
        if protected_problems(change) and not merged_pr(sha):
            out.append(f"{sha[:10]} {change.subject!r} reached a protected branch with no merged pull request, "
                       "and is not records, a release or a birth")
    return out


def set_status(tracker: str, sid: str, status: str) -> str:
    """The tracker with the story's Status cell set and the Summary Statistics recounted."""
    lines = tracker.splitlines(keepends=True)
    hits = [i for i, ln in enumerate(lines) if ln.startswith("|") and ln.strip().strip("|").split("|")[0].strip() == sid]
    if len(hits) != 1:
        raise Refused(f"the tracker holds {len(hits)} rows for {sid}")
    cells = lines[hits[0]].rstrip("\n").split("|")
    cells[3] = f" {status} "
    lines[hits[0]] = "|".join(cells) + "\n"
    text = "".join(lines)
    counts: dict[str, int] = {}
    for story in session_closeout.tracker_stories(text):
        counts[story.status] = counts.get(story.status, 0) + 1
    for label, key in STATISTICS.items():
        value = sum(counts.values()) if key is None else counts.get(key, 0)
        text = re.sub(rf"^(\| \*\*{label}\*\* \| )\d+( \|)$", rf"\g<1>{value}\g<2>", text, count=1, flags=re.M)
    return text


def start_problems(branch: str | None, dirty: bool, status: str | None, deps: dict[str, str], branch_exists: bool,
                   sid: str) -> list[str]:
    problems = []
    if not branch or not PROTECTED.match(branch):
        problems.append(f"start runs on the integration branch, main or release/*; this is {branch or 'a detached HEAD'}")
    if dirty:
        problems.append("the working tree holds uncommitted changes")
    if status is None:
        problems.append(f"{sid} is no story in the tracker")
    elif status not in ("Not Started", "Blocked"):
        problems.append(f"{sid} is {status}; start takes a story Not Started or Blocked")
    waiting = [d for d, s in deps.items() if s != "Done"]
    if waiting:
        problems.append(f"{sid} waits on {', '.join(waiting)}, not Done")
    if branch_exists:
        problems.append(f"story/{sid} exists already")
    return problems


def issues_to_start(log_text: str, sid: str) -> list[str]:
    """The issues a story's start moves to In Progress: each Triaged one that names it. The issue gate refuses Triaged once a named story is In Progress, so they move
    in the commit that starts it."""
    return [i.id for i in issue_log.parse(log_text).issues if not i.example and i.fields.get("Status") == "Triaged"
            and sid in issue_log.items(i.fields.get("Stories", issue_log.NONE))]


def issues_to_resolve(log_text: str, sid: str, statuses: dict[str, str]) -> list[str]:
    """The issues a story's Done resolves: each In Progress one that names it, every other story it
    names Done already. One with a story still open stays In Progress."""
    out = []
    for i in issue_log.parse(log_text).issues:
        named = issue_log.items(i.fields.get("Stories", issue_log.NONE))
        if not i.example and i.fields.get("Status") == "In Progress" and sid in named \
                and all(statuses.get(s) == "Done" for s in named if s != sid):
            out.append(i.id)
    return out


def moved_issues(log_text: str, ids: list[str], changes: dict[str, str]) -> str:
    """The log with each named issue changed through the issue log's own writer."""
    for issue_id in ids:
        log_text = issue_log.update_issue(log_text, issue_id, changes)
    return log_text


def finish_problems(ahead: int, base: str, resolving: list[str], resolution: str | None, sid: str) -> list[str]:
    """Why finish may not begin; [] when it may. Checked before anything merges, so a refusal leaves
    nothing half done."""
    problems = []
    if ahead:
        problems.append(f"{base} holds {ahead} commit(s) its origin lacks: `git push origin {base}` first, so the "
                        "pull request is built on them and the last pull can fast-forward")
    if resolving and not resolution:
        problems.append(f"{sid}'s Done resolves {', '.join(resolving)}: say what changed, "
                        f"`python3 scripts/story_branch.py finish {sid} --resolution \"<what changed>\"`")
    return problems


def title_of(row: str, sid: str) -> str:
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    title = cells[1] if len(cells) > 1 else ""
    short = title if len(title) <= 60 else title[:57].rsplit(" ", 1)[0] + "..."
    return f"story: {sid} {short}".rstrip()


# ==============================================================================
# Git
# ==============================================================================

def git(where: Path, *args: str, check: bool = True) -> str:
    out = subprocess.run(["git", *args], cwd=where, capture_output=True, text=True, check=False)
    if check and out.returncode != 0:
        raise Refused(f"git {' '.join(args)}: {out.stderr.strip() or out.stdout.strip()}")
    return out.stdout


def root_of(where: Path) -> Path:
    return Path(git(where, "rev-parse", "--show-toplevel").strip())


def current_branch(where: Path) -> str | None:
    name = git(where, "branch", "--show-current").strip()
    return name or None


def stories_of(root: Path) -> dict[str, session_closeout.Story]:
    path = root / TRACKER
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    return {s.id: s for s in session_closeout.tracker_stories(text)}


def name_status(lines: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """(every path, the paths added) from `--name-status` output; a rename counts both its paths."""
    paths, added = [], []
    for line in lines.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        paths += parts[1:]
        if parts[0].startswith("A"):
            added.append(parts[1])
    return tuple(paths), tuple(added)


def stamps_in(root: Path, paths: tuple[str, ...], *diff_args: str) -> tuple[str, ...]:
    """The paths outside the records whose diff only stamps version-log rows."""
    return tuple(p for p in paths if not under(p, RECORDS) and stamp_only(git(root, "diff", "-U0", *diff_args, "--", p)))


def staged_change(root: Path, subject: str) -> Change:
    paths, added = name_status(git(root, "diff", "--cached", "--name-status", "--no-renames"))
    born = git(root, "rev-parse", "--verify", "--quiet", "HEAD", check=False).strip()
    return Change(subject, paths, added, 1 if born else 0, stamps_in(root, paths, "--cached"))


def commit_change(root: Path, sha: str) -> Change:
    parents = git(root, "log", "-1", "--format=%P", sha).split()
    subject = git(root, "log", "-1", "--format=%s", sha).strip()
    if parents:
        out = git(root, "diff", "--name-status", "--no-renames", f"{parents[0]}", sha)
    else:
        out = git(root, "diff-tree", "--root", "--no-commit-id", "-r", "--name-status", "--no-renames", sha)
    paths, added = name_status(out)
    stamped = stamps_in(root, paths, parents[0], sha) if parents else ()
    return Change(subject, paths, added, len(parents), stamped)


def is_merging(root: Path) -> bool:
    return Path(root, git(root, "rev-parse", "--git-path", "MERGE_HEAD").strip()).is_file()


def worktree_of(root: Path, branch: str) -> Path | None:
    """The working directory that has the branch checked out, or None."""
    path = None
    for line in git(root, "worktree", "list", "--porcelain").splitlines():
        if line.startswith("worktree "):
            path = Path(line[len("worktree "):])
        elif line == f"branch refs/heads/{branch}":
            return path
    return None


def run(cmd: list[str], where: Path) -> int:
    return subprocess.run(cmd, cwd=where, check=False).returncode


def say(text: str) -> None:
    print(f"story_branch: {text}", flush=True)


# ==============================================================================
# The hooks and the CI check
# ==============================================================================

def cmd_policy(msgfile: str) -> int:
    root = root_of(Path.cwd())
    subject = (Path(msgfile).read_text(encoding="utf-8").splitlines() or [""])[0].strip()
    stories = {sid: s.status for sid, s in stories_of(root).items()}
    problems = branch_problems(current_branch(root), staged_change(root, subject), stories, is_merging(root))
    return report("Branch Policy", problems)


def is_commit(root: Path, ref: str) -> bool:
    return bool(ref) and set(ref) != {"0"} and git(root, "cat-file", "-t", ref, check=False).strip() == "commit"


def pushed_commits(root: Path, local: str, remote_ref: str, remote: str, in_ci: bool) -> list[str]:
    """The commits a push carries: past the remote ref when it is a commit; else, in CI, all of the
    branch's (a new repository, a new branch, a force-push), and in a clone those no remote branch holds."""
    if not is_commit(root, local):
        return []
    if is_commit(root, remote_ref):
        return git(root, "rev-list", f"{remote_ref}..{local}").split()
    if in_ci:
        return git(root, "rev-list", local).split()
    return git(root, "rev-list", local, "--not", f"--remotes={remote}").split()


def cmd_push() -> int:
    root = root_of(Path.cwd())
    branch = os.environ.get("PRE_COMMIT_REMOTE_BRANCH", "").removeprefix("refs/heads/")
    if not PROTECTED.match(branch):
        return report("Branch Push", [])
    repo = os.environ.get("GITHUB_REPOSITORY", "") if os.environ.get("GITHUB_ACTIONS") == "true" else ""
    shas = pushed_commits(root, os.environ.get("PRE_COMMIT_TO_REF", ""), os.environ.get("PRE_COMMIT_FROM_REF", ""),
                          os.environ.get("PRE_COMMIT_REMOTE_NAME", "origin"), bool(repo))
    lookup = merged_pr_lookup(repo) if repo else (lambda sha: False)
    problems = provenance_problems([(sha, commit_change(root, sha)) for sha in shas], lookup)
    if problems:
        problems.append(f"story work reaches {branch} as a merged pull request: "
                        "`python3 scripts/story_branch.py finish <ID>`")
    return report("Branch Push", problems)


def merged_pr_lookup(repo: str) -> Callable[[str], bool]:
    def merged(sha: str) -> bool:
        out = subprocess.run(["gh", "api", f"repos/{repo}/commits/{sha}/pulls",
                              "--jq", "[.[] | select(.merged_at != null)] | length"],
                             capture_output=True, text=True, check=False)
        if out.returncode != 0:
            raise Refused(f"the pull requests of {sha[:10]} could not be read: {out.stderr.strip()[-200:]}")
        return int(out.stdout.strip() or 0) > 0
    return merged


def report(title: str, problems: list[str]) -> int:
    print(f"\n{title}\n{'=' * 60}")
    if not problems:
        print("PASSED")
        return 0
    print(f"BLOCKED: {len(problems)} violation(s)\n")
    for p in problems:
        print(f"  {p}")
    print("\n  The workflow: docs/standards/team_standard_v1.0.md.")
    return 1


# ==============================================================================
# start and finish
# ==============================================================================

def cmd_start(sid: str) -> int:
    root = root_of(Path.cwd())
    branch = current_branch(root)
    if branch and PROTECTED.match(branch):
        git(root, "fetch", "-q", "origin")
        git(root, "merge", "-q", "--ff-only", f"origin/{branch}")
    stories = stories_of(root)
    story = stories.get(sid)
    deps = {d: stories[d].status if d in stories else "no story" for d in (story.deps if story else ())}
    exists = bool(git(root, "branch", "--list", f"story/{sid}").strip())
    problems = start_problems(branch, bool(git(root, "status", "--porcelain").strip()), story and story.status, deps,
                              exists, sid)
    if problems:
        return report("Story Start", problems)
    (root / TRACKER).write_text(set_status((root / TRACKER).read_text(encoding="utf-8"), sid, "In Progress"), encoding="utf-8")
    git(root, "add", TRACKER, *start_issues(root, sid))
    if run(["git", "commit", "-q", "-m", f"checkpoint: {sid} started"], root) != 0:
        raise Refused(f"the commit that starts {sid} was refused; the tracker is staged for you to read")
    git(root, "push", "-q", "origin", branch)
    path = root / WORKTREES / sid
    git(root, "worktree", "add", "-q", "-b", f"story/{sid}", str(path))
    git(root, "config", f"branch.story/{sid}.integration", branch)
    say(f"{sid} In Progress on {branch}, pushed; story/{sid} is in {path}.\n"
        f"  Work and commit there; then `python3 scripts/story_branch.py finish {sid}`.")
    return 0


def start_issues(root: Path, sid: str) -> list[str]:
    """The Triaged issues naming the story moved to In Progress; the log's path to stage, or none."""
    path = root / issue_log.LOG
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    ids = issues_to_start(text, sid) if text else []
    if not ids:
        return []
    path.write_text(moved_issues(text, ids, {"status": "In Progress"}), encoding="utf-8")
    say(f"{', '.join(ids)} In Progress with {sid}")
    return [issue_log.LOG]


def committed(root: Path, ref: str, rel: str) -> str:
    """A file as the ref holds it; empty where it holds none."""
    return git(root, "show", f"{ref}:{rel}", check=False)


def finish_preconditions(root: Path, base: str, sid: str, resolution: str | None) -> tuple[list[str], list[str]]:
    """(the issues the Done resolves, why finish may not begin), read from the integration branch as
    committed, before anything merges."""
    ahead = int(git(root, "rev-list", "--count", f"origin/{base}..{base}").strip() or 0)
    statuses = {s.id: s.status for s in session_closeout.tracker_stories(committed(root, base, TRACKER))}
    resolving = issues_to_resolve(committed(root, base, issue_log.LOG), sid, statuses)
    return resolving, finish_problems(ahead, base, resolving, resolution, sid)


def resolve_issues(home: Path, wt: Path, sid: str, ids: list[str], resolution: str | None) -> None:
    """Each issue the Done resolves set Resolved, the pull request's merge commit its resolving commit."""
    if not ids:
        return
    oid = subprocess.run(["gh", "pr", "view", f"story/{sid}", "--json", "mergeCommit", "--jq", ".mergeCommit.oid"],
                         cwd=wt, capture_output=True, text=True, check=False).stdout.strip()
    if not oid:
        raise Refused(f"the merge commit of story/{sid} could not be read; the tracker is set Done in {home}")
    path = home / issue_log.LOG
    changes = {"status": "Resolved", "resolved_by": oid[:7], "resolution": resolution or ""}
    path.write_text(moved_issues(path.read_text(encoding="utf-8"), ids, changes), encoding="utf-8")
    say(f"{', '.join(ids)} Resolved by {oid[:7]}")


def open_pr(wt: Path, sid: str, base: str, title: str) -> None:
    found = subprocess.run(["gh", "pr", "view", f"story/{sid}", "--json", "state", "--jq", ".state"], cwd=wt,
                           capture_output=True, text=True, check=False)
    if found.returncode == 0 and found.stdout.strip() == "OPEN":
        return
    body = f"{title}\n\nOpened by `scripts/story_branch.py finish {sid}`; squash-merged once CI is green."
    if run(["gh", "pr", "create", "--base", base, "--head", f"story/{sid}", "--title", title, "--body", body], wt) != 0:
        raise Refused(f"the pull request for story/{sid} could not be opened")


def wait_for_checks(wt: Path, sid: str, tries: int = 60, pause: float = 5.0) -> None:
    """A pull request just opened reports no checks until GitHub queues its runs, and watching it then
    ends at once: wait until it reports some."""
    for _ in range(tries):
        out = subprocess.run(["gh", "pr", "checks", f"story/{sid}"], cwd=wt, capture_output=True, text=True, check=False)
        if "no checks reported" not in (out.stdout + out.stderr):
            return
        time.sleep(pause)
    raise Refused(f"the pull request for story/{sid} reported no checks in {int(tries * pause)} seconds")


def cmd_finish(sid: str, resolution: str | None = None) -> int:
    root = root_of(Path.cwd())
    wt = worktree_of(root, f"story/{sid}")
    if wt is None:
        return report("Story Finish", [f"story/{sid} is checked out nowhere"])
    base = git(root, "config", "--get", f"branch.story/{sid}.integration", check=False).strip() or "main"
    if git(wt, "status", "--porcelain").strip():
        return report("Story Finish", [f"{wt} holds uncommitted changes"])
    story = stories_of(wt).get(sid)
    title = title_of(story.row if story else "", sid)
    git(wt, "fetch", "-q", "origin")
    resolving, problems = finish_preconditions(root, base, sid, resolution)
    if problems:
        return report("Story Finish", problems)
    if run(["git", "merge", "-q", "--no-edit", f"origin/{base}"], wt) != 0:
        return report("Story Finish", [f"merging origin/{base} into story/{sid} conflicts: resolve it in {wt}, "
                                       "commit, and run finish again"])
    if run(SUITE, wt) != 0:
        return report("Story Finish", ["the suite fails on the story branch"])
    git(wt, "push", "-q", "-u", "origin", f"story/{sid}")
    open_pr(wt, sid, base, title)
    wait_for_checks(wt, sid)
    if run(["gh", "pr", "checks", f"story/{sid}", "--watch", "--fail-fast"], wt) != 0:
        return report("Story Finish", [f"the pull request's checks did not pass; story/{sid} is unmerged"])
    if run(["gh", "pr", "merge", f"story/{sid}", "--squash", "--subject", title, "--body", ""], wt) != 0:
        return report("Story Finish", [f"the pull request for story/{sid} could not be merged"])
    home = worktree_of(root, base)
    if home is None:                       # the integration branch is checked out nowhere: take the story's tree
        git(wt, "switch", "-q", base)
        home = wt
    git(home, "pull", "-q", "--ff-only", "origin", base)
    (home / TRACKER).write_text(set_status((home / TRACKER).read_text(encoding="utf-8"), sid, "Done"), encoding="utf-8")
    resolve_issues(home, wt, sid, resolving, resolution)
    if (home / STAMPER).is_file():         # the rows the story's work introduced, named by the merge's commit
        run([sys.executable, STAMPER, "--stamp"], home)
    git(home, "add", "-u")
    subject = f"checkpoint: {sid} done" + (f"; {', '.join(resolving)} Resolved" if resolving else "")
    if run(["git", "commit", "-q", "-m", subject], home) != 0:
        raise Refused(f"the commit that marks {sid} Done was refused; the tracker is staged in {home}")
    git(home, "push", "-q", "origin", base)
    if home != wt:
        git(root, "worktree", "remove", str(wt))
    git(home, "branch", "-q", "-D", f"story/{sid}")
    git(home, "push", "-q", "origin", "--delete", f"story/{sid}", check=False)
    say(f"{sid} merged into {base} and Done; its branch and worktree removed.")
    return 0


# ==============================================================================
# SELF-TEST — in-memory fixtures, run on every commit
# ==============================================================================

def _change(*paths: str, subject: str = "checkpoint: work", added: tuple[str, ...] = (), parents: int = 1,
            stamped: tuple[str, ...] = ()) -> Change:
    return Change(subject, tuple(paths), added, parents, stamped)


_TRACKER = """# Story Tracker

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Stories** | 3 |
| **Not Started** | 2 |
| **In Progress** | 0 |
| **Blocked** | 0 |
| **Completed** | 1 |

---

## Epic: ACME-1 - The export

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| ACME-1.1 | Read the source | Done | — | — | — |
| ACME-1.2 | Write a missing region as an empty field | Not Started | ACME-1.1 | — | — |
| ACME-1.3 | Export to CSV | Not Started | ACME-1.2 | — | — |
"""


KB = "docs/orchestration/" + "knowledge/"   # the knowledge base's folder, built so no entry's path is spelled


def _t_protected(check) -> None:
    check("records on a protected branch pass: the tracker, a handoff, a decision, a knowledge entry, the PRD, the roster",
          protected_problems(_change("sprint/story-tracker.md", "sprint/handoffs/HANDOFF_S3.md", "sprint/decision-log.md",
                                     KB + "x.md", "docs/prd/prd.md", ".claude/agents/qa.md")) == [])
    check("code on a protected branch is refused", len(protected_problems(_change("src/a.py"))) == 1)
    check("a path that only begins like a record folder is no record", len(protected_problems(_change("docs/prdx.md"))) == 1)
    check("a release commit may change the version constant's file",
          protected_problems(_change(VERSION_FILE, subject="release: v2.1.0")) == [])
    check("a release commit may change nothing else", len(protected_problems(_change("README.md", subject="release: v2.1.0"))) == 1)
    check("a checkpoint may not change the version constant's file", len(protected_problems(_change(VERSION_FILE))) == 1)
    check("a project's birth commit, the one adding .template-version, passes",
          protected_problems(_change("AGENTS.md", BIRTH_MARK, added=(BIRTH_MARK,))) == [])
    check("a commit that changes .template-version but does not add it is no birth",
          len(protected_problems(_change("AGENTS.md", BIRTH_MARK))) == 1)
    check("a repository's first commit passes", protected_problems(_change("README.md", parents=0)) == [])
    row = "| 1.6 | 2026-10-25 | 2026-01-02-003 | Section 1: the workflow (ACME-8.2) |"
    stamp = f"@@ -161 +161 @@\n-{row} pending |\n+{row} 1a2b3c4 |\n"
    check("a diff that only stamps version-log rows reads as a stamp", stamp_only(stamp) and stamp_only(stamp + stamp))
    for label, diff in (("that also changes the row's text", stamp.replace("+| 1.6 | 2026-10-25 | 2026-01-02-003 | Section 1",
                                                                         "+| 1.6 | 2026-10-25 | 2026-01-02-003 | Section 2")),
                        ("that adds a line", stamp + "+a new line\n"), ("that removes a stamp", f"-{row} 1a2b3c4 |\n+{row} pending |\n"),
                        ("that changes nothing", "")):
        check(f"a diff {label} is no stamp", not stamp_only(diff))
    check("a standard's stamp on a protected branch passes; the same path changed otherwise is refused",
          protected_problems(_change("docs/standards/x.md", stamped=("docs/standards/x.md",))) == []
          and len(protected_problems(_change("docs/standards/x.md"))) == 1)


def _t_branches(check) -> None:
    stories = {"ACME-1.2": "In Progress", "ACME-1.3": "Not Started"}
    code = _change("src/a.py", KB + "x.md", "sprint/decision-log.md", "docs/code_review_log.md")
    check("a story branch takes code, knowledge entries, decisions and the review log while its story is In Progress",
          branch_problems("story/ACME-1.2", code, stories, False) == [])
    for label, branch, change in (("a story not started", "story/ACME-1.3", code),
                                  ("a story the tracker lacks", "story/ACME-9.9", code),
                                  ("the tracker", "story/ACME-1.2", _change("sprint/story-tracker.md")),
                                  ("sprint-status", "story/ACME-1.2", _change("sprint/sprint-status.md")),
                                  ("a handoff", "story/ACME-1.2", _change("sprint/handoffs/KICKOFF_S4.md")),
                                  ("the issue log", "story/ACME-1.2", _change("sprint/issue-log.md")),
                                  ("a branch outside the team's names", "feature/x", code),
                                  ("code on main", "main", code),
                                  ("code on a release branch", "release/profiles", code)):
        check(f"a commit with {label} is refused", len(branch_problems(branch, change, stories, False)) >= 1,
              str(branch_problems(branch, change, stories, False)))
    check("an update branch takes a template update whole",
          branch_problems("update/v2.2.0", _change("scripts/x.py", "sprint/story-tracker.md"), {}, False) == [])
    check("a merge in progress and a detached HEAD are left to the push and provenance checks",
          branch_problems("main", code, {}, True) == [] and branch_problems(None, code, {}, False) == [])
    check("a story ID with a dot in its number is read whole", STORY_BRANCH.match("story/ACME-8.2").group(1) == "ACME-8.2")


def _t_provenance(check) -> None:
    commits = [("a" * 40, _change("src/a.py", subject="story: ACME-1.2 Write a missing region")),
               ("b" * 40, _change("sprint/story-tracker.md", subject="checkpoint: ACME-1.2 done")),
               ("c" * 40, _change("README.md", parents=0, subject="Initial commit")),
               ("d" * 40, _change("src/b.py", subject="a direct push"))]
    found = provenance_problems(commits, lambda sha: sha == "a" * 40)
    check("a merged pull request's commit, records and the first commit pass; a direct push of code is refused",
          len(found) == 1 and found[0].startswith("d" * 10), str(found))
    asked: list[str] = []
    provenance_problems(commits[1:3], lambda sha: asked.append(sha) or False)
    check("records and a first commit are judged without asking GitHub", asked == [], str(asked))


def _t_tracker(check) -> None:
    started = set_status(_TRACKER, "ACME-1.2", "In Progress")
    rows = {s.id: s.status for s in session_closeout.tracker_stories(started)}
    computed, declared, _ = session_closeout.tracker_counts(started)
    check("start sets the story's Status cell and nothing else's", rows == {"ACME-1.1": "Done", "ACME-1.2": "In Progress",
                                                                             "ACME-1.3": "Not Started"}, str(rows))
    check("the statistics are recounted with it, as the state gate counts them",
          not session_closeout.tracker_violations(computed, declared) and "| **In Progress** | 1 |" in started, str(declared))
    done = set_status(started, "ACME-1.2", "Done")
    check("finish sets it Done, the statistics with it", "| **Completed** | 2 |" in done and "| **In Progress** | 0 |" in done)
    try:
        set_status(_TRACKER, "ACME-9.9", "Done")
        check("a story the tracker lacks is refused", False)
    except Refused:
        check("a story the tracker lacks is refused", True)


def _t_start(check) -> None:
    check("a Not Started story whose dependencies are Done starts from main",
          start_problems("main", False, "Not Started", {"ACME-1.1": "Done"}, False, "ACME-1.2") == [])
    for label, args in (("from a story branch", ("story/ACME-1.1", False, "Not Started", {}, False)),
                        ("from a detached HEAD", (None, False, "Not Started", {}, False)),
                        ("with uncommitted changes", ("main", True, "Not Started", {}, False)),
                        ("a story the tracker lacks", ("main", False, None, {}, False)),
                        ("a story already In Progress", ("main", False, "In Progress", {}, False)),
                        ("a story whose dependency is not Done", ("main", False, "Not Started", {"ACME-1.2": "In Progress"}, False)),
                        ("a story whose branch exists", ("main", False, "Not Started", {}, True))):
        check(f"start {label} is refused", len(start_problems(*args, "ACME-1.3")) == 1, str(start_problems(*args, "ACME-1.3")))
    check("the pull request's title is the story's, cut at a word near 60 characters",
          title_of("| ACME-1.2 | " + "word " * 20 + "| Not Started |", "ACME-1.2").endswith("...")
          and len(title_of("| ACME-1.2 | " + "word " * 20 + "| x |", "ACME-1.2")) <= 75
          and title_of("| ACME-1.2 | Export | Done |", "ACME-1.2") == "story: ACME-1.2 Export")


def _issue_log(*issues: tuple[str, str, str]) -> str:
    """A log of (ID, status, stories) issues, each filed and moved through the issue log's writer."""
    text = issue_log.skeleton("ACME")
    for n, (issue_id, status, stories) in enumerate(issues, 1):
        text = issue_log.file_issue(text, {"title": f"Issue {n}", "by": "Chair", "as": "human", "kind": "request",
                                           "severity": "low", "what": "w", "expected": "e", "impact": "i",
                                           "date": "2026-10-25"}, issue_id)
        if status != "Open":
            text = issue_log.update_issue(text, issue_id, {"status": status, "stories": stories})
    return text


def _t_issues(check) -> None:
    judge = lambda text, stories: issue_log.judge(issue_log.parse(text), stories, None, None)  # noqa: E731
    log = _issue_log(("ACME-ISS-1", "Triaged", "ACME-1.2"), ("ACME-ISS-2", "Triaged", "ACME-1.3"),
                     ("ACME-ISS-3", "Open", ""), ("ACME-ISS-4", "In Progress", "ACME-1.1, ACME-1.2"))
    started = {"ACME-1.1": "Done", "ACME-1.2": "In Progress", "ACME-1.3": "Not Started"}
    check("start moves the Triaged issues naming the story, and no other",
          issues_to_start(log, "ACME-1.2") == ["ACME-ISS-1"], str(issues_to_start(log, "ACME-1.2")))
    moved = moved_issues(log, ["ACME-ISS-1"], {"status": "In Progress"})
    check("the log start writes passes the issue gate, where the unmoved log is refused",
          judge(moved, started) == [] and judge(log, started) != [], str(judge(moved, started)))
    open_ = _issue_log(("ACME-ISS-1", "In Progress", "ACME-1.2"), ("ACME-ISS-2", "In Progress", "ACME-1.2, ACME-1.3"))
    check("finish resolves the issues its Done completes, and leaves one with a story still open",
          issues_to_resolve(open_, "ACME-1.2", started) == ["ACME-ISS-1"], str(issues_to_resolve(open_, "ACME-1.2", started)))
    check("finish resolves only an issue In Progress",
          issues_to_resolve(_issue_log(("ACME-ISS-1", "Triaged", "ACME-1.2")), "ACME-1.2", started) == [])
    done = {**started, "ACME-1.2": "Done"}
    resolved = moved_issues(open_, ["ACME-ISS-1"], {"status": "Resolved", "resolved_by": "1a2b3c4", "resolution": "Fixed."})
    check("the log finish writes passes the issue gate, where the unresolved log is refused",
          judge(resolved, done) == [] and judge(open_, done) != [], str(judge(resolved, done)))
    check("finish begins when the integration branch is pushed and no issue waits on a resolution",
          finish_problems(0, "main", [], None, "ACME-1.2") == [] and finish_problems(0, "main", ["ACME-ISS-1"], "Fixed.", "ACME-1.2") == [])
    check("finish is refused before it merges when the integration branch is ahead of its origin",
          len(finish_problems(1, "main", [], None, "ACME-1.2")) == 1)
    check("finish is refused when its Done resolves an issue and no resolution is given",
          len(finish_problems(0, "main", ["ACME-ISS-1"], None, "ACME-1.2")) == 1)


def _t_paths(check) -> None:
    paths, added = name_status("M\tsprint/story-tracker.md\nA\t.template-version\nD\told.md\n")
    check("name-status reads every path and the added ones", paths == ("sprint/story-tracker.md", ".template-version", "old.md")
          and added == (".template-version",), str((paths, added)))


def run_self_test() -> int:
    print("\nStory Branch Self-Test")
    print("=" * 60)
    state = {"failures": 0, "total": 0}

    def check(label: str, ok: bool, detail: str = "") -> None:
        state["total"] += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok:
            state["failures"] += 1
            if detail:
                print(f"        {detail}")

    for group in (_t_protected, _t_branches, _t_provenance, _t_tracker, _t_start, _t_issues, _t_paths):
        try:
            group(check)
        except Exception as e:   # noqa: BLE001  — a crash is a failure of the group, never of the run
            check(f"{group.__name__} ran without raising", False, f"{type(e).__name__}: {e}")
    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 1 if state["failures"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="The team's branch and merge workflow")
    parser.add_argument("command", nargs="?", choices=("start", "finish"))
    parser.add_argument("story", nargs="?", help="The story ID")
    parser.add_argument("--policy", metavar="MSGFILE", help="The commit-msg hook")
    parser.add_argument("--push", action="store_true", help="The pre-push hook")
    parser.add_argument("--resolution", help="finish: what the story changed, written into each issue its Done resolves")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()
    try:
        if args.self_test:
            return run_self_test()
        if args.policy:
            return cmd_policy(args.policy)
        if args.push:
            return cmd_push()
        if args.command and args.story:
            return cmd_start(args.story) if args.command == "start" else cmd_finish(args.story, args.resolution)
    except Refused as e:
        print(f"story_branch: REFUSED — {e}")
        return 1
    parser.print_usage()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
