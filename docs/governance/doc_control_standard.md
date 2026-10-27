---
authority: document control (how an authoritative document declares itself, records each change and is verified)
implements: []
verified: 2026-10-25
---

# Document Control Standard (GitHub-Governed)

## Purpose

Keep each authoritative document (PRD, architecture, standards, runbooks) the current source of
truth for its scope, with controls that git and the gate suite enforce, not manual tracking. A
decision lands in the log first and in the document last; `scripts/doc_authority_scan.py` refuses
the commit that leaves the document behind.

## Authorities

- A document is an authority when its frontmatter says so. The frontmatter is the registry, with
  no list kept beside it; `python3 scripts/doc_authority_scan.py --list` prints it.

  ```yaml
  ---
  authority: <the scope this document is the source of truth for>
  implements: [<decision-id>, ...]   # [] when none
  verified: YYYY-MM-DD               # unquoted
  ---
  ```

- The template marks its standards (`docs/standards/`, this file), the gate-suite runbook and the
  document templates (`docs/templates/`), each template the authority for its document's shape. A
  project marks its PRD, its architecture and its runbooks; a PRD or an architecture is made from
  its template as a draft and becomes the authority for the project's scope when it is approved.
  Once a project's tracker holds a real epic, `doc-authority-scan` requires both approved, one
  document each in `docs/prd/` and `docs/architecture/`, an approved architecture's `prd:` the
  PRD's newest version; or the Chair's skip, an APPROVED decision in `sprint/decision-log.md`
  headed `**Skips:** prd` or `**Skips:** architecture`. A document reopened for revision
  (`status: draft`, its authority and rows kept) stands at its last approved version until it is
  approved again, so a revision in progress can be committed; approving a PRD revision is refused
  until the architecture built on the old version is reopened too.
- One scope, one authority. A document that takes over a scope takes the `authority:` line; the one
  it replaces drops the line and says where the scope went. Two documents claiming one scope fail
  the gate.
- `verified:` moves when the document has been re-read against every decision it implements; the
  gate fails the document when one of them changed later. Never move the date alone.

## Recording a change

1. A decision that changes an authority names it in `**Affects:**`: its path as a code span, the
   sections, the nature of the change. Every decision from 2026-10-22 carries the line, `none` where
   nothing changes.
2. In the same commit, the document's `## Version log`, its last section, gets a row citing the
   decision, newest first, in the columns Version, Date, Decision, Summary, Commit. A factual change
   made inline opens its summary with `fact:` and states the fact: a value, a name or a path in
   backticks, or a count. A structural change is planned work: queue it as a tracker story citing
   the decision and the path, and the row written when the story does the work cites the story. The
   gate accepts the row or the open story, and nothing else.
   A change left for the technical writer is marked on its story's row with a bare `Queued: S<N>`,
   N the session that queued it, and the story names that one document. The `doc-queue` gate, run
   at every cold start, lists the queue and fails a story still open after S<N+1>; the doc-drain
   skill makes every queued change to one document in one pass, in the writer's role, and leaves it
   for the session to review. A story that makes its own change carries no note.
3. The row's Commit reads `pending`. Once the row is committed,
   `python3 scripts/doc_authority_scan.py --stamp` writes the commit that introduced it, and the
   gate verifies every stored hash against git. Never type a hash.
4. Versions are `MAJOR.MINOR`: a structural rewrite raises MAJOR, any other change MINOR. A file name
   keeps the version its document was introduced under, because every tracker cites the standards by
   file name.
5. Each of the template's documents arrives with one row, its starting row: the document's version
   and date, `template` in its Decision and Commit cells, citing nothing and storing no hash. A
   project's own changes go above it, each citing the project's decision; the gate refuses a
   starting row anywhere but last.

## Branching & Protection

- The gate suite blocks locally as git hooks (`.pre-commit-config.yaml`) and reports on GitHub on
  every push and pull request (`.github/workflows/gates.yml`). A red run is fixed in the same session.
- Protection on `main` depends on the repository. The template is public, and a ruleset on its
  `main` blocks deletion and force-push, with no required status check because every checkpoint is a
  direct push. A project is private by default,
  and a private repository on a free plan has no protection at all. Do not write procedures that
  assume a blocked push.
- No force-push. Denied for agents in `.claude/settings.json`; a human uses `git revert`.
- Reviewers are required only where a project adds them; with one developer there are none.

## Change Workflow

No branch-and-pull-request convention is imposed. Work lands on `main` as
`checkpoint:` commits, each judged by the suite. A project that adds reviewers chooses its own branch
convention and records it as a decision.

1. Update the document and its version log (Recording a change, above)
2. `pre-commit run --all-files` exits 0
3. Commit `checkpoint: ...`; the per-commit state gate reconciles the sprint documents
4. Push; the `gates` run on GitHub is green before the session ends

## Review

The gate suite is the review checklist. What each hook blocks, in run order, is in
`docs/governance/gate_suite_runbook.md`, and a gate keeps that page in step with the config. What
the suite cannot judge (intent clear, scope limited, a row's content true) is a reviewer's, where a
project has one.

## Evidence & Audit

- Validation evidence for a material change goes in `evidence/<date>/<artifact>/`, in the shape of
  `sprint/recovery/templates/VALIDATION_EVIDENCE_TEMPLATE.md`, and the session's sprint-status
  entry names it. No gate checks this.
- Baselines are annotated tags in the `vMAJOR.MINOR.PATCH` form.

## Rollback & Recovery

- Use `git revert` (not force-push)
- Restore from previous tag if corrupted
- Keep legacy copies read-only for forensic comparison

## Agentic vs Human Controls

- Agents are authorized for initial build and configuration only; steady-state operations are
  human-run (`CONSTITUTION.md` section 9)

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.10 | 2026-10-25 | template | the template's version 1.10 | template |
