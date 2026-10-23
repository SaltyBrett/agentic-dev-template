# Kickoff — S3

**For session:** S3
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

You are a senior platform engineer and scrum master who builds governance tooling for AI-assisted
development: Python gate scripts with self-tests, pre-commit hook suites, git workflows, and
markdown-based state management. You treat a written rule as a non-control until a script enforces
it. You run fixtures against broken code before trusting them. You keep every document lean and give
each fact one home. You never call work done before its executable check has run and passed, and you
report failures exactly as observed.

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S3.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

- TMPL-1.3 — Personas become subagents in `.claude/agents/<slug>.md`. Before writing anything, download `https://code.claude.com/docs/en/sub-agents.md` with curl and read it whole (WebFetch summarizes only the first 100 K characters of a long page): the frontmatter fields, what a subagent loads at start (some start without project instructions, `AGENTS.md` included), how `claude --agent <name>` runs the main session as the agent, and the `agent_type` a `SessionStart` hook then receives. Map a persona onto an agent file so the Invocation is the agent's prompt and `version:`, the Changelog, Expertise and Insists on survive, keeping the append-only rule of decision 2026-09-23-006 against the committed copy. Repoint `persona-lint` (`session_closeout.py --personas`) and the owned paths of `resources_sync.py`; the kickoff names the agent instead of copying its Invocation, and the kickoff lint changes with it without refusing `KICKOFF_S3.md`, written under the old rule. Move the registry in `dev-resources` as well, ordered so that neither repository's gates go red between the two pushes, since `dev-resources` pins `persona-lint` by rev. Log the decision the move needs.
- TMPL-1.5 — Path-scoped rules under `.claude/rules/`: read the rules section of `https://code.claude.com/docs/en/memory.md` for the `paths:` frontmatter and when a rule loads. Move judgement that applies only when certain files are touched (gate scripts and their fixtures, knowledge entries and their frontmatter, the sprint documents) out of always-loaded text into rules, never restating `AGENTS.md`. `CONSTITUTION.md` §6.3 becomes a pointer to its knowledge entry; §2 and the checklist were already reduced by TMPL-1.1, so record them in the story row as done there.

## 4. Success criteria

- TMPL-1.3: `claude --agent framework-maintainer -p` in a scratch clone answers in the persona and its `SessionStart` input carries `agent_type`, observed, not assumed; `persona-lint` passes on the new location and refuses an Invocation changed without a version bump, by fixture and by a live probe; every broken variant of the changed linters fails at least one fixture; `resources_sync.py` reports every agent up to date after the `dev-resources` move, and that repository's `gates` run is green
- TMPL-1.5: a rule loads only when a file its `paths:` match is read, observed in a scratch session with a canary; `CONSTITUTION.md` §6.3 is a pointer and `kb-freshness-scan` exits 0; no rule repeats a sentence of `AGENTS.md`
- `pre-commit run --all-files` exit 0 at every checkpoint; the closeout push's `gates` run green, observed with `gh run watch --exit-status`

## 5. Closeout

Before ending: add a `## S3 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
flush durable learnings to `docs/orchestration/knowledge/` with an INDEX row, log decisions, update
the tracker, sync the registry (`python3 scripts/resources_sync.py --apply`, publishing what it
reports), then run `python3 scripts/session_closeout.py --scaffold --persona <slug>`, fill both
files for S4, run `pre-commit run session-closeout --hook-stage manual --all-files`, commit `checkpoint: closeout S3`, push, confirm
the `gates` run on GitHub is green, and hand the user the contents of `KICKOFF_S4.md` as the
next session's prompt.
