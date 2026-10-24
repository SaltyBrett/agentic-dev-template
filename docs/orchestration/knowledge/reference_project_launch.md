---
name: A project launches in stages the Chair steers, and the documents hold the state
description: 'Why `/project-launch` is the Chair''s alone and runs in the main session, why each stage''s state is read from the documents rather than a launch file, how intake''s answers survive a pause (the PRD draft, §9 carrying the expertise to the team stage), why a reopened revision stands at its last approved version, how a later stage built on an older version is flagged (the architecture''s `prd:` gated, the plan''s `**Source:**` line reported), and what a skip is. Read before changing the launch skill, the team-selection or planning skills it calls, or the approval gate.'
teaches: [2026-10-23-008, 2026-10-23-020, 2026-10-23-021, 2026-10-23-024]
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

## Why the first closeout comes after planning

Decision 2026-10-23-008 made each stage's end a session boundary taken by a closeout naming the next
stage's lead. The live run (TMPL-5.4) found that impossible before planning: a kickoff's every task
must cite a story in a real epic, and the first real epic is the commit planning makes, which the
approval gate refuses until the PRD and the architecture stand approved or skipped. The session in
the probe even told the Chair a closeout would work, and later that stopping would leave the next
cold start flagging a missing closeout; neither was true. What holds is simpler: with no handoff
pair yet, a new conversation is still S1 and its `session-verify` passes, and the launch skill takes
each stage lead's prompt from the roster itself. So before planning the Chair takes a boundary by
ending the conversation, and the first closeout comes after planning, naming the lead the Chair
chose (decision 2026-10-23-024).

## What a skip is

A decision in the project's log whose header carries `**Skips:**` naming a stage, its reason in the
body: the Chair's form, read as `**Affects:**` is. Any stage may be skipped; only a skipped PRD or
architecture stands in for its approval at the gate.

## Honest limit

`skill-scan` proves the commands the skill names exist; it cannot prove the interview is good. The
proof of the stages is a live run with the Chair at the keyboard, through a pause, a skip and a
return to revise (TMPL-5.4).
The reading rules were proved the other way a skill can be: a fresh agent given only the file
applied `status` to two scratch trees, and every rule it could not apply without guessing (which
Status a skip is read by, a decision approving a deleted file, when the launch is done, a plan with
no recorded versions) became a sentence in the skill before release.

## Rules

- Run `/project-launch` at a project's first session; its stages are the Chair's to pause, skip or
  return to.
- Revise an approved PRD or architecture by reopening it, `status: draft` with its authority and
  rows kept; approving a PRD revision reopens the architecture in the same commit.
- Keep a stage's state in its document; add no file that records where the launch stands.
