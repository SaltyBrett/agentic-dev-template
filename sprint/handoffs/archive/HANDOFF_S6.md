# Handoff — S6

**For session:** S6
**Written by:** S5
**Written:** 2026-10-23

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S6.md`
- `docs/governance/framework_decisions.md` 2026-10-23-003 (as amended) — the adoption answer TMPL-1.10 builds: the updater converts every `docs/personas/` file into the roster and removes the folder, proved against the real `v1.0.0` files; then 2026-10-23-004, the library's team the converted personas sit beside
- [[reference_template_update]] — the ownership map and the `v1.0.0` adoption path the converter implements, and the rule that the updater never writes the roster nor a `source: dev-resources` entry, which TMPL-1.10 changes for adoption
- [[reference_resources_sync]] — what a `v1.0.0` project holds from the retired sync: `docs/personas/`, the `source: dev-resources` knowledge entries and `.resources-version`, the three things TMPL-1.10 settles
- [[reference_session_closeout]] — the persona lint every converted file must pass, and the roster's rule against the library (drift and fork) that a converted persona meets
- [[reference_claude_code_skills]] — the forked closeout TMPL-1.7 runs end to end on the scratch project, and what the S4 probe already saw
- [[reference_claude_code_hooks]] — the start, compact and stop hooks TMPL-1.7 observes, and that hooks wait for the trust dialog in an interactive session
- [[reference_derived_project_start]] — what a scratch birth looks like and what it regenerates, the baseline for TMPL-1.7's first observation

## 2. Completed last session

- Decision 2026-10-23-003 banked after the S4 closeout (5cccd1e) and amended with the operator's four answers; TMPL-1.8 split into TMPL-1.8, TMPL-1.9 and TMPL-1.10 in `sprint/story-tracker.md` (8cb25a2)
- TMPL-1.8 — the five personas moved to the library `personas/`, the template's roster `.claude/agents/` keeping `framework-maintainer`; `scripts/session_closeout.py` lints the library and holds each roster copy to it (`library-drift`, `library-fork`, a newer library noted); `scripts/session_start.py` names a persona the library has moved past; `.claude/skills/team-selection/SKILL.md`; `scripts/new_project.py` clears the roster at birth, `scripts/sanitize_template.py` keeps it, `scripts/template_update.py` keeps it and merges the library; `scripts/resources_sync.py`, its hook, its closeout rule and `.resources-version` removed; supersessions marked on both sides and the teaching entries corrected (ddaaa6c, 94a292c, e09715b)
- TMPL-1.9 — thirty new personas in `personas/` across the software lifecycle, data science with BI and reporting, document management, writing, quality control and game development, each passing the persona lint; the team-selection skill groups the library by those areas (516c3a3)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-23-003 Personas ship as a library in the template, inactive, activated per project at its first session; amended with the operator's answers (full team in `v2.0.0`, `dev-resources` retired, a project's own personas stay in it, the updater converts a `v1.0.0` project's `docs/personas/`); supersedes 2026-09-23-007 and, in scope, 2026-09-23-002, 2026-10-22-005 and 2026-10-23-002
- 2026-10-23-004 The persona library's team: roles across the software lifecycle, data science with BI and reporting, document management, writing, quality control and game development; a code reviewer left to TMPL-4

## 5. Blockers and open questions

- No blockers.
- Decision 2026-10-23-002 was put to the operator at the S4 handover and not answered explicitly; its second and third bullets stand, and its first, fourth and fifth are superseded by 2026-10-23-003.
- Decision 2026-10-22-006 stands unless the operator overturns it.
- The updater's own suite run after `--apply` failed, under the old design, until a roster existed (decision 2026-10-23-002, Consequences); with the conversion inside the updater, TMPL-1.10 confirms the suite passes on the first run.
- Still unobserved: the first interactive session in a fresh clone (hooks wait for the trust dialog) and `disableWorkflows` in a live session, both for TMPL-1.7.

## 6. Verification observed

- cold start: `git pull` exit 0; `pre-commit run session-verify --hook-stage manual --all-files` exit 0 at 5cccd1e
- TMPL-1.8: twenty broken variants across the closeout gate, the start hook, the initializer, the updater and the sanitizer, each failing at least one fixture without crashing (three first written wrong and rewritten); a roster copy edited at the same version failed `session-closeout-check` as `library-drift` and was refused by a real commit; one bumped ahead failed as `library-fork` and was refused too; the library bumped past the roster passed silently, so the start hook now names it
- TMPL-1.8 scratch birth: `new_project.py --apply` exit 0 with the suite green, the roster emptied and the library whole; `session-verify` exit 0 at S1; a `claude -p` session's init event listed only the built-in agents, the `team-selection` skill available
- TMPL-1.9: every library persona passes the persona lint in `session-closeout-check`; a plant of an unquoted list item holding `: ` was refused as `list`
