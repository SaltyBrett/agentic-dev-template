# Sprint Status

**Current Phase:** Template maintenance
**Current Focus:** v2.0.0 — the Claude-native substrate and authoritative documents; then v2.1.0, the team and the coding standard
**Last Updated:** 2026-10-24
**Updated By:** S11

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (setup, update cadence, sprint boundaries).
>
> **READ SELECTIVELY (index-first).** Read the header (Current Phase/Focus) and the newest session
> update first; older updates are context, not required reading. Keep the last 10 updates visible and
> archive older ones — `scripts/session_closeout.py --check` enforces the cap. Markdown only (never JSON).
> Every entry is headed `## S<N> — YYYY-MM-DD — <title>`; the gate reads the session number from it.

---

## S11 — 2026-10-24 — The launch proved live, and two silent gaps

**Status:** Cold start through `scripts/session_start.py` at session start: identity gate, pull,
`session-verify` and `doc-queue` each exit 0; the reads done by hand. Persona
`framework-maintainer`. TMPL-5.4 done, its third run with the Chair at the keyboard in
`SaltyBrett/launch-probe-s10` observing every remaining stage through the probe's first closeout.
Two gaps it found, each passing silently, opened as TMPL-2.9 and TMPL-5.7 by the Chair's choice of
fix, both before TMPL-2.4.

### Done

1. TMPL-5.4's third run, read from the probe's commits and transcripts: the PRD approved and stamped
   (`5794166`, `8c748b1`); `skip architecture` logged with the Chair's reason (`4169b9c`); planning's
   epic LP-1 with the `**Source:**` line `PRD 1.0, architecture skipped` (`0e19e71`),
   `doc-authority-scan` on it exit 0; the PRD revised to 1.1 and re-approved (`1ae29c9`, `62006ff`),
   `status` reading planning stale; the first closeout `c0a6db7` passing `session-closeout`, pushed,
   run 40063609570 green on `gates` and both `birth` jobs; the probe's `session-verify` after it
   exit 0, "This is S2". Recorded in [[reference_launch_live_run]]; TMPL-5.4 Done.
2. TMPL-2.9 opened: `doc-authority-scan` does not read an `**Affects:**` path outside a code span,
   and `docs/templates/README.md` step 5 does not say to use one, so the probe's PRD approval passed
   unchecked. The Chair chose a refusal in the gate and the README's wording.
3. TMPL-5.7 opened: the probe's first closeout, typed as `/closeout` and run as the fork, closed S1
   on an entry still headed `emergency checkpoint`, saying its closeout was not completed, its
   `### Next` stale. The Chair chose a refusal in the closeout gate. TMPL-2.4 waits on both.
4. S1's entry moved to `sprint/archive/sprint-status_2026.md`, the eleventh over the cap.

### Blockers

- None.

---

## S10 — 2026-10-23 — The README front page and the live launch

**Status:** Continued in the S9 conversation at the Chair's request; the cold start run through
`scripts/session_start.py` as `/clear` would run it: identity gate, pull, `session-verify` and
`doc-queue` each exit 0, the journal's `start S10` line written; the reads done by hand. Persona
`framework-maintainer`. The Chair scheduled TMPL-5.4 for this session after TMPL-5.5, on a real
private repository made by the walkthrough. TMPL-5.5 and TMPL-2.8 done; TMPL-5.4 in progress, two
live runs with the Chair in `SaltyBrett/launch-probe-s10` recorded, its second half carried to S11
by the Chair's choice.

### Done

1. TMPL-5.5 built (decision 2026-10-23-022): `README.md` as the operator's front page, a nine-step
   walkthrough and a catalog of commands, operator scripts, session hooks and gates;
   `TEMPLATE_GUIDE.md` cut to named sections on what the initializer leaves; `skill-scan` refusing
   a skill the README's `## Catalog` does not name. Eight fixtures, seven broken variants caught;
   on the real tree a README missing `/doc-drain` refused, restored passing.
