# Document templates

Each template here is the authority for the shape of one kind of document, versioned by its own
version log. A project makes its document from the template, and the document it makes claims a
scope of its own, so the two never claim one; a copy that keeps the template's `authority:` line
fails `doc-authority-scan` (decision 2026-10-23-014). `template_update.py` carries a newer template
to every project; the documents made from it are the project's, in `docs/prd/` and
`docs/architecture/`, which the updater never writes.

| Template | Made into | The scope it claims once approved |
|----------|-----------|-----------------------------------|
| `prd.md` | `docs/prd/prd.md` | `product requirements — <project>` |
| `architecture.md` | `docs/architecture/architecture.md` | `architecture — <project>` |

## Making a document

1. Copy the template to its place.
2. Replace the frontmatter with a draft's. A draft claims no authority yet, so its version log stays
   empty:

   ```yaml
   ---
   status: draft
   template: '1.0'   # the template's version, its newest version-log row
   prd: '1.0'        # the architecture only: the version of the approved PRD it is built from
   ---
   ```

   Quote each version, or YAML reads `1.10` as the number 1.1.
3. Replace each section's guidance with the content, keeping the headings and their numbers; where
   something is not known yet, name it in the open questions.
4. Delete the template's rows from the version log, keeping the heading and the header row.

## Approving it

5. Log the approval in `sprint/decision-log.md`, its `**Affects:**` naming the document's path.
6. Make the document the authority for its scope and set its status:

   ```yaml
   ---
   authority: product requirements — <project>
   implements: []
   verified: 2026-11-02
   status: approved
   template: '1.0'
   ---
   ```

7. Add the version log's first row, its commit `pending`:

   ```
   | 1.0 | 2026-11-02 | <the approval decision> | fact: approved, made from `docs/templates/prd.md` 1.0 | pending |
   ```

   Commit, then `python3 scripts/doc_authority_scan.py --stamp` writes the commit into the row.

A revision reopens the document as a new version: `status: draft` until it is approved again, its
`authority:` line and its rows kept, then a row at the new version citing the decision that approved
it. Until then its last approved version stands, so a revision in progress can be committed. The
architecture records the PRD version it was built from: approving a new PRD version is refused
until the architecture built on the old one is reopened in the same commit, then revised and
approved against the new one (decisions 2026-10-23-008 and 2026-10-23-020).

## Skipping a document

Once the tracker holds a real epic, `doc-authority-scan` refuses the commit unless each of the two
is approved or its skip is logged (decision 2026-10-23-020). A skip is the Chair's: log it in
`sprint/decision-log.md` with the stage in the header block and the reason in the body.

```markdown
## Decision ACME-2026-11-02-001: Skip the architecture

**Date:** 2026-11-02
**Made By:** Chair
**Status:** APPROVED
**Skips:** architecture
**Affects:** none
```

`**Skips:** prd, architecture` passes over both. Any stage of `/project-launch` can be named
(`intake`, `team`, `prd`, `architecture`, `planning`); only `prd` and `architecture` stand in for an
approval. An architecture approved after its PRD was skipped is built from no PRD version, and its
`prd:` is not read.
