# Agentic Development Project Template

A GitHub template for software projects built with AI coding agents. It gives an agent one
canonical brain to read, a constitution to obey, file-based state that survives between sessions,
and a suite of pre-commit gates that refuse a commit when a rule is broken. Every rule that matters
is a script with a self-test; prose describes the controls, it never stands in for them. Claude
Code and Codex work it interchangeably.

This page is the operator's: the walkthrough from a new repository to a running project, then a
catalog of every command, script, hook and gate. Detail it links to lives in
[TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md); the agent's own instructions are in [AGENTS.md](AGENTS.md).

## Walkthrough

### 1. Create the repository

```bash
gh repo create <owner>/<name> --template SaltyBrett/agentic-dev-template --private --clone
cd <name>
```

The repository is **private**: the template is public, the projects made from it are not. It holds
one commit, "Initial commit", and GitHub runs the `gates` workflow on it before you have run
anything; that run is green. If you separate GitHub identities by ssh host alias, point the remote
at yours before the first push ([reference_derived_project_start](docs/orchestration/knowledge/reference_derived_project_start.md)).

### 2. Initialize it

```bash
python3 scripts/new_project.py --name "<Project>" --platform "<stack>" --scope "<one line>" \
    --prefix <ABC> --profile commercial
python3 scripts/new_project.py --name "<Project>" --platform "<stack>" --scope "<one line>" \
    --prefix <ABC> --profile commercial --apply
```

