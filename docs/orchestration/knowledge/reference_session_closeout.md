---
name: Session closeout is a gate and its artifacts live one session
description: 'Why the end-of-session protocol became a script: a prose checklist let a kickoff prompt live only in chat and let handoffs accrete rules nothing watched. Numbered sessions, a handoff/kickoff pair consumed by one session then archived, personas gated by shape not by list and append-only by version against the committed copy, the tracker''s dependency and live-placeholder rules as controls, and the one defect the live probe found.'
teaches: [2026-09-21-001, 2026-09-23-002, 2026-09-24-001]
verified: 2026-09-24
metadata:
  type: reference
---

# Session closeout is a gate and its artifacts live one session

> Durable learning. Wikilink: `[[reference_session_closeout]]`.
> Enforced by `scripts/session_closeout.py`; procedure in `docs/standards/session_handoff_standard_v2.0.md`.

## The failure

The session end protocol was five prose steps. A session followed them, then decided the kickoff
prompt for the next session "is not a repo artifact" and handed it over in chat. The next session
had no prompt in the tree. The same session left an open question in a commit message body. Neither
was caught, because nothing checked.

Handoffs had also become a second knowledge base: the standard's template carried rules and
constraints, so durable facts accumulated in files that no index listed and no freshness gate read.

## The mechanism

- **Sessions are numbered** from the newest `## S<N> — date — title` entry in sprint-status. That
  heading is load-bearing: every mode of the gate reads N from it.
- **A session consumes one pair** (`HANDOFF_S<N>.md`, `KICKOFF_S<N>.md`) and **produces the next**.
  The closeout archives everything older, so the main folder holds at most two consecutive numbers.
- **Structure has no home for durable content.** Exact headings, no extras. Decision IDs must be
  indexed, wikilinks must resolve, tasks must cite tracker stories, and the persona block must equal
  the registry's invocation. A fact that belongs elsewhere has nowhere to sit.
- **Reading follows.** `archive/` is never a mandatory read, so leaving a fact in a handoff loses it
  one session later. That is the enforcement the gate cannot do by reading prose.
- **`--verify` at cold start** turns the closeout into a loop: the next session refuses to build
  until the previous one is closed. A session is not done until its successor can start.

## Personas are gated by shape, not by list

Predicting every persona a future project needs is impossible, so the gate never checks membership
in a list. It checks that the slug a kickoff names resolves to a registered file with the required
sections, and that the kickoff's copy matches. A persona is written when a task first needs it and
registered in the same commit, exactly as a knowledge entry is. The registry grows from real sessions.

## Personas are append-only, against the committed copy

A persona is reused across projects and, once `dev-resources` is its home (decision
2026-09-23-002), across repositories, so a kickoff written against one text must not be silently
answered by another. The gate reads each persona as committed at HEAD (`git show`) beside the
working copy: an Invocation that differs at the same `version:` is refused, a version never goes
down, and the Changelog must carry a bullet for the current version. The comparison is against
HEAD because that is what every stage of the gate can see, in this repository and in a consumer
that runs the published `persona-lint` hook; a bump that changes only Expertise or Insists on is
allowed, since the rule guards the text an agent is addressed with. The kickoff names the version
it copied, and the linter checks it against the registry; the copy check already catches a
drifted Invocation, so the field is for the reader, gated so it cannot be wrong.

A committed copy from before the rule, with no `version:`, constrains nothing: the migration
commit that adds the key is then legal, and every later commit is compared.

## Every wikilink in the tree resolves, not only a handoff's

The handoff linter proved wikilinks for handoffs alone; a `[[slug]]` in a standard, a decision
body or a knowledge entry pointing at nothing was invisible. The state gate now reads every text
file git would commit (the banned-feature scan's file list, so a scratch file is judged and an
ignored one is not) and refuses a link that resolves to no entry.

Two things follow from scanning the gate's own source:

