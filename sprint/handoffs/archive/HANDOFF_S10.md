# Handoff — S10

**For session:** S10
**Written by:** S9
**Written:** 2026-10-23

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S10.md`
- `docs/governance/framework_decisions.md` decision 2026-10-23-009 — the README front page and the catalog gate TMPL-5.5 builds: the walkthrough from creating a project through the session loop, the catalog of every command, operator script and session hook, the gates by link to their runbook, and `skill-scan` holding the catalog to the skills
- `docs/governance/framework_decisions.md` decision 2026-10-23-021 — `/project-launch` as built, the walkthrough's centre: the Chair's alone, in the main session, each stage's state read from the documents, the S1 entry's one next step
- `docs/governance/framework_decisions.md` decision 2026-10-23-020 as amended — the approval gate the walkthrough must describe truly: a reopened revision standing at its last approved version, `**Skips:**` naming any launch stage, only `prd` and `architecture` standing in for an approval
- `docs/governance/framework_decisions.md` decision 2026-10-23-018 — the birth probe and the CI `birth` job, which the walkthrough's release step relies on and TMPL-5.5's success criteria run under both profiles
- [[reference_project_launch]] — how `/project-launch` reads each stage's state, pauses, skips and reopens, which the walkthrough teaches and TMPL-5.4 observes live
- [[reference_doc_authority]] — authorities and their version logs: the `skill-scan` runbook section is an authority whose row cites decision 2026-10-23-009 and TMPL-5.5, and the approval gate the launch passes through
- [[reference_claude_code_skills]] — what the skill gate reads, the base the catalog rule extends, and why `AGENTS.md` lists every skill
- `.claude/skills/project-launch/SKILL.md` — the procedure the walkthrough follows step by step and TMPL-5.4 runs with the Chair
- `scripts/skill_scan.py` — the gate TMPL-5.5 extends to refuse a skill the README's catalog does not name
- `README.md` — the front page TMPL-5.5 rewrites
- `TEMPLATE_GUIDE.md` — cut by TMPL-5.5 to what the initializer does not do

## 2. Completed last session

- TMPL-2.7 — `scripts/birth_probe.py`, its `birth-probe-selftest` hook in `.pre-commit-config.yaml` and section in `docs/governance/gate_suite_runbook.md`, the `birth` job in `.github/workflows/gates.yml`, [[reference_ci_backstop]]; decisions 2026-10-23-017 and 2026-10-23-018. The probe exits 1 at `38c549d` under both profiles at `doc-authority-scan` alone, exits 0 at `19537c4` under both, and run 40050465938 is green on `gates` and both `birth` jobs (139859a, 19537c4; row stamped d1b3deb)
- TMPL-2.2 — the `doc-queue` gate as `scripts/doc_authority_scan.py --queue`, run at cold start by `scripts/session_start.py` and reported by `.claude/skills/closeout/SKILL.md`; the `.claude/skills/doc-drain/SKILL.md` skill; the session-at-work rule in `scripts/session_closeout.py`; the `doc-queue` section of `docs/governance/gate_suite_runbook.md`, `docs/governance/doc_control_standard.md`'s Recording a change, `AGENTS.md`'s cold start and skills table, [[reference_doc_authority]]; decision 2026-10-23-019. A fresh agent drained a queued story by the skill alone and its friction report corrected four steps (0dcccd2, df959dc)
- TMPL-5.3 — the approval gate in `scripts/doc_authority_scan.py`: a real epic needs an approved PRD and architecture or an APPROVED decision headed `**Skips:**`; `docs/governance/gate_suite_runbook.md`, `docs/governance/doc_control_standard.md`, `docs/templates/README.md` and `.claude/skills/planning-session/SKILL.md`'s Preconditions; decision 2026-10-23-020. Proved on a scratch birth (df959dc, d7ad4d7; rows stamped 9f02b8d)
- TMPL-5.2 — `.claude/skills/project-launch/SKILL.md`, the Chair's alone, in the main session; `.claude/skills/team-selection/SKILL.md` takes intake's answer, `.claude/skills/planning-session/SKILL.md` records the plan's sources on the tracker's `**Source:**` line, `scripts/new_project.py`'s S1 entry names it as the one next step; `README.md`, `TEMPLATE_GUIDE.md`, `AGENTS.md`, [[reference_project_launch]]; decision 2026-10-23-021, and decision 2026-10-23-020 amended so a revision in progress can be committed (`scripts/doc_authority_scan.py`, `docs/templates/README.md`). A fresh agent applied `status` to two scratch trees and its friction report sharpened five rules (b612e51, 6e94683; row stamped 0e437b3)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-23-017 CI makes a scratch project on every push to the template: `scripts/birth_probe.py` births a committed revision through the initializer, whose own suite run is the verdict, once per profile; proved red at the commit that blocked births; built as TMPL-2.7 before the release
- 2026-10-23-018 The birth probe as built: the revision's tree by `git archive`, one "Initial commit", that revision's initializer with `--apply`, no `GIT_*` or `CLAUDE_PROJECT_DIR` reaching it; a `birth-probe-selftest` hook over a stub initializer; a `birth` job in CI, one run per profile, skipped in a project
- 2026-10-23-019 The doc-queue as built: `doc_authority_scan.py --queue`, a manual hook the start hook runs at cold start and the closeout reports; the session at work is one rule in `session_closeout.py`; the drain is `doc-drain`, forked as `general-purpose` in the writer's role, uncommitted
- 2026-10-23-020 The approval gate as built (amended 2026-10-23, the Chair's choice, so a reopened revision stands at its last approved version): a real epic needs an approved PRD and architecture, the architecture's `prd:` the PRD's newest version, or an APPROVED project decision headed `**Skips:**`; a rule of `doc-authority-scan`, on every commit
- 2026-10-23-021 `/project-launch` as built: the Chair's alone (`disable-model-invocation`), in the main session; each stage's state read from the documents, with skipped, reopened and stale; intake's answers in the PRD draft; the plan's versions on the tracker's `**Source:**` line; the S1 entry's one next step

## 5. Blockers and open questions

- No blockers.
- TMPL-5.4 needs the Chair at the keyboard for the whole run, so the Chair schedules it at the start of S10.
- Decision 2026-10-23-008's Affects line named `scripts/session_closeout.py` for the approval gate; it was built in `scripts/doc_authority_scan.py` instead, and decision 2026-10-23-020 says why.
- Decisions 2026-10-23-018, 2026-10-23-019 and 2026-10-23-021 settled their mechanics by the AI, within approved decisions. The Chair chose the S9 order, the `**Skips:**` form, that `/project-launch` is the Chair's alone, and that a reopened revision stands (2026-10-23-020 as amended).
- Both new skills, `doc-drain` and `project-launch`, were proved by a fresh agent following the file alone, and their friction reports changed them before release ([[reference_doc_authority]], [[reference_project_launch]]). TMPL-5.4 is the first live run of `/project-launch`.
- The Blender connection's uv command was read from the pinned commit's tree and never run; the first operator to activate it runs it first ([[reference_blender_mcp]]).
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- Decision 2026-10-23-002's second and third bullets stand.
- Decision 2026-10-22-006 stands unless the operator overturns it.
- The three projects keep their own `sprint/recovery/AUTHORITY_MATRIX.md`, theirs to delete (decision 2026-10-23-011); name it to the operator at TMPL-2.4.
- The scratch probe folder `/Users/twdaddy/code/personal/tmpl-s6-probe` can be deleted by the operator.

## 6. Verification observed

- cold start, run by the `SessionStart` hook: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0
- TMPL-2.7: thirteen fixtures pass, ten broken variants each caught; `scripts/birth_probe.py` exit 1 at `38c549d` under both profiles, at `doc-authority-scan` alone; exit 0 at `19537c4` under both; run 40050465938 green on `gates` and both `birth` jobs
- TMPL-2.2: sixteen broken variants each caught; on a scratch birth the cold-start report read the queued story PASS at S1 and S2 and FAILED at S3
- TMPL-5.3: twenty-one fixtures pass, fifteen broken variants each caught (as amended, twenty-six fixtures and twenty variants); on a scratch birth a real epic refused with no documents and with drafts, passing once both are approved by `docs/templates/README.md`, refused on a PRD revision the architecture lags, passing on an approved skip and refused on a proposed one
- TMPL-5.2: a birth from `6e94683` green under both profiles
- closeout: `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
