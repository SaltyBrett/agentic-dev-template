---
name: doc-drain
description: 'Drain the technical writer''s queue for one authoritative document: every open tracker story marked `Queued: S<N>` that names it, made in one pass in the technical writer''s role, with its version-log row, the stories set Done and the gates run; the change is left uncommitted for the main session to review. Use when the cold-start report or the doc-queue gate names a queued story, or when asked to drain the doc queue. Argument: the document''s path.'
argument-hint: <document path, as the doc-queue gate names it>
context: fork
agent: general-purpose
background: false
---

# Doc drain

You are draining the technical writer's queue for one document of this repository, in a fresh
context. You do not see the session's conversation. What you have is the tree, `AGENTS.md` (already
loaded), and the argument below. Report every command's exit code exactly as observed. If a step
fails, stop there and return what failed with its output. Never bypass a gate, and never commit.

Argument: $ARGUMENTS

The argument is the path of one authoritative document. With none, run step 3's command, return
the queue it lists and stop: which document is drained is the session's choice.

## 1. Take the role

Read `personas/technical-writer.md`. The text below its frontmatter is your prompt for this task:
take that role before anything else, and hold to its `insists_on` throughout.

## 2. Check the tree

`git status --short` lists nothing. The main session reviews your change as the whole diff, so an
uncommitted change of its own would be mixed into yours: stop and return the list.

## 3. Find the queue

`pre-commit run doc-queue --hook-stage manual --all-files --verbose` lists each queued story as
`queued <story> (Queued: S<N>, due by S<N+1>): <path>`. Take every story whose path is the argument;
with none, return "nothing queued for <path>" and stop. A violation the gate names for one of those
stories is the session's to fix in the tracker: stop and return it. Violations naming other
documents are not yours.

## 4. Read before writing

- Each queued story's row in `sprint/story-tracker.md`, and every standard in its Required
  Standards column.
- Each decision the rows cite, its index row and its body, in `docs/governance/framework_decisions.md`
  or `sprint/decision-log.md`.
- The document, whole.
- `docs/governance/doc_control_standard.md`, its Authorities and Recording a change.

## 5. Rewrite the document in one pass

Make every queued change at once, reading the document as a whole: a section a change makes wrong is
rewritten, never appended to, and a fact keeps one home, linked from elsewhere rather than repeated.
Keep the `authority:` scope as it is. Add to `implements:` each cited decision the document now
implements, and move `verified:` to today only after re-reading every decision `implements:` names
against the document.

## 6. Record the change

1. One new row at the top of the document's `## Version log`: the next version, MAJOR for a
   structural rewrite and MINOR otherwise; today's date; the decisions the stories cite; a summary
   of the change that names each story ID in parentheses; `pending` as the commit.
2. In `sprint/story-tracker.md`, each drained story `Done` and the Summary Statistics recounted in
   the same edit. The `Queued: S<N>` note stays on the row as its record. A story whose dependency
   is not Done cannot be set Done: stop and return it.

## 7. Run the gates

`pre-commit run --all-files` exits 0, and `pre-commit run doc-queue --hook-stage manual --all-files --verbose`
no longer lists the drained stories. A finding in the document or in the rows you wrote is yours to
fix; any other finding goes back to the session unfixed.

## 8. Return

Stage nothing, commit nothing, stamp nothing. Return, in this order: each command above with its
exit code as observed; the version-log row and each tracker row exactly as written; `git diff --stat`.
The main session reviews `git diff`, commits it as `checkpoint: …`, then runs
`python3 scripts/doc_authority_scan.py --stamp` and commits the stamp.
