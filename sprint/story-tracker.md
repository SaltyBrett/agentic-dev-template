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
| **Total Stories** | 0 |
| **Not Started** | 0 |
| **In Progress** | 0 |
| **Blocked** | 0 |
| **Completed** | 0 |

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
