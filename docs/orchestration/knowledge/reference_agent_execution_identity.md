---
name: Agent execution identity — no sandbox execution; ask for approval
description: 'No agent may create, configure, or execute through a sandbox account, identity, restricted token, or isolated OS principal. Commands run only under the operator''s already-authenticated identity, via the interactive approval path. Read before any agent command.'
teaches: [2026-07-30-001]
verified: 2026-07-30
metadata:
  type: decision
---

# Agent execution identity — no sandbox execution; ask for approval

> **Provenance stamps.** `teaches:` lists the decisions this entry EXPLAINS; `verified:` is when it was
> last confirmed against them. `scripts/kb_freshness_scan.py` fails the commit if a taught decision
> changed after that date. See CONSTITUTION §6.3.

## Absolute rule

No agent working from a repository created from this template may create, configure, resolve, log on
as, impersonate, or execute through a sandbox account, sandbox identity, restricted sandbox token,
private sandbox desktop, or equivalent isolated OS principal. This includes native-Windows Codex
`elevated` and `unelevated` sandbox execution. Commands run only under the operator's
already-authenticated OS identity.

When a session exposes a `read-only` / `workspace-write` sandbox boundary, request operator escalation
before every local command—including the first cold-start command—so the process runs as the existing
operator. Never try the sandbox first and escalate only after failure. The permission labels are not
themselves proof of a forbidden identity and are not a hard stop.

An already-unsandboxed operator session retains `approval_policy = "untrusted"` with
`approvals_reviewer = "user"`: only known-safe reads may run without a prompt; other commands remain
user-reviewed. Stop when escalation is unavailable or the approved process would still execute as a
Sandbox/Codex-Offline identity.

## Mechanical controls

1. `.codex/config.toml` requests `untrusted`, user-reviewed approvals and deliberately does not force
   a sandbox mode.
2. `AGENTS.md` carries the zero-th gate and makes the identity guard the first cold-start command.
3. `scripts/agent_execution_identity_guard.py` checks execution-name markers and project approval
   configuration.
4. `.pre-commit-config.yaml` runs the identity guard before other drift gates.

The script is defense in depth. It cannot prove that the agent requested an approval before invoking
it; the pre-command instruction remains the primary control.

## Official Codex basis

Codex documents sandbox scope and approval policy as separate controls. The Full access preset removes
sandbox restrictions and approval prompts; the portable template instead preserves no-sandbox
operator execution with user-reviewed approvals.

- <https://learn.chatgpt.com/docs/agent-approvals-security.md>
- <https://learn.chatgpt.com/docs/permission-modes.md>
- <https://learn.chatgpt.com/docs/config-file/config-reference.md>
- <https://learn.chatgpt.com/docs/windows/windows-sandbox.md>
