---
name: issue
description: 'File an issue in the project''s issue log, change one, or report on them: a bug, a request or a risk, written through the one writer that keeps the index and the entries in step and refuses an entry the gate would refuse. Use when the Chair or a role reports something wrong, wanted or at risk, when a review or gate finding is deferred to a later fix, when a story resolves an issue, or when asked where the issues stand. Arguments: what was found, or an issue ID, or `report`.'
argument-hint: '<what was found> | <ID> [what changed] | report'
---

# Issue

Arguments: $ARGUMENTS

The log is `sprint/issue-log.md`; its law is section 12 of
`docs/standards/sprint_management_standard_v1.0.md`. Every change goes through `scripts/issue_log.py`, never an edit by hand: it
allocates the ID, writes the index row with the entry, and refuses what the `issue-log` gate would
refuse. A person files the same way, from a terminal: `python3 scripts/issue_log.py --file` asks for
each field it is not given.

## File one

1. Gather the fields from what was reported: a one-line title; the kind, `bug`, `request` or
   `risk`; the severity, `critical`, `high`, `medium` or `low`; what happened, what was expected,
   the impact, and for a bug the steps that reproduce it. Ask the Chair for any you cannot take from
   the report; never guess a severity.
2. File it, naming the reporter: `python3 scripts/issue_log.py --file --title "<title>" --by
   "<the reporter>" --as agent --kind <kind> --severity <severity> --what "<text>" --expected
   "<text>" --impact "<text>"`, with `--steps "<text>"` for a bug and `--as human` when a person
   reported it and you are writing it down.
3. Commit it, `checkpoint: issue <ID> filed`, and tell the Chair its ID.

## Change one

Change a field with `python3 scripts/issue_log.py --update <ID>` and the flags that change it:
`--status`, `--stories`, `--decisions`, `--resolved-by`, `--resolution`, `--severity`, `--title`.

- **Triaged** once a story or a decision answers it: name them with `--stories` or `--decisions`.
  A story that does not exist yet is planned first, with its row in the tracker.
- **In Progress** once one of its stories is. `python3 scripts/story_branch.py start <story>`
  makes this change in the commit that starts the story.
- **Resolved** once every story is Done: `--resolved-by <commit>` and `--resolution "<what changed>"`.
  `python3 scripts/story_branch.py finish <story> --resolution "<what changed>"` makes this change
  in the commit that sets the last story Done, the squash commit its resolving commit.
- **Closed** only on the Chair's word that the fix holds.
- **Won't fix** on the Chair's word, with `--resolution "<the reason>"`.

The gate refuses a status its stories do not bear out, and says which status they do. Commit each
change, `checkpoint: issue <ID> <status>`.

## A deferred finding

When the Chair answers a review or gate finding in `docs/code_review_log.md` with a fix for later,
file the issue first, then write its ID in the row's response (`acknowledged, ACME-ISS-7`). The gate
checks that every issue the log names exists.

## Report

`python3 scripts/issue_log.py --report` counts the issues by status, kind, severity and reporter,
and lists the open ones by age, each with its stories' status. For one issue, read its entry and its
stories' rows in the tracker.
