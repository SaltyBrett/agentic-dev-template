# Sprint Status

**Current Phase:** Template maintenance
**Current Focus:** v2.1.0 — the agentic development team and the coding standard (v2.0.0 released 2026-10-24)
**Last Updated:** 2026-10-24
**Updated By:** S17

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (setup, update cadence, sprint boundaries).
>
> **READ SELECTIVELY (index-first).** Read the header (Current Phase/Focus) and the newest session
> update first; older updates are context, not required reading. Keep the last 10 updates visible and
> archive older ones — `scripts/session_closeout.py --check` enforces the cap. Markdown only (never JSON).
> Every entry is headed `## S<N> — YYYY-MM-DD — <title>`; the gate reads the session number from it.

---

## S17 — 2026-10-24 — The `/story` skill and its live proof

**Status:** Cold start by the `SessionStart` hook: identity gate, pull, `session-verify` ("this is
S17") and `doc-queue` each exit 0; the reads done by hand. Persona `framework-maintainer`, injected
by the hook. TMPL-3.3 in progress.

### Done

1. TMPL-3.3's plan settled with the Chair: the skill in the main session, roles never committing or
   asking, the main session gating and committing each artifact and asking the Chair at each trigger
   and finding; the proof on a scratch copy of Comfy, run from this conversation with each role a
   general-purpose subagent carrying its persona, the story the per-stage timings in `watch_run.py`'s
   finished-run summary, the release pushed to a private scratch repository.

### Blockers

- None.

---

## S16 — 2026-10-24 — The team's law and its gate; Rust and Bevy the default stack

**Status:** Run in the S11 conversation at the Chair's request, the Chair remote, every question
answered in chat; the cold start run through `scripts/session_start.py` as `/clear` would run it:
identity gate, pull, `session-verify` ("this is S16") and `doc-queue` each exit 0, the journal's
`start S16` line written; the reads done by hand. Persona `framework-maintainer`. TMPL-3.2 done.

### Done

1. Decision 2026-10-24-012, the Chair's: Rust the default language and Bevy the default game engine,
   the launch's architecture stage proposing them first (`.claude/skills/project-launch/SKILL.md`);
   the Rust profile, supporting Bevy cleanly, required for `v2.1.0`, TMPL-4.4 carrying the Bevy
   requirement and TMPL-4.6, the release, waiting on it; TMPL-3.2 split, 3.3 opened for the `/story`
   skill and the live proof on a scratch copy of Comfy. S6's entry moved to the archive.
2. TMPL-3.2 done (decision 2026-10-24-013): `docs/standards/team_standard_v1.0.md` written as an
   authority (how a story runs, the artifacts and their frontmatter, the role map by story type, the
   eleven triggers and the Chair's approvals, findings in the code review log, the security audit);
   `scripts/story_artifacts.py`, reading the role map and the triggers from the standard itself, and
   hooks `story-artifacts-selftest` and `story-artifacts`; two runbook sections; `AGENTS.md` and the
   README name the standard; [[reference_story_artifacts]]. 38 fixtures; 27 broken variants, the
   first run vacuous (the runner's Python lacked PyYAML), the rerun exposing five fixtures that
   tripped a neighbouring rule, rewritten until each is caught by its own; `code_standard.py`'s 25
   rerun and confirmed the same way.

### Blockers

- None.

---

## S15 — 2026-10-24 — The coding standard's gate: advise, document, the Chair decides

**Status:** Run in the S11 conversation at the Chair's request, the Chair remote, every question
answered in chat; the cold start run through `scripts/session_start.py` as `/clear` would run it:
identity gate, pull, `session-verify` ("this is S15") and `doc-queue` each exit 0, the journal's
`start S15` line written; the reads done by hand. Persona `framework-maintainer`. TMPL-4.3 done.

### Done

1. TMPL-4.3's plan settled with the Chair: a project opts in with `code-profile.yaml`; the template
   does not opt in; coverage by the project's own tests; linter and type findings on changed lines
   only; the audit on a manifest change and over every pushed range.
2. Mid-build the Chair set the rule (decision 2026-10-24-011, amending 2026-10-24-006, -007 and
   -009): the standard advises and documents and never forces a code change. A finding pauses a
   commit or a story only until `docs/code_review_log.md`, append-only, holds it with the Chair's
   response; an answered finding pauses nothing again unless it gets worse; the Chair's
   acknowledgement is the exception, the exceptions file gone; the code reviewer and the security
   auditor under the same rule. `docs/standards/coding_standard_v1.0.md` 1.1 (§4 the code review
   log), `personas/code-reviewer.md` version 2, `.claude/rules/code-quality.md`,
   [[reference_code_review_log]] new, [[reference_coding_standard_calibration]] corrected.
3. TMPL-4.3 done: `scripts/code_standard.py`, its Python measurer on Python's `ast` (counting `case`,
   which lizard missed) with the tokenizer's recall check; hooks `code-standard-selftest`,
   `code-standard` and `code-standard-range`; the CI range step shared with the commit-message
   check; three runbook sections. 59 fixtures, the gate's numbers held to the standard's §2 and its
   own functions to the limits; 25 broken variants each caught. On a scratch copy of Comfy: an
   over-limit function paused the commit and the Chair's row let it proceed with no code changed; a
   worse value, a clone, a suppression and untyped, unformatted, untested lines paused it; a
   compliant change passed; an edited log row was refused; the range hook passed a compliant range
   and paused a six-parameter function. The proof's first run found ruff's C901 duplicating the
   measurer, so ruff's limit rules are off. S5's entry moved to the archive.

### Blockers

- None.

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

<!-- Add new session updates ABOVE this line, newest first, headed `## S<N> — YYYY-MM-DD — title` -->
<!-- Each entry: Done (by story ID), Blockers. Next-session tasks live in the kickoff, not here. -->
<!-- Keep the last 10 entries visible; move older ones to sprint/archive/ (the gate enforces the cap) -->
