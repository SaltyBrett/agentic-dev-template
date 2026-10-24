---
name: How a derived project takes a newer template release
description: 'A project created with gh repo create --template has no git relationship to the template, so the first adoption was a file list in a kickoff. scripts/template_update.py replaces it: ownership decided by path as the inverse of the initializer, keyed merges for the knowledge index and the framework decisions file, git merge-file for everything else and git merge-file --union for .gitignore alone, template markdown stripped to the project profile before comparison, the stamp written last, and the target release''s own copy of the script doing the work. The Claude Code paths: a project''s persona roster kept, the persona library, skills, rules and settings three-way, the journal, notes and local settings untouched; and adoption from v1.0.0: each docs/personas/ file converted into the roster exactly or refused, by a converter that imports nothing from the project''s old scripts, the sync''s stamp removed and its marked entry merged as content.'
teaches: [2026-09-22-004, 2026-09-23-003, 2026-09-25-002, 2026-10-23-002, 2026-10-23-003, 2026-10-23-005, 2026-10-23-007]
verified: 2026-10-23
metadata:
  type: reference
---

# How a derived project takes a newer template release

> Durable learning. Wikilink: `[[reference_template_update]]`.
> Script: `scripts/template_update.py`. Procedure: `TEMPLATE_GUIDE.md` (Taking a newer template release). Birth, which this
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
was rejected because "template-owned" files are legitimately edited: `TEMPLATE_GUIDE.md` (Customizing the law)
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

## The Claude Code paths and the local files

Decisions 2026-10-23-002 and 2026-10-23-003. A project's persona roster, `.claude/agents/`, is
kept: it holds what the project activated or drafted, and a release ships only the library,
`personas/`, which is three-way like the scripts. The initializer clears the template's own roster
at birth and the sanitizer keeps it; a fixture holds each path equal in every place that names it,
because a rename that missed one would leave a project activating into a folder no gate reads.
`.claude/skills/`, `.claude/rules/` and `.claude/settings.json` are three-way too: the template's,
which a project may edit and extend. The journal, the notes and `.claude/settings.local.json` belong to the running session
(`new_project.LOCAL_STATE`): ignored by the repository's own `.gitignore`, touched by none of the
three scripts, kept here. That ignore is checked with `git -c core.excludesFile=`, because an
operator's global excludes file once covered `settings.local.json` and hid that the repository's
did not.

## Adoption from `v1.0.0`: what the retired sync left

Decisions 2026-10-23-003 and 2026-10-23-005. A `v1.0.0` project holds its personas in
`docs/personas/`, a `.resources-version` stamp, and a knowledge entry marked `source: dev-resources`.
The `adopt` class settles all three by what the project holds rather than by either release, so a
project that skips releases adopts the same way:

- **Every persona is converted into the roster, exactly or not at all**, at the operator's chosen
  cost that each becomes a live agent until the project deactivates it. The converter reads the old
  file as `v1.0.0` read it (flat `key: value` lines, a title, four sections) and refuses anything the
  agent file has no place for, because a dropped line is lost silently and a refusal is not. It
  writes an item plain only where YAML reads it back unchanged, and re-parses the whole frontmatter
  before it writes, because Claude Code skips an agent file it cannot parse without a word. Proved on
  the eighteen real files: each library persona converts to its library copy byte for byte.
- **The converter imports nothing from the sibling scripts.** The target's updater runs beside the
  project's old copies, and `v1.0.0`'s persona lint judges the old shape: calling it would pass or
  fail the wrong file. The suite run after `--apply` is the release's, and judges the roster there.
- **The stamp is removed** and **a marked entry is merged like any other**, the declaration one more
  line, so an unedited copy takes the template's unmarked one; a marked entry no release writes just
  loses the line. A wrapped bullet is one item: the real file that had one showed a fixture written
  from assumption had the rule backwards.

## `.gitignore` is merged by union

The three real adoptions conflicted on `.gitignore` and nowhere else among the files both sides
edit: each project had appended its own ignores at the end, and the release appended the journal,
the notes and `.claude/settings.local.json` at the same place. Resolved by hand, the answer was the
same each time, keep both blocks. It is the reason the index and the decisions file have keyed
merges: both sides add at one place, so a line merge conflicts every time. So `.gitignore` alone
goes through `git merge-file --union` (decision 2026-10-23-007): where both sides changed one place,
both sides' lines are kept, the project's first, and the dry run names the path `union` for the
operator to read in `git diff`. The one order that matters in an ignore file, a `!` line after the
pattern it reverses, the template's exact paths never meet. Every other path still conflicts.
Nested `.gitignore` files were rejected: the journal and the notes live under `sprint/`, which the
updater never writes, so a `v1.0.0` project would never receive one.

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
- The updater never writes a project's persona roster, `.claude/agents/` (decision 2026-10-23-003),
  except to convert a `v1.0.0` project's `docs/personas/` into it at adoption (decision
  2026-10-23-005, [[reference_resources_sync]]). The template's own packaging (`pyproject.toml`,
  `.pre-commit-hooks.yaml`) is never written either; a project is not a hook repository.
- Adoption needs PyYAML in the `python3` that runs the updater, since the conversion writes YAML and
  reads it back.
