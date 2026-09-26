# Sprint Management Standard v1.0

**Version:** 1.0
**Created:** {{DATE}}
**Status:** Active
**Purpose:** Govern how agents BUILD the sprint documents from a planning session and MAINTAIN them
correctly across sessions and tools — so every agent produces the same structure and the docs never drift.

---

## 1. Purpose & Scope

This standard is the authoritative guide for the `sprint/` state documents. It covers:

- **Setup:** turning an approved PRD + Architecture into epics and stories (the Planning Session Protocol, §5).
- **Maintenance:** the status lifecycle, update cadence, and sprint boundaries (§7–§10).

It applies to any agent (Claude Code, Codex, future tools) that creates or updates
`sprint/story-tracker.md`, `sprint/sprint-status.md`, or `sprint/decision-log.md`. It **extends**
`CONSTITUTION.md §2` (session protocols) and `session_handoff_standard_v2.0.md` (handoffs); where those
speak to sprint docs, this standard is the detailed procedure.

---

## 2. The Three-Document System

The three sprint docs are one system. Each has a single, non-overlapping role — never duplicate content
across them.

| Document | Role | Answers | Source of truth for |
|----------|------|---------|---------------------|
| `sprint/story-tracker.md` | **Backlog** — every epic/story, its status, deps, standards | "What work exists and what's its state?" | Story scope, dependencies, Required Standards, Done/Not |
| `sprint/sprint-status.md` | **Snapshot** — current focus + newest session updates | "What is happening right now?" | Current phase/focus, in-progress work, blockers |
| `sprint/decision-log.md` | **Rationale** — durable architectural/design decisions | "Why did we choose this?" | Decisions, supersession chains, the *why* |

**Relationship rule:** the tracker is authoritative for *status*; sprint-status is a rolling *view* of
it plus session narrative; decision-log holds *why*, never task status. If they disagree, the tracker
wins for status and the decision-log wins for rationale. (Consistent with
`sprint/recovery/AUTHORITY_MATRIX.md`.)

**The template's own decisions are not sprint state.** They live in
`docs/governance/framework_decisions.md`, carried by the updater and read by the gates as one set
with the project's log; a project never edits that file, and a session in the template itself logs
there rather than in `sprint/decision-log.md` ([[reference_framework_decisions]]).

---

## 3. Hierarchy & Naming

```
Dependency Layer   e.g. INFRA --> DATA_INGEST --> TRANSFORM --> SERVE --> VALIDATE
   └─ Epic         a coherent capability within a layer     ID prefix: {PREFIX}-{Epic#}
        └─ Story   one independently testable unit of value  ID: {PREFIX}-{Epic#}.{Story#}
```

- **Story ID:** `{PREFIX}-{Epic#}.{Story#}` — e.g. `INFRA-1.1` = Infrastructure epic 1, story 1.
- **Prefix** names the dependency layer (INFRA, DATA, TRANSFORM, SERVE, VALIDATE, …). Define your
  layers from the Architecture before writing stories.
- **Statuses:** `Not Started | In Progress | Blocked | Done` (see §7 for transitions).

---

## 4. Story Authoring Rules (decomposition)

A well-formed story is **INVEST-aligned** and, per `CONSTITUTION.md §9`, **human-executable**:

| Rule | Meaning |
|------|---------|
| **One testable unit** | A story delivers one thing that can be validated against a standard's checklist. If it needs two unrelated validations, split it. |
| **Session-sized** | A story should be completable within one session's productive budget. If it can't, split it — never plan a story that *must* span sessions. |
| **Independent as possible** | Minimize cross-story coupling; express real ordering via **Dependencies**, not hidden assumptions. |
| **Traceable** | Every story links to its origin in the PRD via **PRD Ref**. |
| **Standards-bound** | Every story lists its **Required Standards** — the explicit, authoritative set an agent must read before building it (`CONSTITUTION.md §2.1` Standard Selection Rule). Do not leave this blank; use `—` only when genuinely none apply. |

**Required columns for every story row:** `Story ID | Title | Status | Dependencies | Required Standards | PRD Ref`.

---

## 5. Planning Session Protocol

Run this named procedure whenever creating (or materially re-planning) a sprint from a planning session.
It is the sprint-creation counterpart to the cold-start gate.

### 5.1 Preconditions (do not start until all true)
- [ ] PRD is finalized and approved, living in `docs/prd/`.
- [ ] Architecture is finalized and approved, living in `docs/architecture/`.
- [ ] You have **read both in full** this session (references do not auto-load).
- [ ] `CONSTITUTION.md` and this standard are read.

### 5.2 Steps
1. **Derive dependency layers** from the Architecture (e.g. `INFRA --> DATA_INGEST --> TRANSFORM --> SERVE --> VALIDATE`). Record them in the tracker's **Dependency Order** block.
2. **Group PRD requirements into Epics** — one epic = one coherent capability within a layer. Assign each an `{PREFIX}-{Epic#}` id.
3. **Decompose each epic into Stories** per §4 (one testable, session-sized unit each). Assign `{PREFIX}-{Epic#}.{Story#}` ids.
4. **For each story, set:** Dependencies (other story IDs that must be `Done` first), Required Standards (from `docs/standards/`), and PRD Ref.
5. **Populate `sprint/story-tracker.md`:** fill Summary Statistics, Dependency Order, and one table per epic. **Remove the `[EXAMPLE]` epic.**
6. **Initialize `sprint/sprint-status.md`:** set Current Phase, Current Focus, session number; write the first session update. Replace all `{{PLACEHOLDER}}` values.
7. **Seed `sprint/decision-log.md`:** log the planning decisions (layering, scope boundaries, framework/tech choices) with rationale and IDs. **Remove the `[EXAMPLE]` entry** once a real one exists.
8. **Confirm with the user** before any build work begins (`CONSTITUTION.md §2.1` step 7).

