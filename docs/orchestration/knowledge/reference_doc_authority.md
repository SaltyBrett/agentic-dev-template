---
name: Authoritative documents record every decision that changes them
description: 'Why a source-of-truth document carries `authority:` frontmatter and a version log, why every decision from 2026-10-22 declares `**Affects:**`, and what `scripts/doc_authority_scan.py` accepts: a row citing the decision or an open story citing the decision and the path, nothing else. Why a row is a `fact:` with its fact or a story''s change, why the cutoff is a date, why a hash is matched by version to the first commit holding it, why in a project what the template wrote (its rows, its decisions) is judged only in the template, why one scope has one authority, why a document template is an authority of its own, how the first six authorities were marked, why the technical writer''s queue is a bare `Queued: S<N>` note drained by the next session at cold start, one document per drain, why a real epic needs an approved PRD and architecture or a `**Skips:**` decision, and the gate''s honest limit. Read before marking a document as an authority or writing a decision''s Affects line.'
teaches: [2026-10-22-002, 2026-10-23-008, 2026-10-23-010, 2026-10-23-011, 2026-10-23-014, 2026-10-23-015, 2026-10-23-016, 2026-10-23-019, 2026-10-23-020]
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

"Following renames" means renames only. `git log --follow` also follows copies, because git sets
find-copies-harder for it, so a PRD made from its template inherited the template's history and its
approval row was stamped with the template's commit. Where the path changes, the gate now asks
whether the older path survived the commit that brought the newer one; if it did, that was a copy,
and the history stops there (decision 2026-10-23-015).

## Why what the template wrote is judged only in the template

`gh repo create --template` squashes history, and the updater copies files, not commits. A
standard's row written in the template carries a template commit that a derived project's history
does not contain, and cites a template story that a project's tracker, regenerated at birth, does
not hold; a framework decision is queued, when it is, by a template story too. In a project, a row
citing only framework decisions is therefore the template's, already judged before release: the
gate holds it to neither its marker nor its hash, and `--stamp` never writes it. A framework
decision is held to neither its `**Affects:**` line nor its record. A row citing a project decision,
and every project decision, is the project's and is judged there in full.

The first build applied this to the hash alone, and every birth after the first authorities were
marked was refused: seven violations, each a template story the project could not hold (decision
2026-10-23-015). Nothing saw it, because the template's CI judges the template and the last scratch
adoption ran before the marking. A gate that judges a project differently from the template is
proved on a scratch birth whenever the template content it judges changes, not on the template alone.

## Why one scope has one authority

`sprint/recovery/AUTHORITY_MATRIX.md` kept the map of current artifacts by hand, with a rule to stop
when two claim one concern. It had already gone stale on the persona registry. With the frontmatter
as the registry, the rule is a check: two authorities whose scopes match ignoring case and spacing
fail. The matrix retired from the template in TMPL-2.3; a project's copy is under `sprint/`, which
the updater never writes, so it stays the project's to delete.

## The first authorities

TMPL-2.3 marked the four standards, the document-control standard and the gate runbook (decision
2026-10-23-011). Each log starts at the version the document stated and cites every decision from the
cutoff that names it, after the document was read against each; the one change not yet made, the
README catalog's to the runbook, is queued in its story's row. The old changelog tables were removed
rather than converted: their rows cited no decision the gate reads and their dates were placeholders,
and the handoff standard's had eight rows all at 2.0, the hand-kept value the gate exists to replace.
File names keep their version, because every tracker cites the standards by file name and the updater
never writes a project's tracker. The runbook gate skips the closing `## Version log`, its one H2 that
is not a hook.

## Why a template is an authority of its own

A PRD template carrying a PRD's `authority:` line would claim the scope of every PRD made from it,
and the gate refuses two documents claiming one. So each template in `docs/templates/` is the
authority for its document's shape, with a log of its own like a standard's, and the document made
from it claims the project's scope (decision 2026-10-23-014). A copy that keeps the template's line
fails `scope`, so the one-scope rule catches the forgotten step. A made document is a draft until it
is approved, and claims no authority before then, since it has no decision to cite.

## Why the writer's queue is a note, drained at cold start

The authority gate counts any open story citing a decision and a path as queueing the change, and
some of those stories make the change themselves (TMPL-5.5 rewrites the runbook section of a gate
it builds). No writer could drain those, so the writer's queue is only the stories marked for it,
with a bare `Queued: S<N>` on the row, N the session that queued it (decision 2026-10-23-016). The
`doc-queue` gate reads the note outside code spans, because the story that built the gate quotes the
convention in its own row, and a quoted note must never queue the gate's own story.

The drain is bounded rather than left to judgement: a story queued in S<N> may wait through S<N+1>,
and the gate fails from S<N+2>. It runs at cold start, from the start hook, because a closeout is
where compaction strikes and is never open-ended; the closeout only reports the queue. A queued
story names exactly one authority, because one drain is one document: the writer makes every queued
change to it in one pass, which is the anti-patchwork control decision 2026-10-22-002 asked for,
and sets each story Done. The session at work is read by one rule shared with the start hook, the
newest sprint-status entry plus one while the next kickoff exists, so the two never disagree about
which session a note is late for (decision 2026-10-23-019).

The drain, the doc-drain skill, forks as `general-purpose` and takes the library writer's prompt as
its first step, since a forked skill's `agent:` resolves only to a built-in or a roster agent and
the writer is a library persona. It leaves its change uncommitted: the main session reviews a
rewrite it did not write before it enters history.

The skill was proved the way a forked skill runs: a fresh agent given the scratch tree and the
document's path alone, asked to follow the body and to report where it could not. It drained the
story correctly and named eight frictions, four of them real (a dependency checked only after the
rewrite, the persona's commit rule against the skill's, MAJOR undefined against "structural",
`verified:` on an unchanged date), all fixed before release. A procedure read by an agent that
cannot ask is proved by such an agent, not by its author.

## Why a real epic needs approved documents, and what a skip is

The planning skill would not start without an approved PRD and architecture, and a precondition in
a skill is prose. Decision 2026-10-23-008 made it binding: in a project, the commit that writes the
first real epic is refused unless each document is approved or the Chair's skip of it is logged.
Approved is what decision 2026-10-23-014 made the README's last step: `status: approved` with the
`authority:` line, one document per folder, and the architecture's `prd:` the PRD's newest version,
so an architecture built on a superseded PRD is stale by construction. The rule lives in
`doc-authority-scan` because it reads what that gate already parses: frontmatter, version logs and
decision headers (decision 2026-10-23-020).

A skip is a decision because decision 2026-10-23-008 already logged it as one; the Chair chose a
header line, `**Skips:** prd` or `architecture`, so the gate reads it as it reads `**Affects:**`, and
the reason lives in the body where every other rationale does. Only the project's own log counts,
since a skip is a project's choice and the framework's decisions are not.

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
- Before a project's first real epic, approve the PRD and the architecture by `docs/templates/README.md`,
  or log the Chair's skip as an APPROVED decision headed `**Skips:** prd` or `**Skips:** architecture`.
- Queue a change for the technical writer with a bare `Queued: S<N>` on a story that names the one
  document and the decision; drain it with the doc-drain skill by the next session, and review its
  diff before committing.
