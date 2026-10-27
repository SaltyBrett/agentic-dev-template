---
authority: sprint documents, how the story tracker, sprint-status, the decision log and the issue log are built and kept
implements: []
verified: 2026-10-25
---

# Sprint Management Standard v1.0

**Created:** {{DATE}}
**Status:** Active
**Purpose:** Govern how agents BUILD the sprint documents from a planning session and MAINTAIN them
correctly across sessions and tools, so every agent produces the same structure and the docs never drift.

---

## 1. Purpose & Scope

This standard is the authoritative guide for the `sprint/` state documents. It covers:

- **Setup:** turning an approved PRD + Architecture into epics and stories (the planning session, section 5).
- **Maintenance:** the status lifecycle, update cadence, and sprint boundaries
  (section 7 to section 10).

It applies to any agent (Claude Code, Codex, future tools) that creates or updates
`sprint/story-tracker.md`, `sprint/sprint-status.md`, or `sprint/decision-log.md`. It **extends**
the session protocols in `AGENTS.md` and `session_handoff_standard_v2.0.md` (handoffs); where those
speak to sprint docs, this standard is the detailed procedure.

---

## 2. The Sprint Documents

The sprint docs are one system. Each has a single, non-overlapping role. Never duplicate content
across them.

| Document | Role | Answers | Source of truth for |
|----------|------|---------|---------------------|
| `sprint/story-tracker.md` | **Backlog**: every epic/story, its status, deps, standards | "What work exists and what's its state?" | Story scope, dependencies, Required Standards, Done/Not |
| `sprint/sprint-status.md` | **Snapshot**: current focus + newest session updates | "What is happening right now?" | Current phase/focus, in-progress work, blockers |
| `sprint/decision-log.md` | **Rationale**: durable architectural/design decisions | "Why did we choose this?" | Decisions, supersession chains, the *why* |
| `sprint/issue-log.md` | **Intake**: every issue reported, from filing to resolution (section 12) | "What is wrong or wanted, and where does it stand?" | Issues, who reported them, the stories that resolve them |

**Relationship rule:** the tracker is authoritative for *status*; sprint-status is a rolling *view* of
it plus session narrative; decision-log holds *why*, never task status. If they disagree, the tracker
wins for status and the decision-log wins for rationale.


---

## 3. Hierarchy & Naming

```
Dependency Layer   e.g. INFRA --> DATA_INGEST --> TRANSFORM --> SERVE --> VALIDATE
   +- Epic         a coherent capability within a layer     ID prefix: {PREFIX}-{Epic#}
        +- Story   one independently testable unit of value  ID: {PREFIX}-{Epic#}.{Story#}
```

- **Story ID:** `{PREFIX}-{Epic#}.{Story#}`, e.g. `INFRA-1.1` = Infrastructure epic 1, story 1.
- **Epic heading:** `## Epic: {PREFIX}-{Epic#} - <title>` in the tracker. The gates read an epic by
  its `Epic:` prefix alone, and the label before the title is not counted toward a heading's 8
  words, as section 6 of `docs/standards/writing_standard_v1.0.md` says.
- **Prefix** names the dependency layer (INFRA, DATA, TRANSFORM, SERVE, VALIDATE, ...). Define your
  layers from the Architecture before writing stories.
- **Statuses:** `Not Started | In Progress | Blocked | Done` (see section 7 for transitions).

---

## 4. Story Authoring Rules (decomposition)

A well-formed story is **INVEST-aligned** and, per `CONSTITUTION.md section 9`, **human-executable**:

| Rule | Meaning |
|------|---------|
| **One testable unit** | A story delivers one thing that can be validated against a standard's checklist. If it needs two unrelated validations, split it. |
| **Session-sized** | A story should be completable within one session's productive budget. If it cannot, split it. Never plan a story that *must* span sessions. |
| **Independent as possible** | Minimize cross-story coupling; express real ordering via **Dependencies**, not hidden assumptions. |
| **Traceable** | Every story links to its origin in the PRD via **PRD Ref**. |
| **Standards-bound** | Every story lists its **Required Standards**: the explicit, authoritative set an agent must read before building it (the `AGENTS.md` cold start). Do not leave this blank; use `none` only when genuinely none apply. |

**Required columns for every story row:** `Story ID | Title | Status | Dependencies | Required Standards | PRD Ref`.

