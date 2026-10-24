---
name: Subagent model and effort in Claude Code
description: 'What Claude Code documents about setting a session''s model and effort, a subagent''s model and effort and their precedence, what a hook can see and refuse, and the caps it offers, read in its documentation on 2026-10-24 for the subagent ceiling and not yet observed. No setting caps a subagent relative to its parent, so the ceiling is a PreToolUse hook on the Agent tool; what to probe before building it. Read before building or changing TMPL-3.5.'
teaches: [2026-10-24-024]
verified: 2026-10-24
metadata:
  type: reference
---

# Subagent model and effort in Claude Code

> Durable learning. Wikilink: `[[reference_claude_code_subagent_model]]`. Read on 2026-10-24 from
> `https://code.claude.com/docs/en/sub-agents.md`, `hooks.md`, `model-config.md`, `skills.md` and
> `settings-reference.md`, through a summarizing fetch: the wording is close to the documents but
> not checked line by line, and nothing here is observed yet. Re-read before building.

## The session's model and effort

- Model, highest first: `/model` in the session, `claude --model`, `ANTHROPIC_MODEL`, the settings
  key `model`. Aliases include `sonnet`, `opus`, `haiku` and `fable`; a full ID works too.
- Effort: `/effort <level>`, `claude --effort`, `CLAUDE_CODE_EFFORT_LEVEL`, then the settings key
  `effortLevel`. Levels are `low`, `medium`, `high`, `xhigh` and `max`, depending on the model.

## What a hook can see

- The session's model reaches only the `SessionStart` hook, in its `model` field, which may be
  absent, and the model-switch hooks (`PreModelSwitch`, `PostModelSwitch`). No variable carries it.
- The session's effort reaches every tool hook, as `effort.level` in the input.
- A `PreToolUse` hook matched on `Agent` (renamed from `Task`) reads `tool_input.model` and can
  refuse the spawn by exit 2 or `permissionDecision: deny`, the reason going back to the model, or
  replace the whole input with `updatedInput`. Whether `tool_input` carries `effort` is not in the
  hooks page.

## How a subagent's model and effort resolve

- Model: the spawn's `model`, then the agent file's `model:` (`inherit` meaning the session's),
  then `CLAUDE_CODE_SUBAGENT_MODEL`, then the session's model.
  `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` puts the variable first.
- Effort: `CLAUDE_CODE_EFFORT_LEVEL`, then the spawn's `effort` (v2.1.292 and later), then the agent
  file's `effort:`.
- A forked skill runs at the session's model and effort and takes no effort of its own.

## The caps it offers

`availableModels` is an allow list and `maxEffortLevel` a fixed ceiling, the lowest scope winning.
Neither follows the session, and nothing compares a subagent with its parent. So a ceiling relative
to the session has to be a `PreToolUse` hook on `Agent` that resolves the model as above, an agent
file's `model:` included, and compares it with the session's model tracked from `SessionStart` and
the switch hooks. Claude Code ranks no models, so the comparison needs a ranking written as data.

## Probe before building

- Log the `Agent` tool's real `tool_input` from a `PreToolUse` hook: is `effort` there?
- Does a skill with `context: fork` reach the `Agent` matcher?
- Does a timed-out `PreToolUse` hook let the spawn through? A fail-closed hook must not.

## Rules

- Never trust a subagent's model from the spawn alone; resolve it through the agent file.
- Treat this entry as reading, not observation, until the probe has run.
