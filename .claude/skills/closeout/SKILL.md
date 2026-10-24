---
name: closeout
description: 'Close out the session: scaffold and fill the next handoff and kickoff, run the closeout gate, commit, push, watch the gates run, and return the next kickoff. Use at a natural work-unit boundary, when the user says context is high, or on "end session", after the session has committed its sprint-status entry, decisions, knowledge entries and tracker. Arguments: the next persona''s slug, then the brief for the next session.'
argument-hint: <persona-slug> <brief - tasks by story ID, success criteria, mandatory reads, open questions>
context: fork
agent: general-purpose
background: false
---

# Closeout

You are closing out the current session of this repository in a fresh context. You do not see the
session's conversation. What you have is the committed tree, `AGENTS.md` (already loaded), and the
arguments below. Report every command's exit code exactly as observed. If a step fails, stop there,
leave the tree as it is, and return what failed with its output. Never bypass a gate.

Arguments: $ARGUMENTS

The first word is the persona slug for the next session. The rest is the session's brief for the
next one: its tasks by story ID, their success criteria, the mandatory reads, open questions.

## 1. Check what the session left

1. `git status --short` lists nothing. The session commits its work before invoking you; an
   uncommitted change means it did not, so stop and return the list.
2. The newest entry in `sprint/sprint-status.md` is headed `## S<N> — YYYY-MM-DD — <title>` and holds
   Status, Done and Blockers for this session. N is this session's number.
3. The persona slug names a file in `.claude/agents/`, the project's roster, and the brief names
   at least one task by a story ID that `sprint/story-tracker.md` holds. A missing slug or brief, or
   a persona not in the roster, goes back to the session: the team-selection skill activates one.

## 2. Read the session from the tree

- This session's commits: `git log --oneline <base>..HEAD`, where `<base>` is the commit whose
  subject is `checkpoint: closeout S<N-1>` (`git log --grep '^checkpoint: closeout S<N-1>$' -1 --format=%H`).
  S1 has no previous closeout: its `<base>` is the repository's first commit
  (`git rev-list --max-parents=0 HEAD`), the template's tree.
- The decisions it logged: the index rows that range added to `docs/governance/framework_decisions.md`
  and `sprint/decision-log.md` (`git diff <base> HEAD -- <both files>`). The scaffold leaves
  sections 3 to 5 of the handoff as `{{FILL}}` tokens, so each is a judgement written, never a default.
- `sprint/handoffs/HANDOFF_S<N>.md` and `KICKOFF_S<N>.md`, the pair this session consumed.
- The technical writer's queue: `pre-commit run doc-queue --hook-stage manual --all-files --verbose`
  lists each queued story with its document, and handoff section 5 names each one. The closeout
  drains nothing and waits on nothing: the command's exit code is reported and never stops it.

## 3. Scaffold and fill the pair

`python3 scripts/session_closeout.py --scaffold --persona <slug>` writes `HANDOFF_S<N+1>.md` and
`KICKOFF_S<N+1>.md`. Never type their headings. Fill every `{{FILL}}`:

- Handoff 1: the brief's mandatory reads, one per bullet with why, after the line naming `AGENTS.md`
  and the kickoff. 2: the S<N> entry's Done, by story ID and file path, with commits. 3: the
  tracker's In Progress stories with their exact state, or `- None.` 4: each decision ID the range
  added, with its one-line title, or `- None.` 5: the entry's Blockers and the brief's open
  questions, or `- None.` 6: the verification the entry records, each gate with its exit code.
- Kickoff 3: the brief's tasks, each citing its story ID, in dependency order. 4: the brief's
  success criteria.

A pair lives one session. If the brief holds a rule or a learning that has no home in the tree,
stop and return it to the session to bank in a knowledge entry or a decision.

## 4. Run the closeout gate

`pre-commit run session-closeout --hook-stage manual --all-files` archives the older pairs, verifies
the new one and, on a pass, clears the journal and the working notes. When it archives a pair,
pre-commit exits 1 with `files were modified by this hook` whatever the gate printed: read the
gate's verdict, then run it again ([[reference_session_closeout]]). Fix what it names in the pair; a
finding outside the pair goes back to the session. `--all-files` keeps pre-commit from stashing the
unstaged pair ([[reference_precommit_stash]]).

## 5. Commit, push, watch

1. `git add -A`, then commit with the subject `checkpoint: closeout S<N>` and a body summarizing the
   session from its entry. No AI attribution of any kind in the message; the `commit-msg` gate
   refuses it.
2. `git push origin main`.
3. Find the push's run with `gh run list --limit 1 --json databaseId,headSha` (its `headSha` is the
   commit just pushed) and watch it with `gh run watch <id> --exit-status`. A red run is fixed,
   committed and pushed again before you return ([[reference_ci_backstop]]).

## 6. Return

In this order: each command above with its exit code as observed, the `gates` run id and its
conclusion, then the full text of `sprint/handoffs/KICKOFF_S<N+1>.md`, which the session hands the
user as the prompt for the next session.
