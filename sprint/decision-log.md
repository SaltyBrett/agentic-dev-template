# Architectural Decision Log

**Purpose:** Document all significant architectural and design decisions with rationale
**Last Updated:** {{DATE}}

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (what to log and when).
>
> **READ SELECTIVELY (index-first).** This is an append-only log. Do NOT read it whole. Read the
> **Decision Index** below, then open only the entries relevant to the current task. Keep this file
> markdown (never JSON) and do not accrete changelog paragraphs; add discrete dated entries only.
>
> **This is the project's log.** Prefix each ID with the project's story prefix
> (`ACME-2026-09-24-001`).

---

## How to Use This Log

- Every significant decision gets an entry
- Include rationale so future sessions understand WHY
- Reference relevant standards or constraints
- Update status if decisions are revised
- Use format: `[YYYY-MM-DD-NNN]` for decision IDs

---

## Decision Index

| ID | Date | Title | Status |
|----|------|-------|--------|
| [EXAMPLE] ACME-2025-01-15-000 | 2025-01-15 | Orchestration Framework Selection | APPROVED |

---

## Decision [EXAMPLE] ACME-2025-01-15-000: Orchestration Framework Selection

**Date:** 2025-01-15
**Made By:** Human + AI (Session 1)
**Status:** APPROVED
**Affects:** none

### Context

Needed to select an orchestration approach for multi-session AI agent continuity. Options considered:
1. Memory-based (agent remembers context)
2. File-based state management (sprint-status.md, story-tracker.md, decision-log.md)
3. Database-backed tracking

### Decision

**File-based state management** using markdown files committed to Git.

### Rationale

- Git provides audit trail and versioning for free
- Markdown files are human-readable without tooling
- AI agents can read/write files natively
- No external database dependency
- Portable across any development environment

### Consequences

- State files must be updated after every work unit (checkpoint protocol)
- All agents must follow the Session Startup Protocol to read state files
- Decision supersession chains must be tracked (SUPERSEDED status)

### Related

- Constitution Section 2.2 (Session End Protocol)
- Session Handoff Standard v1.0

---

<!-- Add new decisions above this line, following the template above -->
<!-- Valid statuses: APPROVED | VALIDATED | SUPERSEDED | HYPOTHESIS | CONFIRMED | DENIED -->