2. TMPL-2.8 opened and built (decision 2026-10-23-023, the Chair's choice of fix): the walkthrough run
   for real on the private `SaltyBrett/launch-probe-s10` found GitHub's run on its Initial commit
   red, `doc-authority-scan` judging the uninitialized copy as the template. A copy is now told by
   its history and judged as a project; the birth probe also runs the suite on the Initial commit.
   At `30677d3` the probe reproduces GitHub's red run exactly; at `ea19c0d` it is green at the
   Initial commit and under both profiles, and run 40058466647 is green.
3. TMPL-5.5 done: the walkthrough's steps 1 to 4 and 9 run for real on `SaltyBrett/launch-probe-s10`
   as written, the red first run aside; steps 5 to 8 are TMPL-5.4's.
4. TMPL-5.4's first live run, the Chair at the keyboard in `SaltyBrett/launch-probe-s10`: intake,
   a pause, `status`, a bare resume and team selection worked as written; it stopped in the PRD
   stage. It found that no closeout is possible before planning, so a boundary before planning is a
   new conversation, still S1 (decision 2026-10-23-024, the Chair's choice, amending 2026-10-23-008
   and 2026-10-23-021).
5. TMPL-5.4's second run: a new conversation was S1 and resumed at the PRD; the draft's gaps logged
   in §11 and committed; a closeout before planning refused without a write. The emergency close's
   claim that the next `session-verify` fails, false before a project's first closeout, corrected in
   `AGENTS.md` and the handoff standard; `/clear` named as the boundary (2026-10-23-024, amended).
   Both runs recorded in [[reference_launch_live_run]]. Still unobserved: an approval, a skip with
   its reason, planning, a revision and the first closeout.

### Blockers

- None.

---

## S9 — 2026-10-23 — The birth probe, the doc-queue and the approval gate

**Status:** Cold start by the `SessionStart` hook: identity gate, pull and `session-verify` each
exit 0; the reads done by hand. Persona `framework-maintainer`, injected by the hook. The Chair
ordered TMPL-2.7 before TMPL-2.2, chose a `**Skips:**` line on a decision as a logged skip for
TMPL-5.3, and made `/project-launch` the Chair's alone for TMPL-5.2. TMPL-2.7, TMPL-2.2 and
TMPL-5.3 and TMPL-5.2 done, the Chair choosing mid-session that a reopened revision stands at
its last approved version (decision 2026-10-23-020, amended).

### Done

1. TMPL-2.7 (decision 2026-10-23-018): `scripts/birth_probe.py`, its `birth-probe-selftest` hook
   and runbook section, the `birth` job in `.github/workflows/gates.yml`, [[reference_ci_backstop]].
   Thirteen fixtures, ten broken variants caught. At `38c549d` the probe exits 1 under both
   profiles at `doc-authority-scan` alone; at `19537c4` it exits 0 under both, and run 40050465938
   is green on `gates` and both `birth` jobs.
2. TMPL-2.2 (decision 2026-10-23-019): the `doc-queue` gate as `doc_authority_scan.py --queue`,
   run at cold start by `scripts/session_start.py` and reported by the closeout skill; the
   `doc-drain` skill; the runbook's `doc-queue` section, the document-control standard's Recording a
   change, `AGENTS.md`'s cold start and skills table, [[reference_doc_authority]]. Sixteen broken
   variants caught. On a scratch birth the cold-start report read the queued story PASS at S1 and
   S2 and FAILED at S3; a fresh agent drained it by the skill alone, and its friction report
   corrected four steps before the skill shipped.
3. TMPL-5.3 (decision 2026-10-23-020): the approval gate in `doc-authority-scan`, a real epic
   needing an approved PRD and architecture or an APPROVED decision headed `**Skips:**`, the
   Chair's form; the runbook, the document-control standard, `docs/templates/README.md` and the
   planning skill's preconditions. Twenty-one fixtures, fifteen broken variants caught. On a scratch
   birth: refused with no documents and with drafts, passing once approved by the README, refused
   on a PRD revision the architecture lags, passing on an approved skip and refused on a proposed
   one.
4. TMPL-5.2 (decision 2026-10-23-021): `/project-launch`, the Chair's alone, in the main session,
   each stage's state read from the documents; team selection takes intake's answer, planning
   records its sources on the tracker's `**Source:**` line, the S1 entry's one next step names it;
   [[reference_project_launch]]. Decision 2026-10-23-020 amended so a revision in progress can be
   committed. A fresh agent applied `status` to two scratch trees and its friction report sharpened
   five rules; a birth from `6e94683` green under both profiles. The live run is TMPL-5.4's.

### Blockers

- None.

---

## S8 — 2026-10-23 — Four personas, team presets and the Blender connection

**Status:** Cold start by the `SessionStart` hook: identity gate, pull and `session-verify` each
exit 0; the reads done by hand. Persona `framework-maintainer`, injected by the hook. TMPL-5.1,
TMPL-2.6 (opened and done in the session, a release blocker its proof found) and TMPL-5.6 done;
TMPL-2.2 designed with the Chair and left to S9 by the Chair's choice.

### Done

1. TMPL-5.1 — `docs/templates/prd.md` and `docs/templates/architecture.md`, with
   `docs/templates/README.md` for making and approving a document (decision 2026-10-23-014). The
   Chair chose the location, each template an authority for its own scope, and both section lists;
   a made document is a draft, claiming no authority, until its approval decision gives it its first
   row. Proof on a scratch birth from this tree: drafts unregistered, exit 0; a copy that kept the
   template's line refused as `scope`; approved and stamped with its approval commit, exit 0; a
   swapped hash refused.
2. TMPL-2.6 — two defects of the authority gate, found by that proof (decision 2026-10-23-015, the
   Chair's choice of fix). A birth from the committed `HEAD` was refused at its first suite run:
   seven violations, each a template row or decision whose story a project's tracker cannot hold,
   since S7's marking came after its last scratch adoption. In a project the template's rows and
   decisions are now judged in the template. And `git log --follow` follows copies, so a PRD made
   from its template was stamped with the template's commit; the history now follows renames only.
   Nine fixtures, nine broken variants caught; a scratch birth starts green.
3. TMPL-5.6 — four library personas, `backend-engineer`, `web-developer`, `blender-artist` and
   `image-video-editor`, slugs and the three presets' membership the Chair's (decision
   2026-10-23-013). The presets and the connections are one YAML block in the team-selection skill;
   `skill-scan` gained `preset` and `connection`, so a preset naming a missing persona, an unpinned
   connection, or `.mcp.json` holding one in the template or without its persona fails. The
   connection is Blender Lab's own MCP server at v1.0.3's commit, its add-on pinned by SHA-256; the
   community server was rejected for default-on telemetry, PyPI builds its repository cannot
   reproduce and four advisories ([[reference_blender_mcp]]). Proof: eighty-three fixtures,
   twenty-five broken variants caught, a dead dedent removed when its variant passed; on real trees
   the template refused the connection, a birth wrote none, a project refused it without the
   persona and passed with it.
4. TMPL-2.2's row corrected (`dev-resources` retired, the `technical-writer` already in the library)
   and its design settled with the Chair for S9 to build (decision 2026-10-23-016): the queue is the
   stories marked `Queued: S<N>`, so TMPL-5.5's own runbook change is not the writer's; the drain
   forks as `general-purpose` in the library writer's role and leaves its change for review.

### Blockers

- None.

---

## S7 — 2026-10-23 — The authority gate, the `.gitignore` union and the first authorities

**Status:** Cold start by the `SessionStart` hook: identity gate, pull and `session-verify` each
exit 0; the reads done by hand. Persona `framework-maintainer`, injected by the hook. TMPL-2.1,
TMPL-2.5 and, by the Chair's choice over TMPL-5.1, TMPL-2.3 done.

### Done

1. TMPL-2.1 — `scripts/doc_authority_scan.py` and its two hooks after `kb-freshness-scan`, with
   their runbook sections (decision 2026-10-23-010, [[reference_doc_authority]]). The Chair chose two
   of the build's settlements: a version-log row is a `fact:` with its fact or cites a story whose row
   cites its decision; `**Affects:**` is required from decisions dated 2026-10-22. Proof: fifty-three
   fixtures pass; forty-five broken variants each failed a fixture without a crash. On the real tree:
   no authority yet (TMPL-2.3 marks them), every decision from the cutoff carries `**Affects:**`,
   exit 0. On a scratch clone with a marked copy of the document-control standard: `--stamp` waited
   for the commit and then wrote it, `--history` derived both rows across a rename, a swapped hash was
   refused, a shallow clone exited 2, and with no row citing decision 2026-10-22-002, which names the
   document, the gate reported it unrecorded. My first run of that last step passed because the
   probe's second row cited the same decision; corrected, it failed as it should. Also: `Story`
   carries its tracker row, the decision-log rule and the example body name the `**Affects:**` line,
   and TMPL-2.3 gains the retirement of `sprint/recovery/AUTHORITY_MATRIX.md`, a second registry kept
   by hand and already stale on personas.
2. TMPL-2.5 — `scripts/template_update.py` merges `.gitignore` with `git merge-file --union` where
   both sides changed one place, the project's lines first, and the dry run names the path `union`;
   every other path still conflicts (decision 2026-10-23-007). Proof: five new fixtures, seven
   broken variants each caught. A scratch `v2.0.0` built from this session's tree, and clones of
   Supplier_Research_Dev, Comfy and PocketGames (`--no-hardlinks`; the originals unchanged, still on
   `v1.0.0`) taken to it by Step 9 as written: each dry run named `.gitignore` `union` with no
   conflict, each `--apply` exit 0 with the whole suite green, the authority gate among it; each
   project's ignores kept whole and the template's block after them. [[reference_template_update]]
   and `TEMPLATE_GUIDE.md` Step 9 say so.
3. TMPL-2.3 — six authorities: the four standards, the document-control standard and the gate
   runbook (decision 2026-10-23-011). Each was read against every decision from the cutoff that
   names it; each log starts at the version it stated and cites them; the hand-kept changelog tables
   and `**Version:**` lines are gone, the handoff standard's eight rows all at 2.0. The
   document-control standard is rewritten around the gate and no longer says the template stays
   private. `gate_runbook_scan.py` skips the runbook's closing version log, three broken variants
   caught. `sprint/recovery/AUTHORITY_MATRIX.md` is removed from the template; the three projects'
   copies, `v1.0.0`'s unedited, stay theirs. Seen on the real tree before the decision existed: the
   gate refused the rows citing it, unindexed, and decision 2026-10-23-009 naming the runbook with no
   row and no story; queued in TMPL-5.5's row, which now names the path. After: six authorities,
   seventeen pairs recorded by a row, one queued, exit 0. Then the first real stamp: `--stamp`
   wrote 515f1a5, the commit that introduced the six rows, into each, and the gate verified all six
   against git.
4. After the three stories, the Chair named gaps in the library's team before the release: decision
   2026-10-23-012 adds a backend engineer, a web developer, a Blender 3D artist and an image and
   video editor, named team presets in team selection held by a gate, and an opt-in Blender MCP
   connection, off by default. Story TMPL-5.6 opened for S8; TMPL-2.4 waits on it.

### Blockers

- None.

## S6 — 2026-10-23 — Adoption from v1.0.0

**Status:** Cold start by the `SessionStart` hook: identity gate, pull and `session-verify` each
exit 0; the reads done by hand. Persona `framework-maintainer`, injected by the hook. TMPL-1.10 and
TMPL-1.7 done; epic TMPL-1 complete.

### Done

1. TMPL-1.10 — `scripts/template_update.py` converts every `docs/personas/` file into the roster,
   exactly or as a named conflict, with a converter that imports nothing from the project's old
   scripts; removes `.resources-version`; merges a `source: dev-resources` entry as content and
   unmarks one no release writes (decision 2026-10-23-005, superseding 2026-09-23-008). Proof:
   sixteen new fixtures; twenty-eight broken variants each caught, three first caught wrongly and
   the fixtures rewritten; every real persona file (`v1.0.0`'s, `dev-resources`' frozen tree, the
   three projects') converted to its library copy byte for byte, the one project persona lint-clean;
   the first run refused a real wrapped bullet, which showed a fixture had the rule backwards. Scratch
   clones of the three projects adopted a scratch `v2.0.0`: personas converted, stamp and marker
   gone, one `.gitignore` conflict each; resolved by hand, the whole suite passed on its first run.
2. TMPL-1.7 — a scratch birth beside the template (`tmpl-s6-probe`, origin a local bare repository
   by the operator's choice): `new_project.py --apply` exit 0, suite green, roster empty, library
   whole, `session-verify` exit 0 at S1 once the birth was committed. The operator ran one live
   session there: the start report arrived after the trust dialog; team selection asked, waited,
   activated two personas and drafted one, gate exit 0, committed; `/compact` re-injected "still
   S1" with the notes and journal; the forked closeout ran as `general-purpose` through scaffold,
   gate, commit and push, `gh run list` exit 1 with no GitHub remote, and left out the attribution
   trailer the harness asked for. Read from the session's transcript. Two gaps it reported, fixed
   (decision 2026-10-23-006): handoff sections 3 to 5 are now tokens to fill, three reverted
   variants each caught; S1's range starts at the first commit. Knowledge entry
   [[reference_claude_code_substrate]].
3. After the first closeout, with the operator: the `.gitignore` conflict settled as a union merge
   (decision 2026-10-23-007, story TMPL-2.5), and the project launch designed from the operator's
   proposal (decision 2026-10-23-008): `/project-launch` with intake, team, PRD, architecture and
   planning stages, each steered by the Chair with pause, skip, return and status; epic TMPL-5
   opened; and, at the operator's request, the root README as a walkthrough then a catalog of
   commands, held to the skills by `skill-scan` (decision 2026-10-23-009, TMPL-5.5). The release,
   TMPL-2.4, waits on all of it. The S7 pair was withdrawn and written again to carry them.

### Blockers

- None. Still unobserved: `disableWorkflows` in a live session. The probe folder `tmpl-s6-probe`
  beside the template can be deleted.

---

## S5 — 2026-10-23 — The persona library

**Status:** Started in the same Claude session as S4, after its closeout, at the operator's
request; the persona is unchanged (`framework-maintainer`). Cold start by hand: pull exit 0,
`session-verify` exit 0 at 5cccd1e, the handoff's reads read. Decision 2026-10-23-003's four
questions went to the operator first: the full team ships in `v2.0.0`, `dev-resources` retires, a
project's own personas stay in it, and the updater converts a `v1.0.0` project's `docs/personas/`
(the decision amended). TMPL-1.8 split into TMPL-1.8, TMPL-1.9 and TMPL-1.10; TMPL-1.8 and TMPL-1.9 done.

### Done

1. Decision 2026-10-23-003 amended with the answers; the tracker re-planned (TMPL-1.9, TMPL-1.10
   added; TMPL-1.7, TMPL-2.2, TMPL-2.4 and TMPL-3.1 follow).
2. TMPL-1.8 — the five personas moved to the library `personas/`, the template's
   roster keeping `framework-maintainer`; the closeout gate lints the library and holds each roster
   copy to it (fork and drift fail, a newer library version is noted); the team-selection skill;
   the initializer clears the roster at birth, the sanitizer keeps it, the updater keeps it and
   merges the library. The sync went with it, since it would write every persona into a roster:
   `resources_sync.py`, its hook, its closeout rule and the stamp removed, the shared knowledge
   entry made the template's own. Supersessions marked on both sides; the five entries the
   freshness gate then held were corrected against their decisions. Proof: twenty broken variants,
   each caught (three first written wrong and rewritten); plants of a drifted and a forked roster
   copy each failed the gate and a real commit; a library bumped past the roster passed silently,
   because pre-commit hides a passing hook's output, so the start hook now names it. A scratch
   birth: `new_project.py --apply` exit 0, the roster emptied, the library whole, `session-verify`
   exit 0 at S1, and a `claude -p` session listing only the built-in agents.
3. TMPL-1.9 — the library's team designed with the operator, who added business intelligence and
   reporting roles and the missing game development roles (decision 2026-10-23-004); thirty new
   personas written into `personas/` from one generator, every one passing the persona lint, and a
   plant of an unquoted `: ` item refused as `list`.

### Blockers

- None.

---

## S4 — 2026-10-23 — Procedures as skills; ownership of the new paths

**Status:** Cold start clean: the `SessionStart` hook ran the identity gate (PASS), the pull and
`session-verify` (PASS); both hook types installed; Claude Code 2.1.308. The skills page was read
whole (curl, 114 KB) before any build, with the sub-agents page's startup and tool sections. Two
choices went to the operator, both answered with the recommendation: the forked closeout takes the
next persona and the session's brief as arguments, and the release and the pristine cut are the
operator's alone (decision 2026-10-23-001). TMPL-1.4 and TMPL-1.6 done.

### Done

1. TMPL-1.4 — five skills in `.claude/skills/` (closeout forked as `general-purpose` with
   `background: false`; planning-session and document-production inline; release and pristine-cut
   the operator's alone). `AGENTS.md`'s procedures section rewritten to list them by path for any
   agent, the emergency close moved into its closeout bullet; the handoff, sprint and document
   standards keep the law and point to them; the scaffold's kickoff section 5 points to the
   closeout skill; [[reference_pristine_cut]] and [[reference_template_versioning]] keep the why.
   `skill-scan` and its self-test (43 fixtures) with runbook sections; 38 broken variants, each
   caught, one first written as a no-op and rewritten. Live: plants of a missing hook id and a
   missing stage each failed `pre-commit run skill-scan --all-files` (exit 1) and a real commit;
   the one-home grep finds each procedure's command in its skill alone; `claude -p "/closeout …"`
   in a scratch clone ran as a `general-purpose` subagent, first command `git status --short`,
   and stopped at the sync it could not get approved, tree untouched
   ([[reference_claude_code_skills]]).
2. TMPL-1.6 — ownership decided (decision 2026-10-23-002, made within 2026-10-22-001 and -005):
   `.claude/agents/` kept for the sync, with a fixture holding its path equal in the gate, the
   sync, the initializer, the sanitizer and the updater; `.claude/skills/`, `.claude/rules/` and
   `.claude/settings.json` three-way; the journal, the notes and `.claude/settings.local.json`
   named as `new_project.LOCAL_STATE`, touched by none of the three. Reading the tree found
   `settings.local.json` ignored only by the operator's global excludes file; `.gitignore` now
   carries it, and the initializer's fixture checks with the global file off. A project's
   `docs/personas/` adopts `v2.0.0` through `dev-resources`, never by conversion in the project.
   Self-tests 21, 36 and 20; 19 broken variants, each caught, one first written so it never
   applied and rewritten. Every real `.claude/` path and local file classifies as decided.
3. After the closeout (ecef26d, its `gates` run green), the operator approved a persona library
   in the template, inactive, with each project activating what it needs into `.claude/agents/` at
   its first session (decision 2026-10-23-003). TMPL-1.8 opened ahead of TMPL-1.7, four questions
   left open for its start, and the S5 pair re-pointed to it.

### Blockers

- None.

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

<!-- Add new session updates ABOVE this line, newest first, headed `## S<N> — YYYY-MM-DD — title` -->
<!-- Each entry: Done (by story ID), Blockers. Next-session tasks live in the kickoff, not here. -->
<!-- Keep the last 10 entries visible; move older ones to sprint/archive/ (the gate enforces the cap) -->
