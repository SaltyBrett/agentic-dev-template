# Framework Decisions

**Purpose:** The decisions that shaped this template — why every gate, script and rule is the way it is
**Source:** `agentic-dev-template`; carried to a project by `scripts/template_update.py`, merged by decision ID
**Last Updated:** 2026-10-24

> **READ SELECTIVELY (index-first).** Do NOT read this file whole. Read the **Decision Index**, then only
> the entries a task, a handoff or a knowledge entry's `teaches:` points at. Markdown only (never JSON).
>
> **This is the template's log, not the project's.** A project's own decisions go in
> `sprint/decision-log.md`, which ships with the `[EXAMPLE]` entry only. `scripts/kb_freshness_scan.py`
> and `scripts/session_closeout.py` read both indexes as one set, so a knowledge entry may `teaches:` an
> ID from either and a handoff may cite either. Never edit this file in a project: the updater replaces
> an unedited row or body when a release changes it and reports an edited one. IDs here are bare dates;
> a project prefixes its own (`ACME-2026-09-24-001`) so the two sets cannot collide — on a duplicate ID
> this file's row wins (decision 2026-09-23-003, [[reference_framework_decisions]]).
>
> In the template itself, a session that makes a framework decision logs it **here**: a new index row at
> the top of the table, its body at the end of the file, format `[YYYY-MM-DD-NNN]`.

---

## Decision Index

| ID | Date | Title | Status |
|----|------|-------|--------|
| 2026-10-24-021 | 2026-10-24 | The `/humanize` skill, in the main session: certain fixes by script, the flagged text rewritten by an editor subagent in the assigned voice, the gate run again and every code span, link and number checked; the Chair reviews each file before it is kept; for text already in the tree, an agent fixing its own draft; a voice mode capturing a custom voice; started by an agent or the Chair | APPROVED |
| 2026-10-24-020 | 2026-10-24 | The writing gate refuses a mechanical finding, locally and in CI, printing its fix; an exception is an exact string in the profile's allow list, now covering all four mechanical rules, a change to it a gate change the Chair approves; a judgement finding pauses its story until the Chair answers in the code review log | APPROVED |
| 2026-10-24-019 | 2026-10-24 | The template opts in to the writing standard: every tracked markdown file swept before `v2.1.0` is published, records included; then whole files judged on every commit, never changed lines only; the formats the gates read moved to ASCII; each project swept at adoption | APPROVED |
| 2026-10-24-018 | 2026-10-24; amended 2026-10-24 | The writing guardrails' first lists: characters off a US keyboard, letters excepted, code included; headings with a comma or semicolon, end punctuation or over 8 words; two exact-phrase tables in the standard, read by the gate; development references in production documents; a project's allow list; tone judged by the document reviewer against a rules page, rewritten by the editor | APPROVED |
| 2026-10-24-017 | 2026-10-24 | Voices and audiences assigned in `writing-profile.yaml`, beside `code-profile.yaml`: ordered path rules, the first match winning, no frontmatter; a file no rule names judged as production; an agent's voice in the same profile, a document's own voice winning | APPROVED |
| 2026-10-24-016 | 2026-10-24 | The writing standard's voices: seven built in, the three proposed and Grammarly's four; one file per voice holding its traits and phrase list; a custom voice keeping the Chair's sample of 200 words or more and the traits drawn from it, kept in its own project, private | APPROVED |
| 2026-10-24-015 | 2026-10-24 | The `/story` skill as built, proved live on a scratch copy of Comfy: roles write and the main session gates, commits and asks; a finding reaches the code review log once, with the Chair's words; the code reviewer persona at version 3; three gaps the proof found opened as TMPL-3.4, TMPL-2.10 and TMPL-4.7, the release waiting on them | APPROVED |
| 2026-10-24-014 | 2026-10-24 | The writing standard opens as epic TMPL-6 in `v2.1.0`: assignable voices, a gate over the mechanical tells of machine-written prose (characters off a US keyboard, headings that read as sentences, AI and marketing phrasing, development artifacts in production documents) and a humanizer skill; designed with the Chair at S18; the release waits on it | APPROVED |
| 2026-10-24-013 | 2026-10-24 | The team standard and the `story-artifacts` gate as built: the artifacts' frontmatter and bodies, the role map and the triggers read by the gate from the standard itself, the release always a trigger, a review or security finding answered in the code review log before the story moves on | APPROVED |
| 2026-10-24-012 | 2026-10-24 | Rust is the Chair's default language and Bevy the default game engine: the launch's architecture stage proposes them first; the coding standard's Rust profile, supporting Bevy cleanly, is required for `v2.1.0`, its release a story of its own; TMPL-3.2 split into the team standard with its gate and the `/story` skill with the live proof | APPROVED |
| 2026-10-24-011 | 2026-10-24 | The coding standard advises and documents and never forces a code change: a finding pauses a commit or a story only until `docs/code_review_log.md`, append-only, holds it with the Chair's response; the Chair's acknowledgement is the exception, the exceptions file gone; the gate core and its Python profile as built; amends 2026-10-24-006, 2026-10-24-007 and 2026-10-24-009 | APPROVED |
| 2026-10-24-010 | 2026-10-24 | TMPL-4.2 split, larger than one session: 4.2 the standard, the judgement page and the code reviewer; 4.3 the gate's core and the Python profile, proved on Comfy; 4.4 the Rust profile, proved on PocketGames, the Rust toolchain decided there; 4.5 the TypeScript profile, proved on fixture code; TMPL-3.2 waits on 4.3 | APPROVED |
| 2026-10-24-009 | 2026-10-24; amended 2026-10-24 | The coding standard's judgement page (`.claude/rules/code-quality.md`, path-scoped to code, opening with `CONSTITUTION.md` §4A) and its two briefs: the code reviewer, a new library persona, never the implementer; the security audit, `security-engineer`'s brief for the security stage | APPROVED |
| 2026-10-24-008 | 2026-10-24 | The coding standard's measurement is proved, per language: each stack's profile names one pinned tool per slot, configured to the core numbers and never looser, and a tool counts only once it passes its language's measurement fixture and a recall check on every run; `lizard` 1.17.10 fails Rust and TypeScript | APPROVED |
| 2026-10-24-007 | 2026-10-24; amended 2026-10-24 | The coding standard's core limits, proved against ripgrep, packaging and zod and the Gilded Rose and Tennis katas: per added or edited function, complexity 15, 60 code lines, 5 parameters; no new clones; 80% of new lines covered; tests at complexity 10 and 100 lines; file length a reviewer signal at 500; exceptions recorded, never growing | APPROVED |
| 2026-10-24-006 | 2026-10-24; amended 2026-10-24 | The team's role map: five story types (software, data, document, game, media) whose brief picks the stages and roles; every library persona given its artifact and its judging gate; the verifier and reviewer never the builder; `devops-engineer` ships; the code reviewer's slot left to TMPL-4.1 | APPROVED |
| 2026-10-24-005 | 2026-10-24 | The review triggers: decision 2026-10-22-003's seven plus a deploy or release, a gate or CI change, data loss and a license change; detected from the diff where the change shows it and declared by a role otherwise; a story closes only with every hit trigger approved by the operator in its folder | APPROVED |
| 2026-10-24-004 | 2026-10-24 | The team's orchestration: a `/story <ID>` skill in the main session runs one story end to end, each role a subagent from the roster handing off through committed artifacts in `docs/stories/<ID>/`, a gate judging each before the next role starts; it stops only at a review trigger or a gate failing three times running; the law in a new team standard | APPROVED |
| 2026-10-24-003 | 2026-10-24 | At adoption of `v2.0.0`, a project with real epics approves the PRD and architecture it has been built from as they stand, in the adoption commit: authority frontmatter, a version log opening at the version each states, a project approval decision; with no architecture, the Chair's skip; settles TMPL-2.4's open question | APPROVED |
| 2026-10-24-002 | 2026-10-24 | `session-closeout` refuses to close a session whose entry is still headed `emergency checkpoint` or holds the initializer's `### Next`, a record saying the session is still open; the closeout and launch skills, `AGENTS.md`'s emergency close, the README's step 7 and the initializer's S1 text say so; found by the live launch's first closeout, typed as `/closeout` and run as the fork | APPROVED |
| 2026-10-24-001 | 2026-10-24 | `doc-authority-scan` refuses an authority's path written outside a code span in `**Affects:**`, which it never reads there, and `docs/templates/README.md` step 5 says the path goes in a code span; found by the live launch, whose PRD approval named the PRD bare and passed unchecked | APPROVED |
| 2026-10-23-024 | 2026-10-23; amended 2026-10-23 | Before planning, a launch stage's session boundary is a new conversation, still S1, not a closeout, since no kickoff can cite a story until planning writes the first; the first closeout comes after planning; amends 2026-10-23-008 and 2026-10-23-021 | APPROVED |
| 2026-10-23-023 | 2026-10-23 | A copy of the template before its initializer, GitHub's "Initial commit", judges the template's rows and decisions in the template as a project does, its history holding none of their stamped commits; the birth probe also runs the suite on the Initial commit, as GitHub does; amends 2026-10-23-015, 2026-10-23-017 and 2026-10-23-018 | APPROVED |
| 2026-10-23-022 | 2026-10-23 | The README front page as built: a nine-step walkthrough from `gh repo create` to taking a release, each step what to type and what to see; a catalog of the commands by skill path, the operator scripts, the session hooks and the gates by link; `TEMPLATE_GUIDE.md` cut to named sections on what the initializer leaves; `skill-scan` refusing a skill the `## Catalog` section does not name, in the template and in a project | APPROVED |
| 2026-10-23-021 | 2026-10-23; amended 2026-10-23 | `/project-launch` as built: the Chair's alone (`disable-model-invocation`), in the main session; each stage's state read from the documents, with skipped, reopened and stale; intake's answers written into the PRD draft, §9 carrying the expertise to the team stage; the plan's versions on the tracker's `**Source:**` line; the S1 entry's one next step | APPROVED |
| 2026-10-23-020 | 2026-10-23; amended 2026-10-23 | The approval gate as built: in a project with a real epic, one PRD in `docs/prd/` and one architecture in `docs/architecture/` standing approved, a reopened revision standing at its last approved version (amended, the Chair's choice), an approved architecture's `prd:` the PRD's newest version; or an APPROVED project decision headed `**Skips:**` naming the stage (the Chair's form); a rule of `doc-authority-scan`, on every commit | APPROVED |
| 2026-10-23-019 | 2026-10-23 | The doc-queue as built: `doc_authority_scan.py --queue`, a manual hook the start hook runs at cold start and the closeout reports; a note counts written bare on an open story naming one authority and a decision; the session at work is one rule in `session_closeout.py`; the drain is `doc-drain`, forked as `general-purpose` in the writer's role, uncommitted | APPROVED |
| 2026-10-23-018 | 2026-10-23; amended 2026-10-23 | The birth probe as built: the revision's tree by `git archive`, one "Initial commit", that revision's initializer with `--apply`, no `GIT_*` or `CLAUDE_PROJECT_DIR` reaching it; a `birth-probe-selftest` hook over a stub initializer; a `birth` job in CI, one run per profile, skipped in a project; red at `38c549d` under both profiles | APPROVED |
| 2026-10-23-017 | 2026-10-23; amended 2026-10-23 | CI makes a scratch project on every push to the template: `scripts/birth_probe.py` births a committed revision through the initializer, whose own suite run is the verdict, once per profile; proved red at the commit that blocked births; built as TMPL-2.7 before the release | APPROVED |
| 2026-10-23-016 | 2026-10-23 | The doc-queue as designed for TMPL-2.2: the writer's queue is the open stories marked `Queued: S<N>`, failing at cold start once older than one session; the drain forks as `general-purpose` in the library technical writer's role, one document each, and leaves its change for the main session to review and commit | APPROVED |
| 2026-10-23-015 | 2026-10-23; amended 2026-10-23 | In a project the authority gate judges what the template wrote in the template: a row citing only framework decisions is held to neither its marker nor its hash, a framework decision to neither its `**Affects:**` nor its record, so a birth from the template starts green; and a row's commit is found following renames but never a copy; amends 2026-10-23-010 | APPROVED |
| 2026-10-23-014 | 2026-10-23 | The PRD and architecture templates as built: in `docs/templates/`, each the authority for its own scope so a document made from it claims the project's; a made document a draft until approved, when it becomes the authority with its first row citing the approval; the PRD's eleven sections with goals, FR and NFR numbered, the architecture's thirteen ending in the dependency layers | APPROVED |
| 2026-10-23-013 | 2026-10-23 | TMPL-5.6 as built: `backend-engineer`, `web-developer`, `blender-artist`, `image-video-editor`; the three presets as proposed, Website with `business-writer`; presets and connections one YAML block in team selection, held by `skill-scan`; the connection the Blender Lab server pinned to v1.0.3's commit, the community server rejected | APPROVED |
| 2026-10-23-012 | 2026-10-23 | The library gains a backend engineer, a web developer, a Blender 3D artist and an image and video editor; team-selection offers named team presets, a gate refusing a preset that names no library persona; an opt-in Blender MCP connection offered with the Blender persona, off by default; built as TMPL-5.6 before the release | APPROVED |
| 2026-10-23-011 | 2026-10-23 | The standards, the document-control standard and the gate runbook are the first authorities: each log starts at marking at the version the document states, citing every decision that names it or queueing it; the hand-kept changelog tables and `**Version:**` lines go; file names keep their version; the runbook gate skips the closing version log; the authority matrix retires in the template, a project's copy left to the project | APPROVED |
| 2026-10-23-010 | 2026-10-23; amended 2026-10-23 | The authority gate as built: the frontmatter is the registry; a version-log row is a `fact:` with its fact or the change of a story citing its decision; `**Affects:**` required from decisions dated 2026-10-22; a hash verified as the first commit holding its version, the template's rows verified in the template; one scope, one authority | APPROVED |
| 2026-10-23-009 | 2026-10-23 | The root README is the operator's front page: a step-by-step walkthrough from creating a project through the session loop, then a catalog of every command, operator script and session hook, the gates by link to their runbook; `skill-scan` holds the catalog to the skills; the live launch proof follows the walkthrough as written | APPROVED |
| 2026-10-23-008 | 2026-10-23; amended 2026-10-23 | A project launches through `/project-launch`: intake by three questions or a summary of the PRD, team, PRD, architecture and planning, each stage led by its persona and steered by the chair with pause, skip, return and status; documents versioned and approved on record, a revision flagging the stages built on it; a gate that a real epic needs an approved PRD and architecture or a logged skip | APPROVED |
| 2026-10-23-007 | 2026-10-23 | The updater merges `.gitignore` by union, keeping both sides' lines where both changed the same place, since project and template both append at its end; every other three-way path still conflicts | APPROVED |
| 2026-10-23-006 | 2026-10-23 | What the substrate's live proof found: the closeout's scaffold leaves handoff sections 3 to 5 as tokens to fill, since a pre-filled `- None.` passed unwritten beside a logged decision, and S1's range starts at the repository's first commit | APPROVED |
| 2026-10-23-005 | 2026-10-23 | Adoption from `v1.0.0`, judged by what the project holds: every `docs/personas/` file converted into the roster exactly or refused as a conflict, by a converter that reads nothing from the project's old scripts; the sync's stamp removed; a `source: dev-resources` entry merged like any other and, where no release writes it, stripped of the declaration | APPROVED |
| 2026-10-23-004 | 2026-10-23 | The library's team: roles across the software lifecycle, data science with BI and reporting, document management, writing and quality control, and game development, each a persona in the agent-file shape with the shared habits; a code reviewer left to TMPL-4 | APPROVED |
| 2026-10-23-003 | 2026-10-23; amended 2026-10-23 | Personas ship as a library in the template, inactive; a project activates the ones it needs into `.claude/agents/` at its first session, where a skill recommends from the library and drafts what it lacks; the full team ships in `v2.0.0`; `dev-resources` retires; a project's own personas stay in it; the updater converts a `v1.0.0` project's `docs/personas/`; built as TMPL-1.8 to TMPL-1.10 | APPROVED |
| 2026-10-23-002 | 2026-10-23 | The Claude Code paths and the session's local files are owned by decision: the registry kept for the sync, the skills, rules and settings merged three-way, the journal, notes and local settings untouched and ignored by the repository itself; a project's `docs/personas/` reaches `.claude/agents/` through `dev-resources`, never by conversion in the project | APPROVED; SUPERSEDED (bullets 1, 4 and 5) by 2026-10-23-003 |
| 2026-10-23-001 | 2026-10-23 | Procedures are skills, and a skill is repository markdown: one `SKILL.md` per procedure, listed by path in `AGENTS.md` for any agent; the closeout forked with the brief in its arguments, the release and the pristine cut the operator's alone; the standards keep the law; `skill-scan` keeps every hook, stage and command a skill names in step with the config | APPROVED |
| 2026-10-22-006 | 2026-10-22 | Rules under `.claude/rules/` are path-scoped judgement only and gated: `paths:` that parse and match a tracked file, no sentence of `AGENTS.md` repeated; `CONSTITUTION.md` §6.3 becomes a knowledge entry for the why and two rules for the instructions, and the knowledge index sheds its frontmatter block to a rule | APPROVED |
| 2026-10-22-005 | 2026-10-22 | Personas are agent files in `.claude/agents/`, the body the Invocation and the rest in frontmatter; the session takes its persona from the `SessionStart` hook, `claude --agent` optional because it replaces Claude Code's built-in prompt; the kickoff names the agent; `dev-resources` holds both trees until TMPL-2.4; amends 2026-10-22-001 | APPROVED; SUPERSEDED (dev-resources holding the registry) by 2026-10-23-003 |
| 2026-10-22-004 | 2026-10-22 | The session journal and the working notes are local and gitignored: the journal records raw commands that must not enter a public history, an ignored file is outside pre-commit's stash, and the Stop hook excludes both by path as well; the closeout gate clears them | APPROVED |
| 2026-10-22-003 | 2026-10-22 | `v2.1.0`: an agentic development team of role subagents whose handoffs are gated artifacts, and a coding standard built as mechanical limits, a process layer and one page of judgement; each opens with a design session, the standard proved against real code before adoption; MINOR | APPROVED |
| 2026-10-22-002 | 2026-10-22 | Authoritative documents stop going stale: `authority:` frontmatter and a version log on each source of truth, `Affects:` on every decision, a gate that accepts a version-log row or an open tracker story and nothing else, the commit stamped after the fact and verified, a technical-writer agent draining the queue at cold start; part of `v2.0.0` | APPROVED |
| 2026-10-22-001 | 2026-10-22; amended 2026-10-22 | `v2.0.0`: the framework runs on Claude Code's native machinery where that removes overhead without removing a control: one cold start run by a SessionStart hook, a Stop hook for checkpoint discipline, a journal and working notes against compaction, personas as subagents, procedures as forked skills, path-scoped rules, the constitution and checklist slimmed, the interop contract retired; git hooks and CI stay the enforcement; MAJOR | APPROVED |
| 2026-09-25-004 | 2026-09-25 | The public template's versioning starts at `v1.0.0` on the finished go-live tree: the four go-live tags removed, the tree sanitized to S1, one tag cut; history kept, nothing force-pushed; the earlier "released as" notes read as folded into it | APPROVED |
| 2026-09-25-003 | 2026-09-25 | A ruleset on `main` in both public repositories blocks deletion and force-push; no required status check, because every checkpoint is a direct push by one developer; revisit at the first second contributor | APPROVED |
| 2026-09-25-002 | 2026-09-25 | MIT license, copyright Brett Bennett, in the template and in `dev-resources`; a project receives it at birth and owns it from then on, the updater never writes it; PATCH | APPROVED |
| 2026-09-25-001 | 2026-09-25 | The template and `dev-resources` are public; a project made from the template is private by default, refused by the initializer when public unless `--public`; the archive stays private; branch protection still not enabled; `dev-resources` pins https and gets a `gates` workflow; MINOR | APPROVED |
| 2026-09-24-001 | 2026-09-24; amended 2026-09-24 | Rules with no control found in the fossil sweep: the tracker's dependency and placeholder rules get a gate (TMPL-5.5, built: `dependency-order` and `live-placeholder`, MAJOR); the pull-request workflow, review checklist and manifest are deleted; evidence capture is procedure, marked ungated; PATCH for the sweep | APPROVED |
| 2026-09-23-008 | 2026-09-23 | A knowledge entry is a resource entry when it teaches no decision and explains a machine, a tool or a workflow rather than this repository; the macOS toolchain entry moves, every gate entry stays | APPROVED; SUPERSEDED by 2026-10-23-005 |
| 2026-09-23-007 | 2026-09-23; amended 2026-09-23 | The registry and resource entries are synced from `dev-resources` by `resources_sync.py`: verdicts decided by version, conflicts never picked silently, growth only through `--publish`, the updater keeps those paths, the closeout refuses an unpublished persona; MAJOR | SUPERSEDED by 2026-10-23-003 |
| 2026-09-23-006 | 2026-09-23 | Personas are append-only, gated: `version:` and a `## Changelog` in every persona, an Invocation change refused without a bump against the committed copy, the kickoff names the version; MAJOR | APPROVED |
| 2026-09-23-005 | 2026-09-23; amended 2026-09-23; amended 2026-09-25 | The template is a pre-commit hook repository: `.pre-commit-hooks.yaml` publishes the persona linter, the frontmatter gate and the attribution gate as console scripts of a `pyproject.toml` package that leaves a project at birth; the gates read their root from git | APPROVED |
| 2026-09-23-004 | 2026-09-23 | Commit classification is not built: the release bump stays a documented judgement, because the decision that introduces a change already names its bump and the windows it would compute over are small | APPROVED |
| 2026-09-23-003 | 2026-09-23; amended 2026-09-24 | The template is sanitized to a pristine `v1.0.0` from a fresh init after its build history is archived; framework decisions move to `docs/governance/framework_decisions.md` (built as TMPL-4.1, MAJOR); the sanitizer and the sweep (built as TMPL-4.2, MINOR); the archive repository named; the cut done (TMPL-4.4), this repository archived and the new lineage at `v1.0.0` | APPROVED |
| 2026-09-23-002 | 2026-09-23 | `dev-resources` is the durable home for personas and reference knowledge: projects hold a stamped snapshot synced at closeout, ownership is disjoint from the template's, personas are append-only and enhanced by version | APPROVED; SUPERSEDED (personas and shared knowledge in dev-resources) by 2026-10-23-003 |
| 2026-09-23-001 | 2026-09-23 | The gate suite is described by one runbook page that a gate keeps in step with the config; every hook declares its stage; released MAJOR | APPROVED |
| 2026-09-22-004 | 2026-09-22; amended 2026-09-24 | A derived project takes a newer release through `template_update.py`: ownership by path as the initializer's inverse, keyed merges for the index and the framework decisions file (the project's decision log until 2026-09-23-003 was built), three-way for the rest | APPROVED |
| 2026-09-22-003 | 2026-09-22; amended 2026-10-22 | The closeout command runs with `--all-files`, because pre-commit stashes unstaged edits and the gate then judges the wrong tree; amended: the cold-start verify too, where the stash made a dirty tree pass | APPROVED |
| 2026-09-22-002 | 2026-09-22 | The derived-project probe: the initializer regenerates the tracker; CI restores annotated tags; the version gate names a lightweight tag | APPROVED |
| 2026-09-22-001 | 2026-09-22; amended 2026-09-22; amended 2026-09-23; amended 2026-09-25 | CI runs the gate suite on every push and pull request; a reporting backstop; branch protection not enabled, first for want of a plan, then (public, 2026-09-25-001) because checkpoints push straight to `main` | APPROVED |
| 2026-09-21-001 | 2026-09-21; amended 2026-09-24 | Session closeout is a gate; handoff and kickoff prompt are one-session repo artifacts; personas are shape-gated; every wikilink in the tree resolves | APPROVED |
| 2026-09-20-009 | 2026-09-20 | A project starts on the `gcc` or `commercial` profile; the toggle is mechanical | APPROVED |
| 2026-09-20-008 | 2026-09-20 | gitleaks joins the suite; a private repo has no other secret control | APPROVED |
| 2026-09-20-007 | 2026-09-20 | Employer identifiers are refused by hash, not by name; channel renamed | APPROVED |
| 2026-09-20-006 | 2026-09-20 | Template version is verified against its tags; bump type is a documented judgement | APPROVED |
| 2026-09-20-005 | 2026-09-20 | Parse `.codex/config.toml`; required keys at top level, `sandbox_mode` forbidden at any depth | APPROVED |
| 2026-09-20-004 | 2026-09-20 | Scope the decision-index parser, fail loudly on an unreadable index, self-test it | APPROVED |
| 2026-09-20-003 | 2026-09-20 | Validate KB frontmatter with a parser, and cross-check both readers agree | APPROVED; SUPERSEDED (table-in-body constraint only) by 2026-09-20-004 |
| 2026-09-20-002 | 2026-09-20; amended 2026-09-20 | Content rules are a second scanner channel that bypasses `EXCLUDE_FILES` | APPROVED |
| 2026-09-20-001 | 2026-09-20 | Every clone installs both pre-commit hook types (`pre-commit` + `commit-msg`) | APPROVED |
| 2026-09-19-001 | 2026-09-19 | Split the template from employer-specific brand and program content | APPROVED |
| 2026-07-30-001 | 2026-07-30 | Portable execution identity: no sandbox execution + user-reviewed approvals | APPROVED |

---

## Decision 2026-07-30-001: Portable execution identity and approval boundary

**Date:** 2026-07-30
**Made By:** Chair + AI
**Status:** APPROVED

### Context

Requiring Codex Full access as a precondition conflates two separate controls: command sandbox scope
and approval policy. It also turns `read-only` / `workspace-write` metadata into a false hard stop even
when the client can request approved execution under the operator's existing identity.

### Decision

- Never create or use a sandbox account, sandbox identity, restricted sandbox token, private sandbox
  desktop, or native Windows sandbox execution for repository commands.
- If a session exposes a sandbox boundary, request user-reviewed escalation before every local
  command; never try the sandbox first.
- Treat `read-only` / `workspace-write` metadata as a reason to escalate, not a reason to abandon the
  session.
- If already unsandboxed under the existing operator identity, retain
  `approval_policy = "untrusted"` and `approvals_reviewer = "user"`.
- Stop when escalation is unavailable or still executes through a sandbox/offline identity.

### Enforcement

`.codex/config.toml`, the canonical `AGENTS.md`, `AGENT_INTEROP.md`, `CONSTITUTION.md`, the cold-start
checklist, `scripts/agent_execution_identity_guard.py`, and the first local pre-commit hook.

### Official basis

- <https://learn.chatgpt.com/docs/agent-approvals-security.md>
- <https://learn.chatgpt.com/docs/permission-modes.md>
- <https://learn.chatgpt.com/docs/config-file/config-reference.md>
- <https://learn.chatgpt.com/docs/windows/windows-sandbox.md>

---

## Decision 2026-09-19-001: Split the template from employer-specific brand and program content

**Date:** 2026-09-19
**Made By:** Chair + AI
**Status:** APPROVED

### Context

The framework was developed inside an employer repository and its origin pointed at that employer's
GitHub Enterprise instance. An audit before porting it to a personal machine found employer-specific
content in exactly three locations, with every other file already generic:

- `resources/branding/` — logos, typeface guide, color palette, two branded Word templates
- `resources/README.md` — brand palette values and template filenames
- `docs/standards/document_production_standard_v1.0.md` — brand values plus internal product,
  platform, and program names

`AGENTS.md`, `CONSTITUTION.md`, `AGENT_INTEROP.md`, all four scripts, the sprint scaffolding, and the
other three standards carried no employer identifiers.

The governance machinery is the reusable contribution. The brand assets and program names are not,
and they should not travel to a personal account where they would sit in a private repository that
receives no secret scanning on a free plan.

### Decision

- Maintain two lineages. The employer repository keeps brand assets and program-specific content and
  stays on the employer's GitHub Enterprise instance. The personal template carries only the
  governance machinery.
- Tokenize rather than delete the contaminated documents. `resources/README.md` and the document
  production standard keep their structure, section order, label key (`[Brand official]`, `[Locked]`,
  `[Suggested]`, `[Get from source]`), and craft rules, with brand values replaced by `{{TOKENS}}`.
  The method is the reusable part; the values are per-project.
- Ship `resources/branding/` empty with a scaffold, so the shape is obvious and the assets are not.
- Sections 7 through 14 of the document production standard remain portable craft rules and apply as
  written in any project. Sections 1 through 6 require token fill before first use.
- Start the personal lineage from a fresh `git init`. The prior history is not carried across, which
  also removes the employer remote and the stale generated pre-commit hook.

### Rationale

Splitting on content rather than on file boundaries keeps the framework's value intact. A de-branded
template is in fact more reusable than the original, because §6 of `AGENT_INTEROP.md` already
describes the framework as a template meant to travel between repositories with per-project content
swapped out. This decision makes the existing intent literal.

### Enforcement

`resources/README.md` and `docs/standards/document_production_standard_v1.0.md` carry a template note
directing token fill before first use. No mechanical gate enforces de-branding; adding one is an open
question below.

### Open questions

- ~~Should `banned_feature_scan.py` gain a rule that fails the commit when a known employer
  identifier appears in the personal lineage?~~ **RESOLVED by 2026-09-20-007** — yes. Identifiers are
  matched by hash rather than listed by name, so the rule does not publish what it suppresses.

---

## Decision 2026-09-20-001: Every clone installs both pre-commit hook types

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`scripts/commit_attribution_scan.py` blocks AI attribution trailers in commit messages. It must run at
the `commit-msg` stage, because the commit message does not exist when pre-commit-stage hooks fire.

`pre-commit install` writes only `.git/hooks/pre-commit`. A clone that ran the old command has the
attribution gate in `.pre-commit-config.yaml` and no `.git/hooks/commit-msg` to invoke it. The gate is
then **present in config and absent in practice** — a config file that reads as protected while every
commit passes unchecked. That is strictly worse than having no gate, because it removes the reason to
look.

`.git/hooks/` is never committed, so no repo-side change can fix this. It is a per-clone action, and
the only defense is that the documented command be correct everywhere it appears.

### Decision

- The per-clone install command is, repo-wide and without exception:

      pre-commit install --hook-type pre-commit --hook-type commit-msg

- Every hook in `.pre-commit-config.yaml` declares an explicit `stages:`. A hook with no `stages:` key
  runs at *every installed stage*, so installing the `commit-msg` hook type would otherwise re-run the
  identity, banned-feature and KB-freshness gates a second time on each commit. The three existing
  gates are pinned to `stages: [pre-commit]`; the attribution gate is pinned to `stages: [commit-msg]`.
- The cold-start checklist verifies both hook files exist (`ls .git/hooks/`) rather than asking whether
  "pre-commit is installed", which is the question that passes while the gate is inert.

### Consequences

- **Every existing clone must re-run the install command.** Pulling this change does not install the
  commit-msg hook. Until an operator runs it on a given machine, that machine's attribution gate does
  not exist.
- `pre-commit run --all-files` exercises the pre-commit stage only, so it will report a clean suite on
  a machine where the attribution gate is not installed. Verifying a commit-msg gate requires
  `pre-commit run --hook-stage commit-msg --commit-msg-filename <file>` or a real trial commit.
- Any future commit-msg-, pre-push- or post-checkout-stage gate inherits this problem. Adding a hook at
  a new stage means updating the documented install command in the same work unit.

### Enforcement

`.pre-commit-config.yaml` (header comment + explicit `stages:` on every hook), `TEMPLATE_GUIDE.md`
Step 6, `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md` Part A, `sprint/sprint-status.md`, and the
knowledge entries [[reference_commit_attribution_gate]], [[reference_macos_toolchain]] §1,
[[reference_precommit_interpreter]].

### Related

- `AGENTS.md` prime directive forbidding AI attribution in commit messages
- `CONSTITUTION.md` §6.2 (pre-commit hooks are the primary gate; do not bypass)

---

## Decision 2026-09-20-002: Content rules are a second scanner channel, not more banned patterns

**Amended 2026-09-20 by 2026-09-20-007:** the channel was renamed `PORTABILITY_RULES` -> `CONTENT_RULES`
when a provenance rule joined it. The decision's substance — a second channel that bypasses
`EXCLUDE_FILES`, with per-rule `allow` sets — is unchanged.

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

Every documented way to run a gate by hand invoked the gate script with a bare `python`, which cannot
execute on macOS. The hooks were portable; only the prose was broken. It was corrected across `README.md`,
`AGENTS.md`, the cold-start checklist, four script docstrings and the Claude allow-list — but as a
convention it would return, because the rule lived only in a knowledge entry.

The obvious enforcement was a new entry in `BANNED_PATTERNS` in `scripts/banned_feature_scan.py`.
**That would not have worked, and it would have looked like it was working.** `BANNED_PATTERNS` is
filtered through `EXCLUDE_FILES`, which exempts `AGENTS.md`, `AGENT_COLDSTART_CHECKLIST.md`,
`CONSTITUTION.md` and `TEMPLATE_GUIDE.md` so that governance docs may legitimately *name* banned
Fabric features. Two of those four are where this defect actually landed. The gate would have been
inert in exactly the files it most needed to cover, and a green scan would have certified them.

### Decision

- Add a second channel, `CONTENT_RULES` (originally `PORTABILITY_RULES`), checked by `should_scan_content()` /
  `scan_portability()`. It applies `SCAN_EXTENSIONS` and `EXCLUDE_DIRS` but **not** `EXCLUDE_FILES`.
