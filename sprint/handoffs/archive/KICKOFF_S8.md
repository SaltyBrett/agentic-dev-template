# Kickoff — S8

**For session:** S8
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S8.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

The three tasks are independent; the Chair may reorder them.

- TMPL-5.6 — Per decision 2026-10-23-012. First confirm with the Chair the four persona slugs and each preset's membership. Write the four library personas in `personas/` (a backend engineer, a web developer, a Blender 3D artist, an image and video editor) in the agent-file shape with the shared habits of decision 2026-10-23-004. Add the named team presets (Application development, Website, Imaging, video and 3D) to `.claude/skills/team-selection/SKILL.md`. Build a gate that refuses a preset naming a persona the library lacks, with fixtures each proved against a broken variant, and a section in `docs/governance/gate_suite_runbook.md` if it is a hook of its own. Research and vet a community Blender MCP server and its Blender add-on, pin its version, and document the opt-in connection that team-selection offers only when the Blender persona is activated, off by default and never enabled in the template.
- TMPL-5.1 — Per decision 2026-10-23-008. Settle with the Chair the PRD and architecture templates' sections; where the templates live (`docs/prd/` and `docs/architecture/` are project-owned and never written by the updater); and how a template carries the authority frontmatter of decision 2026-10-23-010 without itself becoming an authority whose scope a PRD made from it would also claim (the gate refuses two documents claiming one scope).
- TMPL-2.2 — If time remains. First correct its row in `sprint/story-tracker.md`: "published to `dev-resources`" is moot since decision 2026-10-23-003, and the `technical-writer` persona is already in the library. Then build the doc-queue gate of decision 2026-10-22-002, run by the `SessionStart` hook, and the drain skill, forked per document.

## 4. Success criteria

- TMPL-5.6: the four personas lint clean under `session-closeout-check`; the preset gate's fixtures pass and every broken variant fails at least one without crashing; the Blender connection documented with a pinned version and written to no project that did not choose it.
- TMPL-5.1: the templates, and a PRD and an architecture made from them, pass `doc-authority-scan`.
- TMPL-2.2: the doc-queue fixtures each proved against a broken variant; its runbook section passing `gate-runbook`; the drain skill passing `skill-scan`.
- `pre-commit run --all-files` exit 0 at every checkpoint; the closeout push's `gates` run green, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S8 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S9.
It writes and fills the pair for S9, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S8`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S9.md`, whose contents go to the user as the next session's prompt.
