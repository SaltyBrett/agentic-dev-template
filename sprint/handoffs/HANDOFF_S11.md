# Handoff — S11

**For session:** S11
**Written by:** S10
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S11.md`
- [[reference_launch_live_run]] — TMPL-5.4's record: what the two live runs showed, the defects they exposed, and what is still unobserved, which this session observes and adds
- [[reference_project_launch]] — how `/project-launch` reads each stage's state, and why the first closeout comes after planning, so the Chair's commands are given in the order the skill accepts them
- `docs/governance/framework_decisions.md` decision 2026-10-23-024 as amended — a boundary before planning is `/clear` or a new conversation, still S1; the emergency close before a project's first closeout, which the probe took at `7c50dae`
- `docs/governance/framework_decisions.md` decision 2026-10-23-023 — a copy of the template judged as a project, and the birth probe judging GitHub's first run, which the probe's first closeout push relies on for a green `gates` run
- `docs/governance/framework_decisions.md` decision 2026-10-23-021 as amended — `/project-launch` as built: the Chair's alone, in the main session, the plan's versions on the tracker's `**Source:**` line
- `docs/governance/framework_decisions.md` decision 2026-10-23-020 as amended — the approval gate planning's first epic must pass, a `**Skips:**` decision standing in for the architecture, a reopened revision standing at its last approved version
- `.claude/skills/project-launch/SKILL.md` — the procedure the Chair runs in the probe, the source of every command the session gives
- `.claude/skills/release/SKILL.md` — the release TMPL-2.4 cuts once TMPL-5.4 is Done; the operator's alone
- `sprint/story-tracker.md` TMPL-2.4's row — what the release and the three projects' adoption must prove

## 2. Completed last session

- TMPL-5.5 — `README.md` as the operator's front page, a nine-step walkthrough and a catalog of commands, operator scripts, session hooks and gates; `TEMPLATE_GUIDE.md` cut to named sections on what the initializer leaves; `scripts/skill_scan.py` refusing a skill the README's `## Catalog` does not name, its section in `docs/governance/gate_suite_runbook.md`, `scripts/gate_runbook_scan.py`, [[reference_claude_code_skills]]; decision 2026-10-23-022 (30677d3). Done once the walkthrough's steps 1 to 4 and 9 ran for real on `SaltyBrett/launch-probe-s10` (d1c3610, rows stamped)
- TMPL-2.8 — opened and built from the walkthrough's red first run: `scripts/doc_authority_scan.py` judges a copy of the template before its initializer as a project; `scripts/birth_probe.py` also runs the suite on the Initial commit; `.pre-commit-config.yaml`, `.github/workflows/gates.yml`, `docs/governance/gate_suite_runbook.md`, [[reference_ci_backstop]], [[reference_derived_project_start]], [[reference_doc_authority]]; decision 2026-10-23-023, the Chair's choice of fix. The probe reproduces GitHub's red run at `30677d3` and is green at `ea19c0d` under both profiles (ea19c0d; done and stamped d1c3610)
- TMPL-5.4, in progress — two live runs with the Chair in `SaltyBrett/launch-probe-s10`: decision 2026-10-23-024, a boundary before planning a new conversation, still S1, in `.claude/skills/project-launch/SKILL.md`, `README.md`, [[reference_project_launch]] (fb67475); then the emergency close before a project's first closeout corrected in `AGENTS.md` and `docs/standards/session_handoff_standard_v2.0.md`, `/clear` named as the boundary, 2026-10-23-024 amended, both runs recorded in [[reference_launch_live_run]] with its `INDEX.md` row (5b886bc; standard's row stamped 4960752). Tracker set In Progress (4a1699e); S10 entry (f046874)

## 3. In progress

