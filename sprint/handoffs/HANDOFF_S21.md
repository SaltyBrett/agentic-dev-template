# Handoff — S21

**For session:** S21
**Written by:** S20
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S21.md`
- `docs/standards/session_handoff_standard_v2.0.md`: the handoff and kickoff formats' law, which TMPL-6.4 amends with a version-log row
- `docs/standards/sprint_management_standard_v1.0.md`: the sprint-status entry heading and the tracker's epic heading, the law TMPL-6.4 amends with a version-log row
- `docs/governance/framework_decisions.md` decision 2026-10-24-019: the formats' move to ASCII, parsers reading both forms, the label rule, and the append-only question the plan settles
- `docs/orchestration/knowledge/reference_writing_standard_design.md`: why the formats move and why the parsers read both forms
- `docs/orchestration/knowledge/reference_session_closeout.md`: the session gate, its pair structure, and the persona gate's append-only rule that a punctuation-only changelog change meets
- `scripts/session_closeout.py`: the entry heading parser, the scaffold and the persona changelog lint the build changes
- `scripts/sanitize_template.py` and `scripts/new_project.py`: where the formats are written at a reset and at birth
- `docs/standards/writing_standard_v1.0.md` section 6: the label rule the new formats must keep within
- `.claude/rules/gate-scripts.md`: a gate script's rules, fixtures proved against a broken copy, exit codes
- `docs/standards/coding_standard_v1.0.md`: the limits the changed gate code meets

## 2. Completed last session

- The S20 handoff dropped the scratch deletion, done by the Chair, in `sprint/handoffs/HANDOFF_S20.md` (51c3110)
- TMPL-6.3's plan, settled with the Chair: decision 2026-10-24-026 in `docs/governance/framework_decisions.md`; `docs/standards/writing_standard_v1.0.md` at 1.1, the gate's reading stated in sections 2, 4, 5, 6, 7, 8, 9 and 11; S20 opened in `sprint/sprint-status.md`, S10's entry moved to `sprint/archive/sprint-status_2026.md`; TMPL-6.3 In Progress in `sprint/story-tracker.md` (4dbcc97)
- TMPL-6.3, the gate: `scripts/writing_standard.py` with `--which`, `--text` over `.docx`, `.pptx` and `.xlsx`, and a self-test of 144 fixtures, each rule's fixture seen failing against one of 53 broken copies; hooks `writing-standard-selftest` (commit stage) and `writing-standard` (manual stage) in `.pre-commit-config.yaml`; `docs/governance/gate_suite_runbook.md` at 1.14; `scripts/md_to_docx.py`'s footer now `Generated from Markdown (draft)`; `.claude/skills/document-production/SKILL.md`'s check step names `--text`; two fixtures in `scripts/template_update.py`'s self-test for the profile merge and the custom voice, proved on a scratch template with two releases (f58936b)
- TMPL-6.3 Done in `sprint/story-tracker.md`; the writing standard's 1.1 row and the runbook's 1.14 row stamped; the real tree's sweep sized at 1379 findings for TMPL-6.6; `docs/orchestration/knowledge/reference_writing_standard_design.md` and its INDEX row gained the gate's reasons and what its build found (94e5338)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-026 The writing gate's design

## 5. Blockers and open questions

- No blockers.
- A persona's punctuation-only changelog change (U+2014 to a hyphen), a new version or a normalized compare, since the persona gate holds a changelog append-only by version (decision 2026-10-24-019): the Chair's, at TMPL-6.4's plan.
- Whether the template's existing lines in the old form move in TMPL-6.4 or in TMPL-6.6's sweep: the Chair's, at the plan.
- The changelog lines of `personas/editor.md` and `personas/document-reviewer.md` stay U+2014 findings of the writing gate until TMPL-6.4 moves the format.
- Carried, not S21's: TMPL-6.5 after TMPL-6.4; TMPL-3.4, TMPL-3.5, TMPL-2.10, TMPL-4.7, TMPL-4.4 and TMPL-4.5, all before the `v2.1.0` release TMPL-4.6.

## 6. Verification observed

- Cold start, as recorded in the S20 entry: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S20"), `doc-queue` exit 0
- TMPL-6.3, as recorded in the S20 entry: `writing-standard-selftest` holds 144 fixtures, and each of 53 broken copies of the script failed its self-test at the fixture named for its rule; the updater's two fixtures each failed against a broken copy; the scratch project took the second release with its suite green
- `pre-commit run writing-standard --hook-stage manual --all-files --verbose` on the real tree: exit 1, 1379 findings in 152 of 167 files, characters 1190 and headings 189, no phrase, reference, profile or voice finding
- Closeout: `git status --short` exit 0, clean; `pre-commit run agent-execution-identity --all-files --verbose` exit 0; `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued; `python3 scripts/session_closeout.py --scaffold --persona framework-maintainer` exit 0