### 5.3 Output checklist (planning is complete when all true)
- [ ] Every PRD requirement maps to at least one story; no story lacks a PRD Ref.
- [ ] Every story has a status, dependencies (or `—`), and Required Standards (or a justified `—`).
- [ ] Dependency Order recorded; no story depends on a later-layer story.
- [ ] Summary Statistics counts are accurate.
- [ ] `sprint-status.md` initialized (no `{{PLACEHOLDER}}` left); first session update written.
- [ ] Planning decisions logged in `decision-log.md`; `[EXAMPLE]` entries removed.
- [ ] User has confirmed the plan.

---

## 6. Initial Population Notes

- The shipped `sprint/*` files contain `[EXAMPLE]` rows and `{{PLACEHOLDER}}` tokens purely as shape
  guides. The Planning Session Protocol replaces them — do not leave examples/placeholders in a live sprint.
- Keep all three files **markdown** (never JSON) and free of accreting changelog paragraphs, per the
  index-first governance rule (`AGENT_INTEROP.md §4`).

---

## 7. Status Lifecycle (state machine)

```
Not Started ──▶ In Progress ──▶ Done
                   │  ▲
                   ▼  │
                 Blocked
```

| Transition | When | Required action |
|------------|------|-----------------|
| Not Started → In Progress | All dependencies are `Done`; agent begins the story | Re-read the story's Required Standards first |
| In Progress → Blocked | A dependency, decision, or external input is missing | Log the blocker in `sprint-status.md`; if architectural, add a question to `decision-log.md` |
| Blocked → In Progress | Blocker resolved | Note resolution in `sprint-status.md` |
| In Progress → Done | Definition of Done (§9) fully met | Update tracker status + Summary Statistics; checkpoint commit |

**Rules:** never start a story whose dependencies are not `Done`. Prefer finishing an in-progress story
before starting another (low work-in-progress). A story returns to `Not Started` only if descoped —
record that as a decision.

**Gated:** the state gate (`scripts/session_closeout.py --check`, on every commit) fails a story
`In Progress` or `Done` whose listed dependency is not `Done`, or is no story in the tracker
(`dependency-order`). `Not Started` and `Blocked` stories are waiting and are not judged. The
`[EXAMPLE]` epic is skipped. Decision 2026-09-24-001; [[reference_session_closeout]].

---

## 8. Maintenance Cadence

Aligns with the Checkpoint Protocol (`CONSTITUTION.md §2.4`) and the handoff triggers.

| When | Update |
|------|--------|
| **After each story or work unit** | `story-tracker.md` (status + stats) → `decision-log.md` (if a decision was made) → `sprint-status.md` (focus/blockers) → `git commit -m "checkpoint: …"` |
| **User signals context is high** | Finish the current work unit only, then run the closeout (`session_handoff_standard_v2.0.md` §7) |
| **Session end** | Reconcile all three docs; flush durable learnings to `docs/orchestration/knowledge/`; run the closeout gate; commit |

State must never be more than one work unit behind reality.

---

## 9. Definition of Done

A story is `Done` only when **all** `session_handoff_standard_v2.0.md §9` criteria are met — do not
redefine them here. In short: artifacts exist in the right place, the gate suite exits 0, they
comply with their Required Standards, tracker/decision-log updated, no open questions.

---

## 10. Sprint Boundaries

- **Open a sprint:** define its scope as a set of stories from the tracker; set `sprint-status.md`
  Current Phase/Focus.
- **Close a sprint:** run the closeout with the sprint transition content (`session_handoff_standard_v2.0.md §10`);
  **roll over** incomplete stories to the next sprint (they keep their IDs and status); archive session
  updates older than the last 10 out of `sprint-status.md`.
- **Never** delete history — supersede or archive. Keep the tracker as the durable backlog across sprints.

---

## 11. Anti-Drift Rules

1. One fact, one home — status in the tracker, rationale in the decision-log, "now" in sprint-status.
2. No `[EXAMPLE]`/`{{PLACEHOLDER}}` content in a live sprint. **Gated:** in a project (a
   `.project-profile` exists) whose tracker holds a non-example epic, the state gate fails an
   `[EXAMPLE]` table row or heading, or an unfilled `{{TOKEN}}`, in the tracker, sprint-status or the
   decision log (`live-placeholder`). Text quoted in inline or fenced code is the convention
   explaining itself and passes. A fresh project keeps the shipped example epic until its first real
   one; the template has no profile and is exempt. Decision 2026-09-24-001; [[reference_session_closeout]].
3. Every story is standards-bound and PRD-traceable.
4. Markdown only; index-first; no accreting prose.
5. Any structural change to how sprints are run is logged as a decision and, if durable, flushed to the
   knowledge base.

---

## 12. Related Documents

- `CONSTITUTION.md` — session protocols, checkpoint protocol, standard-selection rule
- `docs/standards/session_handoff_standard_v2.0.md` — handoffs, Story Completion Criteria (Definition of Done)
- `AGENTS.md` — canonical brain / cold-start sequence
- `sprint/recovery/AUTHORITY_MATRIX.md` — source-of-truth mappings
- `AGENT_INTEROP.md` — index-first governance rule

---

## 13. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-24 | — | §7 and §11: the dependency rule and the live-placeholder rule are gated by the state gate (decision 2026-09-24-001, TMPL-5.5) |
| 1.0 | {{DATE}} | — | Initial version |
