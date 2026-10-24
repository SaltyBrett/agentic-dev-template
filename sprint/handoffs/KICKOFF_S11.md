# Kickoff — S11

**For session:** S11
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S11.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

The two tasks run in this order, the second waiting on the first. TMPL-5.4 needs the Chair at the
keyboard in the probe project; give the Chair commands that work in the session they are in.

- TMPL-5.4 — Complete the live proof carried over from S10, the Chair at the keyboard in the private probe project `SaltyBrett/launch-probe-s10` (clone at `/Users/twdaddy/code/personal/launch-probe-s10`), whose launch stands at the PRD stage with the draft committed (`8f03e4e`) and awaiting approval, intake and team done, the corrected skill, README and `AGENTS.md` copied in (`7c72eba`, `69adefd`). The Chair types `/clear` in the probe session (or opens a new conversation there), then `/project-launch`; approves the PRD; runs `/project-launch skip architecture` with a one-line reason; lets planning write the first epic; runs `/project-launch prd`, changes one requirement and approves it again, then `/project-launch status`, which should show the plan stale; and finishes with the probe's first closeout, `/closeout product-manager <a real brief>`. Read the results from the probe's commits, journal and transcripts, record them in [[reference_launch_live_run]], then set TMPL-5.4 Done.
- TMPL-2.4 — Only if TMPL-5.4 is Done: the `v2.0.0` release and the three projects' adoption, per its row in `sprint/story-tracker.md`. The release skill, `.claude/skills/release/SKILL.md`, is the operator's alone.

## 4. Success criteria

- TMPL-5.4: each remaining step observed live and recorded in [[reference_launch_live_run]]: the PRD approved and stamped; a skip logged with its reason; planning's first epic passing `doc-authority-scan`, with the tracker's `**Source:**` line naming its versions; a revision re-approved and `/project-launch status` reading the plan stale; the probe's first closeout passing `session-closeout` and pushing, with its `gates` run green.
- Every checkpoint: `pre-commit run --all-files` exit 0. The closeout push's `gates` run green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S11 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S12.
It writes and fills the pair for S12, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S11`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S12.md`, whose contents go to the user as the next session's prompt.
