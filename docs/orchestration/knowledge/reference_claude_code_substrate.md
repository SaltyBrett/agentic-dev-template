---
name: The Claude-native substrate, proved end to end in a live session
description: 'What TMPL-1.7 saw when a project born from the committed template ran its first session interactively: the birth (suite green, roster empty, library whole, session-verify at S1 only once the birth is committed); the SessionStart report arriving after the operator accepted the trust dialog; the team-selection skill asking, waiting, copying and drafting; the compact re-injection naming the session and quoting the notes and journal; the forked closeout running as general-purpose in the foreground through scaffold, gate, commit and push, refusing an attribution trailer the harness asked for; and the two gaps it exposed. Read before changing the session hooks, the closeout or team-selection skills, or the initializer, and before the next substrate probe.'
teaches: [2026-10-22-001, 2026-10-23-003, 2026-10-23-006]
verified: 2026-10-23
metadata:
  type: reference
---

# The Claude-native substrate, proved end to end in a live session

> Durable learning. Wikilink: `[[reference_claude_code_substrate]]`.
> The mechanisms: [[reference_claude_code_hooks]], [[reference_claude_code_skills]],
> [[reference_session_closeout]], [[reference_derived_project_start]]. Observed 2026-10-23 on
> Claude Code 2.1.308, in a scratch project cloned from the template at the commit that finished
> TMPL-1.10, its origin a local bare repository.

## Why a live session, after every piece had its own probe

Each hook and skill had been proved in `claude -p`, where Claude Code treats the folder as trusted
and no one is at the keyboard. A real first session differs in three ways no `-p` run shows: the
trust dialog stands between the clone and every committed hook; a skill that asks the operator must
wait for an answer; and a forked closeout must commit and push, which a `-p` session cannot approve.
The probe ran once, in that order, with the operator at the terminal, and the transcript and the
journal are the record.

## What was seen

- **Birth.** `new_project.py --apply` exit 0, "every gate is green"; the roster `.claude/agents/`
  empty; `diff -rq` of `personas/` against the template's printed nothing. `session-verify` exited 1
  (`dirty-tree`) until the initializer's result was committed, then 0 at S1: the gate judges a clean
  tree, so a project's S1 starts with its birth commit.
- **Cold start behind the trust dialog.** The first record after the operator accepted it was
  `SessionStart:startup`, exit 0, before the first prompt: the identity gate PASS, `git pull` exit 0,
  `session-verify` PASS "this is S1", both hook types installed, no `CLAUDE.md` on the path, and no
  S1 kickoff, as a fresh project has none. The journal's first line was `start S1 (startup)`.
- **Team selection.** The skill read the project and the library, then asked two questions (the
  specializations, grouped by area, and the lead) and stopped. On the answer it copied two library
  personas, checked each copy identical with `cmp`, drafted the project's own persona, ran
  `session-closeout-check` (exit 0) and committed with every hook passing.
- **Compaction.** `/compact` wrote a compact boundary, then `SessionStart:compact`, exit 0: "This is
  still S1", the working notes as the session left them, "Nothing uncommitted", and a journal tail
  whose newest line was the last command before the compaction. The next turn quoted all of it.
- **The forked closeout.** It ran as a subagent of type `general-purpose` in the foreground. Scaffold,
  gate (passed, nothing to archive, one run), commit with every hook and the `commit-msg` gate, and
  push each exited 0; `gh run list` exited 1, there being no GitHub remote. The gate cleared the
  journal and the notes on its pass, and the journal then held the fork's later commands tagged
  `[general-purpose]`. The harness asked the fork for a `Co-Authored-By` trailer; it left the
  trailer out, citing `AGENTS.md`: the rule held in a context that saw nothing of the session.
- **The persona at startup** was not exercised here, the S1 kickoff not existing; the template's own
  S6 session, opened in the VS Code extension, received its persona's prompt from the start hook.

## What it found

The fork reported what its procedure left open rather than guess past it, and two of its reports
were defects (decision 2026-10-23-006): the skill named no range for S1, which has no previous
closeout; and the scaffold pre-filled handoff sections 3 to 5 with `- None.`, which the gate accepted
unwritten while the session had logged a decision. The scaffold now leaves them as tokens. A third
report was the session's, not the procedure's: the S1 entry's Done list still held only the birth,
because the operator's session went from team selection straight to the closeout, and the fork named
it instead of editing outside the pair.

## Not observed

`disableWorkflows` in a live session, since nothing here names a keyword that would start a workflow;
and the closeout's `gates` watch on a scratch project, whose origin was local by the operator's
choice. The template's own closeouts watch their runs.

## Rules

- Prove a session mechanism in a live session once, not only in `-p`: trust, waiting for an answer
  and approving a commit exist only there.
- Read the record, not the memory of it: the transcript under `~/.claude/projects/<path>/` holds each
  hook's output as an attachment, and a forked skill's own transcript and type under `subagents/`.
- A closeout that reports a gap outside the pair is doing its job; bank the report in the tree.
