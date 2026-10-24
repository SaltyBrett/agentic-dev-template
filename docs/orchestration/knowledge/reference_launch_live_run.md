---
name: What the live runs of /project-launch showed
description: 'The record of TMPL-5.4, the Chair at the keyboard in a private project made by the README''s walkthrough: what each stage did as written, where the session told the Chair something the gates contradict (a closeout before planning, a failing session-verify after an emergency close), the defects those exposed and the decisions that fixed them, and what is still unobserved. Read before changing the launch skill, the README walkthrough, or the closeout rules at a project''s first session.'
teaches: [2026-10-23-023, 2026-10-23-024]
verified: 2026-10-23
metadata:
  type: reference
---

# What the live runs of /project-launch showed

> Durable learning. Wikilink: `[[reference_launch_live_run]]`. Story: TMPL-5.4. Project:
> `SaltyBrett/launch-probe-s10`, private, made from the template at `30677d3` by the README's
> walkthrough. Companions: [[reference_project_launch]], [[reference_derived_project_start]].

## How it was observed

The Chair ran `/project-launch` in Claude Code sessions opened in the project; the template's session
read the results afterwards from the project's commits, its journal and the sessions' transcripts.
What follows is what those show, not what the sessions said about themselves.

## The walkthrough, steps 1 to 4

Run as written. One finding: GitHub's own run on the new repository's "Initial commit" was red,
`doc-authority-scan` judging the uninitialized copy as the template; every project made since S7
had opened that way, and the birth probe had not judged that run. Fixed by decision
2026-10-23-023 (TMPL-2.8). The clone's remote already read the operator's ssh alias, through a
`url.insteadOf` rewrite in the personal git config.

## Run 1

- **Intake** asked its three questions one at a time and accepted one-line answers, deferring the
  detail to the PRD interview; it wrote the draft by the template's README steps, the answers in §1,
  §3, §4 and §9, six open questions in §11, and committed it through the whole suite.
- **Pause** at the team stage, before anything was chosen, made no commit, since nothing had
  changed; the skill now says so.
- **`status`** read every stage correctly, twice; a bare `/project-launch` resumed at the team stage.
- **Team selection** offered no preset (none fits a game), declined to activate the library's only
  engine persona, `game-engine-developer`, because it is Rust/Bevy only and would choose the engine
  before the architecture stage, and recorded the Chair's choices and lead (`product-manager`).
- **The PRD stage** opened with decision 2026-10-23-008's question.
- **`skip architecture`** asked for the reason, named what the skip would cost (the engine choice
  losing its home), and logged nothing when no reason came.
- The session told the Chair a closeout at the stage's end would start the next session with the
  product manager. It cannot: every kickoff task must cite a story, and planning writes the first.
  Decision 2026-10-23-024 made a boundary before planning a new conversation, still S1.

## Run 2

- The Chair pasted the terminal commands into the old session; it declined to run them and said how
  to leave. The quickest boundary is `/clear`, which the skill and README now name.
- On the old session's offer, the Chair took an S1 emergency checkpoint. The session had said the
  next `session-verify` would then fail; asked to run it, it passed ("This is S1"), and the session
  said it had been wrong. `AGENTS.md` and the handoff standard said the same thing; both are
  corrected (decision 2026-10-23-024, amended).
- The new conversation started as S1, read the emergency entry as expected, and resumed at the PRD;
  on "log the rest in §11" it gave every unfilled section a pointer to its open question, removed
  the empty requirement rows, and committed the draft through the suite. Returning to `prd`, it
  showed the draft for review and waited for an approval that did not come; `status` was correct.
- `/closeout` before planning ran as a fork, read the tree three times, wrote nothing and committed
  nothing.

## Not yet observed

An approved PRD, a skip with its reason, planning and its `**Source:**` line, a return to revise an
approved document with the plan flagged stale, and the first closeout after planning.

## Rules

- A session's account of what a gate will do is a claim; run the gate.
- Give the Chair the command for a boundary that works in the session they are in: `/clear`.
- Record a live run from the project's commits, journal and transcripts, never from memory.
