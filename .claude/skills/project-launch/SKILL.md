---
name: project-launch
description: 'Launch a project in five stages the Chair steers: intake, team, PRD, architecture and planning. Each stage opens with what it produces and how to pause, skip or return; the state is read from the documents themselves. The Chair runs it at a project''s first session and whenever a stage needs revisiting. Arguments: none to resume at the first unfinished stage, `status`, `pause`, `skip <stage>`, or a stage name to return to it.'
argument-hint: '[status | pause | skip <stage> | intake | team | prd | architecture | planning]'
disable-model-invocation: true
---

# Project launch

The Chair runs this at a project's first session and again whenever a stage needs it (decision
2026-10-23-008). It runs in the main session, never forked: every stage asks the Chair questions,
and a subagent can neither ask nor see the conversation. Another agent reads this file and follows
it as instructions.

Arguments: $ARGUMENTS

## Where each stage stands

There is no launch file; each stage's state is read from the tree, before anything else is done.
The documents decide: a decision approving a document that no longer exists approves nothing.

| Stage | Led by | Done when |
|-------|--------|-----------|
| 1. `intake` | the session | `docs/prd/prd.md` exists with `status:` and `template:` in its frontmatter: the PRD draft in the template's shape |
| 2. `team` | the team-selection skill | `.claude/agents/` holds `product-manager`, `solution-architect` and `delivery-manager` |
| 3. `prd` | `product-manager` | `docs/prd/prd.md` has `status: approved` and the `authority:` line |
| 4. `architecture` | `solution-architect` | `docs/architecture/architecture.md` is approved the same way, its `prd:` the PRD's newest version-log version |
| 5. `planning` | `delivery-manager` | `sprint/story-tracker.md` holds an epic not marked `[EXAMPLE]` |

- **Skipped:** a decision in `sprint/decision-log.md` whose Status in the Decision Index is
  APPROVED, as `doc-authority-scan` reads it, carries `**Skips:**` naming the stage. A stage both
  skipped and done reads as done.
- **Reopened:** an approved document is back at `status: draft` for revision, its `authority:` line
  and rows kept; its last approved version stands meanwhile.
- **Stale:** built on an older version of the stage before it. An approved architecture whose
  `prd:` is older than the PRD's newest version, which `doc-authority-scan` refuses; or a plan whose
  tracker `**Source:**` line names an older version of either document than its newest. A plan
  whose `**Source:**` line names no versions was made before this skill: done, its staleness unknown.
- **In progress:** a draft that is not yet approved, or a roster holding some of the three leads.
- **Not started:** none of the above; `status` names what is missing.

## The commands

- No argument: resume at the first stage that is neither done nor skipped, or that is stale.
- `status`: list the five stages, each as not started, in progress, done, skipped, reopened or
  stale, with the file or decision that says so, and for a draft the sections still holding only
  the template's `<!-- -->` guidance. Change nothing. The launch is done when every stage is done or
  skipped.
- `pause`: write the current stage's draft, commit it as `checkpoint: launch — <stage> paused`, say
  where it stopped, and stop; with nothing changed since the last commit, there is nothing to
  commit. Resuming reads the draft: a section still holding only the template's `<!-- -->`
  guidance is the next one to fill.
- `skip <stage>`: ask the Chair's reason, then log it in `sprint/decision-log.md` as a decision whose
  ID carries the project's story prefix, its header block holding `**Skips:** <stage>` and
  `**Affects:** none`, the reason in its body (`docs/templates/README.md`, Skipping a document).
  Commit it, then open the next stage. A skip of `prd` or `architecture` stands in for that
  document's approval; a skipped team leaves the roster empty, and the closeout's kickoff must still
  name a persona in it.
- `<stage>`: return to that stage, to resume, review or revise it (Revising an approved document).

## Opening a stage

Tell the Chair what the stage produces, who leads it and the commands above, then begin. A stage's
end is a session boundary the Chair may take. Before planning, the Chair takes it by ending the
conversation, never by a closeout: a kickoff's tasks cite stories, and planning writes the first.
The next conversation is still S1, its cold start passing with no handoff yet, and
`/project-launch` resumes from the documents with the next stage's lead. From planning on, the
closeout skill, given the next lead as the persona, takes the boundary.

