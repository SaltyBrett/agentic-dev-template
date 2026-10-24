# Handoff — S13

**For session:** S13
**Written by:** S12
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S13.md`
- `docs/governance/framework_decisions.md` decision 2026-10-22-003 — the coding standard's three layers (the core limits as numbers, the per-stack tool mapping, the one judgement page), and why it opens with a design session: it is the hardest thing in the framework to unwind
- `docs/governance/framework_decisions.md` decision 2026-10-24-004 — the team's orchestration TMPL-3.1 designed: the review stage the code reviewer fills, each role handing off through committed artifacts in `docs/stories/<ID>/`, a gate judging each
- `docs/governance/framework_decisions.md` decision 2026-10-24-005 — the eleven review triggers, whose trigger paths the stack profile supplies
- `docs/governance/framework_decisions.md` decision 2026-10-24-006 — the role map by story type, whose build stage the stack profile judges, and which leaves the code reviewer's slot to TMPL-4.1
- `CONSTITUTION.md` §4A — the design quality guardrail, which the judgement page under `.claude/rules/` opens with
- `sprint/story-tracker.md` epics TMPL-3 and TMPL-4 — TMPL-4.1's row, what TMPL-4.2 builds from it, and TMPL-3.2, which waits on TMPL-4.2
- `personas/security-engineer.md` — the library role beside which the security auditor's brief stands, so the two do not overlap
- `personas/qa-engineer.md` — the library role beside which the code reviewer's brief stands: the verifier tests behaviour, the reviewer judges structure and duplication, never the implementer
- [[reference_claude_code_rules]] — how a path-scoped rule loads and fails silently, which bounds what the judgement page can carry

## 2. Completed last session

- TMPL-3.1 — done: the design session with the Chair, run in the S11 conversation with the Chair remote, every question answered in chat; logged in `docs/governance/framework_decisions.md` as the orchestration (2026-10-24-004), the eleven review triggers (2026-10-24-005) and the role map by story type covering every library persona (2026-10-24-006); TMPL-3.1 set Done and TMPL-3.2 scoped by the three decisions in `sprint/story-tracker.md`, waiting on TMPL-4.2; S2's entry moved from `sprint/sprint-status.md` to `sprint/archive/sprint-status_2026.md` (cde9181)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-004 The team's orchestration: a `/story <ID>` skill in the main session runs one story end to end, each role a subagent from the roster handing off through committed artifacts in `docs/stories/<ID>/`, a gate judging each before the next role starts; it stops only at a review trigger or a gate failing three times running; the law in a new team standard
- 2026-10-24-005 The review triggers: decision 2026-10-22-003's seven plus a deploy or release, a gate or CI change, data loss and a license change; detected from the diff where the change shows it and declared by a role otherwise; a story closes only with every hit trigger approved by the operator in its folder
- 2026-10-24-006 The team's role map: five story types (software, data, document, game, media) whose brief picks the stages and roles; every library persona given its artifact and its judging gate; the verifier and reviewer never the builder; `devops-engineer` ships; the code reviewer's slot left to TMPL-4.1

## 5. Blockers and open questions

- No blockers.
- TMPL-4.1 is design and proof only: each limit is proved against a known-good and a known-bad codebase before it is logged in `docs/governance/framework_decisions.md`, and the build is left to TMPL-4.2.
- Which codebases are the known-good and the known-bad is the Chair's to choose at the session's start, the three projects and the template's own scripts being candidates; their code stays out of the session context beyond what the reviewer must read.
- S12 ran in the S11 conversation at the Chair's request with the Chair remote and no terminal, every question answered in chat.
- Comfy's S4 was never closed out, so its next Comfy session completes that closeout before building ([[reference_v2_adoption]]).
- PocketGames' `main` waits for the project's own release step to fast-forward it to `build/milestone-1`, which carries the adoption ([[reference_v2_adoption]]).
- Each project's `sprint/recovery/AUTHORITY_MATRIX.md` is its own to delete (decision 2026-10-23-011).
- The Chair deletes the probe repository `SaltyBrett/launch-probe-s10` (`gh repo delete` asks), its clone `/Users/twdaddy/code/personal/launch-probe-s10`, and `/Users/twdaddy/code/personal/tmpl-s6-probe`.
- The library has no general mobile-game engine persona: `game-engine-developer` is Rust/Bevy only ([[reference_launch_live_run]]).
- The Blender connection's uv command was read from the pinned commit and never run; the first operator to activate it runs it first ([[reference_blender_mcp]]).
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- Decision 2026-10-23-002's second and third bullets stand, and decision 2026-10-22-006 stands.

## 6. Verification observed

- cold start, run through `scripts/session_start.py` as `/clear` would run it: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S12"), `doc-queue` exit 0
- closeout: `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
