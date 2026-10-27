# Template Guide

The manual every project made from the template carries beside its own `README.md`: how the
project is built. The walkthrough starts at step 4, the first commit; steps 1 to 3, which create the
repository, install the hooks and initialize the project, are on the template's front page on
GitHub.

---

## Walkthrough

### 4. Commit the birth

The project's birth is what the initializer wrote; commit it as the project's first commit of its own:

```bash
git add -A
git commit -m "checkpoint: initialized from the template"
git push
gh run list --limit 1
```

Every hook runs on the commit and passes, and the push's `gates` run is green. A message carrying
an AI attribution trailer is refused by the commit-message gate. If you separate GitHub identities
by ssh host alias, point the remote at yours before this first push.

### 5. Open Claude Code

Run `claude` in the clone, or open the folder in the VS Code extension. Claude Code asks whether you
trust the folder: accept, because the project's session hooks run only in a trusted folder. The
`SessionStart` hook then runs the cold start (the checks `AGENTS.md` lists for the start of every
session) and gives Claude the report: the execution-identity gate (it refuses a session run under a
sandbox account or identity), `git pull`, `session-verify` (the check that the previous session
closed out), the queue of document changes waiting for the technical writer, and the newest entry
of `sprint/sprint-status.md`. Sessions are numbered S1, S2 and on, each recorded by an entry there.
This first one is S1; with no session before it, `session-verify` passes. The S1 entry's one next
step is `/project-launch`.

### 6. Launch the project

Type `/project-launch`. The skills that need your decisions call you the Chair: the person who
answers their questions, approves each document and decides what comes next. The launch runs five stages in order, and each
opens by saying what it produces, who leads it and how to steer it:

1. **Intake**: three questions (purpose, the expertise needed, what it should accomplish), whose
   answers start the PRD draft in `docs/prd/prd.md`.
2. **Team**: the team-selection skill activates the personas the project needs, each an agent
   role with its own prompt, from the library in `personas/` into the project's roster,
   `.claude/agents/`: the product manager, solution architect and delivery manager among them. You
   name the lead, the persona that runs the project's sessions.
3. **PRD**: the product manager interviews you until every section is written or names an open
   question, then you approve it.
4. **Architecture**: the solution architect does the same from the approved PRD.
5. **Planning**: the delivery manager runs the planning-session skill, which writes the first epic
   and its stories. `doc-authority-scan` refuses that commit unless the PRD and the architecture are
   approved or their skips logged.

At any point: `/project-launch status` shows where each stage stands, `/project-launch pause` saves
the draft and stops, `/project-launch skip <stage>` passes over a stage with your reason logged as a
decision, and `/project-launch <stage>` returns to one, to resume, review or revise it. A bare
`/project-launch` resumes where the launch stopped. The state is the documents themselves, so a
stage left in one conversation is picked up in the next. Until planning writes the first epic, a new
conversation is still S1, and there is nothing to close out: type `/clear`, or end the
conversation, to take a break between stages.

Do not fill the tracker by hand. The planning-session skill writes the epics, stories,
dependencies, Required Standards (the standards an agent reads before it builds each story) and PRD
references in one repeatable shape, under
`docs/standards/sprint_management_standard_v1.0.md`. How the PRD and the architecture are made from
their templates and approved: `docs/templates/README.md`.

### 7. Close out the session

A closeout ends a session. It writes the next session's handoff (what this session did and left
open) and kickoff (the prompt you paste to start the next session), then runs the closeout gate,
commits, pushes, watches the `gates` run and returns the kickoff's text. Once planning is done, the
launch closes out S1 itself, with the lead you named. It first removes the S1 entry's `### Next`
section, which the closeout gate refuses while it remains.

From S2 on, say "close out the session", or type `/closeout <persona> <brief>`: the slug of the
persona that leads the next session, then what it should do. When you say it, the session first
commits what it learned and decided. When you type the command, the closeout starts at once, so let
the session commit first. A
closeout before the first epic exists is refused, since the next kickoff's tasks must cite stories.

