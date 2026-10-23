# Sprint Status

**Current Phase:** Template maintenance
**Current Focus:** v2.0.0 — the Claude-native substrate and authoritative documents; then v2.1.0, the team and the coding standard
**Last Updated:** 2026-10-22
**Updated By:** S3

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (setup, update cadence, sprint boundaries).
>
> **READ SELECTIVELY (index-first).** Read the header (Current Phase/Focus) and the newest session
> update first; older updates are context, not required reading. Keep the last 10 updates visible and
> archive older ones — `scripts/session_closeout.py --check` enforces the cap. Markdown only (never JSON).
> Every entry is headed `## S<N> — YYYY-MM-DD — <title>`; the gate reads the session number from it.

---

## S3 — 2026-10-22 — Personas as agent files; path-scoped rules

**Status:** Cold start clean: the `SessionStart` hook ran the identity gate (PASS), the pull and
`session-verify` (PASS); both hook types installed; `gh` on the keyring; Claude Code 2.1.308. The
sub-agents page was read whole (curl) before any build, and it changed the plan: under
`claude --agent` an agent's body replaces Claude Code's built-in system prompt whole. A scratch
probe confirmed the rest (persona canary back, `AGENTS.md` loaded, `agent_type` in the hook input)
and measured the agent run's prompt about 2,500 tokens smaller than a control. Two choices went to
the operator, both answered with the recommendation: the session takes its persona from the start
hook, `--agent` optional; `dev-resources` keeps both registry trees until TMPL-2.4, because Comfy
and PocketGames sync `docs/personas/` with `v1.0.0` scripts (decision 2026-10-22-005, amending
2026-10-22-001). TMPL-1.3 and TMPL-1.5 done.

### Done

1. TMPL-1.3 — the five personas are agent files in `.claude/agents/` (frontmatter: name = slug,
   version, expertise, insists_on, changelog; body = the Invocation, text and versions unchanged);
   `docs/personas/` removed. `persona-lint` parses the frontmatter as YAML, lazily, so the session
   hook needs no PyYAML; the conversion found four list items that YAML read as mappings until
   quoted. The kickoff names the agent and the lint still accepts `KICKOFF_S3.md`'s copy.
   `session_start.py` reads `agent_type` and injects the agent's prompt unless the session runs as
   it. Sync, updater, initializer, sanitizer, manifest and docs follow the path. Self-tests 87, 28
   and 18 then; 22 broken variants, each caught. Live: the agent run and a plain run each held the
   persona (the hook said which way); an unbumped body edit exited 1 here and through the published
   hook in `dev-resources`. `dev-resources` 9002dfb pins the template twice (pre-commit accepts it;
   both trees judged) and its `gates` run 39884359420 was green; the template's 386d7b6 run
   39884095218 green before it. The sync back: every agent `up-to-date`, stamp `main 9002dfb`. A
   scratch clone of Comfy still resolved every persona from the frozen tree; its
   `reference_macos_toolchain` CONFLICT comes from S2's publish and is the sync's documented
   one-`--take`-per-project cost, not this move.
2. TMPL-1.5 — four rules in `.claude/rules/` (gate scripts and the suite, knowledge entries,
   decision logs, sprint documents). `CONSTITUTION.md` §6.3 is a pointer: its reasoning moved to
   [[reference_kb_freshness]], its instructions to two rules; the knowledge index shed its
   frontmatter block and its frontmatter-less template. The state gate refuses a rule with no
   parseable `paths:`, a dead glob, or a repeat of `AGENTS.md` (decision 2026-10-22-006). Canary:
   absent with no tool used and after reading `README.md`, present after reading the matching
   entry. The first repeat check compared whole sentences and a planted clause copy passed it; it
   now finds a sentence inside the other text either way, and the re-plant fails. 102 fixtures, 15
   variants caught. The banned-feature scan refused one rule's quoted hook `entry:` as a bare
   interpreter; reworded, not exempted.

### Blockers

- None.

---

## S2 — 2026-10-22 — One cold start in `AGENTS.md`; Claude Code hooks