- TMPL-5.4 — the probe clone `/Users/twdaddy/code/personal/launch-probe-s10` stands at `69adefd`, its launch in the PRD stage: intake (`2f19d68`) and team (`628de65`, lead `product-manager`) done; an S1 emergency checkpoint (`7c50dae`); the PRD draft committed (`8f03e4e`) with its gaps in §11, awaiting the Chair's approval; the template's corrected skill, README and `AGENTS.md` copied in (`7c72eba`, `69adefd`). Its local commits are unpushed past `c5f7b8b` until its first closeout pushes. Unobserved: an approved PRD, a skip with its reason, planning and its `**Source:**` line, a revision re-approved with the plan read stale, and the first closeout after planning.

## 4. Decisions logged

- 2026-10-23-022 The README front page as built: a nine-step walkthrough from `gh repo create` to taking a release, each step what to type and what to see; a catalog of the commands by skill path, the operator scripts, the session hooks and the gates by link; `TEMPLATE_GUIDE.md` cut to named sections on what the initializer leaves; `skill-scan` refusing a skill the `## Catalog` section does not name, in the template and in a project
- 2026-10-23-023 A copy of the template before its initializer, GitHub's "Initial commit", judges the template's rows and decisions in the template as a project does, its history holding none of their stamped commits; the birth probe also runs the suite on the Initial commit, as GitHub does; amends 2026-10-23-015, 2026-10-23-017 and 2026-10-23-018
- 2026-10-23-024 Before planning, a launch stage's session boundary is a new conversation, still S1, not a closeout, since no kickoff can cite a story until planning writes the first; the first closeout comes after planning; amends 2026-10-23-008 and 2026-10-23-021 (amended 2026-10-23: `/clear` the boundary; the emergency close before a project's first closeout corrected)

## 5. Blockers and open questions

- No blockers.
- S10 ran in the S9 conversation at the Chair's request, its cold start run through `scripts/session_start.py` as `/clear` would run it.
- The probe repository is private on GitHub with its local commits unpushed past `c5f7b8b` until its first closeout pushes; the Chair deletes it after TMPL-5.4 (`gh repo delete` asks).
- The probe's skill, README and `AGENTS.md` were brought up to the template by copy, since no release carries them yet.
- For TMPL-2.4: a project born from `main` between releases stamps `.template-version` as `v1.0.0` though it carries later changes, so the updater's three-way base for it is `v1.0.0` ([[reference_template_versioning]]).
- The library has no general mobile-game engine persona: `game-engine-developer` is Rust/Bevy only, observed at the probe's team stage ([[reference_launch_live_run]]).
- Open question on TMPL-2.4's row, found after the S10 closeout and the Chair's to settle before any adoption: the three projects' PRDs and architectures predate the approved form, so the approval gate refuses them after adoption until each is approved or skipped ([[reference_project_launch]]).
- Decision 2026-10-23-022 was settled by the AI within 2026-10-23-009; 2026-10-23-023 and 2026-10-23-024 are the Chair's, each on the AI's report.
- The Blender connection's uv command was read from the pinned commit's tree and never run; the first operator to activate it runs it first ([[reference_blender_mcp]]).
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- Decision 2026-10-23-002's second and third bullets stand.
- Decision 2026-10-22-006 stands unless the operator overturns it.
- The three projects keep their own `sprint/recovery/AUTHORITY_MATRIX.md`, theirs to delete (decision 2026-10-23-011); name it to the operator at TMPL-2.4.
- The scratch probe folder `/Users/twdaddy/code/personal/tmpl-s6-probe` can be deleted by the operator.

## 6. Verification observed

- cold start, run through `scripts/session_start.py`: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0, `doc-queue` exit 0
- TMPL-5.5: eight fixtures pass, seven broken variants each caught; on the real tree a README missing `/doc-drain` refused by `skill-scan`, passing once restored
- TMPL-2.8: `scripts/birth_probe.py` at `30677d3` reproduces GitHub's red run on the Initial commit; at `ea19c0d` green at the Initial commit and under both profiles; run 40058466647 green
- TMPL-5.4: in the probe, a `session-verify` after the S1 emergency checkpoint passed, and a `/closeout` before planning wrote and committed nothing
- closeout: `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
