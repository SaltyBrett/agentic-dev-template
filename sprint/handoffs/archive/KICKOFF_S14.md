# Kickoff — S14

**For session:** S14
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S14.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

One task, the coding standard's build from decisions 2026-10-24-007 to -009; it is larger than one session, so it opens with the Chair.

- TMPL-4.2 — At the session's start, settle with the Chair: whether to split TMPL-4.2 into stories and in what order; which project carries the proof, PocketGames (Rust) or Comfy (Python); and whether to install the Rust toolchain on the operator's machine (`cargo` is missing) or prove Rust in CI only. Then build, in this order:
  1. `docs/standards/coding_standard_v1.0.md`, declared as an authority with its version log (`docs/governance/doc_control_standard.md`): the core limits, the scope of changed code, the exception categories and the exceptions file, the mapping rule.
  2. A stack profile each for Rust, Python and TypeScript, naming one pinned tool per slot (function measurer, clone detector, formatter, linter, type checker, coverage, dependency and license audit, the trigger paths of decision 2026-10-24-005), each measurer proved by its language's measurement fixture (Rust lifetimes and raw strings, a TypeScript method with a return type and a bare catch, Python `match`) and by the recall check the gate runs every time ([[reference_coding_standard_calibration]]).
  3. The gate over the functions a change adds or edits: complexity 15, 60 code lines, 5 parameters; tests at 10 and 100; no new clones at jscpd's defaults with its caps lifted; 80% of new lines covered; the exceptions file never growing; a growing file past 500 lines reported to the reviewer. Built to `.claude/rules/gate-scripts.md`, with fixtures proved against broken variants and its runbook sections.
  4. `.claude/rules/code-quality.md`, path-scoped to code and opening with `CONSTITUTION.md` §4A ([[reference_claude_code_rules]]).
  5. `personas/code-reviewer.md` from decision 2026-10-24-009's brief.
  6. The proof on a scratch copy of the chosen project.

## 4. Success criteria

- TMPL-4.2: every measurer passes its fixture and a broken variant of each fails it; the gate's fixtures pass and each broken variant is caught; on a scratch copy of the chosen project a change adding a function over a limit, or a clone, is refused and a compliant change passes; the standard passes `doc-authority-scan`, the page the rule gate, the persona the persona lint; TMPL-4.2 set Done, or split into stories and the first done, with the tracker's Summary Statistics reconciled in `sprint/story-tracker.md`.
- Every checkpoint: `pre-commit run --all-files` exit 0. The closeout push's `gates` run green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S14 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S15.
It writes and fills the pair for S15, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S14`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S15.md`, whose contents go to the user as the next session's prompt.
