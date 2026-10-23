---
paths:
  - "sprint/decision-log.md"
  - "docs/governance/framework_decisions.md"
---

# Writing a decision

Why: [[reference_kb_freshness]]. Which log takes which decision: [[reference_framework_decisions]].

- A decision's Status and dates outrank prose that teaches it. Where they disagree, the prose is corrected in the same work unit.
- A new decision is a row at the top of the index table and a body, `## Decision <ID>: <title>`, at the end of the file.
- Its header block carries `**Affects:**`: each document it changes as a code span of its path, with the sections and the nature of the change, or `none`. Where it names a document with `authority:` frontmatter, that document's version log cites the decision in the same commit, or an open story citing the decision and the path queues it; `doc-authority-scan` refuses anything else ([[reference_doc_authority]]). A template session writes to `docs/governance/framework_decisions.md`; a project session writes to `sprint/decision-log.md` and prefixes its IDs (`ACME-2026-09-24-001`).
- Amending: the Date cell becomes `<original>; amended <YYYY-MM-DD>` and the body says what changed. Every consumer is then swept, teaching documents included: `git grep -n <ID>`, correct each hit, then `pre-commit run kb-freshness-scan --all-files`.
- Superseding: `SUPERSEDED [(scope)] by <new-id>` in the old row's Status and `**Supersedes:** <old-id>` in the new body. Both sides, or it is not done; a partial supersession names its scope.
