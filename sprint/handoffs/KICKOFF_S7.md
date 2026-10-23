# Kickoff — S7

**For session:** S7
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S7.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

- TMPL-2.1 — Build `scripts/doc_authority_scan.py` per decision 2026-10-22-002: `authority:` frontmatter and version logs on each source of truth, `Affects:` on decisions, the rule that accepts a version-log row or an open tracker story and nothing else, the fact marker, `--stamp` verified against git, `--history`; a self-test hook placed before the gate, fixtures each proved against a broken variant; its section in `docs/governance/gate_suite_runbook.md`; the decisions the build settles logged.
- TMPL-2.5 — The updater merges `.gitignore` by union per decision 2026-10-23-007: `git merge-file --union` for that path alone, named in the dry run; fixtures proved against broken variants; a scratch adoption of clones of the three projects (Supplier_Research_Dev, Comfy, PocketGames, read-only, cloned into the scratchpad) with no `.gitignore` conflict.
- TMPL-5.1 — Only if TMPL-2.1 is Done: the PRD and architecture templates per decision 2026-10-23-008, their frontmatter in the `authority:` format TMPL-2.1 settles. The Chair may choose TMPL-2.3 instead.

## 4. Success criteria

- TMPL-2.1: every fixture passes and every broken variant fails at least one fixture without crashing; the gate run on the real tree and its findings recorded as seen; `gate-runbook` passes with the new section.
- TMPL-2.5: every broken variant caught; the three scratch adoptions report no `.gitignore` conflict and the suite passes.
- TMPL-5.1, if taken: the templates pass the gate TMPL-2.1 built.
- `pre-commit run --all-files` exit 0 at every checkpoint; the closeout push's `gates` run green, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S7 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S8.
It writes and fills the pair for S8, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S7`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S8.md`, whose contents go to the user as the next session's prompt.
