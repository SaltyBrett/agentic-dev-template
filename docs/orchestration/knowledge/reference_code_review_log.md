---
name: The coding standard advises and documents, and the code review log is its record
description: 'Why the coding standard never forces a code change: a finding pauses a commit or a story only until docs/code_review_log.md holds it with the Chair''s response, and an answered finding pauses nothing again unless it gets worse. Why pause-until-logged rather than advise-only (a hook cannot write into the commit it checks), why the Chair''s acknowledgement is the exception, why the log is append-only and an edit is the one thing no response clears, why a tool that cannot run is a finding, and why linter and type findings count on changed lines only. Read before changing the gate, the review stage or the log''s shape.'
teaches: [2026-10-24-011]
verified: 2026-10-24
metadata:
  type: reference
---

# The coding standard advises and documents, and the code review log is its record

> Durable learning. Wikilink: `[[reference_code_review_log]]`. Gate: `scripts/code_standard.py`,
> hooks `code-standard-selftest`, `code-standard`, `code-standard-range`. Law:
> `docs/standards/coding_standard_v1.0.md` §4. Companion: [[reference_coding_standard_calibration]].

## The Chair's rule

The standard measures, advises and documents, and never forces a code change: the Chair can always
acknowledge a finding and proceed (decision 2026-10-24-011). A standard that blocks until code
changes takes the decision away from the person who owns it; one that only prints is forgotten by
the next commit. So every finding is shown, every finding is written down, and the Chair decides.

## Why the commit pauses until the finding is logged

Advice alone leaves no record of a commit made outside a story. Writing the finding into the log
from inside the hook is not safe either: pre-commit stashes unstaged changes around a hook and reads
a file the hook modifies as a failure, and a hook that stages its own write into the commit it is
judging depends on git internals. So the gate pauses the commit and prints the rows to append; the
author adds them with the Chair's response, and the same commit carries its own record. The pause
costs one line, never a code change.

## Why the acknowledgement is the exception

An exceptions file beside the log would be two records of one judgement. The Chair's response to a
finding is the exception, and a category (a parser, a data table, a closed dispatch) is a note in
it. A row answers its place and rule at its value and below, so a function acknowledged at
complexity 21 is not asked about again at 21 or 19, and is asked again at 23: the ratchet survives
without forcing anything.

## Why append-only, and the one refusal

The log is the audit record of findings, the changes made and the Chair's responses. A row edited
or removed would rewrite that record silently, so the gate compares the log with its base and
refuses a changed row whatever else holds; a correction is a new row. It is the only finding no
response clears, because the response would live in the row being changed.

## Why a tool that cannot run is a finding

A missing tool, a report that does not parse, a coverage command that fails: each is a check not
made. Passing it silently is the green-over-nothing failure the calibration found
([[reference_coding_standard_calibration]]); refusing it outright would make a machine without Node
unable to commit. So it is `unmeasured`, and the Chair can answer it ("CI checks clones here").

## Why changed lines only, and the project's own tests

A legacy file edited for one line would otherwise carry every old lint and type error into the
change, which forces cleanup of code the change did not touch. Coverage is measured by the
project's own test command in the project's own environment, since a hook's isolated environment
lacks the project's dependencies.

## Rules

- Never make a finding block until code changes; pause until the Chair's response is in the log.
- Append to `docs/code_review_log.md`; never edit or remove a row.
- Record the gate's, the code reviewer's and the security auditor's findings in the one log.
- Treat a check that could not run as a finding, never as a pass.
