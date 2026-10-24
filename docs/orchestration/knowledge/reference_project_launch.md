---
name: A project launches in stages the Chair steers, and the documents hold the state
description: 'Why `/project-launch` is the Chair''s alone and runs in the main session, why each stage''s state is read from the documents rather than a launch file, how intake''s answers survive a pause (the PRD draft, §9 carrying the expertise to the team stage), why a reopened revision stands at its last approved version, how a later stage built on an older version is flagged (the architecture''s `prd:` gated, the plan''s `**Source:**` line reported), and what a skip is. Read before changing the launch skill, the team-selection or planning skills it calls, or the approval gate.'
teaches: [2026-10-23-008, 2026-10-23-020, 2026-10-23-021]
verified: 2026-10-23
metadata:
  type: reference
---

# A project launches in stages the Chair steers, and the documents hold the state

> Durable learning. Wikilink: `[[reference_project_launch]]`. Skill:
> `.claude/skills/project-launch/SKILL.md`. Gate: `doc-authority-scan`'s approval rules
> ([[reference_doc_authority]]). Companion: [[reference_claude_code_skills]].

## The failure

Every project before the launch improvised its first sessions. The planning skill would not start
without an approved PRD and architecture, both folders shipped empty, and nothing produced either
(decision 2026-10-23-008).

## Why the Chair's alone, in the main session

Every stage asks the Chair questions and ends with the Chair's approval, so the skill is
`disable-model-invocation: true`: Claude never starts a stage unasked, and the S1 entry names the
command as its one next step. A forked skill cannot ask a question or see the conversation, so the
launch runs in the main session, taking each stage lead's prompt from the roster in turn (decision
2026-10-23-021).

## Why the state is the documents

A launch file beside the documents would be a second record of the same facts, and would drift. The
tree already says where each stage stands: the PRD draft exists, the roster holds the three leads,
each document is approved or reopened, the tracker holds a real epic, a decision skips a stage. So
`status` reads those, and a pause loses nothing: intake writes its three answers into the PRD draft
itself, the skills into §9 as the expertise the project depends on, where the team stage reads them
as the Chair's first answer; and a section still holding only the template's guidance is where an
interview resumes.

## Why a revision does not suspend the approval

Reopening an approved document for revision once meant losing the approval, and with a real epic in
the tracker the gate then refused every commit of the revision in progress. The Chair chose that the
last approved version stands while the document is reopened, its authority and rows kept (decision
2026-10-23-020, amended). The same rule carries decision 2026-10-23-008's flag on later stages:
approving a PRD revision leaves an approved architecture built on the old version, which the gate
refuses until the architecture is reopened too. The plan's dependence on the architecture is
recorded on the tracker's `**Source:**` line and reported by `status`, not gated: re-planning is a
judgement about which stories the change touches.

## What a skip is

A decision in the project's log whose header carries `**Skips:**` naming a stage, its reason in the
body: the Chair's form, read as `**Affects:**` is. Any stage may be skipped; only a skipped PRD or
architecture stands in for its approval at the gate.

## Honest limit

`skill-scan` proves the commands the skill names exist; it cannot prove the interview is good. The
proof of the stages is a live run with the Chair at the keyboard, through a pause, a skip and a
return to revise (TMPL-5.4).

## Rules

- Run `/project-launch` at a project's first session; its stages are the Chair's to pause, skip or
  return to.
- Revise an approved PRD or architecture by reopening it, `status: draft` with its authority and
  rows kept; approving a PRD revision reopens the architecture in the same commit.
- Keep a stage's state in its document; add no file that records where the launch stands.
