---
paths:
  - "sprint/**"
---

# Editing the sprint documents

The law: `docs/standards/sprint_management_standard_v1.0.md`, and for handoffs `docs/standards/session_handoff_standard_v2.0.md`; the procedures that write these files are the planning-session and closeout skills. What the gates hold these files to:

- A session's entry in `sprint/sprint-status.md` opens with `## S<N> - YYYY-MM-DD - <title>`, written at its first checkpoint; every session gate reads N from that line, written with hyphens and in no other form. The entry holds Status, Done and Blockers; the next session's tasks belong in its kickoff.
- A tracker status and the Summary Statistics change in the same edit, since `session-closeout-check` recounts the rows. A story goes In Progress or Done only once every listed dependency is Done (`dependency-order`).
- Handoff and kickoff headings come from the closeout skill's scaffold step, never typed; a pair lives one session and has no section for durable content.
- `sprint/recovery/WORKING_NOTES.md` stays newer than every uncommitted change, or the `Stop` hook sends the turn back; the notes and the journal are gitignored.
