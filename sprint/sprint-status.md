# Sprint Status

**Current Phase:** Template maintenance
**Current Focus:** v2.1.0 — the agentic development team and the coding standard (v2.0.0 released 2026-10-24)
**Last Updated:** 2026-10-24
**Updated By:** S20

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (setup, update cadence, sprint boundaries).
>
> **READ SELECTIVELY (index-first).** Read the header (Current Phase/Focus) and the newest session
> update first; older updates are context, not required reading. Keep the last 10 updates visible and
> archive older ones — `scripts/session_closeout.py --check` enforces the cap. Markdown only (never JSON).
> Every entry is headed `## S<N> — YYYY-MM-DD — <title>`; the gate reads the session number from it.

---

## S20 — 2026-10-24 — The writing standard's gate

**Status:** Cold start by the `SessionStart` hook: identity gate, pull, `session-verify` ("this is
S20") and `doc-queue` each exit 0; the reads done by hand. Persona `framework-maintainer`, injected
by the hook. TMPL-6.3 in progress: its plan settled with the Chair.

### Done

1. TMPL-6.3's plan, settled with the Chair (decision 2026-10-24-026): a glob that decides nothing
   refused in a production rule only, the text mode reading Office files itself, a custom voice
   told by the standard's section 2 table, the allow list exact but wrap-tolerant; the readers and
   the rules' exact reading by the AI. A probe outside the repository found 167 tracked markdown
   files, no carriage return, no YAML comment in a frontmatter and backtick fences only.
2. The writing standard at 1.1: the gate's reading stated in sections 2, 4, 5, 6, 7, 8, 9 and 11.
3. TMPL-6.3, the gate: `scripts/writing_standard.py`, the law read from the standard's sections 2,
   5 and 7, the profile and voices judged first, then every tracked markdown file whole; `--which`,
   and `--text` over `.docx`, `.pptx` and `.xlsx` read with the standard library. Its self-test
   holds 144 fixtures; a scratch harness broke the script 53 ways, one rule each, and every broken
   copy failed its self-test at the fixture named for that rule. Writing the harness found three
   fixtures that could not fail (closing hashes, a dash, a link's comma), each made to.
4. TMPL-6.3, the hooks: `writing-standard-selftest` at the commit stage and `writing-standard` at
   the manual stage, with their sections and the runbook at 1.14. A real Word file made by
   `scripts/md_to_docx.py` showed the converter writing U+2014 into every footer; the footer now
   reads `Generated from Markdown (draft)`, and a clean source's file passes `--text`.
5. TMPL-6.3, the updater: two fixtures in `template_update.py`'s self-test, each failing against a
   broken copy. On a scratch template with two releases, a project born green from the first, with
   a custom voice and its own profile lines, took the second: the profile merged, both sides' lines
   kept; the voice byte for byte unchanged; the suite green; `--which README.md` production there.
   The first birth was refused by `session-closeout-check` over a fixture's unresolved wikilink,
   now a real slug.
6. The document-production skill's check step names `--text` (2026-10-24-022).

### Blockers

- None.

## S19 — 2026-10-24 — The writing standard's law

**Status:** Cold start by the `SessionStart` hook: identity gate, pull, `session-verify` ("this is
S19") and `doc-queue` each exit 0; the reads done by hand. Persona `framework-maintainer`, injected
by the hook. TMPL-6.2 done: its plan settled with the Chair, then the law built and gated.

### Done

1. TMPL-6.2's plan, settled with the Chair: the writing standard's eleven sections, the voice file's
   shape, the profile's development paths, `agents: {}`, and consistency over cleverness on the
   rules page. Probes outside the repository measured the tree first: twenty distinct characters off
   a US keyboard, and `README.md` the template's one production file.
2. The README's audience (decision 2026-10-24-025, the Chair's): development in the template alone,
   by a `template:` list the gate applies only where `.project-profile` is absent, so a project's
   README is production; its reader added to TMPL-6.3.
3. TMPL-6.2, the law: `docs/standards/writing_standard_v1.0.md` at 1.0 (d1c6ef9), eleven sections
   and the two phrase tables of fifteen rows each; the seven voices in `docs/standards/voices/`;
   `writing-profile.yaml`, parsing with `rules`, `template`, `default`, `agents` and `allow`. A probe
   of the standard's own rules found no finding in any new file.
4. TMPL-6.2, the judgement: `.claude/rules/writing.md`, scoped to `**/*.md`; `personas/editor.md`
   and `personas/document-reviewer.md` at version 2, their changelog lines in the U+2014 form the
   persona gate reads. The rule and persona linters, called on broken variants, refused a dead
   glob, a planted `AGENTS.md` sentence, a body changed at version 1 and a missing changelog item.
5. TMPL-6.2, the move: section 9 of `docs/standards/document_production_standard_v1.0.md` a
   pointer and its vendor rule in section 10, at 1.1; the document-production skill's check step
   runs the writing rules over a produced file; `AGENTS.md`'s governance map and the README's
   standards table list the writing standard. With TMPL-6.2 Done, removing any one of 014 and 022
   from the 1.1 row, or 025 from the 1.0 row, makes `doc-authority-scan` report it unrecorded.
6. [[reference_writing_standard_design]]: why the README is development in the template alone, and
   why phrases skip code blocks and a list ends with its paragraph.

### Blockers

- None.

---

## S18 — 2026-10-24 — The writing standard designed with the Chair

**Status:** Cold start by the `SessionStart` hook: identity gate, pull, `session-verify` ("this is
S18") and `doc-queue` each exit 0; the reads done by hand. Persona `framework-maintainer`, injected
by the hook. TMPL-6.1 done: seven design questions answered by the Chair, one decision each, and
the build re-cut.

### Done

1. Design question 1, the voices (decision 2026-10-24-016): seven built in, the three proposed and
   Grammarly's four; a custom voice keeping the Chair's sample of 200 words or more and the traits
   drawn from it, in its own project, private.
2. Design question 2, the assignment (decision 2026-10-24-017): `writing-profile.yaml` beside
   `code-profile.yaml`, ordered path rules giving a voice and an audience, no frontmatter; a file no
   rule names judged as production; an agent's voice in the same profile, a document's own winning.
3. Design question 3, the first lists (decision 2026-10-24-018), measured on the template's tree
   first: characters off a US keyboard, letters excepted, code included; headings with a comma or
   semicolon, end punctuation or over 8 words; two exact-phrase tables in the standard, the lean
   design the Chair chose for its upkeep; development references in production documents; a
   project's allow list; tone found by the document reviewer and fixed by the editor.
4. Design question 4, the template's own documents (decision 2026-10-24-019): the template opts in;
   every tracked markdown file swept before `v2.1.0` is published, records included; whole files
   judged from then on, against drift past the rules; the formats the gates read moved to ASCII;
   each project swept at adoption.
5. Design question 5, enforcement (decision 2026-10-24-020, amending 2026-10-24-018): a mechanical
   finding refuses the commit and fails CI, its only exception an exact string in the allow list,
   now over all four rules, a change to it a gate change the Chair approves; a judgement finding
   pauses its story until the Chair answers in the code review log.
6. Design question 6, the humanizer (decision 2026-10-24-021): `/humanize` in the main session;
   certain fixes by script, the flagged text rewritten by an editor subagent in the assigned voice,
   the gate run again and every code span, link and number checked; the Chair reviews each file
   before it is kept; for text already in the tree, an agent fixing its own draft; a voice mode.
7. Design question 7, the em-dash rule (decision 2026-10-24-022): the document production
   standard's §9 moves whole to the writing standard, §10 stays; a deliverable's source judged by
   the gate and its produced file by the document-production skill.
8. TMPL-6 re-cut, approved by the Chair (decision 2026-10-24-023): TMPL-6.2 the law, 6.3 the gate,
   6.4 the formats the gates read moved to ASCII, 6.5 the humanizer and the agent's voice, 6.6 the
   sweep; TMPL-6.1 done; TMPL-4.6 waiting on TMPL-6.6; S19 opens with TMPL-6.2.
9. [[reference_writing_standard_design]]: why each choice, for the builders of TMPL-6.2 to TMPL-6.6.
10. After the closeout, the Chair's ask (decision 2026-10-24-024): the subagent ceiling, the session's
    model and effort never exceeded by a subagent, the operator choosing model and effort or effort
    only; opened as TMPL-3.5 with its design at its start, TMPL-4.6 waiting on it;
    [[reference_claude_code_subagent_model]], read in the documentation, not yet observed.

### Blockers

- None.

---

## S17 — 2026-10-24 — The `/story` skill and its live proof

**Status:** Cold start by the `SessionStart` hook: identity gate, pull, `session-verify` ("this is
S17") and `doc-queue` each exit 0; the reads done by hand. Persona `framework-maintainer`, injected
by the hook. TMPL-3.3 done.

### Done

1. TMPL-3.3's plan settled with the Chair: the skill in the main session, roles never committing or
   asking, the main session gating and committing each artifact and asking the Chair at each trigger
   and finding; the proof on a scratch copy of Comfy, run from this conversation with each role a
   general-purpose subagent carrying its persona, the story the per-stage timings in `watch_run.py`'s
   finished-run summary, the release pushed to a private scratch repository.
2. Decision 2026-10-24-014, the Chair's: a writing standard in `v2.1.0`, with voices assigned to a
   document and an agent, a gate over the mechanical tells of machine-written prose, and a
   humanizer skill, modelled on Grammarly's Humanizer; epic TMPL-6 opened, its design with the
   Chair at S18, TMPL-4.6 waiting on it.
3. TMPL-3.3 done (decision 2026-10-24-015): `.claude/skills/story/SKILL.md`, in the main session
   and the Chair's alone, listed in `AGENTS.md` and the README's catalog, `skill-scan` green. Proved
   on `story-probe-s17`, a clone of Comfy taken to a scratch `v2.1.0` by `template_update.py` with no
   conflict: CU-4.6 ran from brief to release, each role a general-purpose subagent carrying its
   persona, each artifact committed and passing `story-artifacts`, the build passing `code-standard`;
   two review findings answered by the Chair, `tests 1` fixed in the change with verify and review
   run again, `duplication 6` acknowledged with a later story; the release stopped until approved,
   then pushed to the private `SaltyBrett/story-probe-s17`, run 40111133105 green. On the closed
   story, the approval removed failed `trigger` and a log row removed failed `finding`.
   `personas/code-reviewer.md` version 3; [[reference_story_live_run]].
4. Three gaps the proof found, opened by the Chair as TMPL-3.4 (stale artifacts pass), TMPL-2.10 (a
   first push judged at its tip only) and TMPL-4.7 (the format check counting diff context, one
   unformatted line flagging seven); TMPL-4.6 waits on them.

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

<!-- Add new session updates ABOVE this line, newest first, headed `## S<N> — YYYY-MM-DD — title` -->
<!-- Each entry: Done (by story ID), Blockers. Next-session tasks live in the kickoff, not here. -->
<!-- Keep the last 10 entries visible; move older ones to sprint/archive/ (the gate enforces the cap) -->
