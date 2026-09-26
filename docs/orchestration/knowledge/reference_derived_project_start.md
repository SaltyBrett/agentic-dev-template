---
name: What day one of a derived project looks like
description: 'Observed on the first real repository created from the template with gh repo create --template. GitHub runs the gate suite on its own Initial commit before you have run anything; the clone remote is git@github.com and needs your ssh host alias if you separate identities; the initializer regenerates both sprint-status and the tracker, and the tracker starts at zero stories; session-verify passes at S1 with no pair; the attribution gate is live before the first commit.'
teaches: [2026-09-22-002]
verified: 2026-09-25
metadata:
  type: reference
---

# What day one of a derived project looks like

> Durable learning. Wikilink: `[[reference_derived_project_start]]`.
> Procedure: `TEMPLATE_GUIDE.md` Step 8 and `scripts/new_project.py`. The probe was a private
> repository on the `commercial` profile, created from `v4.1.0` of the archive repository,
> `SaltyBrett/agentic-dev-template-archive`.

## In the order it happens

1. **`gh repo create <name> --template SaltyBrett/agentic-dev-template --private --clone`** makes
   a repository with one commit, "Initial commit", carrying the template's `main` HEAD. GitHub
   pushes that commit itself, so the `gates` workflow runs before you have done anything. It is
   green, because the template tree passes its own suite. Expect it; it is not your run. The
   command works only while the repository carries GitHub's template flag, which a fresh `git init`
   and push do not set: after the pristine cut the new repository read `isTemplate: false` until
   `gh repo edit <owner>/<name> --template` set it. Check the flag before blaming the command.
2. **The clone's remote is `git@github.com:<owner>/<name>.git`.** A machine that separates
   identities by ssh host alias (`Host github.com-personal`) has no `Host github.com` block, so
   the first push would use no personal key. Set the remote to the alias before anything else:

       git remote set-url origin git@github.com-personal:<owner>/<name>.git

   Clone under the directory your `includeIf` covers (`~/code/personal/` here) so `user.email`
   resolves; `user.useConfigOnly` refuses the first commit otherwise ([[reference_macos_toolchain]]).
3. **Dry-run the initializer, then `--apply`.** It fills `AGENTS.md`, `CONSTITUTION.md` and the
   decision-log header (the log ships with the `[EXAMPLE]` entry alone since decision
   2026-09-23-003; the framework's decisions are in `docs/governance/framework_decisions.md`);
   regenerates `sprint/sprint-status.md` (one S1 entry) and
   `sprint/story-tracker.md` (zero stories, the `[EXAMPLE]` epic); clears `sprint/handoffs/`
   including the archive; strips the other profile from four documents; writes `.project-profile`
   and `.template-version`; then runs the suite. Before decision 2026-09-22-002 the tracker was
   filled, not regenerated, and the new project inherited the template's own `TMPL` epics.
4. **Install both hook types.** `pre-commit install --hook-type pre-commit --hook-type commit-msg`.
   Then prove the commit-msg gate exists: a trial commit carrying a `Co-Authored-By` trailer is
   refused with `COMMIT ATTRIBUTION GATE: BLOCKED`, and `git log` still shows "Initial commit".
5. **The first real commit and push.** The pre-commit stage runs every gate; the push's `gates`
   run is green. Observe it with `gh run list`, not by assumption.
6. **`pre-commit run session-verify --hook-stage manual` passes at S1** with no incoming pair; the
   initializer's sprint-status entry is what the gate numbers the session from.
7. **S1's closeout is the first real test of the tracker.** Every kickoff task must cite a story
   present in the tracker, and the tracker starts empty, so S1 opens the project's first epic
   before it can scaffold the S2 pair. That is the Planning Session Protocol doing its job on a
   small scale, not friction.

## What was left by hand, on purpose

`TEMPLATE_GUIDE.md` and the `[EXAMPLE]` rows stay until the project decides. The deferred brand
and Azure tokens are reported by the initializer and filled when a document first needs them.
The probe decided, four releases in, to keep both: the guide is the procedure it runs at every
release and the updater keeps it current; the example rows are skipped by every parser and
document the shape.

## Prefix the project's decision IDs

The template's decision IDs are bare dates. When the probe was created they arrived in the
project's log by insertion, and a project decision written as `2026-09-23-007` could collide with
the framework's next `2026-09-23-007`: the merge then reported an edited row and left it, and the
freshness gate read the wrong body. Since decision 2026-09-23-003 the framework's decisions live
in `docs/governance/framework_decisions.md` and never enter the project's log, but the gates read
both indexes as one set and the framework's row wins a duplicate, so an unprefixed project ID can
still be shadowed at the next release ([[reference_framework_decisions]]). A project with the story
prefix `ACME` writes `ACME-2026-09-23-001`. The gates read IDs literally, so any prefix works.
