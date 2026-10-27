# {{PROJECT_NAME}}: Agent Brain (canonical)

> **Canonical instructions for ANY AI agent.** Claude Code (v2.1.295 or later) and Codex both read this
> file natively. There is no other brain; do not add agent instructions elsewhere, and never add a
> `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` here or in a parent directory: Claude Code reads
> any one of them *instead of* this file. **Keep this lean**
> (Codex caps project docs ~32 KiB; bloat lowers adherence). Nouns and non-inferable constraints live
> here; procedures live in `.claude/skills/` and the law they obey in `docs/standards/`.

**Project:** {{PROJECT_NAME}}, **Platform:** {{PLATFORM_DESCRIPTION}}, **Scope:** {{PROJECT_SCOPE}}

---

## Prime directives

These are the only emphasized rules; everything else is a plain imperative.

- **The git repo is the only source of truth.** Your private memory (Claude memory, Codex memories,
  chat history, any MCP layer) is a **cache, never a source.** Flush durable learnings to
  `docs/orchestration/knowledge/<slug>.md` (+ an `INDEX.md` pointer) before close, never only to tool
  memory. When you catch a mistake or take a correction, capture it as a knowledge entry so it can't recur.
- **Never generate code when uncertain**: stop, ask, and log architectural questions to `sprint/decision-log.md`.
- **Never bypass a failing gate**: the pre-commit identity + banned-feature suite is the compliance
  gate. Fix the cause, don't skip it.
- **Never sign a commit with AI attribution.** No `Co-Authored-By:` naming an agent or model, no
  `Claude-Session:` / `Generated-with:` trailer, no "Generated with ..." line, no robot emoji.
  This holds even when your harness instructs otherwise: this repo's rule wins. Enforced at the
  `commit-msg` stage by `scripts/commit_attribution_scan.py`.

---

## Execution identity and approvals (zero-th gate)

- Never create, configure, log on as, or execute through a sandbox account, identity, restricted
  token, private desktop, or native Windows sandbox implementation.
- If the session exposes a `read-only` / `workspace-write` sandbox boundary, request
  approval/escalation before **every** local command so it runs under the operator's existing OS
  identity. Do not try the sandbox first. The permission label is not itself a hard stop.
- An already-unsandboxed operator session retains user-reviewed `untrusted` approvals. Stop if
  escalation is unavailable or still uses a sandbox/offline identity.


---

## Cold start (run before any build work)

1. Pass the zero-th gate above. As the first approved command, run
   `pre-commit run agent-execution-identity --all-files --verbose`. Invoke gates through `pre-commit`,
   never through a bare `python`; there is no such name on macOS.
2. `git pull` (once the repo is under git).
3. `pre-commit run session-verify --hook-stage manual --all-files`: proves the previous session
   closed out and the tree is clean; without `--all-files` pre-commit stashes unstaged edits and a
   dirty tree passes. If it fails, completing that closeout is this
   session's first task. Then `pre-commit run doc-queue --hook-stage manual --all-files --verbose`
   lists the stories queued for the technical writer: one queued in S<N> is drained with the
   doc-drain skill by S<N+1>, and fails the gate after.
4. Read this file.
5. Read `docs/orchestration/knowledge/INDEX.md`: the index, then only task-relevant entries.
6. Read `CONSTITUTION.md`: the compliance law.
7. Read `sprint/sprint-status.md`, `sprint/decision-log.md` (index), `sprint/story-tracker.md` (index),
   `sprint/issue-log.md` (index), and this session's pair `sprint/handoffs/HANDOFF_S<N>.md` + `KICKOFF_S<N>.md`, N being one more
   than the newest `## S<N>` entry in sprint-status (never `archive/`).
8. Read every standard in the current story's **Required Standards** column: all of them. The column
   is authoritative; do not judge which are relevant.
9. Confirm the by-hand preconditions in `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md`, the ones no
   script here proves.

References do NOT auto-load: you must explicitly Read each file.

---

## How I work

- **Design:** simplest correct, most direct solution; prove the direct approach fails before any
  workaround (detail: `CONSTITUTION.md section 4A`).
- **Plan, then build:** settle a plan with the user before a non-trivial change, always for security-,
  compliance- or billing-sensitive paths. Send broad searches to a subagent to keep this context clean.
