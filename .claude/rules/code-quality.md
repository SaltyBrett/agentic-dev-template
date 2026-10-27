---
paths:
  - "**/*.py"
  - "**/*.rs"
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
---

# Writing code

This page opens where `CONSTITUTION.md` section 4A does: the correct, cleanest, most direct design, and no
workaround until the direct fix is shown impossible. The numbers a gate holds code to are in
`docs/standards/coding_standard_v1.0.md`; what follows is the judgement no gate makes, and the code
reviewer reads every change against it.

- Read the story's design before the first line of code, and build what it says.
- Give each function one reason to change. A description that needs "and", a comment naming a phase,
  or a flag parameter says it wants splitting.
- Name things for what they are for. Write a literal once, as a named constant, wherever it would
  recur.
- Put policy in a table or data, not in a chain of branches over names.
- Extract a helper instead of copying, a near-copy with renamed variables included; the clone
  detector sees only exact copies.
- Make every error explicit: handle it, return it or raise it, never swallow it.
- Comment why, not what; the code says what.
- Follow the conventions the codebase already uses, even where another would be nicer.
- Build only what the story asks for, and delete code nothing calls.
- Never game a limit. Hiding logic in a closure, splitting into part one and part two, or adding a
  mode flag passes the measurer and fails the reviewer; split by responsibility instead.
- A limit you cannot meet is a finding for `docs/code_review_log.md`, with the Chair's response;
  never a hidden one. The standard advises and documents, and the Chair decides what proceeds.
