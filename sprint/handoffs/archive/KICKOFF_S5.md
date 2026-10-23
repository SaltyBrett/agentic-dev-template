# Kickoff — S5

**For session:** S5
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S5.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

- TMPL-1.8 — First put decision 2026-10-23-003's four open questions to the operator and log the answers. Then build the persona library: the library's folder in the template, inactive; `.claude/agents/` as the project's roster; the first-session skill that asks which specializations the project needs, recommends from the library, drafts what it lacks and activates the chosen; the closeout's persona rule and the library-version check; the sync, the initializer, the updater and the sanitizer following the answers; the supersessions marked on both sides and every teaching entry corrected.
- TMPL-1.7 — After TMPL-1.8: prove the substrate end to end: a scratch birth from the current template (`new_project.py --apply`, suite green, `session-verify` at S1, the `.claude/` tree as decided); the first-session skill building the roster; an interactive cold start in that fresh clone with the operator at the trust dialog, the SessionStart report observed; a `/compact` in a live session and the compact re-injection observed; the forked `/closeout` run end to end on the scratch project; then a knowledge entry for the substrate with its INDEX row.

## 4. Success criteria

- TMPL-1.8: the answers logged before any build; the library ships no file in `.claude/agents/`, observed in a scratch birth's agent list; the first-session skill passes `skill-scan`; every changed gate's fixtures fail against at least one broken variant; `kb-freshness-scan` passes with the supersessions marked on both sides.
- TMPL-1.7: each observation recorded with what was seen (output or journal lines), not assumed; the substrate entry passes `kb-frontmatter-scan` and `kb-freshness-scan`.
- `pre-commit run --all-files` exit 0 at every checkpoint; the closeout push's `gates` run green, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S5 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S6.
It syncs the registry, writes and fills the pair for S6, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S5`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S6.md`, whose contents go to the user as the next session's prompt.
