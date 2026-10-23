---
authority: sprint documents — how the story tracker, sprint-status and the decision log are built and kept
implements: [2026-09-23-003, 2026-09-24-001, 2026-10-23-001]
verified: 2026-10-23
---

# Sprint Management Standard v1.0

**Created:** {{DATE}}
**Status:** Active
**Purpose:** Govern how agents BUILD the sprint documents from a planning session and MAINTAIN them
correctly across sessions and tools — so every agent produces the same structure and the docs never drift.

---

## 1. Purpose & Scope

This standard is the authoritative guide for the `sprint/` state documents. It covers:

- **Setup:** turning an approved PRD + Architecture into epics and stories (the planning session, §5).
- **Maintenance:** the status lifecycle, update cadence, and sprint boundaries (§7–§10).

It applies to any agent (Claude Code, Codex, future tools) that creates or updates
`sprint/story-tracker.md`, `sprint/sprint-status.md`, or `sprint/decision-log.md`. It **extends**
the session protocols in `AGENTS.md` and `session_handoff_standard_v2.0.md` (handoffs); where those
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
wins for status and the decision-log wins for rationale.

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
| **Standards-bound** | Every story lists its **Required Standards** — the explicit, authoritative set an agent must read before building it (the `AGENTS.md` cold start). Do not leave this blank; use `—` only when genuinely none apply. |

**Required columns for every story row:** `Story ID | Title | Status | Dependencies | Required Standards | PRD Ref`.

---

## 5. Planning Session

A sprint is created, or materially re-planned, from an approved PRD and Architecture by the
planning-session skill, `.claude/skills/planning-session/SKILL.md`, the procedure's one home
(decision 2026-10-23-001). It builds to §2–§4 and §11 of this standard, and it begins no build work
until the user has confirmed the plan (`CONSTITUTION.md` §1).

---

## 6. Initial Population Notes

- The shipped `sprint/*` files contain `[EXAMPLE]` rows and `{{PLACEHOLDER}}` tokens purely as shape
  guides. The planning session replaces them — do not leave examples/placeholders in a live sprint.
- Keep all three files **markdown** (never JSON) and free of accreting changelog paragraphs, per the
  index-first rule (`AGENTS.md` Conventions).

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

Aligns with checkpoint discipline and the handoff triggers (`AGENTS.md` How I work).

| When | Update |
|------|--------|
| **After each story or work unit** | `story-tracker.md` (status + stats) → `decision-log.md` (if a decision was made) → `sprint-status.md` (focus/blockers) → `git commit -m "checkpoint: …"` |
| **User signals context is high** | Finish the current work unit only, then run the closeout skill (`.claude/skills/closeout/SKILL.md`) |
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

- `AGENTS.md` — canonical brain: cold start, standard-selection rule, checkpoint discipline, index-first rule
- `CONSTITUTION.md` — the compliance law
- `docs/standards/session_handoff_standard_v2.0.md` — handoffs, Story Completion Criteria (Definition of Done)
- `docs/governance/doc_control_standard.md` — how an authoritative document declares its scope and records each change

---

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.0 | 2026-10-23 | 2026-10-23-011, 2026-10-22-002, 2026-10-23-001, 2026-10-23-010 | Marked as the authority for the sprint documents (TMPL-2.3); reflects the planning session as a skill. §2 and §12 point to the frontmatter registry instead of the retired authority matrix. The changelog table it replaces is in git | 515f1a5 |
