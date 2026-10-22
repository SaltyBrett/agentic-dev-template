# Sprint Status

**Current Phase:** Template maintenance
**Current Focus:** v2.0.0 — the Claude-native substrate and authoritative documents; then v2.1.0, the team and the coding standard
**Last Updated:** 2026-10-22
**Updated By:** S1

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (setup, update cadence, sprint boundaries).
>
> **READ SELECTIVELY (index-first).** Read the header (Current Phase/Focus) and the newest session
> update first; older updates are context, not required reading. Keep the last 10 updates visible and
> archive older ones — `scripts/session_closeout.py --check` enforces the cap. Markdown only (never JSON).
> Every entry is headed `## S<N> — YYYY-MM-DD — <title>`; the gate reads the session number from it.

---

## S1 — 2026-10-22 — Planning: v2.0.0 and v2.1.0 decided, four epics opened

**Status:** The first session on the public `v1.0.0`, a planning session with the operator and no
build work. Three decisions logged. 2026-10-22-001: the framework runs on Claude Code's native
machinery where that removes overhead and not a control: a `SessionStart` hook runs the cold
start and re-injects after compaction, a `Stop` hook enforces checkpoint discipline, a
`PostToolUse` journal and a working-notes file bank the uncommitted interval, personas become
subagents, procedures become forked skills, judgement rules become path-scoped, the constitution
and checklist shrink, the interop contract retires; git hooks and CI remain the enforcement.
Measured: the cold start today reads about 74 KB across ten files, the procedure exists in four
places; the installed Claude Code is 2.1.267 and native `AGENTS.md` needs 2.1.277, so `CLAUDE.md`
stays as the bridge until then. 2026-10-22-002: authoritative documents carry `authority:`
frontmatter and a version log, decisions carry `Affects:`, a gate accepts a version-log row or an
open tracker story and nothing else, the commit is stamped after the fact and verified, and a
technical-writer agent drains the queue at cold start, bounded by age, never at closeout.
2026-10-22-003: `v2.1.0` is the role-agent team whose handoffs are gated artifacts and the
three-layer coding standard, each opened by a design session, the standard proved against real
code before adoption. The compaction question answered on the record: committed state, the brain,
the kickoff, the journal and the notes survive it; reasoning never written down does not, and the
`Stop` hook narrows that to one turn. Since `v1.0.0`, by the operator outside any session here:
three projects born from the template (`Supplier_Research_Dev`, `Comfy`, `PocketGames`), each
private, initialized green, no template friction.

### Done

1. Decisions 2026-10-22-001, -002, -003; epics TMPL-1 (7 stories), TMPL-2 (4), TMPL-3 (2),
   TMPL-4 (2) opened, 15 stories, dependencies set so the substrate precedes the documents gate,
   and both precede the team and the standard.

### Blockers

- None.

---

<!-- Add new session updates ABOVE this line, newest first, headed `## S<N> — YYYY-MM-DD — title` -->
<!-- Each entry: Done (by story ID), Blockers. Next-session tasks live in the kickoff, not here. -->
<!-- Keep the last 10 entries visible; move older ones to sprint/archive/ (the gate enforces the cap) -->
