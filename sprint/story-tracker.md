# Story Tracker

**Last Updated:** {{DATE}}
**Source:** PRD (see `docs/prd/`)

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` — read it before creating or
> updating stories (build this file from the PRD + Architecture with the planning-session skill).
>
> **READ SELECTIVELY (index-first).** Do NOT read this file whole. Read the **Summary Statistics** and
> **Dependency Order** below, then open only the epic/story rows relevant to the current task. Keep this
> file markdown (never JSON) and do not accrete changelog paragraphs.

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Stories** | 30 |
| **Not Started** | 2 |
| **In Progress** | 0 |
| **Blocked** | 0 |
| **Completed** | 28 |

---

## How to Use This Tracker

1. **Story IDs** follow the pattern: `{PREFIX}-{Epic#}.{Story#}` (e.g., INFRA-1.1 = Epic 1, Story 1)
2. **Dependencies** list other story IDs that must complete first
3. **Status** values: Not Started | In Progress | Blocked | Done
4. **Required Standards** lists standards to consult before implementation
5. **PRD Ref** links to the functional requirement in the PRD

---

## Dependency Order

```
Define your project's dependency layers here. Example:

INFRA --> DATA_INGEST --> TRANSFORM --> SERVE --> VALIDATE
```

No story in a later layer can start until dependencies in earlier layers are complete.

The template's own evolution uses one layer, `TMPL`. Its "PRD" is the goal statement in the
decision that opened the epic; the build history before `v1.0.0` is in the archive repository
that decision 2026-09-23-003 names.

---

## Epic: TMPL-1 — The Claude-native substrate (v2.0.0, decision 2026-10-22-001)

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| TMPL-1.1 | One cold start: the procedure in `AGENTS.md` alone, `CONSTITUTION.md` §2, the checklist and the handoff standard pointing to it; the comprehension questions removed; `AGENT_INTEROP.md` retired into `AGENTS.md`; `CLAUDE.md` kept as the import bridge until Claude Code ≥ 2.1.277 is installed, the condition written down. Condition met at S2: 2.1.308 installed, the native read observed, `CLAUDE.md` retired | Done | — | session_handoff_standard_v2.0.md | 2026-10-22-001 |
| TMPL-1.2 | Hooks: `SessionStart` (startup and `compact`) running the gates and injecting results, kickoff and newest entry; `Stop` refusing an uncommitted or unbanked turn; `PostToolUse` journal and the working-notes file under `sprint/recovery/`; `disableWorkflows`; `ask` rules for the one-way doors; `PreCompact` tested as a backstop | Done | TMPL-1.1 | session_handoff_standard_v2.0.md | 2026-10-22-001 |
| TMPL-1.3 | Personas to `.claude/agents/`: `persona-lint` and `resources_sync.py` repointed, the kickoff names the agent, `session_closeout.py` rules updated, the registry republished to `dev-resources`. Done at S3: the start hook injects the persona, `--agent` optional; `dev-resources` holds both trees (2026-10-22-005) | Done | TMPL-1.1 | session_handoff_standard_v2.0.md | 2026-10-22-001 |
| TMPL-1.4 | Procedures to forked skills: closeout, release cut, planning session, sanitize-and-cut, document production; the standards shrink to the law; a gate keeps each skill's commands in step with the config. Done at S4: five skills listed in `AGENTS.md`, the closeout forked with the brief as arguments, `skill-scan` (2026-10-23-001) | Done | TMPL-1.2, TMPL-1.3 | sprint_management_standard_v1.0.md | 2026-10-22-001 |
| TMPL-1.5 | Path-scoped rules under `.claude/rules/`; `CONSTITUTION.md` slimmed (§2 a pointer, §6.3 a pointer to the knowledge entry); the checklist reduced to what a script does not already prove. §2 and the checklist were done by TMPL-1.1 (S2). Done at S3: four rules, gated (2026-10-22-006) | Done | TMPL-1.1 | doc_control_standard.md | 2026-10-22-001 |
| TMPL-1.6 | Ownership of the new paths in the initializer, the updater and the sanitizer (`.claude/agents`, `.claude/skills`, `.claude/rules`, `.claude/settings.json`, the journal and notes), with fixtures proved against broken variants; TMPL-1.3 renamed `docs/personas/` to `.claude/agents/` in the three scripts' lists, with no ownership fixture yet; a project's own `docs/personas/` carried into `.claude/agents/` at adoption. Done at S4: the registry kept and held equal in five places, skills, rules and settings three-way, the local files untouched and ignored by the repository; personas adopt through `dev-resources` (2026-10-23-002) | Done | TMPL-1.2, TMPL-1.3, TMPL-1.4, TMPL-1.5 | doc_control_standard.md | 2026-10-22-001 |
| TMPL-1.7 | Proof: a scratch birth, a hook-driven cold start, a compaction re-injection observed, a forked closeout; a knowledge entry for the substrate. Done at S6: one live session on a fresh birth, the operator at the trust dialog; two closeout gaps fixed (2026-10-23-006) | Done | TMPL-1.6, TMPL-1.8, TMPL-1.9, TMPL-1.10 | session_handoff_standard_v2.0.md | 2026-10-22-001 |
| TMPL-1.8 | Persona library mechanism: `personas/` in the template, inactive, in the agent-file shape and linted as the roster is; `.claude/agents/` the project's roster; the first-session skill that asks which specializations the project needs, recommends from the library, drafts what it lacks and activates the chosen; the closeout's report of a library version newer than the roster's; the initializer, the updater and the sanitizer following; the five existing personas moved into the library; the `dev-resources` sync removed from the template, since it would write every persona into the roster (script, hook, closeout rule, stamp; the shared knowledge entry made the template's own); the supersessions marked on both sides. Done at S5: twenty broken variants caught; plants refused; a scratch birth's session lists no library persona | Done | TMPL-1.6 | session_handoff_standard_v2.0.md | 2026-10-23-003 |
| TMPL-1.9 | The full team in the library: roles across the software development lifecycle, data science, document management, writing including technical writing, and quality control, designed with the operator, each persona written in the agent-file shape and linted. Done at S5: the team approved with BI, reporting and game roles added (2026-10-23-004) | Done | TMPL-1.8 | session_handoff_standard_v2.0.md | 2026-10-23-003 |
| TMPL-1.10 | Adoption from `v1.0.0`: the updater converts a project's `docs/personas/` into `.claude/agents/` and settles its synced knowledge entries and stamp, proved against the real `v1.0.0` persona files (the sync itself left the template in TMPL-1.8). Done at S6: every real persona file converts to its library copy byte for byte; scratch adoptions of the three projects green after a `.gitignore` conflict resolved by hand (2026-10-23-005) | Done | TMPL-1.8 | doc_control_standard.md | 2026-10-23-003 |

