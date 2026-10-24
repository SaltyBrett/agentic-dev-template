# Kickoff — S18

**For session:** S18
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S18.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

This is the writing standard's design session with the Chair, from decision 2026-10-24-014. It
opens with the Chair and builds nothing until the decisions are logged. Its input is the Chair's ask
at S17, set out in `sprint/handoffs/HANDOFF_S18.md` section 5. Agents' writing shows obvious
machine tells, and the prose rules a session reads at its cold start are imprecise and enforce
nothing. The model is Grammarly's Humanizer: a voice chosen from built-in ones, or made from a
sample of the writer's own writing at least 200 words long, with flagged passages rewritten in that
voice. The Chair wants it in the repository, with a writing style that can be assigned to an agent
and guardrails that are enforced.

- TMPL-6.1: settle the design with the Chair, one question at a time, logging each answer as a decision with `**Affects:**` in `docs/governance/framework_decisions.md` before asking the next:
  1. The built-in voices, and how a custom voice is captured from the Chair's sample and stored.
  2. How a voice and an audience (production or development) are assigned: to a document by its path, in a profile like `code-profile.yaml`, and to an agent or persona.
  3. The first guardrail lists, and which of them are mechanical and which are judgement. Mechanical candidates: characters, heading shape, phrase lists per voice, and development references by audience. Judgement: tone, for the `editor` persona and a path-scoped `.claude/rules/` page.
  4. Whether the template's own documents are judged, given that its sprint documents and decisions use em dashes throughout.
  5. The enforcement model: a refusal, or a pause until the Chair answers in a log, as decision 2026-10-24-011 has code do.
  6. The humanizer skill's flow: scan, rewrite in the assigned voice, and show the Chair the diff before anything is kept.
  7. Where the em-dash rule of `docs/standards/document_production_standard_v1.0.md` §9 goes.
- TMPL-6.2 and TMPL-6.3: re-cut both stories in `sprint/story-tracker.md` to the logged design, each with its Required Standards.

## 4. Success criteria

- Every design question in task TMPL-6.1 is answered by the Chair and logged as a decision with `**Affects:**`.
- TMPL-6.2 and TMPL-6.3 are re-cut to the design in `sprint/story-tracker.md`, each with its Required Standards.
- Every checkpoint: `pre-commit run --all-files` exit 0.
- The closeout push's `gates` run is green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S18 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S19.
It writes and fills the pair for S19, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S18`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S19.md`, whose contents go to the user as the next session's prompt.
