# Handoff — S9

**For session:** S9
**Written by:** S8
**Written:** 2026-10-23

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S9.md`
- `docs/governance/framework_decisions.md` decision 2026-10-23-016 — the doc-queue design TMPL-2.2 builds, settled with the Chair: the queue is the open stories marked `Queued: S<N>`, failing at cold start once older than one session; the drain forks as `general-purpose` in the library technical writer's role, one document each, and leaves its change for review
- `docs/governance/framework_decisions.md` decision 2026-10-22-002 — the doc-queue's origin: `authority:` frontmatter, a version log on each source of truth, `Affects:` on every decision, and a gate that accepts a version-log row or a queued story
- `docs/governance/framework_decisions.md` decision 2026-10-23-008 — the project launch epic: the approval gate TMPL-5.3 builds and the `/project-launch` of TMPL-5.2
- `docs/governance/framework_decisions.md` decision 2026-10-23-014 — what the approval gate reads: an approved PRD or architecture is `status: approved` with the `authority:` line in `docs/prd/` or `docs/architecture/`, the architecture's `prd:` matching the PRD's newest version
- [[reference_doc_authority]] — queued stories, one scope one authority, and in a project what the template wrote is judged in the template (decision 2026-10-23-015), which the doc-queue gate and the approval gate must respect on a birth
- [[reference_claude_code_skills]] — a forked skill sees only the tree and its arguments: the shape of the drain skill
- [[reference_claude_code_hooks]] — how the `SessionStart` hook runs gates and the cap on the context it injects, where the doc-queue's verdict must appear
- `scripts/session_start.py` — the start hook that runs the doc-queue gate at cold start and reports its verdict
- `.claude/rules/gate-scripts.md` — the shape of a gate script and its self-test hook, for the doc-queue gate and the approval gate
- `personas/technical-writer.md` — the role the drain skill's first step reads and takes
- `docs/templates/README.md` — how a PRD or architecture is made and approved: what the approval gate reads, and the steps the scratch-birth proof follows

## 2. Completed last session

- TMPL-5.1 — `docs/templates/prd.md` and `docs/templates/architecture.md`, each the authority for its own scope, with `docs/templates/README.md` for making and approving a document; `docs/governance/doc_control_standard.md` and the root `README.md` name the templates; decision 2026-10-23-014; proved on a scratch birth (e155edf; rows stamped 9a91eff)
- TMPL-2.6 — `scripts/doc_authority_scan.py`: in a project the template's rows and decisions are judged in the template, and a row's commit is found following renames, never a copy; its sections in `docs/governance/gate_suite_runbook.md`; [[reference_doc_authority]]; decision 2026-10-23-015, amending 2026-10-23-010 (e155edf; rows stamped 9a91eff)
- TMPL-5.6 — `personas/backend-engineer.md`, `personas/web-developer.md`, `personas/blender-artist.md`, `personas/image-video-editor.md`; the three presets and the connections as one YAML block in `.claude/skills/team-selection/SKILL.md`; `scripts/skill_scan.py` gained `preset` and `connection`, its section in `docs/governance/gate_suite_runbook.md`; the Blender Lab MCP server pinned to v1.0.3's commit, [[reference_blender_mcp]]; decision 2026-10-23-013 (8180f9e; runbook row stamped b33bbfa)
- TMPL-2.2 — its row in `sprint/story-tracker.md` corrected (8180f9e) and its design settled with the Chair, decision 2026-10-23-016 (8bb20ef); left unbuilt for S9 by the Chair's choice
- TMPL-2.4 — its row in `sprint/story-tracker.md` names the projects' own `sprint/recovery/AUTHORITY_MATRIX.md` (38c549d)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-23-013 TMPL-5.6 as built: `backend-engineer`, `web-developer`, `blender-artist`, `image-video-editor`; the three presets as proposed, Website with `business-writer`; presets and connections one YAML block in team selection, held by `skill-scan`; the connection the Blender Lab server pinned to v1.0.3's commit, the community server rejected
- 2026-10-23-014 The PRD and architecture templates as built: in `docs/templates/`, each the authority for its own scope so a document made from it claims the project's; a made document a draft until approved, when it becomes the authority with its first row citing the approval; the PRD's eleven sections with goals, FR and NFR numbered, the architecture's thirteen ending in the dependency layers
- 2026-10-23-015 In a project the authority gate judges what the template wrote in the template, so a birth from the template starts green; and a row's commit is found following renames but never a copy; amends 2026-10-23-010, whose Date now reads `2026-10-23; amended 2026-10-23`
- 2026-10-23-016 The doc-queue as designed for TMPL-2.2: the writer's queue is the open stories marked `Queued: S<N>`, failing at cold start once older than one session; the drain forks as `general-purpose` in the library technical writer's role, one document each, and leaves its change for the main session to review and commit

## 5. Blockers and open questions

- No blockers.
- Proposed to the Chair at the S8 handover, not decided: a CI job that runs a scratch birth, so a template change that blocks births fails CI. The regression TMPL-2.6 fixed was invisible to CI, which judges only the template.
- Births from the template were refused by `doc-authority-scan` from the S7 closeout push until the S8 closeout push, which carries the fix (decision 2026-10-23-015).
- The Blender connection's uv command was read from the pinned commit's tree and never run; the first operator to activate it runs it first ([[reference_blender_mcp]]).
- Decision 2026-10-23-013's gate design and server choice, 2026-10-23-014's draft-then-authority form and 2026-10-23-015's copy fix were made by the AI within approved decisions, and reported to the Chair at the S8 handover.
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- The scratch probe folder `/Users/twdaddy/code/personal/tmpl-s6-probe` can be deleted by the operator.
- Whether `/project-launch` is the Chair's alone (`disable-model-invocation`) is settled in TMPL-5.2 (decision 2026-10-23-008).
- Decision 2026-10-23-002's second and third bullets stand.
- Decision 2026-10-22-006 stands unless the operator overturns it.
- The three projects keep their own `sprint/recovery/AUTHORITY_MATRIX.md`, theirs to delete (decision 2026-10-23-011); name it to the operator at TMPL-2.4.

## 6. Verification observed

- cold start, run by the `SessionStart` hook: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0
- TMPL-5.1: on a scratch birth from this tree, `doc-authority-scan` exit 0 with the drafts unregistered; a copy that kept the template's line refused as `scope`; approved and stamped with its approval commit, exit 0; a swapped hash refused
- TMPL-2.6: nine fixtures pass; nine broken variants each caught; a scratch birth starts green, the initializer's suite run passing
- TMPL-5.6: eighty-three fixtures pass; twenty-five broken variants each caught, a dead dedent removed when its variant passed; on real trees `skill-scan` refused the connection in the template, a birth wrote no `.mcp.json`, a project refused it without the persona and passed with it
