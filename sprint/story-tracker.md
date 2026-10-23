# Story Tracker

**Last Updated:** {{DATE}}
**Source:** PRD (see `docs/prd/`)

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` — read it before creating or
> updating stories (use its Planning Session Protocol to build this file from the PRD + Architecture).
>
> **READ SELECTIVELY (index-first).** Do NOT read this file whole. Read the **Summary Statistics** and
> **Dependency Order** below, then open only the epic/story rows relevant to the current task. Keep this
> file markdown (never JSON) and do not accrete changelog paragraphs.

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Stories** | 15 |
| **Not Started** | 14 |
| **In Progress** | 0 |
| **Blocked** | 0 |
| **Completed** | 1 |

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
| TMPL-1.2 | Hooks: `SessionStart` (startup and `compact`) running the gates and injecting results, kickoff and newest entry; `Stop` refusing an uncommitted or unbanked turn; `PostToolUse` journal and the working-notes file under `sprint/recovery/`; `disableWorkflows`; `ask` rules for the one-way doors; `PreCompact` tested as a backstop | Not Started | TMPL-1.1 | session_handoff_standard_v2.0.md | 2026-10-22-001 |
| TMPL-1.3 | Personas to `.claude/agents/`: `persona-lint` and `resources_sync.py` repointed, the kickoff names the agent, `session_closeout.py` rules updated, the registry republished to `dev-resources` | Not Started | TMPL-1.1 | session_handoff_standard_v2.0.md | 2026-10-22-001 |
| TMPL-1.4 | Procedures to forked skills: closeout, release cut, planning session, sanitize-and-cut, document production; the standards shrink to the law; a gate keeps each skill's commands in step with the config | Not Started | TMPL-1.2, TMPL-1.3 | sprint_management_standard_v1.0.md | 2026-10-22-001 |
| TMPL-1.5 | Path-scoped rules under `.claude/rules/`; `CONSTITUTION.md` slimmed (§2 a pointer, §6.3 a pointer to the knowledge entry); the checklist reduced to what a script does not already prove | Not Started | TMPL-1.1 | doc_control_standard.md | 2026-10-22-001 |
| TMPL-1.6 | Ownership of the new paths in the initializer, the updater and the sanitizer (`.claude/agents`, `.claude/skills`, `.claude/rules`, `.claude/settings.json`, the journal and notes), with fixtures proved against broken variants | Not Started | TMPL-1.2, TMPL-1.3, TMPL-1.4, TMPL-1.5 | doc_control_standard.md | 2026-10-22-001 |
| TMPL-1.7 | Proof: a scratch birth, a hook-driven cold start, a compaction re-injection observed, a forked closeout; a knowledge entry for the substrate | Not Started | TMPL-1.6 | session_handoff_standard_v2.0.md | 2026-10-22-001 |

---

## Epic: TMPL-2 — Authoritative documents (v2.0.0, decision 2026-10-22-002)

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| TMPL-2.1 | `scripts/doc_authority_scan.py`: `authority:` frontmatter and version logs, `Affects:` on decisions, the row-or-story rule, the fact marker, `--stamp` verified against git, `--history`; fixtures proved against broken variants; runbook section | Not Started | — | doc_control_standard.md | 2026-10-22-002 |
| TMPL-2.2 | The `technical-writer` agent published to `dev-resources`; the `doc-queue` gate run at cold start by the `SessionStart` hook; the per-document forked drain skill | Not Started | TMPL-2.1, TMPL-1.3 | session_handoff_standard_v2.0.md | 2026-10-22-002 |
| TMPL-2.3 | The document-control standard rewritten around the gate; the standards and the gate runbook marked as authorities with version logs; the "stays private" fossil fixed | Not Started | TMPL-2.1 | doc_control_standard.md | 2026-10-22-002 |
| TMPL-2.4 | Proof on a scratch project; `v2.0.0` released with TMPL-1.7; the three derived projects taken to it through `template_update.py`, each suite green | Not Started | TMPL-2.2, TMPL-2.3, TMPL-1.7 | session_handoff_standard_v2.0.md | 2026-10-22-002 |

---

## Epic: TMPL-3 — The agentic development team (v2.1.0, decision 2026-10-22-003)

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| TMPL-3.1 | Design session with the operator: roles, the artifact each produces and the gate that judges it, the review-trigger list, the orchestration shape; logged as decisions | Not Started | TMPL-2.4 | sprint_management_standard_v1.0.md | 2026-10-22-003 |
| TMPL-3.2 | Build: the role agents, their skills, the saved workflow, the trigger list as a gate; proof on one project through a story end to end | Not Started | TMPL-3.1, TMPL-4.2 | doc_control_standard.md | 2026-10-22-003 |

---

## Epic: TMPL-4 — The coding standard (v2.1.0, decision 2026-10-22-003)

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| TMPL-4.1 | Design session with a specialized reviewer agent: the core limits as numbers, the per-stack tool-mapping rule, the one judgement page; proved against a known-good and a known-bad codebase before adoption; logged | Not Started | TMPL-2.4 | doc_control_standard.md | 2026-10-22-003 |
| TMPL-4.2 | Build: the core gates as a stack profile in the suite, the `.claude/rules/` page, the reviewer and auditor briefs; proof on one project | Not Started | TMPL-4.1 | doc_control_standard.md | 2026-10-22-003 |

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
