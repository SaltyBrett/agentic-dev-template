# Handoff — S15

**For session:** S15
**Written by:** S14
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S15.md`
- `docs/standards/coding_standard_v1.0.md` — the law the gate enforces; read every number in §2, the limits the gate is configured to and never looser, with the scope of changed code, the recall check of §3 and the exceptions file `code-exceptions.yaml` of §4
- `docs/governance/framework_decisions.md` decision 2026-10-24-007 — the core limits and their evidence: complexity 15, 60 code lines and 5 parameters per added or edited function, no new clones, 80% of new lines covered, tests at 10 and 100, file length a reviewer signal at 500, exceptions never growing
- `docs/governance/framework_decisions.md` decision 2026-10-24-008 — proved measurement and the mapping rule: one pinned tool per slot, a measurer counted only once it passes its language's fixture and a recall check on every run, and `lizard`'s defects, which the Python measurer on `ast` avoids
- `docs/governance/framework_decisions.md` decision 2026-10-24-010 — the split: what TMPL-4.3 holds (the core and the Python profile, proved on Comfy) and what TMPL-4.4 and TMPL-4.5 hold instead, so 4.3 builds no Rust or TypeScript profile
- [[reference_coding_standard_calibration]] — the silent tool defects the gate must not repeat (lizard on Python `match`, its forgive comment, jscpd's size caps), and the template's own scripts over the limits (25 of 304 functions), which bears on whether the template opts in
- `.claude/rules/gate-scripts.md` — the law a new gate script is built to: fixtures, broken variants, the runbook section
- [[reference_gate_runbook]] — why a new hook changes `docs/governance/gate_suite_runbook.md` in the same commit, which `gate-runbook` enforces
- [[reference_precommit_interpreter]] — why a local hook declares `language: python` and is invoked through `pre-commit`, never a bare `python`
- [[reference_precommit_stash]] — what a manual-stage hook judges without `--all-files`, which bears on running the gate over the commit's staged change

## 2. Completed last session

- TMPL-4.2 split by the Chair (decision 2026-10-24-010): 4.2 the law and the judgement layer; 4.3 the gate's core with the Python profile, proved on Comfy; 4.4 the Rust profile, proved on PocketGames, the Rust toolchain decided at its start; 4.5 the TypeScript profile, proved on fixture code; TMPL-3.2 now waits on 4.3; the stories opened in `sprint/story-tracker.md` (1389fa9)
- TMPL-4.2 — done: `docs/standards/coding_standard_v1.0.md` written as the ninth authority, its version log citing decisions 2026-10-24-007 to -009; `.claude/rules/code-quality.md`, path-scoped to code, opening with `CONSTITUTION.md` §4A; `personas/code-reviewer.md` in the library from decision 2026-10-24-009's brief; `AGENTS.md`'s governance map and `README.md`'s standards list name the standard; S4's entry moved from `sprint/sprint-status.md` to `sprint/archive/sprint-status_2026.md` (1389fa9); the standard's 1.0 version-log row stamped (87a6fa0)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-010 TMPL-4.2 split, larger than one session: 4.2 the standard, the judgement page and the code reviewer; 4.3 the gate's core and the Python profile, proved on Comfy; 4.4 the Rust profile, proved on PocketGames, the Rust toolchain decided there; 4.5 the TypeScript profile, proved on fixture code; TMPL-3.2 waits on 4.3

## 5. Blockers and open questions

- No blockers.
- The gate is new, so its plan is the Chair's at the session's start: how a project opts in and names its profile (a profile file read by the gate); whether the template itself opts in, its scripts being over the limits; where the gate runs (on the commit's staged change through pre-commit, and on the push range in CI); the script and hook names.
- jscpd is a Node tool, so its hook needs pre-commit's `node` language or a pinned install, settled in the plan.
- The measuring tools the calibration installed lived in a scratch environment that is gone with S13, so each tool the Python profile pins is installed through the hook's own environment.
- S12 to S14 ran in the S11 conversation at the Chair's request with the Chair remote, every question answered in chat.
- Comfy's S4 was never closed out, so the proof runs on a scratch copy of Comfy and touches nothing in Comfy itself ([[reference_v2_adoption]]).
- PocketGames' `main` waits for the project's own release step to fast-forward it to `build/milestone-1` ([[reference_v2_adoption]]).
- Each project's `sprint/recovery/AUTHORITY_MATRIX.md` is its own to delete (decision 2026-10-23-011).
- The Chair deletes the probe repository `SaltyBrett/launch-probe-s10` (`gh repo delete` asks), its clone `/Users/twdaddy/code/personal/launch-probe-s10`, and `/Users/twdaddy/code/personal/tmpl-s6-probe`.
- The library has no general mobile-game engine persona ([[reference_launch_live_run]]).
- The Blender connection's uv command was never run ([[reference_blender_mcp]]).
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- Decision 2026-10-23-002's second and third bullets stand, and decision 2026-10-22-006 stands.

## 6. Verification observed

- cold start, run through `scripts/session_start.py` as `/clear` would run it: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S14"), `doc-queue` exit 0
- each new file's gate shown to read it: an unquoted persona list item refused as `list`, a rule restating `AGENTS.md` refused as `rule-restates`, a dead glob refused as `rule-dead`
- `pre-commit run --all-files` exit 0
- closeout: `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
