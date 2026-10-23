# Handoff — S4

**For session:** S4
**Written by:** S3
**Written:** 2026-10-22

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S4.md`
- `docs/governance/framework_decisions.md` 2026-10-22-001 (procedures as forked skills is its fifth bullet; TMPL-1.4 builds it), then 2026-10-22-005 and 2026-10-22-006, which S3 built on top of it
- [[reference_claude_code_agents_md]] — what a subagent loads at start, and that under `claude --agent` an agent's body replaces Claude Code's own system prompt; which agent a forked skill runs as is the same question
- [[reference_claude_code_rules]] — the path-scoped sibling of skills, and the gate shape to copy: every silent failure Claude Code has is checked
- [[reference_gate_runbook]] — the runbook gate the skill gate mirrors (every command a skill names must exist in the config)
- [[reference_template_update]] and [[reference_template_sanitizer]] — the ownership map and the sanitizer TMPL-1.6 extends
- `docs/standards/session_handoff_standard_v2.0.md` §7 and `docs/standards/sprint_management_standard_v1.0.md` — two of the procedures TMPL-1.4 moves into skills

## 2. Completed last session

- TMPL-1.3 — personas are agent files in `.claude/agents/`; `scripts/session_closeout.py`, `scripts/session_start.py`, `scripts/resources_sync.py`, `.pre-commit-hooks.yaml` and the docs follow; `dev-resources` holds both trees (commits 386d7b6, 0db600e; `dev-resources` 9002dfb)
- TMPL-1.5 — four rules in `.claude/rules/`, gated by `session-closeout-check`; `CONSTITUTION.md` §6.3 a pointer to [[reference_kb_freshness]] (commits 83c7099, 732d3b5)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-22-005 Personas are agent files; the start hook gives the session its persona, `claude --agent` optional; `dev-resources` holds both trees until TMPL-2.4; amends 2026-10-22-001
- 2026-10-22-006 Rules under `.claude/rules/` are path-scoped judgement only, and gated

## 5. Blockers and open questions

- 2026-10-22-006 was made by the agent within 2026-10-22-001 and is put to the operator at this handover; if the operator overturns "path-scoped or refused", the `rule-paths` check in `lint_rule` goes.
- `AGENTS.md`'s section "Workflows are portable markdown, not tool skills" says a skill is never the source of truth, while 2026-10-22-001 makes the `SKILL.md` the one home of a procedure. TMPL-1.4 reconciles them before moving anything.
- From S2, still unobserved: the first interactive session in a fresh clone (hooks wait for the trust dialog), and `disableWorkflows` in a live session.
- That `--agent` replaces Claude Code's system prompt rests on the sub-agents page and a 2,500-token difference in prompt size; it was not observed directly.

## 6. Verification observed

- cold start: the `SessionStart` hook ran the identity gate (PASS), `git pull` (exit 0) and `session-verify` (PASS); both hook types installed; `gh` on the keyring; Claude Code 2.1.308
- TMPL-1.3: self-tests 87/87, 28/28, 18/18; 22 broken variants, each caught; live in scratch clones: agent run and plain run each held the persona, `agent_type` present only in the first; unbumped body edit exit 1, bumped exit 0; the published hook refused the same edit in `dev-resources`; `dev-resources` `gates` run 39884359420 green, the template's 39884095218 green; sync back all `up-to-date`, stamp `main 9002dfb`; a scratch clone of Comfy still resolved every persona
- TMPL-1.5: self-test 102/102; 15 broken variants, each caught; canary absent, present, absent; unscoped and dead rules refused by name; the clause-copy plant passed the first check and fails the second
- `pre-commit run --all-files` exit 0 at every checkpoint (the banned-feature scan refused one draft rule, reworded); this closeout ran `session-closeout` at the manual stage and watched the push's `gates` run with `gh run watch --exit-status`