---

## 5. Planning Session

A sprint is created, or materially re-planned, from an approved PRD and Architecture by the
planning-session skill, `.claude/skills/planning-session/SKILL.md`, the procedure's one home. It builds to section 2 to section 4 and section 11 of this standard,
and it begins no build work until the user has confirmed the plan (`CONSTITUTION.md` section 1).

---

## 6. Initial Population Notes

- The shipped `sprint/*` files contain `[EXAMPLE]` rows and `{{PLACEHOLDER}}` tokens purely as shape
  guides. The planning session replaces them. Do not leave examples/placeholders in a live sprint.
- Keep all three files **markdown** (never JSON) and free of accreting changelog paragraphs, per the
  index-first rule (`AGENTS.md` Conventions).

---

## 7. Status Lifecycle (state machine)

```
Not Started --> In Progress --> Done
                   |  ^
                   v  |
                 Blocked
```

| Transition | When | Required action |
|------------|------|-----------------|
| Not Started -> In Progress | All dependencies are `Done`; agent begins the story | Re-read the story's Required Standards first; `python3 scripts/story_branch.py start <ID>` sets it, on the integration branch, and makes its branch and worktree |
| In Progress -> Blocked | A dependency, decision, or external input is missing | Log the blocker in `sprint-status.md`; if architectural, add a question to `decision-log.md` |
| Blocked -> In Progress | Blocker resolved | Note resolution in `sprint-status.md` |
| In Progress -> Done | Definition of Done (section 9) fully met | `python3 scripts/story_branch.py finish <ID>` merges its pull request once CI is green and sets it, with the Summary Statistics, on the integration branch |

**Rules:** never start a story whose dependencies are not `Done`. Prefer finishing an in-progress story
before starting another (low work-in-progress). A story returns to `Not Started` only if descoped.
Record that as a decision.

**Gated:** the state gate (`scripts/session_closeout.py --check`, on every commit) fails a story
`In Progress` or `Done` whose listed dependency is not `Done`, or is no story in the tracker
(`dependency-order`). `Not Started` and `Blocked` stories are waiting and are not judged. The
`[EXAMPLE]` epic is skipped.

---

## 8. Maintenance Cadence

Aligns with checkpoint discipline and the handoff triggers (`AGENTS.md` How I work).

| When | Update |
|------|--------|
| **After each story or work unit** | `story-tracker.md` (status + stats) -> `decision-log.md` (if a decision was made) -> `sprint-status.md` (focus/blockers) -> `git commit -m "checkpoint: ..."` |
| **User signals context is high** | Finish the current work unit only, then run the closeout skill (`.claude/skills/closeout/SKILL.md`) |
| **Session end** | Reconcile all three docs; flush durable learnings to `docs/orchestration/knowledge/`; run the closeout gate; commit |

State must never be more than one work unit behind reality.

---

## 9. Definition of Done

A story is `Done` only when **all** `session_handoff_standard_v2.0.md section 9` criteria are met. Do not
redefine them here. In short: artifacts exist in the right place, the gate suite exits 0, they
comply with their Required Standards, tracker/decision-log updated, no open questions.

---

## 10. Sprint Boundaries

- **Open a sprint:** define its scope as a set of stories from the tracker; set `sprint-status.md`
  Current Phase/Focus.
- **Close a sprint:** run the closeout with the sprint transition content (`session_handoff_standard_v2.0.md section 10`);
  **roll over** incomplete stories to the next sprint (they keep their IDs and status); archive session
  updates older than the last 10 out of `sprint-status.md`.
- **Never** delete history; supersede or archive. Keep the tracker as the durable backlog across sprints.

---

## 11. Anti-Drift Rules

