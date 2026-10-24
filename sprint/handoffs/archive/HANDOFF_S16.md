# Handoff — S16

**For session:** S16
**Written by:** S15
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S16.md`
- `docs/governance/framework_decisions.md` decision 2026-10-24-004 — the orchestration TMPL-3.2 builds: the main-session `/story <ID>` skill running one story end to end, each role a roster subagent handing off through committed artifacts in `docs/stories/<ID>/`, a gate judging each before the next role starts, the law in a new team standard
- `docs/governance/framework_decisions.md` decision 2026-10-24-005 — the eleven review triggers and their detection, from the diff where the change shows it and declared by a role otherwise, every hit trigger approved by the Chair in the story's folder
- `docs/governance/framework_decisions.md` decision 2026-10-24-006 — the role map by the five story types (software, data, document, game, media), each persona's artifact and its judging gate, the verifier and reviewer never the builder
- `docs/governance/framework_decisions.md` decision 2026-10-24-011 — advise and document, amending 006, 007 and 009: findings go to `docs/code_review_log.md` with the Chair's response, a story pausing only until logged, never a forced code change
- `docs/standards/coding_standard_v1.0.md` §4 — the code review log's shape that the story's review and security stages write to
- [[reference_code_review_log]] — why a finding pauses only until it is logged with the Chair's response, and pauses nothing again unless it gets worse
- [[reference_claude_code_skills]] — what a forked skill cannot do, which is why `/story` runs in the main session, the only one that can ask the Chair
- `.claude/skills/project-launch/SKILL.md` — the existing main-session skill whose shape `/story` follows
- `scripts/code_standard.py` — its `TRIGGER_PATHS` in the stack profile, which the `story-artifacts` gate's trigger detection reads

## 2. Completed last session

- TMPL-4.3 — plan settled with the Chair: a project opts in with `code-profile.yaml`, the template does not opt in, coverage by the project's own tests, linter and type findings on changed lines only, the audit on a manifest change and over every pushed range (109a2a6)
- TMPL-4.3 — the Chair's rule logged as decision 2026-10-24-011, amending 2026-10-24-006, -007 and -009: the standard advises and documents and never forces a code change; `docs/standards/coding_standard_v1.0.md` 1.1 (§4 the code review log), `personas/code-reviewer.md` version 2, `.claude/rules/code-quality.md`, `docs/orchestration/knowledge/reference_code_review_log.md` new, `docs/orchestration/knowledge/reference_coding_standard_calibration.md` corrected (109a2a6)
- TMPL-4.3 — done: `scripts/code_standard.py` with its Python measurer on `ast` and the tokenizer's recall check; hooks `code-standard-selftest`, `code-standard` and `code-standard-range` in `.pre-commit-config.yaml`; the CI range step in `.github/workflows/gates.yml`; three sections in `docs/governance/gate_suite_runbook.md`; 59 fixtures, 25 broken variants each caught; proved on a scratch copy of Comfy, staged and over a range; ruff's limit rules off after the proof found C901 duplicating the measurer; S5's entry moved to `sprint/archive/sprint-status_2026.md`; `sprint/story-tracker.md` set Done (109a2a6)
- The coding standard's 1.1 and the runbook's 1.12 version-log rows stamped (57735f9)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-011 The coding standard advises and documents and never forces a code change: a finding pauses a commit or a story only until `docs/code_review_log.md`, append-only, holds it with the Chair's response; the Chair's acknowledgement is the exception, the exceptions file gone; the gate core and its Python profile as built; amends 2026-10-24-006, 2026-10-24-007 and 2026-10-24-009 (their index rows now read `amended 2026-10-24`)

## 5. Blockers and open questions

- No blockers.
- TMPL-3.2 is larger than one session (a standard, a skill, a gate and a live proof), so whether to split it, and in what order, is the Chair's at the session's start.
- Which project carries the proof is the Chair's; Comfy is the only one holding a stack profile the gate builds today (Python).
- The persona `code-reviewer` is in the library at version 2; a project activates it with the team-selection skill.
- The template does not opt in to the coding standard (decision 2026-10-24-011).
- S12 to S15 ran in the S11 conversation at the Chair's request with the Chair remote, every question answered in chat.
- Comfy's S4 was never closed out, so any proof there runs on a scratch copy and touches nothing in Comfy itself ([[reference_v2_adoption]]).
- PocketGames' `main` waits for the project's own release step to fast-forward it to `build/milestone-1` ([[reference_v2_adoption]]).
- Each project's `sprint/recovery/AUTHORITY_MATRIX.md` is its own to delete (decision 2026-10-23-011).
- The Chair deletes the probe repository `SaltyBrett/launch-probe-s10` (`gh repo delete` asks), its clone `/Users/twdaddy/code/personal/launch-probe-s10`, and `/Users/twdaddy/code/personal/tmpl-s6-probe`.
- The library has no general mobile-game engine persona ([[reference_launch_live_run]]).
- The Blender connection's uv command was never run ([[reference_blender_mcp]]).
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- Decision 2026-10-23-002's second and third bullets stand, and decision 2026-10-22-006 stands.

## 6. Verification observed

- cold start, run through `scripts/session_start.py` as `/clear` would run it: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S15"), `doc-queue` exit 0
- `scripts/code_standard.py` fixtures: 59, the gate's numbers held to the standard's §2 and its own functions to the limits; 25 broken variants each caught
- proof on a scratch copy of Comfy: an over-limit function paused the commit and the Chair's log row let it proceed with no code changed; a worse value, a clone, a suppression and untyped, unformatted, untested lines paused it; a compliant change passed; an edited log row was refused; `code-standard-range` passed a compliant range and paused a six-parameter function
- closeout: `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
