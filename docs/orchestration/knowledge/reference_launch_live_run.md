---
name: What the live runs of /project-launch showed
description: 'The record of TMPL-5.4, the Chair at the keyboard in a private project made by the README''s walkthrough, through every stage to the first closeout: what each stage did as written, where the session told the Chair something the gates contradict (a closeout before planning, a failing session-verify after an emergency close), the two silent gaps the third run found (a bare `**Affects:**` path unread, a closeout run on an entry still saying it had not been), and the decisions and stories that answer them. Read before changing the launch skill, the README walkthrough, or the closeout rules at a project''s first session.'
teaches: [2026-10-23-023, 2026-10-23-024]
verified: 2026-10-24
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

## Run 3

- `/clear` began a new conversation, still S1, and `/project-launch` resumed at the PRD review with
  `product-manager` leading. On the Chair's approval it wrote the approval decision
  `LP-2026-10-24-001`, `status: approved`, the `authority:` line and the 1.0 row (`5794166`), then
  stamped the row (`8c748b1`).
- **`skip architecture`** asked the reason and logged `LP-2026-10-24-002`, APPROVED, headed
  `**Skips:** architecture` and `**Affects:** none`, the Chair's reason quoted in its body
  (`4169b9c`); then it opened planning.
- **Planning**, in the delivery manager's role, wrote epic LP-1 and its stories, the tracker's
  `**Source:**` line reading `PRD 1.0, architecture skipped`, and decision `LP-2026-10-24-003`,
  removing the log's `[EXAMPLE]` entry (`0e19e71`). `doc-authority-scan`, run in the probe by the
  template's session on that commit, exit 0.
- **`/project-launch prd`** reopened the PRD (`e30b46c`), committed the draft (`28832c7`), and on
  approval wrote 1.1, MINOR, citing `LP-2026-10-24-004` (`1ae29c9`), then stamped it (`62006ff`);
  with the architecture skipped there was nothing to reopen. **`status`** read planning stale: the
  `**Source:**` line names 1.0, the PRD stands at 1.1.
- **The first closeout**, `/closeout product-manager <brief>`, ran as the fork: scaffold, fill,
  `session-closeout` "closing S1 … PASSED" with no pair to archive, `checkpoint: closeout S1`
  (`c0a6db7`) with no attribution trailer although its harness asked for one, pushed with every
  earlier S1 commit; run 40063609570 green on `gates` and both `birth` jobs. Its kickoff cites
  LP-1.1; in the probe afterwards `session-verify` exits 0, "This is S2".

Two gaps it found, each passing silently:

- **A bare `**Affects:**` path is not read.** `LP-2026-10-24-001` named `docs/prd/prd.md` without
  a code span. The gate reads an `**Affects:**` path only from a code span, so it checked nothing
  and passed, and `docs/templates/README.md` step 5 says only "naming the document's path". The
  probe's session found it while writing the revision's decision and fixed its own in `1ae29c9`.
  The Chair chose a refusal in the gate and the README's wording (TMPL-2.9).
- **The closeout ran on an entry that said it had not.** S1's entry, written as an emergency
  checkpoint in run 2, kept its heading, a Status saying the closeout was not completed, and the
  initializer's `### Next`, though its Done was kept current. The session offered to bring it up to
  date before the closeout, but `/closeout` typed by the Chair runs straight into the fork, so the
  main session never had the turn, and the fork's check accepts any entry holding Status, Done and
  Blockers. It noted the stale Status in the handoff's §5 rather than edit outside the pair. The
  Chair chose a refusal in the closeout gate (TMPL-5.7).

The fork also ran `pre-commit run --all-files` outside its steps, since the entry recorded no exit
code for the handoff's §6.

## Not observed

A re-plan after the stale flag: the probe's S2 kickoff moves the PRD on again first.

## Rules

- A session's account of what a gate will do is a claim; run the gate.
- Give the Chair the command for a boundary that works in the session they are in: `/clear`.
- Record a live run from the project's commits, journal and transcripts, never from memory.
- A precondition a forked skill leaves to the main session is skipped when the operator types the
  skill; the gate the fork runs is where it holds.
- A gate that reads a value only in one form refuses the other form, or the other form passes
  unread.
