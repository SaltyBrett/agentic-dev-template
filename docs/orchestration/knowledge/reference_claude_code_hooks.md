---
name: Claude Code hooks run the cold start, bank the uncommitted interval, and guard the turn
description: 'How the SessionStart, Stop, PostToolUse and PostToolUseFailure hooks in .claude/settings.json carry decision 2026-10-22-001, read against the hooks reference on 2026-10-22: the 10,000-character cap on injected context, why compaction runs no gate, why the Stop hook asks once and never wedges, why the journal and notes are gitignored, what blocking PreCompact does, and which details only a live session showed. Read before editing a session hook, its script, or the settings that register it.'
teaches: [2026-10-22-001, 2026-10-22-004, 2026-10-22-005]
verified: 2026-10-23
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
| `Stop` | (none; Stop takes no matcher) | `session_stop.py` | `hookSpecificOutput.additionalContext` sends the agent back |
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
- **The persona** (decision 2026-10-22-005). The kickoff names an agent in the project's roster,
  `.claude/agents/` (decision 2026-10-23-003), and
  the event's `agent_type`, present only when the session started with `claude --agent <name>`,
  decides: equal to the kickoff's persona, one line says so; otherwise the agent's body is
  injected at priority 1, at startup and after compaction. A plain session and the VS Code
  extension so hold the persona and keep Claude Code's own system prompt, which `--agent`
  replaces whole. A kickoff that already copies the prompt verbatim gets no second copy.
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
- **The agent is sent back with `additionalContext`, not `decision: "block"`.** Both continue the
  turn under the same loop protections, but in the live probe a block also raised a user-facing
  "Stop hook error occurred" notice; the reference recommends `additionalContext` for guidance of
  the "do this before finishing" kind, and with it the notice disappeared.
- The journal is excluded from "uncommitted work" by path because it is written after every tool
  call, the notes edit included: counted, it would leave the notes stale forever. The broken
  variant passed the first fixture, which had the notes older than other work anyway; the fixture
  now puts the journal newest.
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

## What was observed (S2, `claude -p` in scratch clones of the committed hooks)

- **Injection at startup:** a fresh session's first turn quoted the "Cold-start gates" lines and the
  kickoff heading verbatim.
- **Re-injection after compaction:** a real `/compact` fired `SessionStart:compact`; the next turn
  quoted the restore header, a canary line from the notes and the kickoff heading. The journal
  held `start S2` then `compact S2` for the one session, which is how "still S2" was derived.
- **Stop:** with `sprint/sprint-status.md` modified the turn was sent back; the agent answered why
  it could not commit (tools were forbidden), the second stop was allowed and the user saw the
  unbanked list. Committed, the same prompt ended in one turn with no feedback.
- **Journal:** an Edit and a failing `ls` gave `Edit docs/README.md` and `Bash exit=1 ls …`.
- **`ask` rules:** `git push <r> --delete`, `git push <r> -d`, `gh repo delete` and
  `gh repo edit --visibility` were each refused in `-p` despite a matching allow rule (a `-p`
  session cannot answer a prompt); an ordinary push under the same allow rule ran. A trailing
  `:*` is the legacy wildcard, so `git push * :*` would ask on every push; the refspec-delete form
  (`git push <r> :branch`) is therefore not covered.
- **Concurrency beside the suite:** four writers paced to span nine `pre-commit run` stash windows.
  Ignored journal: 2,400 of 2,400 lines, no warning, the unstaged edit restored. The same with the
  journal tracked: "files were modified by this hook" failed the scan, the roll-back's
  `git apply` failed and pre-commit crashed nine times, 2,306 of 2,400 lines were lost, and the
  operator's unstaged edit to `README.md` was left only in pre-commit's cache patch.
- **`PreCompact`:** exit 2 blocked a manual `/compact` (`compact_result: failed`, "Compaction blocked
  by PreCompact hook"). The reference adds that a block on the compaction that recovers from a
  context-limit error makes the request fail, so the agent, out of context, cannot act on the
  reason. No `PreCompact` hook is registered: the `Stop` hook bounds the unbanked interval to one
  turn, and the `compact` branch restores what the files hold.
- **The sanitize check** named 18 items of mid-session build state and neither file, both on disk.
- **Broken variants:** nineteen, across the three scripts and `.gitignore`; every one fails at least
  one fixture (the two concurrency variants by a race, caught on every run so far).

## Rules

- Keep every injected report under the cap; add a section only with a priority and a source file.
- Never run a tree-judging gate from the `compact` branch.
- A Stop hook asks once. Anything stronger belongs in a git hook or CI, which enforce for every
  agent; these hooks are context and ergonomics.
- Edits to hooks in `.claude/settings.json` reach a running session through the file watcher; the
  session that wrote these hooks was governed by them from that point on.
