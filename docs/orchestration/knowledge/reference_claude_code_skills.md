---
name: A skill is repository markdown, a forked skill starts blind, and its frontmatter fails silently
description: 'How .claude/skills/ works, read against the skills reference on 2026-10-23: a skill with context: fork runs as general-purpose unless agent: says otherwise, sees none of the conversation, loads AGENTS.md and git status but not the persona the start hook injected, and runs in the background with fewer tools unless background: false; disable-model-invocation hides the description and blocks Claude''s own call; an unparsable frontmatter loads the skill with no fields and an unknown key is ignored, both silently. Why the closeout takes its brief as arguments, why AGENTS.md and the README''s catalog list every skill, and what the skill gate checks. Read before adding or editing a skill.'
teaches: [2026-10-23-001, 2026-10-23-013, 2026-10-23-009, 2026-10-23-022]
verified: 2026-10-23
metadata:
  type: reference
---

# A skill is repository markdown, a forked skill starts blind, and its frontmatter fails silently

> Durable learning. Wikilink: `[[reference_claude_code_skills]]`.
> Source: `https://code.claude.com/docs/en/skills.md`, read whole 2026-10-23 (Claude Code 2.1.308), and
> `sub-agents.md`, "What loads at startup" and "Available tools". Gate: `scripts/skill_scan.py`.
> Companions: [[reference_claude_code_rules]], [[reference_claude_code_agents_md]].

## What the reference says

- `.claude/skills/<name>/SKILL.md` is a project skill; the directory, or `name:`, is the command.
  Claude sees every description unless `disable-model-invocation: true`, which removes it from
  context and blocks Claude's own call with an instruction not to do the steps another way; only the
  user's `/name` runs it.
- `context: fork` starts a subagent of the `agent:` type, `general-purpose` when omitted, with the
  skill's body as its task. It does not see the conversation. A non-fork subagent loads the
  instruction files the main session does, `AGENTS.md` included, and a git-status snapshot; Explore
  and Plan skip both. No `SessionStart` hook fires for it, so the persona the start hook injects into
  the main session does not reach it.
- A fork runs in the background unless `background: false`, and a background subagent keeps only a
  short list of built-in tools (Bash, Read, Edit, Write and a few others). Under `claude -p` the
  invoking session waits for a fork either way. No subagent has AskUserQuestion.
- Line 1 must be `---` or the whole file is the body. YAML that does not parse loads the skill with no
  fields; a key Claude Code does not know is ignored. Neither is reported.
- A `` !`command` `` line runs before Claude sees the skill and aborts the invocation when it fails or
  when no permission rule allows it; the skills here use none.
- After compaction each invoked skill is re-attached, first 5,000 tokens only, so the important steps
  go first.

## What was observed (2026-10-23, 2.1.308)

- In the session that wrote them, the skill listing in context gained `closeout`,
  `planning-session` and `document-production` within the turn, and never `release` or
  `pristine-cut`, whose `disable-model-invocation` keeps their descriptions out. A `claude -p` run's
  init event listed all five as commands.
- `claude -p "/closeout <slug> <brief>"` in a scratch clone with no remote: the skill ran as a
  subagent (its events carried a `parent_tool_use_id`, and the `PostToolUse` journal tagged each
  command `[general-purpose]`, so hooks fire for a forked skill's tools). Its first command was
  step 1's `git status --short`; step 2 came from git alone, finding the previous closeout commit
  and the decisions added since. At step 3 the sync needed an approval `-p` could not give, and it
  stopped there with the tree untouched and every exit code reported. It also noticed that the
  brief's task could not start under the dependency rule.
- In a live session the operator could approve, the forked closeout ran through commit and push
  ([[reference_claude_code_substrate]]).

## Why the closeout takes its brief as arguments

A forked closeout starts with the tree and nothing else, which is the point: it cannot die of the
main session's full context. But the next session's tasks, success criteria and reads are the
session's judgement, and judgement is not in git until written down. So the session commits all that
is durable first (its entry, decisions, knowledge, tracker), and passes the rest, which is one
session's worth, as the skill's arguments (decision 2026-10-23-001, the operator's choice). The fork
refuses an uncommitted tree rather than guess what the session meant to bank.

## Why `AGENTS.md` and the README list every skill

Claude Code finds a skill by its folder; Codex and a local model find nothing there by themselves.
The table in `AGENTS.md` names each `SKILL.md` by path, and the gate refuses a skill missing from it
and a path with no skill, so a procedure cannot be invisible to an agent that is not Claude. The
frontmatter is Claude Code's settings; another agent follows the body. The operator needs the same
list for the commands they type, so the README's `## Catalog` section names each skill by the same
path beside its command, and the gate holds it to the skills as it holds `AGENTS.md` (decisions
2026-10-23-009 and 2026-10-23-022). It reads that section only: a path the walkthrough mentions
catalogues nothing, and a README with no catalog fails rather than reading as an empty one.

## What the gate checks, and what it cannot

Every silent frontmatter failure above, and every command in a skill's code (inline spans and fenced
blocks): a `pre-commit run` must name a hook the config declares, at a stage it declares, with
`--all-files`; a `scripts/<name>.py` must exist with every flag named; a hook's own entry run with an
interpreter is refused, since a gate is invoked through pre-commit ([[reference_precommit_interpreter]]).
In the team-selection skill it also reads the one YAML block of presets and connections: every
persona named must be in `personas/`, every connection pinned, and `.mcp.json` must hold a
connection only in a project that activated its persona ([[reference_blender_mcp]]). It cannot read prose, so a command written outside code is not seen, and it cannot judge whether the
steps are right.

## Rules

- A procedure lives in one `SKILL.md`, listed in `AGENTS.md`; a standard keeps the law and points to it.
- A forked skill's body stands alone: it says what to read from the tree and what to refuse.
- A skill whose steps cannot be undone is the operator's alone (`disable-model-invocation: true`).
- Write every command in code, so the gate reads it.