A session that must stop at once commits an emergency checkpoint instead: a minimal entry headed
`emergency checkpoint` (`AGENTS.md`, How I work). The next session completes the closeout before it
builds, and the gate refuses to close an entry still so headed.

### 8. The session loop

Start the next session in a fresh conversation, or with `/clear`, and paste the kickoff. The start
hook runs the cold start again, now with the kickoff's persona, and the session works its tasks,
committing a `checkpoint:` after each unit. When the conversation's context runs high, tell Claude
"Context is at <N>%", and it closes out at the end of the current unit. Each session ends as step 7
does.

The session stays on `main`, which takes only the shared records: the tracker, sprint-status, the
logs, the knowledge base and the planning documents. Each story is built on its own branch, in its
own working directory, and several can run at once, one agent to each:

```bash
python3 scripts/story_branch.py start ACME-2.3    # sets it In Progress on main; makes story/ACME-2.3 in .worktrees/ACME-2.3
python3 scripts/story_branch.py finish ACME-2.3   # merges main in, runs the suite, opens the pull request,
                                                  # waits for CI, squash-merges it, sets the story Done on main
```

The issues that name the story move with it: `start` sets them In Progress, and `finish ACME-2.3
--resolution "<what changed>"` sets each issue the story completes to Resolved. `finish` refuses to
begin while a resolution is due and not given, or while `main` holds commits not yet pushed, and
names the command that clears each.

`/story <ID>` runs both for you. The `branch-policy` and `branch-push` hooks refuse code committed or
pushed to `main` and a shared record committed on a story branch; CI turns red on a push to `main`
that did not come through a merged pull request.

### 9. Take a newer template release

An update is built on its own branch, `update/<version>`, and reaches `main` by a pull request, as
a story does; `main` refuses an update committed to it directly.

```bash
git switch -c update/<version>
git fetch --no-tags git@github.com:<template-owner>/agentic-dev-template.git \
    +refs/tags/<version>:refs/template/<version>
git show refs/template/<version>:scripts/template_update.py > scripts/template_update.py
python3 scripts/template_update.py --source git@github.com:<template-owner>/agentic-dev-template.git --to <version>
```

The last command is a dry run naming what it would do to each path; add `--apply` to write. Then
commit on the branch, push it, and merge its pull request once the checks are green:

```bash
git add -A
git commit -m "checkpoint: template <version>"
git push -u origin update/<version>
gh pr create --base main --head update/<version> --fill
gh pr checks update/<version> --watch
gh pr merge update/<version> --squash
git switch main && git pull --ff-only
```

