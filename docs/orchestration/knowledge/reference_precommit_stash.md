---
name: pre-commit stashes unstaged edits unless told --all-files
description: 'Any `pre-commit run <hook>` without --all-files or --files first stashes unstaged changes to tracked files, so a manual-stage gate judges the last commit''s sprint-status and tracker rather than the ones just edited. Untracked files are not stashed, which is why the new pair is seen but the stories it cites are not. The closeout command carries --all-files; the gate cannot detect the stash itself.'
teaches: [2026-09-22-003]
verified: 2026-09-24
metadata:
  type: reference
---

# pre-commit stashes unstaged edits unless told `--all-files`

> Durable learning. Wikilink: `[[reference_precommit_stash]]`.
> Command: `CLOSEOUT_COMMAND` in `scripts/session_closeout.py`. Companion: [[reference_session_closeout]].

## What it looks like

    [WARNING] Unstaged files detected.
    [INFO] Stashing unstaged files to ~/.cache/pre-commit/patch<...>.
    Session Closeout ... Failed
        `ACME-1.2` is not a story in sprint/story-tracker.md
    [INFO] Restored changes from ~/.cache/pre-commit/patch<...>.

The story is in the tracker on disk. The gate read the tracker from the last commit, because
pre-commit restores the working tree to the index before running a hook invoked without
`--all-files` or `--files`, and puts the edits back afterwards. Untracked files are left alone,
so a freshly scaffolded pair is seen while the tracked files it depends on are not.

## Why the flag, and why nothing stronger

- `--all-files` (or `--files`) tells pre-commit the run is over the working tree, and it does not
  stash. For a hook with `pass_filenames: false` and `always_run: true` the flag changes nothing
  else. Measured on one tree with one unstaged edit: stash without the flag, none with it.
- The gate cannot see the stash. Under it the tree simply equals the index. The patch files in
  `~/.cache/pre-commit/` persist after restore, so their presence is not evidence.
- Staging everything first (`git add -A`) also avoids it, and is what the checkpoint protocol
  leads to anyway, but the documented command should not depend on the reader remembering that.

## The failure is loud, not silent

The files a stash hides are the ones carrying the session number and the story IDs, so a stale
read produces a violation rather than a pass. And the per-commit `--check` runs on the staged tree
whatever the manual run saw. The cost is a red that sends the reader to fix a tracker that is
already right.

## The same guard refuses a modified, unstaged config

    [ERROR] Your pre-commit configuration is unstaged.
    `git add .pre-commit-config.yaml` to fix this.

Seen when testing the commit-msg stage right after the updater rewrote `.pre-commit-config.yaml`.
The stash would hide the config the run was asked to use, so pre-commit refuses to run any hook
at all rather than run the wrong suite. `--all-files` lifts it for the same reason it lifts the
stash; so does staging the config. The updater's own suite run passes `--all-files`, which is why
`--apply` is not refused on the config it just wrote.

## Rules

- Invoke a manual-stage gate with `--all-files`. The scaffold writes the closeout command that way.
- Stage `.pre-commit-config.yaml` before testing the commit-msg stage against it.
- When a pre-commit run prints "Stashing unstaged files", read its verdict as a verdict on the
  last commit, not on your edits.