- Each rule carries its own `allow` set of filenames, so an exemption is one rule in one file rather
  than a whole file dropping out of the scan. The bare-`python` rule allows exactly three:
  `.pre-commit-config.yaml` (resolves inside pre-commit's virtualenv), the knowledge entry that quotes
  the broken pattern to teach it, and the scanner that holds the pattern.
- Each rule carries a `fix` string, printed with the violation. A gate that says only "blocked"
  invites a bypass; one that names the correct command does not.
- Portability matching is **case-sensitive**, unlike `BANNED_PATTERNS`, so prose such as "Python
  scripts" is not a violation. `\s+` cannot cross the `3`, so `python3 scripts/…` passes.

### Consequences

- Exempting a file from a content rule means adding it to that rule's `allow` set. Adding it to
  `EXCLUDE_FILES` instead silently drops it from every banned-feature check as well.
- `EXCLUDE_FILES` now has a narrower meaning than its name suggests: it governs `BANNED_PATTERNS`
  only. The comment above `CONTENT_RULES` records why.
- Future content rules (ambient tool names, absolute paths, OS-specific separators) belong in this
  channel rather than in `BANNED_PATTERNS`.

### Verification

A probe line added to `AGENTS.md` — an `EXCLUDE_FILES` member — exits 1; removing it exits 0. Blocking
was confirmed by exit code, not by console text.

### Enforcement

`scripts/banned_feature_scan.py`, already wired as a pre-commit-stage hook. Taught by
[[reference_precommit_interpreter]].

---

## Decision 2026-09-20-003: Validate KB frontmatter with a parser, and cross-check both readers agree

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`kb_freshness_scan.py` reads frontmatter with two regexes rather than a YAML parser. Regexes match;
they do not validate. An entry whose frontmatter is not loadable YAML still satisfies both patterns,
so the gate reports green on a file no YAML consumer can read — the same shape as the defect the
freshness gate exists to catch, one level down.

Investigating this surfaced a second and harder problem. The two parsers **disagree about several
spellings that are valid YAML**, measured rather than assumed. The unquoted zero-padded form is the
only one they read alike; the full comparison is tabulated in
[[reference_kb_frontmatter_validation]]. In short:

- an unquoted zero-padded date is read identically by both — this is the only agreeing spelling
- a **quoted** date is a clean string to YAML and invisible to the regex, which reports UNSTAMPED
- a **timestamp** is truncated by the regex and kept whole by YAML
- a **non-padded** date is a plain string to YAML and invisible to the regex
- `teaches:` as a **block list** parses correctly and is read as empty by the regex, which silently
  skips the entry altogether
- `teaches:` with **quoted** IDs keeps the quote characters in the regex path, so every ID is UNKNOWN

Two are traps. Quoting the date is the natural response to "make it valid YAML" and makes the
freshness gate report a missing date that is visibly present. A block `teaches:` list is idiomatic,
parses correctly, and makes the entry vanish from the freshness gate while still looking stamped.

A separate coverage gap: an entry with `teaches: []` can never be reported stale, so a green scan
reads as full coverage when it is a fraction of it.

### Decision

- Add `scripts/kb_frontmatter_scan.py`, hooked at `stages: [pre-commit]` per decision
  `2026-09-20-001`, with `additional_dependencies: [pyyaml]` — possible only because hooks declare
  `language: python` (decision context: [[reference_precommit_interpreter]]).
- It fails on: no frontmatter block, a YAML parse error, a missing `teaches` key, a missing
  `verified` key, and a `verified` value that is not an unquoted ISO date.
- **It does not enforce "valid YAML". It enforces the intersection — the one spelling both gates read
  identically.** Valid YAML the freshness gate cannot see is still a defect.
- That last rule is implemented as a **cross-check**, not as an enumerated rule list: the scanner
  imports `kb_freshness_scan.parse_frontmatter`, parses each entry both ways, and fails when the
  results differ. The table above is documentation, not logic, so a future divergence is caught
  without anyone remembering to update a rule.
- It runs **before** the freshness gate in the hook order. Validate the input before trusting the
  check that consumes it.
- `teaches: []` stays legal. `kb_freshness_scan.py --list` reports gate reach and names uncovered
  entries — informational, never a failure. Forcing a decision ID into an entry that explains none
  would manufacture a false link, a worse defect than no link.
- Without PyYAML the scanner exits **2**, never 0. A missing parser must not present as a pass.

### Consequences

- Never quote `verified:` or the IDs in `teaches:`, and never write `teaches:` as a block list. All
  three are valid YAML and all three break the freshness gate.
- The freshness regex's strictness is load-bearing and must not be relaxed to accept a new spelling:
  `kb_freshness_scan` compares dates as **strings**, which is correct only for zero-padded ISO.
- Any future consumer of this frontmatter is added to the cross-check rather than trusted to agree.
- ~~Do not put a markdown table in a decision body if any row's second cell contains an ISO date.~~
  **SUPERSEDED by 2026-09-20-004.** This was a prose constraint guarding an append-only file, which
  is not a control. `load_decisions()` is now scoped to the Decision Index section, so a table in a
  decision body is simply not read. Tables in decision bodies are permitted again.

### Verification

Six malformed entries were injected into `docs/orchestration/knowledge/` one at a time — invalid
YAML, quoted date, block list, missing `teaches`, missing `verified`, non-date `verified`. Each
exited 1; the tree returned to exit 0 after removal. Confirmed by exit code without a pipe, since a
pipe reports the last command's status rather than the scanner's.

### Correction to the report that prompted this

The report cited `reference_precommit_interpreter.md` as having been committed with a malformed
`name:` scalar. It was not: that file parses cleanly under `yaml.safe_load` at every commit in its
history in the archive repository, including the one that introduced it. The **mechanism** is real and was reproduced
with a constructed probe; the specific historical instance was not. Recorded so the next reader does
not go looking for a defect that was never in the tree.

### Enforcement

`.pre-commit-config.yaml` (`kb-frontmatter-scan`, before `kb-freshness-scan`). Taught by
[[reference_kb_frontmatter_validation]].

---

## Decision 2026-09-20-004: Scope the decision-index parser, fail loudly, and self-test it

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED
**Supersedes:** 2026-09-20-003 (the table-in-body prose constraint only; the rest of that decision —
frontmatter validation and the parser cross-check — stays in force)

### Context

`load_decisions()` parsed every `|`-prefixed line in `sprint/decision-log.md`, so a markdown table in
a decision body was absorbed as a phantom decision. Decision 2026-09-20-003 answered that with a
written rule: do not put such tables in decision bodies.

**A prose constraint guarding an append-only file is not a control.** It has no enforcement, and it
sits in the one file that grows without review — every future decision is a fresh chance to violate
it, and the violation is silent. It is also the exact fossil shape `CONSTITUTION.md` §6.3 exists to
catch: a written rule standing in for a mechanism.

The latent failure was worse than the phantom row. Because the parser scanned the whole file, a
rename of the `## Decision Index` heading would have yielded zero decisions with no error. Every
`teaches:` would then report UNKNOWN — or, with nothing stamped, the gate would report **green while
checking nothing**. That is the same failure mode as the regex-not-a-parser defect in 003.

### Decision

- `load_decisions()` reads the **Decision Index section only**. The boundary is taken from the file's
  actual structure: the `## Decision Index` heading, then the contiguous run of `|` lines beneath it,
  ending at the first horizontal rule, the next heading, or the end of the table.
- **An index that cannot be located raises `DecisionIndexNotFound` and exits non-zero** with a
  diagnostic. An unreadable index is never zero decisions. The same applies to a decision log that is
  missing while entries still declare `teaches:` — that now fails instead of returning 0.
- The parser proves its own boundary on every commit. `--self-test` runs nine in-memory fixtures
  covering: index rows parsed, a table inside a decision body, a `|`-prefixed body line shaped to look
  like an index row, `[EXAMPLE]` rows, supersession resolution, an index with zero data rows, a
  missing heading, and a heading with no table. Wired as `kb-freshness-selftest`, `stages:
  [pre-commit]` per 2026-09-20-001, ordered before the gate it validates.
- Tables in decision bodies are permitted again. The constraint from 2026-09-20-003 is withdrawn.

### Consequences

- Renaming the `## Decision Index` heading now breaks the build loudly instead of silently emptying
  the gate. Renaming it deliberately means updating `INDEX_HEADING` in the same work unit.
- Fixtures must **discriminate**. The first draft of the "pipe-prefixed body line" fixture passed
  against the broken parser too — its second cell held no date, so the old code rejected it for an
  unrelated reason. A fixture that passes under the bug is false confidence; it was reshaped to carry
  a date and now fails against the unscoped parser. Verified by running the suite against a
  monkeypatched copy of the original parser: 5/9 pass, and the phantom `` `verified: 2026-09-20` ``
  reappears exactly as it did in the real file.

### Audit: the same shape elsewhere

Every gate script was checked for "scans a whole file for a pattern rather than a scoped region".

- **`commit_attribution_scan.py` — FOUND, FIXED HERE.** `git commit --verbose` appends the staged
  diff below a scissors line, and those diff lines are not comment-prefixed. The scanner read the
  diff as if it were the message, so staging any change touching an attribution example — `AGENTS.md`
  carries one in its prime directive — blocked the commit and told the author to remove a line they
  never wrote. Demonstrated, then fixed by truncating at the scissors line. Re-verified in four
  directions: clean-message-with-dirty-diff passes, dirty-message-above-scissors still blocks, and
  both non-verbose cases are unchanged.
- **`agent_execution_identity_guard.py` — FOUND, NOT FIXED.** It checks `.codex/config.toml` with
  `re.MULTILINE` over the whole file, unscoped by TOML table. A probe config with
  `approval_policy = "untrusted"` under `[some.unrelated.table]` **passes the gate** while
  `tomllib` reports the top-level key as absent — i.e. absent where Codex actually reads it. This is
  a false negative in the zero-th gate. Left for a separate decision because the fix needs one:
  `tomllib` is stdlib only on Python 3.11+, so a clone on 3.10 needs a fallback or a declared
  `additional_dependencies: [tomli]`. Recorded as an open question below.
- **`banned_feature_scan.py` — not this defect.** Whole-file scanning is its purpose; its scoping is
  the per-rule `allow` sets and `EXCLUDE_FILES` (2026-09-20-002).
- **`kb_frontmatter_scan.py` — not this defect.** It parses a delimited frontmatter block, and the
  cross-check against the freshness gate's reader is itself a boundary assertion.
- **`md_to_docx.py`** is a converter, not a gate.

### Open questions

- ~~Should `agent_execution_identity_guard.py` parse `.codex/config.toml` with `tomllib` and assert
  the keys at top level?~~ **RESOLVED by 2026-09-20-005** — yes, with a `tomli` fallback declared via
  `additional_dependencies`.

### Verification

`--self-test` exits 0 against the fixed parser and 1 against a monkeypatched copy of the original,
naming the exact phantom ID the real file produced. The full suite was run with a renamed index
heading (exit 1, diagnostic) and restored (exit 0). All by exit code without a pipe.

### Enforcement

`scripts/kb_freshness_scan.py` (`index_rows`, `DecisionIndexNotFound`, `--self-test`) and
`.pre-commit-config.yaml` (`kb-freshness-selftest`). Taught by
[[reference_kb_frontmatter_validation]].

---

## Decision 2026-09-20-005: Parse the Codex config, and fail closed in both directions

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED
**Resolves:** the open question on 2026-09-20-004

### Context

The zero-th gate checked `.codex/config.toml` with `re.MULTILINE` over the whole file. Two false
negatives, both measured against real probe files:

- keys under `[some.unrelated.table]` — the regex matched; `tomllib` reports top level as empty, so
  the keys were absent exactly where Codex reads them
- a file containing `this is not = = valid toml [[[` — the regex matched; no TOML parser can load it

The second was not in the original audit. It is the regex-is-not-a-parser defect from 2026-09-20-003,
in the one gate that runs first.

### Decision

- Parse with `tomllib` (3.11+), falling back to `tomli`, declared as
  `additional_dependencies: [tomli]` on both identity hooks. **No parser available exits 2, never 0**,
  per the precedent set by `kb_frontmatter_scan.py`. A missing parser must not present as a pass.
- **Required keys are checked at top level**, where Codex reads them. A key found elsewhere is not
  compliance, and the diagnostic names the table it was found in — otherwise the next reader concludes
  the key is missing and adds a second copy.
- **`sandbox_mode` is forbidden at any depth.** See the reasoning below.
- A nested `approval_policy` / `approvals_reviewer` that *contradicts* the required value is also a
  violation. A profile table that weakens the approval policy is precisely the bypass this gate
  exists to prevent.
- `--self-test` with nine in-memory fixtures, wired as `agent-execution-identity-selftest` ahead of
  the gate it validates, per the pattern in 2026-09-20-004.

### Why the rule is asymmetric

Required keys must be where Codex reads them; a forbidden key is refused wherever it appears. The
asymmetry is not an inconsistency — **both directions fail closed**:

- Whether a nested table is live is external, versioned knowledge about another tool. Codex supports
  profile tables selectable at launch, and this gate must not encode a guess about which tables are
  active in which version.
- If a nested `sandbox_mode` is inert, refusing it costs nothing: the remedy is deleting a key that
  does nothing.
- If it is live, refusing it is the entire purpose of the gate.
- Either way its presence states intent to configure a sandbox mode, which the law forbids outright.

Checking a forbidden key only at top level would have been a regression — the old regex, being
line-based and unscoped, did catch `sandbox_mode` under `[profiles.x]`. A fixture pins that.

### Audit: the identity check itself

`getpass.getuser()` plus `USERNAME` / `USER` / `LOGNAME`, matched against `sandbox|codex.*offline`.

**This is not the config bug's shape.** The config bug was an unscoped text scan of a structured file.
This is a **provenance** defect: the inputs are not the authority.

`getpass.getuser()` is environment-first by its own implementation — it reads LOGNAME, USER, LNAME,
USERNAME and only then falls back to the password database. So all four inputs collapsed into one
class, environment, and the gate had no authoritative source at all. Demonstrated: with `USER` and
`LOGNAME` set to `sandbox-agent`, the guard reports a forbidden identity on a machine whose real uid
resolves to `twdaddy`; the environment alone decided the verdict, in both directions.

Fixed here: `pwd.getpwuid(os.getuid())` is consulted first and is the name reported in the PASS line,
which now carries its source — `PASS (twdaddy [uid]; …)` or `[env-only]` where `pwd` is unavailable,
as on Windows. Environment values are still read as additional signals, but they can no longer hide
the uid-derived name.

**What remains, stated plainly:** name matching is a denylist. It catches an identity *named*
sandbox/offline, not every sandboxed identity, and no local check can prove the boundary a session
was launched under. The docstring already called this defense in depth; that remains true, and is now
true of an input that is at least authoritative.

### Verification

Fixtures were run against the **old** regex parser before being trusted: 6 of 10 passed there and
were testing nothing. The three that discriminate are the unrelated table, the weakened profile, and
malformed TOML — plus the diagnostic assertion, which the old parser cannot satisfy.

Then proved on **real probe files** written to `.codex/config.toml`, by exit code without a pipe:
baseline 0; unrelated table 1; malformed TOML 1; `sandbox_mode` under `[profiles.x]` 1; missing key 1;
file absent 1; restored 0, byte-identical.

One harness bug was found and fixed in the process: the extra diagnostic assertion raised `IndexError`
instead of reporting FAIL when the parser returned no violations. A self-test that crashes reports
nothing at the moment it matters most.

### Enforcement

`scripts/agent_execution_identity_guard.py` and `.pre-commit-config.yaml`
(`agent-execution-identity-selftest`, then `agent-execution-identity`). Taught by
[[reference_execution_identity_config]].

---

## Decision 2026-09-20-006: Verify the template version against its tags; keep the bump a judgement

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`new_project.py` stamps `.template-version` into every project it initializes, from a constant in its
own source. Nothing compared that constant to the tag. Tag `v1.1.0`, forget to bump the constant, and
every project created afterwards is labelled `v1.0.0` — silently. The only existing check confirmed
the string *looked* like a version, not that it was the right one.

That was the last hand-maintained value in the repository, and the same convention-instead-of-control
shape as the twelve defects already recorded. It was introduced in the same session that removed the
others, which is why it is being closed rather than noted.

A second question came with it: what justifies `v1.1.0` over `v1.0.1`?

### Decision

**The mechanics are gated. The bump is not, because it cannot be.**

`scripts/template_version.py --check` runs on every commit and verifies, for every tag:

1. the name is `vMAJOR.MINOR.PATCH`
2. the commit it points at carries `TEMPLATE_VERSION` equal to that tag
3. the annotation names the bump — MAJOR, MINOR or PATCH

Rule 3 exempts the earliest tag, and not as a carve-out: a bump is defined relative to a predecessor,
and the first release has none. The gate skips entirely in a repository with no tags, which is every
project created from this template.

The bump *type* stays a documented judgement in [[reference_template_versioning]], keyed to one
question: **would adopting this force a human to do something** — run a different command, or edit a
file to pass a check that did not exist? Yes is MAJOR. The tiebreaker is *when unsure, go up*:
under-versioning hides a change that costs someone an afternoon, over-versioning costs a digit.

A gate can check that a tag is well-formed and that its commit agrees with it. It cannot weigh what a
change costs whoever adopts it. Pretending otherwise would produce a rule that is mechanical and
wrong, which is worse than one that is honest and manual.

### Consequences

- **Releases have an order, and it is not the obvious one.** Set the constant, commit, *then* tag.
  Tagging first points the tag at a commit carrying the previous version; the gate then fails on the
  next commit, after the tag is published. `--release vX.Y.Z` sets the constant and prints the two
  remaining commands in order.
- **For a compliance template, most new gates are MAJOR.** A gate exists to block commits, so adding
  one can block content a project already has. MINOR is therefore narrower here than in a library —
  in practice a self-test, which cannot fail a project's content.
- **Between releases the stamp names the last release.** `gh repo create --template` takes `main`'s
  HEAD, and at pre-commit time `git describe` reports the *previous* commit, so no hook can stamp the
  commit being made. The gate prints a note when `main` is ahead of the last tag. Tag before creating
  a project if the distinction matters.

### Verification

Self-test: 8 in-memory fixtures. The gate itself was proved in a scratch clone by creating a badly
named tag and a tag pointing at a mis-stamped commit with no bump type in its annotation — three
violations reported with fixes, exit 1; exit 0 before they were added.

An incidental confirmation: the scratch clone sits outside `~/code/personal/`, so
`user.useConfigOnly true` refused to create the annotated tag until a local identity was set. Layer 4
of the identity separation working as designed, observed rather than assumed.

### Enforcement

`scripts/template_version.py` and `.pre-commit-config.yaml` (`template-version-selftest`, then
`template-version`). Taught by [[reference_template_versioning]].

---

## Decision 2026-09-20-007: Employer identifiers are refused by hash, not by name

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED
**Resolves:** the open question on 2026-09-19-001
**Amends:** 2026-09-20-002 (channel renamed; substance unchanged)

### Context

Decision `2026-09-19-001` split this template from employer brand and program content, and closed with
an open question: should a rule fail the commit when an employer identifier appears? It stayed
procedural for a day.

It became urgent for a concrete reason. The macOS runbook — about to enter version control — carries
an employer product name in prose. Creating that repository first and adding the rule later would put
the identifier in a permanent git object and then fail the repository against its own gate, with only
a history rewrite or a standing exception to resolve it. Sequencing the rule first avoids rework of
the expensive kind.

### Decision

**The identifiers are stored as hashes, not names.** An identifier this repository must never contain
cannot be written into this repository in order to be banned. Plaintext would put the very string in
`scripts/banned_feature_scan.py` and force the scanner to exempt itself — defeating the rule in the
act of stating it.

- SHA-256 of the normalized form: lowercased, stripped to alphanumerics, re-joined. One hash covers
  every spelling of a name — spaced, hyphenated, camel-cased or upper-cased.
- Matching sweeps 1- to 3-word n-grams per line and concatenates each, so a multi-word identifier is
  caught whatever punctuation separates it.
- The rule has an **empty `allow` set**. There is no file in this repository where such a name belongs.
- `--add-identifier "Name"` prints a hash to paste. The name is never written to any file.

**The channel is renamed** `PORTABILITY_RULES` -> `CONTENT_RULES`, amending `2026-09-20-002`. "No
employer identifier" is not a portability concern, and filing it under a name that says otherwise
misleads the next reader. The channel is defined by its *scope* — every file, `EXCLUDE_FILES` included
— not by a topic. A rule now carries either `patterns` (regex) or `hashes`.

### Honest limit

A hash is **non-disclosure, not secrecy**. It is unsalted, because a salt stored beside it protects
nothing. Anyone who already guesses a name can confirm it. The goal is that the control does not
*publish* the name, not that the name is unknowable.

### Consequences

- Adding an identifier is a two-step: run `--add-identifier`, paste the hash. Slightly more friction
  than a plaintext list, and the friction is the point.
- A hashed denylist is unreadable by design. The violation message shows the offending line, which
  contains the name — visible to the author who already has it, published nowhere.
- Only one identifier is seeded. The others are the operator's to add; the rule is live either way.

### Two defects found while building it

**The scanner caught me writing the identifier into the comment explaining why identifiers must never
be written.** The explanatory block used a real name as its example. The rule flagged it on the first
run. The examples are now fictional and the comment says why.

**The scanner blocked a commit over a gitignored file.** `.claude/settings.local.json` is covered by
the global gitignore and can never be committed, yet it failed the rule — a false positive naming a
file the author cannot fix by committing. `candidate_files()` now takes the file list from
`git ls-files --cached --others --exclude-standard`, i.e. what git would actually commit, falling back
to a filesystem walk outside a repository.

### Verification

Ten in-memory fixtures, including: every spelling collapses to one hash, a multi-word identifier is
found through punctuation, an unrelated line does not match, n-grams cover exactly up to the limit,
the provenance rule's `allow` set is empty, and content rules still bypass `EXCLUDE_FILES`. Live: a
hyphenated occurrence in a committable file exits 1; removing it exits 0.

### Enforcement

`scripts/banned_feature_scan.py` (`CONTENT_RULES`), `.pre-commit-config.yaml`
(`content-rules-selftest`, then `banned-feature-scan`). Taught by [[reference_content_provenance]].

---

## Decision 2026-09-20-008: gitleaks joins the suite

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

GitHub runs secret scanning and push protection free on **public** repositories only. A private
repository on a free personal account gets neither — the inverse of most people's intuition, and the
reason "I made it private" is not a control.

### Decision

Add `gitleaks` from its upstream repository, pinned at `v8.21.2`, with an explicit
`stages: [pre-commit]`.

**That `stages:` line is mandatory and is the whole reason this needed a decision.** Gitleaks'
upstream `.pre-commit-hooks.yaml` declares no `stages:` key — verified by fetching it — and a hook
without one runs at *every installed stage*. With both hook types installed it would scan twice per
commit. `2026-09-20-001` requires an explicit `stages:` on every hook; that rule applies to hooks
pulled from other repositories, not only to local ones.

### Consequences

- First run in a fresh clone downloads and builds the gitleaks environment, so it needs the network
  once — alongside `tomli` and `pyyaml`.
- This is a new gate that can fail content a project already has: a committed secret that previously
  went unnoticed now blocks the commit. MAJOR under [[reference_template_versioning]].

### Enforcement

`.pre-commit-config.yaml`, the `gitleaks` repo entry.

---

## Decision 2026-09-20-009: A project starts on the `gcc` or `commercial` profile

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

The GCC compliance regime is the law of one kind of engagement, not of every project. This template
imposed it on all of them, which is wrong for commercial or personal work — and the machinery around
it (the gates, the decision log, the knowledge base, the versioning) is worth keeping either way.

The tempting fix is a sentence in the constitution saying the section may not apply. **That sentence
is precisely the fossil §6.3 exists to prevent:** a governance document stating a rule nobody
enforces, which the next agent reads *instead of* the source.

### Decision

- `.project-profile` holds one word — `gcc` or `commercial`. `new_project.py --profile` **requires**
  the flag; there is no default, because a toggle that silently picks a side is not a toggle.
- **Documents are stripped, not annotated.** Profile-specific prose is fenced in HTML comments and
  the initializer removes the other side, marker lines included. Removed numbered sections have
  counterparts, so §4, §5 and §7 stay coherent.
- **The scanner reads the same file.** `GCC_BANNED_PATTERNS` applies only under `gcc`;
  `ALWAYS_BANNED_PATTERNS` applies everywhere. The enforced rule and the written rule cannot drift,
  because one value drives both.
- **No `.project-profile` means the template**, which keeps every block and enforces the **union** —
  fail-closed, and what lets the template carry law it does not impose on descendants.
- Marker balance is a gate. An unclosed marker swallows the rest of a file when stripped; a fixture
  demonstrates exactly that. Nesting and unknown profile names are refused too.

### Consequences

- **`--profile` is now required.** Any script or habit that called the initializer without it breaks,
  deliberately.
- Adding profile-specific law means adding a counterpart for every other profile, or the document
  loses a numbered section under one of them.
- A script that *explains* banned features necessarily names them. `project_profile.py` joins
  `EXCLUDE_FILES` for that reason; `CONTENT_RULES` still covers it, since `EXCLUDE_FILES` does not
  reach that channel.
- For consulting, one profile per engagement type is the natural extension, composing with the
  per-client identifiers in [[reference_content_provenance]].

### Verification

Two real projects were built from one template, one per profile. On `gcc`: §5 reads "GCC Portability
Requirements", the banned-features bullet is present, and `{"mode": "DirectLake"}` in a file exits 1.
On `commercial`: §5 reads "Portability Requirements", the commercial bullet replaces the banned one,
and the same file exits 0. Neither carries a leftover marker. Twelve in-memory fixtures cover
stripping, balance, nesting, unknown names, and the swallowed-tail failure.

### Enforcement

`scripts/project_profile.py`, `scripts/banned_feature_scan.py` (`active_banned_patterns()`),
`scripts/new_project.py` (`--profile`), `.pre-commit-config.yaml` (`project-profile-selftest`, then
`project-profile`). Taught by [[reference_project_profiles]].

---

## Decision 2026-09-21-001: Session closeout is a gate, and its artifacts live one session

**Amended 2026-09-24 (TMPL-5.2):** the wikilink rule the handoff linter applied to handoffs
alone now covers every text file git would commit: a `[[slug]]` that resolves to no knowledge
entry blocks the commit, with an allow set (`WIKILINK_ALLOW`) for the convention's own
placeholders and the slug the self-test fixtures use. Released MAJOR as `v9.0.0`, since a
project with a dangling link in any document now fails.

**Date:** 2026-09-21
**Made By:** Chair + AI
**Status:** APPROVED
**Resolves:** the handoff-versus-prompt conflation noted in a commit message in the archive repository's history (never logged)

### Context

The session end protocol (`CONSTITUTION.md` §2.2) is five prose steps. Nothing verifies that a
handoff was written, that sprint-status was updated, that learnings were flushed, or that the next
session has a prompt. The last session decided the kickoff prompt "is not a repo artifact at all and
is handed over as text". That put the next session's instructions in chat only, which is the failure
this repository exists to prevent. The same session left an open question in a commit message body
instead of this log. Both are the convention-instead-of-control shape already recorded twelve times.

Handoffs also accreted: the standard's own template carried durable rules and constraints, so a
handoff became a second knowledge base that nothing indexed and no gate watched.

### Decision

1. **Closeout is mechanical.** `scripts/session_closeout.py` verifies the closeout artifact set. Its
   `--check` mode runs on every commit; `--closeout` runs at session end and performs the rotation
   below; `--verify` runs at the next cold start and refuses build work if the previous session did
   not close out.
2. **Sessions are numbered.** `S1`, `S2`, … The pair `HANDOFF_S{N}.md` + `KICKOFF_S{N}.md` in
   `sprint/handoffs/` is written at the closeout of session N−1 and consumed by session N. The
   sprint-status entry for session N is headed `## S{N} — <date> — <title>`.
3. **Handoffs and kickoffs live one session.** Nothing may exist only in a handoff or kickoff that is
   needed beyond the session that consumes it. Durable facts go to the knowledge base, decisions to
   this log, work to the tracker; the handoff links to them. The templates have no section a durable
   rule could live in, and the linter rejects unknown headings.
4. **Rotation keeps two pairs.** At closeout the script moves every pair older than the consumed one
   into `sprint/handoffs/archive/`. The main folder holds at most two session numbers, consecutive:
   the pair this session consumed and the pair it produced. Archived files are never a mandatory
   read, so anything left only in one is lost by design.
5. **The kickoff prompt is a repo artifact and is standalone.** It names a persona, the cold start,
   a task list where every task cites a story ID present in the tracker, success criteria, and the
   closeout command. It is pasted verbatim into the next chat.
6. **Personas are shape-gated, not list-gated.** `docs/personas/<slug>.md` holds one persona each,
   with required frontmatter and sections. A kickoff names a persona by slug and copies its
   invocation block verbatim; the gate proves the slug exists and the copy matches. A persona is
   written when a task first needs it and registered in the same commit. No list is predicted.
7. **Pre-gate handoffs are archived as-is.** The handoff dated 2026-09-20 and the two `SAMPLE_`
   files predate the structure and are not linted; the samples are deleted because a linted template
   supersedes an unlinted example.
8. **The recovery handoff template is retired.** `sprint/recovery/templates/HANDOFF_TEMPLATE.md`
   competed with the standard for the same concern, which the authority matrix forbids. Recovery
   sessions use the standard handoff plus the validation-evidence template.

### Honest limit

The gate cannot read prose. It proves counts, sequence, structure, that every task cites a real
story, that every persona reference resolves, and that decision IDs and wikilinks resolve. It cannot
prove a sentence in a handoff was not durable. The rotation is what enforces that: a fact left only
in a handoff disappears from mandatory reads one session later.

### Consequences

- Adding this gate is MAJOR under [[reference_template_versioning]]: it fails a project whose
  handoff folder is unstructured. Released as `v4.0.0`.
- `session_handoff_standard` is rewritten as v2.0. The percentage ladder, the "Handoff Prompt
  Template" conflation, and the `HANDOFF_SESSION[N]` naming are removed.
- The initializer clears `sprint/handoffs/` including the archive. A new project starts at S1 with
  no incoming pair, which the gate accepts as a fresh project.

### Enforcement

`scripts/session_closeout.py` and `.pre-commit-config.yaml` (`session-closeout-selftest`,
`session-closeout-check`, and the manual-stage `session-closeout` / `session-verify`). Taught by
[[reference_session_closeout]].

---

## Decision 2026-09-22-001: CI is the backstop for per-clone hooks

**Amended 2026-09-25 (TMPL-1.5, under 2026-09-25-001):** the repository is public. Protection is
now available at no cost and is still not enabled: every checkpoint is a direct push to `main`,
and a required check would force a pull-request flow on one developer for a run that already
reports. The design below stands with its reason changed; the 2026-09-22 resolution of the open
question is superseded.
**Amended 2026-09-22:** the repository stays private and branch protection is not pursued.
The workflow is a reporting backstop; the local hooks are the blocking control. The open question
below is resolved accordingly, and the operator command was removed from the knowledge entry.
**Amended 2026-09-23 (TMPL-5.1):** "a new stage added later needs a matching step in the
same work unit" is now a control: `gate_runbook_scan.py` fails any non-manual stage the config
declares that no workflow step runs, and a missing or unreadable workflow. Released MAJOR as
`v8.0.0`, since a project that added a stage without a step now fails.

**Date:** 2026-09-22
**Made By:** Chair + AI
**Status:** APPROVED

### Context

Every gate in this repository is a git hook, and git hooks are per-clone. A clone that never ran
`pre-commit install --hook-type pre-commit --hook-type commit-msg` commits with no gate at all, and
no file in the repository can detect that (decision 2026-09-20-001 recorded the problem for the
commit-msg stage; it applies to every stage). The suite was therefore only as strong as the last
operator's memory of the install command.

### Decision

- `.github/workflows/gates.yml` runs the full pre-commit-stage suite on every push and pull request,
  and runs the commit-msg gate over every commit the event carries. Same scripts, same config; the
  clone's hook state does not matter.
- Branch protection is not part of the design. It needs GitHub Pro or a public repository; this one
  stays private, and with one developer the blocking value is low. A red run is a report acted on in
  the same session.
- The check is proved in both directions before it is trusted: a commit from a clone with no hooks,
  carrying a violation, turned the run red; the same tree without it turned green.

### Consequences

- A push that fails locally-uninstalled gates now fails on GitHub instead of landing. The first such
  failure in a derived project is expected, not alarming: it is the backstop doing its job.
- **The workflow reports; it does not refuse.** GitHub returned 403 on branch protection: it
  requires GitHub Pro or a public repository, the same plan limit decision 2026-09-20-008 recorded
  for secret scanning. The local hooks remain the only blocking control, and the workflow is the
  visible audit of what they would have caught.
- No branch-and-pull-request convention is imposed. Without enforcement it would be exactly the
  written-rule-as-control shape this repository keeps removing.
- GitHub Actions minutes on a private repository are metered against the free monthly allowance;
  a run of this suite takes about two minutes.

### Open question

- ~~Should this repository be made public so branch protection can be enabled?~~ **RESOLVED
  2026-09-22:** no. The operator is not comfortable publishing the history, and with one
  developer branch protection is not urgent. If that changes, GitHub Pro enables protection on
  private repositories without publishing anything.
- The template-version gate needs the full history, so checkout runs with `fetch-depth: 0`.
- `pre-commit run --all-files` in CI does not cover the commit-msg stage; the workflow's second step
  exists for that reason, and a new stage added later needs a matching step in the same work unit.
- MINOR under [[reference_template_versioning]]: adopting it forces no one to act, and it cannot
  fail content the local suite already passes.

### Enforcement

`.github/workflows/gates.yml`. Taught by [[reference_ci_backstop]].

---

## Decision 2026-09-22-002: What the first derived project found, and the three fixes

**Date:** 2026-09-22
**Made By:** Chair + AI
**Status:** APPROVED

### Context

TMPL-2.3 created a real private repository from the template on GitHub (the derived probe),
initialized it on the `commercial` profile, installed both hook types, pushed, and ran its S1 to
closeout. Three defects surfaced, none of them visible from inside the template because each needs
either a tag push or a second repository to appear.

1. **The template's release run went red.** Pushing `v4.1.0` with `--follow-tags` produced two
   `gates` runs; the tag-triggered one failed the version gate with "annotation does not name
   MAJOR, MINOR or PATCH: 'release: v4.1.0'". The checkout log shows why: `actions/checkout`
   re-fetches the pushed ref as `+<sha>:refs/tags/v4.1.0` with `--no-tags`, which replaces the
   annotated tag with a lightweight one. `%(contents:subject)` on a lightweight tag is the commit
   subject. The gate then told the reader to re-annotate a tag that was annotated all along.
2. **The derived tracker was the template's tracker.** The initializer filled one token in
   `sprint/story-tracker.md` and left the `TMPL-1` and `TMPL-2` epics in place, so the new project
   started with ten stories, eight done, none its own, and Summary Statistics that described the
   template's backlog. Sprint-status was already regenerated for the same reason; the tracker was not.
3. **The clone's remote used the wrong ssh host.** `gh repo create --clone` writes
   `git@github.com:…`; on a machine that separates identities by ssh host alias there is no
   `Host github.com` block, so the first push would have used no personal key. Environment-shaped,
   but the guide names the command, so the entry that teaches it names the follow-up.

### Decision

- **The workflow restores the real tag objects** with `git fetch --force --tags origin` after
  checkout. The tag-push event is the one that exists to verify a tag, so it must see the tag as
  pushed. The trigger is left as `on: push` for every ref; a release costs one duplicate run.
- **The version gate distinguishes a lightweight tag** (`%(objecttype)` is `commit`, not `tag`)
  and reports it as `lightweight-tag` with a fix that names both causes, instead of printing the
  commit subject as a missing bump type. The rule applies exactly where a bump must be named: every
  tag but the earliest, which has no predecessor and so needs no annotation. The per-tag rules are
  a pure function, `judge()`, with seven fixtures; the lightweight fixture was run against the
  previous code in a scratch clone, which reported `no-bump-type` with the commit subject, as
  GitHub did.
- **The initializer regenerates the tracker** from a skeleton with the `[EXAMPLE]` epic and zero
  statistics, exactly as it regenerates sprint-status. The fixture judges the skeleton with the
  state gate's own `tracker_counts()` and `tracker_violations()`: no real story ID, and counts that
  reconcile. A skeleton that still carried the `TMPL` epics fails it.
- **The release is a PATCH (`v4.1.1`).** Adopting it forces no one to act: a derived project with
  its own tags either has none (the gate skips) or had already to pass the bump-type rule on every
  tag but the earliest, and a lightweight tag could pass that rule only if its commit subject
  happened to contain MAJOR, MINOR or PATCH.

### What worked without change, observed

The GitHub-side "Initial commit" triggers a `gates` run before the initializer has run; it was
green, since the template tree passes its own suite. The initializer's dry run and apply matched.
`session-verify` passed at S1 with no incoming pair. The attribution gate refused a
`Co-Authored-By` trailer in the derived clone before the first real commit. The first push's
`gates` run was green. Profile stripping left no marker in any of the four documents.

### Enforcement

`.github/workflows/gates.yml` (the fetch step), `scripts/template_version.py` (`judge`,
`lightweight-tag`, `--self-test`), `scripts/new_project.py` (`story_tracker_skeleton`,
`--self-test`). Taught by [[reference_ci_annotated_tags]] and [[reference_derived_project_start]].

---

## Decision 2026-09-22-003: The closeout command runs with `--all-files`

**Date:** 2026-09-22; amended 2026-10-22
**Made By:** Chair + AI
**Status:** APPROVED

### Amendment 2026-10-22: the verify carries the flag too

The bullet below that left `session-verify` unchanged reasoned that a gate requiring a clean tree
leaves nothing to stash. That is circular: the stash runs before the gate, and an unstaged edit to
a tracked file is exactly what it hides. Measured in S2 on a clone at the S1 closeout commit: clean,
`pre-commit run session-verify --hook-stage manual` passed; with one unstaged edit to `README.md`
the same command printed "Stashing unstaged files" and **passed**; with `--all-files` it failed on
`dirty-tree`. Unlike the closeout case this is a hidden green, not a confusing red: the cold start's
proof that the previous session committed its work passed while work sat uncommitted. A staged edit
was caught either way, since `git status` still lists it under the stash.

`VERIFY_COMMAND` in `scripts/session_closeout.py` is now
`pre-commit run session-verify --hook-stage manual --all-files`; the kickoff scaffold writes it,
and `AGENTS.md`, the handoff standard §5, the gate runbook and the hook comment name this form. The
`SessionStart` hook built in TMPL-1.2 runs it the same way. A kickoff written before the amendment
is not refused; the linter checks section 2 for `AGENTS.md` and the handoff, as before.

### Context

The derived project's S1 closeout ran the documented command, `pre-commit run session-closeout
--hook-stage manual`, with the tracker and sprint-status edited but not yet staged. pre-commit
printed "Unstaged files detected. Stashing unstaged files", ran the hook, and the gate reported
that the kickoff's two stories were not in the tracker. They were in the tracker on disk; the gate
had read the last commit's tracker, because pre-commit stashes unstaged changes to tracked files
before running any hook invoked without `--all-files` or `--files`. The new pair, being untracked,
was not stashed, which is why the gate saw the kickoff and not the stories it cited.

Measured both ways on the same tree with one unstaged edit: without the flag pre-commit stashes;
with `--all-files` it does not. The hook declares `pass_filenames: false` and `always_run: true`,
so the flag changes nothing about what the gate checks, only whether the tree it checks is the
one on disk.

The gate cannot detect that it ran under a stash: the working tree is simply the index, and the
patch files pre-commit writes to its cache persist after restore, so their presence proves nothing.

### Decision

- `CLOSEOUT_COMMAND` is `pre-commit run session-closeout --hook-stage manual --all-files`. The
  scaffold writes it into every kickoff's section 5, and every document that names the command
  names this form. The linter keeps checking for `session-closeout` only, so kickoffs written
  before this decision still pass.
- The scaffold's closeout paragraph also names the push, the `gates` run to confirm, and the
  hand-over of the next kickoff, matching `session_handoff_standard_v2.0.md` §7 steps 6 and 7,
  which the previous text stopped short of.
- `session-verify` is unchanged: it requires a clean tree, so there is nothing to stash.
  (Wrong; see the amendment above.)
- The initializer's S1 sprint-status entry says that its "Next" list stands in for the kickoff S1
  does not have, and that S1 must open an epic before the S2 kickoff can cite a story.

### Honest limit

The failure mode is a spurious failure, not a spurious pass: the stashed files are exactly the ones
that carry the session number and the story IDs, so a stale read produces a violation, and the
per-commit `--check` judges the staged tree regardless. The flag removes a confusing red, not a
hidden green. It is still worth a decision because the confusion sends the reader to fix a tracker
that is already correct.

### Enforcement

`scripts/session_closeout.py` (`CLOSEOUT_COMMAND`, the kickoff scaffold), `.pre-commit-config.yaml`
(the hook comment), `CONSTITUTION.md` §2.2, `README.md`, `TEMPLATE_GUIDE.md`,
`docs/standards/session_handoff_standard_v2.0.md` §5 and §7. Taught by [[reference_precommit_stash]].

---

## Decision 2026-09-22-004: A derived project takes a newer release through an updater

**Date:** 2026-09-22; amended 2026-09-24 (TMPL-4.1: the decision log is kept, the framework decisions file is what is merged by ID)
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`gh repo create --template` squashes history, so a derived project shares no commit with the
template: `git merge` has no base, and `git pull` has nothing to pull. The first derived project
(decision 2026-09-22-002) was told in its second kickoff which files to copy, one by
one, and which decision to append so the freshness gate would accept the new knowledge entries.
That is a checklist, and this repository converts checklists into controls.

Two harder questions sat underneath. What does the template own in a project after birth, given
that the initializer fills some files, regenerates others, strips a profile from the documents
and never touches the decision log or knowledge base? And how does a framework decision reach a
project's decision log, which is the project's append-only record, without rewriting it?

### Decision

- **`scripts/template_update.py` carries a project from its `.template-version` to a named
  release.** It fetches both releases from `--source` into `refs/template/<version>`, outside
  `refs/tags/` so the version gate never sees them, and judges every path in either tree.
- **Ownership is decided by path and is the initializer's inverse.** `keep`: `sprint/` except
  the decision log, `.project-profile`, and the content folders shipped empty; never written.
  `merge`: the knowledge INDEX by slug and the decision log by decision ID; project rows are
  never touched. `three-way`: everything else, through `git merge-file` over the previous
  release, the project's copy and the target. A fixture reads `new_project.py`'s
  `REGENERATE_FILES`, `CLEAR_GLOBS`, `FILL_FILES` and `NEVER_RESET` and checks the map against
  them.
- **One mechanism for files, not two.** Overwriting "template-owned" paths was rejected because
  they are legitimately edited (`TEMPLATE_GUIDE.md` Step 5 adds patterns to the scanner; the
  standards carry tokens the project fills). For an unedited copy the merge reduces to overwrite.
- **The decision log is inserted into, never rewritten.** A framework decision the log lacks
  gets its index row at the top of the table and its body appended at the end, because the
  framework's entries `teaches:` it. An existing row or body changes only when it still equals
  the previous release's; an edited one is reported and left. Nothing is removed. `[EXAMPLE]`
  rows and bodies never travel. This is the answer to the question an earlier kickoff reserved for
  the operator: the design does not rewrite a derived log, it appends to it, and the dry run
  shows every insertion before `--apply`.
- **Template markdown is stripped to the project's profile before comparison and before
  writing**, as at birth. Without it every document with a profile block reads as edited.
- **The target release's copy of the script runs.** The map lives in the file, so the run
  compares the executing file with the target's blob and refuses with the two commands that
  fetch it. A target that predates the updater is accepted with a note.
- **The stamp is written last and withheld on a conflict.** A conflict leaves the file alone and
  names the diff; `--keep <path>` or `--take <path>` settles it on the re-run. `--apply` refuses
  a dirty tree (the updater itself excepted, since first adoption fetches it untracked) so the
  review afterwards is one `git diff`, and then runs the full suite.
- **MINOR (`v4.2.0`)** under [[reference_template_versioning]]: an opt-in script and a self-test
  hook, which cannot fail a project's content.

**Amended 2026-09-24 (TMPL-4.1, under 2026-09-23-003):** the framework decisions live in
`docs/governance/framework_decisions.md`, and that file is the one merged by decision ID, rows and
bodies, with the rules above unchanged. `sprint/decision-log.md` is kept with the rest of
`sprint/`: the updater never writes it again, so the project's append-only record is the project's
alone. A project that took a release before `v11.0.0` keeps the framework rows the old insertion
put in its log; the freshness gate reads both indexes as one set and lets the framework file win
the duplicate IDs ([[reference_framework_decisions]]).

### Verification

Thirty in-memory fixtures. Six deliberately broken variants were run against them in a scratch
harness before the suite was trusted: inserts at the table's end, no profile stripping,
both-sides-changed silently taking the template, `[EXAMPLE]` rows treated as decisions,
conflicts reported clean, and bodies read to end of file. Each failed between one and six
fixtures. On the derived probe, from the archive repository's `v4.1.0` to its `v4.1.2`: the dry run planned 14 updates, 3
additions and 3 merges; `CONSTITUTION.md` merged cleanly across the project's token fill and
profile strip; the two decisions arrived with bodies; `--apply` ran the suite green; the push's
`gates` run was observed.

### Enforcement

`scripts/template_update.py` (`classify`, `verdict`, `merge_rows`, `merge_decisions`,
`--self-test`), `.pre-commit-config.yaml` (`template-update-selftest`), `TEMPLATE_GUIDE.md`
Step 9. Taught by [[reference_template_update]].

---

## Decision 2026-09-23-001: The gate suite is described by a runbook the config verifies

**Date:** 2026-09-23
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`TEMPLATE_GUIDE.md` Step 6 carried a hand-written table of the gates. It was keyed by script
rather than by hook id, named no stage, and by the time it was replaced it already lacked the
updater's self-test added one session earlier. Nothing compared it to `.pre-commit-config.yaml`.
A page that describes the suite is what the next reader consults instead of the config, so a
stale one is the fossil `CONSTITUTION.md` §6.3 exists to catch, in the one place that claims to
be the map. The operator asked for a runbook: one section per hook, in run order, its stage, the
self-test it pairs with, what it blocks, why, and how to run it alone.

Two questions sat underneath. Where does the page live so the updater carries it to derived
projects, given that `classify()` keeps `docs/runbooks/` and three-way merges `docs/governance/`?
And what bump does a check that reads a project's config and page deserve?

### Decision

- **The page is `docs/governance/gate_suite_runbook.md`.** `docs/runbooks/` is project-owned by
  the updater's map: it holds the project's operational procedures and the template never writes
  there, so a page that must track the template's own hook config cannot live in it. Governance is
  where the compliance policy's enforcement belongs, beside the document-control standard. The
  three-way merge is the right mechanism, not a limitation: a project that adds a hook to its
  config must add a section, and the merge lets both sides edit the page.
- **Every H2 on the page is a hook id**, spelled as `id:` spells it, in the config's order. Prose
  that is not about one hook sits above the first H2. Each section carries a `**Stage:**` line.
  What a section says a gate blocks, and why, links the decision and the knowledge entry and does
  not restate them.
- **`scripts/gate_runbook_scan.py` is the control.** It reads the hook ids from the config with a
  YAML parser, every repo included, and the sections from the page outside fenced code. It fails
  on a hook with no section, a section naming no hook, sections out of run order, a stage line
  missing or disagreeing with the hook's `stages:`, and a config that cannot be parsed or holds no
  hooks, which is never read as an empty suite. Wired as `gate-runbook-selftest` then
  `gate-runbook`, `stages: [pre-commit]`, with `additional_dependencies: [pyyaml]`; exit 2, never
  0, without the parser.
- **A hook without `stages:` is a violation.** Decision 2026-09-20-001 required an explicit
  `stages:` on every hook and enforced it by prose. The stage line on the page can only be checked
  against a declared stage, so the check refuses a hook that declares none. The written rule is
  now a control.
- **MAJOR, released as `v5.0.0`.** Under [[reference_template_versioning]] the question is whether
  adopting it forces a human to act. It does, in content a project can already have: a hook the
  project added to its config (the config is three-way merged, and adding a hook is a supported
  edit) has no section until someone writes one, and a project hook declared without `stages:`
  fails outright. For a project that never edited the config the updater carries the page and the
  config together and the gate passes, which is the common case; but the bump is judged by the
  case it can fail, and the tiebreaker goes up. `TMPL-2.7` takes the probe to `v5.0.0` to observe
  which case it is.

### Honest limit

The check cannot read prose. It proves the page's shape follows the config: nothing listed that
does not exist, nothing that exists left out, the run order, and the stage a reader will pass to
`--hook-stage`. Whether a section's account of what a gate blocks is still true is the author's to
keep, and the linked decision is the source when they disagree.

### Verification

Fifteen in-memory fixtures. Six deliberately broken variants were run against them in a scratch
harness before the suite was trusted: H2s inside fenced code counted as sections, the order rule
removed, stage disagreements ignored, only the first repo's hooks read, an unreadable config read
as zero hooks, and a hook without `stages:` accepted. Each failed between one and ten fixtures.
Live, by exit code: a scratch config with an extra hook id exited 1 on `no-section`; a scratch
page with an extra section exited 1 on `no-hook`; a page with the two manual-stage hooks
relabelled `pre-commit` exited 1 on `stage` twice; a config with the attribution hook's `stages:`
removed exited 1 on `no-stages`. The real tree: 22 hooks, 0 violations.

### Enforcement

`scripts/gate_runbook_scan.py` and `.pre-commit-config.yaml` (`gate-runbook-selftest`, then
`gate-runbook`). `TEMPLATE_GUIDE.md` Step 6 links to the page and holds no table. Taught by
[[reference_gate_runbook]].

---

## Decision 2026-09-23-002: `dev-resources` is the durable home for personas and reference knowledge

**Date:** 2026-09-23
**Made By:** Chair + AI
**Status:** APPROVED; SUPERSEDED (personas and shared knowledge in dev-resources) by 2026-10-23-003

### Context

The persona registry lives in `docs/personas/` of every project. The initializer preserves it at
birth and the updater three-way merges it, so a template release reaches every project; nothing
travels the other way. A persona written in a project stays there, and the template never sees
it, so each clone is only as good as the registry it started with. The same holds for reference
knowledge that is not specific to one project. The operator's aspiration: one repository whose
registry and reference documents grow from every project and reach every project.

`dev-handbook` already existed for that purpose in miniature: a README, one runbook, and a copy
of the attribution gate that its README names as a known duplication. It was renamed
`dev-resources` on GitHub and locally on 2026-09-23, keeping its history and the redirect.

### Decision

- **The project holds a synced snapshot, never a pointer.** The session gate proves a kickoff's
  persona block equals the registry file, and CI reads local files, so the registry must be in
  the tree. `dev-resources` is the source; the project's copy is a cache refreshed mechanically,
  which is the repository's own single-source-of-truth law one level up.
- **Sync is a script in the updater's idiom, not a submodule or subtree.** `scripts/resources_sync.py`
  fetches `dev-resources` into `refs/resources/<ref>`, compares blobs, writes, reports, and stamps
  `.resources-version`. Submodules are not initialized by `gh repo create --template` and need a
  checkout flag in CI; a subtree is a second merge channel over the same paths as the updater.
- **Ownership is disjoint.** `dev-resources` owns `docs/personas/` and knowledge entries that
  declare `source: dev-resources` in their frontmatter; the updater's map marks those paths
  `keep`, so only the sync writes them. The template keeps everything version-locked to its own
  config, the gate-suite runbook above all, since `gate-runbook` proves that page against the
  config the project actually has. Resource knowledge entries carry `teaches: []`.
- **Sync runs at closeout, never at cold start.** The produced kickoff is scaffolded from the
  registry as just synced; the consumed kickoff matches the registry as it was at its scaffold.
  A mid-session sync is the only way the two can disagree, and the gate then fails loudly.
- **Personas are append-only.** A persona is added when a task first needs one, as now. An
  Invocation never changes in place: an enhancement bumps `version:` in the frontmatter and
  appends a changelog line, and the persona linter refuses an Invocation change without the bump.
  The kickoff names the version it was written against.
- **Contribution is gated.** At closeout, a persona in the local registry that the fetched
  `dev-resources` ref lacks is a violation; the sync's `--publish` writes it into the local clone
  of `dev-resources` for commit and push. The registry grows only through that path.
- **The template publishes `.pre-commit-hooks.yaml`** so `dev-resources` consumes the persona
  linter, the frontmatter gate, the attribution gate and gitleaks as a hook repository pinned by
  `rev`, replacing the copied script. A registry with no linter is not a registry.

### Consequences

- Epic TMPL-3, four stories, in this order: the published hooks, the append-only rule, the sync
  script with the ownership split and the closeout check, then the move and the proof on the probe.
- Adopting the sync is MAJOR under [[reference_template_versioning]]: the closeout gains a check a
  project must satisfy, and the persona linter gains a required key.
- `dev-resources` becomes a gated repository. Its README's own rule, "prose, not code", still
  holds for its content; the gates it runs are the template's, consumed, not copied.

### Enforcement

To be built: `scripts/resources_sync.py`, the version rule in `session_closeout.lint_persona`,
`.pre-commit-hooks.yaml`, and the `keep` prefixes in `template_update.classify`.

---

## Decision 2026-09-23-003: A pristine `v1.0.0` from a fresh init, with the build history archived

**Date:** 2026-09-23; amended 2026-09-24 (the decisions move built, its enforcement and bump named; the sanitizer built and the sweep done; the archive repository named; the cut done)
**Made By:** Chair + AI
**Status:** APPROVED

### Context

The template carries six sessions of its own construction: sprint-status entries, the `TMPL`
epics, handoff pairs and their archive, and decision bodies that read as a build diary. A
project created from it inherits none of the sprint state, because the initializer regenerates
or clears it, but the template itself is not the pristine artifact the operator wants to clone
from. The operator asked for a sanitized `1.0.0` and for the completed, unsanitized repository
to be kept for reference.

One dependency makes a naive reset break the first commit: every knowledge entry declares
`teaches: [<decision-id>]` and the freshness gate refuses an ID absent from
`sprint/decision-log.md`. The initializer records this as the reason it never clears the log.

### Decision

- **Framework decisions move to `docs/governance/framework_decisions.md`**, same index-and-bodies
  structure, IDs unchanged. The freshness gate and the session gate read both logs. The updater
  merges the framework file by ID instead of inserting into a project's append-only log, which
  removes the least comfortable part of 2026-09-22-004. `sprint/decision-log.md` starts with the
  `[EXAMPLE]` row only. Docstrings that cite decision IDs stay correct.
- **The sanitizer is the initializer's machinery without the fill.** `scripts/sanitize_template.py`
  regenerates sprint-status with the template's own S1 entry, regenerates the tracker, clears the
  handoffs and the sprint archive, keeps every token and both profile blocks, writes no
  `.project-profile`, and runs the suite. Its `--check` fails while build state remains: an
  `S<N>` above 1, a `TMPL-` story, the sprint archive, the probe's name.
- **The sweep is by hand.** Knowledge entries and decision bodies keep their learnings and lose
  incidental session numbers, probe references and commit hashes; where history matters, the
  citation names the archive repository.
- **Ten tags cannot be retagged `v1.0.0`**, because the version gate verifies every tag. So: this
  repository is renamed to an archive name, given a final tag, and archived read-only on GitHub.
  The sanitized tree starts from a fresh `git init` as `agentic-dev-template`, as 2026-09-19-001
  did for the employer split, with `TEMPLATE_VERSION` set to `v1.0.0`, committed, then tagged.
  The version gate exempts the earliest tag from the bump rule. Keeping the name keeps the
  initializer's self-refusal and the guide's URLs correct.
- **Proof before the cut.** The sanitized tree is produced on a scratch clone first; a derived
  project is created from it, initialized, and its S1 verified, before anything is archived.
- **Order.** After epic TMPL-3, because the resources that move out must move before the
  sanitize, and the framework-decisions move is what the sync's `teaches: []` rule relies on.

**Amended 2026-09-24 (TMPL-4.2):** the archive repository is `SaltyBrett/agentic-dev-template-archive`, the name a
citation uses where the build history matters; TMPL-4.4 renames this repository to it. The
sweep left the session numbers that are the numbering convention itself (a fresh project at S1,
the S2 kickoff) and every `TMPL-` story ID a decision cites, since the check reads the tracker's
rows alone. `.resources-version` stays through the reset: it is the template's sync state, read by
the closeout's persona rule, not session state. MINOR for the sanitizer: an opt-in script and a
self-test that reads nothing from a project's tree.

**Amended 2026-09-24 (TMPL-4.4):** the cut is done. The sanitize check named nothing outside the
files the reset clears, so no further sweep preceded it. This repository was renamed to
`SaltyBrett/agentic-dev-template-archive` on GitHub, the sanitizer ran in the local clone while
its origin still named the template, the tracked files of the reset were copied to a fresh
directory, and `SaltyBrett/agentic-dev-template` was created empty and received `release: v1.0.0`
as its first commit, tagged `v1.0.0` with an annotation naming MAJOR and the archive; both of its
`gates` runs were read green before this amendment was written. The order that matters, and the
one hazard met, are taught by [[reference_pristine_cut]]: the old clone's origin is switched to
the archive name before the new repository takes the old one, because GitHub's redirect from the
old name lasts only until it is reused. The record of the cut, this amendment and that entry, is
carried into the new lineage as a commit after its tag, so `v1.0.0` is the sanitized tree alone.
The archive's final tag is a PATCH whose annotation names `v1.0.0` and the new repository; the
derived probe repository is left to the operator, retired or restamped, as the consequences say.

### Consequences

- Epic TMPL-4, four stories: the decisions move, the sanitizer and sweep, the scratch proof,
  the archive and the fresh init.
- The derived probe repository belongs to the archived lineage; its `.template-version` names
  tags the new repository does not have. It is retired with the archive or restamped by hand.
- The new lineage's first MAJOR is `v1.0.0`; the archive's last tag records where it came from.

### Bump

The decisions move (TMPL-4.1) is MAJOR, released as `v11.0.0`: a project adopting it receives a
new file the gates read, and its own log stops receiving framework decisions. The sanitizer and
the fresh init (TMPL-4.2 to TMPL-4.4) are the new lineage's `v1.0.0`.

### Enforcement

Built (TMPL-4.1): `kb_freshness_scan.parse_logs` and `log_texts` read
`sprint/decision-log.md` and `docs/governance/framework_decisions.md` as one set, an index missing
from either raising with the log's name, the framework file winning a duplicate ID;
`session_closeout.decision_ids` reads the same set; `template_update.MERGE` names the framework
file and the project's log falls under `sprint/`, kept; `new_project.NEVER_RESET` names the
framework file and the initializer's fixture keeps it out of every mutating list; the template's
own `sprint/decision-log.md` holds the `[EXAMPLE]` entry alone. Taught by
[[reference_framework_decisions]] and [[reference_template_update]]. Built (TMPL-4.2):
`scripts/sanitize_template.py`, whose `--check` names every sprint-status entry above S1, every
`TMPL-` story row, every file in `sprint/archive/` and `sprint/handoffs/archive/`, every pair in
`sprint/handoffs/` and the probe repository's name in any text file git would commit, the script
itself excepted; whose `--apply` is the initializer's regenerate-and-clear with no fill, no profile
strip and no `.project-profile`, followed by the suite; which refuses to run where `origin` is not
the template. `sanitize-template-selftest` runs on every commit, `sanitize-template-check` at the
manual stage, because this repository fails it until the cut. Taught by
[[reference_template_sanitizer]]. Done (TMPL-4.3, TMPL-4.4): the scratch proof, then the cut,
whose order and hazard are taught by [[reference_pristine_cut]].

---

## Decision 2026-09-23-004: Commit classification is not built; the bump stays a judgement

**Date:** 2026-09-23
**Made By:** AI, under the kickoff's instruction to decide TMPL-2.2 rather than defer it
**Status:** APPROVED
**Closes:** TMPL-2.2, opened under 2026-09-20-006 and carried through four sessions

### Context

Decision 2026-09-20-006 gated the release mechanics and left the bump type a documented judgement.
TMPL-2.2 proposed removing the judgement: type every commit at `commit-msg` time and have
`--release` compute the bump as the highest type in the window since the last tag.
[[reference_commit_classification]] recorded the constraints before the work was attempted:
the hook fires on merge commits, an all-exempt window must fail rather than default to PATCH,
`checkpoint:` is most of the history and cannot simply be exempt, and the policy itself is not
up for revision. Every session since then recorded the same observation in its sprint-status
entry: the commits since the last tag were few and were classified from the log without effort.

Measured on 2026-09-23, the commits between consecutive tags of the archive repository:

| Window | Commits |
|---|---|
| `v1.0.0`..`v1.1.0`, `v1.1.0`..`v2.0.0`, `v2.0.0`..`v3.0.0` | 1 each |
| `v3.0.0`..`v4.0.0` | 10 |
| `v4.0.0`..`v4.1.0` | 5 |
| `v4.1.0`..`v4.1.1`, `v4.1.1`..`v4.1.2` | 2 each |
| `v4.1.2`..`v4.2.0` | 4 |
| `v4.2.0`..`v5.0.0` | 3 |

And every change that moved the version was introduced by a decision whose body names the bump
and its reason (`2026-09-22-002` PATCH, `2026-09-22-004` MINOR, `2026-09-23-001` MAJOR, and so
on back to `2026-09-20-008`). The judgement is already made when the change is fresh. It is
recorded in the decision log, which the freshness gate keys every teaching document to, not in
the commit message, which nothing reads back.

### Decision

**Won't do.** TMPL-2.2 closes. The release bump remains the judgement of 2026-09-20-006, made at
release time from the decisions logged since the last tag, and named in the tag annotation the
version gate verifies.

### The recommendation and its cost, as the kickoff asked

The mechanism would cost the operator a type on every commit in every repository that carries
the `commit-msg` hook, which after TMPL-3.1 includes `dev-resources` and every derived project,
because the hook is one script and the config is three-way merged. It would also need a decided
and verified treatment for merge, revert, squash and amend, and a rule mapping `checkpoint:` to
a type. What it would buy is the automation of a decision that takes one reading of a window
that has held between one and ten commits, over ten releases, and whose answer is already
written in the decision that introduced the change. The gate that matters, that the tag names a
bump and its commit carries the version, already exists. Automating the remaining judgement
would cost more than the judgement.

### What would reopen this

A release window that grows past what one reading covers, or a second maintainer whose
classification disagrees with the first. Either is visible in the sprint-status entry that
precedes a release, which is where every session so far has recorded the count. The constraints
in [[reference_commit_classification]] stand for that day.

### Enforcement

None is added. `scripts/template_version.py` continues to verify the tag, the version constant
and the annotation's bump word. Taught by [[reference_commit_classification]] and
[[reference_template_versioning]].

---

## Decision 2026-09-23-005: The template is a pre-commit hook repository

**Amended 2026-09-23 (same session):** the consequence on consumer access first claimed
that the keychain credential served the https URL locally. It did not; the check that said so
read the exit code of a pipe. What holds is below: ssh from the directory pre-commit clones into.
**Amended 2026-09-23 (with the operator):** the open question is resolved; the
template stays private and `dev-resources` runs its gates as local hooks only.
**Amended 2026-09-25 (under 2026-09-25-001):** the template is public; `dev-resources` pins the
plain https URL and has a `gates` workflow. The ssh-alias reasoning below stays as the record of
what a private hook repository costs a consumer; the open question's resolution is superseded.

**Date:** 2026-09-23; amended 2026-09-23; amended 2026-09-25
**Made By:** Chair + AI (the design in 2026-09-23-002; the mechanics decided here)
**Status:** APPROVED
**Builds:** the last bullet of 2026-09-23-002 (TMPL-3.1)

### Context

`dev-resources` carried a copy of `commit_attribution_scan.py` because the template published
no `.pre-commit-hooks.yaml`, and its README named the duplication. Decision 2026-09-23-002 made
the template publish one, so that repository consumes the persona linter, the frontmatter gate
and the attribution gate pinned by `rev`, with gitleaks from its own repository as here.

Publishing turned up three mechanics the design had not named. pre-commit installs a
`language: python` hook repository with `pip install .`, so the repository must be a package.
A remote hook runs from the consuming repository's root, so an `entry:` naming a path under
`scripts/` resolves to nothing there; the entry must be a console script. And every gate derived its
repository root from `__file__`, which inside pre-commit's virtualenv is a `site-packages`
directory: the persona linter would have judged the virtualenv.

### Decision

- **`pyproject.toml` makes the four modules the manifest needs installable**, flat from
  `scripts/`, with console scripts `session-closeout`, `kb-frontmatter-scan` and
  `commit-attribution-scan`. Its version is read from `new_project.TEMPLATE_VERSION`, the one
  value the tag gate verifies, so no second version is maintained by hand. `pyyaml` is a package
  dependency, so consumers declare nothing.
- **`.pre-commit-hooks.yaml` publishes three hooks:** `persona-lint` (`session-closeout
  --personas`, a new mode that runs the persona rule of `--check` alone), `kb-frontmatter-scan`
  and `commit-attribution`. Every hook declares `stages:` (2026-09-20-001). The two content
  gates carry `files:` for the paths they judge, so a consumer without that content shows them
  Skipped rather than passing over nothing; the attribution gate is `always_run`.
- **gitleaks is not re-published.** A manifest publishes only hooks that live in its repository;
  a consumer takes gitleaks from upstream with an explicit `stages:`, as this config does.
- **The published gates read their root from `git rev-parse --show-toplevel`**, falling back to
  the working directory, in `session_closeout.py` and `kb_frontmatter_scan.py`. pre-commit runs
  every hook from the consuming repository's root, and the documented direct invocations run
  from it too. The unpublished scripts keep `__file__`; they only ever run from `scripts/`.
- **A project is not a hook repository.** `new_project.TEMPLATE_ONLY` removes `pyproject.toml`
  and `.pre-commit-hooks.yaml` at birth, and `template_update.KEEP` never writes them: a Python
  project has a `pyproject.toml` of its own, and the updater's three-way merge would have
  conflicted on it at every release. The updater's fixture cross-checks the two lists.
- **MINOR, released as `v5.1.0`** under [[reference_template_versioning]]. No hook is added to
  the config, no command changes, and a project on the previous release adopts nothing; two
  files leave a new project at birth, which an existing project never had in use.

### Consequences

- The template is private, so a consumer needs read access to clone it, and pre-commit clones
  into `~/.cache/pre-commit`, which no per-directory git config reaches: the `includeIf` that
  rewrites plain ssh URLs to the personal identity inside `~/code/personal` does not apply
  there, and the keychain holds no https credential for github.com. Measured from that
  directory: https refused for want of a username; plain ssh accepted by whichever agent key
  GitHub recognized first, which the operator's environment runbook names as the wrong-identity
  failure; the `github.com-personal` alias accepted deterministically. `dev-resources` pins the
  alias URL. A GitHub Actions run in the consumer needs a deploy key or token secret, or a
  public template; `dev-resources` runs the gates as local hooks only until that is decided.
- A consumer keeps the template's layout for what these gates judge: `docs/personas/` and
  `docs/orchestration/knowledge/` with its `INDEX.md`. TMPL-3.4 moves the registry and the
  resource entries into `dev-resources` under those paths.
- `--personas` passes on a repository with no registry, with the count in its heading. The
  manifest's `files:` keeps that case from presenting as a run.

### Open question

- ~~Should `dev-resources` get a `gates` workflow, and if so how does it read the private
  template: a deploy key or fine-grained token stored as a repository secret, or the template
  made public?~~ **RESOLVED 2026-09-23 (with the operator):** the
  template stays private, including the sanitized lineage TMPL-4.4 will start. `dev-resources`
  gets no `gates` workflow: it has one clone with both hook types installed and proved, and a CI
  run there would duplicate what the local hooks already block while adding a secret to rotate.
  If a workflow is ever wanted, the credential is a read-only deploy key scoped to the template,
  never a token that expires, and the job recreates the `github.com-personal` ssh alias the
  pinned URL names.

### Verification

`pip install .` into a scratch virtualenv reported version `5.0.0` from the constant and the
three console scripts. Run from inside `dev-resources`, the installed scripts judged that tree:
no registry, no knowledge base, the attribution gate refusing a trailer (exit 1) and passing a
clean message (exit 0). A persona lacking `description:` and the `Insists on` and `Invocation`
sections exited 1 on `frontmatter` and `sections`; a well-formed one exited 0; an entry with no
frontmatter exited 1 on `no-frontmatter` and `no-entries-section`. Run from inside the template
with the same installed scripts, the linter found the two personas and the scan seventeen
entries, which proves the root comes from git and not from the virtualenv. Then `pre-commit
try-repo` from `dev-resources` against the template's working tree: the content gates Skipped,
the attribution hook exit 1 on a trailer and 0 on a clean message. The template's own suite
exit 0 with the new fixtures.

### Enforcement

`pyproject.toml`, `.pre-commit-hooks.yaml`, `scripts/session_closeout.py` (`repo_root`,
`--personas`, `cli`), `scripts/kb_frontmatter_scan.py` (`repo_root`),
`scripts/commit_attribution_scan.py` (`main` over the process arguments),
`scripts/new_project.py` (`TEMPLATE_ONLY`, its fixture), `scripts/template_update.py` (`KEEP`,
its fixture). Taught by [[reference_published_hooks]].

---

## Decision 2026-09-23-006: Personas are append-only, and the gate holds them to it

**Date:** 2026-09-23
**Made By:** Chair + AI (the rule in 2026-09-23-002; the mechanics decided here)
**Status:** APPROVED
**Builds:** the append-only bullet of 2026-09-23-002 (TMPL-3.2)

### Context

Decision 2026-09-23-002 ruled that an Invocation never changes in place: an enhancement bumps a
version and appends a changelog line, the linter refuses an Invocation change without the bump,
and the kickoff names the version it was written against. Three mechanics were left open: where
the version and changelog live, what the linter compares against, and what a bump without an
Invocation change means.

### Decision

- **`version:` is a positive integer in the persona's frontmatter**, required alongside `name`
  and `description`; both seeds start at 1. **`## Changelog` is a fourth required section**,
  after Invocation, one bullet per version: `- <version> — <date> — <what changed>`. The
  Invocation is extracted by section, so the changelog does not travel into a kickoff.
- **The comparison is against the committed copy at HEAD** (`git show HEAD:<path>`), which
  every stage of the gate can see, here and in a consumer running the published `persona-lint`.
  An Invocation that differs from it at the same version is `invocation-unbumped`; a lower
  version is `version-order`; a version with no changelog bullet is `changelog`. A new persona,
  or a committed copy from before the rule, constrains nothing, which makes the migration commit
  legal.
- **A bump with no Invocation change is allowed.** Expertise and Insists on may be enhanced too,
  and a bump that records nothing costs one changelog line. The rule guards the text an agent is
  addressed with.
- **The kickoff carries `**Persona version:** <n>`**, written by the scaffold and checked against
  the registry. The copy check already catches a drifted Invocation, so this field is for the
  reader; it is gated so it cannot be wrong. It is required, and the two kickoffs still in the
  folder (the consumed pair and the one being consumed) gained the line in the same commit as the rule.
- **MAJOR, released as `v6.0.0`** under [[reference_template_versioning]]: a required key fails
  every existing persona, a required section fails every existing persona file, and the kickoff
  field fails every existing kickoff. A project adopting it adds `version: 1`, a changelog bullet
  and the kickoff line, once. `dev-resources` moves its `rev` to it.

### Verification

Fixtures: a well-formed persona passes; missing `version:`, a non-integer version, a version with
no changelog bullet, an Invocation change without a bump, a version below the committed one, and
a kickoff naming the wrong or no version each fail on their rule; an Invocation change with its
bump and bullet, a bump with no Invocation change, and a pre-rule committed copy each pass. Six
broken variants run against the fixtures in a scratch harness before the suite was trusted. The
live proof on the real registry had to wait for the migration commit: against a committed copy
with no `version:` the rule constrains nothing, by design, so an Invocation edit before that
commit exited 0; after it, the same edit exited 1. Recorded in the archive repository's sprint-status.

### Enforcement

`scripts/session_closeout.py` (`PERSONA_KEYS`, `PERSONA_SECTIONS`, `CHANGELOG_ENTRY`, `Persona`,
`lint_persona` with `previous`, `persona_version`, `committed_text`, `lint_kickoff`,
`kickoff_skeleton`), `docs/personas/*.md`, `docs/standards/session_handoff_standard_v2.0.md` §5
and §6. Taught by [[reference_session_closeout]].

---

## Decision 2026-09-23-007: The registry and resource entries are synced from `dev-resources`

**Amended 2026-09-23:** `.resources-version` is the project's own state. The first derived
project to take `v7.1.0` received the template's stamp as an `add`; the updater now keeps it and
the initializer clears it at birth, released as `v7.1.1` (PATCH).

**Date:** 2026-09-23; amended 2026-09-23
**Made By:** Chair + AI (the design in 2026-09-23-002; the mechanics decided here)
**Status:** SUPERSEDED by 2026-10-23-003
**Builds:** the sync, ownership and contribution bullets of 2026-09-23-002 (TMPL-3.3)

### Context

Decision 2026-09-23-002 made `dev-resources` the source of the persona registry and of reference
knowledge that belongs to no one project, with the project holding a synced snapshot: a script in
the updater's idiom, ownership disjoint from the template's, sync at closeout, growth only through
a gated publish. Four mechanics were left to the build: how a verdict is decided when both sides
differ, how a resource entry is told from the template's own in the same directory, what the
closeout refuses, and what the first run does when `dev-resources` holds no registry at all.

### Decision

- **`scripts/resources_sync.py` fetches `dev-resources` at `--ref` into `refs/resources/<ref>`**
  and judges every owned path against that tree, exactly as the updater does against a release.
  Owned: every `docs/personas/*.md`; every `docs/orchestration/knowledge/*.md` whose frontmatter
  declares `source: dev-resources`, on either side. `INDEX.md` is merged by slug with the
  updater's own `merge_index`, so a synced entry gets its row the way a released one does.
- **Verdicts are decided by version, never silently.** Fetched only: `add`. Local only:
  `unpublished`. A higher fetched `version:`: `update`. A higher local one: `ahead`. The same
  version with different text, or an unversioned entry edited on either side: `CONFLICT`, kept,
  the stamp withheld; `--take <path>` takes the fetched copy, `--publish` sends the local one.
  A fetched entry without the declaration is `unmarked` and refused, because the declaration is
  what tells the updater to leave the synced copy alone.
- **The updater keeps what the sync owns.** `template_update.KEEP` gains `docs/personas/`, and
  `build_plan` keeps a knowledge entry when any of its three copies declares the source; the
  rule is one function, `resource_owned`, which the sync imports rather than copies. The
  updater's fixtures pin both.
- **The closeout refuses an unpublished persona.** With `.resources-version` present, every local
  persona is looked up in `refs/resources/<ref>`: absent there, or behind the local version, is
  `unpublished`; a stamp whose ref is not fetched in this clone is refused too, so a sync must
  precede every closeout. A project that has never synced is not held to it, which is what lets
  the migration land. Behind locally is the sync's business, not the gate's.
- **`--publish <clone>` writes what is ahead, unpublished or conflicting into a local checkout of
  `dev-resources`** for commit and push there; that clone's gates, the persona linter it consumes
  from this template, judge the contribution. The stamp `<ref> <sha>` is written only when
  nothing remains to publish and nothing conflicts.
- **The first run seeds the registry.** `dev-resources` held no `docs/personas/`; the first sync
  reported both personas `unpublished`, `--publish` wrote them, they were committed there under
  its `persona-lint`, and the sync back found both `up-to-date` and wrote the stamp.
- **MAJOR, released as `v7.0.0`** under [[reference_template_versioning]]: the closeout gains a
  check, and every project's closeout procedure gains a step and a script to run.

### Honest limit

The sync cannot tell an unedited local copy from an edited one without the previous synced blob,
so an unversioned entry that differs on both sides is always a conflict, resolved by hand with
`--take` or `--publish`. Personas carry versions and decide themselves; resource knowledge
entries do not, and the cost is one flag per edit. Adding `version:` to resource entries would
remove it and is the natural next step if the flag proves frequent.

### Verification

Seventeen fixtures over the pure verdicts, ownership and stamp; the updater's suite gained two
fixtures for the keep rule and the sync's session-gate rule three. Live, recorded in the archive
repository's sprint-status: the dry run against `dev-resources` reporting both personas unpublished;
`--apply --publish` writing them into the clone; that clone's commit under its own
`persona-lint`; the sync back up-to-date with the stamp written; and the closeout rule proved
by a scratch persona the ref lacks, by exit code without a pipe.

### Enforcement

`scripts/resources_sync.py`, `scripts/template_update.py` (`KEEP`, `resource_owned`, `build_plan`),
`scripts/session_closeout.py` (`published_state`, `unpublished_personas`, `cmd_closeout`),
`.pre-commit-config.yaml` (`resources-sync-selftest`), `docs/standards/session_handoff_standard_v2.0.md`
§7, `CONSTITUTION.md` §2.2. Taught by [[reference_resources_sync]].

---

## Decision 2026-09-23-008: Which knowledge entries are resource entries

**Date:** 2026-09-23
**Made By:** Chair + AI (the class in 2026-09-23-002; the rule decided here)
**Status:** APPROVED; SUPERSEDED by 2026-10-23-005 (with the sync retired, no entry is a resource
entry: the macOS toolchain entry is the template's own again, and a project's marked copy is settled
at adoption)
**Builds:** the "handbook-class knowledge" of 2026-09-23-002 (TMPL-3.4)

### Context

Decision 2026-09-23-002 made `dev-resources` the home for reference knowledge that is not
specific to one project, and 2026-09-23-007 built the sync that carries it. Neither said which
of the knowledge entries here qualify. The template's entries mostly explain its gates and the
decisions behind them, which is exactly what the freshness gate keys to this repository's log.

### Decision

- **An entry is a resource entry when both hold:** it declares `teaches: []`, because a resource
  explains no decision of any one repository; and its subject is a machine, a tool or a workflow
  rather than this template's own mechanisms. It is marked `source: dev-resources` and published.
- **One entry moves now:** [[reference_macos_toolchain]]. It was the only `teaches: []` entry,
  and its subject is the operator's machine.
- **Every gate entry stays,** including the two that teach no decision by content but describe
  this repository's scripts, and every entry with a non-empty `teaches:`. If an entry ever
  qualifies on the first rule but not the second, it stays; the second rule is the one that
  matters.
- **A moved entry keeps its slug, path and INDEX row here.** The sync merges rows from
  `dev-resources`' own `docs/orchestration/knowledge/INDEX.md`, which carries the same table
  shape and only resource rows, so a project's index gains the row without a second format.
- **MINOR, released as `v7.1.0`:** the mark changes which script writes the file, and a project
  on the previous release adopts nothing; the updater keeps the marked entry, and the project's
  first sync after that takes the marked copy with `--take`, once.

### Migration, stated

A project whose copy of a moved entry predates the mark holds an unmarked file; the updater
keeps it (any of the three copies marked means keep), and the sync then sees a fetched marked
copy against a local unmarked one, which is a conflict by 2026-09-23-007's rule. The remedy is
`--take <path>`, once per moved entry per project, and the probe records it under TMPL-3.4.

### Enforcement

`source: dev-resources` in the moved entry's frontmatter, read by `template_update.resource_owned`
and `resources_sync.owned`. Taught by [[reference_resources_sync]].

---

## Decision 2026-10-22-001: `v2.0.0` runs the framework on Claude Code's native machinery

**Amended 2026-10-22 (S3):** a session takes its persona from the `SessionStart` hook, which injects
the agent's prompt unless the session already runs as that agent. `claude --agent` is available, not
required: under it the agent's prompt replaces Claude Code's built-in system prompt whole (decision
2026-10-22-005).

**Date:** 2026-10-22; amended 2026-10-22
**Made By:** Chair + AI
**Status:** APPROVED
**Affects:** `AGENTS.md`, `CLAUDE.md`, `AGENT_INTEROP.md`, `CONSTITUTION.md` §2 and §6, `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md`, `docs/standards/session_handoff_standard_v2.0.md`, `docs/personas/`, `.claude/`

### Context

Claude Code does nearly all the agentic work on this framework, with local models as the only
other reader. Measured on 2026-10-22, the cold start asks an agent to read about 74 KB of
markdown across ten files before building; the cold-start procedure is written in four places
and the closeout in three; the interop contract is a 6 KB rationale for a tool split that no
longer exists. Claude Code's own docs, read the same day: it reads `AGENTS.md` natively from
v2.1.277 (the operator's install is 2.1.267); a `SessionStart` hook can run commands and inject
their output into context, and runs again with a `compact` matcher after compaction; a `Stop`
hook can refuse to end a turn; `PostToolUse` fires after every edit and command; subagents in
`.claude/agents/` carry their own context and can run the main session by `claude --agent`;
skills in `.claude/skills/` run forked into a subagent with `context: fork`; rules under
`.claude/rules/` load only when a matching path is touched. The docs also say that `CLAUDE.md`
and hooks are context, not enforcement, except permissions and `PreToolUse`.

The operator's standing problem is the compaction cliff: a closeout that dies mid-way, and
in-flight plans and judgements lost when the conversation is summarized.

### Decision

- **One cold start, run by a hook.** The procedure lives in `AGENTS.md` alone; `CONSTITUTION.md`
  §2, the checklist and the handoff standard point to it. A `SessionStart` hook runs the identity
  gate, `git pull`, `session-verify` and the document-queue check, and injects their results, the
  current kickoff and the newest sprint-status entry; with the `compact` matcher it re-injects the
  same after compaction. The checklist's comprehension questions, which no script verifies, go.
- **Checkpoint discipline becomes a `Stop` hook** that refuses to end a turn while sprint files are
  modified and uncommitted, or while the working notes are older than the turn's edits.
- **The uncommitted interval is banked mechanically.** A `PostToolUse` hook writes a session
  journal under `sprint/recovery/` (file changed, command run, exit code) without the model's
  cooperation; a working-notes file of fixed small shape (plan, open decisions, half-done work)
  is what the `Stop` hook demands; both are re-injected after compaction and cleared at closeout.
  `PreCompact` is a backstop, tested before it is relied on, since a block when the context is
  already full can wedge a session.
- **Personas are subagents** in `.claude/agents/<slug>.md`: the registry moves there, `persona-lint`
  and `resources_sync.py` follow it, and a kickoff names the agent instead of copying its
  invocation. The main session runs as the named agent.
- **Procedures are skills**, forked where heavy: the closeout, the release cut, the planning
  session, the sanitize-and-cut, document production. The `SKILL.md` is the one home of the
  procedure; the standards shrink to the law. A gate keeps a skill's commands in step with the
  config, as the runbook gate does for hooks.
- **Judgement rules are path-scoped** under `.claude/rules/`, loaded when a matching file is
  touched; the constitution and the checklist shrink accordingly.
- **`AGENT_INTEROP.md` is retired** into `AGENTS.md`; its one law is already a prime directive
  there. `CLAUDE.md` stays as the `@AGENTS.md` bridge until the installed Claude Code is at least
  v2.1.277, then goes; the condition is written into the story.
- **What does not move.** The pre-commit suite, the CI workflow, the sprint files, the decisions,
  the knowledge base and the closeout gate stay as they are: git hooks and CI enforce for any
  agent on any machine; Claude hooks are for context and ergonomics.
- **Settings.** `disableWorkflows` on, so a typed keyword cannot start a multi-agent workflow;
  `ask` rules for the one-way doors met this month: `gh repo delete`, `git push --delete`,
  `gh repo edit --visibility`.
- **MAJOR**, `v2.0.0`, together with 2026-10-22-002: files a project references are removed and
  renamed, and the registry moves, so every derived project acts once at adoption.

### Consequences

- Compaction becomes a slope: committed state, the brain, the kickoff, the journal and the notes
  survive it; only reasoning never written down is lost, and the `Stop` hook narrows that window
  to one turn.
- A derived project's `template_update.py` must carry `.claude/agents/`, `.claude/skills/`,
  `.claude/rules/` and `.claude/settings.json` by the ownership rules; the initializer and the
  sanitizer learn the journal and notes paths.
- The three existing projects take `v2.0.0` through the updater as the release's own proof.

### Enforcement

To be built as epic TMPL-1; each story names its gate. Taught by a knowledge entry written with
the build.

---

## Decision 2026-10-22-002: Authoritative documents stop going stale

**Date:** 2026-10-22
**Made By:** Chair + AI
**Status:** APPROVED
**Affects:** `docs/governance/doc_control_standard.md`, every document that carries `authority:`, this file's body format

### Context

Updates, design changes and reversals land in the decision log and the knowledge base, and the
documents that are supposed to be the source of truth for a scope, the PRD, the architecture,
the runbooks and the standards, are never brought up to date. The document-control standard says
"update the documents and the changelog table" and nothing enforces it. The knowledge base does
not have this problem because `teaches:` and `verified:` are gated; it also cannot catch a
*missing* update, since a new decision names no document.

The operator's two further constraints: an agent rewriting a document inline at decision time
produces patchwork, and the remedy cannot be a closeout item, because closeouts are where
compaction strikes, nor open-ended.

### Decision

- **Authorities declare themselves.** A source-of-truth document carries frontmatter `authority:
  <scope>`, `implements: [decision-ids]`, `verified: <date>`, and ends with a `## Version log`
  table: version, date, decision, summary, commit. The frontmatter is the registry.
- **Decisions declare impact.** Every decision body from this one forward carries `**Affects:**`:
  the authorities it changes, with the sections and the nature of the change, or `none`. Older
  decisions read as `none`.
- **The gate accepts two outcomes and nothing else.** For each decision naming a document, the
  document's version log holds a row citing that decision, or the tracker holds a story citing the
  decision and the document, not Done. A row written by a session other than the technical
  writer must carry a fact marker: a value, a name, a path, a count. Structural changes are queued.
- **The queue drains at cold start, bounded.** A `doc-queue` manual-stage gate, run by the
  `SessionStart` hook, fails while any queued story is older than one session, read from a
  `Queued: S<N>` note on its row. The drain runs as the technical-writer subagent, one document per
  invocation, in its own context, and returns the rows it wrote. The queue is visible at every
  closeout and is never a closeout step.
- **The commit is stamped after the fact and verified.** The newest row reads `pending`;
  `--stamp` fills the hash once the commit exists, and the gate verifies every stored hash against
  git. `--history <doc>` derives the commit for any unstamped row. A stored value with a gate is
  allowed; a hand-maintained one without is not.
- **Scope at introduction.** The standards and the gate runbook are marked first, so the gate has
  real content to prove against; a project marks its PRD, architecture and runbooks.
- **Part of `v2.0.0`.** A new gate that can fail content a project already has.

### Consequences

- The document-control standard is rewritten around the gate and loses its "stays private" fossil.
- The `technical-writer` is the second subagent in the registry, published to `dev-resources`.
- The batching is the anti-patchwork control: one writer pass per document over every pending
  change, instead of one paragraph per deciding session.

### Enforcement

To be built as epic TMPL-2: `scripts/doc_authority_scan.py` with fixtures proved against broken
variants, the `doc-queue` gate, the writer agent and its forked drain skill.

---

## Decision 2026-10-22-003: `v2.1.0` is the development team and the coding standard, designed first

**Date:** 2026-10-22
**Made By:** Chair + AI
**Status:** APPROVED
**Affects:** none yet; the design sessions name them

### Context

Where a project's task is software, the operator wants a trained team of role agents that hand
off to each other as a human team does and produce code that passes a security audit, running
autonomously until something needs the operator. Separately, agents write verbose, run-on,
repetitive code when nothing stops them, and a coding standard that is prose stops nothing.

### Decision

- **The team is built on the `v2.0.0` substrate, not with it.** Roles are subagents with isolated
  context and narrow briefs (product owner, architect, planner, implementer, test engineer, code
  reviewer, security auditor, technical writer, release manager). Every handoff is an artifact in
  the repository that a gate judges, never a conversation between agents; a role may not start
  until its input artifact exists and passes. The operator's checkpoints are a written list of
  review triggers the orchestrating skill stops at: a new dependency, a schema, auth or crypto
  change, an external service, a cost, a security finding the auditor cannot clear, anything a gate
  cannot judge. Orchestration is a saved workflow invoked deliberately, one story at a time.
- **The coding standard has three layers.** Mechanical, in the gate suite: function and file
  length, complexity ceilings, duplicate detection, formatter and linter, type checks, a coverage
  floor, dependency audit; a core of numbers with a rule that every stack maps each to a tool,
  chosen per project at its planning session. Process, in the team: design before code, stories
  the size of a module, a reviewer whose brief is structure and duplication and who is not the
  implementer, plan mode forced on for implementation skills. Judgement: one page under
  `.claude/rules/`, path-scoped to code, opening with `CONSTITUTION.md` §4A.
- **Each opens with a design session.** The team's: roles, artifacts, triggers, orchestration,
  with the operator. The standard's: with a specialized reviewer agent, the core limits proved
  against a known-good and a known-bad codebase before adoption, because this standard is the
  hardest thing in the framework to unwind once development starts.
- **MINOR**, `v2.1.0`: agents and a stack profile a project opts into.

### Enforcement

Epics TMPL-3 and TMPL-4; the design sessions log their own decisions.

---

## Decision 2026-09-25-004: The first public release is `v1.0.0`, cut on the finished tree

**Date:** 2026-09-25
**Made By:** Chair (the ask) + AI (the mechanics)
**Status:** APPROVED
**Builds on:** 2026-09-23-003 (the pristine cut and the sanitizer)

### Context

The pristine cut tagged the sanitized tree `v1.0.0` before the go-live work: the template flag,
the hook pin, the birth probe, the visibility decision and its control, the license, the public
README and the rulesets. Those three sessions cut `v1.0.1`, `v1.1.0` and `v1.1.1`, so the first
version anyone outside the owner's account could take was a `v1.1.1` whose predecessors had never
been usable by them. The operator asked that the finished template's first release be `v1.0.0`.

### Decision

- **The four tags are removed**, locally and on GitHub, and the finished tree is sanitized with
  `sanitize_template.py --apply`, which regenerates the two sprint documents to the template's own
  S1 and clears the handoff pairs and their archive, as the cut did. Then `--release v1.0.0`, one
  commit `release: v1.0.0`, one annotated tag `v1.0.0`. The version gate sees one tag, the earliest,
  exempt from the bump rule, and the constant it verifies reads `v1.0.0`.
- **History is kept.** No force-push, no rewritten commits: the go-live sessions' commits and their
  `release:` messages stay in `git log`, and the rulesets of 2026-09-25-003 stay in force. A
  reader who wants the go-live diary has the commits; the sprint documents describe the pristine
  state, as they did after the cut.
- **The consumer follows.** `dev-resources` pins the new `v1.0.0`; nothing it consumes changed
  between the removed tags and this one. No derived project exists that carries a removed tag.
- **Earlier "released as" notes are read as folded in.** Decisions 2026-09-25-001 and -002 name
  `v1.1.0` and `v1.1.1`; those tags no longer exist and both changes are part of `v1.0.0`. The
  notes are amended to say so rather than rewritten, because a decision body is a record.
- No bump type: the earliest tag has no predecessor. Everything after this is judged from
  `v1.0.0` by [[reference_template_versioning]].

### Consequences

- The next session on this repository is S1 with no pair, as after the cut; it opens its first
  story before it can close out. The go-live epics are in the git history, not the tracker.
- A tag, once published, is meant to be permanent. This is the one time it was not, before any
  outside consumer existed; it is not a precedent, and [[reference_pristine_cut]] says so.

### Enforcement

`scripts/template_version.py --check` (one tag, its commit stamped `v1.0.0`),
`sanitize_template.py --check` exit 0 and `session-verify` exit 0 at S1, both recorded at the cut.
Taught by [[reference_pristine_cut]].

---

## Decision 2026-09-25-003: The default branch is protected against deletion and force-push, and nothing more

**Date:** 2026-09-25
**Made By:** Chair + AI
**Status:** APPROVED
**Builds on:** 2026-09-22-001 (protection not pursued while private), 2026-09-25-001 (public)

### Context

With both repositories public, branch protection is available at no cost. Two of its rules guard
against loss that nothing else can undo: a deleted default branch and a rewritten history. The
third common rule, a required status check before anything lands on `main`, would end the direct
push that every checkpoint and closeout here is, and force a pull-request flow on one developer
for a workflow that already reports within two minutes.

### Decision

- A repository ruleset named `protect main`, enforcement active, on the default branch of
  `SaltyBrett/agentic-dev-template` and `SaltyBrett/dev-resources`, with two rules: `deletion`
  and `non_fast_forward`. Created through the REST API; the archive is read-only and needs none.
- No required status check and no pull-request requirement. The `gates` workflow keeps reporting;
  the local hooks keep blocking (2026-09-22-001).
- Revisit when a second contributor exists: that is the day a required check earns its cost.

### Consequences

- The Claude-only `settings.json` deny of `git push --force` is now backed by the server for the
  default branch; a force-push from any clone or tool is refused by GitHub.
- A mistaken push to `main` is still corrected by a new commit, never by rewriting.

### Enforcement

GitHub, server-side. Nothing in the tree; `gh api repos/<owner>/<repo>/rulesets` lists it. Taught
by [[reference_ci_backstop]].

---

## Decision 2026-09-25-002: MIT, under the operator's name

**Date:** 2026-09-25
**Made By:** Chair (the license) + AI (the mechanics)
**Status:** APPROVED

### Context

A public repository with no license file is all rights reserved: anyone who creates a project from
the template infringes. Neither public repository had one after decision 2026-09-25-001.

### Decision

- **MIT**, copyright 2026 Brett Bennett, as `LICENSE` in the root of the template and of
  `dev-resources`, identical text. MIT because the template exists to be copied into private
  commercial projects, and MIT asks nothing of them beyond keeping the notice.
- **A project owns its license from birth.** The initializer leaves `LICENSE` in place (it is in
  no mutating list), and `template_update.KEEP` names it so a release never rewrites the license
  a project chose. A project born before this decision receives no license by update; adding one
  is that project's own act.
- **PATCH**, released as `v1.1.1` with the public README (TMPL-2.2): no project must act. That tag
  was folded into the first public `v1.0.0` by 2026-09-25-004.

### Enforcement

`LICENSE`; `scripts/template_update.py` (`KEEP`). Verified by both self-tests and a scratch birth
whose dry run lists no `remove LICENSE`; GitHub reports the license on both repositories.

---

## Decision 2026-09-25-001: The template is public; a project made from it is private by default

**Date:** 2026-09-25
**Made By:** Chair (the visibility) + AI (the control and the mechanics)
**Status:** APPROVED
**Supersedes:** the "stays private" resolutions in 2026-09-22-001 and 2026-09-23-005

### Context

After the pristine cut the live repository's history begins at the sanitized tree, which removed
the operator's original reason for keeping it private. Two consequences of privacy remained in
force: `dev-resources` could have no `gates` workflow, because a consumer's Actions run cannot
clone a private hook repository without a secret, and its pin had to name an ssh host alias that
only the operator's machines resolve. The operator decided: the template and `dev-resources` go
public, and every project created from the template is private unless it is meant otherwise.

"Private by default" cannot be set on GitHub's side for a personal account: the "Use this
template" flow and `gh repo create --template` both take the visibility at creation time, and
nothing stops a public choice. A written rule in the guide would be the convention-as-control
shape this repository removes.

### Decision

- **`SaltyBrett/agentic-dev-template` and `SaltyBrett/dev-resources` are public.** Before the
  flip, gitleaks scanned the full history of both (13 and 9 commits) and found nothing. The
  archive, `SaltyBrett/agentic-dev-template-archive`, stays private: it is the build diary.
- **The initializer enforces private by default.** `new_project.py` reads the project's
  visibility from GitHub (`gh repo view --json isPrivate`) before it plans anything and refuses a
  public repository unless `--public` is given, printing the one command that makes it private.
  A visibility it cannot read (no `gh`, or a remote that is not GitHub) is reported and not
  refused: an unreadable answer is neither public nor private. `--force` does not bypass this;
  the two refusals are separate flags because they are separate intentions.
- **Branch protection is still not enabled** on the template, though it is now free. Every
  checkpoint is a direct push to `main`; a required status check would force a pull-request flow
  on one developer for a workflow that already reports, and a red run is fixed in the session
  that caused it (2026-09-22-001).
- **`dev-resources` pins the https URL** at the current template tag and gains the same `gates`
  workflow, which its public template now lets it run without a credential.
- **MINOR**, released as `v1.1.0`: a project already born never re-runs the initializer, so
  nothing existing has to act; a new refusal at birth is new capability. That tag was folded into
  the first public `v1.0.0` by 2026-09-25-004.

### Consequences

- A project's first command tells its operator when the repository is public. The web flow's
  visibility picker is no longer the only control.
- A consumer of the published hooks no longer needs the ssh host alias or a credential; the
  measured cost of a private hook repository stays recorded in [[reference_published_hooks]] for
  anyone who consumes a private one.
- The initializer now shells out to `gh`. Where `gh` is absent the rule is not checked, and the
  run says so; it never fails for want of the tool.

### Verification

Self-test fixtures for the slug parser and the verdict over every reading, proved against
broken variants before they were trusted; live, the initializer refusing the public template
clone itself before the template refusal is reached is not possible (the template refusal comes
first), so the live proof is a scratch project: refused while public, accepted with `--public`,
accepted once private. `dev-resources` ran its suite from a cleared pre-commit cache against the
https pin and its first `gates` run was observed. Recorded in the S2 sprint-status entry.

### Enforcement

`scripts/new_project.py` (`repo_slug`, `repo_visibility`, `visibility_verdict`, `--public`, three
fixtures), `TEMPLATE_GUIDE.md` Step 8. Taught by [[reference_ci_backstop]] and
[[reference_published_hooks]], both re-verified.

---

## Decision 2026-09-24-001: Rules with no control, found in the fossil sweep: which get one, which go

**Date:** 2026-09-24; amended 2026-09-24 (TMPL-5.5 built, its enforcement and bump named)
**Made By:** Chair + AI
**Status:** APPROVED
**Builds:** TMPL-5.3 and TMPL-5.4 (epic TMPL-5, opened for exactly this shape); TMPL-5.5 after them

### Context

The three standards and `sprint/recovery/` predate every gate and no session since had read them
whole. TMPL-5.4 read them, with `CONSTITUTION.md` §6.2 and `doc_control_standard.md` under
TMPL-5.3, for two shapes: a checklist standing in for a control, and a GCC line a commercial
project inherits. Fossils were fixed in the same work unit (the archive repository's sprint-status names
each). What remains is every written rule that no script enforces. The kickoff's instruction was
to decide, per rule, whether it gets a control or is deleted, and to build nothing here.

### Decision

| Rule | Where | Verdict |
|------|-------|---------|
| Never start a story whose dependencies are not `Done` | sprint standard §7 | **Gets a control: TMPL-5.5.** The state gate already parses the tracker for its statistics; a story `In Progress` or `Done` with a dependency not `Done` is one more row check. |
| No `[EXAMPLE]` or `{{PLACEHOLDER}}` content in a live sprint | sprint standard §6, §5.3, §11.2 | **Gets a control: TMPL-5.5**, in a project (a `.project-profile` exists) once a non-example epic exists, so a fresh project's shipped example epic does not fail it at birth. |
| Agents change documents through pull requests only; feature branch, reviewers, merge | doc control, Change Workflow and Agentic vs Human | **Deleted.** Withdrawn by 2026-09-22-001 ("no branch-and-pull-request convention is imposed") and contradicted by every `checkpoint:` commit since. The section now states what is enforced. |
| PR Review Checklist: linting clean, governance header, changelog, manifest/tag plan, evidence path, agentic usage documented | doc control | **Deleted.** The items the suite judges are the suite's (the runbook names them); the rest name things this repository does not define: a linter, a governance header, a manifest. |
| Maintain a manifest with pointers and tag references | doc control, Tagging | **Deleted.** No manifest exists; `template_version.py` verifies the template's tags, and a project's baseline uses the same form. |
| Validation evidence must be captured with the template | recovery README rule 3; doc control, Evidence | **Not a control, and now says so.** The trigger, a validation run, is not observable from the tree, so no gate can prove it happened. Reworded from *must* to where a result goes, marked ungated. |
| Update the authority matrix on supersession; STOP and escalate when two artifacts claim CURRENT | recovery README, `AUTHORITY_MATRIX.md` | **Instruction, kept.** Behaviour in a situation, the class of `CONSTITUTION.md` §8, not a claim that a check exists. |
| Prohibited practices, rotation schedule, audit, emergency procedures | secrets standard §7 to §10 | **Kept, outside a repository gate's reach.** They govern the project's runtime. gitleaks covers the committable subset (a secret in code). |
| Planning protocol preconditions and output checklist | sprint standard §5.1, §5.3 | **Kept as the protocol's own output check.** Its mechanical items are gated (statistics reconcile, the entry cap) or go to TMPL-5.5; the rest (PRD coverage, user confirmation) are judgement. |
| `[Locked]` craft rules | document production standard §7 to §14 | **Kept.** Style for produced Office documents, not repository state. |

### Bump

PATCH for the sweep. No enforced rule changes: the deletions remove prose a decision had already
withdrawn or that named a control that never existed, and the fences move GCC lines to where the
profile already governs. Released as `v8.0.1`.

MAJOR for TMPL-5.5: a project's tracker can now fail on rows it already has, a `Done` story
whose dependency was never finished, or the shipped example epic left beside a real one. Released
as `v10.0.0`.

### Enforcement

`scripts/session_closeout.py --check`, on every commit: `dependency-order` (a story `In Progress`
or `Done` whose listed dependency is not `Done`, or is no story) and `live-placeholder` (in a
project whose tracker holds a non-example epic, an `[EXAMPLE]` row or heading or an unfilled
token in the tracker, sprint-status or the decision log, outside inline or fenced code). The
sprint standard §7 and §11 say the rules are gated; the runbook's `session-closeout-check` section
lists them. `doc_control_standard.md` and `sprint/recovery/README.md` name this decision where a
rule is stated as ungated. Taught by [[reference_session_closeout]] for the two controls and by
[[reference_project_profiles]] for the fences; the sweep itself is recorded in the archive
repository's sprint-status.

---

## Decision 2026-10-22-004: The session journal and the working notes are local, never committed

**Date:** 2026-10-22
**Made By:** AI (S2), within decision 2026-10-22-001; put to the operator at the S2 handover
**Status:** APPROVED
**Affects:** `.gitignore`, `scripts/session_journal.py`, `scripts/session_stop.py`, `scripts/session_start.py`, `scripts/session_closeout.py` (`--closeout`)

### Context

TMPL-1.2 builds the journal (`sprint/recovery/journal.md`, one line per Edit, Write or Bash event,
written by a `PostToolUse` hook) and the working notes (`sprint/recovery/WORKING_NOTES.md`, which
the `Stop` hook demands). Decision 2026-10-22-001 says both are cleared at closeout and that the
journal writer must be safe beside the gate suite; it does not say whether they are committed.

Tracked, the journal would carry every command an agent ran into the history of a public
repository, where one command holding a token is a leak that rewriting history cannot fully undo,
and a command naming a banned feature fails the scanner on the next commit. pre-commit stashes
unstaged edits to tracked files around a hook run, so a journal line appended by a parallel tool
call inside that window would land between the stash and its restore. And every tracked sprint
file the agent touches each turn would trip the `Stop` hook's own rule against uncommitted sprint
files.

### Decision

- Both files are gitignored. `session_journal.py` owns their paths and the notes' shape; the
  `SessionStart` hook creates the notes when they are missing; the closeout gate (`--closeout`)
  resets both when it passes.
- The `Stop` hook leaves both out of "uncommitted work" by path as well as by `.gitignore`, so its
  rule holds even if the ignore lines are lost; the journal self-test fails if they are.
- What survives a lost clone or a move to another machine is the committed state, as before. The
  journal and notes bank the interval against compaction and a dead session on the same clone,
  which is the failure the decision names.

### Consequences

- The writer is safe beside the suite by construction: an ignored file is outside the stash, and
  the scanners, gitleaks and the sanitize check read only what git would commit.
- The notes are reasoning in flight, a cache under the prime directive; anything durable in them
  still goes to the tracker, the decision log or a knowledge entry.
- The initializer and the updater carry the two `.gitignore` lines with the file; TMPL-1.6 confirms
  the ownership.

### Enforcement

`scripts/session_journal.py --self-test` (`session-journal-selftest`) checks that the repository's
`.gitignore` covers both paths and that concurrent appends keep every line whole;
`scripts/session_stop.py --self-test` that the notes never count as the newest change. Taught by
[[reference_claude_code_hooks]].

---

## Decision 2026-10-22-005: Personas are agent files, and the start hook gives the session its persona

**Date:** 2026-10-22
**Made By:** Chair + AI (S3): the persona's path to the session and the `dev-resources` window by
the operator, put as questions; the format by the AI
**Status:** APPROVED; SUPERSEDED (dev-resources holding the registry) by 2026-10-23-003
**Amends:** 2026-10-22-001 (its personas bullet: the main session no longer runs as the agent by default)
**Builds:** the personas bullet of 2026-10-22-001 (TMPL-1.3)
**Affects:** `.claude/agents/`, `docs/personas/` (removed), `scripts/session_closeout.py`, `scripts/session_start.py`, `scripts/resources_sync.py`, `scripts/template_update.py`, `scripts/new_project.py`, `scripts/sanitize_template.py`, `.pre-commit-hooks.yaml`, `.pre-commit-config.yaml`, `docs/standards/session_handoff_standard_v2.0.md` §3, §5 and §6, `dev-resources`

### Context

Decision 2026-10-22-001 moved the persona registry to `.claude/agents/` and said the main session
runs as the named agent. The sub-agents reference, read whole on 2026-10-22 (Claude Code 2.1.308),
settles the mechanics: the file's body is the agent's system prompt; only `name` and `description`
are required, and a key Claude Code does not know is ignored without a word; a frontmatter that
does not parse makes Claude Code skip the file, also without a word; `name` is the identity hooks
receive as `agent_type`. And under `claude --agent <name>` a non-empty prompt **replaces Claude
Code's built-in system prompt whole**, as `--system-prompt` does, while `AGENTS.md` still loads.

A probe in a scratch clone of the committed hooks: `claude --agent framework-maintainer -p` gave back
a canary from the agent's body, quoted the heading of `AGENTS.md`, saw the kickoff the start hook
injected, and the hook's input carried `agent_type: framework-maintainer`. Its prompt was about
2,500 tokens smaller than a control run without `--agent`, whose hook input carried no `agent_type`
and whose answer had no persona.

Separately, `dev-resources` pins `persona-lint` at `v1.0.0`, and the three projects on `v1.0.0`
sync `docs/personas/` from its `main`. Two of them hold a sync stamp, so if the folder left
`dev-resources`, their next closeout would refuse every persona as unpublished, and the remedy it
prints (`--publish`) would write the old folder back.

### Decision

- **The format.** `.claude/agents/<slug>.md`. The frontmatter holds `name` (the slug, equal to the
  filename stem), `description`, `version` (a positive integer) and `expertise`, `insists_on` and
  `changelog` as YAML lists of strings. The body is the Invocation, verbatim, and nothing else,
  because the body is the prompt. `slug:` and the human title go: `name` is the slug. The five
  personas move with their text unchanged, so each keeps its version and the S3 kickoff's copy
  still matches.
- **The linter parses the frontmatter as YAML**, since Claude Code skips a file whose frontmatter
  does not parse and says nothing. The import is lazy, so the session hook, which imports the
  closeout module, needs no PyYAML. The append-only rules of 2026-09-23-006 carry over unchanged
  against the committed copy at HEAD, the body standing for the Invocation. A moved file has no
  committed copy at its new path and constrains nothing, which makes the move commit legal.
- **The session takes its persona from the start hook, not from `--agent`** (the operator's
  choice). The kickoff names the agent, and `session_start.py` reads `agent_type`: equal to the
  kickoff's persona, it says so; otherwise it injects the agent's prompt as context, at startup and
  after compaction. A plain `claude` session, the VS Code extension and `claude --agent` all end
  with the persona in context; only `--agent` also drops Claude Code's built-in prompt, so it is
  available, not required.
- **The kickoff names the agent.** Section 1 is one line, written by the scaffold, naming
  `.claude/agents/<slug>.md`. The linter accepts that line or a verbatim copy of the prompt, so
  `KICKOFF_S3.md`, written under the old rule, stays valid. `**Persona version:**` stays and is
  still checked against the registry.
- **`dev-resources` holds both trees until TMPL-2.4** (the operator's choice). It gains
  `.claude/agents/`, judged by `persona-lint` at a template commit that reads the new location, and
  keeps `docs/personas/` frozen, still judged by `persona-lint` at `v1.0.0`, so a project on
  `v1.0.0` keeps syncing unchanged. TMPL-2.4, which takes the three projects to `v2.0.0`, removes the
  old tree. The template pushes first; `dev-resources` then pins that commit by its SHA, there being
  no `v2` tag yet. Between the two pushes neither repository's gates read the other's new state.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001): the registry's path, the persona's shape and
  the kickoff's section 1 change for every project.

### Consequences

- A persona enhanced during the window is published by the template to `.claude/agents/`. A
  `v1.0.0` project's publish writes `docs/personas/` and reaches `.claude/agents/` only when
  TMPL-2.4 ports it, so TMPL-2.4 compares the two trees before removing the old one.
- A project adopting `v2.0.0` must carry its own `docs/personas/` into `.claude/agents/`; the
  ownership rules (TMPL-1.6) and the adoption (TMPL-2.4) own that migration.
- Claude may delegate to a persona agent by its description, as to any project agent; that is the
  reuse the role agents of 2026-10-22-003 will build on.

### Verification

Fixtures: the closeout self-test (87 checks) covers the agent shape, the YAML refusals, the
append-only rules, both forms of section 1 and a module load with PyYAML blocked; the start
self-test (28) the four persona cases at startup and after compaction; the sync self-test (18)
pins the owned path. Twenty-two broken variants, each failing at least one fixture. Live, in a
scratch clone of the committed template: `claude --agent framework-maintainer -p` answered in the
persona, its hook input carried `agent_type: framework-maintainer` and the hook said the session
ran as that agent; a plain `claude -p` got the prompt injected verbatim and answered as Claude Code
holding the persona; a body edited without a bump exited 1 (`invocation-unbumped`), with the bump 0.
In `dev-resources`, both pins ran (five personas in each tree), the published hook refused the same
unbumped edit, and its `gates` run was green; the template's sync then reported every agent
`up-to-date`, and a `v1.0.0` project's own sync, in a scratch clone, still resolved every persona
from the frozen tree.

### Enforcement

`scripts/session_closeout.py` (`PERSONAS`, `PERSONA_KEYS`, `persona_frontmatter`, `lint_persona`,
`persona_line`, `lint_kickoff`, `kickoff_skeleton`), `scripts/session_start.py` (the persona
section), `scripts/resources_sync.py` (`PERSONAS`), `.pre-commit-hooks.yaml` (`persona-lint`'s
`files:`), and in `dev-resources` its `.pre-commit-config.yaml`. Taught by
[[reference_session_closeout]] and [[reference_resources_sync]].

---

## Decision 2026-10-22-006: Rules are path-scoped judgement, and a gate keeps them so

**Date:** 2026-10-22
**Made By:** AI (S3), within decision 2026-10-22-001; reported to the operator at the S3 handover
**Status:** APPROVED
**Builds:** the path-scoped rules bullet of 2026-10-22-001 (TMPL-1.5)
**Affects:** `.claude/rules/`, `CONSTITUTION.md` §6.3, `docs/orchestration/knowledge/INDEX.md`, `scripts/session_closeout.py` (`--check`), `AGENTS.md` (governance map)

### Context

Decision 2026-10-22-001 moves judgement that applies only when certain files are touched into
`.claude/rules/`. The memory reference, read 2026-10-22: a rule with `paths:` loads when Claude
reads, writes or edits a matching file; a rule without `paths:` loads in every session, like
`CLAUDE.md`; a frontmatter that does not parse is ignored and the rule loads as if it had no
`paths:`; a glob that matches nothing makes a rule that never loads. Claude Code reports none of
these. And a rule is Claude's alone: Codex reads `AGENTS.md` and what it points to.

### Decision

- **A rule here is path-scoped or it is refused.** Always-loaded text belongs in `AGENTS.md`, the
  one brain; an unscoped rule would be a second one. The session state gate refuses a rule whose
  `paths:` does not parse as a list of globs, a rule no file git would commit matches, and a rule
  that repeats a sentence of `AGENTS.md`.
- **Rules are repository markdown and the home of their instructions.** `AGENTS.md`'s governance
  map tells any agent to read the rules whose `paths:` match what it edits, so the instructions stay
  portable. A rule points to the knowledge entry that holds the why, and never restates it.
- **Three subjects, four files:** gate scripts and the suite, knowledge entries, decision logs and
  the sprint documents. `CONSTITUTION.md` §6.3 becomes a pointer: its reasoning moves to a
  knowledge entry and its reading and writing rules to the knowledge-entry and decision-log rules.
  The knowledge index keeps its reading rule and sheds its frontmatter block, and its template
  (which had no frontmatter at all), to the knowledge-entry rule.
- Part of `v2.0.0` (decision 2026-10-22-001): a project's own unscoped rules fail the new check.

### Consequences

- A project that kept instructions in an unscoped rule moves them to `AGENTS.md` or scopes them.
- The sprint documents keep their own headers: the generators write them, and the header is read
  at cold start, when the reading rule matters.
- TMPL-1.6 carries `.claude/rules/` through the initializer, the updater and the sanitizer.

### Enforcement

`scripts/session_closeout.py` (`RULES`, `lint_rule`, `glob_regex`, `expand_braces`, `sentences`,
`restatements`) in `session-closeout-check`. Taught by [[reference_claude_code_rules]]; the moved
section by [[reference_kb_freshness]].

### Verification

Fixtures in the closeout self-test for every refusal and the glob translation; fifteen broken
variants, each failing one. Live, in a scratch clone: an unscoped and a dead rule each failed the
check by name; a canary rule scoped to one knowledge entry was absent from a session that used no
tool and from one that read `README.md`, and present in one that read the entry. The first version
compared whole sentences and let a rule copying a clause of `AGENTS.md` pass; the check now finds a
sentence inside the other text either way, and the plant fails it.

---

## Decision 2026-10-23-001: Procedures are skills, and a skill is repository markdown

**Date:** 2026-10-23
**Made By:** Chair + AI (S4): how the forked closeout receives the session's judgement, and which
skills are the operator's alone, by the operator, put as questions; the rest by the AI
**Status:** APPROVED
**Builds:** the procedures bullet of 2026-10-22-001 (TMPL-1.4)
**Affects:** `.claude/skills/`, `AGENTS.md` (How I work, Conventions, the governance map, the procedures section), `CONSTITUTION.md` §2.4, `docs/standards/session_handoff_standard_v2.0.md` §4, §5, §7 and §11, `docs/standards/sprint_management_standard_v1.0.md` §1, §5, §6 and §8, `docs/standards/document_production_standard_v1.0.md`, `scripts/skill_scan.py`, `scripts/session_closeout.py` (the kickoff's section 5), `scripts/new_project.py` (the S1 entry and the tracker header), `.pre-commit-config.yaml`, `docs/governance/gate_suite_runbook.md`, `.claude/rules/sprint-documents.md`, `TEMPLATE_GUIDE.md` Step 7, `README.md`

### Context

Decision 2026-10-22-001 makes each procedure a skill whose `SKILL.md` is its one home. `AGENTS.md`
said the opposite in its section "Workflows are portable markdown, not tool skills": a skill was a
per-tool accelerator, never the source of truth. That section was written when a skill meant a
copy in one tool's private folder. A `SKILL.md` committed under `.claude/skills/` is repository
markdown, as a rule under `.claude/rules/` is (decision 2026-10-22-006); what another agent lacks
is a way to find it.

The skills reference, read whole on 2026-10-23 (Claude Code 2.1.308): a skill with `context: fork`
runs as the subagent its `agent:` names, `general-purpose` by default, with the skill's body as
its task. That subagent sees none of the conversation; it loads `AGENTS.md` and a git-status
snapshot (Explore and Plan skip both), not the persona the start hook injected. A fork runs in the
background, with a narrower tool set, unless `background: false`; under `claude -p` it is waited
for either way. `disable-model-invocation: true` takes the description out of Claude's context, and
Claude Code blocks Claude's own call and tells it not to do the steps another way. All silent: a
frontmatter that does not parse loads the skill with no fields, so `context: fork` is lost; a key
Claude Code does not know is ignored; a directory with no `SKILL.md` is no skill.

### Decision

- **A skill is repository markdown and the one home of its procedure.** `AGENTS.md` lists each by
  path; Claude Code runs it by name or by its description, and any other agent opens the file and
  follows the body, the frontmatter being Claude Code's settings. It is never copied into another
  tool's folder. The standard that held the procedure keeps its law and points to the skill.
- **Five skills.** `closeout`, forked, `agent: general-purpose`, `background: false`, so the session
  waits for the kickoff it hands the user. `planning-session` and `document-production` run inline,
  because the first needs the user's confirmation and the second the conversation's content.
  `release` and `pristine-cut` run inline and are the operator's alone (`disable-model-invocation`),
  being one-way doors on GitHub; each refuses outside the template.
- **The forked closeout takes the session's judgement as arguments** (the operator's choice): the
  next persona's slug, then a brief of the next session's tasks, success criteria, reads and open
  questions. Before invoking it the session commits everything durable, as checkpoint discipline
  already requires; the fork refuses an uncommitted tree, reads the rest from git, syncs, scaffolds,
  fills, gates, commits, pushes, watches the run and returns the kickoff.
- **The emergency close moves to `AGENTS.md`**: it is what the main session does when its context is
  critical, and `AGENTS.md` is the file always loaded. The kickoff's section 5, written by the
  scaffold, points to the skill instead of restating the procedure.
- **`scripts/skill_scan.py` keeps the skills honest**, as `gate_runbook_scan.py` keeps the runbook:
  every silent frontmatter failure above is refused; every `pre-commit run` a skill's code names must
  name a hook the config declares, at a stage it declares, with `--all-files`; every script and flag
  must exist; a hook's entry run bare is refused; and `AGENTS.md` must list every skill and no
  missing one. It reads the config with the runbook gate's own reader.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001): the procedures move and a new gate can fail a
  project's own skills.

### Consequences

- TMPL-1.6 decides how the initializer, the updater and the sanitizer own `.claude/skills/`, the
  template-only skills included.
- A project's own skill must be listed in `AGENTS.md` and pass the gate.
- TMPL-1.7 proves a forked closeout end to end.

### Enforcement

`scripts/skill_scan.py` (`frontmatter`, `lint_skill`, `precommit_violations`, `script_violations`,
`scan`) in `skill-scan`, after `skill-scan-selftest`. Taught by [[reference_claude_code_skills]].

### Verification

Fixtures in the skill self-test for every rule, among them an option's value never read as a hook
id and a `SKILL.md` one level too deep; thirty-eight broken variants of the gate, each failing at
least one fixture without crashing (the first draft of one variant changed nothing and passed; it
was rewritten to break the code). On the tree the gate reads five skills and the commands in each.
Live plants in a skill, a hook id and then a stage the config lacks, each failed
`pre-commit run skill-scan --all-files` and a real commit. A grep over the markdown, decision
records and handoff pairs aside, finds each procedure's distinctive command in its skill alone.
`claude -p "/closeout framework-maintainer <brief>"` in a scratch clone ran the skill as a
`general-purpose` subagent whose first command was step 1's `git status --short`; it read step 2
from git and stopped at step 3, whose sync needed an approval `-p` cannot give, the tree untouched.

---

## Decision 2026-10-23-002: The Claude Code paths and the local files are owned by decision; personas adopt through `dev-resources`

**Date:** 2026-10-23
**Made By:** AI (S4), within decisions 2026-10-22-001 and 2026-10-22-005; reported to the operator
at the S4 handover
**Status:** APPROVED; SUPERSEDED (bullets 1, 4 and 5) by 2026-10-23-003
**Builds:** the ownership consequence of 2026-10-22-001 and the adoption consequence of 2026-10-22-005 (TMPL-1.6)
**Affects:** `scripts/new_project.py` (`LOCAL_STATE`, the self-test), `scripts/template_update.py` (`KEEP`, the docstring, the self-test), `scripts/sanitize_template.py` (`LOCAL_STATE`, the self-test), `.gitignore`

### Context

Decision 2026-10-22-001 left the initializer, the updater and the sanitizer to learn the new
paths: `.claude/agents/`, `.claude/skills/`, `.claude/rules/`, `.claude/settings.json`, the
journal and the working notes. TMPL-1.3 renamed the registry from `docs/personas/` in three lists
with no fixture to say they agree. Decision 2026-10-22-005 left a project's own `docs/personas/`
to be carried into `.claude/agents/` when it adopts `v2.0.0`.

Reading the tree for this found `.claude/settings.local.json`, one operator's permissions, ignored
on the template's machine only by that operator's global excludes file: the repository's
`.gitignore` lacked it, so on any other machine it could be committed, and a release would then
have carried one person's grants into every project. `git check-ignore` reads the global file too,
so the journal's own ignore check could not have seen the gap; with `-c core.excludesFile=` it can.

### Decision

- **The registry, `.claude/agents/`, is kept**, being the resources sync's alone: preserved at
  birth, kept by the sanitizer, never written by a release. It is one path in five places (the
  closeout gate reads it, the sync writes it, the initializer, the sanitizer and the updater keep
  it), and a fixture holds all five to the same string.
- **`.claude/skills/`, `.claude/rules/` and `.claude/settings.json` are merged three-way**: the
  template's, which a project may edit and extend. A skill or rule the project added is in
  neither release and never touched. The initializer and the sanitizer leave them as shipped. The
  template-only skills stay in a project: each says it runs only in the template and stops
  elsewhere, and neither's description enters Claude's context.
- **The journal, the notes and `.claude/settings.local.json` are the running session's**
  (`new_project.LOCAL_STATE`): gitignored by the repository's own `.gitignore`, checked with the
  global excludes off; never written or removed by the initializer or the sanitizer, which may run
  from inside a session; kept by the updater.
- **A project's `docs/personas/` reaches `.claude/agents/` through `dev-resources`**, in this
  order: (1) before adopting, the project publishes every persona `dev-resources` lacks with its
  own `v1.0.0` sync; (2) TMPL-2.4 ports `dev-resources`' frozen `docs/personas/` into
  `.claude/agents/` before any project adopts; (3) `template_update.py` deletes the template's
  unedited `docs/personas/` copies, now an ordinary three-way path the target release removed, and
  reports the edited ones; (4) the project's `v2.0.0` `resources_sync.py --apply` writes
  `.claude/agents/`, which the suite needs before it can pass, since the current kickoff's persona
  is looked for there; (5) the project removes what is left of `docs/personas/` once every slug in
  it is in `.claude/agents/` at an equal or higher version. A persona left behind cannot pass
  silently: the closeout gate refuses a kickoff whose persona `.claude/agents/` lacks.
- **Not converted in the project**, because the registry grows only through `--publish` (decision
  2026-09-23-007) and a conversion per project would make copies outside it; the conversion met
  YAML traps when it was done once by hand (decision 2026-10-22-005), and one conversion in
  `dev-resources` serves every project.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001).

### Consequences

- TMPL-2.4 runs the adoption in that order on a scratch project first. The updater's own suite
  run after `--apply` fails until step 4 has run; TMPL-2.4 judges whether the updater should say so.
- A machine whose global excludes already cover a local file no longer hides a gap in the
  repository's own `.gitignore`.

### Verification

Fixtures: the initializer's self-test gained five, the updater's four, the sanitizer's one.
Nineteen broken variants across the three scripts, the sync's and the gate's registry path and
`.gitignore`, each failing at least one fixture and none crashing; one was first written so that
it never applied, and was rewritten. On the real tree every tracked `.claude/` path and the three
local files classify as decided: ten three-way, eight kept. Before the `.gitignore` line,
`git -c core.excludesFile= check-ignore` reported `.claude/settings.local.json` not ignored, while
the plain command reported it ignored.

### Enforcement

`scripts/new_project.py` (`LOCAL_STATE`, `--self-test`), `scripts/template_update.py` (`KEEP`,
`--self-test`: the decided paths, the registry across five places, the initializer's agreement),
`scripts/sanitize_template.py` (`LOCAL_STATE`, `--self-test`). Taught by [[reference_template_update]].

---

## Decision 2026-10-23-003: Personas ship as a library in the template, activated per project at its first session

**Amended 2026-10-23 (S5): the four open questions, answered by the operator.**

- **The full team ships in `v2.0.0`.** The roles across the software development lifecycle, data
  science, document management, writing including technical writing, and quality control are
  designed with the operator and written into the library before the release (TMPL-1.9). TMPL-3
  keeps the orchestration, the gated handoffs and the review triggers that build on them.
- **`dev-resources` is retired.** `v2.0.0` carries no sync: `scripts/resources_sync.py`, its
  closeout step and the closeout's unpublished-persona rule go, and the shared knowledge entries
  become the template's own (TMPL-1.10). `dev-resources` keeps serving the projects still on
  `v1.0.0` and is archived once all three have adopted (TMPL-2.4).
- **A project's own personas stay in the project.** The library holds only the personas built and
  released in the template; nothing travels from a project to the template.
- **The updater converts a `v1.0.0` project's `docs/personas/`** into agent files in
  `.claude/agents/`, every one, and removes the old folder (TMPL-1.10). Chosen over a judgement step
  at adoption, with the cost named: every converted persona becomes a live subagent, and the project
  deactivates what it does not use. The conversion is proved against the real `v1.0.0` persona
  files, whose conversion by hand under decision 2026-10-22-005 is the expected output.
- The library's folder is `personas/` at the repository's root, each file in the agent-file shape,
  so activation is a copy (the AI's choice of mechanics). The mechanism is TMPL-1.8.

**Date:** 2026-10-23; amended 2026-10-23
**Made By:** Chair (S4, after its closeout): the library in the template and activation at the first
session, approved as proposed; the mechanics by the AI, to be settled in the build
**Status:** APPROVED
**Supersedes:** 2026-09-23-007; 2026-09-23-002 (personas and shared knowledge in `dev-resources`);
2026-10-22-005 (`dev-resources` holding the registry); 2026-10-23-002 (its first, fourth and fifth
bullets)
**Affects:** `personas/`, `.claude/agents/`, `.claude/skills/team-selection/`, `.claude/skills/closeout/`,
`scripts/session_closeout.py`, `scripts/resources_sync.py` (removed), `.resources-version` (removed),
`scripts/new_project.py`, `scripts/template_update.py`, `scripts/sanitize_template.py`,
`.pre-commit-config.yaml`, `.pre-commit-hooks.yaml`, `AGENTS.md`, `CONSTITUTION.md`, `README.md`,
`TEMPLATE_GUIDE.md`, `docs/standards/session_handoff_standard_v2.0.md`,
`docs/governance/gate_suite_runbook.md`, `.claude/rules/knowledge-entries.md`

### Context

Since decision 2026-09-23-002 the personas have lived in `dev-resources`, a second repository, and
reached each project through a sync that judges versions and grows only through `--publish`
(decision 2026-09-23-007). Decision 2026-10-22-005 moved them into `.claude/agents/` and left
`dev-resources` holding two trees until the three projects adopt `v2.0.0`. The operator wants the
public template itself to ship a base library: a full team covering the software development
lifecycle, data science, document management, writing including technical writing, and quality
control across all three.

Every file in `.claude/agents/` is a live subagent: its description is listed in every session's
context, and Claude may delegate to it unprompted. A full team in that folder would cost context in
every session of every project and make delegation unpredictable.

### Decision

- **The template ships a persona library**, outside `.claude/agents/` and inactive, versioned by
  template releases. Adding a persona to it forces no project to act, so it is a MINOR change: the
  library is how the template grows to cover new use cases without loading every project.
- **`.claude/agents/` is a project's roster**: only the personas that project activated. The
  session's persona, the kickoff's persona and a delegated subagent all come from the roster.
- **At a project's first session a skill builds the roster:** it asks the operator which
  specializations the project needs, scans the library, recommends personas, drafts new ones for
  any gap, and copies the chosen ones into `.claude/agents/`. More can be activated later the same way.
- **The gates follow:** the closeout keeps refusing a kickoff whose persona the roster lacks; a
  roster persona taken from the library is held to a library version, and a newer library version
  is reported. The append-only rule of decision 2026-09-23-006 holds in both places.
- **Part of `v2.0.0`** (MAJOR, decision 2026-10-22-001), built as TMPL-1.8 before TMPL-1.7 proves
  the substrate, since it changes the birth that proof observes.

### Open, to settle with the operator at the start of TMPL-1.8

- How much of the library ships in `v2.0.0`. Recommended: the mechanism and a starter set, the full
  team designed in TMPL-3.1's design session and shipped as MINOR releases.
- Whether `dev-resources` is retired, its few shared knowledge entries folded into the template,
  or kept for knowledge alone.
- Whether a persona a project drafts for itself can be proposed back to the library, and how.
- How a `v1.0.0` project's `docs/personas/` reaches its roster when it adopts `v2.0.0`.

### Supersession

Marked on both sides by TMPL-1.8, with the code: decisions 2026-09-23-007 (the sync, whole),
2026-09-23-002 (personas and shared knowledge in `dev-resources`; its append-only rule and the
published hooks stand), 2026-10-22-005 (`dev-resources` holding the registry; the agent-file shape
and the persona from the start hook stand) and 2026-10-23-002 (its first, fourth and fifth bullets,
the registry as the sync's and the adoption through `dev-resources`).

### Consequences

- TMPL-1.8 is opened; TMPL-1.7 depends on it.
- TMPL-2.2's technical writer becomes a library persona; TMPL-2.4's port of `dev-resources`' frozen
  tree is replaced by whatever the adoption question settles; TMPL-3.1's design session designs the
  full team as library personas.

### Verification

Fixtures: the closeout gate's library rules, the start hook's roster notes, and the initializer's,
the updater's and the sanitizer's checks on the roster and the library. Twenty broken variants
across those five scripts, each failing at least one fixture without crashing; three were first
written wrong (one changed nothing, one targeted a line already rewritten, one crashed instead of
failing) and were rewritten. Live plants in the real tree: a roster copy edited at the same version
failed `session-closeout-check` as `library-drift` and was refused by a real commit; one bumped ahead
of the library failed as `library-fork`, and was refused too. The library bumped past the roster
passed and printed nothing, because pre-commit hides a passing hook's output; that is why the start
hook now names such a persona itself. A scratch birth from the committed template:
`new_project.py --apply` exit 0 with the suite green, the template's roster removed and the library
whole, `session-verify` exit 0 at S1, and a `claude -p` session whose init event listed only the
built-in agents, with the `team-selection` skill available.

### Enforcement

`scripts/session_closeout.py` (`LIBRARY`, `library_state`, `NOTE_RULES`, `library_findings`) in
`session-closeout-check`; `scripts/session_start.py` (`roster_lines`); `scripts/new_project.py`
(`CLEAR_GLOBS`), `scripts/sanitize_template.py` (`NEVER_RESET`) and `scripts/template_update.py`
(`KEEP`), cross-checked in the updater's self-test; `.claude/skills/team-selection/SKILL.md`, held by
`skill-scan`. Taught by [[reference_session_closeout]], [[reference_claude_code_agents_md]],
[[reference_resources_sync]] and [[reference_template_update]].

---

## Decision 2026-10-23-004: The persona library's team

**Date:** 2026-10-23
**Made By:** Chair (S5): the team approved, with business intelligence and reporting roles and the
missing game development roles added at the Chair's request; the role definitions by the AI
**Status:** APPROVED
**Builds:** the full-team answer in decision 2026-10-23-003 (TMPL-1.9)
**Affects:** `personas/`, `.claude/skills/team-selection/SKILL.md`

### Context

Decision 2026-10-23-003, as amended, ships the full team in `v2.0.0`: personas across the software
development lifecycle, data science, document management, writing including technical writing, and
quality control for all three. The library held five personas, three of them built for one project
each. The roles were put to the operator as a table by area.

### Decision

- **The team, by area.** Software lifecycle: `product-manager`, `business-analyst`,
  `solution-architect`, `software-engineer`, `frontend-engineer`, `ux-designer`, `devops-engineer`,
  `security-engineer`, `delivery-manager`. Data science, business intelligence and reporting:
  `data-engineer`, `analytics-engineer`, `bi-developer`, `reporting-analyst`, `data-analyst`,
  `data-scientist`, `ml-engineer`, beside `data-platform-engineer` for the Microsoft stack. Document
  management: `document-controller`, `information-architect`. Writing: `technical-writer`, `editor`,
  `business-writer`. Quality control: `qa-engineer`, `data-quality-engineer`, `document-reviewer`.
  Game development: `game-designer`, `game-artist`, `game-audio-designer`, `narrative-designer`,
  `game-producer`, `game-qa-tester`, beside `game-engine-developer` and `game-ui-ux-designer`.
  `framework-maintainer` and `generative-video-engineer` stay.
- **One shape and shared habits.** Each persona is an agent file at version 1: a description that
  says what the role does, so Claude can delegate to it once a project activates it; expertise and
  insists_on as lists of strings; and a prompt that addresses the agent as the role. Each reads its
  story's Required Standards first and calls nothing done on an unobserved check; a role that
  touches data keeps raw data out of the session.
- **A code reviewer is left to TMPL-4**, whose coding-standard design defines the reviewer and
  auditor briefs.
- Adding a persona to the library later is MINOR (decision 2026-10-23-003); these ship with
  `v2.0.0`.

### Verification

Each persona passes `session-closeout-check`'s persona lint in the library: YAML frontmatter that
parses, `name` equal to the filename, the required keys, string lists, and a changelog item for
version 1. A plant that unquoted one list item holding `: ` was refused as `list`.

### Enforcement

`scripts/session_closeout.py` (`library_findings`, `lint_persona`) in `session-closeout-check`.

---

## Decision 2026-10-23-005: Adoption from `v1.0.0` converts the personas and settles what the sync left

**Date:** 2026-10-23
**Made By:** AI (S6), within decision 2026-10-23-003, whose amendment made the conversion the
operator's choice; reported to the operator at the S6 handover
**Status:** APPROVED
**Supersedes:** 2026-09-23-008
**Builds:** the adoption bullet of 2026-10-23-003's amendment (TMPL-1.10)
**Affects:** `scripts/template_update.py` (`classify`, `ROSTER`, `LIBRARY`, `LEGACY_PERSONAS`,
`RETIRED`, `v1_persona`, `yaml_scalar`, `agent_file`, `marked`, `unmarked`, `adoption_steps`,
`plan_path`, `build_plan`, the self-test), `.pre-commit-config.yaml` (`template-update-selftest`),
`TEMPLATE_GUIDE.md` Step 9, `docs/governance/gate_suite_runbook.md`

### Context

Decision 2026-10-23-003, as amended, has the updater convert a `v1.0.0` project's `docs/personas/`
into agent files in its roster and remove the folder, and settle what the retired sync left behind:
the knowledge entries marked `source: dev-resources` and the `.resources-version` stamp. Until now
the updater kept a marked entry and the stamp untouched (`resource_owned`, `KEEP`), and treated
`docs/personas/` as an ordinary path the release removed, so a project's own persona would have
stayed in the old folder, read by nothing.

The three projects on `v1.0.0` each hold `docs/personas/`, one persona in it the project's own, and
the marked `reference_macos_toolchain.md`, equal to the `v1.0.0` copy; two hold a stamp. One real
persona wraps an Expertise bullet onto a second line, which the hand conversion of decision
2026-10-22-005 joined with a space. And during adoption the target's updater runs beside the
project's `v1.0.0` sibling scripts, whose persona lint knows only the old shape.

### Decision

- **Adoption is judged by what the project holds**, never by either release, so a project that
  skips releases adopts the same way. A fourth class, `adopt`, covers `docs/personas/` and
  `.resources-version`; the release loop leaves them to `adoption_steps`.
- **Every persona converts exactly or not at all.** The file is read as `v1.0.0` read it: flat
  `key: value` frontmatter with exactly `name`, `slug`, `description` and `version`, then a title and
  the four sections. A bullet wrapped onto the next line is one item, as Markdown reads it. The agent
  file takes the library's shape (decision 2026-10-22-005): `name` the slug, an item plain where YAML
  reads it back unchanged and double-quoted otherwise, the body the Invocation; it is refused unless
  its frontmatter parses back to exactly the values read. Anything the shape has no place for
  (another key, prose outside the sections, a line after a blank one in a list) is a conflict, left
  in place and named, never dropped. A roster file already holding the slug with other text is a
  conflict; with the same text, only the old file goes. The emptied folder is removed.
- **The converter reads nothing from the sibling scripts.** The suite the updater runs after
  `--apply`, by then the release's, judges the roster with the current persona lint and the library
  rule; the dry run already says, per persona, whether the library holds the same text.
- **The stamp is removed**: nothing in `v2.0.0` reads it.
- **A marked entry is merged three-way like any other**, the declaration being one more line, so a
  copy equal to `v1.0.0`'s takes the template's unmarked copy. A marked entry that no release step
  writes loses the declaration and is the project's own. `resource_owned` and the keep it drove go,
  and with them the resource-entry class of decision 2026-09-23-008, superseded whole: with no sync,
  no entry is anyone's copy.
- `--keep <path>` leaves any of these as it is.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001).

### Consequences

- The updater writes the roster in one case, the conversion; the rule that it never writes the
  roster otherwise stands.
- Adoption needs PyYAML in the `python3` that runs the updater; with `docs/personas/` present and no
  PyYAML it exits 2 naming the install. The self-test hook declares it.
- Each of the three projects conflicts on `.gitignore`, where the project and `v2.0.0` both append at
  the end of the file. It is resolved by hand, keeping both blocks, then `--keep .gitignore`; whether
  the updater should union-merge `.gitignore` is put to the operator for TMPL-2.4.

### Verification

Fixtures: the updater's self-test lost the resource-entry fixture and gained sixteen: the conversion of a fixture persona to exact bytes
(a description and two items holding `: `, one opening with a backtick, one reading as a bool, one
wrapped, a fenced `## ` line in the Invocation), the output passing the state gate's persona lint,
CRLF, fourteen refusals, the read-back check through a broken scalar writer, the marker in the
frontmatter only, unmarking that keeps the body's mention, a marked entry merged as content, and
the adoption steps (convert and delete, the library note, a roster already equal, a roster holding
other text, a file that is no persona, the stamp retired, `--keep`). Twenty-eight broken variants of
the converter and the adoption pass, each failing at least one fixture without crashing. Two first
crashed the self-test instead of failing a fixture; the fixture rewritten to stop the crash then let
a third variant through, because it no longer reached the parse error that variant breaks; both
were rewritten. Without PyYAML declared, the hook failed on the first conversion fixture.

On the real files: the two `v1.0.0` personas, the five in `dev-resources`' frozen tree and every
persona the three projects hold, eighteen files, each converted to a file that passes the persona
lint, and each of the library's equals its library copy byte for byte; the one project persona
converts and lints. The first run refused the wrapped bullet, and the hand conversion, the
expected output, showed the fixture had encoded the wrong rule. Scratch clones of the three projects
adopted a scratch `v2.0.0` built from this tree: each converted every persona, the dry run naming
each library persona's text as the same, removed `docs/personas/`, removed the stamp where one
existed, took the template's unmarked macOS entry, and conflicted on `.gitignore` alone. Resolved by
hand and re-run with `--keep .gitignore`, each wrote the stamp and passed the whole suite on its
first run, the state gate included.

### Enforcement

`scripts/template_update.py --self-test` in `template-update-selftest`; the state gate's persona
lint and library rule on the roster after adoption. Taught by [[reference_template_update]] and
[[reference_resources_sync]].

---

## Decision 2026-10-23-006: What the substrate's live proof found, and the two closeout fixes

**Date:** 2026-10-23
**Made By:** AI (S6), within decisions 2026-09-21-001 and 2026-10-23-001; reported to the operator
at the S6 handover
**Status:** APPROVED
**Builds:** TMPL-1.7, the proof of decision 2026-10-22-001's substrate
**Affects:** `scripts/session_closeout.py` (`handoff_skeleton`, the self-test),
`.claude/skills/closeout/SKILL.md` (step 2)

### Context

TMPL-1.7 ran the substrate end to end on a scratch project born from the committed template: the
operator opened an interactive session in the fresh clone, accepted the trust dialog, ran the
team-selection skill, compacted, and ran the forked closeout ([[reference_claude_code_substrate]]).
Everything ran as designed. The closeout's fork reported two things the procedure did not settle:

- Its step 2 finds the session's range from the commit `checkpoint: closeout S<N-1>`. A project's S1
  has none, so the fork chose a base itself.
- The scaffold wrote handoff sections 3, 4 and 5 as `- None.`, not as tokens. The session had logged
  a decision; the fork replaced section 4's `- None.` because the skill told it to, but nothing
  required it: a closeout that skipped the step would have passed the gate saying no decision was
  logged.

### Decision

- **The scaffold leaves every judged section of the handoff as a `{{FILL}}` token**, sections 3 to
  5 included, so `unfilled-token` refuses the pair until each is written, `- None.` where there is
  nothing. A written rule in the skill becomes a control in the gate.
- **S1's range starts at the repository's first commit** (`git rev-list --max-parents=0 HEAD`), which
  in a project made with `gh repo create --template` is the template's tree.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001).

### Consequences

- Every closeout writes three more lines; a session with nothing in progress, no decision and no
  blocker writes `- None.` three times.
- Not observed, and carried: `disableWorkflows` in a live session (no keyword that would trigger a
  workflow is named in this repository), and the `gates` watch on a scratch project, whose origin was
  a local bare repository by the operator's choice; every template closeout watches its run.

### Verification

The closeout self-test gained a fixture that every handoff section after the first read holds a
token; reverting any one of sections 3, 4 or 5 to `- None.` failed it, without crashing. The fixture
for the unfilled scaffold now expects `decision-id` beside `unfilled-token`, since section 4's token
is no decision ID either. The probe's observations are in [[reference_claude_code_substrate]].

### Enforcement

`scripts/session_closeout.py` (`handoff_skeleton`, `lint_handoff`) in `session-closeout-selftest`,
`session-closeout-check` and `session-closeout`; the closeout skill's step 2, held by `skill-scan`.
Taught by [[reference_claude_code_substrate]] and [[reference_session_closeout]].

---

## Decision 2026-10-23-007: The updater merges `.gitignore` by union

**Date:** 2026-10-23
**Made By:** Chair (S6), approving the AI's recommendation
**Status:** APPROVED
**Builds:** the `.gitignore` consequence of 2026-10-23-005 (TMPL-2.5)
**Affects:** `scripts/template_update.py` (`three_way`, the union path, the self-test),
`TEMPLATE_GUIDE.md` Step 9, `docs/orchestration/knowledge/reference_template_update.md`

### Context

The scratch adoptions of all three projects conflicted on `.gitignore` and nowhere else among the
files both sides edit: each project appended its own ignores at the end of the file, and `v2.0.0`
appends the journal, the notes and `.claude/settings.local.json` at the same place. Resolved by
hand, the answer was the same each time: keep both blocks.

### Decision

- **`.gitignore` is merged with `git merge-file --union`**: where both sides changed the same place,
  both sides' lines are kept, the project's first. It is the reason the knowledge index and the
  framework decisions already have keyed merges: both sides add at the same place, so a line merge
  conflicts every time. Every other three-way path still conflicts.
- The dry run names the path as a union merge, so the operator reads it in `git diff` before the
  commit. The one order that matters in an ignore file is a `!` line after the pattern it reverses;
  the template's lines are exact paths no project un-ignores.
- **Rejected:** the template's ignores in nested `.gitignore` files. The journal and the notes live
  under `sprint/`, which the updater never writes, so a `v1.0.0` project would never receive the
  file; and it settles only this instance.
- Part of `v2.0.0`, and in place before the release, since adoption runs the target's updater.

### Verification and enforcement

To be built in TMPL-2.5: fixtures for appends at the end kept on both sides, a same-line change on
both sides kept twice, and another path still conflicting, each proved against a broken variant; a
scratch adoption of the three projects with no `.gitignore` conflict.

---

## Decision 2026-10-23-008: A project launches through `/project-launch`

**Amended 2026-10-23 (TMPL-5.4, the Chair, decision 2026-10-23-024):** before planning, a stage's end
is a session boundary taken by ending the conversation, not by a closeout: no kickoff can cite a
story until planning writes the first, and the next conversation is still S1. The first closeout
comes after planning and names the next stage's persona.

**Date:** 2026-10-23
**Made By:** Chair (S6): the skill, its stages and the chair's control of each stage; the
refinements by the AI, approved by the Chair; the mechanics left to the build
**Status:** APPROVED
**Builds:** opens epic TMPL-5
**Affects:** `.claude/skills/project-launch/` (new), templates for `docs/prd/` and
`docs/architecture/`, `.claude/skills/team-selection/SKILL.md`, `.claude/skills/planning-session/SKILL.md`,
`scripts/new_project.py` (the S1 entry's next steps), `scripts/session_closeout.py` (the approval
gate), `AGENTS.md` (the skills table), `TEMPLATE_GUIDE.md`

### Context

The planning-session skill will not start without an approved PRD in `docs/prd/` and an approved
architecture in `docs/architecture/`. Both folders ship empty, no template or step produces either,
and a project's S1 entry lists team selection and then planning. Each project so far improvised its
first sessions. The Chair proposed a launch skill: three questions to the Chair when there is no PRD,
or a summary of the PRD when there is; then a product manager who interviews the Chair until it can
write the PRD for approval; then the project's next stages.

### Decision

- **One command, `/project-launch`**, which the Chair runs at a project's first session and again
  whenever a stage needs it. Not "kickoff": that word already names each session's prompt.
- **Five stages, in order.**
  - **Intake.** With no PRD in `docs/prd/`, the Chair answers three questions: the purpose of the
    project; the skills and expertise it needs; what it should accomplish. With one, the skill
    summarizes it against the same three questions, lists what the PRD template asks for and the PRD
    lacks, and the Chair confirms or redirects.
  - **Team.** The team-selection skill, with the second answer as its input, so the Chair is asked
    once: it activates `product-manager`, `solution-architect` and `delivery-manager` beside the
    specialists the work needs, and the Chair names the lead.
  - **PRD.** The main session takes the product manager's prompt and interviews the Chair, opening
    with: "Describe in as much detail as you can what your goals are for this project and what you
    want produced at project completion." The main session, because a subagent can neither ask the
    Chair a question nor see the conversation. The interview runs until each section of the PRD
    template is filled or names an open question, the draft saved in `docs/prd/` as it grows; then
    the Chair reviews and approves. With a PRD already there, the interview covers its gaps only.
  - **Architecture.** The same pattern led by `solution-architect`, from the approved PRD, into
    `docs/architecture/`.
  - **Planning.** The planning-session skill, led by `delivery-manager`.
- **The Chair steers every stage.** Each stage opens with what it will produce and the commands:
  `/project-launch pause` saves the draft and stops, to resume where it stopped;
  `/project-launch skip <stage>` passes over it, the Chair's reason logged as a decision;
  `/project-launch <stage>` returns to a stage at any later time, to resume, review or revise it;
  `/project-launch status` shows where each stage stands. A bare `/project-launch` resumes at the
  first unfinished stage. Another agent runs the same words as instructions.
- **Revising an approved document reopens it as a new version**, approved again, and flags each
  later stage built on the old one: the architecture records the PRD version it was built from, and
  the plan the architecture's. A revision never silently strands the work downstream (decision
  2026-10-22-002's version logs).
- **The state lives in the documents.** Each one's status and version, and a skip's decision, are
  what `status` reads; there is no separate launch file to drift from them.
- **Approval is on record**: the document's status becomes approved with a version-log row, and a
  decision is logged. A gate makes it binding: in a project, a real epic needs an approved PRD and an
  approved architecture, or a logged skip of either.
- **A stage's end is a session boundary the Chair may take**: closing out there names the next
  stage's persona, so each stage starts with fresh context.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001); TMPL-2.4's release waits for it.

### Open, to settle in the build

- The PRD template's sections. Proposed: purpose; users and stakeholders; goals with measurable
  success criteria; what is produced at completion; scope and non-goals; numbered requirements
  (`FR-1` …), which the tracker's PRD Ref cites; constraints (profile, platform, data sensitivity,
  timeline); assumptions; risks; open questions. The architecture template's likewise.
- The documents' frontmatter, in the `authority:` format TMPL-2.1 builds.
- Whether the skill is the Chair's alone (`disable-model-invocation`), since every stage needs the
  Chair present.

### Consequences

- Epic TMPL-5 is opened; TMPL-2.4 depends on it.
- A new project's S1 entry names `/project-launch` as its one next step. A project on an earlier
  release receives the skill at adoption; one that has a PRD takes the intake's summary path.

---

## Decision 2026-10-23-009: The README is the operator's front page, and a gate keeps its catalog whole

**Date:** 2026-10-23
**Made By:** Chair (S6): a root README that walks the user step by step through launching and using
the repository, then catalogs its features, skills and commands; the shape and the gate by the AI
**Status:** APPROVED
**Builds:** TMPL-5.5
**Affects:** `README.md`, `TEMPLATE_GUIDE.md`, `scripts/skill_scan.py`, `docs/governance/gate_suite_runbook.md`

### Context

`README.md` says how to create a project in two commands and what each path holds. It does not say
what to do next: open Claude Code, accept the trust dialog, launch the project, paste each kickoff,
close out, take a release. Nor does it list the commands a user types. The skills are listed in
`AGENTS.md` for agents, and the hooks in the gate runbook. `TEMPLATE_GUIDE.md` still opens with
by-hand token replacement that the initializer has done since before `v1.0.0`.

### Decision

- **The README opens with a walkthrough**, in the order a user meets it: create the repository and
  initialize it; install the hooks; open Claude Code in the clone and accept the trust dialog; run
  `/project-launch`; then the session loop (paste the kickoff, work, `/closeout`, paste the next
  kickoff); and taking a newer release. Each step says what to type and what the user should see.
- **Then a catalog**: every slash command (each skill) with what it does and when to use it; the
  operator's scripts (`new_project.py`, `template_update.py`) with their commands; the session hooks
  and what each does for the user; the gates by link to the gate runbook, their one home, never
  copied.
- **One home per fact.** The walkthrough links to `TEMPLATE_GUIDE.md` for detail rather than repeat
  it, and the guide's steps the initializer already performs are removed, so the two cannot disagree.
- **A gate keeps the catalog whole**: `skill-scan` refuses a skill the README's catalog does not
  name, as it already refuses one missing from `AGENTS.md`.
- **The live proof of the launch follows the README as written** (TMPL-5.4), so the walkthrough is
  tested by use, not by reading.
- Ships in `v2.0.0`, after `/project-launch` exists, since the walkthrough centres on it.

### Verification and enforcement

To be built in TMPL-5.5: `skill-scan` fixtures for a skill missing from the README, proved against a
broken variant; the walkthrough exercised in TMPL-5.4.

---

## Decision 2026-10-23-010: The authority gate as built

**Date:** 2026-10-23
**Made By:** Chair (S7): how a row is told to be a fact, and which decisions must declare their
impact; the rest by the AI within decision 2026-10-22-002, reported at the S7 handover
**Status:** APPROVED
**Builds:** TMPL-2.1, the gate of decision 2026-10-22-002
**Affects:** `scripts/doc_authority_scan.py` (new), `scripts/session_closeout.py` (`Story` carries
its row), `.pre-commit-config.yaml` (two hooks after `kb-freshness-scan`),
`docs/governance/gate_suite_runbook.md` (their sections), `.claude/rules/decision-logs.md` (the
`**Affects:**` line), `sprint/decision-log.md` (the example body), `sprint/story-tracker.md`
(TMPL-2.3 retires the authority matrix)

### Context

Decision 2026-10-22-002 fixed the gate's shape: `authority:` frontmatter and a version log on each
source of truth, `**Affects:**` on every decision, a version-log row or an open story and nothing
else, the fact marker, the stamp verified against git. The build had to settle what each of those
means to a script. The gate cannot see who wrote a row; "every decision from this one forward" needs
a boundary a project can compute; and a derived project's history, squashed at birth, holds none
of the template's commits, so a template row's hash cannot be verified there.

### Decision

- **The frontmatter is the registry.** Any markdown file git would commit whose frontmatter has a
  top-level `authority:` is an authority, parsed with YAML: the scope a non-empty string,
  `implements:` a list of decision IDs, `verified:` an unquoted ISO date. A block that claims
  authority and does not parse fails; it is never skipped. `implements:` and `verified:` are judged
  by the freshness rule `kb_freshness_scan.py` applies to a knowledge entry.
- **The version log** is the document's last H2, `## Version log`, outside fenced code: columns
  Version, Date, Decision, Summary, Commit; newest row first, versions strictly descending (`3`,
  `2.1`), dates never rising; every row cites at least one indexed decision.
- **A row is a fact or a story's change (Chair).** Its summary opens `fact:` and states the fact (a
  code span or a number: a value, a name, a path, a count), or cites a tracker story whose row cites
  the row's decision. The technical writer's drain (TMPL-2.2) and a story whose own work is the
  document take the second form, so a structural change is evidence of the queue, not a claim.
- **`**Affects:**` from decisions dated 2026-10-22 (Chair)**, the date of decision 2026-10-22-002,
  read from the index's Date cell in either log, so any ID convention works. Older decisions read as
  `none`. A document is named as a code span of its path; a named path that is no authority is not
  judged.
- **Recorded or queued, as built.** For a decision whose `**Affects:**` names an authority: a row
  of that document's log cites the decision, or a story not Done cites the decision and contains the
  path. A decision ID is cited only where it is not part of a longer ID.
- **The stamp.** `pending` is allowed on any row. A stored hash must be a prefix, at least seven
  characters, of the first commit (following renames) whose copy of the document holds that version;
  matching by version rather than row text is what lets `--stamp` edit the row it stamps. `--stamp`
  writes seven characters for each committed `pending` row; `--history <doc>` prints stored beside
  derived. A shallow clone exits 2, since its history ends early (the CI checkout already fetches
  the full history for the version gate).
- **The template's rows are verified in the template.** In a project, a row citing only framework
  decisions was written by the template; the gate does not verify its hash and `--stamp` leaves it.
  A row citing a project decision is verified in the project. *Amended 2026-10-23 by decision
  2026-10-23-015:* nor is such a row held to its marker there, nor a framework decision to its
  `**Affects:**` line or its record.
- **One scope, one authority.** Two documents claiming one scope, compared without case or spacing,
  fail: the escalation rule of `sprint/recovery/AUTHORITY_MATRIX.md` made mechanical. The matrix, a
  second registry kept by hand and already stale on personas, is retired in TMPL-2.3.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-002).