- **The allow set is exact and literal.** The convention's documents write `[[slug]]` and
  `[[<slug>]]` to explain the convention, the gate's message writes `[[{slug}]]`, and the
  fixtures write `[[reference_nowhere]]`. Each is in `WIKILINK_ALLOW` by name. A fixture that
  needs a new dangling slug adds it there in the same commit.
- **A fixture that lives in a scanned file can only use allowed literals.** The dangling cases
  therefore vary the allow argument (`set()`, a near miss) rather than the slug. And because the
  fixture slug is allowed, it is the one slug a live probe must not use: the live probe linked a
  slug `reference_no_such_entry` beside `[[reference_nowhere]]`, and only the first was reported.
  This entry cannot write that probe as a link either; the gate read the draft that did.

## The tracker's two rules are controls, not prose

The sprint standard said "never start a story whose dependencies are not Done" and "no
`[EXAMPLE]` or `{{PLACEHOLDER}}` content in a live sprint" for nine sessions before anything
checked either (decision 2026-09-24-001). The state gate already parsed every story row for the
statistics, so both became row checks on the same parse: `tracker_stories` reads each row once,
and the statistics, the kickoff's story IDs and the dependency rule cannot disagree about what a
row is.

- **`dependency-order`** judges after the fact: a story `In Progress` or `Done` whose listed
  dependency is anything but `Done`, or is no story at all. `Not Started` and `Blocked` are
  waiting, which is what the rule asks of them. A dependency inside the example epic is skipped
  with the epic, so a real story that names one fails as naming no story.
- **`live-placeholder`** has a condition the rule text does not state: it applies in a project
  (a `.project-profile` exists) whose tracker holds a non-example epic. The template has no
  profile and ships every shape; a fresh project ships the example epic and must pass its first
  commit; the planning session that writes the first real epic is when the examples go. The
  condition is on the tracker alone, and it opens the check on all three sprint documents at once,
  so the example decision row leaves with the example epic.
- **Quoted text is not a placeholder.** The decision bodies a project inherits write `[EXAMPLE]`
  and `{{PLACEHOLDER}}` in code spans to explain the convention, and one decision does so inside a
  table row. The scanner strips inline code and skips fenced blocks before it looks, and judges
  `[EXAMPLE]` only in a table row or a heading; the marker in running prose is a mention. The
  live probe was a scratch commercial project through the real initializer: a real epic beside the
  example epic exited 1 on three lines, the tracker's example heading and the log's example row and
  heading; with those removed it exited 0 while seven quoted mentions still sat in the log.

## The defect the live probe found

`verify_state` had a fresh-project exemption: session 1 may start with no incoming pair. Run as the
closeout of S1, the same exemption passed a session that had produced no pair for S2. The self-test
passed because no fixture asked the closeout question. The fix separates `closing=True` from the
cold-start verify, and a fixture now pins it. The lesson repeats one already recorded: a fixture set
that only asks the questions you thought of is not proof; run the tool on the real tree as well.

## pre-commit reports the rotation as a failure

When the closeout archives a pair, pre-commit prints `files were modified by this hook` and exits
1, whatever the gate printed. That is pre-commit's convention for any hook that changes the
working tree, not a verdict: the gate's own output above it says PASSED or BLOCKED. Read the
gate's verdict, then run the command again; with nothing left to archive it exits 0. The two
exit codes together are what the handoff records.

## Rules

- Never hand-type handoff or kickoff headings. `--scaffold --persona <slug>` writes them.
- The sprint-status entry comes first; the scaffold and the closeout both read the session number
  from it.
- If the closeout cannot be completed, commit an emergency entry and say so. `--verify` failing next
  session is the correct outcome, not something to route around.
- Run the closeout with `--all-files`, or pre-commit judges a stash of the last commit rather than
  the files just edited ([[reference_precommit_stash]]).
- A kickoff task may cite only this repository's stories. The lint reads every ID-shaped token in
  a task bullet, so another project's story ID (the derived probe's, say) fails it; name that
  story in words.
