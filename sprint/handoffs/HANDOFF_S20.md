# Handoff — S20

**For session:** S20
**Written by:** S19
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S20.md`
- `docs/standards/writing_standard_v1.0.md`, whole: the law the gate implements and the tables it reads, the character table `Code points | Characters | Replace with` in section 5 and the `### AI phrases` and `### Marketing phrases` tables, each `Phrase | Where`, in section 7
- `writing-profile.yaml`: the data the gate reads, its `rules`, `template`, `default`, `agents` and `allow`
- `docs/standards/voices/`: the seven voice files whose frontmatter (`name`, `tables`) the gate reads, and the shape a custom voice's `## Sample` takes
- `docs/governance/framework_decisions.md` decisions 2026-10-24-018, 2026-10-24-019, 2026-10-24-020 and 2026-10-24-025: the rules, whole files, refusal and the `template:` list the gate builds
- `docs/orchestration/knowledge/reference_writing_standard_design.md`: why each choice was made, the README and code-block reasons included, so the gate follows the design's reasons and not only its words
- `scripts/code_standard.py` (`load_profile`): the profile reader pattern to reuse
- `scripts/story_artifacts.py`: how a gate reads a standard's tables, the pattern for reading the character and phrase tables
- `scripts/session_closeout.py` (`glob_regex`, `expand_braces`): the glob translation the standard names for the profile's paths
- `.claude/rules/gate-scripts.md`: a gate script's rules, its exit codes, self-test and fixtures
- `docs/standards/coding_standard_v1.0.md`: the limits the gate's own code meets
- `docs/orchestration/knowledge/reference_template_update.md`: how `template_update.py` merges, for the proof that it leaves a project's custom voice alone and merges the profile three-way

## 2. Completed last session

- Decision 2026-10-24-024, the subagent ceiling, opened as TMPL-3.5 with `docs/orchestration/knowledge/reference_claude_code_subagent_model.md` and its INDEX row, in `docs/governance/framework_decisions.md` and `sprint/story-tracker.md`; committed after S18's closeout (2f64620)
- TMPL-6.2's plan, settled with the Chair: the writing standard's eleven sections, the voice file's shape, the profile's development paths, `agents: {}` and consistency over cleverness on the rules page. Decision 2026-10-24-025, the README development in the template alone by a `template:` list applied only where `.project-profile` is absent, in `docs/governance/framework_decisions.md`; S19 opened in `sprint/sprint-status.md`, S9's entry moved to `sprint/archive/sprint-status_2026.md` (0c30416)
- TMPL-6.2, the law: `docs/standards/writing_standard_v1.0.md` at 1.0, eleven sections and two phrase tables of fifteen rows each; the seven voices in `docs/standards/voices/`; `writing-profile.yaml`, parsing with `rules`, `template`, `default`, `agents` and `allow` (d1c6ef9)
- TMPL-6.2, the judgement: `.claude/rules/writing.md`, scoped to `**/*.md`; `personas/editor.md` and `personas/document-reviewer.md` at version 2, their changelog lines in the U+2014 form the persona gate reads; the writing standard's 1.0 row stamped (5e3438c)
- TMPL-6.2, the move: section 9 of `docs/standards/document_production_standard_v1.0.md` a pointer and its vendor rule in section 10, at 1.1; `.claude/skills/document-production/SKILL.md`'s check step runs the writing rules over a produced file; `AGENTS.md`'s governance map and `README.md`'s standards table list the writing standard; `docs/orchestration/knowledge/reference_writing_standard_design.md` gained why the README is development in the template alone and why phrases skip code blocks and a list ends with its paragraph; TMPL-6.2 Done in `sprint/story-tracker.md` (0e8d44e)
- The document production standard's 1.1 row stamped (6523bd4)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-024 The subagent ceiling (committed after S18's closeout, inside this range)
- 2026-10-24-025 The template's README is development in the template alone

## 5. Blockers and open questions

- No blockers.
- The writing gate's design, where the standard leaves room, is the Chair's at TMPL-6.3's plan: how `scripts/writing_standard.py` reads the standard's character and phrase tables; the profile reader, with the `template:` list applied ahead of `rules` only where `.project-profile` is absent; the voices' frontmatter and a custom voice's `## Sample` counted at 200 words or more; the allow-list match, the flagged text inside an occurrence of an allowed string in the same file; `--which <path>`; the text mode for a produced file.
- Whether the gate refuses a profile glob that matches nothing: five of the starter's globs (`docs/prd/**`, `docs/architecture/**`, `docs/stories/**`, `docs/code_review_log.md`, `evidence/**`) are project paths that match nothing in the template by design.
- A persona's changelog lines keep the U+2014 form the persona gate reads until TMPL-6.4 moves the formats to ASCII, so the changelog lines of `personas/editor.md` and `personas/document-reviewer.md` are the expected findings among the files S19 wrote.
- Carried, not S20's: TMPL-3.4, TMPL-3.5, TMPL-2.10, TMPL-4.7, TMPL-4.4 and TMPL-4.5, all before the `v2.1.0` release TMPL-4.6. TMPL-6.4 needs only TMPL-6.1 and can run in any session.

## 6. Verification observed

- Cold start, as recorded in the S19 entry: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S19"), `doc-queue` exit 0
- TMPL-6.2, as recorded in the S19 entry: the rule and persona linters refused each broken variant (a dead glob, a planted `AGENTS.md` sentence, a body changed at version 1, a missing changelog item); `doc-authority-scan` reported a decision unrecorded when 014 or 022 was removed from the 1.1 row or 025 from the 1.0 row
- Closeout: `git status --short` exit 0, clean; `pre-commit run agent-execution-identity --all-files --verbose` exit 0; `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued; `python3 scripts/session_closeout.py --scaffold --persona framework-maintainer` exit 0