## 1. Intake

- With nothing in `docs/prd/`, ask the Chair three questions, one at a time, waiting for each answer:
  1. What is the purpose of the project?
  2. What skills and expertise does it need?
  3. What should it accomplish?

  Make `docs/prd/prd.md` from `docs/templates/prd.md` by steps 1 to 4 of `docs/templates/README.md`,
  and write the answers into it: the purpose into §1, what it should accomplish into §3 and §4, and
  the skills into §9 as the expertise the project depends on, where the team stage reads them.
- With a PRD already in `docs/prd/`, summarize it against the same three questions and list each
  section of `docs/templates/prd.md` it lacks or leaves thin; the Chair confirms or redirects. One
  not yet in the template's shape is remade as the draft by the README's steps, its content carried
  into the matching sections and every gap named in §11; git keeps the original.
- Commit `checkpoint: launch — intake`.

## 2. Team

Run the team-selection skill, `.claude/skills/team-selection/SKILL.md`, with the expertise the PRD's
§9 names as the Chair's first answer, so the Chair is asked only what it leaves open. It activates
`product-manager`, `solution-architect` and `delivery-manager` beside the specialists the work needs,
the Chair names the lead, the persona later kickoffs name, and it commits the roster.

## 3. PRD

1. Take the product manager's prompt: the text below the frontmatter of
   `.claude/agents/product-manager.md`.
2. Open with: "Describe in as much detail as you can what your goals are for this project and what
   you want produced at project completion." With a PRD already there, interview its gaps only.
3. Interview until every section of the draft holds the project's content or names its open
   question in §11. Write each answer into the draft as it comes, and commit the draft at each
   natural pause as `checkpoint: launch — PRD draft`.
4. The Chair reviews the whole draft. On the Chair's approval, approve it by steps 5 to 7 of
   `docs/templates/README.md`: the approval decision in `sprint/decision-log.md`, its `**Affects:**`
   naming `docs/prd/prd.md`; the authority frontmatter with `status: approved`; the first
   version-log row, `pending`. `pre-commit run --all-files` exits 0; commit
   `checkpoint: launch — PRD approved`; then `python3 scripts/doc_authority_scan.py --stamp`, and
   commit the stamp.

## 4. Architecture

The same four steps, led by `solution-architect` (`.claude/agents/solution-architect.md`): from the
approved PRD, into `docs/architecture/architecture.md` made from `docs/templates/architecture.md`,
its `prd:` the PRD's newest version, or omitted when the PRD was skipped. Open with the questions the
PRD leaves to the build: what it runs on, what it connects to, which requirement must never fail.

## 5. Planning

Take the delivery manager's prompt (`.claude/agents/delivery-manager.md`) and run the
planning-session skill, `.claude/skills/planning-session/SKILL.md`; its tracker's `**Source:**` line
names the versions the plan is built from. The first real epic it writes is the commit
`doc-authority-scan` refuses unless the PRD and the architecture stand approved or skipped. With
planning done the launch is done, unless an earlier stage is neither done nor skipped; the session
closes out with the lead the Chair named.

## Revising an approved document

Returning to `prd` or `architecture` once it is approved:

1. Reopen it: `status: draft`, its `authority:` line and its rows kept. Its last approved version
   stands, so the revision can be paused and committed like a first draft.
2. Interview the change in the stage lead's role.
3. On the Chair's approval: a decision naming the document in `**Affects:**`; a row for the next
   version at the top of the version log, MAJOR when sections are replaced or reordered and MINOR
   otherwise; `status: approved`.
4. A PRD revision's approval reopens the approved architecture in the same commit, since
   `doc-authority-scan` refuses an approved architecture built from an older PRD version; then return
   to the architecture stage. A plan built on an older architecture version shows as stale in
   `status`: re-plan with the planning-session skill, whose `**Source:**` line then names the new
   versions.
