# Knowledge Base Index

**This is the single source of truth for accumulated knowledge and feedback.** It is tool-neutral: every
agent (Claude Code, Codex, future tools) reads and writes here, never into a tool's private memory.
`AGENTS.md` holds the law and the cold-start sequence that points here.

> **Every entry declares what it teaches and when it was verified** (`teaches:`, `verified:`). An entry
> whose `verified:` predates a change to a decision it teaches is SUSPECT: check it against the decision
> and the canonical source before acting on it. `scripts/kb_freshness_scan.py` enforces this on every
> commit. The frontmatter shape and the writing rules are in
> `.claude/rules/knowledge-entries.md`, which Claude Code loads when an entry is read or edited.

---

## How this works

- **Read:** at session start, read this index, then only the entries relevant to the current task.
- **Write:** one fact per file, `docs/orchestration/knowledge/<slug>.md`, with a row in the table below;
  every corrected mistake becomes an entry so it cannot recur.
- **Link:** reference other entries with the wikilink convention `[[<slug>]]`, which resolves to
  `docs/orchestration/knowledge/<slug>.md`.

---

## Entries

| Slug | Summary | Type |
|------|---------|------|
<!-- Add one row per knowledge entry above this line, newest first -->
