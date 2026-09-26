# Authority Matrix — Single Source of Truth Map

**Goal:** For every concern, identify exactly one "CURRENT" artifact, and mark all others as superseded/archived.

**Rule:** If two artifacts claim to be CURRENT for the same concern, STOP and escalate to the user for resolution.

---

## How to Use

1. Before working on any recovery or reconciliation task, check this matrix
2. Only the artifact marked CURRENT is authoritative
3. If a new artifact supersedes an existing one, update this matrix
4. Never create a new artifact for a concern that already has a CURRENT entry without marking the old one SUPERSEDED

---

## Authority Map

| Concern | CURRENT Artifact | Superseded | Notes |
|---------|-----------------|------------|-------|
| Session Handoff Protocol | `docs/standards/session_handoff_standard_v2.0.md` | `session_handoff_standard_v1.0.md`; `sprint/recovery/templates/HANDOFF_TEMPLATE.md` (retired, 2026-09-21-001) | Governs all session transitions, recovery sessions included; enforced by `scripts/session_closeout.py` |
| Persona Registry | `docs/personas/` | — | One file per persona; a kickoff copies the Invocation block |
| Secrets Management | `docs/standards/secrets_management_standard_v1.0.md` | — | Key Vault + SPN authoritative |
| Document Control | `docs/governance/doc_control_standard.md` | — | GitHub-governed changes |

<!-- Add project-specific authority mappings below this line -->
<!-- Format: | Concern | Current artifact path | Superseded artifact(s) | Notes | -->

---

## Escalation Rule

**If you discover two artifacts that both claim authority over the same concern:**
1. STOP work on that concern
2. Document both artifacts and the conflict
3. Escalate to user for resolution
4. Do NOT pick one arbitrarily