### Consequences

- Until TMPL-2.3 marks the standards and the gate runbook, the template's registry is empty: the gate
  holds the decisions' `**Affects:**` lines and nothing else. Observed on the real tree at S7.
- Marking a document makes every decision from the cutoff whose `**Affects:**` names it due at once:
  the first rows cite them, or stories queue them. That is the real content decision 2026-10-22-002
  asked the gate to be proved against.
- A project decision dated from the cutoff needs the line at adoption. The three projects had none
  on 2026-10-23.

### Verification

Fifty-three fixtures in the self-test, each rule with a passing and a failing case, a fixture that
raises reported as a failure. Forty-five broken variants of the script, one per rule and reader, each
failed at least one fixture without a crash. On a scratch clone of the template, a marked copy of the
document-control standard: `--stamp` left an uncommitted row pending and then wrote the commit that
introduced it; `--history` derived both rows across a rename; a hash swapped to the next row's was
refused; a shallow clone exited 2; with no row citing decision 2026-10-22-002, whose `**Affects:**`
names the document, the gate reported it unrecorded.

### Enforcement

`doc-authority-selftest` and `doc-authority-scan` in `.pre-commit-config.yaml`, after
`kb-freshness-scan`; [[reference_doc_authority]].

---

## Decision 2026-10-23-011: The first authorities

