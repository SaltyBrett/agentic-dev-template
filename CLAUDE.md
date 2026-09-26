@AGENTS.md

# CLAUDE.md — Claude Code bridge

> The canonical brain is **`AGENTS.md`**, imported above (Claude Code loads `@`-imports in full at
> session start). This file adds **Claude-only accelerators**; it is never a second source of truth,
> so it cannot drift from the brain. Codex reads `AGENTS.md` directly and ignores this file.

## Claude Code only (accelerators)

- **Plan-first:** start non-trivial changes in Plan mode (shift+tab twice), iterate on the plan, then
  auto-accept edits — a good plan usually one-shots the work. Always use Plan mode for security-,
  compliance-, or billing-sensitive paths.
- **Subagents** for investigation/search, to keep the main context clean.
- **`.claude/rules/`** may hold path-scoped rules as a Claude-only convenience. Anything that must also
  reach Codex belongs in repo markdown (`docs/standards/`, `CONSTITUTION.md`) — not only in `.claude/`.
- **Permissions / hooks** in `.claude/settings.json` are Claude-only. A conservative starter ships in
  this repo (pre-allows safe read-only git + the banned-feature scan; denies force-push / hard-reset) —
  tune it to your toolchain and keep it checked in so the team shares one allow-list. The portable,
  tool-neutral gate remains the git pre-commit hook (`.pre-commit-config.yaml` → `scripts/banned_feature_scan.py`).
