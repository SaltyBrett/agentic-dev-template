# Handoff — S8

**For session:** S8
**Written by:** S7
**Written:** 2026-10-23

## 1. Mandatory reads

- `AGENTS.md` cold start, then `sprint/handoffs/KICKOFF_S8.md`
- `docs/governance/framework_decisions.md` decision 2026-10-23-012 — the whole design of TMPL-5.6: the four personas, the named team presets, the gate refusing a preset that names no library persona, and the opt-in Blender MCP connection, off by default
- `docs/governance/framework_decisions.md` decision 2026-10-23-004 — the library's team and the shared habits every persona carries, which the four new personas must carry too
- `docs/governance/framework_decisions.md` decision 2026-10-23-008 — the project launch epic and TMPL-5.1's open items: the PRD and architecture templates' sections and where they live
- `docs/governance/framework_decisions.md` decisions 2026-10-23-010 and 2026-10-23-011 — the authority format as built and the first six authorities, which the PRD and architecture templates must carry without claiming the scope a PRD made from them would also claim
- [[reference_doc_authority]] — what the authority gate accepts and why, one scope one authority among it
- `.claude/skills/team-selection/SKILL.md` — where the team presets go, and where the Blender connection is offered
- `docs/standards/session_handoff_standard_v2.0.md` §6 — the persona shape `session-closeout-check` holds the four new personas to
- `.claude/rules/gate-scripts.md` — the shape every gate script and its self-test hook take, for the preset gate and the doc-queue gate
- [[reference_claude_code_skills]] — a forked skill sees no conversation, only the tree and its arguments: the shape of the doc-queue drain skill

## 2. Completed last session

- TMPL-2.1 — `scripts/doc_authority_scan.py` with its hooks `doc-authority-selftest` and `doc-authority-scan` after `kb-freshness-scan` in `.pre-commit-config.yaml`, their sections in `docs/governance/gate_suite_runbook.md`, knowledge entry [[reference_doc_authority]] with its INDEX row; `.claude/rules/decision-logs.md` and the example body name the `**Affects:**` line; the `Story` of `scripts/session_closeout.py` carries its tracker row, which the authority gate reads; decision 2026-10-23-010 (79dba32)
- TMPL-2.5 — `scripts/template_update.py` merges `.gitignore` by `git merge-file --union`, the project's lines first, the dry run naming the path `union`; [[reference_template_update]] and `TEMPLATE_GUIDE.md` Step 9 (4696f91)
- TMPL-2.3 — six authorities marked: the four standards in `docs/standards/`, `docs/governance/doc_control_standard.md` (rewritten around the gate) and `docs/governance/gate_suite_runbook.md`; their changelog tables and `**Version:**` lines removed; `scripts/gate_runbook_scan.py` skips the runbook's closing version log; `sprint/recovery/AUTHORITY_MATRIX.md` removed, `sprint/recovery/README.md` pointing to the frontmatter registry; [[reference_gate_runbook]] and [[reference_doc_authority]] updated; decision 2026-10-23-011 (515f1a5); then `--stamp` wrote 515f1a5 into all six logs (2bf4459)
- Decision 2026-10-23-012 logged and story TMPL-5.6 opened in `sprint/story-tracker.md`, TMPL-2.4 now waiting on it (c12792c)

## 3. In progress

- None.

## 4. Decisions logged

- 2026-10-23-010 The authority gate as built: the frontmatter is the registry; a version-log row is a `fact:` with its fact or the change of a story citing its decision; `**Affects:**` required from decisions dated 2026-10-22; a hash verified as the first commit holding its version, the template's rows verified in the template; one scope, one authority
- 2026-10-23-011 The standards, the document-control standard and the gate runbook are the first authorities: each log starts at marking at the version the document states, citing every decision that names it or queueing it; the hand-kept changelog tables and `**Version:**` lines go; file names keep their version; the runbook gate skips the closing version log; the authority matrix retires in the template, a project's copy left to the project
- 2026-10-23-012 The library gains a backend engineer, a web developer, a Blender 3D artist and an image and video editor; team-selection offers named team presets, a gate refusing a preset that names no library persona; an opt-in Blender MCP connection offered with the Blender persona, off by default; built as TMPL-5.6 before the release

## 5. Blockers and open questions

- No blockers.
- `disableWorkflows` is still unobserved in a live session (decision 2026-10-23-006).
- The scratch probe folder `/Users/twdaddy/code/personal/tmpl-s6-probe` can be deleted by the operator.
- Whether `/project-launch` is the Chair's alone is settled in TMPL-5.2 (decision 2026-10-23-008).
- Decision 2026-10-23-002's second and third bullets were not answered explicitly at S4 and stand.
- Decision 2026-10-22-006 stands unless the operator overturns it.
- Decisions 2026-10-23-010 and 2026-10-23-011 were made by the AI within approved decisions, the Chair choosing two of 010's settlements; reported to the Chair at the S7 handover.
- The three projects keep their own `sprint/recovery/AUTHORITY_MATRIX.md`, `v1.0.0`'s unedited, after adoption, theirs to delete (decision 2026-10-23-011); name it to the operator at TMPL-2.4.
- The S7 checkpoints were not pushed before the S7 closeout, so the `checkpoint: closeout S7` push carried them and was the authority gate's first run on CI, where its hash check relies on the checkout's full history (`fetch-depth: 0` in `.github/workflows/gates.yml`).

## 6. Verification observed

- cold start: identity gate exit 0, `git pull` exit 0, `pre-commit run session-verify --hook-stage manual --all-files` exit 0
- TMPL-2.1: fifty-three fixtures pass; forty-five broken variants each failed a fixture without a crash; the gate on the real tree exit 0; on a scratch clone `--stamp`, `--history` and the swapped-hash refusal as designed, a shallow clone exit 2, an unrecorded decision reported
- TMPL-2.5: five new fixtures pass; seven broken variants each caught; scratch adoptions of clones of Supplier_Research_Dev, Comfy and PocketGames to a scratch `v2.0.0`, each dry run naming `.gitignore` `union` with no conflict, each `--apply` exit 0 with the whole suite green
- TMPL-2.3: `gate_runbook_scan.py` three broken variants caught; `doc-authority-scan` on the real tree: six authorities, seventeen pairs recorded, one queued, exit 0; after `--stamp` wrote 515f1a5, the gate verified all six against git