**Date:** 2026-10-23
**Made By:** AI (S7), within decisions 2026-10-22-002 and 2026-10-23-010, on the story the Chair
chose; reported at the S7 handover
**Status:** APPROVED
**Builds:** TMPL-2.3
**Affects:** `docs/governance/doc_control_standard.md` (rewritten around the gate),
`docs/governance/gate_suite_runbook.md` (marked; the preamble's exception; the updater's section),
`docs/standards/session_handoff_standard_v2.0.md`, `docs/standards/sprint_management_standard_v1.0.md`
(§2 and §12), `docs/standards/secrets_management_standard_v1.0.md`,
`docs/standards/document_production_standard_v1.0.md` (each marked, its changelog replaced),
`scripts/gate_runbook_scan.py` (the closing version log), `sprint/recovery/AUTHORITY_MATRIX.md`
(removed), `sprint/recovery/README.md`, `sprint/story-tracker.md` (TMPL-5.5 names the runbook),
`docs/orchestration/knowledge/reference_gate_runbook.md`, `docs/orchestration/knowledge/reference_doc_authority.md`

### Context

Decision 2026-10-22-002 marks the standards and the gate runbook first, so the gate has real
content to prove against. Each standard already carried a hand-kept `**Version:**` line and a
changelog table, the stored value without a gate that the decision forbids: the session-handoff
standard's table had eight rows since 2026-09-21, every one at version 2.0. Marking a document makes
every decision from 2026-10-22 whose `**Affects:**` names it due at once.