**Status:** Cold start clean apart from `main` having no upstream (lost in the `v1.0.0` cut); set
to `origin/main`, which it already equalled. TMPL-1.1 done. Claude Code is 2.1.308, past the
2.1.277 condition, and the native read was observed before `CLAUDE.md` went: a scratch repository's
`AGENTS.md` canary came back from `claude -p`, and an empty `CLAUDE.md` beside it made the answer
`NONE` ([[reference_claude_code_agents_md]]). Cold start measured as every file it makes a
mandatory read, the session pair included and the story's Required Standards excluded both times:
89,493 bytes across 12 files before, 60,616 across 9 after; the governance files alone 67,723 →
38,846. The handoff standard is now read at closeout, reached from `AGENTS.md`, not at every cold
start. Two of the kickoff's greps cannot hold literally, and were judged by intent:
`AGENT_INTEROP` remains in decision bodies, the tracker row and the S2 pair, all records, and in
no live document; `session-verify --hook-stage manual` remains in the gate runbook's per-hook
`Alone:` line and one knowledge entry's observation, neither a copy of the procedure.

### Done

1. TMPL-1.1 — `AGENTS.md` alone holds the cold start; it gained the Standard Selection Rule, the
   index-first rule, the enforcement sentence from the interop contract, a plan-first line from
   `CLAUDE.md`, and a ban on any `CLAUDE.md` that would hide it. `CONSTITUTION.md` §2.1, §2.2, §2.4,
   the handoff standard §8 and §11, `README.md`, `TEMPLATE_GUIDE.md`, `docs/README.md`, the sprint
   standard and the index header point there. The checklist holds auth and the hook install only,
   so the scanner's exemption for it went, proved by a planted feature that now blocks.
   `AGENT_INTEROP.md` and `CLAUDE.md` deleted. Knowledge entries citing moved text re-verified:
   `reference_precommit_interpreter` (names the exempt set, not its members),
   `reference_macos_toolchain` §6 (true before and after 2.1.277; a resource entry, published at
   closeout).

2. TMPL-1.2 — the hooks reference read in full before any hook was written. `session_start.py`
   (`SessionStart`, matchers startup, clear and compact), `session_stop.py` (`Stop`) and
   `session_journal.py` (`PostToolUse` and `PostToolUseFailure` on Edit, Write, Bash), each with a
   self-test hook and a runbook section; the notes' fixed shape; `disableWorkflows`; `ask` rules for
   the one-way doors; the closeout gate clears journal and notes. Decision 2026-10-22-004: both
   files gitignored. Observed in scratch clones, not assumed: the first turn quoted the gate lines
   and the kickoff; a real `/compact` re-injected the notes and the kickoff; the `Stop` hook sent a
   turn back with `sprint-status.md` modified and allowed it once committed; the journal gained a
   line per Edit and per Bash with the failing exit code; the four one-way doors were refused under
   a matching allow rule. Nineteen broken variants, each failing a fixture. Beside nine pre-commit
   stash windows the ignored journal kept 2,400 of 2,400 lines; tracked, it lost 2,306 and
   pre-commit crashed leaving an unstaged edit only in its cache. `PreCompact` blocking a manual
   `/compact` works; not registered, since blocking the recovery compaction fails the request
   ([[reference_claude_code_hooks]]). `clear` was added to the kickoff's two matchers: it empties
   the context as a new session does. The `Stop` hook answers with `additionalContext`, not a
   block, after a block raised a "hook error" notice in the probe. Two defects the first live
   run found: `git pull --ff-only` refuses a dirty tree under `pull.rebase` (now `--no-rebase`);
   untracked directories hid their files from the stale-notes rule (now `--untracked-files=all`).
3. Found while building TMPL-1.2: the cold start's `session-verify` passed a dirty tree, because
   pre-commit's stash hid an unstaged edit (measured at the S1 closeout commit). Decision
   2026-09-22-003 amended; the command carries `--all-files` everywhere it is written.

### Blockers

- None.

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
