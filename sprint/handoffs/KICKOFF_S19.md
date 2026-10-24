# Kickoff — S19

**For session:** S19
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S19.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

This session builds the writing standard's law, from decisions 2026-10-24-016 to 2026-10-24-023.
Write every new file in ASCII, with headings of 8 words or fewer and no comma, since the gate will
judge them once TMPL-6.6 turns it on.

- TMPL-6.2, the plan first: settle with the Chair the writing standard's section layout and the rules of the template's own `writing-profile.yaml`. That includes which of the template's own files are production: `README.md` and `TEMPLATE_GUIDE.md` use S1, sessions and the Chair as product vocabulary for a template adopter, and the options are the allow list or a development rule. Build nothing until the plan is settled.
- TMPL-6.2, the law: `docs/standards/writing_standard_v1.0.md` as an authority with its version log. It holds the voices and audiences; the four mechanical rules, each character named by code point; the two exact-phrase tables the gate will read; the allow list; refusal; whole files; and the label rule.
- TMPL-6.2, the voices: the seven built-in voice files in `docs/standards/voices/`: technical, business, simple, professional, academic, streamlined and creative. `business` carries §9's prose rules as traits, and `creative` skips the marketing table.
- TMPL-6.2, the profile: the template's `writing-profile.yaml`, with ordered path rules giving a voice and an audience, its development paths declared, `default: technical`, the `agents:` map and an empty `allow:` list.
- TMPL-6.2, the rules page: `.claude/rules/writing.md`, path-scoped to the governed markdown, holding the judgement.
- TMPL-6.2, the personas: new versions of `personas/document-reviewer.md`, which judges against the rules page, and `personas/editor.md`, which rewrites, its em-dash line pointing to the writing standard. Each writes its changelog line in the current em-dash form, which the persona gate's `CHANGELOG_ENTRY` reads until TMPL-6.4 moves the formats to ASCII.
- TMPL-6.2, the move: §9 of `docs/standards/document_production_standard_v1.0.md` replaced by a pointer, its vendor rule moved to §10, with a version-log row citing 2026-10-24-022 and TMPL-6.2. Point the check step of `.claude/skills/document-production/SKILL.md` to the writing standard. Do not name the writing gate's command until TMPL-6.3 builds it, since `skill-scan` refuses a script or hook that does not exist.

## 4. Success criteria

- `docs/standards/writing_standard_v1.0.md` carries authority frontmatter and a stamped version-log row; `doc-authority-scan` green.
- The seven voice files and `writing-profile.yaml` exist; the profile parses as YAML with `rules`, `default`, `agents` and `allow`.
- `.claude/rules/writing.md` passes the session state gate's rule lint.
- `personas/document-reviewer.md` and `personas/editor.md` pass the persona gate at their new versions.
- The version-log row of `docs/standards/document_production_standard_v1.0.md` cites 2026-10-24-022 and TMPL-6.2 and is stamped.
- `skill-scan` green.
- TMPL-6.2 Done in `sprint/story-tracker.md`, with the Summary Statistics recounted.
- Every checkpoint: `pre-commit run --all-files` exit 0.
- The closeout push's `gates` run is green on `gates` and both `birth` jobs, observed with `gh run watch --exit-status`.

## 5. Closeout

Before ending: commit the `## S19 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
the decisions, the knowledge entries with their INDEX rows, and the tracker. Then run the closeout
skill, `.claude/skills/closeout/SKILL.md`, with the next persona's slug and the brief for S20.
It writes and fills the pair for S20, runs `pre-commit run session-closeout --hook-stage manual --all-files`, commits
`checkpoint: closeout S19`, pushes, confirms the `gates` run on GitHub is green, and returns
`KICKOFF_S20.md`, whose contents go to the user as the next session's prompt.