### Decision

- **Six authorities**: the four standards in `docs/standards/`, the document-control standard and
  the gate-suite runbook, each with a scope of its own and `implements:` the decisions it carries.
- **Each log starts at marking**, at the version the document states (2.0, 1.0), 1.0 where it
  stated none. The first row cites this decision, decision 2026-10-22-002 and every decision from
  the cutoff whose `**Affects:**` names the document and is built, the document having been read
  against each; its summary cites TMPL-2.3. A named change not yet made is queued instead: decision
  2026-10-23-009's change to the runbook's `skill-scan` section, by TMPL-5.5's row naming the path.
- **The changelog tables and `**Version:**` lines are removed**, not converted: their rows cite no
  decision in a form the gate reads, their dates were placeholders or stale, and their history is in
  git and in the decisions. The version is the log's newest row.
- **File names keep their version** (`_v2.0`, `_v1.0`): every tracker, a project's included, cites
  the standards by file name in Required Standards, and the updater never writes `sprint/`.
- **The runbook's closing `## Version log` names no hook**: `gate_runbook_scan.py` skips that one
  H2 when it is last; anywhere else it is a section naming no hook. The self-test holds the heading
  equal to the authority gate's.
- **The document-control standard is rewritten around the gate**: how a document becomes an
  authority, how a change is recorded, and the protection on `main` as it is, the template public
  with a ruleset and a project private by default; "this one stays private" was false from decision
  2026-09-25-001.
