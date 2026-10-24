# Handoff — S17

**For session:** S17
**Written by:** S16
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S17.md`
- `docs/standards/team_standard_v1.0.md`, every section — the law `/story` follows: how a story runs, the artifacts in `docs/stories/<ID>/` and their frontmatter (§2), the role map by story type, the eleven triggers and the Chair's approvals, findings in the code review log, the security audit
- [[reference_story_artifacts]] — what the `story-artifacts` gate holds and when it judges triggers and findings, so the skill commits each artifact in the order the gate accepts
- `docs/governance/framework_decisions.md` decision 2026-10-24-004 — the orchestration: a main-session skill running one story end to end over gated, committed artifacts
- `docs/governance/framework_decisions.md` decision 2026-10-24-011 — advise and document: a finding pauses the story only until `docs/code_review_log.md` holds it with the Chair's response, never a forced code change
- `docs/governance/framework_decisions.md` decision 2026-10-24-013 — the team standard and the `story-artifacts` gate as built, the artifacts the skill writes and the gate judges
- [[reference_claude_code_skills]] — why `/story` runs in the main session and never forked, and what `disable-model-invocation` does to make it the Chair's to start
- `.claude/skills/project-launch/SKILL.md` — the main-session skill whose shape `/story` follows
- [[reference_code_review_log]] — the log the review and security stages append to, and why a logged finding pauses nothing again unless it gets worse

## 2. Completed last session

- Decision 2026-10-24-012, the Chair's: Rust the default language and Bevy the default game engine, the launch's architecture stage proposing them first (`.claude/skills/project-launch/SKILL.md`); the Rust profile, supporting Bevy cleanly, required for `v2.1.0`, TMPL-4.4 carrying the Bevy requirement and TMPL-4.6, the release, waiting on it; TMPL-3.2 split and TMPL-3.3 opened in `sprint/story-tracker.md`; S6's entry moved to `sprint/archive/sprint-status_2026.md` (eb2ba63)
- TMPL-3.2 — done (decision 2026-10-24-013): `docs/standards/team_standard_v1.0.md` written as an authority; `scripts/story_artifacts.py`, reading the role map and the triggers from the standard itself; hooks `story-artifacts-selftest` and `story-artifacts` in `.pre-commit-config.yaml`; two sections in `docs/governance/gate_suite_runbook.md`; `AGENTS.md` and `README.md` name the standard; `docs/orchestration/knowledge/reference_story_artifacts.md` with its `INDEX.md` row; 38 fixtures, 27 broken variants each caught by its own fixture; `sprint/story-tracker.md` set Done (a2d1a78)
- The team standard's 1.0 and the runbook's 1.13 version-log rows stamped (983dbce)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-012 Rust is the Chair's default language and Bevy the default game engine: the launch's architecture stage proposes them first; the coding standard's Rust profile, supporting Bevy cleanly, is required for `v2.1.0`, its release a story of its own; TMPL-3.2 split into the team standard with its gate and the `/story` skill with the live proof
- 2026-10-24-013 The team standard and the `story-artifacts` gate as built: the artifacts' frontmatter and bodies, the role map and the triggers read by the gate from the standard itself, the release always a trigger, a review or security finding answered in the code review log before the story moves on

## 5. Blockers and open questions

- No blockers.
- Roster agents load only in a session opened in the project, so a proof run from the template's conversation calls each role as a general-purpose subagent carrying its persona's prompt (decision 2026-10-24-012); that proves the procedure and the gates, not Claude Code's roster wiring. A real run in a session opened in the project is the stronger proof, the Chair's to schedule.
- The story for the proof is the Chair's to choose or approve.
- Rust and Bevy are the Chair's default stack (decision 2026-10-24-012); TMPL-4.4, the Rust profile supporting Bevy, is required for `v2.1.0`, its Bevy design (a system's many parameters, the clippy lints Bevy projects allow) settled with the Chair at its start.
- S12 to S16 ran in the S11 conversation at the Chair's request with the Chair remote, every question answered in chat.
- Comfy's S4 was never closed out, so the proof runs on a scratch copy and touches nothing in Comfy ([[reference_v2_adoption]]).
- PocketGames' `main` waits for the project's own release step to fast-forward it to `build/milestone-1` ([[reference_v2_adoption]]).
- Each project's `sprint/recovery/AUTHORITY_MATRIX.md` is its own to delete (decision 2026-10-23-011).
- The Chair deletes the probe repository `SaltyBrett/launch-probe-s10` (`gh repo delete` asks), its clone `/Users/twdaddy/code/personal/launch-probe-s10`, and `/Users/twdaddy/code/personal/tmpl-s6-probe`.
- The Blender connection's uv command was never run ([[reference_blender_mcp]]).
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- Decision 2026-10-23-002's second and third bullets stand, and decision 2026-10-22-006 stands.

## 6. Verification observed

- cold start, run through `scripts/session_start.py` as `/clear` would run it: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S16"), `doc-queue` exit 0
- `scripts/story_artifacts.py` fixtures: 38; 27 broken variants each caught by its own fixture, the first run vacuous (the runner's Python lacked PyYAML) and the rerun exposing five fixtures that tripped a neighbouring rule, rewritten until each was caught by its own
- `scripts/code_standard.py`'s 25 broken variants rerun and each confirmed caught by its own fixture
- closeout: `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
