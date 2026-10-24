# Kickoff — S12

**For session:** S12
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S12.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

One task, a design session with the Chair; design only, no build.

- TMPL-3.1 — The design session with the Chair over the persona library's team. For each role in the library (designed in TMPL-1.9, decision 2026-10-23-004), the artifact it produces and the gate that judges it; the review-trigger list, the points at which work stops for the operator; the orchestration shape, roles handing off through gated artifacts in the repository rather than conversation (decision 2026-10-22-003), bounded by what a forked skill can do ([[reference_claude_code_skills]]). Log each settled point as a decision in `docs/governance/framework_decisions.md`, and scope TMPL-3.2's build by them, leaving room for TMPL-4.1's reviewer.

## 4. Success criteria

- TMPL-3.1: every library role in `personas/` named with its artifact and its judging gate in a logged decision; the review-trigger list and the orchestration shape each logged; TMPL-3.1 set Done in `sprint/story-tracker.md` with the Summary Statistics reconciled.
- Every checkpoint: `pre-commit run --all-files` exit 0. The closeout push's `gates` run green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S12 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S13.
It writes and fills the pair for S13, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S12`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S13.md`, whose contents go to the user as the next session's prompt.
