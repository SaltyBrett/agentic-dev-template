# Kickoff — S13

**For session:** S13
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S13.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

One task, the coding standard's design session with a specialized reviewer agent; design and proof only, the build left to TMPL-4.2.

- TMPL-4.1 — At the session's start, the Chair chooses the known-good and the known-bad codebase, the three projects and the template's own scripts being candidates; their code stays out of the session context beyond what the reviewer must read. Then design decision 2026-10-22-003's three layers: the core limits as numbers (function and file length, complexity ceilings, duplication, a coverage floor, the formatter, linter, type checks and dependency audit), each proved against both codebases before it is logged, since this standard is the hardest thing in the framework to unwind; the rule by which every stack maps each limit to a tool, chosen per project at its planning session; and the one judgement page under `.claude/rules/`, path-scoped to code and opening with `CONSTITUTION.md` §4A, bounded by how a path-scoped rule loads and fails silently ([[reference_claude_code_rules]]). Since decision 2026-10-24-006 leaves the code reviewer's slot to TMPL-4.1, design the reviewer's brief (structure and duplication, never the implementer) and the security auditor's, beside `personas/qa-engineer.md` and `personas/security-engineer.md`. Log each settled point as a decision in `docs/governance/framework_decisions.md`.

## 4. Success criteria

- TMPL-4.1: every core limit logged as a number with its evidence, the known-good codebase passing and the known-bad failing it; the per-stack mapping rule and the judgement page's content logged; the reviewer's and the auditor's briefs logged, ready for TMPL-4.2 to draft as library personas; TMPL-4.1 set Done in `sprint/story-tracker.md` with the Summary Statistics reconciled.
- Every checkpoint: `pre-commit run --all-files` exit 0. The closeout push's `gates` run green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S13 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S14.
It writes and fills the pair for S14, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S13`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S14.md`, whose contents go to the user as the next session's prompt.
