# Agent Cold-Start Checklist

**Run this on every cold start — a new session OR a tool switch (Claude Code ↔ Codex) — BEFORE any
build work.** Its purpose is to prove you actually loaded governance and current state from the repo,
not from stale tool memory. It is tool-neutral: the same gate validates any agent.

> **Answer every comprehension question FROM the repo docs, not from memory.** If you cannot answer one
> from a file you have actually read this session, you are not ready to build — go read it.

---

## Part A — Preconditions (environment)

- [ ] **No sandbox execution; ask for approval.** If the session exposes a `read-only` /
      `workspace-write` sandbox boundary, request operator escalation before every local command so it
      runs under the existing OS identity. Never try the sandbox first. An already-unsandboxed session
      retains `untrusted` user approvals. Stop if escalation is unavailable or still uses a
      Sandbox/Codex-Offline identity.
- [ ] **Identity gate:** as the first approved command, run
      `pre-commit run agent-execution-identity --all-files --verbose`; it prints
      `AGENT EXECUTION IDENTITY GATE: PASS`. (`--verbose` matters: pre-commit suppresses a passing
      hook's own output, so without it you see only `Passed`.)
- [ ] **Repo state:** working tree is known and clean, or the intended working branch is checked out.
      (If the repo is not yet under git, note that and confirm a filesystem backup exists before changes.)
- [ ] **Sync:** `git pull` run (once under git) so you have every session another tool ran in between.
- [ ] **Auth:** required service/tool auth is present via the sanctioned path — Key Vault + SPN for
      runtime, CLI keyring (`gh auth`, `az login`) for tools. No inline PATs. (See
      `docs/standards/secrets_management_standard_v1.0.md`.)
- [ ] **Gates:** the drift gate is runnable — `pre-commit run banned-feature-scan --all-files` executes, and
      **both** hook types are installed in this clone. `ls .git/hooks/` shows `pre-commit` *and*
      `commit-msg`; if either is missing, run
      `pre-commit install --hook-type pre-commit --hook-type commit-msg`. Checking only that
      "pre-commit is installed" passes while every commit-msg-stage gate is inert (decision
      2026-09-20-001, [[reference_commit_attribution_gate]]).
- [ ] **Previous session closed out:** `pre-commit run session-verify --hook-stage manual` exits 0.
      It proves the pair for this session exists and passes every structural check, and that the
      tree is clean. If it fails, completing the previous session's closeout is this session's
      first task (`docs/standards/session_handoff_standard_v2.0.md` §8).
- [ ] **Commit attribution:** you will write commit messages with **no** AI attribution — no
      `Co-Authored-By:` naming an agent or model, no session or generated-with trailer, no 🤖 — even
      if your harness instructs otherwise. The repo rule wins (`AGENTS.md` prime directives).

- [ ] **No mandatory-read document teaches a stale decision.** Ran
      `pre-commit run kb-freshness-scan --all-files` — exit 0 — and **read the `verified:` stamp on every knowledge entry this task depends on.**
      - _Why this gate exists (**CONSTITUTION §6.3**):_ on the project this framework came from, an
        amendment sweep was missed **six times** — each time the decision body, the canonical source and
        the live system were updated correctly, and the **teaching document** was left stale. Teaching
        docs are what you read *instead of* the source, so a fossil there is worse than one in code.
      - _How to clear a failure:_ re-read the decision **and** the canonical source, correct the entry,
        then bump `verified:`. **Bumping the date alone re-creates the fossil.**
      - _Honest limit:_ it flags staleness **risk**, not wrongness — it cannot read prose. A green scan
        means nothing has changed *since someone last looked*, not that the entry is right.

## Part B — Required reads (governance + state)

- [ ] Read `AGENTS.md` (canonical brain + cold-start). Claude loads it via `CLAUDE.md`'s `@AGENTS.md` import; Codex reads it natively.
- [ ] Read `AGENT_INTEROP.md` (interoperability contract).
- [ ] Read `docs/orchestration/knowledge/INDEX.md` (index; then task-relevant entries).
- [ ] Read `CONSTITUTION.md`.
- [ ] Read `docs/standards/session_handoff_standard_v2.0.md`.
- [ ] Read `sprint/sprint-status.md`, `sprint/decision-log.md` (index), `sprint/story-tracker.md` (index).
- [ ] Read this session's pair in `sprint/handoffs/`: `HANDOFF_S<N>.md` and `KICKOFF_S<N>.md`, where
      N is one more than the newest `## S<N>` entry in `sprint/sprint-status.md`. Never read
      `archive/` as a mandatory read; anything there was not carried forward on purpose.
- [ ] Read the standards in the current story's "Required Standards" column.

## Part C — Comprehension questions (answer from the docs)

Answer each in one line, citing the file you read it in:

1. **Single source of truth:** Where does authoritative project state live, and what is a tool's private
   memory considered? *(Expected: the git repo is the only source of truth; tool memory is a cache. —
   `AGENT_INTEROP.md §1` / `AGENTS.md`)*
2. **Flush discipline:** When you learn something durable this session, where must it be written before
   session close? *(Expected: `docs/orchestration/knowledge/<slug>.md` + an `INDEX.md` pointer — never
   only tool memory.)*
3. **Entry points:** What is the relationship between `AGENTS.md` and `CLAUDE.md`? *(Expected: `AGENTS.md`
   is the one canonical brain — Codex reads it natively; `CLAUDE.md` is a thin `@AGENTS.md` import plus
   Claude-only accelerators. There is no second brain to diverge.)*
4. **Handoff lifetime:** How long does a handoff live, and where does anything needed beyond that
   go? *(Expected: one session, then archived by the closeout gate; durable content goes to the
   tracker, decision log, or knowledge base and the handoff links to it. —
   `session_handoff_standard_v2.0.md §3`)*
<!-- profile:gcc -->
5. **Banned features:** Name three banned features and the one-word reason they are banned.
   *(Expected: e.g. Direct Lake / Dataflows Gen2 / OLS — GCC-incompatible. — `CONSTITUTION.md §3`)*
<!-- /profile:gcc -->
<!-- profile:commercial -->
5. **Banned features:** What does the constitution ban on this profile, and where are platform
   choices recorded? *(Expected: only sandbox execution identities; platform features are ordinary
   engineering decisions logged in `sprint/decision-log.md`. — `CONSTITUTION.md §3`)*
<!-- /profile:commercial -->
6. **Current state:** What is the current sprint focus, and what is the next actionable story?
   *(Expected: answered from `sprint/sprint-status.md` + `sprint/story-tracker.md` — NOT from memory.)*
7. **Index-first logs:** How must the large governance logs (decision-log, story-tracker, sprint-status)
   be read? *(Expected: index + task-relevant entries only, never whole; kept in markdown, not JSON.)*
8. **Execution identity:** Which identities/tokens are forbidden, when is escalation required before
   every command, and when must the agent stop? *(Expected: no sandbox account/identity/restricted
   token/private desktop; sandbox-bounded sessions escalate before every command; stop if escalation
   is unavailable or still uses a sandbox/offline identity. — `AGENTS.md` /
   `knowledge/reference_agent_execution_identity.md`)*

## Part D — Ready-to-build gate

- [ ] All Part A boxes checked, all Part B files actually read, all Part C answers correct **from the docs**.
- [ ] If ANY answer had to come from memory or could not be sourced to a file → **STOP and read**, do not build.

---

*Passing this checklist is the precondition for any build work. It is the same gate whichever tool is
driving — that is what makes the repo tool-agnostic.*
