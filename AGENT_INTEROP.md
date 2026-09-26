# Agent Interoperability Standard

**Portable repo standard — reusable verbatim across repositories.**

This repository is **tool-agnostic**. Any AI coding agent (Claude Code, Codex, or a future tool) can
work it **interchangeably — in either direction, at any time — with zero drift and zero knowledge loss.**
This document is the durable policy that guarantees that. It is not tied to any one tool or to any
one-time migration event.

---

## 1. The Single-Source-of-Truth Law (authoritative)

> **No AI tool may hold authoritative project state in its own private store.**
> A tool's private memory (e.g. Claude's `~/.claude/.../memory/`, Codex's `~/.codex/memories_*.sqlite`)
> is a **cache, never a source.** The **git repository is the only source of truth.**
> Every session, regardless of tool, **flushes its durable learnings to repo markdown at close.**

This is the one rule everything else follows from. Every other section is a consequence of it.

## 1A. The Execution-Identity Law (authoritative)

> **No agent may create or use a sandbox account, sandbox identity, restricted sandbox token,
> private sandbox desktop, or equivalent isolated OS principal for this repository.**

Every local command executes under the operator's already-authenticated OS identity. When a session
exposes a `read-only` / `workspace-write` sandbox boundary, request operator escalation before every
local command; do not try the sandbox first. Those labels identify a boundary, not a forbidden
identity. An already-unsandboxed operator session retains `untrusted`, user-reviewed approvals.

`.codex/config.toml`, `scripts/agent_execution_identity_guard.py`, and the first pre-commit hook provide
defense in depth. If escalation is unavailable or still uses a Sandbox/Codex-Offline identity, stop.
Durable rationale: [[reference_agent_execution_identity]].

---

## 2. Why interchangeability holds

- **Both tools read the same brain.** `AGENTS.md` (repo root) is the one canonical brain: Codex reads it
  natively; `CLAUDE.md` loads it via an `@AGENTS.md` import. Its cold-start sequence reads
  `docs/orchestration/knowledge/INDEX.md`. No tool relies on private memory to know the project.
- **Git is the sync substrate.** Pull before, commit after. Whatever one tool does, the next tool sees
  on `git pull`. No tool-specific knowledge silo.
- **Drift gates are tool-neutral.** Git hooks (pre-commit) and repo scripts fire identically under any
  agent — they are not part of any tool's harness.
- **The repo knowledge base is the only shared store.** No external memory/MCP knowledge layer is
  required or trusted as a source.

A returning tool picks up instantly and losslessly: it reads the identical brain (`AGENTS.md` — natively
as Codex, or via `CLAUDE.md`'s import as Claude) → `knowledge/INDEX.md`, and `git pull` delivers every
session another tool ran in between. Any frozen private memory it kept is simply not authoritative.

---

## 3. Required file scheme (the repo contract)

| File | Role |
|------|------|
| `AGENTS.md` | **Canonical agent brain** (guardrails, conventions, cold-start) — Codex reads it natively; project-specific content |
| `CLAUDE.md` | Claude Code bridge → `@AGENTS.md` import + Claude-only accelerators |
| `AGENT_INTEROP.md` | **This standard** — the durable interoperability policy |
| `.codex/config.toml` | Codex project approval defaults; never forces a sandbox mode |
| `scripts/agent_execution_identity_guard.py` | Portable execution-identity/approval drift gate |
| `.pre-commit-config.yaml` | Tool-neutral mechanical gates; identity guard runs first |
| `docs/orchestration/knowledge/` + `INDEX.md` | The knowledge base — single source of truth for accumulated knowledge/feedback |
| `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md` | The cold-start drift gate (§5) |

The entry points and this standard travel near-verbatim between repos. `AGENTS.md`, the
knowledge base, and the checklist share the same *pattern* everywhere; their *content* is per-project.

---

## 4. The sync model (the flush discipline)

- **Session start:** `git pull`; read `AGENTS.md` + `knowledge/INDEX.md` (and the cold-start
  sequence's listed state files).
- **During the session:** durable learnings are written to `docs/orchestration/knowledge/<slug>.md`
  (plus an `INDEX.md` pointer) — **never** only to the tool's private memory feature.
- **Session close:** commit; generate/update the handoff. State lives in the repo, not the tool.
- **Index-first governance logs:** large append-only logs (decision/sprint/validation) are read as *index
  + task-relevant entries only*, never whole — keep them markdown (not JSON) and free of accreting
  changelog paragraphs, so ingestion stays cheap as they grow.

Wikilink convention: `[[<slug>]]` resolves to `docs/orchestration/knowledge/<slug>.md`.

---

## 5. Cold-start gate

Every cold start (new session, or a tool switch) runs `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md`
**before** any build work — proving the agent actually loaded governance and current state rather than
guessing from stale memory. It is tool-neutral: the same gate validates Codex now and Claude later.

---

## 6. Adopting this standard in a new repo

To make any repo tool-agnostic from day one:

1. Drop in `AGENTS.md` (the brain), `CLAUDE.md` (the `@AGENTS.md` bridge), and this `AGENT_INTEROP.md`.
2. Fill in `AGENTS.md` for that repo (guardrails, conventions, cold-start), keeping it lean.
3. Create `docs/orchestration/knowledge/INDEX.md` (seed it; grow it via the flush discipline).
4. Add `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md` (adapt the comprehension questions to that repo).
5. Preserve `.codex/config.toml` and `scripts/agent_execution_identity_guard.py`; install the
   repo-level pre-commit hook in each clone.

A **greenfield repo has no migration** — it is born interoperable by adopting this scheme. Only a repo
with **prior single-tool state** (e.g. an existing tool's out-of-repo memory) performs a one-time
migration; that event is recorded separately (in this repo, `docs/orchestration/TRANSITION_TO_CODEX.md`)
and is **not** part of this durable standard.

---

*Portable. Tool-neutral. The interoperability contract for this repo and a template for all others.*