---

## Epic: TMPL-2 — Authoritative documents (v2.0.0, decision 2026-10-22-002)

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| TMPL-2.1 | `scripts/doc_authority_scan.py`: `authority:` frontmatter and version logs, `Affects:` on decisions, the row-or-story rule, the fact marker, `--stamp` verified against git, `--history`; fixtures proved against broken variants; runbook section. Done at S7: a row is a `fact:` or a story's change, `**Affects:**` from decisions dated 2026-10-22, the template's rows verified in the template, one scope one authority (2026-10-23-010) | Done | — | doc_control_standard.md | 2026-10-22-002 |
| TMPL-2.2 | The `doc-queue` gate run at cold start by the `SessionStart` hook, over the stories marked `Queued: S<N>`, with its section in `docs/governance/gate_suite_runbook.md`; the per-document forked drain skill, as `general-purpose` in the role of the library's `technical-writer` (written in TMPL-1.9; `dev-resources` retired by 2026-10-23-003), leaving its change for review (2026-10-23-016) | Done | TMPL-2.1, TMPL-1.3, TMPL-1.9 | session_handoff_standard_v2.0.md | 2026-10-22-002 |
| TMPL-2.3 | The document-control standard rewritten around the gate; the standards and the gate runbook marked as authorities with version logs; the "stays private" fossil fixed; `sprint/recovery/AUTHORITY_MATRIX.md` retired into the frontmatter registry (2026-10-23-010). Done at S7: six authorities, their logs citing every decision that names them, one queued in TMPL-5.5 (2026-10-23-011) | Done | TMPL-2.1 | doc_control_standard.md | 2026-10-22-002 |
| TMPL-2.4 | Proof on a scratch project; `v2.0.0` released with TMPL-1.7; the three derived projects taken to it through `template_update.py`, each suite green, each project's `docs/personas/` converted by the updater into its roster and every converted persona checked (2026-10-23-003), and each told that its `sprint/recovery/AUTHORITY_MATRIX.md`, `v1.0.0`'s unedited, is now its own to delete (2026-10-23-011); then `dev-resources` archived, no project syncing from it any longer. Each project's existing PRD and architecture are approved as they stand in its adoption commit, Supplier_Research_Dev's missing architecture skipped by the Chair (2026-10-24-003, settling the open question found after the S10 closeout). Done at S11: scratch adoptions first; `v2.0.0` at `a159053`; the three adopted, pushed and green; `dev-resources` archived; [[reference_v2_adoption]] | Done | TMPL-2.2, TMPL-2.3, TMPL-1.7, TMPL-2.5, TMPL-5.4, TMPL-5.6, TMPL-2.6, TMPL-2.7, TMPL-2.8, TMPL-2.9, TMPL-5.7 | session_handoff_standard_v2.0.md | 2026-10-22-002 |
| TMPL-2.5 | The updater merges `.gitignore` by union: `git merge-file --union` for that path alone, named in the dry run; fixtures proved against broken variants; a scratch adoption of the three projects with no `.gitignore` conflict. Done at S7: the dry run names it `union`; the three scratch adoptions of a scratch `v2.0.0` had no conflict and passed the suite | Done | — | doc_control_standard.md | 2026-10-23-007 |
| TMPL-2.6 | The authority gate in a project: `scripts/doc_authority_scan.py` judges the template's rows and decisions in the template, since their stories and commits are the template's, and finds a row's commit following renames but never a copy; fixtures proved against broken variants; `docs/governance/gate_suite_runbook.md` and [[reference_doc_authority]] say so. Found at S8 by TMPL-5.1's birth probe, which a birth from `HEAD` failed. Done at S8: a scratch birth starts green and a PRD made from its template stamps its own commit (2026-10-23-015) | Done | TMPL-2.1, TMPL-2.3 | doc_control_standard.md | 2026-10-23-015 |
| TMPL-2.7 | CI makes a scratch project on every push: `scripts/birth_probe.py` births a committed revision through the initializer, its verdict the initializer's own suite run; `.github/workflows/gates.yml` runs it once per profile, in the template only; proved red at `38c549d` and green at its own commit; [[reference_ci_backstop]] says why | Done | TMPL-2.6 | doc_control_standard.md | 2026-10-23-017 |
| TMPL-2.8 | A copy of the template before its initializer, GitHub's "Initial commit", judges the template's rows in the template as a project does, its history holding none of their stamped commits; `scripts/birth_probe.py` also runs the suite on the Initial commit, as GitHub does; red at `30677d3`, green at its own commit (2026-10-23-023) | Done | TMPL-2.6, TMPL-2.7 | doc_control_standard.md | 2026-10-23-023 |
| TMPL-2.9 | `doc-authority-scan` refuses an `**Affects:**` value naming an authoritative document's path outside a code span, which it otherwise does not read, and prints the fix; `docs/templates/README.md` step 5 says the path goes in a code span; fixtures proved against broken variants; `docs/governance/gate_suite_runbook.md` and [[reference_doc_authority]] say so. Found at S11 by TMPL-5.4: the probe's PRD approval named the PRD bare and passed unchecked; the Chair's choice of fix. Done at S11: the `bare-path` rule, seven fixtures, five broken variants caught, the real tree passing (2026-10-24-001) | Done | TMPL-2.1 | doc_control_standard.md | 2026-10-22-002 |

