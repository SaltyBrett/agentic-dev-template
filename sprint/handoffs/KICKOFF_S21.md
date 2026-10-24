# Kickoff — S21

**For session:** S21
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S21.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

This session opens with TMPL-6.4, the Chair's choice at S20's close; TMPL-6.5 follows it, then
TMPL-6.6, which needs both.

- TMPL-6.4, the plan first: settle with the Chair, and build nothing until it is settled, (a) whether a persona's punctuation-only changelog change (U+2014 to a hyphen) is a new version or a normalized compare, since the persona gate holds a changelog append-only by version (decision 2026-10-24-019); (b) the exact ASCII form of each format the gates read: the sprint-status entry heading `## S<N> - YYYY-MM-DD - <title>`, the handoff and kickoff headings the scaffold writes, a persona's changelog lines, and the tracker's `## Epic: <ID> - <title>`; (c) whether the template's existing lines in the old form move now or in TMPL-6.6's sweep. Find every file that names a format with `git grep -n` on U+2014 near `S<N>`, `Handoff`, `Kickoff`, `Epic:` and the changelog form, the closeout skill, `.claude/rules/sprint-documents.md` and the sprint-status header among them.
- TMPL-6.4, the build, per its tracker row: `scripts/session_closeout.py`, `scripts/sanitize_template.py`, `scripts/new_project.py` and the persona linter write the hyphen form and read both forms, since `template_update.py` never writes a project's `sprint/`; each parser's fixtures proved against a deliberately broken copy; `docs/standards/session_handoff_standard_v2.0.md` and `docs/standards/sprint_management_standard_v1.0.md` say so, each with a version-log row; the S21 entry headed in the new form. The writing gate's label rule already reads both forms (S20, decision 2026-10-24-026).

## 4. Success criteria

- Every parser that reads a format accepts the hyphen and the U+2014 form, each fixture seen failing against a broken copy; `pre-commit run session-closeout-selftest --all-files` exit 0, and the persona lint, which `pre-commit run session-closeout-check --all-files` runs, exit 0.
- A pair written by `python3 scripts/session_closeout.py --scaffold` and a project born by `python3 scripts/birth_probe.py` hold no U+2014 in the formats, and both births are green.
- `pre-commit run writing-standard --hook-stage manual --all-files --verbose` run again, its exit code and finding counts by rule recorded in the S21 entry against S20's 1379 (characters 1190, headings 189).
- TMPL-6.4 Done in `sprint/story-tracker.md`, with the Summary Statistics recounted.
- Every checkpoint: `pre-commit run --all-files` exit 0.
- The closeout push's `gates` run is green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S21 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S22.
It writes and fills the pair for S22, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S21`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S22.md`, whose contents go to the user as the next session's prompt.
