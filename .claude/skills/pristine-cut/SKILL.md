---
name: pristine-cut
description: 'Reset the template to pristine and start a new lineage from it: read the sanitize check, sweep, rename the repository on GitHub, sanitize, copy the tracked files, create the new repository, cut v1.0.0, then close out and archive the old one. Operator only; the GitHub steps are one-way doors.'
argument-hint: <archive repository name>
disable-model-invocation: true
---

# Pristine cut

Archive name: $ARGUMENTS

This runs only in the template, whose `origin` names the template repository; the sanitizer
refuses anywhere else. Why each step sits where it does is in [[reference_pristine_cut]], and what
the sanitizer resets in [[reference_template_sanitizer]]. Put every GitHub step to the operator
before running it: a rename, a create and an archive are visible to everyone who holds a clone.

1. **Read the check before touching anything.**
   `pre-commit run sanitize-template-check --hook-stage manual --all-files` names every item of build
   state. Group them by file: an item in `sprint/sprint-status.md`, `sprint/story-tracker.md`,
   `sprint/handoffs/` or `sprint/archive/` is the reset's. Any other is the sweep's: by hand, the
   learning kept and the session number, probe reference or commit hash dropped, `verified:` moved,
   and committed before the cut.
2. **Rename the repository on GitHub** to the archive name (`gh repo rename`), so the new repository
   can take the old name. Do not touch the local clone's `origin` yet.
3. **Sanitize in the local clone:** `python3 scripts/sanitize_template.py --apply`, then the check
   above exits 0. The reset stays uncommitted here.
4. **Copy the tracked files only** to a fresh directory: `git ls-files`, filtered to the paths that
   still exist after the reset. Then `git checkout -- .` restores the clone.
5. **Point the old clone at the archive** with `git remote set-url origin <archive URL>`, before the
   new repository exists.
6. **In the fresh directory:** `git init -b main`;
   `python3 scripts/template_version.py --release v1.0.0`; create the empty private repository with
   `gh repo create`; set `origin` under the ssh host alias;
   `pre-commit install --hook-type pre-commit --hook-type commit-msg`; prove the `commit-msg` gate
   with zero commits (a trial commit carrying an attribution trailer is refused); commit
   `release: v1.0.0`; tag it with `git tag -a v1.0.0` and an annotation naming MAJOR and the archive
   repository. Then, before pushing: `pre-commit run template-version --all-files`, the sanitize
   check, `pre-commit run session-verify --hook-stage manual --all-files` at S1 with no pair,
   `pre-commit run --all-files`, and a search for the probe's name that finds only the sanitizer.
7. **Push `main` and the tag**, and read both `gates` runs to the end with
   `gh run watch <id> --exit-status`.
8. **Close out in the archive**, then cut its last release, a PATCH whose annotation names `v1.0.0`
   and the new repository, through the release skill's steps; push, watch its runs, and
   `gh repo archive`.
9. **Carry the cut's record into the new lineage** as one commit after its tag: the knowledge entry
   and the decision's amendment. The tag carries neither.