---

## Epic: TMPL-3 — The agentic development team (v2.1.0, decision 2026-10-22-003)

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| TMPL-3.1 | Design session with the operator: over the library's team (designed in TMPL-1.9, 2026-10-23-003), the artifact each role produces and the gate that judges it, the review-trigger list, the orchestration shape; logged as decisions. Done at S12 with the Chair: the orchestration (2026-10-24-004), the eleven triggers (2026-10-24-005), the role map by story type covering every library persona (2026-10-24-006) | Done | TMPL-2.4 | sprint_management_standard_v1.0.md | 2026-10-22-003 |
| TMPL-3.2 | Build: the role agents, their skills, the saved workflow, the trigger list as a gate; proof on one project through a story end to end. Scoped at S12 by decisions 2026-10-24-004 to -006: `docs/standards/team_standard_v1.0.md` (the stages, the role map, the eleven triggers), the main-session `/story <ID>` skill, the `story-artifacts` gate over `docs/stories/<ID>/` with its trigger detection, fixtures proved against broken variants, the runbook sections, `AGENTS.md`'s skills table and the README's catalog | Not Started | TMPL-3.1, TMPL-4.2 | doc_control_standard.md | 2026-10-22-003 |

---

## Epic: TMPL-4 — The coding standard (v2.1.0, decision 2026-10-22-003)

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| TMPL-4.1 | Design session with a specialized reviewer agent: the core limits as numbers, the per-stack tool-mapping rule, the one judgement page; proved against a known-good and a known-bad codebase before adoption; logged. Done at S13 with the Chair and a reviewer agent: the limits proved against ripgrep, packaging and zod and the Gilded Rose and Tennis katas (2026-10-24-007), proved measurement and the mapping rule (2026-10-24-008), the judgement page and the reviewer and auditor briefs (2026-10-24-009); [[reference_coding_standard_calibration]] | Done | TMPL-2.4 | doc_control_standard.md | 2026-10-22-003 |
| TMPL-4.2 | Build: the core gates as a stack profile in the suite, the `.claude/rules/` page, the reviewer and auditor briefs; proof on one project. Scoped at S13 by decisions 2026-10-24-007 to -009: `docs/standards/coding_standard_v1.0.md`, stack profiles for Rust, Python and TypeScript with pinned tools each proved by its measurement fixture and the recall check, the gate over changed functions (limits, new clones, coverage of new lines, the exceptions file), `.claude/rules/code-quality.md`, `personas/code-reviewer.md`, fixtures proved against broken variants, the runbook sections; the proof on one project | Not Started | TMPL-4.1 | doc_control_standard.md | 2026-10-22-003 |