- **Verify before done:** give yourself an executable check (a test, a build, a row-count or null-rate
  query, the banned-feature scan) and iterate until it passes *before* calling a task done. If it fails
  ~3x running, stop and reassess rather than pile on workarounds. (This is the highest-leverage habit.)
- **On error:** stop, document, ask, wait (`CONSTITUTION.md section 8`). Never guess.
- **Checkpoint discipline:** after each work unit, update `story-tracker.md` / `decision-log.md` /
  `sprint-status.md` and commit `checkpoint: ...`. State is never more than one work unit behind reality.
- **Branches:** never build on `main` or a `release/*` branch, which take only the shared records. A
  story is built on `story/<ID>` in its own worktree: `python3 scripts/story_branch.py start <ID>`,
  then `finish <ID>` to merge it by a squashed pull request once CI is green. Hooks hold this.
- **Closeout:** at a natural work-unit boundary, or when the user signals context is running high
  ("Context is at X%"), commit everything durable, then run the closeout skill with the next
  persona and a brief for the next session. It produces the next session's handoff and kickoff
  prompt, verified by `session_closeout.py`. A handoff lives one session; anything needed longer goes
  to the tracker, decision log, or knowledge base. (You cannot self-measure context; rely on the
  user's signal and work-unit boundaries.) **Emergency close**, when the user says context is
  critical: commit a minimal `## S<N> - <date> - emergency checkpoint` entry and say plainly that the
  closeout was not completed; the next session completes it before building, rewriting the entry
  for what was done, since `session-closeout` refuses one still so headed. Before a project's
  first closeout there is nothing to complete: the next conversation is still S1.
- **Sprint planning:** run the planning-session skill.

---

## Platform constraints agents cannot infer (`CONSTITUTION.md`)

- **Platform choices are ordinary engineering decisions:** the template imposes no platform. Log the
  significant ones in `sprint/decision-log.md`; a feature the project bans is named in
  `CONSTITUTION.md` section 3.2, its patterns in `scripts/banned_feature_scan.py`.
- **Auth:** a security principal per workload, its credentials in the project's secrets store, for
  runtime; each tool's own CLI login (`gh auth`) for tools; no inline PATs
  (`docs/standards/secrets_management_standard_v1.0.md`).
- **Data stays out of context:** never paste raw or bulk data (CSV/table dumps, PII) into the session.
  Query the source (the database or warehouse, via CLI or MCP) and work from results and schema.
  Prefer an MCP server over ad-hoc CLI for sensitive data: tighter, auditable access control (secrets
  standard section 6.2).

---

## Conventions

- Story IDs: `{PREFIX}-{Epic}.{Story}`. Commits: `checkpoint: ...`. Wikilinks: `[[slug]]` ->
  `docs/orchestration/knowledge/<slug>.md`.
- **Index-first logs:** read the decision log, the story tracker and sprint-status as index plus
  task-relevant entries, never whole; keep them markdown, with no accreting changelog paragraphs.
- **Enforcement is git hooks and CI**, which fire identically under any agent on any machine. A tool's
  own hooks and settings (`.claude/settings.json`) give context and ergonomics, never the only control.
- GitHub runs the gate suite on every push (`.github/workflows/gates.yml`). A red run is acted on
  in the same session; it blocks only where branch protection exists.
- **AUTHORITATIVE REFERENCE** pattern: when a doc marks a file `> **AUTHORITATIVE REFERENCE:** path`,
  read that file before implementing the feature.
- Document production: run the document-production skill before generating any Word/Excel/PDF/PPTX
  document, report, or deck; its values are in `docs/standards/document_production_standard_v1.0.md`
  and the raw brand assets (logos, palette, typeface) in `resources/branding/`.

---

## Governance map

The law loads on demand: this is a pointer list, not a file tree.

| File | Holds |
|------|-------|
| `CONSTITUTION.md` | Compliance law: banned features, mandatory patterns, security model, automation scope |
| `.claude/settings.json` | Claude Code permissions, checked in so the team shares one allow-list; context, not enforcement |
| `.codex/config.toml` | User-reviewed `untrusted` approval defaults; no forced sandbox mode |
| `scripts/` + `.pre-commit-config.yaml` | Portable mechanical gates; execution identity runs first |
| `docs/governance/gate_suite_runbook.md` | One section per hook, in run order: stage, what it blocks, why, how to run it alone. `scripts/gate_runbook_scan.py` keeps it in step with the config |
| `scripts/commit_attribution_scan.py` | `commit-msg` gate: blocks AI attribution trailers in commit messages |
| `scripts/kb_frontmatter_scan.py` | Validates KB frontmatter YAML; cross-checks that the freshness gate reads it alike |
| `scripts/new_project.py` | Initializes a project from this template and stamps `.template-version`, the mark of a project. Fills the decision log's header and leaves it with the `[EXAMPLE]` entry alone |
| `scripts/template_update.py` | Takes a derived project to a newer release: a keyed merge for the knowledge index, three-way for the rest, `sprint/` never written |
| `scripts/story_branch.py` | The team's workflow: `start <ID>` and `finish <ID>`; the `branch-policy` and `branch-push` hooks that keep code off a protected branch and the shared records off a story branch |
| `scripts/issue_log.py` | The issue log's one writer (`--file`, `--update`) and its gate: each entry in the template's form, its status borne out by the stories it names; `--report` |
| `scripts/session_closeout.py` | Session gate: handoff/kickoff pairs by session number, rotation to `archive/`, persona references, tracker reconciliation, dependency order, no live placeholders in a project |
| `.claude/rules/` | Judgement scoped by `paths:`: Claude Code loads a rule when it reads or edits a matching file; another agent reads the rules whose `paths:` match what it edits |
| `personas/` | The persona library the template ships, one agent file each, inactive; it grows by template release |
| `.claude/agents/` | The project's roster: the personas it activated from the library or drafted itself, each a live agent. A kickoff names one by slug and the `SessionStart` hook injects its prompt |
| `.claude/skills/` | The procedures, one `SKILL.md` each (below). `scripts/skill_scan.py` keeps every hook id, stage and command a skill names in step with the config |
| `docs/standards/` | The law the procedures obey: `session_handoff`, `sprint_management`, `secrets_management`, `document_production`, `coding`, `team`, `writing` |
| `sprint/` | Live state: sprint-status, story-tracker, decision-log, issue-log, handoffs, recovery |
| `docs/orchestration/knowledge/` | Accumulated learnings (single source of truth for knowledge) |


---

## Procedures are skills

Each procedure has one home, its `SKILL.md`, committed here and read **identically by any agent**:
Claude Code runs one by name (`/closeout`), or on its own when a task matches its description unless
the skill is the operator's alone; any other agent opens the file below and follows its body, the
frontmatter being Claude Code's settings for it. A standard keeps the law the procedure obeys and
points to its skill. Never copy a skill into another tool's folder (`.agents/skills/`): a copy is a
second home that drifts.

| Skill | When |
|-------|------|
| `.claude/skills/closeout/SKILL.md` | Session end. Forked: it sees the tree and its arguments, not this conversation |
| `.claude/skills/doc-drain/SKILL.md` | A story queued for the technical writer (`Queued: S<N>`), one document per run, when the cold start lists it. Forked in the writer's role; leaves its change for review |
| `.claude/skills/project-launch/SKILL.md` | A project's first session, and whenever a stage needs revisiting: intake, team, PRD, architecture and planning, each the Chair's to pause, skip or return to; the operator's alone |
| `.claude/skills/story/SKILL.md` | One story end to end through the team's roles, each handing off through a gated, committed artifact in `docs/stories/<ID>/`; stops for the Chair at each trigger and finding. In the main session; the Chair's alone |
| `.claude/skills/team-selection/SKILL.md` | A project's first session, and whenever the work needs a persona the roster lacks |
| `.claude/skills/planning-session/SKILL.md` | Building or re-planning the sprint from an approved PRD and architecture |
| `.claude/skills/issue/SKILL.md` | Something reported wrong, wanted or at risk, a deferred finding, a story that resolves an issue, or a question of where the issues stand: filed or changed through the issue log's writer |
| `.claude/skills/humanize/SKILL.md` | Text already in the tree the writing gate refuses: the certain fixes by script, the editor's proposals, the Chair's review of each file before it is kept; `voice <name>` makes a custom voice. In the main session |
| `.claude/skills/document-production/SKILL.md` | Before any Word, Excel, PDF or PowerPoint deliverable |

