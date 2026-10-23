# Handoff — S5

**For session:** S5
**Written by:** S4
**Written:** 2026-10-23

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S5.md`
- `docs/governance/framework_decisions.md` 2026-10-23-003 — the persona library TMPL-1.8 builds, its four open questions, and the supersessions it marks; then 2026-09-23-002, 2026-09-23-007 and 2026-10-22-005, the persona design it replaces
- [[reference_resources_sync]] and [[reference_session_closeout]] — the sync and the persona gate TMPL-1.8 changes
- `docs/governance/framework_decisions.md` 2026-10-22-001 — the substrate TMPL-1.7 proves end to end; then 2026-10-23-001 and 2026-10-23-002, which S4 built on it (the skills, and the ownership the scratch birth's `.claude/` tree is checked against)
- [[reference_claude_code_skills]] — the forked closeout, its brief in the arguments, and what the S4 probe saw, which the TMPL-1.7 closeout run extends to a run end to end
- [[reference_claude_code_hooks]] — the start, compact and stop hooks the cold-start and compaction proofs observe, and that hooks wait for the trust dialog in an interactive session
- [[reference_derived_project_start]] — what a scratch birth looks like and what it regenerates, the baseline for TMPL-1.7's first observation

## 2. Completed last session

- TMPL-1.4 — five skills in `.claude/skills/` (`closeout` forked as `general-purpose`, `planning-session` and `document-production` inline, `release` and `pristine-cut` the operator's alone), listed by path in `AGENTS.md`; the handoff, sprint and document standards keep the law and point to them; `scripts/skill_scan.py` with its self-test and runbook sections in `docs/governance/gate_suite_runbook.md`; [[reference_claude_code_skills]] (commits 16562d8, bb78f85)
- TMPL-1.6 — ownership of the new paths in `scripts/new_project.py` (`LOCAL_STATE`), `scripts/template_update.py` and `scripts/sanitize_template.py`, the registry path held equal in five places by fixture; `.gitignore` carries `.claude/settings.local.json`; [[reference_template_update]] updated (commit f2f62d6)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-23-001 Procedures are skills, and a skill is repository markdown; the closeout forked with the brief in its arguments, the release and the pristine cut the operator's alone; `skill-scan` keeps each skill in step with the config
- 2026-10-23-002 The Claude Code paths and the session's local files are owned by decision; a project's `docs/personas/` reaches `.claude/agents/` through `dev-resources`
- 2026-10-23-003 Personas ship as a library in the template, inactive; a project activates the ones it needs at its first session; approved by the operator after the closeout

## 5. Blockers and open questions

- Decision 2026-10-23-003 leaves four questions for the operator at the start of TMPL-1.8: how much of the library ships in `v2.0.0` (recommended: the mechanism and a starter set, the full team through TMPL-3.1 as MINOR releases); whether `dev-resources` is retired or kept for knowledge alone; whether a project's own persona can be proposed back to the library; how a `v1.0.0` project's `docs/personas/` reaches its roster.
- Decision 2026-10-23-002 was made by the agent; its second and third bullets stand, and its first, fourth and fifth are superseded by 2026-10-23-003 when TMPL-1.8 builds it.
- Decision 2026-10-22-006, put to the operator at the S3 handover, stands unless the operator overturns it.
- Still unobserved: the first interactive session in a fresh clone (hooks wait for the trust dialog) and `disableWorkflows` in a live session, both for TMPL-1.7; that `--agent` replaces Claude Code's system prompt rests on the docs and a prompt-size difference.

## 6. Verification observed

- cold start: the `SessionStart` hook ran the identity gate (PASS), the pull and `session-verify` (PASS); both hook types installed; Claude Code 2.1.308
- TMPL-1.4: `skill-scan` self-test, 43 fixtures; 38 broken variants, each caught; plants of a missing hook id and a missing stage each failed `pre-commit run skill-scan --all-files` (exit 1) and a real commit; the one-home grep finds each procedure's command in its skill alone; `claude -p "/closeout …"` in a scratch clone ran as a `general-purpose` subagent, first command `git status --short`, stopped at the sync it could not get approved, tree untouched
- TMPL-1.6: self-tests 21, 36 and 20; 19 broken variants, each caught; every real `.claude/` path and local file classifies as decided
- this closeout: `python3 scripts/resources_sync.py --apply` exit 0, every entry `up-to-date`, stamp `main 9002dfb01f40`; `pre-commit run session-closeout --hook-stage manual --all-files` PASSED (exit 1 on the first run for the archive move, exit 0 on the rerun); `pre-commit run --all-files` exit 0
- after the closeout: decision 2026-10-23-003 banked, TMPL-1.8 opened and this pair re-pointed to it; `pre-commit run --all-files` exit 0 and `pre-commit run session-closeout --hook-stage manual --all-files` exit 0 on the edited pair
