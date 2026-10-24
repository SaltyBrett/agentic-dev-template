# Kickoff — S15

**For session:** S15
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S15.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

One task, the coding standard's gate core and its Python profile, from `docs/standards/coding_standard_v1.0.md` and decisions 2026-10-24-007, 2026-10-24-008 and 2026-10-24-010. It is a new gate, so it opens with the Chair.

- TMPL-4.3 — At the session's start, settle a plan with the Chair: how a project opts in and names its profile (a profile file read by the gate), and whether the template itself opts in, its scripts being over the limits; where the gate runs (on the commit's staged change through pre-commit, and on the push range in CI); how jscpd, a Node tool, is installed (pre-commit's `node` language or a pinned install); the script and hook names. Then build, in this order:
  1. The language-neutral core: the functions a change adds or edits, found from the diff; the limits of §2; the recall check of §3; the exceptions file `code-exceptions.yaml` of §4, a value never rising; the clone check with jscpd at its defaults, its caps lifted; coverage of the change's new lines.
  2. The Python profile: its function measurer on Python's own `ast`, so no tokenizer can skip a function, and its pinned formatter, linter, type checker, coverage and audit tools, each installed through the hook's own environment and proved by the Python fixture (`match`, nested functions, decorators, a method's `self`).
  3. Fixtures for every rule, each proved against a broken variant.
  4. The gate's sections in `docs/governance/gate_suite_runbook.md`, in the same commit as the hook, with `gate-runbook` passing.
  5. The proof on a scratch copy of Comfy, touching nothing in Comfy itself: a change adding a function over a limit, a clone and an unrecorded exception are each refused, and a compliant change passes.

## 4. Success criteria

- TMPL-4.3: the Python measurer passes its fixture and a broken variant of it fails; every gate rule has a passing and a failing fixture, each failing fixture caught by its broken variant; on the scratch copy of Comfy a change over a limit, a clone and an unrecorded exception are each refused and a compliant change passes; TMPL-4.3 set Done with the tracker's Summary Statistics reconciled in `sprint/story-tracker.md`.
- Every checkpoint: `pre-commit run --all-files` exit 0. The closeout push's `gates` run green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S15 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S16.
It writes and fills the pair for S16, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S15`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S16.md`, whose contents go to the user as the next session's prompt.