How each path is treated, and what to do with a conflict:
[Taking a newer template release](#taking-a-newer-template-release).

---

## Catalog

### Commands

Each command is a skill: in Claude Code you type it; another agent opens the file and follows it.

| Command | Skill | What it does | When |
|---------|-------|--------------|------|
| `/project-launch` | `.claude/skills/project-launch/SKILL.md` | Intake, team, PRD, architecture and planning, each stage yours to pause, skip or return to; `status`, `pause`, `skip <stage>`, `<stage>` | A project's first session, and whenever a stage needs revisiting. Yours alone: Claude never starts it |
| `/story <ID>` | `.claude/skills/story/SKILL.md` | Runs one story from brief to release through the team's roles, each stage's artifact gated and committed in `docs/stories/<ID>/`; asks you at each review trigger and each review or security finding; `<ID> status` | A planned story, once its dependencies are done. Yours alone: Claude never starts it |
| `/closeout <persona> <brief>` | `.claude/skills/closeout/SKILL.md` | Writes the next session's handoff and kickoff, runs the closeout gate, commits, pushes, watches CI, returns the kickoff | Session end, or when context runs high |
| `/team-selection` | `.claude/skills/team-selection/SKILL.md` | Builds or extends the persona roster from the library, with presets (named teams to start from) and opt-in connections to outside tools, such as Blender | Run by `/project-launch`; again when the work needs a specialization the roster lacks |
| `/planning-session` | `.claude/skills/planning-session/SKILL.md` | Turns the approved PRD and architecture into layers, epics and stories | Run by `/project-launch`; again to re-plan |
| `/doc-drain <path>` | `.claude/skills/doc-drain/SKILL.md` | Makes every change queued for the technical writer to one document in one pass, and leaves it for review | When the cold start lists a queued story |
| `/humanize <path>` | `.claude/skills/humanize/SKILL.md` | Fixes what the writing gate flags in files already in the tree: the certain fixes by script, the rest rewritten by the editor as proposals you keep, trim or reject for each file; `voice <name>` makes your own voice from a sample of your writing | A sweep of existing documents, or files you name |
| `/issue <what was found>` | `.claude/skills/issue/SKILL.md` | Files a bug, a request or a risk in `sprint/issue-log.md`, changes one as its stories move, or reports where they stand; `<ID>`, `report` | When anyone, you or an agent, finds something wrong, wanted or at risk |
| `/document-production` | `.claude/skills/document-production/SKILL.md` | Produces a Word, Excel, PDF or PowerPoint deliverable in the house style | Before any such deliverable |


### Operator scripts

| Script | Command | What it does |
|--------|---------|--------------|
| `scripts/new_project.py` | `python3 scripts/new_project.py --name ... [--apply]` | Initializes a project from the template (walkthrough step 3, on the template's front page) |
| `scripts/template_update.py` | `python3 scripts/template_update.py --source <url> --to <version> [--apply]` | Takes a project to a newer release (walkthrough step 9) |
| `scripts/story_branch.py` | `python3 scripts/story_branch.py start <ID>` (`finish <ID>`) | Starts a story on its own branch and worktree; finishes it by a squashed pull request once CI is green |
| `scripts/issue_log.py` | `python3 scripts/issue_log.py --file` (`--update <ID>`, `--report`) | Files an issue, asking in the terminal for each field not given; changes one; reports them |
| `scripts/doc_authority_scan.py` | `python3 scripts/doc_authority_scan.py --stamp` (`--list`, `--history <doc>`) | `--stamp` writes the commit into each committed `pending` row of a document's version log; `--list` lists the authorities, the documents that are each the source of truth for a scope and keep a version log; `--history` shows the commit of each row of one document's log |
| `scripts/session_closeout.py` | `python3 scripts/session_closeout.py --scaffold --persona <slug>` | Writes the next handoff and kickoff skeletons; the closeout skill runs it |
| `scripts/md_to_docx.py` | `python3 scripts/md_to_docx.py <input.md> <output.docx>` | Converts markdown to Word; needs `python-docx` |


### Session hooks

Registered in `.claude/settings.json`. Most give Claude context and ask once, and the git hooks and
CI are the enforcement. The subagent ceiling refuses outright, because a spawn leaves nothing in git
for those to judge.

| Event | Script | What it does for you |
|-------|--------|----------------------|
| `PreToolUse` (`Agent`, `Skill`), `SessionStart`, `PostModelSwitch` | `scripts/subagent_ceiling.py` | Refuses a subagent or a skill that would run above the model and effort you chose for the session, under the mode you set |
| `SessionStart` (startup, `/clear`) | `scripts/session_start.py` | Runs the cold start's gates and gives Claude the report, the persona, the kickoff and the newest sprint-status entry |
| `SessionStart` (compact) | `scripts/session_start.py` | After compaction, gives back the working notes, the persona, the kickoff, the uncommitted paths and the journal's tail; runs no gate |
| `Stop` | `scripts/session_stop.py` | Sends Claude back once when a turn would end with work unrecorded: a sprint document changed and uncommitted, or the working notes (`sprint/recovery/WORKING_NOTES.md`, the agent's record of uncommitted work) older than the newest uncommitted change |
| `PostToolUse`, `PostToolUseFailure` | `scripts/session_journal.py` | Writes one journal line per edit and command, with its exit code, so an interrupted session can be reconstructed |

You set the session's model and effort (`/model`, `/effort`). The mode decides how far below them
Claude may run a subagent, and no mode lets it go above:

| Mode | Claude may change |
|------|-----------------------------|
| `max` | nothing: every subagent runs at the session's model and effort |
| `tuned` | the effort only, at or below the session's |
| `efficient` | the model and the effort, each at or below the session's (the default) |

The mode is `SUBAGENT_CHOICE` in the `env` block of `.claude/settings.json`; set it for one machine
in `.claude/settings.local.json`, which git ignores.

### Gates

Every gate is a pre-commit hook, described once, in run order, with its stage, what it blocks and
how to run it alone: [gate_suite_runbook.md](docs/governance/gate_suite_runbook.md). A gate keeps
that page in step with the config, and the same suite runs on GitHub on every push and pull request.

```bash
pre-commit run --all-files                    # every pre-commit-stage gate
pre-commit run banned-feature-scan --all-files  # one gate
printf 'checkpoint: x\n\nClean body.\n' > /tmp/msg  # the commit-msg gate needs a message file
pre-commit run --hook-stage commit-msg --commit-msg-filename /tmp/msg --all-files
```

Invoke a gate through `pre-commit`, which provisions its interpreter; a bare `python` does not exist
on macOS.

---

## Repository structure

This table is the one home for what each path holds; `docs/README.md` links here.

| Path | Description |
|------|-------------|
| `README.md` | The front page: the template's, until the initializer replaces it with the project's own |
| `TEMPLATE_GUIDE.md` | This guide, the framework's manual; required in a project |
| `AGENTS.md` | The agent's instructions and the cold start; Claude Code and Codex read it natively |
| `CONSTITUTION.md` | AI agent governance rules and session protocols |
| `LICENSE` | MIT; the project's own from birth, to keep or replace |
| `.pre-commit-config.yaml` | The gate suite's hooks, described in `docs/governance/gate_suite_runbook.md` |
| `writing-profile.yaml` | The voice and audience the writing gate judges each markdown file in |
| `.claude/settings.json` | Claude Code's shared permissions and the session hooks |
| `.claude/rules/` | Judgement for agents, each rule loaded when Claude Code reads or edits a file its `paths:` match |
| `.github/workflows/` | CI: the gate suite on every push and pull request |
| `.codex/` | Codex's approval defaults |
| `sprint/` | The project's state: sprint-status, the story tracker, the decision log, the issue log, the session handoffs and the recovery notes |
| `docs/orchestration/knowledge/` | The knowledge base, the one place durable learnings go |
| `personas/` | The persona library: every persona the template ships, as Claude Code agent files, inactive until a project activates it |
| `.claude/agents/` | The project's roster: the personas it activated or drafted, each a live agent; every kickoff prompt names one |
| `.claude/skills/` | The procedures, one `SKILL.md` each, readable by any agent; `AGENTS.md` and the catalog above list them |
| `docs/standards/` | Implementation standards: the law the procedures obey |
| `docs/governance/` | Document control and the gate-suite runbook |
| `docs/templates/` | The PRD and architecture templates, each the authority for its document's shape; a project makes its own documents from them |
| `docs/prd/` | Product requirements document(s) |
| `docs/architecture/` | Architecture specs, diagrams, ADRs |
| `docs/executive/` | Executive summaries, stakeholder presentations |
| `docs/research/` | Spike results, POC findings, analysis |
| `docs/testing/` | Test plans, test cases, validation specs |
| `docs/runbooks/` | Operational procedures for IT/ops teams |
| `evidence/` | Timestamped validation evidence for audit trails |
| `infra/` | Infrastructure as code, in the project's tool |
| `resources/` | External reference docs, data dictionaries, vendor specs; `branding/` holds the project's brand assets |
| `scripts/` | Automation scripts, compliance gates, utilities |


## Key standards

| Standard | Purpose |
|----------|---------|
| [Sprint Management](docs/standards/sprint_management_standard_v1.0.md) | Planning-session setup + sprint-doc maintenance |
| [Document Production](docs/standards/document_production_standard_v1.0.md) | Brand + formatting standard for Word/Excel/PDF/PPTX deliverables |
| [Session Handoff](docs/standards/session_handoff_standard_v2.0.md) | Zero-drift session continuity |
| [Secrets Management](docs/standards/secrets_management_standard_v1.0.md) | Security principals and one secrets store |
| [Coding](docs/standards/coding_standard_v1.0.md) | Limits on code a change adds or edits, held by each stack's profile |
| [Team](docs/standards/team_standard_v1.0.md) | How a story runs through its roles, their handoffs and the Chair's approvals |
| [Writing](docs/standards/writing_standard_v1.0.md) | The voices documents are written in and the rules their text obeys |
| [Document Control](docs/governance/doc_control_standard.md) | GitHub-governed changes |

---

## The initializer

`scripts/new_project.py` dry-runs by default and prints exactly what it would change; `--apply`
writes, then runs the full gate suite to prove the new project starts green. It fills the project's
tokens in `AGENTS.md`, `CONSTITUTION.md` and the decision log's header; regenerates
`sprint/sprint-status.md`, `sprint/story-tracker.md` and `sprint/issue-log.md`; writes the project's
own `README.md`, its name, platform and scope and a link to this guide; clears any handoff pair
and persona roster; and writes `.template-version`, the mark of a project.

It refuses to run when `origin` is the template repository itself, because that would make the
template a project.

It refuses before writing anything when pre-commit is not installed, since `--apply` ends by running the gate suite through pre-commit. The refusal prints the commands that install it.

It also refuses when the project's repository is **public** and `--public` was not given. The template is public; a project made from it is private by default, and neither GitHub's "Use this template" flow nor `gh repo create` can be told a default, so the initializer checks. The refusal prints the `gh repo edit ... --visibility private` command. When the visibility cannot be read (no `gh`, or a remote that is not GitHub) the run says so and continues.

`sprint/sprint-status.md` and `sprint/story-tracker.md` are regenerated, not filled, so the project starts at its own S1 with the example epic alone.

The `README.md` it writes is a production document, the project's front page for its users, and
the writing gate judges it so: it holds no development reference. The template's own README, the
page an adopter reads before a project exists, is replaced, and a template release never writes a
project's README again.

**What it leaves to the project.** `docs/orchestration/knowledge/` and `sprint/decision-log.md` are the project's: the initializer fills the log's header and nothing else, so your log starts with the `[EXAMPLE]` entry alone.


Still by hand, because they are judgement calls:
- `LICENSE`: the template's MIT license arrives with the project and is the project's from then on. Keep it, or replace it with your own; a template release never rewrites it
- `README.md`: grow it into the front page your users read once the project has an application to describe
- The `[EXAMPLE]` entries in `sprint/decision-log.md`, `sprint/story-tracker.md` and `sprint/issue-log.md` stay: each is numbered zero, the form its log's entries follow, and your first real entry is 1
- The deferred tokens the initializer reports, when the project first needs them (next section)

---

## Customizing the law

No script decides these for a project.

- **Banned features and mandatory patterns.** `CONSTITUTION.md` sections 3.2 and 4 impose none. Add
  the project's own there, and name the target environments in section 5.
- **The banned-feature scanner.** Open `scripts/banned_feature_scan.py` and review the pattern
  dict. `BANNED_PATTERNS` holds the features the project bans, none in the template; add each with
  its patterns. The same file
  holds a second dict, `CONTENT_RULES`, for rules that must also cover the governance docs listed in
  `EXCLUDE_FILES`: that list exempts files which legitimately *name* banned features, and it would
  silently neuter a rule aimed at the docs themselves. Content rules bypass it and carry a per-rule
  `allow` set plus a `fix` string shown with each violation. Put "this spelling is not portable"
  rules here; put "this feature is forbidden" rules in `BANNED_PATTERNS`.
- **The deferred tokens.** The initializer leaves the brand values and the secrets-store names
  unfilled and lists them: `docs/standards/secrets_management_standard_v1.0.md` holds
  `{{SECRETS_STORE}}` and `{{PRINCIPAL}}`, and `docs/standards/document_production_standard_v1.0.md`
  and `resources/README.md` the brand values. Fill them when the project first needs a secrets store
  or a document.

---

## The gate suite

`.pre-commit-config.yaml`, at the repository's root, wires the gates as git hooks that fire on every
commit and push, whichever agent or person makes it; they are the compliance gate `CONSTITUTION.md`
relies on. The runbook, `docs/governance/gate_suite_runbook.md`, also names the self-test each hook
pairs with. A hook you add to the config needs its runbook section in the same commit, since a gate
keeps the two in step.

**The freshness gate reads your knowledge entries.** Each entry in `docs/orchestration/knowledge/`
names the decisions it explains (`teaches:`) and the date it was last checked against them
(`verified:`). The gate fails an entry whose decision changed after that date, so an entry still
teaching a rule the log has since amended cannot pass as current.

It needs no configuration: decision IDs are read literally from the first column of your
`sprint/decision-log.md` index, so any convention works (`DEC-041`, `ACME-2026-07-30-001`, `ADR-7`).
Rows marked `[EXAMPLE]` are ignored. Stamp each knowledge entry, as
`.claude/rules/knowledge-entries.md` describes:

```yaml
teaches: [ACME-2026-07-30-001]     # decisions this entry EXPLAINS
verified: 2026-07-30          # when it was last confirmed against them
```


**Every hook type installs with plain `pre-commit install`** (walkthrough step 2): the config names
pre-commit, commit-msg and pre-push in `default_install_hook_types`. A hook type left uninstalled
never fires its gates while the config still reads as protected, so the session-start report names
any type a clone lacks. `pre-commit run --all-files` covers the pre-commit stage only; the runbook
gives the commands for the commit-msg, pre-push and manual stages.

---

## Taking a newer template release

`gh repo create --template` squashes history, so a derived project has no git relationship to the
template. `scripts/template_update.py` supplies one: it fetches the release you are on and the one
you want into `refs/template/<version>` (outside `refs/tags/`, apart from the project's own tags) and
carries the difference across. Run the **target release's** copy, because the ownership map lives in
the script, and a release that carries no updater is refused; walkthrough step 9 gives the commands.

It dry-runs by default. `--apply` writes, stamps `.template-version` last, then runs the full gate
suite. Run it on the update branch and merge that by pull request (walkthrough step 9).

What it does per path is decided by ownership:

| Class | Paths | Behaviour |
|---|---|---|
| keep | `sprint/` (the decision log included), the project's `README.md`, the content folders shipped empty, the persona roster `.claude/agents/` | never written; template changes there are named in one line |
| merge | `docs/orchestration/knowledge/INDEX.md` by slug | your rows never touched; a row the release adds, changes or drops is applied only where your copy still equals the previous release's; an edited row is reported and left |
| three-way | everything else, through `git merge-file` | an unedited copy takes the template's version; an edited copy takes the change where it does not overlap; an overlap is a conflict, left alone and named. `.gitignore` alone is merged with `--union`: where both sides changed one place, both sides' lines are kept, yours first, and the dry run names it `union` so you read it in `git diff` before the commit |

A conflict withholds the stamp. Commit what merged on the branch first, since `--apply` runs only on
a clean tree, then edit the file and re-run with `--keep <path>`, or take the template's copy with
`--take <path>`.


