---
name: Path-scoped rules load beside the file, and fail silently both ways
description: 'How .claude/rules/ works, read against the memory reference on 2026-10-22 and observed with a canary: a rule with paths: loads when Claude reads, writes or edits a matching file and not before; a rule without paths:, or whose YAML does not parse, loads in every session; a glob that matches nothing never loads. Claude Code reports none of it, so the session state gate checks every rule, and why the check looks for copied clauses, not only whole sentences. Read before adding or editing a rule.'
teaches: [2026-10-22-006]
verified: 2026-10-22
metadata:
  type: reference
---

# Path-scoped rules load beside the file, and fail silently both ways

> Durable learning. Wikilink: `[[reference_claude_code_rules]]`.
> Source: `https://code.claude.com/docs/en/memory.md`, "Organize rules with `.claude/rules/`", read 2026-10-22.
> Gate: `scripts/session_closeout.py` (`lint_rule`) in `session-closeout-check`. Companion: [[reference_claude_code_agents_md]].

## What the reference says

- A rule is a markdown file under `.claude/rules/`, found recursively. With `paths:` (a YAML list or a
  comma-separated string of globs, relative to the project root) it loads when Claude uses Read,
  Write or Edit on a matching file, or reads one with `cat`; `paths:` is the only key Claude Code
  reads, and the frontmatter is stripped before the rule enters the context.
- Without `paths:` a rule loads at launch, like `CLAUDE.md`. A frontmatter that does not parse is
  ignored and the rule loads as if it had none. A glob that matches nothing matches nothing.
- After compaction a path-scoped rule loads again only when a matching file is touched again.
- A rule that loads on demand is cut at a per-file size limit, 40,000 characters on a 200K window.

## What was observed (S3, `claude -p` in a scratch clone)

A canary rule scoped to one knowledge entry: a session that used no tool answered `NONE`; one that
read the matching entry gave the canary; one that read `README.md` answered `NONE`.

## Why the gate checks every rule

Each failure is silent and each defeats the purpose: an unscoped rule is a second always-loaded
brain beside `AGENTS.md`, and a dead glob is judgement that never arrives. The state gate refuses a
rule whose `paths:` does not parse as a list of globs, a rule no file git would commit matches (its
glob translation: `**/` any run of directories or none, `**` anything, `*` and `?` inside one path
segment, braces expanded), and a rule that repeats `AGENTS.md`.

The repeat check first compared whole sentences. The live plant copied the first clause of an
`AGENTS.md` sentence into a rule and passed, so it now flags a sentence of six or more words found
inside the other text, in either direction; shorter shared phrases are vocabulary.

## Rules

- A rule holds judgement for the files it names and points to the entry that explains it; it never
  restates `AGENTS.md`, and anything every session needs belongs in `AGENTS.md`.
- Another agent cannot load a rule by path: `AGENTS.md`'s governance map tells it to read the rules
  whose `paths:` match what it edits.
