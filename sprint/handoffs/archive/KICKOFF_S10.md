# Kickoff — S10

**For session:** S10
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S10.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

The three tasks run in this order, each waiting on the one before. TMPL-5.4 needs the Chair at the
keyboard for the whole run, so the Chair schedules it at the start of the session.

- TMPL-5.5 — Build per decision 2026-10-23-009. Make the root `README.md` the operator's front page: a step-by-step walkthrough from creating a project through `/project-launch`, the session loop and taking a release, then a catalog of every command (every skill under `.claude/skills/`, `/project-launch` and `/doc-drain` among them), every operator script (`scripts/birth_probe.py` among them) and every session hook, with the gates linked to `docs/governance/gate_suite_runbook.md`. Cut `TEMPLATE_GUIDE.md` to what the initializer does not do. Make `skill-scan` (`scripts/skill_scan.py`) refuse a skill the catalog does not name, and have its runbook section say so; that section records decision 2026-10-23-009's change, queued in TMPL-5.5 since TMPL-2.3.
- TMPL-5.4 — Once TMPL-5.5 is Done: a scratch birth and one live session with the Chair at the keyboard through every stage of `/project-launch`, with a pause, a skip and a return to revise an approved document, following the README's walkthrough as written. Record the observations as seen.
- TMPL-2.4 — Only if TMPL-5.4 is Done: the `v2.0.0` release and the three projects' adoption, per its row in `sprint/story-tracker.md`. The release skill, `.claude/skills/release/SKILL.md`, is the operator's alone.

## 4. Success criteria

- TMPL-5.5: each fixture of the catalog rule proved against a broken variant; the `skill-scan` runbook section passing `gate-runbook`, its version-log row citing decision 2026-10-23-009 and TMPL-5.5; every command in the walkthrough run on a scratch birth; `python3 scripts/birth_probe.py` exit 0 under both profiles.
- TMPL-5.4: each stage's state as `/project-launch status` reports it, observed live, and the observations recorded in a knowledge entry.
- Every checkpoint: `pre-commit run --all-files` exit 0. The closeout push's `gates` run green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S10 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S11.
It writes and fills the pair for S11, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S10`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S11.md`, whose contents go to the user as the next session's prompt.
