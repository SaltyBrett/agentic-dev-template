# Handoff — S18

**For session:** S18
**Written by:** S17
**Written:** 2026-10-24

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S18.md`
- `docs/governance/framework_decisions.md` decision 2026-10-24-014: the Chair's ask this session designs. It sets up the writing standard, voices assigned to a document by path and to an agent, the four guardrails named, a humanizer skill, and Grammarly's Humanizer as the model. TMPL-4.6 waits on the epic
- `docs/standards/document_production_standard_v1.0.md` §9: the house style the writing standard takes over, and the one written rule, "No em dashes anywhere", which the design moves out of this standard
- `.claude/skills/document-production/SKILL.md`: its check step searches a produced document for the em dash (§9), the procedure that moves or points to the new standard once the rule does
- `personas/editor.md`: the persona that edits for clarity and house style, the candidate holder of the judgement guardrails (tone)
- `personas/document-reviewer.md`: the persona that checks a document against its standards, which the writing standard becomes one of
- `personas/technical-writer.md`: the persona that writes READMEs, runbooks and guides, the main writer whose voice is assigned
- `docs/standards/coding_standard_v1.0.md` §4: findings and the code review log, the pause-until-answered pattern decision 2026-10-24-011 gives code, one of the two enforcement models in question
- [[reference_code_review_log]]: why a finding pauses only until the log holds the Chair's response, why the log is append-only, and why an answered finding pauses nothing again
- `scripts/code_standard.py`'s profile reader, `load_profile` and its `REQUIRED` keys: the shape a writing profile assigning voice and audience by path could take, beside `code-profile.yaml`
- [[reference_claude_code_rules]]: how a path-scoped `.claude/rules/` page loads, for the writing rule the design puts there

## 2. Completed last session

- TMPL-3.3, its plan settled with the Chair: the skill in the main session, roles never committing or asking, the main session gating, committing and asking at each trigger and finding; the proof on a scratch copy of Comfy. S17 opened in `sprint/sprint-status.md`, TMPL-3.3 In Progress in `sprint/story-tracker.md`, and S7's entry moved to `sprint/archive/sprint-status_2026.md` (30a74cf)
- TMPL-3.3, the `/story` skill: `.claude/skills/story/SKILL.md` (new), in the main session and the Chair's alone, listed in `AGENTS.md`'s skills table and `README.md`'s catalog (828d783)
- Decision 2026-10-24-014, the Chair's: the writing standard opens as epic TMPL-6 in `v2.1.0`, with TMPL-6.1 (design), TMPL-6.2 (law and gate) and TMPL-6.3 (humanizer) in `sprint/story-tracker.md` and TMPL-4.6 waiting on them. `.claude/skills/story/SKILL.md` now has every role's brief carry the project's `code-profile.yaml` (5fdf99f)
- TMPL-3.3 done (decision 2026-10-24-015): proved live on `story-probe-s17`, a clone of Comfy taken to a scratch `v2.1.0` by `template_update.py`. CU-4.6 ran from brief to release, with each artifact committed and passing `story-artifacts` and the build passing `code-standard`. Of the two review findings answered by the Chair, `tests 1` was fixed and `duplication 6` acknowledged. The release was stopped until approved, then pushed to the private `SaltyBrett/story-probe-s17`, run 40111133105 green. `personas/code-reviewer.md` is now version 3. `docs/orchestration/knowledge/reference_story_live_run.md` (new) has its `INDEX.md` row. TMPL-3.4, TMPL-2.10 and TMPL-4.7 were opened in `sprint/story-tracker.md` for the three gaps the proof found (6970ced)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-24-014 The writing standard opens as epic TMPL-6 in `v2.1.0`: assignable voices, a gate over the mechanical tells of machine-written prose (characters off a US keyboard, headings that read as sentences, AI and marketing phrasing, development artifacts in production documents) and a humanizer skill; designed with the Chair at S18; the release waits on it
- 2026-10-24-015 The `/story` skill as built, proved live on a scratch copy of Comfy: roles write and the main session gates, commits and asks; a finding reaches the code review log once, with the Chair's words; the code reviewer persona at version 3; three gaps the proof found opened as TMPL-3.4, TMPL-2.10 and TMPL-4.7, the release waiting on them

## 5. Blockers and open questions

- No blockers.
- S18 is a design session: it opens with the Chair, asks one question at a time, and logs each answer as a decision with `**Affects:**` before asking the next. It builds nothing until the decisions are logged.
- The Chair's ask at S17, the design's input. Agents' writing shows obvious machine tells, and the prose rules a session reads at its cold start are imprecise and enforce nothing. The tells the Chair named: headings and subheadings that read as prose; symbols no standard US keyboard types (em dashes, curly quotes, arrows, ellipsis characters, emoji, invisible spaces); technical documents that sound like marketing; production documents that cite development artifacts their reader cannot use (decision and story IDs, session numbers, sprint paths, wikilinks, "the Chair", commit hashes); "and more".
- The model is Grammarly's Humanizer. It offers a voice chosen from built-in ones, or a custom voice made from a sample of the writer's own writing, at least 200 words long, and it rewrites flagged passages in that voice. The Chair wants it in the repository, with a writing style that can be assigned to an agent and guardrails that are enforced.
- The template's own sprint documents and decisions use em dashes throughout, so whether the template's own documents are judged is an open design question.
- Carried, none of them S18's task, all before the `v2.1.0` release TMPL-4.6: TMPL-3.4, TMPL-2.10 and TMPL-4.7, the gate fixes S17's proof found (decision 2026-10-24-015); TMPL-4.4 and TMPL-4.5.
- The Chair deletes the scratch repository `SaltyBrett/story-probe-s17` (`gh repo delete` asks) and its clone `/Users/twdaddy/code/personal/story-probe-s17`, along with `SaltyBrett/launch-probe-s10`, `/Users/twdaddy/code/personal/launch-probe-s10` and `/Users/twdaddy/code/personal/tmpl-s6-probe`.

## 6. Verification observed

- Cold start, as recorded in the S17 entry: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0 ("this is S17"), `doc-queue` exit 0
- `skill-scan` over `.claude/skills/story/SKILL.md`: green, as the S17 entry records
- On `story-probe-s17`: every artifact passed `story-artifacts` when it was committed; the build passed `code-standard`; the scratch repository's run 40111133105 was green on `gates` and both `birth` jobs; on the closed story, removing the approval failed `trigger` and removing a log row failed `finding`, as decision 2026-10-24-015 records
- Closeout: `git status --short` exit 0, clean; `pre-commit run doc-queue --hook-stage manual --all-files --verbose` exit 0, nothing queued
