---
name: The template is reset to pristine by a script, and what pristine means
description: 'Why scripts/sanitize_template.py exists and what it is not: the initializer''s machinery without the fill, run only in the template, its --check naming every item of build state (a sprint-status entry above S1, a TMPL- story row, either archive, a pair, the probe repository''s name) while the sweep of session numbers, probe references and commit hashes out of the knowledge entries and decision bodies stays by hand. Why the script excludes itself from the name check, why the sync stamp stays, why --check is a manual hook, and what the scratch proof showed. Read before running the sanitizer, before the pristine cut, or before writing a session number into a knowledge entry.'
teaches: [2026-09-23-003]
verified: 2026-09-24
metadata:
  type: reference
---

# The template is reset to pristine by a script, and what pristine means

> Durable learning. Wikilink: `[[reference_template_sanitizer]]`.
> Script: `scripts/sanitize_template.py`. Hooks: `sanitize-template-selftest` (every commit),
> `sanitize-template-check` (manual). Decision 2026-09-23-003. Birth, which this mirrors:
> `scripts/new_project.py` and [[reference_derived_project_start]].

## The failure this closes

The template carried its own construction: sprint-status entries for every session, the `TMPL`
epics, a handoff pair per session and the archive of the older ones, the sprint-status archive
once the cap fired, and the name of the derived probe repository in every place that recorded a
proof. A project created from it inherited none of that, because the initializer regenerates or
clears the sprint documents, but the template itself was not the artifact the operator wanted to
clone from, and the build diary in the decision bodies read as history a new project has no part
in. The operator asked for a pristine tree and for the unsanitized repository to be kept.

## What the script is, and is not

- **The initializer's machinery without the fill.** `--apply` regenerates `sprint/sprint-status.md`
  with the template's own S1 entry and `sprint/story-tracker.md` with the initializer's skeleton
  (the `[EXAMPLE]` epic, statistics at zero), removes every file under `sprint/handoffs/`, its
  `archive/` and `sprint/archive/`, then runs the suite. It fills no token, strips no profile block
  and writes no `.project-profile`, so the template keeps every shape it ships. The tracker keeps
  its `{{DATE}}` token, which the initializer fills at a project's birth.
- **NEVER_RESET holds, plus the sync stamp.** The framework decisions, the project's decision log,
  the knowledge base and the personas are in no mutating list, pinned by the same kind of fixture
  the initializer carries. `.resources-version` stays too: it names the `dev-resources` ref this
  repository last synced, which is the template's own state and what the closeout's persona rule
  reads, not session state.
- **`--check` names build state; it does not sweep.** Five rules, each pure over a snapshot of
  the tree: a sprint-status entry numbered above S1, a table row whose Story ID is `TMPL-`, a file
  in either archive, a handoff or kickoff in `sprint/handoffs/`, and the probe repository's name
  in any text file git would commit. A `TMPL-` ID in prose is a mention, not a row. The sweep of
  session numbers, probe references and commit hashes out of the knowledge entries and decision
  bodies is by hand, as the decision says, because a script cannot tell an incidental `S7` from a
  learning that needs it; the name check is the one part of the sweep a script can prove.
- **The script is the one file allowed to hold the name.** A rule that looks for a name has to
  write it somewhere, and a check that scanned its own source would fail forever. The exclusion
  is by path and a fixture pins it, so the rule applies to every other file, the runbook included,
  which describes the check without naming what it looks for.
- **It runs only in the template.** The inverse of the initializer's refusal: `origin` must be
  the template's repository, judged by the same function the initializer uses, so the two cannot
  disagree about which repository is which. A local clone of the template has that origin, which
  is how the scratch proof runs it. `--force` overrides for a deliberate re-scaffold.
- **`--check` is a manual-stage hook.** This repository fails it until the cut, so it cannot be a
  commit gate; and a derived project is never asked the question, since the refusal answers it
  first. The self-test reads nothing from the tree, so the suite stays green in every project.

## Observed on the scratch proof

A local clone of the template has the template's origin, so the sanitizer ran there without
`--force`: `--apply` exited 0 with the suite green inside it, `--check` exited 0, the suite alone
exited 0, and `session-verify` exited 0 once the reset was committed, at S1 with no pair. Before
that commit it exited 1 on `not-closed` and `stale-pair` rather than `dirty-tree`: pre-commit had
stashed the unstaged reset and the gate judged the last commit's tree ([[reference_precommit_stash]]).
A second clone, of the sanitized clone, was refused by the sanitizer and initialized by
`new_project.py` on `commercial` with the suite green, the log's index holding the example alone,
the freshness gate indexing every framework decision with none UNKNOWN, and `session-verify`
exit 0 after the first commit. Its `.template-version` named the last release, not the pristine
cut, because the constant is set at release time; a local clone also carries the template's tags,
which a project created on GitHub does not.

## The maintenance loop after the cut

The pristine tree passes `--check` at S1 with no pair. The first maintenance session on it opens
a story, closes out and scaffolds S2, and the tree fails `--check` again. That is by design: the
check proves the state at a cut, not a property every commit must keep. The next cut runs
`--apply` again and sweeps by hand again; the archive repository holds the history in between.

## Citations after the sweep

A knowledge entry or decision body keeps its learning and loses the session number, the probe
reference and the commit hash that dated it. Where the history matters, the citation names the
archive repository, `SaltyBrett/agentic-dev-template-archive`, and the release tag in that
lineage, whose numbering the new lineage does not share: the new lineage's first tag is `v1.0.0`
and its constant is set at the fresh `git init`, not by the sanitizer.

## Rules

- Run `--check` before a cut and read every item it names; the sweep is what clears the ones the
  reset does not.
- Never write a session number, a probe story ID or a commit hash into a knowledge entry or a
  decision body as a citation. Say what was observed; if the where matters, name the archive
  repository and its tag.
- The self-test's fixtures are proved against broken copies before they are trusted, as every gate
  here is; a variant that crashes instead of failing a fixture proves nothing and is rewritten.
