# Handoff — S14

**For session:** S14
**Written by:** S13
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S14.md`
- `docs/governance/framework_decisions.md` decision 2026-10-24-007 — the core limits and their evidence: complexity 15, 60 code lines and 5 parameters per added or edited function, no new clones, 80% of new lines covered, tests at 10 and 100, file length a reviewer signal at 500, exceptions never growing; the numbers the gate is configured to and never looser
- `docs/governance/framework_decisions.md` decision 2026-10-24-008 — proved measurement and the mapping rule: one pinned tool per slot in each stack profile, a measurer counted only once it passes its language's fixture and a recall check on every run, `lizard` 1.17.10 failing Rust and TypeScript
- `docs/governance/framework_decisions.md` decision 2026-10-24-009 — the judgement page `.claude/rules/code-quality.md` and the code reviewer's and security auditor's briefs, which `personas/code-reviewer.md` is drafted from
- `docs/governance/framework_decisions.md` decision 2026-10-24-005 — the eleven review triggers, whose trigger paths each stack profile supplies
- [[reference_coding_standard_calibration]] — why the numbers are what they are, and the silent tool defects (lizard on Rust lifetimes, raw strings, typed TypeScript methods and Python `match`; its forgive comment; jscpd's size caps) the gate must not repeat
- [[reference_kb_frontmatter_validation]] — a gate that reads nothing reports green, which the recall check exists to prevent
- [[reference_claude_code_rules]] — how a path-scoped rule loads and fails silently, which bounds what `.claude/rules/code-quality.md` can carry
- `.claude/rules/gate-scripts.md` — the law a new gate script is built to: fixtures, broken variants, the runbook section
- `docs/governance/doc_control_standard.md` — how `docs/standards/coding_standard_v1.0.md` declares itself as an authority with its version log, so it passes `doc-authority-scan`

## 2. Completed last session

- TMPL-4.1 — done: the coding standard's design session with the Chair and a specialized reviewer agent, run in the S11 conversation with the Chair remote, every question answered in chat; calibrated on pinned industry code (ripgrep 14.1.1, packaging 24.1, zod v3.23.8 known-good; the Gilded Rose and Tennis katas known-bad) and logged in `docs/governance/framework_decisions.md` as the core limits (2026-10-24-007), proved measurement and the mapping rule (2026-10-24-008) and the judgement page with the reviewer and auditor briefs (2026-10-24-009); the evidence in `docs/orchestration/knowledge/reference_coding_standard_calibration.md` with its `INDEX.md` row; TMPL-4.1 set Done and TMPL-4.2 scoped in `sprint/story-tracker.md`; S3's entry moved from `sprint/sprint-status.md` to `sprint/archive/sprint-status_2026.md` (25d738d)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-007 The coding standard's core limits, proved against ripgrep, packaging and zod and the Gilded Rose and Tennis katas: per added or edited function, complexity 15, 60 code lines, 5 parameters; no new clones; 80% of new lines covered; tests at complexity 10 and 100 lines; file length a reviewer signal at 500; exceptions recorded, never growing
- 2026-10-24-008 The coding standard's measurement is proved, per language: each stack's profile names one pinned tool per slot, configured to the core numbers and never looser, and a tool counts only once it passes its language's measurement fixture and a recall check on every run; `lizard` 1.17.10 fails Rust and TypeScript
- 2026-10-24-009 The coding standard's judgement page (`.claude/rules/code-quality.md`, path-scoped to code, opening with `CONSTITUTION.md` §4A) and its two briefs: the code reviewer, a new library persona, never the implementer; the security audit, `security-engineer`'s brief for the security stage

## 5. Blockers and open questions

- No blockers.
- TMPL-4.2 is larger than one session (the standard, three profiles, the gate, the page, the persona, the proof), so whether to split it into stories, and in what order, is the Chair's at the session's start.
- Which project carries the proof is the Chair's: PocketGames (Rust) or Comfy (Python).
- Rust's tools need the Rust toolchain, which is not installed on the operator's machine (`cargo` is missing), so installing it there or proving Rust in CI only is the Chair's call.
- The calibration's reference clones and the reviewer agent's scripts were scratch and are gone with the session; the evidence is kept in decision 2026-10-24-007 and [[reference_coding_standard_calibration]].
- S12 and S13 ran in the S11 conversation at the Chair's request with the Chair remote, every question answered in chat.
- Comfy's S4 was never closed out, so its next Comfy session completes that closeout before building ([[reference_v2_adoption]]).
- PocketGames' `main` waits for the project's own release step to fast-forward it to `build/milestone-1` ([[reference_v2_adoption]]).
- Each project's `sprint/recovery/AUTHORITY_MATRIX.md` is its own to delete (decision 2026-10-23-011).
- The Chair deletes the probe repository `SaltyBrett/launch-probe-s10` (`gh repo delete` asks), its clone `/Users/twdaddy/code/personal/launch-probe-s10`, and `/Users/twdaddy/code/personal/tmpl-s6-probe`.
- The library has no general mobile-game engine persona ([[reference_launch_live_run]]).
- The Blender connection's uv command was never run ([[reference_blender_mcp]]).
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- Decision 2026-10-23-002's second and third bullets stand, and decision 2026-10-22-006 stands.

## 6. Verification observed

- cold start, run through `scripts/session_start.py` as `/clear` would run it: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S13"), `doc-queue` exit 0
- closeout: `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
