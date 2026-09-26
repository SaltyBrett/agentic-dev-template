---
name: How a derived project takes a newer template release
description: 'A project created with gh repo create --template has no git relationship to the template, so the first adoption was a file list in a kickoff. scripts/template_update.py replaces it: ownership decided by path as the inverse of the initializer, keyed merges for the knowledge index and the framework decisions file, git merge-file for everything else, template markdown stripped to the project profile before comparison, the stamp written last, and the target release''s own copy of the script doing the work.'
teaches: [2026-09-22-004, 2026-09-23-003, 2026-09-25-002]
verified: 2026-09-25
metadata:
  type: reference
---

# How a derived project takes a newer template release

> Durable learning. Wikilink: `[[reference_template_update]]`.
> Script: `scripts/template_update.py`. Procedure: `TEMPLATE_GUIDE.md` Step 9. Birth, which this
> is the inverse of: [[reference_derived_project_start]] and `scripts/new_project.py`.

## Why an updater and not a remote

`gh repo create --template` copies a tree and squashes history. The derived project and the
template share no commit, so `git merge` has no base and `git pull` has nothing to pull. The first
derived project's second kickoff therefore listed the files to copy by name, which is a checklist. The
updater gives the project the base git lacks: it fetches the release the project is on and the
release it wants into `refs/template/<version>`, and every path is judged against both.

The refs sit outside `refs/tags/` on purpose. The version gate reads `git tag`, and a tag named
`v4.1.2` in a derived project would fail it (no commit there carries that version).

## Ownership is decided by path, and it is the initializer's inverse

What `new_project.py` regenerates or clears at birth (`sprint/sprint-status.md`, the tracker,
the handoffs) the updater never writes, and so is the project's decision log, filled at the header
at birth and the project's own from then on. What it fills otherwise (`AGENTS.md`,
`CONSTITUTION.md`) is merged three-way. What it preserves because the knowledge entries
`teaches:` it (the framework decisions, the knowledge base, the personas) is carried forward. A
fixture reads the initializer's lists and checks the map against them, so the two scripts cannot
drift apart silently. One path is the project's without the initializer touching it: `LICENSE`
arrives at birth as the template's MIT text and is kept from then on, because a project may
replace it with its own and a release must never rewrite a license (decision 2026-09-25-002); a
project born before the license existed receives none by update.

## Why three-way for everything, not overwrite for template-owned files

The natural design has two mechanisms: overwrite template-owned paths, merge shared ones. It
was rejected because "template-owned" files are legitimately edited: `TEMPLATE_GUIDE.md` Step 5
tells a project to add patterns to `banned_feature_scan.py`, and the standards carry tokens the
project fills. `git merge-file` covers both cases with one mechanism, and for an unedited copy it
reduces to overwrite. Only two files need something else, because both sides append rows at the
same place in a table and a line merge would conflict every time: the knowledge INDEX (keyed by
slug) and the framework decisions file (keyed by decision ID, rows and bodies).

## The framework decisions are merged by ID; the project's log is never written

A framework decision the project lacks must arrive, because the framework's knowledge entries
declare `teaches:` against it and the freshness gate refuses an unindexed ID. Until `v11.0.0` it
arrived by insertion into `sprint/decision-log.md`, the one file under `sprint/` the template
still wrote and the reason decision 2026-09-23-003 called that merge the least comfortable part
of the design. Since then the template's decisions live in
`docs/governance/framework_decisions.md` and that file is what the merge reads: a row the project
lacks is inserted at the top of the index and its body appended at the end; an existing row or
body is replaced only when it still equals the previous release's, byte for byte; an edited one is
reported and left; nothing is ever removed; `[EXAMPLE]` rows and bodies never travel. The
project's log is kept with the rest of `sprint/`. A project that took a release before the split
still carries the old copies in its log, and the gates let the framework file win those duplicate
IDs ([[reference_framework_decisions]]).

## Three things that were not obvious until the probe ran

- **Knowledge entries carry profile blocks too.** `reference_project_profiles.md` in the probe
  differed from the template's copy by five stripped lines. Every comparison and every write of
  template markdown goes through `strip_profiles` with the project's profile first, or every
  document with a block reads as project-edited.
- **The updater updates itself, so the target's copy must run.** The ownership map is in the
  script. The run compares the executing file with the target release's blob and refuses with
  the two commands that fetch it; a target that predates the updater is accepted with a note.
- **The stamp is written last, after every clean write, and withheld on a conflict.** A
  conflict leaves the file alone and names the `git diff refs/template/…` that shows it. The
  re-run needs `--keep <path>` or `--take <path>`, because a hand-resolved file still differs
  from both sides and would conflict again.

## Honest limit

The one-line `not applied` summary names every project-owned path the template changed, and
between releases that includes the template's own `sprint/handoffs/` pairs and sprint files,
which mean nothing to a project. It is one line, and it stays: a `keep` that reported nothing
would be indistinguishable from a `keep` that saw nothing.

## Rules

- Take a release with `scripts/template_update.py`, dry run first, then `--apply`, then commit
  the whole result as one checkpoint and observe the push's `gates` run.
- A kickoff written before a release names the release it knows. When the template moves on
  before the session runs, take the newer release and say so in the sprint-status entry.
- Since decision 2026-09-23-007 the updater never writes `docs/personas/` or a knowledge entry
  whose frontmatter declares `source: dev-resources`; those are the resources sync's, told apart
  by content because they share a directory with the template's own entries
  ([[reference_resources_sync]]). The template's own packaging (`pyproject.toml`,
  `.pre-commit-hooks.yaml`) is never written either; a project is not a hook repository.
