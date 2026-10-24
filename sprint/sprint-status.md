# Sprint Status

**Current Phase:** Template maintenance
**Current Focus:** v2.1.0 — the agentic development team and the coding standard (v2.0.0 released 2026-10-24)
**Last Updated:** 2026-10-24
**Updated By:** S14

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (setup, update cadence, sprint boundaries).
>
> **READ SELECTIVELY (index-first).** Read the header (Current Phase/Focus) and the newest session
> update first; older updates are context, not required reading. Keep the last 10 updates visible and
> archive older ones — `scripts/session_closeout.py --check` enforces the cap. Markdown only (never JSON).
> Every entry is headed `## S<N> — YYYY-MM-DD — <title>`; the gate reads the session number from it.

---

## S14 — 2026-10-24 — The coding standard written; its build split by stack

**Status:** Run in the S11 conversation at the Chair's request, the Chair remote, every question
answered in chat; the cold start run through `scripts/session_start.py` as `/clear` would run it:
identity gate, pull, `session-verify` ("this is S14") and `doc-queue` each exit 0, the journal's
`start S14` line written; the reads done by hand. Persona `framework-maintainer`. TMPL-4.2 split by
the Chair and its first part done.

### Done

1. TMPL-4.2 split by the Chair (decision 2026-10-24-010): 4.2 the law and the judgement layer; 4.3
   the gate's core with the Python profile, proved on Comfy; 4.4 the Rust profile, proved on
   PocketGames, the Rust toolchain decided at its start; 4.5 the TypeScript profile, proved on
   fixture code. TMPL-3.2 now waits on 4.3.
2. TMPL-4.2 done: `docs/standards/coding_standard_v1.0.md` written as the ninth authority, its
   version log citing decisions 2026-10-24-007 to -009 (the limits, their scope, the exceptions file
   `code-exceptions.yaml`, proved measurement, the mapping rule); `.claude/rules/code-quality.md`,
   path-scoped to code, opening with `CONSTITUTION.md` §4A; `personas/code-reviewer.md` in the
   library from decision 2026-10-24-009's brief; `AGENTS.md`'s governance map and the README's
   standards list name the standard. Each new file's gate shown to read it: an unquoted persona list
   item refused as `list`, a rule restating `AGENTS.md` as `rule-restates`, a dead glob as
   `rule-dead`; the suite exit 0. S4's entry moved to `sprint/archive/sprint-status_2026.md`.

### Blockers

- None.

---

## S13 — 2026-10-24 — The coding standard calibrated on industry code

**Status:** Run in the S11 conversation at the Chair's request, the Chair remote, every question
answered in chat; the cold start run through `scripts/session_start.py` as `/clear` would run it:
identity gate, pull, `session-verify` ("this is S13") and `doc-queue` each exit 0, the journal's
`start S13` line written; the reads done by hand. Persona `framework-maintainer`. TMPL-4.1 done,
design and proof only, no build.

### Done

