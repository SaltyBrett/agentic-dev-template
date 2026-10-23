---
name: Claude Code reads AGENTS.md natively, and any CLAUDE.md on the path hides it
description: 'From v2.1.277 Claude Code reads AGENTS.md itself, but only when no CLAUDE.md, .claude/CLAUDE.md or CLAUDE.local.md sits in the working directory or above it; observed on 2.1.308 with a canary in a scratch repository, both halves. Why the template retired its CLAUDE.md bridge, the silent hazard that creates, and what a SessionStart hook must not inject. Read before adding any Claude instruction file, or when Claude seems not to know the brain.'
teaches: [2026-10-22-001, 2026-10-22-005]
verified: 2026-10-22
metadata:
  type: reference
---

# Claude Code reads AGENTS.md natively, and any CLAUDE.md on the path hides it

> Durable learning. Wikilink: `[[reference_claude_code_agents_md]]`.
> Source: `https://code.claude.com/docs/en/memory.md`, section "AGENTS.md", read 2026-10-22.
> Companion: [[reference_macos_toolchain]] §6 (why never a symlink).

## What the docs say

- From v2.1.277, Claude Code reads every `AGENTS.md` and `.claude/AGENTS.md` in the working
  directory and its parents at session start, `@path` imports expanded. A built-in plugin does it
  (`cc-plugin-agents-md@builtin`; `agents-md@builtin` before v2.1.285).
- The default setting reads `AGENTS.md` only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or
  `CLAUDE.local.md` in the working directory or above it. `~/.claude/CLAUDE.md`, a managed
  `CLAUDE.md` and `.claude/rules/` do not count, and load alongside.
- It does not load before v2.1.277, with the plugin disabled, and sometimes in the first session
  after an upgrade from v2.1.276 or earlier.
- A natively read `AGENTS.md` fires no `InstructionsLoaded` hook; one a `CLAUDE.md` imports does.
- A `SessionStart` hook that prints `AGENTS.md` adds a second copy to the context.

## What was observed

2.1.308, 2026-10-22, a scratch git repository with no instruction file on its path. `claude -p`
asked for the canary word in its project instructions: with `AGENTS.md` alone it answered the word
`AGENTS.md` held; with an empty `CLAUDE.md` added beside it, `NONE`. Nothing in the output said the
brain had been dropped.

## Under `claude --agent`, and in a subagent

The sub-agents reference (read whole 2026-10-22): a project subagent loads the same instruction
files the main session does, `AGENTS.md` included, unless its definition sets `omitClaudeMd`;
Explore and Plan skip them. Run as the main session with `claude --agent <name>`, an agent with a
non-empty body replaces Claude Code's built-in system prompt whole, and `AGENTS.md` still loads.
Observed in S3, a scratch clone, `claude --agent framework-maintainer -p`: a canary from the agent's
body and the heading of `AGENTS.md` both came back, and the prompt was about 2,500 tokens smaller
than a control run without the flag. That replacement is why the template's sessions take their
persona from the start hook instead (decision 2026-10-22-005, [[reference_claude_code_hooks]]).

## Why the template retired its CLAUDE.md

Decision 2026-10-22-001 kept `CLAUDE.md` as an `@AGENTS.md` bridge until the installed Claude Code
reached v2.1.277. S2 found 2.1.308 and observed the native read, so the bridge went. Its
accelerators worth keeping (plan first, searches to a subagent, `.claude/settings.json` as context
and not enforcement) moved into `AGENTS.md`. Leaving the bridge would have been harmless to loading
(an imported `AGENTS.md` is not read twice), but it was a second file presenting itself as an entry
point in a repository that says there is one.

## The hazard the retirement creates

With the bridge, a stray `CLAUDE.md` added instructions. Without it, the same file replaces the
brain: an operator's `CLAUDE.local.md` for personal notes, a `CLAUDE.md` in a parent such as
`~/code/`, or a teammate's `/init` leaves Claude running without `AGENTS.md`, silently. `AGENTS.md`
names the three files and forbids them. An operator who wants a personal file sets **Project
instructions** to `claude-md-and-agents-md` in user settings; project and local settings files are
ignored for it.

## Rules

- Never add `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` to a repository built on this
  template, or to a directory above a clone of one.
- When Claude seems not to know the brain, look for one of those files on the path first.
- A `SessionStart` hook injects gate results and the kickoff, never `AGENTS.md` itself.
