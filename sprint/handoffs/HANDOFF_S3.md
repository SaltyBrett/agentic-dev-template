# Handoff — S3

**For session:** S3
**Written by:** S2
**Written:** 2026-10-22

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S3.md`
- `docs/governance/framework_decisions.md` 2026-10-22-001 — personas as subagents and path-scoped rules are its fourth and sixth bullets; TMPL-1.3 and TMPL-1.5 build them
- [[reference_claude_code_hooks]] — the `SessionStart` hook now runs the cold start's gate steps and injects the kickoff; the `Stop` hook sends a turn back while a tracked sprint file is uncommitted or `sprint/recovery/WORKING_NOTES.md` is older than the newest uncommitted change, so keep the notes current as you work
- [[reference_session_closeout]] — the persona rules TMPL-1.3 changes: shape-gated, append-only by version against the committed copy, the kickoff copying the Invocation
- [[reference_resources_sync]] — the registry is a cache of `dev-resources`; a move of owned paths is published there, never made here alone
- [[reference_published_hooks]] — `persona-lint` is published by `.pre-commit-hooks.yaml` and `dev-resources` pins it by rev, so the move must keep both repositories' gates green between the two pushes
- [[reference_claude_code_agents_md]] — what a session and a subagent load at start; a persona as an agent changes what the main session reads

## 2. Completed last session

- TMPL-1.1 — one cold start in `AGENTS.md`; `CONSTITUTION.md` §2.1, §2.2, §2.4, the checklist and the handoff standard §8 point there; `CLAUDE.md` and `AGENT_INTEROP.md` deleted (commit f7016cf)
- TMPL-1.2 — `scripts/session_start.py`, `scripts/session_stop.py`, `scripts/session_journal.py`, registered in `.claude/settings.json` with `disableWorkflows` and the `ask` rules; three self-test hooks and runbook sections (commits a877d15, 95e5966)
- `scripts/session_closeout.py` `VERIFY_COMMAND`: the cold-start verify carries `--all-files`, and the scaffold writes it

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-22-004 The session journal and the working notes are local, never committed
- 2026-09-22-003 amended: the cold-start verify runs with `--all-files`, since the stash let a dirty tree pass

## 5. Blockers and open questions

- 2026-10-22-004 was made by the agent inside 2026-10-22-001 and put to the operator at the S2 handover; if the operator overturns it, the journal and notes become tracked and the concurrency proof in [[reference_claude_code_hooks]] says what that costs.
- Every S2 hook observation was a `claude -p` session, where project hooks run without a trust dialog. In an interactive session they wait for the folder to be trusted; the first interactive session in a fresh clone has not been observed.
- `disableWorkflows: true` is set in `.claude/settings.json` but was not exercised in a session.

## 6. Verification observed

- cold start: identity gate PASS; `main` had no upstream (set to `origin/main`, already equal); `session-verify` exit 0; `kb-freshness-scan` exit 0; both hook types installed; `gh` on the keyring
- TMPL-1.1: `pre-commit run --all-files` exit 0; a banned feature planted in the checklist blocked the scan once its exemption went; the native `AGENTS.md` read observed with a canary, and its loss beside a `CLAUDE.md`
- TMPL-1.2: self-tests 18/18, 21/21, 17/17; nineteen broken variants, each failing a fixture; live in scratch clones: startup injection, compaction re-injection, the `Stop` hook refusing then allowing, journal lines with exit codes, the four `ask` rules refusing; the ignored journal kept 2,400 of 2,400 lines beside nine stash windows and the tracked variant lost 2,306
- the stash defect: at the S1 closeout commit, `session-verify` without `--all-files` passed a tree with an unstaged edit; with the flag it failed on `dirty-tree`
- registry: `reference_macos_toolchain` published to `dev-resources` (c37ef16, its `gates` run 39880624205 green); `resources_sync.py --apply` PASSED, stamp `main c37ef160b17c`
- this closeout: `session-closeout` at the manual stage and `pre-commit run --all-files` before the commit; the push's `gates` run watched with `gh run watch --exit-status` before the hand-over
