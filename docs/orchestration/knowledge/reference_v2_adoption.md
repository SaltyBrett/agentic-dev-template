---
name: How the three projects were taken to v2.0.0
description: 'The record of TMPL-2.4''s adoption: a scratch v2.0.0 and scratch clones first, the release''s own updater refused only by the approval gate, the documents approved as they stood, the stamp, the push to the branch each project works on and its gates run. What each project showed (a branch that is not main, a session never closed out, one document where the script assumed two) and the rules they leave for the next adoption. Read before taking a project to a new MAJOR release.'
teaches: [2026-10-24-003]
verified: 2026-10-24
metadata:
  type: reference
---

# How the three projects were taken to v2.0.0

> Durable learning. Wikilink: `[[reference_v2_adoption]]`. Story: TMPL-2.4. Procedure:
> `TEMPLATE_GUIDE.md` (Taking a newer template release). Companions: [[reference_template_update]],
> [[reference_doc_authority]].

## Scratch first

Before the tag existed, a scratch `v2.0.0` was cut on a clone of the template and a clone of each
project taken to it with the release's own updater. Every path applied with no conflict and every
persona converted; the suite's one failing hook was `doc-authority-scan`, its only violations the
two `approval` lines each project's real epics raise. That settled what the adoption needed before
anything public moved, and the decision on bringing the documents in (2026-10-24-003) was written
from it. A MAJOR release is proved on scratch clones of the projects that will take it, not on the
template alone, since the gates judge a project differently.

## The adoption, per project

The release's updater, dry run then `--apply`, which ends by running the suite and was refused by
the approval gate alone; then the documents approved as they stood by one script, the suite, the
commit, `--stamp`, the stamp's commit, the suite again, and the push with its `gates` run watched.

- **Supplier_Research_Dev**: the PRD at Rev E approved as 1.0, the architecture it does not have
  skipped by the Chair: "The stack is still undecided; the architecture is written when it is
  chosen." The first run's wording assumed two documents ("approve the PRD as they stand", a commit
  subject naming the architecture); both commits were unpushed, so the clone was reset to its head
  before the adoption and the fixed script run again.
- **Comfy**: the PRD at 1.4 and the architecture at 1.0, its `prd:` 1.4. The push carried nine
  earlier commits of an S4 never closed out; its `session-verify` fails as it did before the
  adoption, which touches nothing under `sprint/`, and its next session completes the closeout.
- **PocketGames**: the same at 1.4 and 1.0. The clone works on `build/milestone-1` and
  fast-forwards `main` to it at a release, which deploys; the first push sent the stale local
  `main` and was rejected, changing nothing. The adoption went to `build/milestone-1`, and `main`
  waits for the project's own release step.

Each run was green on `gates` and both `birth` jobs; the run IDs are in the S11 sprint-status entry.

## Rules

- Prove a MAJOR release on scratch clones of the projects that will take it before the tag.
- Push the branch the project works on (`git status -sb`), never `main` by assumption; a project's
  `main` may be its deploy.
- Read the project's session state before the adoption commit lands: a session left open stays
  open, and the adoption touches nothing under `sprint/`.
- Read a scripted decision's text in every shape it is written for before the push; once pushed,
  the record stands.
