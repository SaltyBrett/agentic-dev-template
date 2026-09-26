---
name: How the pristine cut is performed, and the order that keeps two repositories apart
description: 'The cut under decision 2026-09-23-003 as executed: the sanitize check read first and every item judged against what the reset clears; the GitHub rename before anything else; the sanitizer run while the local clone''s origin still names the template; only tracked files copied to the fresh directory; the old clone''s origin switched to the archive name BEFORE the new repository is created, because the old URL redirects to the renamed repository only until a repository with the old name exists again; the first commit proved against the commit-msg gate with zero commits behind it; what is carried into the new lineage after its v1.0.0 and why the tag itself is the sanitized tree alone. Read before the next cut or before renaming a repository a clone still pushes to.'
teaches: [2026-09-23-003, 2026-09-25-004]
verified: 2026-09-25
metadata:
  type: reference
---

# How the pristine cut is performed, and the order that keeps two repositories apart

> Durable learning. Wikilink: `[[reference_pristine_cut]]`.
> Decision 2026-09-23-003. Tools: `scripts/sanitize_template.py` ([[reference_template_sanitizer]]),
> `scripts/template_version.py` ([[reference_template_versioning]]). The archive is
> `SaltyBrett/agentic-dev-template-archive`; its final tag names the new lineage's `v1.0.0`.

## The order, and what forces it

1. **Read the sanitize check before touching anything.** `pre-commit run sanitize-template-check
   --hook-stage manual --all-files` names every item of build state. Group the items by rule and
   by file: an item inside `sprint/sprint-status.md`, `sprint/story-tracker.md`, `sprint/handoffs/`
   or `sprint/archive/` is cleared by `--apply`; an item anywhere else is the sweep's, by hand,
   with `verified:` bumped and committed before the cut. At the cut every item was inside the
   reset's files, the probe mentions included, so there was nothing to sweep.
2. **Rename the repository on GitHub first.** The new repository needs the old name, so the old
   one must give it up before the new one can be created. A rename is reversible.
3. **Run the sanitizer while the local clone's origin still names the template.** Its refusal
   judges the URL string, which a rename on GitHub does not change. `--apply` then `--check` to
   exit 0, in the clone itself; the reset is uncommitted there and `git checkout -- .` restores it
   once the copy is taken, because the sanitizer deletes and rewrites but never creates.
4. **Copy tracked files only.** The working tree carries ignored files a plain copy would put into
   the first commit: `.DS_Store`, `__pycache__/`, the `egg-info/` a local `pip install .` left, a
   tool's `settings.local.json`. `git ls-files`, filtered to the paths that still exist after the
   reset, is the list; copy those and nothing else.
5. **Switch the old clone's origin to the archive name before creating the new repository.**
   GitHub redirects the old name to the renamed repository only until a repository with the old
   name exists again. Once the new one is created, the old URL points at the new repository, and a
   push from a clone whose origin was never switched lands in the wrong lineage. The switch is one
   `git remote set-url`, done between the sanitizer and the create.
6. **In the fresh directory:** `git init -b main`, `template_version.py --release v1.0.0` so the
   constant is set before the commit that gets tagged, create the empty private repository, set
   origin under the ssh host alias, install both hook types, and prove the commit-msg gate before
   the first real commit: a trial commit carrying an attribution trailer is refused with zero
   commits in the repository, and the clean `release: v1.0.0` is accepted. Tag `v1.0.0` annotated;
   the earliest tag is exempt from the bump rule and the annotation names MAJOR anyway, and it
   names the archive repository, so the two lineages point at each other. Then, before pushing:
   the version gate, the sanitize check, `session-verify` at S1 with no pair, the whole suite, and
   a grep for the probe's name that names the script alone.
7. **Push `main` and the tag, and read both `gates` runs to completion** with `gh run watch
   --exit-status`, not by assumption.
8. **Only then close out in the archive**, because the story the closeout marks Done says the new
   lineage's `gates` run was observed. The archive's last commits are the closeout and a PATCH
   release cut with `--release`, whose annotation names `v1.0.0` and the new repository. Then the
   version gate, the push, its `gates` runs, and `gh repo archive`.

## What v1.0.0 is, and what is carried after it

At the cut, `v1.0.0` was the sanitized tree and nothing else: the fixed constant was its one change
from the sanitizer's output. The record of the cut itself, this entry and the decision's amendment,
exists only once the cut is done, so it was carried in as a commit after the tag, leaving `main`
one commit ahead of its release, the ordinary state between releases.

Then the go-live work followed (the template flag, the visibility decision and its control, the
license, the public README, the rulesets), and the operator asked that the *finished* template's
first release be `v1.0.0` (decision 2026-09-25-004). So the cut's tag and the three that followed
it were removed, the finished tree was sanitized again to S1 with the same script, and one
`v1.0.0` was cut on it. History was kept; only tags moved, before any outside consumer existed.
Do not read that as a precedent: a published tag is permanent once anyone else can have taken it.
The sanitizer's job is the same each time, which is the point of having it as a script.

## Where the session that performed the cut records itself

In the archive: its sprint-status entry, the tracker row, and the pair it scaffolds for the next
session. The next session runs in the new lineage at S1, under the entry the sanitizer wrote, with
no incoming pair, which `session-verify` accepts; its kickoff, read from the archive, says so and
names the new repository. The first maintenance session on the new lineage opens its first story
before it can scaffold S2, as any fresh project does ([[reference_derived_project_start]]).

## Rules

- A rename on GitHub does not change a clone's origin, and a redirect from the old name lasts only
  until the name is reused. Switch every clone that will push before reusing the name.
- Copy a tree by its tracked file list, never by directory.
- The cut's own record goes into both lineages; the tag carries neither.
