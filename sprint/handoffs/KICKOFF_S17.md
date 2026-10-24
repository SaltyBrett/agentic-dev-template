# Kickoff — S17

**For session:** S17
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S17.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

One task, the agentic development team's orchestration, from decisions 2026-10-24-004, 2026-10-24-011, 2026-10-24-012 and 2026-10-24-013 under `docs/standards/team_standard_v1.0.md`. It is a new skill and a live proof, so it opens with the Chair: settle the plan, and the story for the proof is the Chair's to choose or approve.

- TMPL-3.3 — Build the `/story <ID>` skill, then prove it live, in this order:
  1. `.claude/skills/story/SKILL.md`, in the main session and never forked, the Chair's to start (`disable-model-invocation`), following the shape of `.claude/skills/project-launch/SKILL.md`: one story end to end, each stage's role called as a subagent of the roster's agent type, or a general-purpose subagent carrying the persona's prompt where the roster agent cannot be called; each role reading its input artifact and writing its own in `docs/stories/<ID>/` with the frontmatter of the standard's §2.
  2. Before the next role starts: `pre-commit run story-artifacts --all-files` and the stage's own gates run (the coding standard's `code-standard` at the build), and the artifact committed.
  3. Stopping at a review trigger to ask the Chair and recording the approval in `approvals.md`, or when a gate fails three times running; each review and security finding appended to `docs/code_review_log.md` and the story paused for the Chair's response, never a forced code change.
  4. Listed in `AGENTS.md`'s skills table and the README's `## Catalog`, held by `skill-scan`.
  5. The live proof on a scratch copy of Comfy, touching nothing in Comfy: activate the story's roles into its roster with the team-selection skill (`code-reviewer` among them), add a code profile, and run one small software story from brief to release with the Chair answering its triggers in chat.

## 4. Success criteria

- `/story` passes `skill-scan` and is listed in `AGENTS.md`'s skills table and the README's catalog.
- On the scratch copy one story runs from brief to release: each stage's artifact committed and passing `story-artifacts`, the build passing or answering `code-standard`, a trigger stopping it until the Chair approved, a review finding answered in the code review log.
- TMPL-3.3 set Done with the tracker's Summary Statistics reconciled in `sprint/story-tracker.md`.
- Every checkpoint: `pre-commit run --all-files` exit 0. The closeout push's `gates` run green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S17 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S18.
It writes and fills the pair for S18, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S17`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S18.md`, whose contents go to the user as the next session's prompt.
