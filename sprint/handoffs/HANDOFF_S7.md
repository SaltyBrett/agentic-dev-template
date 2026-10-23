# Handoff — S7

**For session:** S7
**Written by:** S6
**Written:** 2026-10-23

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S7.md`
- `docs/governance/framework_decisions.md` decision 2026-10-22-002 — the whole design of the gate TMPL-2.1 builds: `authority:` frontmatter and version logs, `Affects:` on decisions, the rule that accepts a version-log row or an open tracker story and nothing else, the fact marker, `--stamp` verified against git, `--history`
- `docs/governance/framework_decisions.md` decision 2026-10-23-007 — the `.gitignore` union merge TMPL-2.5 builds (`git merge-file --union` for that path alone, named in the dry run), the fixtures it asks for, and the rejected alternative of nested `.gitignore` files
- `docs/governance/framework_decisions.md` decision 2026-10-23-008 — the project launch epic TMPL-5 builds, and its open items TMPL-5.1 settles: the PRD and architecture templates' sections, and their frontmatter in TMPL-2.1's `authority:` format
- [[reference_kb_freshness]] — the freshness gate the authority gate generalizes from knowledge entries to every authoritative document, and its honest limit, which the new gate inherits
- [[reference_kb_frontmatter_validation]] — parse with a YAML parser, never a regex; an empty parse raises; a fixture is trusted only after it fails against broken code
- [[reference_gate_runbook]] — the new hook needs its section in `docs/governance/gate_suite_runbook.md` in the same commit, or `gate-runbook` fails
- [[reference_template_update]] — the updater's three-way merge and the adoption from `v1.0.0` that TMPL-2.5 changes for `.gitignore`
- `.claude/rules/gate-scripts.md` — the shape every gate script and its self-test hook take, the self-test placed before the gate

## 2. Completed last session

- TMPL-1.10 — `scripts/template_update.py` converts every `docs/personas/` file of a `v1.0.0` project into the roster `.claude/agents/`, exactly or as a named conflict, with a converter that imports nothing from the project's old scripts; it removes `.resources-version`, merges a `source: dev-resources` knowledge entry as content and unmarks one no release writes; sixteen new fixtures, twenty-eight broken variants each caught; every real persona file converted byte for byte to its library copy; scratch adoptions of the three projects passed the whole suite on first run after a hand-resolved `.gitignore` conflict each. Also `.pre-commit-config.yaml`, `docs/governance/gate_suite_runbook.md`, `TEMPLATE_GUIDE.md`, [[reference_template_update]], [[reference_resources_sync]] (5ae88a8)
- TMPL-1.7 — the substrate proved end to end on a scratch birth `tmpl-s6-probe`: `new_project.py --apply`, suite green, roster empty, library whole, `session-verify` at S1, a live session through the trust dialog, team selection, `/compact` re-injection and the forked closeout. Two gaps fixed: `scripts/session_closeout.py` scaffolds handoff sections 3 to 5 as tokens to fill, and S1's range starts at the first commit in `.claude/skills/closeout/SKILL.md`; knowledge entry [[reference_claude_code_substrate]] with its INDEX row; [[reference_claude_code_hooks]], [[reference_claude_code_skills]] and [[reference_session_closeout]] updated (a3c6920)
- Epic TMPL-1 complete. First closeout (aa8f411): archived the S5 pair and wrote an S7 pair, since withdrawn.
- After the first closeout, with the operator: decisions 2026-10-23-007, -008 and -009 logged in `docs/governance/framework_decisions.md`; story TMPL-2.5 and epic TMPL-5 (TMPL-5.1 to TMPL-5.5) opened in `sprint/story-tracker.md`, TMPL-2.4 now depending on TMPL-2.5 and TMPL-5.4; the S6 entry in `sprint/sprint-status.md` extended; the S7 pair withdrawn so this closeout writes it again (fd50451)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-23-005 Adoption from `v1.0.0`, judged by what the project holds: every `docs/personas/` file converted into the roster exactly or refused as a conflict, by a converter that reads nothing from the project's old scripts; the sync's stamp removed; a `source: dev-resources` entry merged like any other and, where no release writes it, stripped of the declaration. Supersedes 2026-09-23-008.
- 2026-10-23-006 What the substrate's live proof found: the closeout's scaffold leaves handoff sections 3 to 5 as tokens to fill, and S1's range starts at the repository's first commit
- 2026-10-23-007 The updater merges `.gitignore` by union, keeping both sides' lines where both changed the same place; every other three-way path still conflicts (TMPL-2.5)
- 2026-10-23-008 A project launches through `/project-launch`: intake, team, PRD, architecture and planning, each stage steered by the Chair with pause, skip, return and status; documents versioned and approved on record; a gate that a real epic needs an approved PRD and architecture or a logged skip (opens epic TMPL-5)
- 2026-10-23-009 The root README is the operator's front page: a walkthrough from creating a project through the session loop, then a catalog of every command, operator script and session hook, held to the skills by `skill-scan` (TMPL-5.5)

## 5. Blockers and open questions

- No blockers.
- `disableWorkflows` is still unobserved in a live session; no trigger keyword is named in this repository (decision 2026-10-23-006).
- The scratch probe folder `/Users/twdaddy/code/personal/tmpl-s6-probe` and its scratchpad origin can be deleted by the operator.
- Decision 2026-10-23-008 leaves open whether `/project-launch` is the Chair's alone (`disable-model-invocation`); settled in TMPL-5.2.
- Decision 2026-10-23-002 was put to the operator at the S4 handover and not answered explicitly; its second and third bullets stand.
- Decision 2026-10-22-006 stands unless the operator overturns it.

## 6. Verification observed

- cold start: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0
- TMPL-1.10: sixteen new fixtures pass; twenty-eight broken variants each caught (three first caught wrongly, fixtures rewritten); every real persona file converted byte for byte; the three scratch adoptions each passed the whole suite on first run after the `.gitignore` conflict was resolved by hand
- TMPL-1.7: `new_project.py --apply` exit 0 with the suite green; `session-verify` exit 0 at S1 on the scratch birth; the team-selection gate exit 0; the forked closeout's `gh run list` exit 1 with no GitHub remote, as expected; three reverted variants of the closeout fix each caught
- First closeout: the `gates` run 40025256563 on aa8f411 concluded `success`
