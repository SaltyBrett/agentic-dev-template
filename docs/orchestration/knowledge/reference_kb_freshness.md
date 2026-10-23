---
name: Decision currency and KB freshness — how amendments stay swept
description: 'Why a knowledge entry declares the decisions it teaches and the date it was last verified, and why a gate fails the entry when a taught decision changed after that date: on the project this framework came from an amendment sweep missed the teaching document six times, because nothing linked a decision to what teaches it and amendment dates were not machine-readable. Why decisions outrank prose, why an entry is never the authority for a value, what the gate computes, its honest limit, and why a count of a growing set is a fossil. Moved from CONSTITUTION.md §6.3 by TMPL-1.5.'
teaches: [2026-09-20-004]
verified: 2026-10-22
metadata:
  type: reference
---

# Decision currency and KB freshness

> Durable learning. Wikilink: `[[reference_kb_freshness]]`. Gate: `scripts/kb_freshness_scan.py`.
> The instructions themselves: `.claude/rules/knowledge-entries.md` and `.claude/rules/decision-logs.md`.
> Companions: [[reference_kb_frontmatter_validation]] (the gate reading the wrong thing),
> [[reference_framework_decisions]] (the two logs it reads as one set).

## The failure

On the project this framework came from, an amendment sweep was missed six times. Every miss had
the same shape: the decision body, the canonical source and the live system were all updated, and
the teaching document was left stale. That shape is the dangerous one, because teaching documents
are what the next agent reads *instead of* the source. The worst instance told agents that a value
two ratified decisions required was "legacy, retained only until parity proves it has no remaining
consumer". It had five live consumers. A sweep that stops at code and decision bodies is not a
sweep.

The root cause, once measured: nothing linked a decision to the documents that teach it, and
amendment dates were not machine-readable, so neither a human nor a script could answer "which
decisions changed since this document was written?"

## Why each rule exists

- **A decision's Status and dates outrank prose that teaches it**, because the decision is where a
  change is recorded first and the prose is where it arrives last. Disagreement means the prose is
  a fossil, fixed in the same work unit rather than reported.
- **An entry whose `verified:` predates a decision it `teaches:` is suspect** until checked against
  the decision and the canonical source. The date is the only machine-readable claim an entry
  makes about its own currency.
- **An entry is never the authority for a value.** Values live in canonical source; entries explain
  why. Where a value must appear for the explanation to work, its authority and a one-line command
  that re-verifies it sit beside it. This is the rule that shrinks the problem permanently: the
  others manage duplication, this one removes it.
- **An amendment carries its date in the index row and is swept through every consumer**, teaching
  documents included, because the gate can only compare dates it can read.
- **A supersession is recorded on both sides**, `SUPERSEDED [(scope)] by <id>` on the old row and
  `**Supersedes:**` in the new body, because a one-sided link leaves the old decision looking live
  to whoever reads only it. A partial supersession names its scope; the remainder stays in force.
- **`teaches:` lists the decisions an entry explains**, not every ID it mentions, and never another
  repository's or an unratified one, because each listed ID is a date the gate will hold the entry to.

## What the gate computes

`kb_freshness_scan.py` fails an entry when a taught decision changed after the entry was last
verified, where change is the latest of the amended date in the decision's Date cell and the date
of any decision recorded as superseding or amending it. Supersession dates come from the
superseding decision, so historical rows need no backfill. Decision IDs are read literally from the
index of each log, so any ID convention works, and an index the parser cannot find raises rather
than reading as empty (decision 2026-09-20-004).

Clearing a failure means re-reading the decision and the canonical source, correcting the entry,
then bumping `verified:`. Bumping the date alone re-creates the exact fossil the gate exists to
catch.

## The honest limit

The gate flags staleness risk, not wrongness: it cannot read prose. A green scan means nothing has
changed since someone last looked, not that the entry is right. That is still the whole win, since
it turns a silent failure into a blocking one.

## Corollary: name the set, not its size

"All five drift scans" had already drifted to six. A count of a growing set is a fossil waiting to
happen, so a document names the set (the hooks in `.pre-commit-config.yaml`, the entries in the
index) and lets the source say how many there are.
