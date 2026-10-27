# Recovery Orchestration Framework (Control Plane)

This folder is the **drift-proof control plane** for multi-agent recovery and reconciliation work.

## Purpose

When work spans multiple sessions or agents, artifacts can drift: two files may contradict each other, or a decision may be implemented inconsistently. This framework prevents that.

## Rules

1. **Single Source of Truth:** an authoritative document declares its scope in its own frontmatter (`authority:`), and `python3 scripts/doc_authority_scan.py --list` prints every one. The gate refuses two documents claiming one scope (`docs/governance/doc_control_standard.md`).

2. **Handoff Required:** A recovery session closes out like any other: the standard handoff/kickoff pair, verified by `scripts/session_closeout.py` (`docs/standards/session_handoff_standard_v2.0.md`). Drift gates executed and their evidence go in the handoff's "Verification observed" section and in an evidence record.

3. **Evidence:** a validation result is recorded in the shape of `templates/VALIDATION_EVIDENCE_TEMPLATE.md`
   under `evidence/<date>/<artifact>/`. No gate checks this; it is procedure, not a control.

4. **Escalate Ambiguity:** If two artifacts disagree and neither is an authority for the concern, escalate to the user. Do not guess which is correct.

## Contents

| File | Purpose |
|------|---------|
| `templates/VALIDATION_EVIDENCE_TEMPLATE.md` | Evidence capture for audit trails |