- **The authority matrix retires in the template**: the file is removed, and the recovery README and
  the sprint-management standard point to the frontmatter registry. A project's copy is under
  `sprint/`, which the updater never writes, so it stays the project's to delete; each of the three
  projects holds `v1.0.0`'s copy unedited.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-002).

### Consequences

- A decision that changes a standard or the runbook now needs a row or an open story in the same
  commit; adding a hook does, since the runbook gains a section.
- In a project the six logs' rows cite framework decisions alone, so they are the template's and
  their hashes are verified here.
- The rows are stamped by `--stamp` after the commit that writes them.

### Verification

Before the decision was written, the gate on the marked tree reached six authorities and eleven
recorded pairs, and refused exactly two things: the rows citing this decision, then unindexed, and
decision 2026-10-23-009 naming the runbook with no row and no story. Both closed as above.
`gate_runbook_scan.py` gained two fixtures and a cross-check, each proved against a broken variant.

### Enforcement

`doc-authority-scan` and `gate-runbook`; [[reference_doc_authority]], [[reference_gate_runbook]].

---

## Decision 2026-10-23-012: Four more personas, team presets and an opt-in Blender connection

**Date:** 2026-10-23
**Made By:** Chair (S7): the gaps, the four personas, presets over one-by-one choice, an opt-in
connection to Blender, and the build in S8; the shapes recommended by the AI and approved
**Status:** APPROVED
**Builds:** opens TMPL-5.6; extends decision 2026-10-23-004
**Affects:** `personas/` (four new agent files), `.claude/skills/team-selection/SKILL.md` (the
presets, and the connection offered with the Blender persona), the gate that holds the presets (its
script settled in the build), a project's MCP configuration (its file settled in the build),
`sprint/story-tracker.md` (TMPL-5.6; TMPL-2.4 waits on it)

### Context

Before the release the Chair named gaps in the library's team (decision 2026-10-23-004): an
application development team with backend as well as frontend and UI/UX developers, website
development, and imaging, video and 3D with a Blender expert and a way to connect to Blender. The
library holds `software-engineer`, stack-agnostic, `frontend-engineer` and `ux-designer`, but no
backend engineer; web applications, but no websites; `game-artist` and `generative-video-engineer`,
but no Blender, imaging or post-production role. Team selection offers personas one at a time,
grouped by area, and the template configures no MCP server.

### Decision

- **Four library personas**, in the agent-file shape with the shared habits and linted as the
  library is: a **backend engineer** (APIs, services, databases, auth, background jobs, the data
  contract with the frontend); a **web developer** (websites: a static-site generator or a CMS,
  responsive layout, SEO, accessibility, performance budgets, hosting, forms and analytics); a
  **Blender 3D artist** (modeling, materials, UVs, rigging, animation, lighting and rendering,
  geometry nodes, Blender Python for repeatable scene work); an **image and video editor**
  (retouching and compositing, color, editing, motion graphics, encoding and delivery). Slugs are
  settled in the build.
- **Team presets.** Team selection offers named teams as one choice, each a list of library
  personas the Chair may then add to or drop from: proposed are Application development (product
  manager, solution architect, UX designer, frontend and backend engineers, QA, DevOps, security),
  Website (UX designer, web developer, a writer or editor, QA) and Imaging, video and 3D (Blender 3D
  artist, image and video editor, generative video engineer). Membership is confirmed with the Chair
  in the build. A gate refuses a preset naming a persona the library lacks, proved against broken
  variants, so a rename cannot leave a preset pointing at nothing.
- **An opt-in Blender connection.** The template documents an MCP connection to a running Blender, a
  community server and its Blender add-on, offered by team selection only when the Blender persona
  is activated and written to the project's configuration only on the Chair's yes. Off by default
  and never enabled in the template itself, because such a server runs Python inside Blender: the
  build vets the server, pins its version, and names what the operator installs and approves.
- Part of `v2.0.0`; TMPL-2.4 waits on TMPL-5.6.

### Consequences

- The project launch's team stage (decision 2026-10-23-008) can offer a preset beside the three
  personas it always activates.
- A persona the library lacks is still drafted as the project's own; the presets only shorten the
  common choices.

### Verification and enforcement

To be built in TMPL-5.6: the four personas lint clean; the preset gate's fixtures, each proved
against a broken variant, with a runbook section if it is a hook of its own; the connection
documented with its pinned version, and refused nowhere it was not chosen.

---

## Decision 2026-10-23-013: Four personas, team presets and the Blender connection as built

**Date:** 2026-10-23
**Made By:** Chair (S8): the slugs and each preset's membership; the gate's home, the data block,
the pin's forms and the choice of server by the AI within decision 2026-10-23-012, reported to the
Chair
**Status:** APPROVED
**Builds:** TMPL-5.6, the open items of decision 2026-10-23-012
**Affects:** `personas/backend-engineer.md`, `personas/web-developer.md`, `personas/blender-artist.md`,
`personas/image-video-editor.md` (new), `.claude/skills/team-selection/SKILL.md` (the connection
step, Team presets, Connections, the data block), `scripts/skill_scan.py` (rules `preset` and
`connection`), `docs/governance/gate_suite_runbook.md` (`skill-scan-selftest` and `skill-scan`),
`docs/orchestration/knowledge/reference_blender_mcp.md` (new), `sprint/story-tracker.md` (TMPL-5.6)

### Context

Decision 2026-10-23-012 left to the build the four slugs, the presets' membership, the gate's script,
and the server and the file the connection is written to.

### Decision

- **Slugs (Chair):** `backend-engineer`, `web-developer`, `blender-artist` and `image-video-editor`,
  the last so it is never confused with the writing `editor`. Each is at version 1 with the shared
  habits of decision 2026-10-23-004; the backend engineer, who touches data, keeps it out of the
  session, and the Blender artist saves and says what a script will change before running it in a
  connected Blender.
- **Presets (Chair), as proposed:** Application development (`product-manager`,
  `solution-architect`, `ux-designer`, `frontend-engineer`, `backend-engineer`, `qa-engineer`,
  `devops-engineer`, `security-engineer`); Website (`ux-designer`, `web-developer`,
  `business-writer`, `qa-engineer`); Imaging, video and 3D (`blender-artist`, `image-video-editor`,
  `generative-video-engineer`).
- **One YAML block** at the end of the team-selection skill holds `presets:` and `connections:`, read
  by a parser. A connection is keyed by its persona and gives the `.mcp.json` server entry, so the
  block is the one home of the pin.
- **The gate is `skill-scan`**, two rules beside its own: a skill names only personas that exist as
  it names only hooks that exist, and it already reads the roster. `preset` refuses a missing,
  unparsable or second block and a preset naming a persona `personas/` lacks or naming one twice.
  `connection` refuses a connection naming no library persona or pinned to no exact release
  (`==` or `@` a version, or a git source at a full commit, since a tag or branch can move); and
  `.mcp.json` holding a connection, by its name or by running its package, in the template, in a
  project whose roster lacks the persona, or other than written. No new hook.
- **The file is `.mcp.json`**, Claude Code's project scope, at the repository root: committed, so
  the choice is the project's, and approved once in each clone by its operator.
- **The server is Blender Lab's**, the Blender Foundation's own, at v1.0.3, commit
  `2cea8d566dde07fbac28a61d698909d69724e853`, its add-on pinned by the SHA-256 of its release zip:
  no telemetry and no outside service. The community server, though far more widely used, was
  rejected: telemetry on by default, PyPI builds its repository cannot reproduce, four advisories,
  and a PyPI name, `blender-mcp`, that installs it in place of Blender Lab's
  ([[reference_blender_mcp]]). Blender Lab's needs Blender 5.1 or newer.

### Consequences

- The project launch's team stage offers the presets; a persona the library lacks is still drafted
  as the project's own.
- Moving the pin is a change to the skill's block and a fresh vetting, recorded in the entry.
- A headless run loads a committed connection without asking; the entry and the skill say so.

### Verification

`skill-scan`'s self-test: eighty-three checks, every new rule with a passing and a failing case and a
fixture that raises reported as a failure; twenty-five broken variants of the new code each failed
at least one without a crash, and one dead branch (a dedent PyYAML never needed) removed when its
variant passed. The four personas lint clean, and a planted persona whose name differs from its file
was refused. On the real tree the gate refused the skill with no presets block, then passed with it.
On a copy of the template, `.mcp.json` holding the connection, written from the block, was refused
with the persona active or not. A scratch birth wrote no `.mcp.json`; there the same file was refused
without `blender-artist` in the roster, passed with it, and was refused at another commit.

### Enforcement

`skill-scan-selftest` and `skill-scan`; `session-closeout-check` for the personas.

---

## Decision 2026-10-23-014: The PRD and architecture templates as built

**Date:** 2026-10-23
**Made By:** Chair (S8): where the templates live, each an authority for its own scope, the PRD's
and the architecture's sections; the draft that becomes the authority at approval and the quoted
versions by the AI within decision 2026-10-23-008
**Status:** APPROVED
**Builds:** TMPL-5.1, the open items of decision 2026-10-23-008
**Affects:** `docs/templates/prd.md` (new), `docs/templates/architecture.md` (new),
`docs/templates/README.md` (new: making and approving a document), `docs/governance/doc_control_standard.md`
(Authorities), `README.md` (the structure table), `sprint/story-tracker.md` (TMPL-5.1)

### Context

Decision 2026-10-23-008 left three things to the build: the templates' sections, their frontmatter
in the `authority:` format, and where they live. `docs/prd/` and `docs/architecture/` are the
project's, never written by the updater, so a template kept there would reach no project after its
birth. And the gate refuses two documents claiming one scope (decision 2026-10-23-010): a template
carrying a PRD's `authority:` line would collide with every PRD made from it.

### Decision

- **Where (Chair).** `docs/templates/prd.md` and `docs/templates/architecture.md`, a path the
  template owns, so the updater's three-way merge carries a newer template to every project.
  `docs/templates/README.md` holds how a document is made from one and approved, its one home until
  `/project-launch` (TMPL-5.2) runs those steps.
- **A template is the authority for its own scope (Chair)**: the sections every PRD, or every
  architecture, carries, with `implements:` and a version log as a standard has. The document made
  from it claims the project's scope, `product requirements — <project>` or
  `architecture — <project>`. A copy that keeps the template's line fails the one-scope rule, so the
  gate catches the forgotten step without a change to it.
