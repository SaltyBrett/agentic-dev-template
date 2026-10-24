# Handoff — S19

**For session:** S19
**Written by:** S18
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S19.md`
- `docs/governance/framework_decisions.md` decisions 2026-10-24-016 to 2026-10-24-023: the design TMPL-6.2 builds. They set the voices, the profile, the four mechanical rules and the two phrase tables, the allow list, refusal, whole files, the move of §9 and the re-cut
- `docs/orchestration/knowledge/reference_writing_standard_design.md`: why each choice was made, so the law is written to the design's reasons and not only its words
- `docs/standards/document_production_standard_v1.0.md` §9 and §10: the rules that move to the writing standard and the list that stays, with the vendor rule moving into §10
- `docs/governance/doc_control_standard.md`: how a new authority declares itself, its version log and the stamp, which the writing standard and the document production standard's new row must meet
- `docs/standards/coding_standard_v1.0.md`: the shape of a standard whose numbers a gate holds, the model for the writing standard's tables the gate will read
- `.claude/skills/document-production/SKILL.md`: the check step that now points to the writing standard
- `personas/editor.md`: the persona that rewrites, versioned, its em-dash line pointing to the writing standard
- `personas/document-reviewer.md`: the persona that judges against the rules page, versioned
- `docs/standards/session_handoff_standard_v2.0.md`: the persona version and changelog rules both new persona versions must follow
- `docs/orchestration/knowledge/reference_claude_code_rules.md`: how a path-scoped rule loads and what the rule lint refuses, for `.claude/rules/writing.md`

## 2. Completed last session

- TMPL-6.1, design question 1, the voices (decision 2026-10-24-016): seven built in, a custom voice keeping the Chair's sample of 200 words or more, in its own project and private. S18 opened in `sprint/sprint-status.md`, with S8's entry moved to `sprint/archive/sprint-status_2026.md`, and `sprint/story-tracker.md` updated (ec8a497)
- TMPL-6.1, design question 2, the assignment (decision 2026-10-24-017): `writing-profile.yaml` beside `code-profile.yaml`, ordered path rules giving a voice and an audience; a file no rule names judged as production; an agent's voice in the same profile, in `docs/governance/framework_decisions.md` (2bdf900)
- TMPL-6.1, design question 3, the first lists (decision 2026-10-24-018): characters off a US keyboard, heading shape, two exact-phrase tables, development references in production documents, a project's allow list, tone judged and rewritten, in `docs/governance/framework_decisions.md` (ed2fb0d)
- TMPL-6.1, design question 4, the template's own documents (decision 2026-10-24-019): the template opts in, swept before `v2.1.0`, then judged whole; the formats the gates read moved to ASCII, in `docs/governance/framework_decisions.md` (0d402ca)
- TMPL-6.1, design question 5, enforcement (decision 2026-10-24-020, amending 2026-10-24-018): a mechanical finding refuses the commit and fails CI, the allow list over all four rules; a judgement finding pauses its story until the Chair answers in the code review log, in `docs/governance/framework_decisions.md` (80e961a)
- TMPL-6.1, design question 6, the humanizer (decision 2026-10-24-021): `/humanize` in the main session, an editor subagent rewriting in the assigned voice, the Chair reviewing each file before it is kept, in `docs/governance/framework_decisions.md` (f64bc6b)
- TMPL-6.1, design question 7, the em-dash rule (decision 2026-10-24-022): §9 of the document production standard moves whole to the writing standard and §10 stays, in `docs/governance/framework_decisions.md` and `sprint/story-tracker.md` (15cddd7)
- TMPL-6 re-cut, approved by the Chair (decision 2026-10-24-023): TMPL-6.2 the law, 6.3 the gate, 6.4 the formats moved to ASCII, 6.5 the humanizer and the agent's voice, 6.6 the sweep; TMPL-6.1 Done and TMPL-4.6 waiting on TMPL-6.6, in `sprint/story-tracker.md` (165d11e)
- `docs/orchestration/knowledge/reference_writing_standard_design.md` (new), with its `docs/orchestration/knowledge/INDEX.md` row: why each choice, for the builders of TMPL-6.2 to TMPL-6.6 (bd23d74)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-016 The writing standard's voices, built in and custom
- 2026-10-24-017 Voices and audiences assigned in writing-profile.yaml
- 2026-10-24-018 The writing guardrails' first lists, mechanical and judged
- 2026-10-24-019 The template is swept, then judged whole
- 2026-10-24-020 Mechanical findings refuse, judgement pauses
- 2026-10-24-021 The humanizer's flow
- 2026-10-24-022 The house style's writing rules move to the writing standard
- 2026-10-24-023 TMPL-6 re-cut to the design
- 2026-10-24-024 The subagent ceiling, opened as TMPL-3.5 after the closeout, its design at its start

## 5. Blockers and open questions

- No blockers.
- The Chair decides which of the template's own files are production in its `writing-profile.yaml`. `README.md` and `TEMPLATE_GUIDE.md` use S1, sessions and the Chair as product vocabulary for a template adopter. The options are the allow list or a development rule.
- A persona's changelog lines keep the em-dash form the persona gate's `CHANGELOG_ENTRY` reads until TMPL-6.4 moves the formats to ASCII. The two new persona versions write their changelog line in the current form.
- The document-production skill's check step cannot name the writing gate's command until TMPL-6.3 builds it, since `skill-scan` refuses a script or hook that does not exist.
- Carried, not S19's: TMPL-3.4, TMPL-3.5, TMPL-2.10, TMPL-4.7, TMPL-4.4 and TMPL-4.5, all before the `v2.1.0` release TMPL-4.6.
- The Chair deletes the scratch repositories `SaltyBrett/story-probe-s17` and `SaltyBrett/launch-probe-s10`, and the clones `/Users/twdaddy/code/personal/story-probe-s17`, `/Users/twdaddy/code/personal/launch-probe-s10` and `/Users/twdaddy/code/personal/tmpl-s6-probe`.

## 6. Verification observed

- Cold start, as recorded in the S18 entry: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S18"), `doc-queue` exit 0
- Closeout: `git status --short` exit 0, clean; `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
