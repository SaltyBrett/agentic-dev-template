# Kickoff — S4

**For session:** S4
**Persona:** framework-maintainer
**Persona version:** 1

## 1. Persona

Run as the `framework-maintainer` agent, `.claude/agents/framework-maintainer.md`. The `SessionStart` hook injects its prompt as context unless the session already runs as that agent (`claude --agent framework-maintainer`).

## 2. Cold start

Run the cold start in `AGENTS.md`. Read `sprint/handoffs/HANDOFF_S4.md`, then the files it lists.
Run `pre-commit run session-verify --hook-stage manual --all-files` and do no build work until it passes.

## 3. Tasks

- TMPL-1.4 — Procedures become skills in `.claude/skills/<name>/SKILL.md`. Before writing anything, download `https://code.claude.com/docs/en/skills.md` with curl and read it whole: the frontmatter, `context: fork` and which agent a forked skill runs as, what that agent loads (a non-fork subagent loads `AGENTS.md` unless `omitClaudeMd` is set), `disable-model-invocation`, and how a skill is invoked. First reconcile `AGENTS.md`'s section "Workflows are portable markdown, not tool skills" with decision 2026-10-22-001's "the `SKILL.md` is the one home of the procedure": a `SKILL.md` is repository markdown, so say where an agent other than Claude finds it, and log the decision. Then move the five procedures (closeout, release cut, planning session, sanitize-and-cut, document production) so each has one home, shrink the standards that held them to the law and a pointer, and build the gate that keeps every hook id, stage and command a skill names in step with `.pre-commit-config.yaml`, with a self-test proved against broken variants and a runbook section.
- TMPL-1.6 — After TMPL-1.4: ownership of `.claude/agents/`, `.claude/skills/`, `.claude/rules/`, `.claude/settings.json`, the journal and the notes in `scripts/new_project.py`, `scripts/template_update.py` and `scripts/sanitize_template.py`, with fixtures proved against broken variants. TMPL-1.3 renamed `docs/personas/` to `.claude/agents/` in the three scripts' lists without an ownership fixture, so a cross-check that the initializer's `NEVER_RESET` and the updater's `KEEP` agree on the registry comes first. Decide, and log, how a project's own `docs/personas/` reaches `.claude/agents/` when it adopts `v2.0.0`.

## 4. Success criteria

- TMPL-1.4: each of the five procedures has one home, its `SKILL.md`, and the standard that held it keeps only the law and a pointer (a grep for each procedure's distinctive command over the markdown names one file); a forked skill invoked by `claude -p` in a scratch clone is observed doing its first step, observed, not assumed; the new gate exits 0 on the tree and refuses a skill naming a hook id or stage the config lacks, by fixture and by a live plant; every broken variant fails at least one fixture; `gate-runbook` passes with the new section
- TMPL-1.6: every `.claude/` path and the two recovery files classify as decided in the updater, and the initializer and the sanitizer agree with it, by fixtures that each fail against at least one broken variant; the adoption path for a project's `docs/personas/` is logged as a decision
- `pre-commit run --all-files` exit 0 at every checkpoint; the closeout push's `gates` run green, observed with `gh run watch --exit-status`

## 5. Closeout

Before ending: add a `## S4 — <date> — <title>` entry at the top of `sprint/sprint-status.md`,
flush durable learnings to `docs/orchestration/knowledge/` with an INDEX row, log decisions, update
the tracker, sync the registry (`python3 scripts/resources_sync.py --apply`, publishing what it
reports), then run `python3 scripts/session_closeout.py --scaffold --persona <slug>`, fill both
files for S5, run `pre-commit run session-closeout --hook-stage manual --all-files`, commit `checkpoint: closeout S4`, push, confirm
the `gates` run on GitHub is green, and hand the user the contents of `KICKOFF_S5.md` as the
next session's prompt.
