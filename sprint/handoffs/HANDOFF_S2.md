# Handoff — S2

**For session:** S2
**Written by:** S1
**Written:** 2026-10-22

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S2.md`
- `docs/governance/framework_decisions.md` 2026-10-22-001 — the whole design of `v2.0.0`: what moves to Claude's native machinery, what stays as git hooks and CI, and why; TMPL-1.1 and TMPL-1.2 are its first two stories
- `sprint/story-tracker.md` epics TMPL-1 and TMPL-2 — fifteen stories, dependency order set; TMPL-2.1 (the document-authority gate) has no dependency and is the one story that can run beside TMPL-1 if a session has room
- `CONSTITUTION.md` §2 and `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md` — the copies of the cold start that TMPL-1.1 collapses into `AGENTS.md`; read them to know what each says that the others do not, so nothing is lost in the collapse
- `AGENT_INTEROP.md` — retired by TMPL-1.1 into `AGENTS.md`; its §1 and §1A are already prime directives there, its §4 index-first rule is in `AGENTS.md` Conventions, and the rest is rationale
- [[reference_session_closeout]] — the pair's structural rules the kickoff lint enforces; TMPL-1.3 later changes the persona rules, TMPL-1.1 must not
- [[reference_precommit_stash]] — every manual-stage gate with `--all-files`; the `SessionStart` hook in TMPL-1.2 calls them the same way
- [[reference_execution_identity_config]] — the identity gate reads `.codex/config.toml`; TMPL-1.1 keeps that file and the gate, since removing Codex is not in the decision

## 2. Completed last session

- Planning only: decisions 2026-10-22-001, -002, -003 logged; epics TMPL-1 to TMPL-4 opened with fifteen stories; the S1 entry records the measurements (a 74 KB cold start across ten files, the procedure in four places) and the Claude Code version finding (2.1.267 installed; native `AGENTS.md` needs 2.1.277)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-22-001: `v2.0.0` runs the framework on Claude Code's native machinery
- 2026-10-22-002: authoritative documents stop going stale
- 2026-10-22-003: `v2.1.0` is the development team and the coding standard, designed first

## 5. Blockers and open questions

- Hook field names and the `PreCompact` blocking semantics were read from a docs summary, not the reference page; TMPL-1.2 checks each against `https://code.claude.com/docs/en/hooks.md` before writing a hook, and records what it found in the knowledge entry.
- `CLAUDE.md` is retired only when `claude --version` reports 2.1.277 or later on the operator's machine; until then it stays as the `@AGENTS.md` bridge. Check at the start of TMPL-1.1 and write the result into the story's row.
- The three derived projects (`Supplier_Research_Dev`, `Comfy`, `PocketGames`) are at `v1.0.0` and are TMPL-2.4's adoption proof; nothing is pushed to them before the release.

## 6. Verification observed

- cold start: identity gate PASS, `session-verify` exit 0 at S1 with no pair, `kb-freshness-scan` exit 0
- after the planning edits: `pre-commit run --all-files` exit 0 with the state gate reconciling 15 stories, all Not Started, no dependency violation; `kb_freshness_scan.py --list` exit 0 with the three new decisions indexed; the sync in step at `main 904e0bc`
- this closeout: `session-closeout` exit 0 at the manual stage; the push's `gates` run green, its ID in the Actions history