The first prints the plan and writes nothing. The second fills the tokens, regenerates the sprint
state, strips the documents to the profile (`commercial`, or `gcc` for Government-cloud
constraints), writes the version stamp, and runs the whole suite, ending
`PASSED: project initialized and every gate is green.` It refuses to run in the template itself,
and refuses a public repository unless you pass `--public`. What it does, refuses and leaves to
you: [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md#the-initializer).

### 3. Install the hooks

```bash
python3 -m pip install pre-commit    # or: brew install pre-commit
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

Two lines report each hook installed under `.git/hooks/`. Both flags matter: plain
`pre-commit install` leaves the commit-message gate inert. `python3 -m pip`, because macOS ships
neither a bare `python` nor a bare `pip`.

### 4. Commit the birth

```bash
git add -A
git commit -m "checkpoint: initialized from the template"
git push
gh run list --limit 1
```

Every hook runs on the commit and passes, and the push's `gates` run is green. A message carrying
an AI attribution trailer is refused by the commit-message gate.

### 5. Open Claude Code

Run `claude` in the clone, or open the folder in the VS Code extension. Claude Code asks whether you
trust the folder: accept, because the project's hooks run only in a trusted folder. Its
`SessionStart` hook then runs the cold start and gives Claude the report: the identity gate, the
pull, `session-verify` (which passes at S1 with no handoff), the doc queue, and the S1 entry, whose
one next step is `/project-launch`.

### 6. Launch the project

Type `/project-launch`. It runs five stages in order, and each opens by saying what it produces,
who leads it and how to steer it:

1. **Intake**: three questions (purpose, the expertise needed, what it should accomplish), whose
   answers start the PRD draft in `docs/prd/prd.md`.
2. **Team**: the team-selection skill activates the personas the project needs into
   `.claude/agents/`, the product manager, solution architect and delivery manager among them, and
   you name the lead.
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
conversation is still S1, and there is nothing to close out: end the conversation to take a break
between stages ([reference_project_launch](docs/orchestration/knowledge/reference_project_launch.md)).

### 7. Close out the session

Once the launch has planned the first epic, say "close out the session", or type
`/closeout <persona> <brief>`: the slug of the persona that leads the next session, then what it
should do. A closeout before then is refused, since the next kickoff's tasks must cite stories. The session first commits what it learned and
decided; the closeout then writes the next session's handoff and kickoff, runs the closeout gate,
commits, pushes, watches the `gates` run, and returns the kickoff's text.

### 8. The session loop

Start the next session in a fresh conversation, or with `/clear`, and paste the kickoff. The start
hook runs the cold start again, now with the kickoff's persona, and the session works its tasks,
committing a `checkpoint:` after each unit. When the conversation's context runs high, tell Claude
"Context is at <N>%", and it closes out at the end of the current unit. Each session ends as step 7
does.

### 9. Take a newer template release

```bash
git fetch --no-tags git@github.com:SaltyBrett/agentic-dev-template.git \
    +refs/tags/<version>:refs/template/<version>
git show refs/template/<version>:scripts/template_update.py > scripts/template_update.py
python3 scripts/template_update.py --source git@github.com:SaltyBrett/agentic-dev-template.git --to <version>
```

The last command is a dry run naming what it would do to each path; add `--apply` to write, then
commit the result as one checkpoint and confirm the push's `gates` run. How each path is treated,
and what to do with a conflict: [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md#taking-a-newer-template-release).

## Catalog

### Commands

Each command is a skill: in Claude Code you type it; another agent opens the file and follows it.

| Command | Skill | What it does | When |
|---------|-------|--------------|------|
| `/project-launch` | `.claude/skills/project-launch/SKILL.md` | Intake, team, PRD, architecture and planning, each stage yours to pause, skip or return to; `status`, `pause`, `skip <stage>`, `<stage>` | A project's first session, and whenever a stage needs revisiting. Yours alone: Claude never starts it |
| `/closeout <persona> <brief>` | `.claude/skills/closeout/SKILL.md` | Writes the next session's handoff and kickoff, runs the closeout gate, commits, pushes, watches CI, returns the kickoff | Session end, or when context runs high |
| `/team-selection` | `.claude/skills/team-selection/SKILL.md` | Builds or extends the persona roster from the library, with presets and opt-in connections | Run by `/project-launch`; again when the work needs a specialization the roster lacks |
| `/planning-session` | `.claude/skills/planning-session/SKILL.md` | Turns the approved PRD and architecture into layers, epics and stories | Run by `/project-launch`; again to re-plan |
| `/doc-drain <path>` | `.claude/skills/doc-drain/SKILL.md` | Makes every change queued for the technical writer to one document in one pass, and leaves it for review | When the cold start lists a queued story |
| `/document-production` | `.claude/skills/document-production/SKILL.md` | Produces a Word, Excel, PDF or PowerPoint deliverable in the house style | Before any such deliverable |
| `/release` | `.claude/skills/release/SKILL.md` | Cuts a template release | The template only; the operator's alone |
| `/pristine-cut` | `.claude/skills/pristine-cut/SKILL.md` | Returns the template to its pristine state and cuts it | The template only; the operator's alone |

### Operator scripts

| Script | Command | What it does |
|--------|---------|--------------|
| `scripts/new_project.py` | `python3 scripts/new_project.py --name … --profile … [--apply]` | Initializes a project from the template (walkthrough step 2) |
| `scripts/template_update.py` | `python3 scripts/template_update.py --source <url> --to <version> [--apply]` | Takes a project to a newer release (walkthrough step 9) |
| `scripts/birth_probe.py` | `python3 scripts/birth_probe.py [--rev <revision>] [--profile <profile>]` | Births a scratch project from a committed revision through its initializer; CI runs it once per profile in the template |
| `scripts/doc_authority_scan.py` | `python3 scripts/doc_authority_scan.py --stamp` (`--list`, `--history <doc>`) | Writes each committed `pending` version-log row's commit; lists the authorities; shows each row's derived commit |
| `scripts/session_closeout.py` | `python3 scripts/session_closeout.py --scaffold --persona <slug>` | Writes the next handoff and kickoff skeletons; the closeout skill runs it |
| `scripts/md_to_docx.py` | `python3 scripts/md_to_docx.py <input.md> <output.docx>` | Converts markdown to Word; needs `python-docx` |
| `scripts/sanitize_template.py` | `python3 scripts/sanitize_template.py --apply` | The template only: the pristine-cut skill runs it |

### Session hooks

Registered in `.claude/settings.json`; they give Claude context and ask once, and the git hooks and
CI are the enforcement.

| Event | Script | What it does for you |
|-------|--------|----------------------|
| `SessionStart` (startup, `/clear`) | `scripts/session_start.py` | Runs the cold start's gates and gives Claude the report, the persona, the kickoff and the newest sprint-status entry |
| `SessionStart` (compact) | `scripts/session_start.py` | After compaction, gives back the working notes, the persona, the kickoff, the uncommitted paths and the journal's tail; runs no gate |
| `Stop` | `scripts/session_stop.py` | Sends Claude back once when a turn would end with work unbanked: sprint state modified, or working notes older than the change |
| `PostToolUse`, `PostToolUseFailure` | `scripts/session_journal.py` | Writes one journal line per edit and command, with its exit code, so an interrupted session can be reconstructed |

### Gates

Every gate is a pre-commit hook, described once, in run order, with its stage, what it blocks and
how to run it alone: [gate_suite_runbook.md](docs/governance/gate_suite_runbook.md). A gate keeps
that page in step with the config, and the same suite runs on GitHub on every push and pull request
([reference_ci_backstop](docs/orchestration/knowledge/reference_ci_backstop.md)).

```bash
pre-commit run --all-files                    # every pre-commit-stage gate
pre-commit run banned-feature-scan --all-files  # one gate
printf 'checkpoint: x\n\nClean body.\n' > /tmp/msg  # the commit-msg gate needs a message file
pre-commit run --hook-stage commit-msg --commit-msg-filename /tmp/msg --all-files
```

Invoke a gate through `pre-commit`, which provisions its interpreter; a bare `python` does not exist
on macOS ([reference_precommit_interpreter](docs/orchestration/knowledge/reference_precommit_interpreter.md)).
Three gates (the persona linter, the frontmatter gate and the attribution gate) are also published
in `.pre-commit-hooks.yaml`, for another repository to pin by `rev`:

```yaml
  - repo: https://github.com/SaltyBrett/agentic-dev-template
    rev: v1.0.0
    hooks:
      - id: persona-lint
      - id: kb-frontmatter-scan
      - id: commit-attribution
```

## Where things live

- **The law:** [AGENTS.md](AGENTS.md) is the agent's brain and cold-start sequence, read natively by
  Claude Code (v2.1.277 or later) and Codex; [CONSTITUTION.md](CONSTITUTION.md) is the compliance
  law; every framework decision, with its reasoning, is in
  [framework_decisions.md](docs/governance/framework_decisions.md).
- **The state:** `sprint/` holds sprint status, the story tracker, the decision log and the
  session handoffs; `docs/orchestration/knowledge/` is the knowledge base, the one place durable
  learnings go.
- **The license:** [MIT](LICENSE). A project keeps it or replaces it with its own.

## Repository structure

This table is the one home for what each path holds; `docs/README.md` and `TEMPLATE_GUIDE.md` link here.

| Path | Description |
|------|-------------|
| `AGENTS.md` | Canonical agent brain and cold start; Claude Code and Codex read it natively |
| `CONSTITUTION.md` | AI agent governance rules and session protocols |
| `LICENSE` | MIT; the project's own from birth |
| `sprint/` | Active project state (sprint-status, story-tracker, decision-log, handoffs, recovery) |
| `docs/orchestration/knowledge/` | Knowledge base (single source of truth for accumulated learnings) |
| `personas/` | The persona library: every persona the template ships, as Claude Code agent files, inactive until a project activates it |
| `.claude/agents/` | The project's roster: the personas it activated or drafted, each a live agent; every kickoff prompt names one |
| `.claude/skills/` | The procedures, one `SKILL.md` each, readable by any agent; `AGENTS.md` and the catalog above list them |
| `docs/standards/` | Implementation standards: the law the procedures obey |
| `docs/governance/` | Document control, the gate-suite runbook, the framework's own decision log, compliance policies |
| `docs/templates/` | The PRD and architecture templates, each the authority for its document's shape; a project makes its own documents from them |
| `docs/prd/` | Product requirements document(s) |
| `docs/architecture/` | Architecture specs, diagrams, ADRs |
| `docs/executive/` | Executive summaries, stakeholder presentations |
| `docs/research/` | Spike results, POC findings, analysis |
| `docs/testing/` | Test plans, test cases, validation specs |
| `docs/runbooks/` | Operational procedures for IT/ops teams |
| `evidence/` | Timestamped validation evidence for audit trails |
| `infra/` | Infrastructure-as-code (Bicep, Terraform, ARM templates) |
| `resources/` | External reference docs, data dictionaries, vendor specs; `branding/` holds the project's brand assets |
| `scripts/` | Automation scripts, compliance gates, utilities |

## Key standards

| Standard | Purpose |
|----------|---------|
| [Sprint Management](docs/standards/sprint_management_standard_v1.0.md) | Planning-session setup + sprint-doc maintenance |
| [Document Production](docs/standards/document_production_standard_v1.0.md) | Brand + formatting standard for Word/Excel/PDF/PPTX deliverables |
| [Session Handoff](docs/standards/session_handoff_standard_v2.0.md) | Zero-drift session continuity |
| [Secrets Management](docs/standards/secrets_management_standard_v1.0.md) | Key Vault + SPN auth |
| [Document Control](docs/governance/doc_control_standard.md) | GitHub-governed changes |