- **A made document is a draft until it is approved.** It starts with `status: draft`, `template:`
  (the template's version) and, for the architecture, `prd:` (the PRD version it is built from), and
  an empty version log; it claims no authority, since it has no decision to cite. At approval it
  gains `authority:`, `implements: []`, `verified:` and `status: approved`, and its first row cites
  the decision that approved it, as a `fact:`, since no story exists before planning. That is
  decision 2026-10-23-008's approval on record as the gate reads it. Versions are quoted, since YAML
  reads `1.10` as the number 1.1.
- **The PRD's sections (Chair):** purpose; users and stakeholders; goals and success criteria
  (`G-n`); deliverables; scope and non-goals; functional requirements (`FR-n`), which the tracker's
  PRD Ref cites; non-functional requirements (`NFR-n`) with thresholds; constraints; assumptions and
  dependencies; risks; open questions.
- **The architecture's sections (Chair):** context; quality attributes, each NFR with how it is met
  and verified; system context; components, each with the FRs it serves; data; interfaces;
  technology choices, each with its decision; deployment and environments; security; observability
  and operations; dependency layers, which the planning session turns into epics; risks and
  trade-offs; open questions.
- Part of `v2.0.0` (decision 2026-10-23-008).

### Consequences

- TMPL-5.2's PRD and architecture stages make their documents by the README's steps; TMPL-5.3's
  approval gate can read `status:` and the authority, and the architecture's `prd:` against the
  PRD's newest version.
- In a project the templates' rows cite framework decisions only, so their hashes are verified in
  the template (decision 2026-10-23-010).

### Verification

On the template the gate registers both templates beside the six authorities, exit 0. On a scratch
birth from this tree, a PRD and an architecture made by the README's steps: the drafts committed
and unregistered, exit 0; a copy keeping the template's line refused as `scope`; approved by two
logged decisions, exit 0 with the rows `pending`; `--stamp` wrote each document's approval commit
and the gate verified both; a stamped hash swapped refused as `commit`. The first run stamped the
template's commit instead and the birth itself was refused: the two defects of decision
2026-10-23-015, fixed before this proof was taken again.

### Enforcement

`doc-authority-scan`; [[reference_doc_authority]].

---

## Decision 2026-10-23-015: In a project, what the template wrote is judged in the template

**Amended 2026-10-23 (TMPL-2.8, decision 2026-10-23-023):** so is a copy of the template before its
initializer, GitHub's "Initial commit": it has no profile yet, and its history, squashed by GitHub,
holds none of the commits the template's rows were stamped with.

**Date:** 2026-10-23
**Made By:** Chair (S8), on the AI's report of the defect and its proposed fix; the copy fix by the
AI, bringing the code to decision 2026-10-23-010's "following renames"
**Status:** APPROVED
**Amends:** 2026-10-23-010 (the template's rows verified in the template)
**Builds:** TMPL-2.6
**Affects:** `scripts/doc_authority_scan.py` (`judge`, `renames_only`, the docstring, nine fixtures),
`docs/governance/gate_suite_runbook.md` (`doc-authority-selftest` and `doc-authority-scan`),
`docs/orchestration/knowledge/reference_doc_authority.md`, `sprint/story-tracker.md` (TMPL-2.6;
TMPL-2.4 waits on it)

### Context

TMPL-5.1's proof made a scratch project from the working tree, and the initializer's closing suite
run refused the birth. A birth from the committed `HEAD` alone did the same: `doc-authority-scan`
failed seven times. Each of the six authorities' rows cites TMPL-2.3, and a project's tracker,
regenerated at birth, holds no TMPL story, so every row was `unmarked`; decision 2026-10-23-009 is
queued for the gate runbook by TMPL-5.5, likewise absent, so it was `unrecorded`. Decision
2026-10-23-010 had already ruled that a template row's hash is verified in the template, because the
project's history holds no template commit; the same holds of its story and of a framework
decision's queue, and the build applied the rule to the hash alone. S7's scratch adoptions ran
before TMPL-2.3 marked the first authorities, and no birth ran after, so nothing saw it. The
template's own CI judges the template, where every rule held.

### Decision

- **In a project, a row citing only framework decisions is the template's** and is held to neither
  `unmarked` nor `commit`; the template judged both before the release.
- **In a project, a framework decision is held to neither `no-affects` nor `unrecorded`**: its
  record and its queue are the template's.
- **The project's own are judged in full**: a row citing a project decision, alone or beside a
  framework one, and every project decision from the cutoff.
- **A row's commit is found following renames, never a copy.** The same proof stamped a PRD's
  approval row with the commit that introduced its template: `git log --follow` sets
  find-copies-harder, so a document made by copying another inherits that one's history. Where the
  path changes, the older path surviving in the commit that brought the newer one is a copy, and the
  history stops there; decision 2026-10-23-010 said "following renames", and the code now does only
  that.
- Two `v2.0.0` defects found before the release, so both fixes ship in `v2.0.0`; TMPL-2.4 waits on
  them.

### Verification

Seven fixtures, one per side of each project rule, the template's own case beside them, and two for
the history, a rename followed and a copy cut; nine broken variants each failed at least one without
a crash. A scratch birth from the working tree started green, the initializer's suite run passing; a
PRD made from its template then stamped with its own approval commit, and a `git mv` of it still
derived that commit.

### Enforcement

`doc-authority-selftest` and `doc-authority-scan`; [[reference_doc_authority]].

---

## Decision 2026-10-23-016: The doc-queue as designed

**Date:** 2026-10-23
**Made By:** Chair (S8): which stories are the writer's queue, the drain's agent, that the drain does
not commit, and that S9 builds it
**Status:** APPROVED
**Builds:** TMPL-2.2, within decision 2026-10-22-002
**Affects:** `scripts/session_start.py` (runs the gate at cold start), `.pre-commit-config.yaml` (a
manual-stage `doc-queue` hook; its script settled in the build), `docs/governance/gate_suite_runbook.md`
(its section), `.claude/skills/` (the drain skill), `AGENTS.md` (the skills table),
`sprint/story-tracker.md` (TMPL-2.2)

### Context

Decision 2026-10-22-002 queues a structural change to an authority as a tracker story, and drains
the queue at cold start, bounded by a `Queued: S<N>` note: the `doc-queue` gate fails while a queued
story is older than one session, and the technical writer drains one document per forked
invocation, returning the rows it wrote. The authority gate counts any open story citing a decision
and a path as queueing it, and today the only such story is TMPL-5.5, whose runbook change describes
a gate it has not built: no writer could drain it, in one session or any. And `agent:` in a forked
skill resolves only to a built-in or a roster agent, while `technical-writer` is a library persona.

### Decision

- **The writer's queue is the stories marked for it (Chair).** An open story whose row carries
  `Queued: S<N>`, written by the session that queued a change for the writer, is in the queue; at a
  session later than S<N+1> it fails `doc-queue`. A story that makes its own document change, as
  TMPL-5.5 does, carries no note and is an ordinary story.
- **The drain forks as `general-purpose` in the writer's role (Chair):** its first step reads
  `personas/technical-writer.md`, present in the template and every project, and takes that prompt.
  One document per invocation, every queued change to it in one pass.
- **The drain leaves its change for review (Chair):** it rewrites the document, adds the version-log
  row citing the story, sets the story Done with the tracker's counts, runs the gates, and returns
  the rows it wrote; the main session reviews the diff and commits.
- **The gate runs at cold start by the `SessionStart` hook** as a manual-stage hook, reported, and is
  visible at closeout, never a closeout step (decision 2026-10-22-002).
- **Built in S9 (Chair).**

### Verification and enforcement

To be built in TMPL-2.2: the gate's fixtures, each proved against a broken variant; its runbook
section passing `gate-runbook`; the drain skill passing `skill-scan` and listed in `AGENTS.md`.

---

## Decision 2026-10-23-017: CI makes a scratch project on every push

**Amended 2026-10-23 (TMPL-2.8, decision 2026-10-23-023):** the probe's verdict is two runs, not
one: the suite on the Initial commit, as GitHub runs it before anyone has run the initializer, and
the initializer's own. The first was found red on a real project while every birth was green.

**Date:** 2026-10-23
**Made By:** Chair (after the S8 closeout), on the AI's recommendation; the shape by the AI
**Status:** APPROVED
**Builds:** opens TMPL-2.7
**Affects:** `scripts/birth_probe.py` (new), `.github/workflows/gates.yml` (a step),
`docs/orchestration/knowledge/reference_ci_backstop.md` (why the backstop births a project),
`sprint/story-tracker.md` (TMPL-2.7; TMPL-2.4 waits on it)

### Context

From the S7 closeout push until the S8 closeout push, every project born from the template was
refused by its own first suite run, while the template's CI stayed green (decision 2026-10-23-015).
CI judges the template, and several gates judge a project differently: the profile's stripped
documents, the tracker the initializer regenerates, the project's decisions beside the framework's,
the roster. GitHub's "Use this template" copies the default branch as it stands, not a release tag,
so `main` must make a healthy project at every push. The regression was found only because TMPL-5.1's
proof needed a birth, and the lesson stood as prose in [[reference_doc_authority]]: a rule with no
control.

### Decision

- **`scripts/birth_probe.py`** makes a scratch project from a committed revision (`HEAD` unless
  named): the revision's tree in a temporary directory, a fresh repository, the initializer with
  `--apply` and a profile. Its verdict is the initializer's own: the suite run that already refuses a
  birth that is not green. A script, so the operator or any agent runs the same check locally, as
  the release does.
- **CI runs it on every push and pull request in the template**, once for each profile
  (`commercial`, `gcc`), since the profile's stripping is one way a birth breaks; skipped where
  `.project-profile` exists, in a project. It reports, as the rest of CI does (decision
  2026-09-22-001): a red run is fixed in the same session.
- **Proved against a real broken commit**: at `38c549d`, the S7 tree, it fails for the defect
  TMPL-2.6 fixed; at the commit that builds it, it passes.
- **Out of scope**: an existing project taken to a newer release through `template_update.py`,
  heavier and kept by hand at the release (TMPL-2.4).
- Part of `v2.0.0`; TMPL-2.4 waits on TMPL-2.7.

### Verification and enforcement

To be built in TMPL-2.7: the probe red at `38c549d` and green at its own commit, for both profiles;
the CI step's run observed green with `gh run watch --exit-status`.

---

## Decision 2026-10-23-018: The birth probe as built

**Amended 2026-10-23 (TMPL-2.8, decision 2026-10-23-023):** before the initializer the probe runs the
suite on the bare Initial commit, once per run since no profile applies yet, with the same
environment; a red run there refuses the birth.

**Date:** 2026-10-23
**Made By:** AI (S9), within decision 2026-10-23-017; the Chair placed TMPL-2.7 before TMPL-2.2
**Status:** APPROVED
**Builds:** TMPL-2.7
**Affects:** `scripts/birth_probe.py` (new), `.pre-commit-config.yaml` (the `birth-probe-selftest`
hook), `docs/governance/gate_suite_runbook.md` (its section), `.github/workflows/gates.yml` (the
`birth` job), `AGENTS.md` (the governance map),
`docs/orchestration/knowledge/reference_ci_backstop.md` (why CI births a project),
`sprint/story-tracker.md` (TMPL-2.7)

### Context

Decision 2026-10-23-017 fixed what the probe does and left its mechanics to the build: how the
revision reaches the scratch, what runs the initializer, how the probe's own rules are proved, and
how CI runs it once per profile.

### Decision

- **The committed tree, by `git archive`**, written to a temporary directory: neither the working
  tree nor an untracked file reaches the birth, and the source repository gains no worktree or ref.
  The scratch is a fresh repository holding the tree as one "Initial commit", what GitHub's template
  flow gives a project, and the initializer is that revision's own, run with `--apply`, the profile
  and filler values for its tokens. Its exit code is the verdict.
- **No `GIT_*` variable and no `CLAUDE_PROJECT_DIR` reach git or the birth.** Inside a commit hook
  git exports the index it is committing, so a scratch `git add` could write into the source's; and a
  gate reading `CLAUDE_PROJECT_DIR` would judge the source instead of the birth. The initializer runs
  unbuffered, so its lines keep their place beside the suite's in a CI log.
- **A self-test hook, `birth-probe-selftest`**, as every script here has, over a stub initializer in
  a scratch template: a birth takes minutes, so the probe itself is not a commit gate. Its fixtures
  hold each rule above, the scratch removed, every profile born when none is named, a project's
  revision refused (exit 2) and an unknown revision unjudged.
- **CI runs it as a `birth` job**, a matrix over `commercial` and `gcc` beside the `gates` job, so
  the two births run in parallel and a red one names its profile. The probe step carries
  `if: hashFiles('.project-profile') == ''`, which skips it in a project; a job-level `if:` cannot
  read the tree.
- `AGENTS.md`'s governance map names the script, so an agent changing what a project inherits can
  run the same check before it pushes.

### Verification

Thirteen fixtures pass; ten broken variants, one per rule, each fail at least one without a crash.
At `38c549d`, the S7 tree, the probe exits 1 under both profiles, the initializer's suite refusing
each birth at `doc-authority-scan` alone with the seven violations of decision 2026-10-23-015. At
`19537c4`, the commit that builds it, it exits 0 under both, locally and on GitHub: run 40050465938,
`gates`, `birth (commercial)` and `birth (gcc)` each `success` under `gh run watch --exit-status`,
both probe steps run, not skipped.

### Enforcement

`birth-probe-selftest`; the `birth` job in `.github/workflows/gates.yml`; [[reference_ci_backstop]].

---

## Decision 2026-10-23-019: The doc-queue as built

**Date:** 2026-10-23
**Made By:** AI (S9), within decisions 2026-10-22-002 and 2026-10-23-016
**Status:** APPROVED
**Builds:** TMPL-2.2
**Affects:** `scripts/doc_authority_scan.py` (`--queue`, `judge_queue`, its fixtures),
`scripts/session_closeout.py` (`current_session`), `scripts/session_start.py` (runs the gate,
reports its verdict), `.pre-commit-config.yaml` (the manual `doc-queue` hook),
`docs/governance/gate_suite_runbook.md` (`doc-authority-selftest`, `doc-queue`, the preamble),
`docs/governance/doc_control_standard.md` (Recording a change), `.claude/skills/doc-drain/SKILL.md`
(new), `.claude/skills/closeout/SKILL.md` (reports the queue), `AGENTS.md` (the cold start, the
skills table), `docs/orchestration/knowledge/reference_doc_authority.md` (the queue),
`sprint/story-tracker.md` (TMPL-2.2)

### Context

Decision 2026-10-23-016 fixed the queue, the drain's agent and that the drain leaves its change for
review, and left the gate's script and the note's reading to the build.

### Decision

- **The gate is a mode of the authority gate**, `doc_authority_scan.py --queue`, since it reads the
  same registry, decision index and tracker parse; its fixtures run in `doc-authority-selftest`. A
  manual hook, `doc-queue`: its verdict depends on the session at work, which a commit does not
  change.
- **A note is read bare.** `Queued: S<N>` outside a code span on a row not Done is a note; quoted in
  a code span it is the convention, as in TMPL-2.2's own row. One note per row, naming one session.
- **A queued story names exactly one authority in a code span, and cites an indexed decision**: one
  drain is one document and sets its stories Done, and its version-log row cites the stories'
  decisions. Either missing, or a session to come, fails.
- **The session at work is one rule**, `session_closeout.current_session`: the newest sprint-status
  entry, plus one while the next kickoff exists. The start hook and the gate both read it.
- **The start hook runs it after `session-verify`**, `--verbose` so a passing run's list reaches the
  report: the verdict, each queued story with the drain that clears it, and on a failure each
  violation with what it means. pre-commit's own `[ERROR]` lines are never read as items. The
  closeout skill runs it too and names each queued story in the handoff, never waiting on it.
- **The drain is `doc-drain`**, forked as `general-purpose`, `background: false` so the session has
  its result before it reviews. Its first step takes `personas/technical-writer.md`'s prompt; it
  refuses a dirty tree, so the review sees its change alone; it makes every queued change to the
  document in one pass, writes one version-log row naming each story, sets them Done with the
  counts, runs the gates, and stages, commits and stamps nothing. With no argument it lists the
  queue and stops, since which document is drained is the session's choice.
- `AGENTS.md`'s cold start runs the gate by hand for an agent with no start hook.

### Verification

Eighteen queue fixtures in `doc-authority-selftest`, a current-session fixture in
`session-closeout-selftest`, and six reporting fixtures in `session-start-selftest`; sixteen broken
variants each fail at least one without a crash. A reporting fixture caught a real defect on its
first run: pre-commit's `[ERROR]` line was read as a queue violation. On the template the gate
reads S9 with nothing queued, since TMPL-2.2's row quotes the note. On a scratch birth from `0dcccd2`
with a project decision queued for the writer as PROBE-1.1, `Queued: S1`, the start hook's report
read PASS with the story listed and its drain named at S1 and at S2, and FAILED with the overdue
violation and its meaning at S3; the project's suite passed with the story queued. A fresh agent
then followed `doc-drain` on that tree with only the document's path: it rewrote §8 of the sprint
standard, wrote version 1.1 citing the decision and the story, set the story Done with the counts,
ran both gates to exit 0 and committed nothing; committed and stamped there, the gate verified the
project's own hash. Its friction report changed the skill before it shipped: a story's dependency is
checked before the document is touched, the skill governs where the persona's prompt differs, the
version rule says what MAJOR measures, and the re-read before `verified:` is owed on any date.

### Enforcement

`doc-authority-selftest` and the manual `doc-queue`, run by the `SessionStart` hook;
`skill-scan` over `doc-drain`; [[reference_doc_authority]].

---

## Decision 2026-10-23-020: The approval gate as built

**Amended 2026-10-23 (TMPL-5.2, the Chair):** a document reopened for revision keeps its
`authority:` line and its rows and stands approved at its newest row's version until it is approved
again, the new row written only then; the architecture's `prd:` is held to the PRD's newest version
only while the architecture is `status: approved`. As first built, a reopened draft was no approval,
so once a real epic existed every commit of a revision in progress was refused and `/project-launch
pause` could not save one. Approving a PRD revision now refuses the commit until the architecture
built on the old version is reopened too, which is how decision 2026-10-23-008's "flags each later
stage" is held. `**Skips:**` names any stage of `/project-launch`; only `prd` and `architecture`
stand in for an approval.

**Date:** 2026-10-23
**Made By:** Chair (S9): how a skip is logged; the gate's home and its reading by the AI, within
decisions 2026-10-23-008 and 2026-10-23-014
**Status:** APPROVED
**Builds:** TMPL-5.3
**Affects:** `scripts/doc_authority_scan.py` (`judge_approval`, `check_tree`, `header_field`, the
fixtures), `docs/governance/gate_suite_runbook.md` (`doc-authority-selftest`, `doc-authority-scan`),
`docs/governance/doc_control_standard.md` (Authorities), `docs/templates/README.md` (skipping a
document), `.claude/skills/planning-session/SKILL.md` (Preconditions),
`docs/orchestration/knowledge/reference_doc_authority.md` (why a real epic needs approved
documents), `sprint/story-tracker.md` (TMPL-5.3)

### Context

Decision 2026-10-23-008 made approval binding: in a project, a real epic needs an approved PRD and
an approved architecture, or a logged skip of either. Decision 2026-10-23-014 defined approved: the
document in `docs/prd/` or `docs/architecture/` with `status: approved` and the `authority:` line,
the architecture's `prd:` the version of the PRD it is built from. How a skip is logged, and where
the gate lives, were left to the build; 2026-10-23-008's Affects line guessed
`scripts/session_closeout.py`.

### Decision

- **A skip is a decision headed `**Skips:**` (Chair).** An APPROVED decision of the project's own
  log, `sprint/decision-log.md`, whose header block carries `**Skips:** prd`, `**Skips:**
  architecture` or both, comma-separated, its reason in the body. The log is already where
  2026-10-23-008 records a skip, and a header line is read as `**Affects:**` is. A skip in the
  framework's log, or a decision not APPROVED, counts for nothing; a `**Skips:**` naming another
  stage fails.
- **The gate is a rule of `doc-authority-scan`**, not of the session state gate: it reads the
  authority frontmatter, the version logs and the decisions' header lines, all of which that gate
  already parses. It runs on every commit through `check_tree`, the one function the command and a
  fixture both call.
- **It applies in a project whose tracker holds a real epic**: the template is never judged, and a
  project is not judged before its planning session writes the first epic, which is the commit the
  gate exists to refuse.
- **Approved is read strictly.** One document per folder with the `authority:` line, a version-log
  row and `status: approved`, or `status: draft` while reopened for revision (amended above); one
  that claims no authority, has no row, sits outside the folder or carries another status is no
  approval. Two in one folder fail. An approved architecture's `prd:` is the PRD's newest
  version-log version, compared as the quoted string; an unquoted `prd: 1.1` is a number and fails.
  With the PRD skipped, `prd:` is not read.

### Verification

Twenty-one fixtures, two of them over `check_tree`; fifteen broken variants each fail at least one
without a crash, the variant that left the rule out of the command among them. Amended: twenty-six
fixtures and twenty variants, the reopened revision and the ungated skips among them. On a scratch birth from
`d7ad4d7` under `commercial`: before planning, exit 0; the first real epic with no documents
refused, both folders named; with both documents made as drafts by `docs/templates/README.md`,
refused again; both approved by its steps, exit 0 with the rows pending and again once stamped, the
project's whole suite green; the PRD revised to 1.1 with the architecture still built from 1.0,
refused as `prd-version`; the architecture removed and an APPROVED `**Skips:** architecture` logged,
exit 0; the same skip `PROPOSED`, refused.

### Enforcement

`doc-authority-selftest` and `doc-authority-scan`; [[reference_doc_authority]].

---

## Decision 2026-10-23-021: `/project-launch` as built

**Amended 2026-10-23 (TMPL-5.4, decision 2026-10-23-024):** the skill says a boundary before planning
is a new conversation, still S1, and that a pause with nothing changed commits nothing.

**Date:** 2026-10-23
**Made By:** Chair (S9): that the skill is the Chair's alone, and that a reopened revision stands
(decision 2026-10-23-020, amended); the rest by the AI, within decision 2026-10-23-008
**Status:** APPROVED
**Builds:** TMPL-5.2
**Affects:** `.claude/skills/project-launch/SKILL.md` (new), `.claude/skills/team-selection/SKILL.md`
(step 2, the intake's answer), `.claude/skills/planning-session/SKILL.md` (step 5, the `**Source:**`
line; Done when), `scripts/new_project.py` (the S1 entry's one next step, its fixture, the self-test
counting its checks), `docs/governance/gate_suite_runbook.md` (`new-project-selftest`), `AGENTS.md`
(the skills table), `TEMPLATE_GUIDE.md` (Step 7), `README.md` (the structure table),
`docs/orchestration/knowledge/reference_project_launch.md` (new), `sprint/story-tracker.md` (TMPL-5.2)

### Context

Decision 2026-10-23-008 fixed the five stages, the Chair's control of each and that the state lives
in the documents, and left three things open: the templates' sections (settled by 2026-10-23-014),
their frontmatter (likewise), and whether the skill is the Chair's alone.

### Decision

- **The Chair's alone (Chair).** `disable-model-invocation: true`: every stage needs the Chair to
  answer and approve, so Claude never starts one unasked. The S1 entry names `/project-launch` as
  its one next step, so the Chair types it.
- **The main session, never forked**, since a subagent can neither ask the Chair nor see the
  conversation; another agent follows the file as instructions.
- **Each stage's state is read from the tree**: intake done when the PRD draft exists in the
  template's shape; team when the roster holds the three leads; the PRD and the architecture when
  approved; planning when the tracker holds a real epic. Skipped is an APPROVED `**Skips:**`
  decision; reopened is an approved document back at `status: draft`; stale is a stage built on an
  older version of the one before it. A bare `/project-launch` resumes at the first stage neither
  done nor skipped, or stale; `status` changes nothing.
- **Intake writes into the PRD draft**: the purpose into §1, what it should accomplish into §3 and
  §4, the skills into §9 as the expertise the project depends on. A pause between intake and team
  loses nothing, and the team stage reads §9 as the Chair's first answer to team selection.
- **A pause resumes from the draft**: a section holding only the template's `<!-- -->` guidance is
  the next to fill. Each stage's draft is committed as it grows.
- **The plan records its sources**: the planning skill sets the tracker's `**Source:**` line to the
  PRD and architecture versions it is built from, which `status` reads to flag a plan built on an
  older architecture. Only the architecture's `prd:` is gated; the plan's staleness is reported.
- **A PRD revision reopens the architecture in the same commit**, since `doc-authority-scan` refuses
  an approved architecture built on an older PRD version.

### Verification

`skill-scan` over the skill and the two it calls; the initializer's fixture for the S1 entry's one
next step, caught by two broken skeletons; a birth from `6e94683` green under both profiles. A fresh
agent given only the skill applied `status` to two scratch trees and read every stage as the rules
say; its friction report sharpened them before release: a skip's status is the index's, as the gate
reads it; the documents decide over a decision approving a file that is gone; the launch is done
when every stage is done or skipped; a plan with no versions on its `**Source:**` line is done with
its staleness unknown, and stale compares both documents it names. The live run through every stage
with the Chair at the keyboard is TMPL-5.4's.

### Enforcement

`skill-scan`; `new-project-selftest`; `doc-authority-scan` for the approvals the stages produce;
[[reference_project_launch]].

---

## Decision 2026-10-23-022: The README front page as built

**Date:** 2026-10-23
**Made By:** AI (S10), within decision 2026-10-23-009
**Status:** APPROVED
**Builds:** TMPL-5.5
**Affects:** `README.md` (the walkthrough and the catalog), `TEMPLATE_GUIDE.md` (cut to named
sections), `scripts/skill_scan.py` (`uncatalogued`, `catalog`, its fixtures),
`docs/governance/gate_suite_runbook.md` (`skill-scan-selftest`, `skill-scan`, the preamble),
`scripts/gate_runbook_scan.py` (a fix text), `docs/orchestration/knowledge/reference_claude_code_skills.md`
(the catalog), `docs/orchestration/knowledge/reference_derived_project_start.md` and
`docs/orchestration/knowledge/reference_template_update.md` (pointers to the guide),
`sprint/story-tracker.md` (TMPL-5.5)

### Context

Decision 2026-10-23-009 fixed the README's order and contents and the gate's purpose; how the
catalog names a skill, what the gate reads, and what the guide keeps were left to the build.

### Decision

- **Nine walkthrough steps**: create the repository; initialize it; install the hooks; commit the
  birth; open Claude Code and trust the folder; `/project-launch`; close out; the session loop; take
  a release. Committing the birth is a step of its own, since the initializer's changes are
  otherwise left in the tree. Each step gives the command and what the user sees, and links to the
  guide for detail rather than repeat it.
- **The catalog names each skill by its path** beside the command it gives the operator, as
  `AGENTS.md` does, so one reader serves both gates. It also lists the operator scripts, the session
  hooks and the gates, the gates by link to the runbook and never copied.
- **The gate reads the `## Catalog` section only**, to its next H2, fences honoured: a path the
  walkthrough mentions catalogues nothing. A README with no such section fails, never read as an
  empty catalog. It holds in a project as in the template: the README is the operator's front page
  in both, and a project's own skill is catalogued there too.
- **The guide keeps what the initializer leaves**, in named sections the README links to (the
  initializer, customizing the law, installing the gates, launching the project, taking a release);
  its by-hand token steps are gone, and every live reference to a numbered step now names the
  section. References inside decisions and old sprint entries record their time and stay.
- The README's list of what the template provides, a count of a growing set, is gone; the catalog
  and the runbook hold the sets.

### Verification

Eight catalog fixtures in `skill-scan-selftest`, seven broken variants each caught; on the real
tree a README whose catalog lacked `/doc-drain` refused, restored passing. The walkthrough run for
real on the private `SaltyBrett/launch-probe-s10`, made from `30677d3`: steps 1 to 4 as written (one
"Initial commit"; the dry run writing nothing; the apply ending in the line the README quotes; both
hook types installed; a trailer commit refused by the attribution gate; the birth committed through
twenty-nine hooks, pushed, its run green), except that GitHub's own run on the Initial commit was
red, the defect TMPL-2.8 fixed; step 9's commands exit 0, the dry run `already on v1.0.0` while no
newer release exists. Steps 5 to 8 are TMPL-5.4's live run.

### Enforcement

`skill-scan-selftest` and `skill-scan`; [[reference_claude_code_skills]].

---

## Decision 2026-10-23-023: A copy of the template is judged as a project, and the probe judges GitHub's first run

**Date:** 2026-10-23
**Made By:** Chair (S10), on the AI's report of the defect and its proposed fix
**Status:** APPROVED
**Amends:** 2026-10-23-015 (a copy judged as a project), 2026-10-23-017 (the probe's verdict),
2026-10-23-018 (the probe's Initial-commit run)
**Builds:** TMPL-2.8
**Affects:** `scripts/doc_authority_scan.py` (`template_copy`, `resolves`, `plan_stamps`, `judge`, the
fixtures), `scripts/birth_probe.py` (the Initial commit's run, its fixtures),
`docs/governance/gate_suite_runbook.md` (`doc-authority-selftest`, `doc-authority-scan`,
`birth-probe-selftest`), `docs/orchestration/knowledge/reference_doc_authority.md`,
`docs/orchestration/knowledge/reference_ci_backstop.md`,
`docs/orchestration/knowledge/reference_derived_project_start.md`, `sprint/story-tracker.md`
(TMPL-2.8; TMPL-2.4 waits on it)

### Context

TMPL-5.5's walkthrough, run for real on a private repository made from `30677d3`, found GitHub's own
`gates` run on the new project's "Initial commit" red: `doc-authority-scan` refused nineteen rows as
`commit`. That commit is the template's tree with no `.project-profile`, so the gate judged it as the
template, and verified each stamped row's hash against a history GitHub had squashed to the one
commit. Every project made since S7 marked the first authorities opened with that red run, while
the README said it was green. The birth probe did not see it: it judged a birth only after the
initializer, whose profile makes the template's rows foreign, and never the run GitHub makes first.

### Decision

- **A copy is told by its history (Chair).** With no profile, a repository holding none of the
  commits the template's rows were stamped with is a copy of the template, and what the template
  wrote is judged in the template there, as in a project: its rows are held to neither marker nor
  hash, its decisions to neither `**Affects:**` nor record, and `--stamp` never writes them. The
  template always holds those commits, so one mistyped hash beside the rest is still refused; with
  nothing stamped there is nothing to tell by, and the repository is judged as the template. A
  shallow clone cannot say, and the gate exits 2 there as before.
- **The probe judges the run GitHub makes first (Chair).** It runs the suite on the bare Initial
  commit before the initializer, once per run since no profile applies yet, in the same clean
  environment; a red run refuses the birth whatever the initializer says.
- Both fixes ship in `v2.0.0`; TMPL-2.4 waits on TMPL-2.8.

### Verification

Seven copy fixtures in `doc-authority-selftest`, seven broken variants each caught; four
Initial-commit fixtures in `birth-probe-selftest`, four more broken variants caught beside the ten
before. At `30677d3` the probe exits 1, refusing the Initial commit at `doc-authority-scan` with the
nineteen violations GitHub showed on `SaltyBrett/launch-probe-s10`'s first run, while both profiles
were green after the initializer; at `ea19c0d`, the commit that fixes it, it exits 0 at the Initial
commit and under both profiles, and run 40058466647 is green on `gates` and both `birth` jobs.

### Enforcement

`doc-authority-selftest` and `doc-authority-scan`; `birth-probe-selftest` and the CI `birth` job;
[[reference_doc_authority]], [[reference_ci_backstop]].

---

## Decision 2026-10-23-024: Before planning, a launch boundary is a new conversation

**Amended 2026-10-23 (TMPL-5.4's second run):** the emergency close says the same. `AGENTS.md` and
the handoff standard §7 said the next session's `session-verify` fails after one; before a project's
first closeout it passes, there being no pair, and the next conversation is still S1. The second
run's old session wrote an S1 emergency checkpoint on that claim, then found it false. The boundary
is taken with `/clear` or a new conversation.

**Date:** 2026-10-23
**Made By:** Chair (S10), on the AI's report from the live run
**Status:** APPROVED
**Amends:** 2026-10-23-008 (a stage's end as a session boundary), 2026-10-23-021 (the skill's text)
**Builds:** TMPL-5.4's finding
**Affects:** `.claude/skills/project-launch/SKILL.md` (Opening a stage, `pause`), `README.md`
(walkthrough steps 6 and 7), `docs/orchestration/knowledge/reference_project_launch.md` (why the
first closeout comes after planning); amended: `AGENTS.md` (the emergency close),
`docs/standards/session_handoff_standard_v2.0.md` (§7)

### Context

The live run of `/project-launch` on `SaltyBrett/launch-probe-s10` (TMPL-5.4) stopped in the PRD
stage, and the session offered the Chair a closeout it could not make: every task of a kickoff must
cite a story in a real epic (`session_closeout.py`, `task-story`), and the first real epic is the
commit planning makes, which the approval gate refuses until the PRD and the architecture stand
approved or skipped. Decision 2026-10-23-008's "closing out there names the next stage's persona"
holds only from planning on. A new conversation in the probe, by contrast, was still S1, its
`session-verify` passing with no pair.

### Decision

- **Before planning, the Chair takes a boundary by ending the conversation (Chair).** The next is
  still S1, and `/project-launch` resumes from the documents, taking the next stage's lead from the
  roster as it already does. No gate changes.
- **The first closeout comes after planning**, naming the lead the Chair chose at the team stage.
- **A pause with nothing changed since the last commit commits nothing**, as the live session did.

### Verification

`pre-commit run session-verify --hook-stage manual --all-files` in the probe after the session
stopped: exit 0, "This is S1". The resumed live run opens a new conversation there.

### Enforcement

The kickoff linter's `task-story` rule, unchanged, is why; [[reference_project_launch]].

---

## Decision 2026-10-24-001: An authority's path written bare in `**Affects:**` is refused

**Date:** 2026-10-24
**Made By:** Chair (S11), on the AI's report from the live launch: a refusal in the gate and the
README's wording; the rule's reading by the AI
**Status:** APPROVED
**Builds:** TMPL-2.9
**Affects:** `scripts/doc_authority_scan.py` (`judge`, the `bare-path` rule, its fix, its fixtures, the
docstring's rules and honest limit), `docs/templates/README.md` (Approving it, step 5),
`docs/governance/gate_suite_runbook.md` (`doc-authority-selftest`, `doc-authority-scan`),
`docs/orchestration/knowledge/reference_doc_authority.md` (the honest limit, a rule),
`sprint/story-tracker.md` (TMPL-2.9)

### Context

TMPL-5.4's third run approved the probe's PRD with the decision `LP-2026-10-24-001`, its
`**Affects:**` naming `docs/prd/prd.md` without backticks. The gate reads an `**Affects:**` path
only from a code span, so it held the PRD to no record and passed; the PRD happened to cite the
decision, but nothing had checked it. `docs/templates/README.md` step 5, the instruction the launch
follows, said only "naming the document's path". The gate's docstring and [[reference_doc_authority]]
named the limit; nothing told the author.

### Decision

- **The gate refuses the bare form (Chair).** A decision held to `**Affects:**`, dated from the
  cutoff and not the template's in a project, fails as `bare-path` when its value names an
  authority's path outside a code span and in none, since that document then goes unjudged. A path
  also named in a code span is read, and passes; a path no authority holds may be written bare; a
  longer path ending in an authority's is not that path.
- **The README says it (Chair).** Step 5 names the path as a code span, with the example, and says
  the gate refuses it bare.
- A document named in words, "the PRD", is still not read: the gate cannot read prose.
- Ships in `v2.0.0` before TMPL-2.4. A new refusal, so MAJOR on its own
  ([[reference_template_versioning]]); a derived project's decisions are judged by it at adoption.

### Verification

Seven fixtures in `doc-authority-selftest`; five broken variants each caught by the fixture written
for it: the rule left out, a path also in a code span counted bare (twice, broad and narrow), no
boundary before the path, and decisions before the cutoff judged. The real tree passes: no decision
from the cutoff names an authority bare.

### Enforcement

`doc-authority-selftest` and `doc-authority-scan`; [[reference_doc_authority]].

---

## Decision 2026-10-24-002: A closeout refuses an entry that says the session is still open

**Date:** 2026-10-24
**Made By:** Chair (S11), on the AI's report from the live launch: a refusal in the closeout gate;
the rule's reading by the AI
**Status:** APPROVED
**Builds:** TMPL-5.7
**Affects:** `scripts/session_closeout.py` (`unfinished_entry`, `cmd_closeout`, the docstring, the
fixtures), `scripts/new_project.py` (the S1 entry's `### Next` text), `.claude/skills/closeout/SKILL.md`
(step 1.2), `.claude/skills/project-launch/SKILL.md` (Planning), `AGENTS.md` (the emergency close),
`README.md` (walkthrough step 7), `docs/standards/session_handoff_standard_v2.0.md` (§7),
`docs/governance/gate_suite_runbook.md` (`session-closeout-selftest`, `session-closeout`),
`docs/orchestration/knowledge/reference_session_closeout.md`, `sprint/story-tracker.md` (TMPL-5.7)

### Context

TMPL-5.4's third run closed the probe's S1 on an entry still headed `emergency checkpoint`, written
in the second run, its Status saying the closeout of S1 was not completed and the initializer's
`### Next` standing in for a kickoff the closeout had just written. The session had offered to
rewrite the entry first; the Chair typed `/closeout`, which runs the forked skill at once, so the
main session never had the turn. The skill's precondition, that the session commit its entry
first, was left to the session; the fork's check accepted any entry holding Status, Done and
Blockers, and the gate read only the heading's number. The README's step 7 said the session first
commits what it learned, true only when the closeout is asked for in words.

### Decision

- **The closeout gate refuses the open record (Chair).** `--closeout` fails as `emergency-entry`
  when the entry it closes has a title starting `emergency checkpoint`, in any case, and as
  `next-section` when the entry holds a `### Next` heading outside fenced code. Only the newest
  entry is read, and only at the closeout: at a cold start, and in `--check`, the emergency entry is
  the true record.
- The heading is the marker, since `AGENTS.md` prescribes it; the Status sentence is prose and is
  not read.
- The closeout skill's step 1.2 returns such an entry to the session before writing the pair; the
  launch's planning stage brings S1's entry up to date before closing out; `AGENTS.md`'s emergency
  close says the completing session rewrites the entry; the README's step 7 says a typed
  `/closeout` starts at once; the initializer's `### Next` says it goes before S1's closeout.
- Ships in `v2.0.0` before TMPL-2.4. A new refusal, so MAJOR on its own
  ([[reference_template_versioning]]): every project's first closeout now removes the `### Next`.

### Verification

Nine fixtures in `session-closeout-selftest`; seven broken variants each caught by the fixture
written for it. On a scratch clone of the real tree with the S12 pair scaffolded: the S11 heading
set to `emergency checkpoint` refused by `--closeout` as `emergency-entry`, and passed by `--check`
and `--verify`; a `### Next` added refused as `next-section` by `--closeout` alone; restored,
neither; with the rule left out of `--closeout`, the emergency heading passed it.

### Enforcement

`session-closeout-selftest` and `session-closeout`; the closeout skill's step 1.2, held by
`skill-scan`; [[reference_session_closeout]].

---

## Decision 2026-10-24-003: At adoption, a project's documents are approved as they stand

**Date:** 2026-10-24
**Made By:** Chair (S11): approval as-is, chosen over a skip of both and a full launch review; the
form by the AI, proved on scratch adoptions
**Status:** APPROVED
**Builds:** TMPL-2.4's open question
**Affects:** `TEMPLATE_GUIDE.md` (Taking a newer template release: adopting `v2.0.0` with real
epics), `.claude/skills/project-launch/SKILL.md` (Where each stage stands: another name),
`sprint/story-tracker.md` (TMPL-2.4)

### Context

The three projects hold real epics and documents their owner approved before `v2.0.0`'s form
existed: Supplier_Research_Dev a PRD at Rev E and no architecture, Comfy a PRD at 1.4 and an
architecture at 1.0, PocketGames a PRD at 1.4 and an architecture at 1.0, none with `authority:`,
`status:` or a version log. The approval gate (decision 2026-10-23-020) refuses every commit of
such a project, the adoption's own included, and the updater writes neither folder. No decision
covered bringing an existing project's documents in.

### Decision

- **Approve as they stand, in the adoption commit (Chair).** Each document the project has been
  built from claims the project's scope (`product requirements — <project>`, `architecture —
  <project>`) with `implements: []`, `verified:` and `status: approved`; ends with a version log
  whose one row opens at the version it states, 1.0 where it states none in numbers, a `fact:`
  citing the approval; and the project's log holds the approval decision, its `**Affects:**`
  naming each path in a code span. The content is unchanged.
- **The architecture's `prd:` is the PRD's version**, quoted: approving both as they stand is the
  Chair's confirmation that the architecture stands against the PRD as it now is, though it was
  written against an earlier one.
- **No architecture is the Chair's skip**, logged with its reason, as at a launch.
- **The files keep their names**, which their trackers and decisions cite; the launch skill reads
  the folder's one document as the file it names.
- The updater is unchanged; `TEMPLATE_GUIDE.md` names the step, and the suite's refusal is what
  prompts it.

### Verification

On a scratch `v2.0.0` cut from `dee7385`, a clone of each project taken to it by the release's own
updater: every path applied with no conflict, every persona converted, and the suite's one failing
hook `doc-authority-scan`, its only violations the two `approval` lines. The as-is approval, written
by a script, then passed the whole suite; committed and stamped, the suite passed again, and
`session-verify` passed in two of the three, the third (Comfy) failing exactly as its unadopted
clone does, its S4 never closed out.

### Enforcement

`doc-authority-scan`'s approval rule, unchanged; [[reference_doc_authority]].

---

## Decision 2026-10-24-004: The team's orchestration is a main-session skill over gated artifacts

**Date:** 2026-10-24
**Made By:** Chair (S12, the TMPL-3.1 design session): the orchestrator in the main session, the
artifacts committed per story, one story end to end, the law in a new standard; the mechanics by
the AI, to be settled in TMPL-3.2
**Status:** APPROVED
**Builds:** TMPL-3.1, the orchestration of decision 2026-10-22-003
**Affects:** `sprint/story-tracker.md` (TMPL-3.1 done, TMPL-3.2 scoped). To be built in TMPL-3.2:
`docs/standards/team_standard_v1.0.md` (new), `.claude/skills/story/SKILL.md` (new), the
`story-artifacts` gate (new)

### Context

Decision 2026-10-22-003 made the team role subagents handing off through gated artifacts, never
conversation, with the operator's checkpoints a written list of triggers, orchestrated as a saved
workflow invoked one story at a time. Two facts bound the shape ([[reference_claude_code_skills]]):
no subagent has AskUserQuestion, so only the main session can stop and ask the operator; and a
forked skill sees none of the conversation.

### Decision

- **The orchestrator is a skill in the main session (Chair):** `/story <ID>` runs one story. It
  calls each role as a subagent of the roster's agent type, so the role's prompt is the persona,
  passing it the path of its input artifact; it runs the gate on the artifact the role writes, and
  commits it as a checkpoint before the next role starts. A role the story needs and the roster
  lacks stops the run and names it; the team-selection skill activates it.
- **The artifacts live in the repository (Chair):** `docs/stories/<ID>/`, one committed file per
  stage (`brief`, `design`, `build`, `verify`, `review`, `security`, `docs`, `release`), each with
  frontmatter a gate reads: the story, the role, its input, a status of `pass`, `fail` or
  `needs-operator`, and the triggers it declares. A build's artifact records the commits and the
  checks it ran; the change itself is in the codebase.
- **One story runs end to end (Chair):** it stops only at a review trigger (decision 2026-10-24-005)
  or when a gate still fails after three attempts running, and then reports what it stopped on.
- **The law has its own home (Chair):** a new standard, `docs/standards/team_standard_v1.0.md`, an
  authority with a version log, holds the roles, stages, artifacts and triggers, and a project may
  extend its triggers; `/story` is the procedure and `story-artifacts` the enforcement, the
  repository's usual split.
- **MINOR**, `v2.1.0` (decision 2026-10-22-003): the gate judges only `docs/stories/`, which no
  project holds until it opts in, so adopting asks nothing of a project.

### Consequences

- TMPL-3.2 builds the standard, the skill and the gate, with fixtures proved against broken
  variants, the runbook sections, `AGENTS.md`'s skills table and the README's catalog, then proves
  them on one project through a story end to end. It waits on TMPL-4.2, whose stack profile gives
  the build stage its gates and the trigger detection its paths.

### Enforcement

To be built in TMPL-3.2: the `story-artifacts` gate and `skill-scan` over `/story`.

---

## Decision 2026-10-24-005: The review triggers, detected from the diff and declared by the roles

**Date:** 2026-10-24
**Made By:** Chair (S12, the TMPL-3.1 design session): the four triggers added and the detection;
the recording of an approval by the AI, to be settled in TMPL-3.2
**Status:** APPROVED
**Builds:** TMPL-3.1, the review-trigger list of decision 2026-10-22-003
**Affects:** `sprint/story-tracker.md` (TMPL-3.2 scoped). To be built in TMPL-3.2: the triggers in
`docs/standards/team_standard_v1.0.md`, their detection in the `story-artifacts` gate

### Context

Decision 2026-10-22-003 listed the points at which a story stops for the operator: a new
dependency, a schema change, an auth or crypto change, an external service, a cost, a security
finding the auditor cannot clear, anything a gate cannot judge. A list that only the roles apply
passes silently when a role forgets.

### Decision

- **Eleven triggers (Chair):** the seven, plus a deploy or release (anything that ships to users:
  a production deploy, a store submission, a public tag), a change to the project's own gates,
  hooks, CI or branch protection, a change that deletes data or migrates it lossily, and a license
  change or a dependency whose license breaks the project's policy.
- **Detected two ways (Chair):** from the diff where the change shows it (dependency manifests and
  lockfiles, migration and schema paths, auth and crypto paths, infrastructure-as-code, CI and hook
  files, the license file), the paths per stack coming from TMPL-4.2's stack profile; and declared by
  a role in its artifact's frontmatter where no path can show it (an external service, a cost, a
  finding not cleared, a judgement no gate makes).
- **The operator's approval is recorded in the story's folder** by the orchestrator, with the
  trigger, what was approved and the operator's words; a story's release, and its Done, is refused
  while any trigger it hit has none.
- A project adds its own triggers to the standard's list; it removes none.

### Enforcement

To be built in TMPL-3.2: the `story-artifacts` gate's trigger rules, each with fixtures proved
against broken variants.

---

## Decision 2026-10-24-006: The team's role map, by story type

**Amended 2026-10-24 (S15, the Chair, decision 2026-10-24-011):** a review or security finding is
fixed or answered by the Chair in `docs/code_review_log.md`; it pauses the story only until the
Chair responds, never until the code changes.

**Date:** 2026-10-24
**Made By:** Chair (S12, the TMPL-3.1 design session): every library role covered by story type,
`devops-engineer` shipping, the map approved as drafted by the AI
**Status:** APPROVED
**Builds:** TMPL-3.1, the artifact each role produces and the gate that judges it
**Affects:** `sprint/story-tracker.md` (TMPL-3.2 scoped). To be built in TMPL-3.2: the map in
`docs/standards/team_standard_v1.0.md`

### Context

The library holds the team of decision 2026-10-23-004 across five areas, more than the software
lifecycle decision 2026-10-22-003 named, and no release manager or code reviewer; the reviewer's
brief is TMPL-4's.

### Decision

- **A story has a type, set in its brief, that picks its stages and roles.** The verifier and the
  reviewer are never the builder. A security stage joins any type whose story hits an auth, crypto
  or external-service trigger.

| Type | brief | design | build | verify | review | security | docs | release |
|------|-------|--------|-------|--------|--------|----------|------|---------|
| software | `product-manager` or `business-analyst` | `solution-architect`, `ux-designer` for UI | `software-engineer`, `frontend-engineer`, `backend-engineer` or `web-developer` | `qa-engineer` | the code reviewer | `security-engineer` | `technical-writer` | `devops-engineer` |
| data | `business-analyst` | `solution-architect`, or `data-platform-engineer` on the Microsoft stack | `data-engineer`, `analytics-engineer`, `bi-developer`, `ml-engineer`, `data-scientist`, `data-analyst` or `reporting-analyst` | `data-quality-engineer` | the code reviewer | `security-engineer` | `technical-writer` | `devops-engineer` |
| document | `business-analyst` or `product-manager` | `information-architect` | `business-writer` or `technical-writer` | `editor` | `document-reviewer` | — | — | `document-controller` |
| game | `game-producer` | `game-designer`, with `narrative-designer` and `game-ui-ux-designer` | `game-engine-developer`, `game-artist` or `game-audio-designer` | `game-qa-tester` | the code reviewer, for code | — | — | `devops-engineer` |
| media | `product-manager` | — | `generative-video-engineer`, `image-video-editor` or `blender-artist` | `image-video-editor`, not the builder | — | — | — | `devops-engineer`, when something ships |

- **Outside the per-story flow:** `delivery-manager` writes the plan, judged by the approval gate
  and the tracker's rules; `framework-maintainer` writes the template's gates, judged by their
  self-tests against broken variants.
- **The judging gates, by stage.** Every artifact: `story-artifacts`, its shape, its input passing
  before the role started, the stage order. Brief: numbered acceptance criteria, each PRD reference
  resolving. Build: TMPL-4.2's stack profile (tests, linter, types, coverage, complexity) and the
  suite; for data, the data tests observed; for assets, the architecture's budgets. Verify: every
  acceptance criterion mapped to a check observed passing. Review and security: every finding
  resolved, or a trigger; gitleaks and the dependency audit stay in the suite. Docs, and a
  document's release: `doc-authority-scan`. Release: the CI run observed green, its ID recorded.
- **`devops-engineer` ships (Chair);** no release-manager persona.
- **The code reviewer's slot is TMPL-4.1's**, which drafts the reviewer and the auditor briefs; a
  code story's review stage waits for it, which is why TMPL-3.2 waits on TMPL-4.2.

### Enforcement

To be built in TMPL-3.2: the `story-artifacts` gate over the map; the persona lint over any persona
it adds.

---

## Decision 2026-10-24-007: The coding standard's core limits, proved against known-good and known-bad code

**Amended 2026-10-24 (S15, the Chair, decision 2026-10-24-011):** the limits and their evidence
stand; what follows a finding changed. A changed function over a limit, a clone or a coverage
shortfall is a finding the code review log records with the Chair's response, never a refusal that
forces a code change, and the exceptions file merges into the log: the Chair's acknowledgement is
the exception, its category an optional note. An answered finding pauses nothing again unless it
gets worse.

**Date:** 2026-10-24
**Made By:** Chair (S13, the TMPL-4.1 design session): the reference codebases, every limit below and
its scope, on the evidence of the session and of the specialized reviewer agent
**Status:** APPROVED
**Builds:** TMPL-4.1, the mechanical layer of decision 2026-10-22-003
**Affects:** `sprint/story-tracker.md` (TMPL-4.1 done, TMPL-4.2 scoped). To be built in TMPL-4.2:
`docs/standards/coding_standard_v1.0.md` (new), the exceptions file, the gate

### Context

Decision 2026-10-22-003 asked for a core of numbers, proved against a known-good and a known-bad
codebase before adoption, since this standard is the hardest thing in the framework to unwind. The
Chair asked that it be language-agnostic as far as possible, with Rust cleanly supported, and an
industry standard rather than a fit to the few codebases the framework holds, which agents wrote.

### Decision

- **The reference codebases (Chair).** Known-good: ripgrep 14.1.1 (Rust), packaging 24.1 (Python),
  zod v3.23.8 (TypeScript), pinned at their tags. Known-bad: the Gilded Rose and Tennis refactoring
  katas, the industry's teaching examples of bad code, in the same three languages. All measured,
  never run. The framework's own code was measured only to report what adopting would mean.
- **Per function a change adds or edits (Chair):** cyclomatic complexity at most 15, at most 60
  code lines (blanks and comments excluded), at most 5 parameters.
- **Duplication (Chair):** a change adds no clone of existing code, at jscpd's defaults of 50
  tokens and 5 lines with its size caps lifted, unless the clone is a recorded exception; the
  codebase's duplication rate never rises.
- **Coverage (Chair):** at least 80% of a change's new lines covered by tests, SonarQube's gate.
- **Tests (Chair):** complexity at most 10, at most 100 code lines; duplication in tests reported,
  not gated; test helpers held to the production limits.
- **File length (Chair):** a reviewer signal, not a gate: a change that grows a file past 500
  production lines is flagged to the code reviewer.
- **Scope and exceptions (Chair):** only code a change adds or edits is judged. An edited function
  already over a limit is brought under it or recorded at its current value. An exception is an
  entry in a checked-in exceptions file naming the function, the metric, its value, a category
  (data or table, parser or state machine, exhaustive dispatch over a closed set, generated code,
  measured hot path) and the reason; the code reviewer approves each, and the gate fails a function
  that grows past its recorded value. A tool's own suppression comment counts only with a matching
  entry.
- MINOR, `v2.1.0` (decision 2026-10-22-003): a stack profile a project opts into.

### Evidence

The published defaults: NIST SP 500-235 §2.5 (McCabe's limit of 10, "limits as high as 15 have been
used successfully as well"); SonarQube's Sonar way gate (new-code coverage at least 80%, new-code
duplication at most 3%); clippy (7 arguments, 100 lines); pylint (5 arguments, 50 statements, 1,000
module lines); ESLint (complexity 20, 50 lines per function). Measured with lizard and jscpd, the
Rust and TypeScript figures from copies the reviewer agent repaired where lizard fails
(decision 2026-10-24-008):

- **Complexity 15:** about 20 of some 2,800 known-good functions exceed it, about half of which the
  reviewer judged should have been split (ripgrep's `from_low_args` at 41, zod's `ZodString._parse`
  at 53), the rest parsers, state machines and exhaustive dispatch. It catches Gilded Rose's
  `update_quality` (19) in all three languages, Tennis 2 (30 to 40) in all three, and Tennis 1 and 6
  in TypeScript (16). At 20 Gilded Rose passes; at 10 some 66 known-good functions exceed, many only
  by Rust's `?`.
- **60 code lines:** about 20 known-good functions exceed it, about 12 judged should split; it
  catches Tennis 2 in all three languages and Tennis 6 in TypeScript. At 80 it catches no kata.
- **5 parameters:** one known-good function exceeds it (packaging's `_cmpkey`); ripgrep never does.
  It catches no kata: a design signal, not a kata detector.
- **Duplication:** packaging 0%, zod 2.88% in production code, ripgrep 87 clones, mostly
  deliberate parallel implementations; Gilded Rose's 8-line in-function clone in Rust and TypeScript
  is caught at the 5-line default and missed at 10. A percentage judges a small change noisily, so
  the gate judges new clones.
- **Tests:** one known-good exception each at complexity 10 (ripgrep's harness, zod's
  exhaustiveness switch) and one at 100 lines (zod's email table, a fixture candidate).
- **File length:** a gate would fail all three references (ripgrep 17 of 87 files over 500, 6 over
  1,000; zod's `types.ts` 4,561 lines).
- **What a mechanical limit cannot catch:** Tennis 3 (complexity 8, 14 lines; cryptic names, nested
  ternaries, an arithmetic trick) passes every limit; only the reviewer catches it.
- **Coverage is not proved here:** proving it means running the reference code, which the session
  did not do; TMPL-4.2 proves it on a project.
- **Our code, for adoption:** at these limits the template's scripts have 25 of 304 functions over,
  Comfy 13 of 125, PocketGames 23 of 804 (lizard, unrepaired), which is why the gate judges changed
  code, not the codebase.

### Enforcement

To be built in TMPL-4.2: the coding-standard gate over changed code, its fixtures proved against
broken variants; [[reference_coding_standard_calibration]].

---

## Decision 2026-10-24-008: The coding standard's measurement is proved per language, and each stack maps it to tools

**Date:** 2026-10-24
**Made By:** Chair (S13): that each language's measurer proves itself; the mapping rule as drafted by
the AI from the reviewer agent's findings
**Status:** APPROVED
**Builds:** TMPL-4.1, the per-stack tool-mapping rule of decision 2026-10-22-003
**Affects:** `sprint/story-tracker.md` (TMPL-4.2 scoped). To be built in TMPL-4.2: the stack
profiles, their measurement fixtures

### Context

The specialized reviewer agent found that lizard 1.17.10, the multi-language measurer the session
began with, silently fails to measure much Rust and TypeScript: in ripgrep it measured 1,196 of
2,673 functions, none of `crates/ignore/src/dir.rs`'s 58 (reproduced by the session); it drops a
TypeScript class method with a return type (reproduced), so zod's `ZodString._parse` and the Tennis
kata's complexity-40 method were invisible; it ignores Python's `match`; and its `#lizard forgives`
comment drops a function from every metric with no reason recorded. jscpd skips files over 1,000
lines or 100 KB by default and finds exact copies only. A gate that measures nothing reports green.

### Decision

- **A measurer proves itself (Chair).** Each stack's tool for the function limits passes a
  measurement fixture of its language's hard cases (Rust lifetimes and raw strings, a TypeScript
  method with a return type and a bare `catch`, Python's `match`) and, on every run, a recall check:
  it finds as many functions in each changed file as the file defines, or the gate fails. Tool
  versions are pinned.
- **The mapping rule.** Each stack's profile names one pinned tool per slot: the function measurer,
  the clone detector, the formatter, the linter, the type checker, coverage, the dependency and
  license audit, and the trigger paths of decision 2026-10-24-005. The numbers are the core's
  (decision 2026-10-24-007), the same in every stack; a tool is configured to them, stricter or
  equal, never looser. A stack with an empty slot is not adoptable. The planning session chooses
  the profile.
- **The starting candidates, for TMPL-4.2 to prove:** Rust: rustfmt, clippy (5 arguments, 60
  lines), the compiler, cargo-llvm-cov, cargo-audit and cargo-deny. Python: ruff format, ruff
  (complexity 15, 5 arguments), mypy in strict mode, coverage.py with diff coverage, pip-audit.
  TypeScript: prettier, ESLint (complexity 15, 60 lines skipping blanks and comments, 5
  parameters), `tsc --strict`, vitest coverage, npm audit with a license check. jscpd with its caps
  lifted for clones in all three. lizard only where it passes its fixture.
- **Generated code** is declared by path in the profile; a generated-code marker anywhere else is
  refused.

### Enforcement

To be built in TMPL-4.2: each profile's fixture and the recall check in the gate's self-test, proved
against broken variants; [[reference_coding_standard_calibration]].

---

## Decision 2026-10-24-009: The coding standard's judgement page and its reviewer and auditor briefs

**Amended 2026-10-24 (S15, the Chair, decision 2026-10-24-011):** the code reviewer and the security
auditor record every finding in `docs/code_review_log.md` with the change made in response; a
blocking finding, or an open high or critical one, pauses the story until the Chair responds there,
never until the code changes. The page's last line and the persona (version 2) say so.

**Date:** 2026-10-24
**Made By:** Chair (S13): the auditor a brief for `security-engineer`, the reviewer a new persona,
the page and both briefs as drafted by the AI from the reviewer agent's draft
**Status:** APPROVED
**Builds:** TMPL-4.1, the judgement layer of decision 2026-10-22-003 and the code reviewer's slot
left by decision 2026-10-24-006
**Affects:** `sprint/story-tracker.md` (TMPL-4.2 scoped). To be built in TMPL-4.2:
`.claude/rules/code-quality.md` (new), `personas/code-reviewer.md` (new); the audit brief with the
stages, in TMPL-3.2

### Decision

- **The judgement page**, `.claude/rules/code-quality.md`, path-scoped to the stack's code files,
  opens with `CONSTITUTION.md` §4A, then holds what no gate checks: read the design before the
  code; one reason to change per function; names that say what a thing is for, and no repeated
  literal; policy in a table or data rather than in branching; a helper instead of a copy, near-copies
  the clone detector misses included; errors explicit, never swallowed; comments that say why; the
  codebase's own conventions; no speculative generality, and dead code deleted; no limit gamed by
  hiding logic in closures, part1 and part2 splits or mode flags, but a split by responsibility; an
  exception only as an entry in the exceptions file.
- **The code reviewer (Chair: a new library persona, `code-reviewer`).** Never the implementer; never
  edits the code. Reads every changed function whole, the callers and callees it crosses, the
  story's acceptance criteria, the standard and the gate's output, and first checks that the gate
  measured the change, an unmeasured function being a blocking finding. Judges cohesion, naming,
  near-copy duplication, attempts to game a limit, every new exception against its category, and
  whether tests assert behaviour. Does not re-argue a number the gate settled or restyle what the
  formatter owns. Reports each finding with its location, severity (blocking, fix in this change,
  minor), evidence and the shape of the fix; blocks only on a violation of the standard, unmeasured
  code, an unjustified exception or a new clone, never on taste; passes when no blocking finding
  remains and the gates are green on the final revision.
- **The security audit (Chair: a brief for `security-engineer`, no new persona),** the security stage
  of decision 2026-10-24-006: the change read against the OWASP Top 10 and the CWE Top 25 for its
  stack, secrets, authorization, input handling and data flows, the dependency and license audit's
  results; each finding with its exploit path, severity and fix; the stage fails while a high or
  critical finding is open, and a finding it cannot clear is a trigger (decision 2026-10-24-005).

### Enforcement

To be built: the page held by the rule gate (`session-closeout-check`'s rule lint), the persona by
the persona lint, in TMPL-4.2; the audit brief with the stages in TMPL-3.2.

---

## Decision 2026-10-24-010: TMPL-4.2 split into the law, the gate's core, and one story per stack

**Date:** 2026-10-24
**Made By:** Chair (S14): the split and its order, the Rust toolchain decided at TMPL-4.4
**Status:** APPROVED
**Builds:** TMPL-4.2's scope, from decisions 2026-10-24-007 to 2026-10-24-009
**Affects:** `sprint/story-tracker.md` (TMPL-4.2 rescoped; TMPL-4.3, TMPL-4.4 and TMPL-4.5 opened;
TMPL-3.2's dependency)

### Context

TMPL-4.2 held the standard, three stack profiles, the gate, the judgement page, the reviewer persona
and a proof on a project: more than one session, which the sprint standard's session-sized rule
forbids. The Rust toolchain is not installed on the operator's machine.

### Decision

- **TMPL-4.2:** the law and the judgement layer, `docs/standards/coding_standard_v1.0.md`,
  `.claude/rules/code-quality.md` and `personas/code-reviewer.md`.
- **TMPL-4.3:** the gate's language-neutral core (the changed functions from the diff, the limits,
  the recall check, the exceptions file, the clone check, coverage of new lines) with the Python
  profile, whose measurer reads Python's own `ast`, so no tokenizer can skip a function; proved on a
  scratch copy of Comfy.
- **TMPL-4.4:** the Rust profile, proved on a scratch copy of PocketGames; whether the toolchain is
  installed locally or proved in CI only is decided at its start.
- **TMPL-4.5:** the TypeScript profile, proved on fixture code, since no project holds TypeScript.
- **TMPL-3.2** waits on TMPL-4.3, the first working profile, not on all three.

### Enforcement

`session-closeout-check`'s dependency order over the tracker.

---

## Decision 2026-10-24-011: The coding standard advises and documents, and its gate as built

**Date:** 2026-10-24
**Made By:** Chair (S15): that the standard advises and documents and never blocks a code change, the
Chair always able to acknowledge and proceed; an audit log of findings, changes and the Chair's
responses; a finding pausing until logged; one log per project; the exceptions file merged into it;
the reviewer and the auditor under the same rule; the template not opted in; coverage by the
project's own tests; findings on changed lines only; the audit on a manifest change and in CI. The
gate's mechanics by the AI
**Status:** APPROVED
**Amends:** 2026-10-24-006 (review and security findings), 2026-10-24-007 (refusal and the
exceptions file), 2026-10-24-009 (the reviewer's and the auditor's blocking)
**Builds:** TMPL-4.3
**Affects:** `docs/standards/coding_standard_v1.0.md` (Purpose, §1, §3, §4 replaced by the code review
log, §5, §7), `docs/governance/gate_suite_runbook.md` (`code-standard-selftest`, `code-standard`,
`code-standard-range`), `scripts/code_standard.py` (new), `.pre-commit-config.yaml` (three hooks),
`.github/workflows/gates.yml` (the range step), `personas/code-reviewer.md` (version 2),
`.claude/rules/code-quality.md` (its last line), `docs/orchestration/knowledge/reference_code_review_log.md`
(new), `docs/orchestration/knowledge/reference_coding_standard_calibration.md`, `sprint/story-tracker.md`
(TMPL-4.3)

### Context

As TMPL-4.3 was built to decision 2026-10-24-007, which refused a change over a limit unless an
exceptions file recorded it, the Chair set the rule: the standard advises and documents at a
minimum and is never a blocker; the Chair can always acknowledge and proceed without forcing code
updates; and an audit log of code review records the findings, the changes and the Chair's response.

### Decision

- **Advise and document, never force (Chair).** Every finding is shown and recorded; none requires a
  code change.
- **A finding pauses until logged (Chair).** The commit, or the story, waits until
  `docs/code_review_log.md` holds a row for it with the Chair's response, "acknowledged, proceed"
  being enough. A row answers its place and rule at its value and below; a finding that gets worse
  is asked again. A hook cannot safely write into the commit it judges, so the gate prints the rows
  to append and the same commit carries them.
- **One log per project (Chair):** a table, Date, Change, Where, Finding, Source, Change made, Chair's
  response, appended to and never edited. A base row changed or removed is the one thing no response
  clears.
- **The acknowledgement is the exception (Chair):** no exceptions file; a category is a note in the
  response. A suppressing comment on a changed line is a finding of its own.
- **The reviewer and the auditor under the same rule (Chair):** their findings in the same log, a
  story pausing only until the Chair responds.
- **The plan (Chair):** a project opts in with `code-profile.yaml` (profile, code and test paths,
  generated paths, its coverage command and report, its manifests and license policy); the template
  does not opt in, its scripts having 25 functions over the limits; coverage is measured by the
  project's own tests in its own environment; ruff, mypy `--strict` and ruff format findings count on
  changed lines only; the audit runs when a manifest changes and over every pushed range.
- **As built (AI):** `scripts/code_standard.py`, hooks `code-standard-selftest`, `code-standard` (the
  staged change) and `code-standard-range` (manual, `CODE_STANDARD_RANGE`, run by CI over the push's
  range). The Python measurer reads Python's own `ast`, counting the calibration measurer's decision
  points plus `case`, which it missed; recall compares its functions with the tokenizer's `def`
  count. Tools pinned in the hook's environment (ruff 0.6.9, mypy 1.11.2, pip-audit 2.7.3) and jscpd
  4.0.5 through npx; a tool that cannot run is an `unmeasured` finding, never a pass. Ruff runs
  without its own limit rules (C901, PLR0913), decision 2026-10-24-008's candidate configuration
  changed, since the measurer holds §2 and the proof showed ruff asking the same finding twice. The self-test
  holds the gate's numbers equal to the standard's §2 and the gate's own functions within the
  production limits.

### Verification

Fifty-nine fixtures in `code-standard-selftest`; twenty-five broken variants of the script, one per
rule and reader, each caught by a failing fixture. On a scratch copy of Comfy with this gate, its
config and a profile, through `pre-commit run code-standard` on the staged change: a function at
complexity 17 paused the commit; the same with a log row answered by the Chair passed, no code
changed; made worse, to 19, paused again; a copy of an existing function paused it as `clone 9`; a
`noqa: C901` comment paused it as `suppression`; a compliant typed, formatted and tested change
passed; a compliant change that edited a base row of the log was refused; untyped, unformatted and
untested lines paused it as `format`, `types` and `coverage`. The first run also showed ruff's C901
reporting the measurer's finding a second time, so ruff's limit rules are off. Over a committed
range through `code-standard-range`, as CI runs it: a compliant range passed, noting the audit had
no manifest to judge; a six-parameter function paused it.

### Enforcement

`code-standard-selftest`, `code-standard` and `code-standard-range`; [[reference_code_review_log]].

---

## Decision 2026-10-24-012: Rust and Bevy are the default stack, and the Rust profile ships in v2.1.0

**Date:** 2026-10-24
**Made By:** Chair (S16): Rust the go-to language and Bevy for games whenever possible; the Rust
profile in this version's build requirements, Bevy a requirement of it; TMPL-3.2 split; Comfy for
the team's live proof
**Status:** APPROVED
**Builds:** TMPL-3.2's scope; TMPL-4.4's scope; opens TMPL-3.3 and TMPL-4.6
**Affects:** `.claude/skills/project-launch/SKILL.md` (Architecture: the default stack proposed
first), `sprint/story-tracker.md` (TMPL-3.2 rescoped, TMPL-3.3 and TMPL-4.6 opened, TMPL-4.4's Bevy
requirement)

### Context

The Chair builds future projects in Rust, and games in Bevy, PocketGames being the first. The
coding standard's Rust profile (TMPL-4.4) was one of three profiles planned for `v2.1.0` with nothing
holding it there. Bevy's systems take their resources and queries as parameters, PocketGames' up to
eleven, and Bevy projects commonly allow clippy's `too_many_arguments` and `type_complexity`, so a
Rust profile blind to Bevy would report nearly every system. TMPL-3.2 held a standard, a gate, a
skill and a live proof, more than one session.

### Decision

- **The default stack (Chair):** the launch's architecture stage proposes Rust first, and Bevy for a
  game, unless a requirement rules them out; choosing another stack is a decision with its reason.
  The library's `game-engine-developer`, Rust and Bevy only, is the default it serves, not a gap.
- **The Rust profile is required for `v2.1.0` (Chair),** and supporting Bevy cleanly is a
  requirement of it. How a Bevy system's parameters and the lints Bevy projects allow are measured
  is settled with the Chair at TMPL-4.4's start, the numbers of decision 2026-10-24-007 never
  loosened without a decision.
- **The release is a story (AI):** TMPL-4.6, `v2.1.0` cut and the projects taken to it, waits on
  TMPL-3.3, TMPL-4.4 and TMPL-4.5.
- **TMPL-3.2 split (Chair):** 3.2 the team standard and the `story-artifacts` gate; 3.3 the `/story`
  skill, its listings and the live proof on a scratch copy of Comfy (Chair), its roles run as
  general-purpose subagents carrying each persona's prompt from this conversation, since roster
  agents load only in a session opened in the project.

### Enforcement

`session-closeout-check`'s dependency order over the tracker holds TMPL-4.6 behind TMPL-4.4.

---

## Decision 2026-10-24-013: The team standard and the story-artifacts gate as built

**Date:** 2026-10-24
**Made By:** AI (S16), within decisions 2026-10-24-004, 2026-10-24-005, 2026-10-24-006 and
2026-10-24-011
**Status:** APPROVED
**Builds:** TMPL-3.2
**Affects:** `docs/standards/team_standard_v1.0.md` (new), `scripts/story_artifacts.py` (new),
`.pre-commit-config.yaml` (two hooks), `docs/governance/gate_suite_runbook.md` (`story-artifacts-selftest`,
`story-artifacts`), `AGENTS.md` (the governance map), `README.md` (the standards),
`docs/orchestration/knowledge/reference_story_artifacts.md` (new), `sprint/story-tracker.md` (TMPL-3.2)

### Context

Decisions 2026-10-24-004 to -006 fixed the orchestration, the triggers and the role map, and left
the artifacts' exact shape and the gate's reading to the build.

### Decision

- **One frontmatter for every stage file:** `story`, `stage` (its file's name), `role`, `input` (the
  stage just before, `none` for the brief), `status` (pass, fail, needs-operator) and `triggers`;
  the brief adds `type` and numbered acceptance criteria, the build its `commits`, verify a checks
  table by criterion, review and security a findings table written as the code review log writes a
  finding, the release its CI `run`. The Chair's approvals are a table in `approvals.md`.
- **The law is read, not copied:** the gate reads the role map (§3) and the trigger list (§4) from
  the team standard at every run, so a project that adds a trigger or a persona to a stage, by a
  decision, is judged by its own copy; a section that cannot be read stops the gate (exit 2), never
  reads as nothing to check.
- **The release is always a trigger**, a deploy or release, so every story that ships waits for the
  Chair's approval before it closes. A hit trigger is judged once the story releases or is Done;
  before then it waits for the Chair as the story does.
- **A finding is judged when the story moves past its stage:** a review or security finding must be
  answered in the code review log before any later stage exists.
- **Optional stages:** a game's review and a media story's release; every other stage is required in
  order, a security stage joining a story that hits an auth or crypto change or an external service.
- **The gate's own functions meet the coding standard's production limits**, held by its self-test,
  as `code_standard.py`'s are.

### Verification

Thirty-eight fixtures in `story-artifacts-selftest`; twenty-seven broken variants, one per rule and
reader, each caught by the fixture written for it. The first variant run passed every variant
through one crash: the runner's Python lacked PyYAML, so the frontmatter fixtures all raised. Rerun
with PyYAML, five variants passed, each because its failing fixture also tripped a neighbouring
rule; the five fixtures were rewritten to isolate their rule, and all twenty-seven are caught. The
same rerun confirmed `code_standard.py`'s twenty-five, its profile fixture among them. On the real
tree, with no `docs/stories/`, the gate passes.

### Enforcement

`story-artifacts-selftest` and `story-artifacts`; [[reference_story_artifacts]].


---

## Decision 2026-10-24-014: The writing standard, its gate and a humanizer join v2.1.0

**Date:** 2026-10-24
**Made By:** Chair (S17): the need, the voices assignable to an agent, the guardrails named, its
release `v2.1.0`, its design at S18; the epic's shape by the AI
**Status:** APPROVED
**Builds:** opens TMPL-6
**Affects:** `sprint/story-tracker.md` (epic TMPL-6 opened, TMPL-4.6 waiting on it). To be built
in TMPL-6: `docs/standards/writing_standard_v1.0.md` (new), the prose gate and its hooks (new), the
humanizer skill (new); the em-dash rule of `docs/standards/document_production_standard_v1.0.md`
moved into the new standard, queued in TMPL-6.2

### Context

The Chair's projects forbid machine-sounding writing in prose a session reads at its cold start,
which no gate checks, and agents still produce it: headings and subheadings that read as prose,
symbols no US keyboard types, technical documents that sound like marketing, and production
documents that cite development artifacts (decisions, stories, sessions) meaningless to their
reader. The one rule written into the template, no em dashes, lives in the document production
standard and holds only for produced documents. The Chair pointed to Grammarly's Humanizer as the
model: a voice chosen from built-in ones or made from a sample of the writer's own, and flagged
passages rewritten in it.

### Decision

- **A writing standard (Chair):** the voices and the guardrails in one authority, the procedure in a
  skill and the enforcement in a gate, the repository's usual split.
- **Voices are assigned (Chair):** a document, by its path, and an agent are given the voice they
  must write in; the built-in voices and how a custom voice is made from the Chair's sample are the
  design session's.
- **The guardrails the Chair named,** each mechanical where a pattern can show it: characters off a
  standard US keyboard; headings that read as sentences; marketing and AI phrasing in technical
  writing; development artifacts in documents for a production reader.
- **A humanizer:** a skill that rewrites each flagged passage in the document's voice and shows the
  Chair the change before it is kept.
- **The plan (Chair):** designed with the Chair at S18 (TMPL-6.1), the enforcement model among its
  questions (a refusal, or a pause until the Chair answers as decision 2026-10-24-011 has code do);
  built in `v2.1.0`, TMPL-4.6 waiting on it.

### Enforcement

`session-closeout-check`'s dependency order holds TMPL-4.6 behind TMPL-6; the gate itself is TMPL-6.2.

---

## Decision 2026-10-24-015: The /story skill as built, and what its live proof found

**Date:** 2026-10-24
**Made By:** AI (S17), within decisions 2026-10-24-004, 2026-10-24-011 and 2026-10-24-013; the
Chair's: the plan, the proof's story, its release to a private scratch repository and its runner,
every finding's and the release's answer, and the three gaps opened as stories
**Status:** APPROVED
**Builds:** TMPL-3.3; opens TMPL-3.4, TMPL-2.10 and TMPL-4.7
**Affects:** `.claude/skills/story/SKILL.md` (new), `AGENTS.md` (the skills table), `README.md` (the
catalog), `personas/code-reviewer.md` (version 3), `docs/orchestration/knowledge/reference_story_live_run.md`
(new), `sprint/story-tracker.md` (TMPL-3.3 done; TMPL-3.4, TMPL-2.10 and TMPL-4.7 opened, TMPL-4.6
waiting on them)

### Context

Decision 2026-10-24-004 fixed the orchestration and 2026-10-24-013 the artifacts the gate judges;
the procedure, and its proof on a scratch copy of Comfy run from the template's conversation
(2026-10-24-012), were TMPL-3.3's.

### Decision

- **Roles write; the main session gates, commits and asks.** A role writes only its artifact, and
  the build its code and tests; it never commits and never asks, returning a question as
  `status: needs-operator`. The main session runs `story-artifacts` and the stage's gates itself,
  commits, and stops for the Chair: one committer, and the only place that can ask.
- **A finding reaches the log once, with the Chair's words.** The log is append-only (2026-10-24-011),
  so a row written to await a response could never receive it. The role records findings in its
  artifact; the skill commits it, puts each to the Chair, and appends the row with the answer. A
  finding the Chair wants fixed goes back to the builder, its row naming the fix once committed,
  and verify and review run again. The code reviewer persona, which appended its own rows, is
  version 3.
- **The build commits twice:** the code, then `build.md` naming that commit, which an artifact
  cannot do for its own.
- **A trigger stops the story at the commit that hits it,** and the release always, before its role
  ships.
- **Every role's brief carries the project's `code-profile.yaml`,** since the proof's first brief,
  written without it, planned a check the gate could not count.
- **Three gaps, opened as stories (Chair), each a gate fix in `v2.1.0`, TMPL-4.6 waiting on them:**
  `story-artifacts` checks an input's status and not its age, so a verify and review older than a
  rebuilt build still pass (TMPL-3.4); CI judges a new repository's or branch's first push over
  `HEAD~1..HEAD` alone, leaving every earlier commit unjudged by the commit-msg and coding-standard
  steps (TMPL-2.10); `code-standard` counts the context lines of a `ruff format --diff` hunk as
  unformatted, flagging a correct changed line within three lines of legacy unformatted code
  (TMPL-4.7).

### Verification

`story-probe-s17`, a clone of Comfy taken to a scratch `v2.1.0` by `template_update.py` (no conflict,
the suite green), eight roles activated by the team-selection skill, a Python code profile. CU-4.6,
the per-stage times in `watch_run.py`'s finished-run summary, ran from brief to release, every role a
general-purpose subagent carrying its persona: each artifact committed and passing `story-artifacts`;
the build passing `code-standard`; two review findings put to the Chair, `tests 1` fixed in the
change and the build, verify and review run again, `duplication 6` acknowledged with a later story;
the release stopped until the Chair approved it, then pushed to the private `SaltyBrett/story-probe-s17`,
run 40111133105 green on `gates` and both `birth` jobs. On the closed story, the approval row
removed failed `trigger` and a log row removed failed `finding`. `format_rows` on one unformatted
line flagged seven.

### Enforcement

`skill-scan` over the skill; `story-artifacts` over what it writes; [[reference_story_live_run]].

---

## Decision 2026-10-24-016: The writing standard's voices, built in and custom

**Date:** 2026-10-24
**Made By:** Chair (S18): the built-in set, the three proposed and Grammarly's; a custom voice
keeping its sample and the traits drawn from it; the Chair's custom voice kept in each project,
private. Simple and plain merged, the file's shape and its folder by the AI
**Status:** APPROVED
**Builds:** TMPL-6.1 (design question 1)
**Affects:** none at this decision. To be built in TMPL-6: `docs/standards/voices/` (new), one file
per built-in voice

### Context

Decision 2026-10-24-014 left the built-in voices and the capture of a custom voice to this session.
Grammarly's Humanizer, the model, makes a custom voice from a name and a sample of the writer's own
writing of 200 words or more, kept as its style reference and shared with Grammarly's Paraphraser,
whose preset styles are Academic, Professional, Streamlined, Creative and Simple (Grammarly's help
pages, read 2026-10-24). A voice is how a document sounds. Who reads it, a production or a
development reader, is its audience, assigned apart from the voice (design question 2).

### Decision

- **Seven built-in voices (Chair):** the three proposed, `technical` (READMEs, runbooks, standards,
  references and the development records), `business` (briefings, proposals and statements of work,
  in the document production standard's house style) and `simple` (help text and app copy for a
  general reader); and Grammarly's, `professional`, `academic`, `streamlined` and `creative`, since
  the Chair's later projects will need creative writing and others. Grammarly's Simple and the
  proposed plain voice are one voice, named `simple` (AI).
- **A voice is one markdown file (AI):** `docs/standards/voices/<slug>.md`, holding its traits
  (sentence length, person, register, contractions, what it never does) and its phrase list (design
  question 3). The standard is the law and the voices are its data, as `code-profile.yaml` is the
  coding standard's.
- **A custom voice keeps its sample and its traits (Chair):** the Chair's sample word for word, the
  reference a rewrite imitates, and the traits drawn from it, approved by the Chair before the file
  is kept. A gate counts the sample at 200 words or more; whose writing it is, no gate can tell.
- **A custom voice lives in its project, private (Chair):** the template ships the built-in voices
  only. The updater already leaves alone a file in neither release, a project's custom voice
  included, which the build proves; using the voice in another project is a copy of one file. Its
  capture is the humanizer skill's (design question 6).

### Enforcement

None yet: the voice files and the sample count are TMPL-6's gate.

---

## Decision 2026-10-24-017: Voices and audiences assigned in writing-profile.yaml

**Date:** 2026-10-24
**Made By:** Chair (S18): one profile beside `code-profile.yaml` and no frontmatter; a file no rule
names judged as production; an agent's voice in the same profile, a document's own voice winning.
The default voice, the files in scope and the profile's merge by the AI
**Status:** APPROVED
**Builds:** TMPL-6.1 (design question 2)
**Affects:** none at this decision. To be built in TMPL-6: `writing-profile.yaml` (new, the starter
profile)

### Context

A voice says how a document sounds (decision 2026-10-24-016). Its audience says whether it may cite
development references: decision and story IDs, session numbers, sprint paths, wikilinks, "the
Chair", commit hashes. A development document may; a production document, written for the
project's users or operators, may not. The Chair asked what frontmatter would give and what it
would take, and whether a strict default would discourage adoption.

### Decision

- **One profile, no frontmatter (Chair):** `writing-profile.yaml` at the root holds ordered rules,
  each a list of path globs with a voice and an audience, `production` or `development`; the first
  rule that matches a file wins, and a rule may name a single file. Frontmatter was weighed and
  refused: at S18, 102 of the template's 152 markdown files carry frontmatter that Claude Code or a
  gate already reads and judges (skills, rules, agents, personas, knowledge entries, authorities),
  and an unknown key in a skill fails silently; GitHub shows a README's frontmatter to its
  production reader as a table; and a project's change to the block of a file the template ships
  would conflict at every update. The gate prints any file's voice and audience on request.
- **A file no rule names is production (Chair):** development references are refused unless its
  path is declared development. The starter profile declares every framework development path, so
  a project is born with no finding, and the gate's message prints the rule to add. The audience
  rule fires only on development references; the adoption risk is noise, which keeps the phrase
  lists short and exact (design question 3).
- **An agent's voice is in the same profile (Chair):** an `agents:` map from a roster slug to a
  voice, the persona files unchanged. It is the agent's voice for everything it writes, commit
  messages, pull request descriptions and replies included; in a document the profile assigns, the
  document's voice wins, and the agent's brief says so. The gate judges a document by its own
  voice, since it cannot tell who wrote a file.
- **The details (AI):** the profile's `default` names the voice of a file no rule names,
  `technical` in the starter profile; the gate judges the markdown git tracks; the updater merges
  the profile three-way, so a development path a release adds reaches a project's profile and the
  project's own rules are kept.

### Enforcement

None yet: the profile's reader and the audience rule are TMPL-6's gate.

---

## Decision 2026-10-24-018: The writing guardrails' first lists, mechanical and judged

**Amended 2026-10-24 (S18, the Chair, decision 2026-10-24-020):** the allow list exempts text from
all four mechanical rules, characters and headings included, and a change to it is a gate change
the Chair approves.

**Date:** 2026-10-24
**Made By:** Chair (S18): each rule below and its scope; the lean phrase design over a list per
voice, for the cost of maintaining it; the reviewer finding and the editor fixing. The patterns'
exact form by the AI
**Status:** APPROVED
**Builds:** TMPL-6.1 (design question 3)
**Affects:** none at this decision. To be built in TMPL-6: the writing standard's two phrase tables,
`writing-profile.yaml`'s `allow:` list, `.claude/rules/writing.md` (new),
`personas/document-reviewer.md` and `personas/editor.md` (new versions)

### Context

Decision 2026-10-24-014 named four guardrails; this one sets their first lists, measured on the
template's 152 tracked markdown files at S18 with a probe outside the repository. Twenty distinct
characters off a US keyboard appeared, U+2014 em dash 729 times and box drawing about 720 times in
two standards' diagrams, U+00A7 section sign 259, U+2026 ellipsis 31, arrows 17, emoji 2. Of 1,273
headings, 142 hold a comma or semicolon, 151 run over 8 words, none ends in a full stop, and 105
are a colon and a subtitle, most of them the `## Decision <ID>: <title>` format the gates read.
Thirty-one hits of single AI or marketing words were all legitimate: a browser's audio unlock,
Claude Code's harness, Windows' elevated sandbox, "highest-leverage", Grammarly's preset names. A
bare word is noise; a list holds exact phrases. The Chair asked whether per-voice lists would become
a surface too costly to maintain.

### Decision

- **Characters, every voice and audience (Chair):** the gate refuses any character outside printable
  ASCII, tab and newline, except letters and their accents (Unicode categories L and M), so a name
  keeps its spelling. Code blocks are judged too, a pasted tree or arrow being the same tell. Each
  finding names the character by its code point with its ASCII replacement: U+2014 to a comma, a
  colon or parentheses; curly quotes to straight; U+2026 to three full stops; U+00A7 to "section";
  box drawing to `|` and `+--`. The standard names a character by code point, never by the
  character itself.
- **Headings, every voice and audience (Chair):** a heading reads as a sentence when it holds a
  comma or semicolon, ends in `.`, `!`, `;` or `:`, or runs over 8 words, a code span counting as
  one word. A question mark is allowed. A colon and a subtitle are judgement, since `Step 1: Install`
  and the decision format are sound.
- **Phrases, two tables in the standard (Chair):** an AI table for every voice and a marketing table
  for every voice but `creative`; a voice says only which tables apply to it, and per-voice lists
  wait until a need is shown and a decision adds them. The gate reads the tables from the standard,
  as `story-artifacts` reads the team standard's role map, each phrase in a code span so the
  standard never flags itself. Matching is case-insensitive at word boundaries, outside code spans,
  where a phrase is quoted rather than used. A phrase joins only once seen in an agent's writing, by
  a review finding or a humanizer rewrite, and leaves at its first false positive; each change is a
  `fact:` row. The seed, every form listed:
  - AI: `delve into`, `a testament to`, `it's worth noting`, `it is worth noting`, `it's important to
    note`, `it is important to note`, `plays a pivotal role`, `plays a crucial role`, `plays a vital
    role`, `in the realm of`, `let's dive in`, `I hope this helps`, and `and more`, `and much more`
    or `and so much more` closing a list;
  - marketing: `seamless`, `seamlessly`, `cutting-edge`, `game-changer`, `game-changing`, `unlock
    the power`, `unlock the potential`, `harness the power`, `world-class`, `best-in-class`,
    `next-generation`, `revolutionize`, `supercharge`, `effortless`, `effortlessly`.
- **Development references, production documents only (Chair):** decision IDs with or without a
  project's prefix, story IDs, session numbers, wikilinks, "the Chair", the sprint and orchestration
  paths, and commit hashes of 7 to 40 hex characters holding a digit and a letter. A reference in a
  code span still counts.
- **One allow list per project (Chair):** `allow:` in `writing-profile.yaml`, exact strings exempt
  from the phrase and reference rules, one line per real collision (Amazon S3, a commit a runbook
  pins). It starts empty.
- **Judgement (Chair):** tone against the voice's traits, filler, hedging, flattery, the rule-of-three
  cadence, uniform rhythm, vague claims and colon subtitles are held by `.claude/rules/writing.md`,
  path-scoped to the markdown the profile governs. The `document-reviewer` judges a document against
  it and records findings; the `editor` rewrites them through the humanizer; the reviewer is never
  the builder (decision 2026-10-24-006).

### Enforcement

None yet: the rules are TMPL-6's gate, the judgement its rules page and the two personas.

---

## Decision 2026-10-24-019: The template is swept, then judged whole

**Date:** 2026-10-24
**Made By:** Chair (S18): the template opted in; everything swept before publishing, records
included; whole files from then on, against drift past the rules; each project swept at adoption.
The formats' move to ASCII and the label rule by the AI
**Status:** APPROVED
**Builds:** TMPL-6.1 (design question 4)
**Affects:** none at this decision. To be built in TMPL-6: every tracked markdown file swept; the
authorities among them are named, with their version-log rows, by the decision that re-cuts the
stories

### Context

The template's tree held about 729 U+2014 em dashes, 720 box-drawing characters, 259 U+00A7 section
signs and 260 headings that read as sentences at S18 (decision 2026-10-24-018). Its files are of
two kinds: those every project receives, which agents read at each cold start and imitate, and its
own records (`sprint/`, the archives, the bodies of logged decisions). The coding standard judges
changed lines only and the template does not opt in to it (decision 2026-10-24-011), since legacy
code is costly to clean. The Chair wants the new version clean and compliant with its standards
before it is published, and named the risk: these characters exist because drift bypassed rules
already in place.

### Decision

- **The template opts in (Chair),** unlike the coding standard.
- **Everything is swept now (Chair):** every tracked markdown file, records included, is made to
  pass the gate in TMPL-6 before `v2.1.0` is published. The sweep changes no decision's substance,
  Status or dates, so it amends none (AI).
- **Whole files from then on (Chair):** every governed file is judged in full at every commit and in
  CI, never changed lines only. In a clean tree the two give the same findings for new work; they
  part on text that entered unjudged, by a commit without the hooks or `--no-verify`, a template
  update, or a first push judged at its tip (TMPL-2.10). Changed lines would never see that text
  again; whole files catch it at the next commit. Prose is cheap to clean, with the humanizer, which
  is why the coding standard's reason for changed lines does not carry over.
- **Each project is swept at adoption (Chair):** taking `v2.1.0` (TMPL-4.6), each project's
  documents are swept with the humanizer, the Chair reviewing the diffs, before its suite is green.
- **The formats the gates read move to ASCII (AI):** the sprint-status entry heading, the handoff
  and kickoff headings, a persona's changelog lines and the tracker's epic headings use a hyphen
  for U+2014. Their parsers read both forms, since the updater never writes a project's `sprint/`
  and it keeps the old form until its own sweep. In those formats the label before the title
  (`S<N> - <date> -`, `Decision <ID>:`, `Epic: <ID> -`) is not counted toward a heading's 8 words.
- **No gate is loosened for the sweep (AI):** where one holds text append-only, as the persona gate
  holds a changelog by version, whether the sweep's change is a new version or a normalized compare
  is settled with the Chair in the build.

### Enforcement

None yet: the sweep and the gate over whole files are TMPL-6's.

---

## Decision 2026-10-24-020: Mechanical findings refuse, judgement pauses

**Date:** 2026-10-24
**Made By:** Chair (S18): a mechanical finding refused, its exception an exact string in the allow
list, now for every mechanical rule, a change to the list approved by the Chair; a judgement
finding pausing its story until the Chair answers. The trigger path by the AI
**Status:** APPROVED
**Amends:** 2026-10-24-018 (the allow list's reach)
**Builds:** TMPL-6.1 (design question 5)
**Affects:** none at this decision. To be built in TMPL-6: the writing gate's refusal, the allow
list over every mechanical rule, `writing-profile.yaml` among the trigger paths of a gate or CI
change

### Context

Decision 2026-10-24-014 left the enforcement model to this session: a refusal, or a pause until
the Chair answers in a log as decision 2026-10-24-011 has code do. The coding standard never
refuses, since a code change is costly and risky and the Chair decides what proceeds. A mechanical
writing finding always has a cheap and certain fix, which the humanizer makes, and its rare
legitimate exception (a reading in degrees, a commit a runbook pins, Amazon S3) is an exact string.
A judgement finding is taste.

### Decision

- **A mechanical finding refuses (Chair):** characters, headings, phrases and references refuse the
  commit locally and fail the `gates` run in CI. Each finding prints its fix and the allow-list line
  that would exempt it.
- **The allow list is the only exception (Chair):** exact strings in `writing-profile.yaml`'s
  `allow:`, now exempting text from all four mechanical rules, where decision 2026-10-24-018 named
  the phrase and reference rules only. There is no log of mechanical findings: the list is the
  record, and each line is a visible commit.
- **A change to the allow list is a gate change (Chair):** in `/story` it is the trigger of a gate
  or CI change, approved by the Chair before the story closes; the profile is counted among the
  trigger paths that show it (AI).
- **A judgement finding pauses (Chair):** the `document-reviewer`'s findings take the review path
  every finding already takes, recorded in the code review log with the Chair's response, the story
  waiting until the Chair answers (decisions 2026-10-24-011, 2026-10-24-013 and 2026-10-24-015). No
  new log.

### Enforcement

None yet: the refusal and the allow list are TMPL-6's gate; the judgement path is
`story-artifacts`'s, as built.

---

## Decision 2026-10-24-021: The humanizer's flow

**Date:** 2026-10-24
**Made By:** Chair (S18): the editor subagent rewriting flagged text only, the guard on meaning, the
review per file, an agent fixing its own draft, one skill with a voice mode, started by an agent or
the Chair. The skill's name and the subagent's source by the AI
**Status:** APPROVED
**Builds:** TMPL-6.1 (design question 6)
**Affects:** none at this decision. To be built in TMPL-6: `.claude/skills/humanize/SKILL.md` (new),
listed in `AGENTS.md` and `README.md`

### Context

Decision 2026-10-24-014 gave the humanizer its shape: the flagged passages rewritten in the
document's voice and the change shown to the Chair before it is kept. Only the main session can
ask the Chair (decision 2026-10-24-015). The template's own sweep (decision 2026-10-24-019) is
thousands of fixes across every tracked markdown file, and each project's sweep at adoption is of
the same kind.

### Decision

- **One skill, `/humanize`, in the main session (Chair; the name by the AI):** it runs the writing
  gate over the files it is given and works through the findings.
- **Certain fixes by script (Chair):** a fix with one right answer is applied mechanically: curly
  quotes to straight, U+2026 to three full stops, invisible and non-breaking spaces, arrows to
  `->`, box drawing to `|` and `+--`.
- **The editor rewrites the flagged text only (Chair):** an `editor` subagent, the roster's or a
  general-purpose one carrying `personas/editor.md` where the roster has none (AI), rewrites each
  flagged sentence or heading, and any finding the `document-reviewer` recorded, in the document's
  assigned voice; a custom voice brings its traits and its sample. A whole-document pass in a voice
  is made only when the Chair asks for one.
- **The gate, then a guard on meaning (Chair):** the gate runs again, up to three tries, the
  findings still open after the third going to the Chair; and every code span, link and number in
  the passage must survive the rewrite, a development reference removed from a production document
  excepted, so the meaning cannot drift unseen.
- **The Chair reviews each file before it is kept (Chair):** the script's fixes shown as counts by
  kind, the editor's rewrites change by change; the Chair keeps the file, keeps some of its changes
  or rejects it. The main session commits only what the Chair kept.
- **For text already in the tree (Chair):** the sweep, a project's adoption, or a file the Chair
  points at. An agent's own uncommitted draft that the gate refuses is fixed by the agent, as a
  failing test is, and reaches the Chair through its story's review.
- **A voice mode (Chair):** the same skill takes the Chair's sample, counts it at 200 words or more,
  drafts the traits from it, and writes the voice file once the Chair approves them (decision
  2026-10-24-016).
- **Started by an agent or the Chair (Chair):** an agent may start it when the gate refuses text
  already in the tree, and so may the Chair; it never keeps a change without the Chair's answer.

### Enforcement

None yet: `skill-scan` over the skill once built, and the writing gate over what it keeps.
