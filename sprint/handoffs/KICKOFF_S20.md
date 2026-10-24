# Kickoff — S20

**For session:** S20
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S20.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

This session builds the writing standard's gate, from the law S19 wrote and decisions
2026-10-24-016 to 2026-10-24-025. Write every new file in ASCII, with headings of 8 words or fewer
and no comma, since the gate judges them.

- TMPL-6.3, the plan first: settle with the Chair the writing gate's design where the standard leaves room, and build nothing until it is settled. That covers how `scripts/writing_standard.py` reads the standard's tables (the character table `Code points | Characters | Replace with` in section 5; `### AI phrases` and `### Marketing phrases`, each `Phrase | Where`, in section 7); the profile reader (`rules`, the `template:` list applied ahead of `rules` only where `.project-profile` is absent per decision 2026-10-24-025, `default`, `agents`, `allow`); the voices' frontmatter (`name`, `tables`) and a custom voice's `## Sample` counted at 200 words or more; the allow-list match (the flagged text inside an occurrence of an allowed string in the same file); `--which <path>`; the text mode for a produced file; and whether the gate refuses a profile glob that matches nothing, given that five of the starter's (`docs/prd/**`, `docs/architecture/**`, `docs/stories/**`, `docs/code_review_log.md`, `evidence/**`) are project paths that match nothing in the template by design.
- TMPL-6.3, the build, per its tracker row: every tracked markdown file judged whole for characters, headings with the label rule, phrases (outside code spans and code blocks, whitespace matching across line breaks, `list end` at the close of a sentence, paragraph or list item) and development references in production files; exit 0, 1 or 2, each finding printing its fix and the allow-list line; `--self-test` with each rule's fixtures proved against a deliberately broken copy.
- TMPL-6.3, the hooks: `writing-standard-selftest` and `writing-standard`, the gate at the manual stage until TMPL-6.6, with their sections and a version-log row in `docs/governance/gate_suite_runbook.md`; its run on the real tree reporting the sweep's size by rule.
- TMPL-6.3, the updater: `template_update.py` proved on a scratch copy to leave a project's custom voice alone and merge the profile three-way.
- TMPL-6.3, the skill: `.claude/skills/document-production/SKILL.md`'s check step naming the text mode (2026-10-24-022).

## 4. Success criteria

- `pre-commit run writing-standard-selftest --all-files` exit 0, with each rule's fixture seen failing against a broken copy.
- `pre-commit run writing-standard --hook-stage manual --all-files --verbose` run on the real tree, its exit code and finding counts by rule recorded in the S20 entry; it is expected to fail until the TMPL-6.6 sweep.
- The files S19 wrote (`docs/standards/writing_standard_v1.0.md`, `docs/standards/voices/*.md`, `.claude/rules/writing.md`) pass the gate, apart from the U+2014 changelog lines of `personas/editor.md` and `personas/document-reviewer.md`, which TMPL-6.4 moves.
- `--which README.md` gives development in the template and production with a `.project-profile` present, as a fixture.
- The updater proof observed and recorded.
- `gate-runbook`, `skill-scan` and `doc-authority-scan` green, the runbook's row stamped.
- TMPL-6.3 Done in `sprint/story-tracker.md`, with the Summary Statistics recounted.
- Every checkpoint: `pre-commit run --all-files` exit 0.
- The closeout push's `gates` run is green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S20 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S21.
It writes and fills the pair for S21, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S20`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S21.md`, whose contents go to the user as the next session's prompt.
