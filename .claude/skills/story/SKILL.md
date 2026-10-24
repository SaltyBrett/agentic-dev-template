---
name: story
description: 'Run one story end to end through the team''s roles: each stage''s role called as a subagent, writing its artifact in docs/stories/<ID>/; the story-artifacts gate and the stage''s own gates run and the artifact committed before the next role starts; the story stops for the Chair at every review trigger and every review or security finding, and when a gate fails three times running. The Chair runs it. Arguments: the story ID, then `status` to report where it stands.'
argument-hint: '<ID> [status]'
disable-model-invocation: true
---

# Story

The Chair runs this to build one story with the team (decision 2026-10-24-004). It runs in the
main session, never forked: only the main session can ask the Chair, and a subagent can neither ask
nor see the conversation. The law is `docs/standards/team_standard_v1.0.md`; read it whole before
the first stage, and `docs/standards/coding_standard_v1.0.md` before a build. Another agent reads
this file and follows it as instructions.

Arguments: $ARGUMENTS

## The rules that hold at every step

- Roles hand off through committed files, never through this conversation: a role reads its input
  artifact and writes its own, and nothing it says outside the file carries to the next role.
- Each artifact passes `pre-commit run story-artifacts --all-files` and its stage's own gates, and
  is committed, before the next role starts.
- The story stops only for the Chair (a trigger, a finding, a question a role returns) or when a
  gate still fails on the third attempt running. It says what it stopped on, and waits.
- Nothing forces a code change: a finding waits only for the Chair's response in
  `docs/code_review_log.md` (decision 2026-10-24-011). The log is appended to, never edited.
- The verifier and the reviewer are never the builder. Nothing ships without the Chair's approval
  in `approvals.md`.

## Where the story stands

There is no state file; the story's folder is read before anything else is done.

- `docs/stories/<ID>/` holds one file per stage reached, each opening with the frontmatter of the
  standard's §2. The story resumes at the first stage of its type, in §3's order, with no file or
  with a `status:` other than `pass`. With no folder it starts at the brief.
- `approvals.md` holds the Chair's approvals; `docs/code_review_log.md` holds every finding with
  the Chair's response.
- `<ID> status`: list the type's stages, each passed, failed, waiting on the Chair or not started,
  with the triggers hit and not yet approved and the findings not yet answered. Change nothing.

## Before the first stage

1. The story is a row of `sprint/story-tracker.md` with every dependency Done; a story the tracker
   lacks is planned first, with the planning-session skill.
2. The roster, `.claude/agents/`, holds a role the map allows at the brief. After the brief, it
   holds one for every stage of the brief's type. A stage with none stops the story, naming the
   roles the map allows there; the team-selection skill activates one.
3. Before a build that writes code, read whether the project has adopted the coding standard
   (`code-profile.yaml` at its root). With none, `code-standard` passes saying so; tell the Chair
   once.

## Each stage

1. **Choose the role:** the roster persona §3 allows at the stage that fits the story. Ask the Chair
   only when two fit equally.
2. **Call it** as a subagent of that agent type, its slug. A roster agent loads only in a session
   opened in the project; where its type cannot be called, call a general-purpose subagent whose
   prompt opens with the persona's prompt, the text below the frontmatter of
   `.claude/agents/<slug>.md`. Its brief:
   - the story's tracker row, and the path of its input artifact (for the brief, the PRD
     requirement the row cites);
   - the stage's frontmatter from §2, `input:` the stage just before it (`none` for the brief), and
     what §2 says the stage's file holds;
   - the triggers of §4 by name, to declare in `triggers:` any its work hits;
   - write only its artifact, and for the build the code and its tests; commit nothing; ask
     nothing, but put a question for the Chair in the artifact and set `status: needs-operator`.
3. **Gate it:** `pre-commit run story-artifacts --all-files` and the stage's own gates (below). A
   failure goes back to the same role with the gate's output. On the third failure running, stop:
   report the gate, its output and the three attempts.
4. **Commit it** as `checkpoint: <ID> <stage>`, holding only what the stage made.
5. **Stop for the Chair** when the artifact's `triggers:` names a trigger `approvals.md` lacks, a
   build touched a trigger path, or the status is `needs-operator`. Say what was hit and what
   going on means, and wait for the Chair's words. Approved: a row in `approvals.md`,
   `| Trigger | What was approved | Chair's words | Date |`, the words verbatim, committed as
   `checkpoint: <ID> approved — <trigger>`. Not approved: the story stops where it stands, and the
   Chair says what changes.

## The stages

A stage §3 makes optional is passed over only where its condition holds (a game build that changed
no code, a media story that ships nothing), and the Chair is told.

- **brief:** `type:`, one of §3's types, and `## Acceptance criteria`, numbered, each one a check
  can observe. Its commit also sets the story In Progress in the tracker, with the Summary
  Statistics in the same edit.
- **design:** within the approved architecture in `docs/architecture/`; it names each file the build
  changes and declares each new dependency, schema change, external service and cost.
- **build:** the builder writes the code and its tests. Then:
  1. Stage the change and run `pre-commit run code-standard --all-files --verbose`. Each
     `note  trigger:` line is a trigger path the change touches: stop for the Chair after the
     commit, as step 5 says.
  2. On `PAUSED`, the builder fixes what the design and `CONSTITUTION.md` §4A ask of it, counted as
     an attempt. Each finding left goes to the Chair with the gate's advice; the gate's suggested
     row, the Chair's words in its last cell, is appended to `docs/code_review_log.md` in the same
     commit as the code.
  3. Commit the code as `checkpoint: <ID> build — <what it does>`; then write that commit's hash
     into `build.md`'s `commits:` and commit `build.md` as the stage's artifact.
- **verify:** the verifier runs each criterion's check itself and records what it observed, a row
  per criterion in `## Checks`. A failed criterion sends the story back to the build with the
  verify's failures as the builder's brief, then to verify again; the third failed verify running
  stops the story.
- **review** and **security:** each finding is a row of the artifact's `## Findings`, Where a place
  (`path:function`) and Finding opening with a rule and its value. The role does not write the
  log. Commit the artifact, then put each finding to the Chair with its severity and fix. Append
  each answer as a row of `docs/code_review_log.md` in the coding standard's §4 columns, Change the
  story ID, Source the role, the Chair's words in the last cell, and commit before the next stage.
  A finding the Chair wants fixed goes back to the builder first, and its row, naming the fix in
  Change made, is appended once the fix is committed; verify and review then run again on the new
  build. Security is `security-engineer` with §6's brief, wherever §3 or a trigger brings it in.
- **docs:** the writer changes the documents the story's reader uses (a runbook, the README),
  naming each.
- **release:** a deploy or release is always a trigger. Before the role starts, ask the Chair to
  approve shipping, naming what ships and where, and record the row. The role ships, watches the
  CI run to its end (`gh run watch <run-id> --exit-status`) and names it as `run:`; a red run is a
  failed attempt. Then, in one commit, `release.md` and the story set Done in the tracker with the
  Summary Statistics; `pre-commit run story-artifacts --all-files` judges every trigger and finding
  of the story as it closes.

## Stopping and resuming

Every stage is committed before the next starts, so a stop loses nothing. `/story <ID>` resumes at
the first stage not passing, once the Chair's answer it stopped on is recorded. A story may span
sessions; the session's closeout is the closeout skill's, never this skill's.
