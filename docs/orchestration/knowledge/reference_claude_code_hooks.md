---
name: Claude Code hooks run the cold start, bank the uncommitted interval, and guard the turn
description: 'How the SessionStart, Stop, PostToolUse and PostToolUseFailure hooks in .claude/settings.json carry decision 2026-10-22-001, read against the hooks reference on 2026-10-22: the 10,000-character cap on injected context, why compaction runs no gate, why the Stop hook asks once and never wedges, why the journal and notes are gitignored, what blocking PreCompact does, and which details only a live session showed. Read before editing a session hook, its script, or the settings that register it.'
teaches: [2026-10-22-001, 2026-10-22-004]
verified: 2026-10-22
metadata:
  type: reference
---

# Claude Code hooks run the cold start, bank the uncommitted interval, and guard the turn

> Durable learning. Wikilink: `[[reference_claude_code_hooks]]`.
> Source: `https://code.claude.com/docs/en/hooks.md`, read in full on 2026-10-22 (Claude Code 2.1.308).
> Scripts: `scripts/session_start.py`, `scripts/session_stop.py`, `scripts/session_journal.py`.
> Companions: [[reference_claude_code_agents_md]], [[reference_precommit_stash]].

## What is registered, and why each piece is shaped as it is

| Event | Matcher | Script | Effect |
|-------|---------|--------|--------|
| `SessionStart` | `startup\|clear\|compact` | `session_start.py` | plain stdout becomes context |
| `Stop` | (none; Stop takes no matcher) | `session_stop.py` | `{"decision":"block","reason":…}` sends the agent back |
| `PostToolUse` | `Edit\|Write\|Bash` | `session_journal.py` | one journal line |
| `PostToolUseFailure` | `Edit\|Write\|Bash` | `session_journal.py` | one journal line with the exit code |

- **Exec form** (`"command": "python3", "args": ["${CLAUDE_PROJECT_DIR}/scripts/…"]`): the reference
  prefers it whenever a path placeholder appears, since no shell re-parses the path.
- **`clear` beside `startup`**: `/clear` empties the context exactly as a new session does.
  `resume` and `fork` restore the conversation whole, so the script prints nothing for them.
- **A Bash failure arrives on `PostToolUseFailure`**, not `PostToolUse`, with `error` whose first
  line is `Exit code N`; that line is the only stable part of the string. Hence two registrations
  for one journal.

## SessionStart: the cap, and what compaction must not run

- Plain stdout and `additionalContext` are each **capped at 10,000 characters**. Past it Claude Code
  writes the text to a file and gives Claude a 2,000-character preview, and does not ask Claude to
  read the rest. A kickoff (about 5 KB) plus a sprint-status entry plus the gate lines is close to
  the cap, so the script renders sections by priority and cuts the lowest first, naming the file
  that holds a cut section whole. The self-test proves no input exceeds the budget.
- **After compaction the tree is dirty by design.** `session-verify` would report the previous
  session unclosed, which is false and would send the agent to "finish the closeout". The `compact`
  branch runs no gate and no pull; it prints the notes, the kickoff, `git status --short`, the
  journal tail and the newest entry.
- **The session number after compaction** comes from the journal's `start S<N>` line for this
  session id. The sprint-status rule (newest entry, plus one if that kickoff exists) misreads a
  session that has already written its own entry, or scaffolded the next pair.
- **`git pull --ff-only --no-rebase`.** With `pull.rebase` set, a pull refuses any dirty tree even
  with nothing to pull; observed in S2 as exit 128 on the first live run.
- **The verify runs with `--all-files`.** Without it pre-commit's stash hides an unstaged edit and a
  dirty tree passes (decision 2026-09-22-003, amended; [[reference_precommit_stash]]).
- The report also says whether both hook types are installed and whether a `CLAUDE.md` on the path
  hides `AGENTS.md` ([[reference_claude_code_agents_md]]); the user-level `~/.claude/CLAUDE.md`
  does not count. It never prints `AGENTS.md` itself.
- Text is written as statements of state; the reference warns that imperative "system" phrasing can
  trip Claude's prompt-injection defences.
- In an interactive session, hooks from settings files wait until the folder is trusted; in a `-p`
  session the folder is treated as trusted and committed hooks run at once.

## Stop: ask once, never wedge

- Rules: a tracked file under `sprint/` modified (staged or not); uncommitted work newer than the
  working notes; the notes without exactly Plan, Open decisions, Half-done.
- Untracked files are listed one by one (`--untracked-files=all`). Under `normal`, a wholly
  untracked directory is one entry with the directory's mtime, so a new file inside it, and the
  notes themselves, were invisible; the self-test caught it on its first run.
- `stop_hook_active` is true when the turn is already a continuation from a Stop hook. The script
  then allows the stop and shows the user a `systemMessage` naming what is unbanked. Blocking again
  would loop until Claude Code's cap of eight consecutive continuations; an agent with a real reason
  not to commit says so once and the user hears it.
- Plan mode is allowed silently: nothing can be committed or written there.
- `onFailure: "block"` has no effect on Stop hooks (the reference: Claude cannot repair a hook that
  will not run), so a crashing script allows the stop; it prints its error to stderr.

## The journal and the notes

Both are gitignored (decision 2026-10-22-004): the journal records raw commands, which must not
enter a public history, and an ignored file is outside pre-commit's stash, so an append from a
parallel tool call cannot land inside a stash-and-restore window. Each line is one `os.write` on an
`O_APPEND` descriptor under `flock`, bounded far below `PIPE_BUF`; the self-test runs eight
processes appending sixty lines each and requires every line whole. The closeout gate resets both
on a pass; the start script recreates the notes when missing.

## Rules

- Keep every injected report under the cap; add a section only with a priority and a source file.
- Never run a tree-judging gate from the `compact` branch.
- A Stop hook asks once. Anything stronger belongs in a git hook or CI, which enforce for every
  agent; these hooks are context and ergonomics.
- Edits to hooks in `.claude/settings.json` reach a running session through the file watcher; the
  session that wrote these hooks was governed by them from that point on.
