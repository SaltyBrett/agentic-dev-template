# Kickoff — S6

**For session:** S6
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S6.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

- TMPL-1.10 — Adoption from `v1.0.0`: `scripts/template_update.py` converts a project's `docs/personas/` into agent files in `.claude/agents/` (`name` = slug, `description`, `version`, `expertise`, `insists_on` and `changelog` as YAML lists of strings, body = the Invocation) and removes the old folder; it settles the knowledge entries the project synced from `dev-resources` (marked `source: dev-resources`) and its `.resources-version` stamp. Prove it against the real `v1.0.0` persona files (`git show v1.0.0:docs/personas/<slug>.md`), whose conversion by hand under decision 2026-10-22-005 is the library copy now in `personas/`; fixtures proved against broken variants; the decision logged.
- TMPL-1.7 — After TMPL-1.10: prove the substrate end to end: a scratch birth (`new_project.py --apply`, suite green, `session-verify` at S1, the roster empty and the library whole); the team-selection skill building the roster; an interactive cold start in that fresh clone with the operator at the trust dialog, the SessionStart report observed; a `/compact` in a live session and the compact re-injection observed; the forked `/closeout` run end to end on the scratch project; then a knowledge entry for the substrate with its INDEX row.

## 4. Success criteria

- TMPL-1.10: each real `v1.0.0` persona converts to a file that passes the persona lint and equals its library copy at the same version (frontmatter parsed equal, body equal); a project's own unpublished persona converts and lints; every broken variant of the converter fails at least one fixture; the decision logged.
- TMPL-1.7: each observation recorded with what was seen (output or journal lines), not assumed; the substrate entry passes `kb-frontmatter-scan` and `kb-freshness-scan`.
- `pre-commit run --all-files` exit 0 at every checkpoint; the closeout push's `gates` run green, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S6 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S7.
It writes and fills the pair for S7, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S6`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S7.md`, whose contents go to the user as the next session's prompt.
