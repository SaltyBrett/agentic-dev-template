# Template Guide: What the Initializer Leaves to You

The path from a new repository to a running project is the [README's walkthrough](README.md#walkthrough).
This guide holds the detail it links to: what `scripts/new_project.py` does and refuses, the
customizations no script makes for you, why the gates are installed the way they are, and how a
release is taken.

---

## The initializer

`scripts/new_project.py` dry-runs by default and prints exactly what it would change; `--apply`
writes, then runs the full gate suite to prove the new project starts green. It fills the project's
tokens in `AGENTS.md`, `CONSTITUTION.md` and the decision log's header, regenerates
`sprint/sprint-status.md` and `sprint/story-tracker.md`, clears the template's handoffs and its own
persona roster, strips every document to the chosen profile, and writes `.project-profile` and
`.template-version`.

It refuses to run when `origin` is the template repository itself, because that would clear the
template's own sprint state.

It also refuses when the project's repository is **public** and `--public` was not given. The template is public; a project made from it is private by default (decision 2026-09-25-001), and neither GitHub's "Use this template" flow nor `gh repo create` can be told a default, so the first command every project runs checks. The refusal prints the `gh repo edit … --visibility private` command. When the visibility cannot be read (no `gh`, or a remote that is not GitHub) the run says so and continues.

`sprint/sprint-status.md` and `sprint/story-tracker.md` are regenerated, not filled: both hold the template's own state (session updates, the `TMPL` epics), which a new project must not inherit. The S1 entry's one next step is `/project-launch`. The first derived project ([[reference_derived_project_start]]) records what else to expect on day one, including the `gates` run GitHub triggers on the "Initial commit" before you have run anything.

**What it will not touch, and why.** `docs/governance/framework_decisions.md` and `docs/orchestration/knowledge/` are preserved, and `sprint/decision-log.md` gets its header filled and nothing else. Clearing the decisions is the intuitive move and it breaks the first commit: every knowledge entry declares `teaches: [<decision-id>]`, and the freshness gate fails when an ID is in neither decision index. The framework decisions are the provenance for why each gate exists; your log starts with the `[EXAMPLE]` entry alone ([[reference_framework_decisions]]). A self-test fixture pins this.

Still by hand, because they are judgement calls:
- `LICENSE` — the template's MIT license arrives with the project and is the project's from then on: keep it, or replace it with your own; a template release never rewrites it (decision 2026-09-25-002)
- This file (`TEMPLATE_GUIDE.md`) — remove, or keep it as a reference
- `[EXAMPLE]` rows in `sprint/decision-log.md` and `sprint/story-tracker.md`: the planning session removes them with the first real epic, and the state gate refuses them after
- The deferred tokens the initializer reports, when the project first needs them (next section)

---

## Customizing the law

No script decides these for a project.

- **Banned features and mandatory patterns.** Under the `gcc` profile `CONSTITUTION.md` §3 and §4
  carry the GCC-incompatible features and the mandatory patterns as hard rules; under `commercial`
  none are imposed. Add the project's own below each section's comment marker, and name the target
  environments in §5.
- **The banned-feature scanner.** Open `scripts/banned_feature_scan.py` and review the pattern
  dicts. `GCC_BANNED_PATTERNS` applies only under the `gcc` profile; `ALWAYS_BANNED_PATTERNS`
  applies everywhere. Add any project-specific patterns below the comment marker. The same file
  holds a second dict, `CONTENT_RULES`, for rules that must also cover the governance docs listed in
  `EXCLUDE_FILES` — that list exempts files which legitimately *name* banned features, and it would
  silently neuter a rule aimed at the docs themselves. Content rules bypass it and carry a per-rule
  `allow` set plus a `fix` string shown with each violation. Put "this spelling is not portable"
  rules here; put "this feature is forbidden" rules in `BANNED_PATTERNS`. See decision 2026-09-20-002.
- **The deferred tokens.** The initializer leaves the brand values and the Azure names unfilled and
  lists them: `docs/standards/secrets_management_standard_v1.0.md` holds `{{KEYVAULT_NAME}}`,
  `{{SPN_NAME}}` and `{{APP_ID}}`, and `docs/standards/document_production_standard_v1.0.md` and
  `resources/README.md` the brand values. Fill them when the project first needs a vault or a
  document.

---

## Installing the gates

A `.pre-commit-config.yaml` is **already provided** in the repo root. It wires the tool-neutral scans as
git pre-commit hooks that fire under any agent (Claude, Codex) or a manual commit — this is the 100%
compliance gate the CONSTITUTION relies on. Every hook is described in
`docs/governance/gate_suite_runbook.md`: one section per hook id, in run order, with its stage,
the self-test it pairs with, what it blocks, why, and the command to run it alone. A gate keeps that
page and the config in step, so a hook you add there needs a section in the same commit.

**The freshness gate is the one people skip, and it is the one that pays.** It exists because a
governance rule enforced only by an agent remembering is not enforcement. On the project this framework
came from, the amendment-sweep rule was written down in a mandatory-read file and **missed six times** —
each time the decision body, the code and the live system were correct, and only the *teaching document*
was stale. Teaching documents are what the next agent reads **instead of** the source.

It needs no configuration: decision IDs are read literally from the first column of your
`sprint/decision-log.md` index and of `docs/governance/framework_decisions.md`, the template's own
log, as one set, so any convention works (`DEC-041`, `2026-07-30-001`, `ADR-7`); prefix yours so
they cannot collide with the framework's bare dates. Rows marked `[EXAMPLE]` are ignored. Just stamp
each knowledge entry (`.claude/rules/knowledge-entries.md`; why, [[reference_kb_freshness]]):

```yaml
teaches: [2026-07-30-001]     # decisions this entry EXPLAINS
verified: 2026-07-30          # when it was last confirmed against them
```

**When you first stamp an existing project, expect a backlog, not a clean pass** — that backlog is the
measure of how long the convention went unenforced. Set `verified:` from each file's **last commit
date, never today**; stamping today marks every entry "verified" when nobody verified it, and defeats
the gate on day one.

**Both `--hook-type` flags are required** when you install (walkthrough step 3). Plain
`pre-commit install` writes only `.git/hooks/pre-commit`. The commit-msg-stage gate
(`commit_attribution_scan.py`) would then sit in config and never fire — the worst failure mode a
gate has, because the config reads as protected. `pre-commit run --all-files` covers the pre-commit
stage only; the runbook gives the commands for the commit-msg and manual stages, which it does not
reach.

---

## Launching the project

**Governed by `docs/standards/sprint_management_standard_v1.0.md`.** For a real project, don't hand-fill
the tracker ad hoc: run **`/project-launch`** (`.claude/skills/project-launch/SKILL.md`; walkthrough
step 6), whose stages take you from intake through the team, the PRD and the architecture to the
**planning-session skill**, which produces the epics, stories, dependencies, Required Standards and
PRD refs in a repeatable structure. `doc-authority-scan` refuses the first real epic until the PRD
and the architecture are approved or their skips logged; making and approving each document is
`docs/templates/README.md`.

---

## Taking a newer template release

`gh repo create --template` squashes history, so a derived project has no git relationship to the
template. `scripts/template_update.py` supplies one: it fetches the release you are on and the one
you want into `refs/template/<version>` (outside `refs/tags/`, invisible to the version gate) and
carries the difference across. Run the **target release's** copy, because the ownership map lives in
the script; a project that predates the updater fetches it the same way:

```bash
git fetch --no-tags git@github.com:SaltyBrett/agentic-dev-template.git \
    +refs/tags/v5.0.0:refs/template/v5.0.0
git show refs/template/v5.0.0:scripts/template_update.py > scripts/template_update.py
python3 scripts/template_update.py --source git@github.com:SaltyBrett/agentic-dev-template.git --to v5.0.0
```

It dry-runs by default. `--apply` writes, stamps `.template-version` last, then runs the full gate
suite. Commit the result as one checkpoint and confirm the push's `gates` run.

What it does per path is decided by ownership, and the initializer's lists are the inverse of it
(a fixture cross-checks the two):

| Class | Paths | Behaviour |
|---|---|---|
| keep | `sprint/` (the decision log included), `.project-profile`, the content folders shipped empty, the persona roster `.claude/agents/`, the template's own packaging | never written; template changes there are named in one line |
| merge | `docs/orchestration/knowledge/INDEX.md` by slug; `docs/governance/framework_decisions.md` by decision ID, rows and bodies | project rows never touched; a framework decision the file lacks is inserted, because the framework's entries `teaches:` it; an edited row or body is reported and left |
| three-way | everything else, through `git merge-file` | an unedited copy takes the template's version; an edited copy takes the change where it does not overlap; an overlap is a conflict, left alone and named. `.gitignore` alone is merged with `--union`: where both sides changed one place, both sides' lines are kept, yours first, and the dry run names it `union` so you read it in `git diff` before the commit |
| adopt | what a `v1.0.0` project holds from the retired `dev-resources` sync: `docs/personas/`, `.resources-version`, a knowledge entry declaring `source: dev-resources` | each persona converted into an agent file in `.claude/agents/` and the old folder removed; the stamp removed; a marked entry merged three-way like any other, and the declaration dropped from one no release step writes. A persona that does not convert exactly is a conflict. Needs PyYAML in the `python3` that runs it |

Template markdown is stripped to your profile before it is compared or written, as at birth. A
conflict withholds the stamp: edit the file and re-run with `--keep <path>`, or take the template's
copy with `--take <path>`. Why it is shaped this way: [[reference_template_update]].

**Adopting `v2.0.0` with real epics.** The approval gate (`doc-authority-scan`) refuses the
adoption's suite run until the PRD in `docs/prd/` and the architecture in `docs/architecture/`
stand approved in `v2.0.0`'s form; the updater writes neither, since both folders are the
project's. Approve the documents the project has been built from as they stand, in the same
commit (decision 2026-10-24-003): each gets the frontmatter of `docs/templates/README.md` step 6
with the project's own scope, the architecture's `prd:` the PRD's version, quoted; a closing
`## Version log` whose one row opens at the version the document states (1.0 where it states none
in numbers) and cites the approval; and the approval decision in `sprint/decision-log.md`, its
`**Affects:**` naming each path as a code span. With no architecture, log the Chair's skip instead
(`docs/templates/README.md`, Skipping a document). The content is unchanged and the file keeps its
name. Run the suite, commit, then `python3 scripts/doc_authority_scan.py --stamp` and commit the
stamp.

---

## Directory Purpose Reference

What each path holds is the repository structure table in
[README.md](README.md#repository-structure), its one home.

---

## AI Agent Workflow Summary

The cold start, checkpoint discipline and the closeout are in `AGENTS.md`, their one home.
