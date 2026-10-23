---
name: Authoritative documents record every decision that changes them
description: 'Why a source-of-truth document carries `authority:` frontmatter and a version log, why every decision from 2026-10-22 declares `**Affects:**`, and what `scripts/doc_authority_scan.py` accepts: a row citing the decision or an open story citing the decision and the path, nothing else. Why a row is a `fact:` with its fact or a story''s change, why the cutoff is a date, why a hash is matched by version to the first commit holding it, why a template row is verified only in the template, why one scope has one authority, and the gate''s honest limit. Read before marking a document as an authority or writing a decision''s Affects line.'
teaches: [2026-10-22-002, 2026-10-23-010]
verified: 2026-10-23
metadata:
  type: reference
---

# Authoritative documents record every decision that changes them

> Durable learning. Wikilink: `[[reference_doc_authority]]`. Gate: `scripts/doc_authority_scan.py`,
> hooks `doc-authority-selftest` and `doc-authority-scan`. Generalizes [[reference_kb_freshness]] from
> knowledge entries to every source of truth.

## The failure

A decision lands in the log, the knowledge base explains it, and the document that is the source of
truth for that scope (a PRD, an architecture, a standard, a runbook) is never brought up to date.
The freshness gate covers one direction only: an entry names the decisions it teaches, so a change
to one of them is caught. A new decision names nothing, so a document it should have changed looks
current to every gate. Decision 2026-10-22-002 adds the other direction: the decision declares what
it changes (`**Affects:**`), and the document records each change it received (a version log).

## Why the gate accepts two outcomes and nothing else

For a decision naming an authority, either the document's version log has a row citing it, or the
tracker holds a story that is not Done and cites the decision and the path. The first is the change
made. The second is the change queued: written down where the next session will see it. Anything
else is the silent miss this gate exists for. A Done story queues nothing, because its work is
finished and the document still lacks the row.

## Why a row is a fact or a story's change

The decision asked that a row written by anyone but the technical writer carry a fact marker, so
that structural rewrites go through the writer's queue instead of being patched in by the deciding
session. The gate cannot see who wrote a row. It can see two kinds of evidence, which the Chair
chose (decision 2026-10-23-010): a summary opening `fact:` that states the fact itself, a value,
name or path in a code span or a count; or a summary citing the tracker story whose row cites the
row's decision. A story citation proves the change was planned work. `fact:` is the author's
declaration, checked only for form.

## Why the cutoff is a date

"Every decision from this one forward" needed a boundary that both logs can compute under any ID
convention. The Date cell of the index gives it: decisions dated 2026-10-22 or later need the line,
older ones read as `none`. A marker naming the first decision per repository would spare a project a
back-fill at adoption, but it is one more stored value to keep correct. The three projects had no
decision from that date when the rule was set.

## Why a hash is matched by version, and why `pending` is allowed

The stamp is written after the commit exists, so stamping edits the row, and the row's text then
differs from the text the commit introduced. The gate therefore identifies a row by its version: the
stored hash must be a prefix of the first commit, following renames, whose copy of the document holds
that version. `--history <doc>` derives that commit for every row, which is why a row left `pending`
loses nothing: the value is always derivable, and a stored one is allowed only because the gate
verifies it. A shallow clone cannot derive it, so the gate exits 2 there instead of judging a
truncated history.

## Why the template's rows are verified only in the template

`gh repo create --template` squashes history, and the updater copies files, not commits. A
standard's row written in the template carries a template commit that a derived project's history
does not contain. In a project, a row citing only framework decisions is therefore the template's,
already verified before release; the gate skips its hash and `--stamp` never writes it. A row citing
a project decision is the project's and is verified there.

## Why one scope has one authority

`sprint/recovery/AUTHORITY_MATRIX.md` kept the map of current artifacts by hand, with a rule to stop
when two claim one concern. It had already gone stale on the persona registry. With the frontmatter
as the registry, the rule is a check: two authorities whose scopes match ignoring case and spacing
fail. The matrix retires in TMPL-2.3.

## Honest limit

The gate cannot read prose. A row citing a decision says the document was updated, not that it was
updated correctly; a path named outside a code span in `**Affects:**` is not read; a `fact:` row is
judged by form. Like the freshness gate, it turns a silent miss into a blocking one, and the reader
still has to check the content.

## Rules

- Write `**Affects:**` in the header block of every decision: each document it changes as a code span
  of its path, with the sections and the nature of the change, or `none`.
- When a decision changes an authority, add a row in the same commit (`fact:` with the fact, or the
  story that did the work) or open a story that cites the decision and the path.
- Leave the newest row `pending`; run `python3 scripts/doc_authority_scan.py --stamp` once it is
  committed. Never type a hash by hand.
- See the registry with `python3 scripts/doc_authority_scan.py --list`.
