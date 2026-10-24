# Kickoff — S9

**For session:** S9
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S9.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

The four tasks are independent, their dependencies all Done; the Chair may reorder them, and first
places TMPL-2.7 against TMPL-2.2.

- TMPL-2.7 — Build per decision 2026-10-23-017. `scripts/birth_probe.py` makes a scratch project from a committed revision (`HEAD` unless named) through `scripts/new_project.py --apply` with a profile, its verdict the initializer's own suite run. `.github/workflows/gates.yml` runs it on every push and pull request once per profile (`commercial`, `gcc`), skipped where `.project-profile` exists. [[reference_ci_backstop]] says why.
- TMPL-2.2 — Build per decision 2026-10-23-016. The `doc-queue` gate, a manual-stage hook run at cold start by the `SessionStart` hook (`scripts/session_start.py`), over the open stories whose row carries `Queued: S<N>`, failing at a session later than S<N+1>. Its section in `docs/governance/gate_suite_runbook.md`, an authority, so its version-log row cites the story. The drain skill under `.claude/skills/`, forked as `general-purpose`: its first step reads `personas/technical-writer.md` and takes that role; one document per invocation, every queued change to it in one pass; it adds the version-log row citing the story, sets the story Done with the counts, runs the gates, returns the rows it wrote and leaves the change uncommitted for the main session to review. List the skill in `AGENTS.md`.
- TMPL-5.3 — The approval gate of decision 2026-10-23-008. In a project, a real (non-`[EXAMPLE]`) epic needs an approved PRD and an approved architecture, read as decision 2026-10-23-014 defines them (`status: approved` with the `authority:` line in `docs/prd/` and `docs/architecture/`, the architecture's `prd:` matching the PRD's newest version), or a logged skip of either. First settle with the Chair how a skip is logged. Fixtures each proved against a broken variant; a section in `docs/governance/gate_suite_runbook.md` if it is a hook of its own.
- TMPL-5.2 — If time remains. `/project-launch`; first settle with the Chair whether it is the Chair's alone (`disable-model-invocation`).

## 4. Success criteria

- TMPL-2.7: the probe fails at `38c549d`, the S7 tree, for the defect TMPL-2.6 fixed, and passes at its own commit, for both profiles; the new CI step observed green with `gh run watch --exit-status`.
- TMPL-2.2: the doc-queue fixtures each proved against a broken variant; its runbook section passing `gate-runbook`; the drain skill passing `skill-scan`; the gate's verdict seen in the cold-start report.
- TMPL-5.3: the fixtures pass and every broken variant fails at least one without crashing; on a scratch birth, a real epic refused without approved documents, and passing with documents made and approved by `docs/templates/README.md`.
- `pre-commit run --all-files` exit 0 at every checkpoint; the closeout push's `gates` run green, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S9 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S10.
It writes and fills the pair for S10, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S9`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S10.md`, whose contents go to the user as the next session's prompt.