1. One fact, one home: status in the tracker, rationale in the decision-log, "now" in sprint-status.
2. No `{{PLACEHOLDER}}` content in a live sprint. **Gated:** in a project (a `.template-version`
   exists) whose tracker holds a non-example epic, the state gate fails an unfilled `{{TOKEN}}` in
   the tracker, sprint-status or the decision log (`live-placeholder`). Text quoted in inline or
   fenced code is the convention explaining itself and passes; the template has no
   `.template-version` and is exempt. Each log keeps its `[EXAMPLE]` entry, numbered zero (the
   tracker's epic `ACME-0`, the decision `ACME-2025-01-15-000`, the issue `ACME-ISS-0`), as the form
   its entries follow: nothing removes it, and a project's first entry is 1.
3. Every story is standards-bound and PRD-traceable.
4. Markdown only; index-first; no accreting prose.
5. Any structural change to how sprints are run is logged as a decision and, if durable, flushed to the
   knowledge base.

---

## 12. Issues

An issue is something reported as wrong, wanted or at risk, filed before anyone knows what work it
needs. `sprint/issue-log.md` holds every one: an index table, then one entry per issue, in the
form of the log's `[EXAMPLE]` entry, which is the template.

**Filing.** A person or an agent files through one writer, which allocates the next ID and writes
the index row and the entry from the template: `python3 scripts/issue_log.py --file`, which asks
for each missing field when run in a terminal, or the `/issue` skill. `--update <ID>` changes an
issue's fields the same way. An entry written by hand is held to the same rules. An issue is never
deleted: Won't fix closes one.

**IDs.** `<PREFIX>-ISS-<n>`, numbered from 1 with no gap. The prefix is the project's story prefix,
which the initializer records in the log's `**Prefix:**` line; every issue is filed under it.

**The entry.** Headed `## Issue <ID>`, then these fields in this order, then the sections below.

| Field | Values |
|-------|--------|
| Title | one line, as the index shows it |
| Reported | the date filed, `YYYY-MM-DD` |
| Reporter | who filed it, then `(human)` or `(agent)` |
| Kind | `bug`, `request`, `risk` |
| Severity | `critical`, `high`, `medium`, `low` |
| Status | `Open`, `Triaged`, `In Progress`, `Resolved`, `Closed`, `Won't fix` |
| Stories | the story IDs that resolve it, comma-separated, or `none` |
| Decisions | the decision IDs that answer it, or `none` |
| Resolved by | the resolving commit, or `none` |

The sections, in order: `What happened`, `Expected`, `Steps to reproduce` (a bug's alone),
`Impact`, `Resolution`. All but `Resolution` hold text from the start; `Resolution` holds `none`
until the issue is resolved or declined.

**Statuses.** Each holds only while its condition does, judged against the tracker.

| Status | Holds when |
|--------|------------|
| Open | no story and no decision is named |
| Triaged | a story or a decision is named, and no named story is `In Progress` or `Done` |
| In Progress | a named story is `In Progress` or `Done`, and not every one is `Done` |
| Resolved | every named story is `Done`, the commit is named and the resolution written |
| Closed | as Resolved, and the Chair has confirmed the fix holds |
| Won't fix | the resolution gives the reason, and no named story is `In Progress` |

**Links.** An issue names the stories that resolve it; the tracker's columns do not change, and the
report derives which issue each story serves. A row of a project's `docs/code_review_log.md` whose
response defers a fix names the issue that tracks it (`acknowledged, ACME-ISS-7`).

**Moved by the workflow.** A story's issues change status in the commits that change the story.
`python3 scripts/story_branch.py start <ID>` sets each Triaged issue naming the story In Progress
in the commit that starts it. Before it merges anything, `finish <ID>` refuses a story whose Done
would leave an issue In Progress with every named story Done; given `--resolution "<what
changed>"`, its Done commit sets each such issue Resolved, the squash commit its resolving commit.
An issue with a story still open stays In Progress.

**Gated:** `issue-log` (on every commit) fails an entry that departs from the template, an index
row that disagrees with its entry, an ID out of sequence, a status its stories do not bear out, a
named story or decision that does not exist, and an issue the code review log names that the log
does not hold. A project with no issue log has no issues and passes. `python3 scripts/issue_log.py
--report` counts issues by status, kind, severity and reporter, lists the open ones by age, and
shows each issue's stories with their status.

---

## 13. Related Documents

- `AGENTS.md` (canonical brain): cold start, standard-selection rule, checkpoint discipline, index-first rule
- `CONSTITUTION.md`: the compliance law
- `docs/standards/session_handoff_standard_v2.0.md`: handoffs, Story Completion Criteria (Definition of Done)
- `docs/governance/doc_control_standard.md`: how an authoritative document declares its scope and records each change

---

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.9 | 2026-10-25 | template | the template's version 1.9 | template |
