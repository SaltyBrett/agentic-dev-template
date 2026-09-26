# Document Control Standard (GitHub-Governed)

## Purpose

Prevent drift, loss, or corruption of authoritative documents (PRD, Architecture, Standards,
Runbooks) with controls that git and the gate suite enforce, not with manual tracking.

## Scope

Governed documents include: PRD, Architecture specs, Standards, Runbooks, and metadata seeds.

## Branching & Protection

- The gate suite blocks locally as git hooks (`.pre-commit-config.yaml`) and reports on GitHub on
  every push and pull request (`.github/workflows/gates.yml`). A red run is fixed in the same session.
- `main` carries no GitHub branch protection: it needs GitHub Pro or a public repository, and this
  one stays private (decision 2026-09-22-001). Do not write procedures that assume a blocked push.
- No force-push. Denied for agents in `.claude/settings.json`; a human uses `git revert`.
- Reviewers are required only where a project adds them; with one developer there are none.

## Change Workflow

No branch-and-pull-request convention is imposed (decision 2026-09-22-001). Work lands on `main` as
`checkpoint:` commits, each judged by the suite. A project that adds reviewers chooses its own branch
convention and records it as a decision.

1. Update the documents, and the changelog table where a document carries one, with the rationale
2. `pre-commit run --all-files` exits 0
3. Commit `checkpoint: …`; the per-commit state gate reconciles the sprint documents
4. Push; the `gates` run on GitHub is green before the session ends

## Review

The gate suite is the review checklist. What each hook blocks, in run order, is in
`docs/governance/gate_suite_runbook.md`, and a gate keeps that page in step with the config. What
the suite cannot judge (intent clear, scope limited) is a reviewer's, where a project has one.

## Evidence & Audit

- Validation evidence for a material change goes in `evidence/<date>/<artifact>/`, in the shape of
  `sprint/recovery/templates/VALIDATION_EVIDENCE_TEMPLATE.md`, and the session's sprint-status
  entry names it. No gate checks this (decision 2026-09-24-001).
- Baselines are annotated tags. The template's own are verified by `scripts/template_version.py`;
  a project's baseline tag uses the same `vMAJOR.MINOR.PATCH` form.

## Rollback & Recovery

- Use `git revert` (not force-push)
- Restore from previous tag if corrupted
- Keep legacy copies read-only for forensic comparison

## Agentic vs Human Controls

- Agents are authorized for initial build and configuration only; steady-state operations are
  human-run (`CONSTITUTION.md` §9)
<!-- profile:gcc -->

## Banned Content

- No reintroduction of GCC-incompatible features (`CONSTITUTION.md` §3 Banned Features); the
  banned-feature scan enforces it on every commit
- T-SQL-first, no M/Power Query for transformation (`CONSTITUTION.md` §4)
<!-- /profile:gcc -->