---

## Epic: TMPL-5 — The project launch (v2.0.0, decision 2026-10-23-008)

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| TMPL-5.1 | The PRD and architecture templates: their sections, frontmatter in TMPL-2.1's `authority:` format, a version log, and the version of the document each was built from. Done at S8: `docs/templates/prd.md` and `docs/templates/architecture.md`, each the authority for its own scope, and `docs/templates/README.md`; a made document a draft until approved; proved on a scratch birth (2026-10-23-014) | Done | TMPL-2.1 | doc_control_standard.md | 2026-10-23-008 |
| TMPL-5.2 | `/project-launch`: intake by three questions or a PRD summary with its gaps; team through team-selection; the PRD interview in the product manager's role, saved as it grows; architecture; planning; each stage's opening with pause, skip (logged), return and status; a revision as a new version that flags the stages built on it; the S1 entry's one next step; listed in `AGENTS.md` and held by `skill-scan` | Done | TMPL-5.1, TMPL-1.8 | sprint_management_standard_v1.0.md | 2026-10-23-008 |
| TMPL-5.3 | The approval gate: in a project, a real epic needs an approved PRD and an approved architecture, or a logged skip of either; fixtures proved against broken variants; a runbook section if it is a hook of its own | Done | TMPL-5.1 | doc_control_standard.md | 2026-10-23-008 |
| TMPL-5.4 | Proof: a scratch birth and one live session with the Chair at the keyboard through every stage, with a pause, a skip and a return to revise an approved document, following the README's walkthrough as written; observations recorded as seen. Done at S11: three runs on `SaltyBrett/launch-probe-s10`, the last through approval, a skip with its reason, planning, a revision read stale and the first closeout, its `gates` run green; [[reference_launch_live_run]] | Done | TMPL-5.2, TMPL-5.3, TMPL-5.5 | session_handoff_standard_v2.0.md | 2026-10-23-008 |
| TMPL-5.5 | The root README as the operator's front page: a step-by-step walkthrough from creating a project through `/project-launch`, the session loop and taking a release, then a catalog of every command, operator script and session hook, the gates by link to the runbook; `TEMPLATE_GUIDE.md` cut to what the initializer does not do; `skill-scan` refusing a skill the catalog does not name, its section in `docs/governance/gate_suite_runbook.md` saying so | Done | TMPL-5.2 | doc_control_standard.md | 2026-10-23-009 |
| TMPL-5.6 | Four library personas in the agent-file shape and linted (a backend engineer, a web developer, a Blender 3D artist, an image and video editor); team presets in team-selection (Application development, Website, Imaging, video and 3D), membership confirmed with the Chair, a gate refusing a preset that names no library persona, proved against broken variants; an opt-in Blender MCP connection offered with the Blender persona, the server vetted and pinned, off by default. Done at S8: `backend-engineer`, `web-developer`, `blender-artist`, `image-video-editor`; presets and connections one block held by `skill-scan`; the Blender Lab server pinned to v1.0.3's commit; `docs/governance/gate_suite_runbook.md` says so (2026-10-23-013) | Done | TMPL-1.9 | session_handoff_standard_v2.0.md, secrets_management_standard_v1.0.md | 2026-10-23-012 |
| TMPL-5.7 | `session-closeout` refuses to close a session whose sprint-status entry is still an emergency checkpoint, headed `emergency checkpoint` or holding the initializer's `### Next` section, and sends it back to the session to bring up to date; `AGENTS.md`'s emergency close says the completing session rewrites the entry; fixtures proved against broken variants; `docs/governance/gate_suite_runbook.md` and [[reference_session_closeout]] say so. Found at S11 by TMPL-5.4: the probe's first closeout, typed as `/closeout` and so run as the fork, closed S1 on an entry saying its closeout was not completed; the Chair's choice of fix. Done at S11: `unfinished_entry` in `--closeout`, nine fixtures, seven broken variants caught, proved on a scratch clone of the real tree (2026-10-24-002) | Done | TMPL-5.4 | session_handoff_standard_v2.0.md | 2026-10-23-008 |

---

## Epic: INFRA-1 — Environment Setup [EXAMPLE]

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| INFRA-1.1 | Provision development environment | Not Started | — | secrets_management_standard_v1.0.md | — |
| INFRA-1.2 | Configure CI/CD pipeline | Not Started | INFRA-1.1 | doc_control_standard.md | — |
| INFRA-1.3 | Set up monitoring | Not Started | INFRA-1.1 | — | — |

---

<!-- Add new epics and stories below, following the table format above -->
<!-- Update status after each work unit per the Checkpoint Protocol -->
