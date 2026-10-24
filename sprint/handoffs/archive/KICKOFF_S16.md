# Kickoff — S16

**For session:** S16
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S16.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

One task, the agentic development team TMPL-3.1 designed, from decisions 2026-10-24-004, 2026-10-24-005 and 2026-10-24-006 as amended by 2026-10-24-011. It is a new skill and a new gate, so it opens with the Chair.

- TMPL-3.2 — At the session's start, settle a plan with the Chair: whether to split the story, being larger than one session (a standard, a skill, a gate and a live proof), and in what order; which project carries the proof, Comfy being the only one holding a stack profile the gate builds today (Python). Then build, in this order:
  1. `docs/standards/team_standard_v1.0.md` as an authority with its version log: the stages, the five story types' role map, the eleven review triggers with their detection, the security auditor's brief of decision 2026-10-24-009, every finding and the Chair's response in `docs/code_review_log.md`.
  2. The main-session `/story <ID>` skill, never forked since only the main session can ask the Chair: one story end to end through roster subagents handing off through committed artifacts in `docs/stories/<ID>/`, each artifact gated before the next role starts, stopping at a trigger or a gate failing three times running, pausing for the Chair's response to each finding, never forcing a code change.
  3. The `story-artifacts` gate over `docs/stories/`: each artifact's frontmatter, its input passing before the role started, the stage order, the brief's numbered acceptance criteria each mapped in verify, every hit trigger approved by the Chair before release or Done; the trigger paths read from the stack profile's `TRIGGER_PATHS` in `scripts/code_standard.py`.
  4. Fixtures for every rule, each proved against a broken variant.
  5. The gate's sections in `docs/governance/gate_suite_runbook.md`, `AGENTS.md`'s skills table and the README's catalog.
  6. The proof on a scratch copy of one project, touching nothing in the project itself: one story end to end, the Chair at the keyboard for its triggers.

## 4. Success criteria

- `docs/standards/team_standard_v1.0.md` passes `doc-authority-scan`.
- `/story` passes `skill-scan` and is listed in `AGENTS.md`'s skills table and the README's catalog.
- Every `story-artifacts` rule has a passing and a failing fixture, each caught by its broken variant.
- On the scratch copy one story runs from brief to release, each stage's artifact committed and gated, a trigger stopping it until the Chair approved, a finding answered in the code review log.
- TMPL-3.2 set Done, or split into stories and the first done, with the tracker's Summary Statistics reconciled in `sprint/story-tracker.md`.
- Every checkpoint: `pre-commit run --all-files` exit 0. The closeout push's `gates` run green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S16 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S17.
It writes and fills the pair for S17, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S16`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S17.md`, whose contents go to the user as the next session's prompt.