1. TMPL-4.1, with the Chair and a specialized reviewer agent. The Chair chose industry reference
   code over the framework's own: ripgrep 14.1.1, packaging 24.1 and zod v3.23.8 as known-good,
   the Gilded Rose and Tennis refactoring katas as known-bad, in Rust, Python and TypeScript, pinned,
   measured with lizard and jscpd and never run. Published defaults confirmed against their sources
   (NIST SP 500-235 §2.5, SonarQube's Sonar way, clippy, pylint, ESLint). Decision 2026-10-24-007:
   per changed function complexity 15, 60 code lines, 5 parameters; no new clones; 80% of new lines
   covered; tests at 10 and 100; file length a reviewer signal at 500; exceptions recorded and never
   growing. Decision 2026-10-24-008: each language's measurer proves itself by a fixture and a recall
   check, the reviewer agent having found lizard 1.17.10 silently skipping Rust and TypeScript
   (ripgrep's `dir.rs`, 58 functions, measured as none; a typed TypeScript method dropped; both
   reproduced by the session); the per-stack mapping rule. Decision 2026-10-24-009: the judgement
   page and the code reviewer's and security auditor's briefs. Recorded in
   [[reference_coding_standard_calibration]].
2. TMPL-4.2 scoped by them in the tracker. S3's entry moved to
   `sprint/archive/sprint-status_2026.md`, the eleventh over the cap.

### Blockers

- None.

---

## S12 — 2026-10-24 — The team designed: orchestration, triggers and the role map

**Status:** Run in the S11 conversation at the Chair's request, the Chair remote with no terminal,
every question answered in chat; the cold start run through `scripts/session_start.py` as `/clear`
would run it: identity gate, pull, `session-verify` ("this is S12") and `doc-queue` each exit 0, the
journal's `start S12` line written; the reads done by hand. Persona `framework-maintainer`. TMPL-3.1
done, design only, no build.

### Done

1. TMPL-3.1, the design session with the Chair, logged as three decisions. The orchestration
   (2026-10-24-004): a `/story <ID>` skill in the main session, since no subagent can ask the
   operator, runs one story end to end, each role a roster subagent handing off through committed
   artifacts in `docs/stories/<ID>/`, a gate judging each before the next role starts, stopping only
   at a trigger or a gate failing three times running; the law in a new team standard. The triggers
   (2026-10-24-005): decision 2026-10-22-003's seven plus a deploy or release, a gate or CI change,
   data loss and a license change, detected from the diff and declared by the roles, a story closing
   only with each hit trigger approved. The role map (2026-10-24-006): five story types, every
   library persona given its artifact and judging gate, `devops-engineer` shipping, the code
   reviewer's slot left to TMPL-4.1.
2. TMPL-3.2 scoped by them in the tracker; it waits on TMPL-4.2. S2's entry moved to
   `sprint/archive/sprint-status_2026.md`, the eleventh over the cap.

### Blockers

- None.

---

## S11 — 2026-10-24 — The launch proved live, and two silent gaps

**Status:** Cold start through `scripts/session_start.py` at session start: identity gate, pull,
`session-verify` and `doc-queue` each exit 0; the reads done by hand. Persona
`framework-maintainer`. TMPL-5.4 done, its third run with the Chair at the keyboard in
`SaltyBrett/launch-probe-s10` observing every remaining stage through the probe's first closeout.
Two gaps it found, each passing silently, opened as TMPL-2.9 and TMPL-5.7 by the Chair's choice of
fix, both before TMPL-2.4, and both built. Then TMPL-2.4 done: `v2.0.0` released, the three projects
taken to it, `dev-resources` archived.

### Done

1. TMPL-5.4's third run, read from the probe's commits and transcripts: the PRD approved and stamped
   (`5794166`, `8c748b1`); `skip architecture` logged with the Chair's reason (`4169b9c`); planning's
   epic LP-1 with the `**Source:**` line `PRD 1.0, architecture skipped` (`0e19e71`),
   `doc-authority-scan` on it exit 0; the PRD revised to 1.1 and re-approved (`1ae29c9`, `62006ff`),
   `status` reading planning stale; the first closeout `c0a6db7` passing `session-closeout`, pushed,
   run 40063609570 green on `gates` and both `birth` jobs; the probe's `session-verify` after it
   exit 0, "This is S2". Recorded in [[reference_launch_live_run]]; TMPL-5.4 Done.
2. TMPL-2.9 opened and built (decision 2026-10-24-001, the Chair's choice of fix):
   `doc-authority-scan` read an `**Affects:**` path only in a code span, and
   `docs/templates/README.md` step 5 did not say to use one, so the probe's PRD approval passed
   unchecked. Now the `bare-path` rule refuses an authority's path written bare, and step 5 says
   so; seven fixtures, five broken variants each caught, the real tree passing.
3. TMPL-5.7 opened and built (decision 2026-10-24-002, the Chair's choice of fix): the probe's
   first closeout, typed as `/closeout` and run as the fork, closed S1 on an entry still headed
   `emergency checkpoint`, saying its closeout was not completed, its `### Next` stale. Now
   `--closeout` refuses an entry so headed or holding `### Next`; the closeout and launch skills,
   `AGENTS.md`, the README's step 7 and the initializer's S1 text say so. Nine fixtures, seven
   broken variants each caught; on a scratch clone of the real tree refused by `--closeout` alone.
4. S1's entry moved to `sprint/archive/sprint-status_2026.md`, the eleventh over the cap.
5. TMPL-2.4 started: its open question settled by the Chair (decision 2026-10-24-003), each
   project's PRD and architecture approved as they stand in its adoption commit, the step named in
   `TEMPLATE_GUIDE.md`. Proved on a scratch `v2.0.0` cut from `dee7385`: each project's clone adopted
   by the release's updater with no conflict, refused only by the two `approval` lines, then green
   with the as-is approval, before and after the stamp.
6. TMPL-2.4: `v2.0.0` released by the Chair (`/release`): `release: v2.0.0` at `a159053`, tagged
   MAJOR; runs 40066350212 (`main`) and 40066356871 (the tag) green on `gates` and both `birth` jobs.
7. TMPL-2.4: the three projects taken to `v2.0.0`, each by the release's updater, its documents
   approved as they stood, stamped, pushed and green on `gates` and both `birth` jobs:
   Supplier_Research_Dev (`96993b6`, `9f05e46`; architecture skipped by the Chair; run
   40066882658), Comfy (`ba0da08`, `13b9f4d`; run 40066960006, carrying its unpushed S4 commits),
   PocketGames (`5089cf5`, `3fbc6e3` on `build/milestone-1`, its working branch; run 40067080070).
   No project syncs from `dev-resources`. Recorded in [[reference_v2_adoption]].
8. TMPL-2.4 done: `dev-resources` given a retirement notice at the top of its README (`4e062ea`,
   run 40067296277 green), then archived, read-only, at the Chair's choice.

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

<!-- Add new session updates ABOVE this line, newest first, headed `## S<N> — YYYY-MM-DD — title` -->
<!-- Each entry: Done (by story ID), Blockers. Next-session tasks live in the kickoff, not here. -->
<!-- Keep the last 10 entries visible; move older ones to sprint/archive/ (the gate enforces the cap) -->
