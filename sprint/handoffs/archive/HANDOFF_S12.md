# Handoff — S12

**For session:** S12
**Written by:** S11
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S12.md`
- `docs/governance/framework_decisions.md` decision 2026-10-22-003 — `v2.1.0` is the team of role subagents handing off through gated artifacts and the coding standard, each opening with a design session; TMPL-3.1 is the team's
- `docs/governance/framework_decisions.md` decision 2026-10-23-003 — the persona library ships in the template, inactive, and each project activates its roster into `.claude/agents/`; the roles TMPL-3.1 designs live in the library, not in a project
- `docs/governance/framework_decisions.md` decision 2026-10-23-004 — the library's team as designed in TMPL-1.9, the roles across the lifecycle each of which TMPL-3.1 gives an artifact and a judging gate, a code reviewer left to TMPL-4
- `sprint/story-tracker.md` epics TMPL-3 and TMPL-4 — TMPL-3.1's row and what TMPL-3.2 must build; TMPL-4.1's reviewer builds on the roles TMPL-3.1 defines, so the design leaves room for it
- `personas/` — the library as shipped in `v2.0.0`, thirty-nine agent files, the roles the design names one by one
- [[reference_claude_code_skills]] — what a forked skill can and cannot do (no conversation, `general-purpose`, no injected persona), which bounds the orchestration shape
- [[reference_v2_adoption]] — how the three projects stand on `v2.0.0`, the ground TMPL-3.2's proof on one project starts from

## 2. Completed last session

- TMPL-5.4 — done: the third live run with the Chair in `SaltyBrett/launch-probe-s10`, the PRD approved and stamped, `skip architecture` logged, planning's epic LP-1 with its `**Source:**` line passing `doc-authority-scan`, the PRD revised to 1.1 and re-approved with the plan read stale, the probe's first closeout pushed green (run 40063609570); recorded in `docs/orchestration/knowledge/reference_launch_live_run.md` with its `INDEX.md` row; S1's entry archived to `sprint/archive/sprint-status_2026.md`; TMPL-2.9 and TMPL-5.7 opened in `sprint/story-tracker.md` (3b22e75)
- TMPL-2.9 — opened and built: `scripts/doc_authority_scan.py`'s `bare-path` rule refuses an authority's path written bare in `**Affects:**`; `docs/templates/README.md` step 5, `docs/governance/gate_suite_runbook.md`, [[reference_doc_authority]]; decision 2026-10-24-001 (5a7ab47; runbook's 1.10 row stamped e90108d)
- TMPL-5.7 — opened and built: `scripts/session_closeout.py --closeout` refuses an entry headed `emergency checkpoint` or holding `### Next`; `.claude/skills/closeout/SKILL.md`, `.claude/skills/project-launch/SKILL.md`, `AGENTS.md`, `README.md` step 7, `scripts/new_project.py`'s S1 text, `docs/standards/session_handoff_standard_v2.0.md`, `docs/governance/gate_suite_runbook.md`, [[reference_session_closeout]]; decision 2026-10-24-002 (20bc428; runbook's 1.11 and the standard's 2.2 rows stamped dee7385)
- TMPL-2.4 — its open question recorded on the tracker row after the S10 closeout (43648d2), then settled by the Chair: each project's PRD and architecture approved as they stand in its adoption commit, the step named in `TEMPLATE_GUIDE.md` and `.claude/skills/project-launch/SKILL.md`; decision 2026-10-24-003 (2767a8e)
- TMPL-2.4 — `v2.0.0` released by the Chair through `/release`, `scripts/new_project.py` stamped (a159053, tagged MAJOR); the three projects taken to it by the release's updater, approved, stamped, pushed and green: Supplier_Research_Dev (`96993b6`, `9f05e46`), Comfy (`ba0da08`, `13b9f4d`), PocketGames (`5089cf5`, `3fbc6e3` on `build/milestone-1`); recorded in `docs/orchestration/knowledge/reference_v2_adoption.md` with its `INDEX.md` row (6b8ec56)
- TMPL-2.4 — done: `dev-resources` given a retirement notice (`4e062ea` in that repository) and archived read-only; `docs/orchestration/knowledge/reference_resources_sync.md`, `reference_v2_adoption.md`, `scripts/session_closeout.py`, tracker set Done (217437e)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-001 `doc-authority-scan` refuses an authority's path written outside a code span in `**Affects:**`, which it never reads there, and `docs/templates/README.md` step 5 says the path goes in a code span; found by the live launch, whose PRD approval named the PRD bare and passed unchecked
- 2026-10-24-002 `session-closeout` refuses to close a session whose entry is still headed `emergency checkpoint` or holds the initializer's `### Next`, a record saying the session is still open; the closeout and launch skills, `AGENTS.md`'s emergency close, the README's step 7 and the initializer's S1 text say so
- 2026-10-24-003 At adoption of `v2.0.0`, a project with real epics approves the PRD and architecture it has been built from as they stand, in the adoption commit; with no architecture, the Chair's skip; settles TMPL-2.4's open question

## 5. Blockers and open questions

- No blockers.
- TMPL-3.1 is design only, no build: each settled point is logged as a decision in `docs/governance/framework_decisions.md`, and TMPL-3.2's build is scoped by them.
- Comfy's S4 was never closed out, so its next Comfy session completes that closeout before building ([[reference_v2_adoption]]).
- PocketGames' `main` waits for the project's own release step to fast-forward it to `build/milestone-1`, which carries the adoption ([[reference_v2_adoption]]).
- Each project's `sprint/recovery/AUTHORITY_MATRIX.md` is its own to delete (decision 2026-10-23-011), named to the Chair at S11.
- The Chair deletes the probe repository `SaltyBrett/launch-probe-s10` (`gh repo delete` asks), its clone `/Users/twdaddy/code/personal/launch-probe-s10`, and `/Users/twdaddy/code/personal/tmpl-s6-probe`.
- The library has no general mobile-game engine persona: `game-engine-developer` is Rust/Bevy only ([[reference_launch_live_run]]).
- The Blender connection's uv command was read from the pinned commit and never run; the first operator to activate it runs it first ([[reference_blender_mcp]]).
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- Decision 2026-10-23-002's second and third bullets stand, and decision 2026-10-22-006 stands.

## 6. Verification observed

- cold start, run through `scripts/session_start.py`: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0, `doc-queue` exit 0
- TMPL-5.4: in the probe, `doc-authority-scan` on epic LP-1 exit 0; the probe's first closeout passed `session-closeout`, run 40063609570 green on `gates` and both `birth` jobs; the probe's `session-verify` after it exit 0, "This is S2"
- TMPL-2.9: seven fixtures pass, five broken variants each caught, the real tree passing
- TMPL-5.7: nine fixtures pass, seven broken variants each caught; a scratch clone of the real tree refused by `--closeout` alone
- TMPL-2.4: a scratch `v2.0.0` cut from `dee7385`, each project's clone adopted with no conflict, refused only by the two `approval` lines, then green with the as-is approval, before and after the stamp; runs 40066350212 (`main`) and 40066356871 (the tag) green on `gates` and both `birth` jobs; project runs 40066882658, 40066960006 and 40067080070 green; `dev-resources` run 40067296277 green
- closeout: `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
