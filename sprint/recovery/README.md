# Recovery Orchestration Framework (Control Plane)

This folder is the **drift-proof control plane** for multi-agent recovery and reconciliation work.

## Purpose

When work spans multiple sessions or agents, artifacts can drift — two files may contradict each other, or a decision may be implemented inconsistently. This framework prevents that.

## Rules

1. **Single Source of Truth:** The `AUTHORITY_MATRIX.md` in this folder maps every concern to exactly one authoritative artifact. If it's not in the matrix, it's not authoritative.

2. **Handoff Required:** A recovery session closes out like any other — the standard handoff/kickoff pair, verified by `scripts/session_closeout.py` (`docs/standards/session_handoff_standard_v2.0.md`). Drift gates executed and their evidence go in the handoff's "Verification observed" section and in an evidence record.

3. **Evidence:** a validation result is recorded in the shape of `templates/VALIDATION_EVIDENCE_TEMPLATE.md`
   under `evidence/<date>/<artifact>/`. No gate checks this; it is procedure, not a control
   (decision 2026-09-24-001).

4. **Escalate Ambiguity:** If two artifacts claim authority for the same concern, escalate to the user. Do not guess which is correct.

## Contents

| File | Purpose |
|------|---------|
| `AUTHORITY_MATRIX.md` | Maps concerns to authoritative artifacts |
| `templates/VALIDATION_EVIDENCE_TEMPLATE.md` | Evidence capture for audit trails |
