---
name: CI is the reporting backstop for per-clone hooks
description: 'Git hooks are per-clone and nothing in the repository can tell whether a clone installed them. The GitHub workflow runs the same suite on every push and pull request, plus the commit-msg gate over each carried commit. It reports; the local hooks block. Why branch protection is not part of the design even now that the repository is public, and what the red probe proved.'
teaches: [2026-09-22-001, 2026-09-25-001]
verified: 2026-09-25
metadata:
  type: reference
---

# CI is the reporting backstop for per-clone hooks

> Durable learning. Wikilink: `[[reference_ci_backstop]]`.
> Workflow: `.github/workflows/gates.yml`. Companion: [[reference_commit_attribution_gate]], which
> first recorded that a hook can be present in config and absent in practice.

## Why a second run of the same suite

A hook lives in `.git/hooks/`, which is never committed. A clone that skipped the install command
commits through no gate, and every file in the repository reads as protected. The workflow runs the
identical suite where the clone's hook state is irrelevant. It is not a second set of rules; it is
the same scripts with a second trigger.

## What the workflow does that `--all-files` does not

`pre-commit run --all-files` exercises the pre-commit stage only. The commit-msg gate needs a message
file, so the workflow's second step walks every commit the push or pull request carried and runs the
commit-msg stage against each message. A new hook stage added later needs a matching step here in
the same work unit, or it is present in config and absent on CI too. Since 2026-09-23 that is a
control, not a rule: `gate_runbook_scan.py` reads the stages every hook declares and the
`pre-commit run` lines in the workflow's steps, and fails a non-manual stage no step runs, a
missing workflow, or one that does not parse ([[reference_gate_runbook]]).

The range is `before..HEAD` for an ordinary push, `origin/<base>..HEAD` for a pull request, and the
tip alone when `before` is unknown or no longer exists (a new branch, or a force-push). Checkout uses
`fetch-depth: 0` because the template-version gate reads tags.

## It reports; the hooks block

A red run is visible after the push has landed. Turning it into a refusal needs GitHub branch
protection. While the repository was private that was unavailable on a free plan (the API returned
403, measured); since decision 2026-09-25-001 the repository is public and protection is free, and
it is still not enabled, for a different reason: every checkpoint is a direct push to `main`, and a
required status check would force a pull-request flow on one developer for a run that already
reports. So the design is unchanged: the local hooks are the blocking control, and the workflow is
the audit of what they would have caught. A red run is acted on in the same session. One run of
this suite takes about two minutes.

Derived projects are private by default (the initializer refuses a public one without `--public`),
so for them protection stays a GitHub Pro question; the template's visibility protects nothing
downstream.

## What the probe proved

A clone made without installing hooks committed a stray file into `sprint/handoffs/` and pushed it
on a throwaway branch. The local suite never ran; the workflow went red on the session state gate.
The same tree without the file went green. Both runs were observed, not assumed.

## Rules

- Never add a hook stage without a matching workflow step; the runbook gate refuses the commit.
- Never treat a green local suite as proof that CI will pass a message trailer; the stages differ.
- A red run on GitHub is fixed in the session that caused it, before the closeout.
- A tag push is its own run, and the checkout flattens the tag it was triggered by; the workflow
  fetches the tag objects back before the suite runs ([[reference_ci_annotated_tags]]).
