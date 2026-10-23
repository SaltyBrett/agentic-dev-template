---
paths:
  - "docs/orchestration/knowledge/**"
---

# Writing a knowledge entry

Why each of these exists: [[reference_kb_freshness]]. The frontmatter traps: [[reference_kb_frontmatter_validation]].

- One fact per file, `docs/orchestration/knowledge/<slug>.md`, with its row in `INDEX.md` in the same commit, newest at the top of the table.
- The frontmatter must read the same to YAML and to the freshness gate's regexes:

  ```yaml
  ---
  name: <short title>
  description: '<one line, used to judge relevance; single-quoted, an apostrophe doubled>'
  teaches: [<decision-id>, …]    # flow form on one line: the freshness gate's regex reads no other
  verified: <YYYY-MM-DD>
  metadata:
    type: reference | decision | feedback | project
  ---
  ```

- `teaches:` names the decisions the entry explains: not every ID it mentions, never another repository's, never one still unratified.
- `verified:` moves only after each taught decision and the canonical source have been re-read and the entry corrected to match. A freshness failure is cleared that way, never by the date alone.
- An entry explains why; it is never the authority for a value. A value the explanation needs carries its authority and a one-line command that re-checks it.
- An entry marked `source: dev-resources` is a cache of that repository: publish an edit with `resources_sync.py --publish` and take it back by sync, never edit it in place ([[reference_resources_sync]]).
- Name a growing set, never its count.
