# Agentic Development Project Template

A GitHub template for software projects built with AI coding agents. It gives an agent one
canonical brain to read, a constitution to obey, file-based state that survives between sessions,
and a suite of pre-commit gates that refuse a commit when a rule is broken. Every rule that matters
is a script with a self-test; prose describes the controls, it never stands in for them. Claude
Code and Codex work it interchangeably.

## Start a project

Two commands. The repository is created **private**; the template is public, the projects made
from it are not.

```bash
gh repo create <owner>/<name> --template SaltyBrett/agentic-dev-template --private --clone
cd <name>
python3 scripts/new_project.py --name "<Project>" --platform "<stack>" --scope "<one line>" \
    --prefix <ABC> --profile commercial --apply
```

The initializer fills the tokens, regenerates the sprint state, strips the documents to the chosen
profile (`commercial`, or `gcc` for Government-cloud constraints), writes the version stamp, and
runs the whole gate suite so the project starts green. Run it without `--apply` first to see the
plan. It refuses to run in the template itself, and it refuses a **public** project unless you pass
`--public`: private is the default, and the first command every project runs is where that is
checked. Then install the hooks once per clone:

```bash
python3 -m pip install pre-commit    # or: brew install pre-commit
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

Both flags matter; plain `pre-commit install` leaves the commit-message gate inert. `python3 -m pip`
rather than `pip`, because macOS ships neither a bare `python` nor a bare `pip`. The full
procedure, including taking a newer template release later, is [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md).

## Where things live

- **The law:** [AGENTS.md](AGENTS.md) is the agent's brain and cold-start sequence;
  [CONSTITUTION.md](CONSTITUTION.md) is the compliance law; every framework decision, with its
  reasoning, is in [framework_decisions.md](docs/governance/framework_decisions.md).
- **The gates:** one section per hook, in run order, with its stage, what it blocks and how to run
  it alone: [gate_suite_runbook.md](docs/governance/gate_suite_runbook.md). A gate keeps that page
  in step with the config.
- **The state:** `sprint/` holds sprint status, the story tracker, the decision log and the
  session handoffs; `docs/orchestration/knowledge/` is the knowledge base, the one place durable
  learnings go.
- **The license:** [MIT](LICENSE). A project keeps it or replaces it with its own.

## What the template provides

- **Agent governance** — a constitution, session protocols, and a gated session closeout that
  produce the next session's handoff and kickoff prompt, verified by a script
- **State management** — sprint status, story tracker and decision log as markdown, read
  index-first, with the tracker's statistics and dependency order reconciled on every commit
- **Compliance gates** — execution identity, content rules, knowledge freshness, session
  closeout, template versioning, secrets, commit attribution, and the GCC banned-feature scan
  under the `gcc` profile
- **Secrets management** — an Azure Key Vault and service-principal standard
- **Document control** — GitHub-governed change management with evidence trails
- **Recovery framework** — a drift-proof control plane for reconciliation work

## Repository structure

This table is the one home for what each path holds; `docs/README.md` and `TEMPLATE_GUIDE.md` link here.

| Path | Description |
|------|-------------|
| `AGENTS.md` | Canonical agent brain — Codex-native; Claude loads it via `CLAUDE.md`'s `@AGENTS.md` import |
| `CLAUDE.md` | Claude Code bridge (`@AGENTS.md` + Claude-only accelerators) |
| `AGENT_INTEROP.md` | Tool-interoperability contract (single-source-of-truth law) |
| `CONSTITUTION.md` | AI agent governance rules and session protocols |
| `LICENSE` | MIT; the project's own from birth |
| `sprint/` | Active project state (sprint-status, story-tracker, decision-log, handoffs, recovery) |
| `docs/orchestration/knowledge/` | Knowledge base (single source of truth for accumulated learnings) |
| `docs/personas/` | Persona registry; every kickoff prompt names one |
| `docs/standards/` | Implementation standards that govern how artifacts are built |
| `docs/governance/` | Document control, the gate-suite runbook, the framework's own decision log, compliance policies |
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

## How an agent works a session

This repository is **tool-agnostic**: Claude Code, Codex, or any future agent works it interchangeably.
`AGENTS.md` (repo root) is the one canonical brain — Codex reads it natively, and `CLAUDE.md` loads it
via an `@AGENTS.md` import. AI agents follow a structured protocol:

1. Read `AGENTS.md` (canonical brain) + `AGENT_INTEROP.md` at session start
2. Read `docs/orchestration/knowledge/INDEX.md` (index first, then task-relevant entries)
3. Read `CONSTITUTION.md`, `sprint/sprint-status.md`, `sprint/story-tracker.md` for current state
4. Run `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md` before any build work
5. Flush durable learnings to `docs/orchestration/knowledge/` and update state files at session end
6. Close out with `session_closeout.py`: a handoff and a kickoff prompt for the next session, verified
   by a gate, living one session, then archived

See `AGENTS.md` for the complete cold-start sequence.

## Running the gates

```bash
# Run every pre-commit-stage check
pre-commit run --all-files

# Run one gate only
pre-commit run banned-feature-scan --all-files

# The commit-msg-stage gate is NOT covered by --all-files; test it explicitly
printf 'checkpoint: x\n\nClean body.\n' > /tmp/msg
pre-commit run --hook-stage commit-msg --commit-msg-filename /tmp/msg --all-files

# Session boundaries: manual-stage hooks the agent runs at cold start and at session end
pre-commit run session-verify --hook-stage manual
pre-commit run session-closeout --hook-stage manual --all-files
```

Three of the gates (the persona linter, the frontmatter gate and the attribution gate) are also
published as a pre-commit hook repository in `.pre-commit-hooks.yaml`, so another repository pins
them by `rev` instead of copying a script:

```yaml
  - repo: https://github.com/SaltyBrett/agentic-dev-template
    rev: v1.0.0
    hooks:
      - id: persona-lint
      - id: kb-frontmatter-scan
      - id: commit-attribution
```

Invoke the gates through `pre-commit`, which provisions its own interpreter. Invoking a gate script
with a bare `python` does not work on macOS, which ships no unversioned `python` on PATH — and the
banned-feature scan blocks that spelling repo-wide. See
[reference_precommit_interpreter](docs/orchestration/knowledge/reference_precommit_interpreter.md).

## Key standards

| Standard | Purpose |
|----------|---------|
| [Sprint Management](docs/standards/sprint_management_standard_v1.0.md) | Planning-session setup + sprint-doc maintenance |
| [Document Production](docs/standards/document_production_standard_v1.0.md) | Brand + formatting standard for Word/Excel/PDF/PPTX deliverables |
| [Session Handoff](docs/standards/session_handoff_standard_v2.0.md) | Zero-drift session continuity |
| [Secrets Management](docs/standards/secrets_management_standard_v1.0.md) | Key Vault + SPN auth |
| [Document Control](docs/governance/doc_control_standard.md) | GitHub-governed changes |
