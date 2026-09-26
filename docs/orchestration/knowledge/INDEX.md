# Knowledge Base — Index

**This is the single source of truth for accumulated knowledge and feedback.** It is tool-neutral: every
agent (Claude Code, Codex, future tools) reads and writes here, never into a tool's private memory. See
`AGENT_INTEROP.md` for the interoperability contract and `AGENTS.md` for the cold-start sequence that
points here.

> **★ Every entry declares its decision provenance (CONSTITUTION §6.3).** YAML frontmatter carries
> `teaches: [<decision-id>, …]` (decisions the entry *explains*) and `verified: <date>` (when it was last
> confirmed against them):
>
> ```yaml
> ---
> name: <short title>
> description: <one line — used to judge relevance at recall time>
> teaches: [2026-07-30-001]
> verified: 2026-07-30
> metadata:
>   type: reference | decision | feedback | project
> ---
> ```
>
> **If `verified:` predates a change to something the entry teaches, the entry is SUSPECT** — verify against
> the decision *and* the canonical source before acting on it. `scripts/kb_freshness_scan.py` enforces this
> on every commit. It exists because teaching documents are what the next agent reads **instead of** the
> source, so a fossil here is worse than one in code.
>
> **Clearing a freshness failure means re-verifying and CORRECTING, then bumping `verified:` — never bumping
> the date alone.** And never treat any entry here as authority for a **value**: values live in canonical
> source; these entries explain *why*.

---

## How this works (the flush discipline)

- **Read:** at session start, read this index, then only the entries relevant to the current task.
- **Write:** when you learn something durable (a gotcha, a convention, a resolved decision, a
  non-obvious constraint) — **or when you catch a mistake or take a correction** — create
  `docs/orchestration/knowledge/<slug>.md` and add a one-line pointer to the table below. This is how the
  base compounds: every corrected mistake becomes a permanent rule so it can't recur. **Never** leave the
  learning only in a tool's private memory or chat history.
- **Link:** reference other entries with the wikilink convention `[[<slug>]]`, which resolves to
  `docs/orchestration/knowledge/<slug>.md`.
- **One fact per file.** Keep entries small and single-purpose so ingestion stays cheap as the base grows.

### Entry template

```markdown
# <Title>

**Type:** convention | gotcha | decision | reference
**Added:** YYYY-MM-DD

<the durable learning; link related entries with [[other-slug]]>
```

---

## Entries

| Slug | Summary | Type |
|------|---------|------|
| [reference_pristine_cut](reference_pristine_cut.md) | The cut as executed: read the sanitize check and judge every item against what the reset clears; rename on GitHub first; run the sanitizer while the clone's origin still names the template; copy tracked files only; switch the old clone's origin to the archive name before the new repository takes the old one, because the redirect lasts only until the name is reused; prove the commit-msg gate with zero commits behind it; `v1.0.0` is the sanitized tree alone and the cut's record is carried in after it. | reference |
| [reference_template_sanitizer](reference_template_sanitizer.md) | `sanitize_template.py` is the initializer's machinery without the fill, run only in the template: `--apply` regenerates the two sprint documents and clears the pairs and both archives, keeping every token, both profile blocks and the sync stamp; `--check`, a manual hook, names every item of build state while the sweep of session numbers, probe references and hashes from knowledge entries and decision bodies stays by hand. Why the script excludes itself from the name check, and how citations name the archive repository. | reference |
| [reference_framework_decisions](reference_framework_decisions.md) | The template's decisions live in `docs/governance/framework_decisions.md`, IDs unchanged, and a project's in `sprint/decision-log.md`, which ships with the example alone. The freshness and session gates read both indexes as one set, a missing index still raises naming the log, the framework row wins a duplicate ID, and the updater merges the framework file and never writes the log. Where each kind of session logs, and why a project prefixes its IDs. | reference |
| [reference_resources_sync](reference_resources_sync.md) | The persona registry and resource knowledge entries are a cache of `dev-resources`: `resources_sync.py` fetches a ref and judges every owned path by version, never picking a conflict silently; a resource entry is marked `source: dev-resources` so the updater keeps it; the closeout refuses a persona the synced ref lacks; growth only through `--publish`. | reference |
| [reference_published_hooks](reference_published_hooks.md) | The template is a pre-commit hook repository: `.pre-commit-hooks.yaml` publishes the persona linter, the frontmatter gate and the attribution gate for a consumer to pin by `rev`. pre-commit pip-installs the repository, so `pyproject.toml` exists and every entry is a console script; the gates read their root from git, because `__file__` would judge the virtualenv; the packaging leaves a project at birth. | reference |
| [reference_gate_runbook](reference_gate_runbook.md) | The page describing the pre-commit suite is verified against `.pre-commit-config.yaml` on every commit: one H2 per hook id, in run order, each naming its stage; a hook without `stages:` fails. Why it lives in `docs/governance/` (the updater keeps `docs/runbooks/` for the project), why MAJOR, and what the check cannot read. | reference |
| [reference_template_update](reference_template_update.md) | A derived project shares no commit with the template, so `template_update.py` fetches both releases into `refs/template/` and judges every path against them: `sprint/` kept, the knowledge index and decision log merged by key, everything else three-way, markdown stripped to the profile first. Run the target's copy; the stamp comes last. | reference |
| [reference_precommit_stash](reference_precommit_stash.md) | `pre-commit run <hook>` without `--all-files` stashes unstaged edits to tracked files first, so a manual-stage gate judges the last commit's tracker and sprint-status. The closeout command carries the flag; the gate cannot detect the stash. The same guard refuses to run any hook while the config itself is modified and unstaged. | reference |
| [reference_ci_annotated_tags](reference_ci_annotated_tags.md) | On a tag push, actions/checkout replaces the annotated tag with a lightweight one, so a gate reading annotations sees the commit subject. The workflow fetches tag objects back; the version gate reports `lightweight-tag` instead of a misleading missing bump. | reference |
| [reference_derived_project_start](reference_derived_project_start.md) | Day one of a project created from the template, observed: GitHub's own Initial-commit run, the ssh host alias on the clone remote, what the initializer regenerates, the attribution probe, S1 verify with no pair, and why S1 must open an epic before it can close out. | reference |
| [reference_ci_backstop](reference_ci_backstop.md) | Hooks are per-clone and undetectable from inside the repo; the GitHub workflow runs the same suite plus the commit-msg gate per carried commit. It reports and the hooks block; why branch protection is not in the design even with the repository public, and what the red probe proved. | reference |
| [reference_session_closeout](reference_session_closeout.md) | Session end is a gate: numbered sessions, a handoff/kickoff pair consumed by one session then archived, exact structure with no home for durable content, personas gated by shape not list and append-only by version against the committed copy, every wikilink in the tree resolving with a literal allow set, and `--verify` at the next cold start closing the loop. | reference |
| [reference_commit_classification](reference_commit_classification.md) | Ground rules for deriving a release bump from commit messages, written before the work and kept after it was closed won't-do: `commit-msg` fires on merge commits so a naive prefix rule blocks every merge, and a window with no typed commit must fail rather than default to PATCH. Why the judgement stays: the decision that introduces a change already names its bump. | reference |
| [reference_project_profiles](reference_project_profiles.md) | A project starts under GCC/Gov constraints or under none. One word in `.project-profile` strips the governance prose and switches the scanner together, so the written rule and the enforced rule cannot drift. No profile = the template, which enforces the union. | reference |
| [reference_content_provenance](reference_content_provenance.md) | A rule that bans a name must not write that name down: employer identifiers are stored as hashes of a normalized form, matched over n-grams. Also why the scanner takes its file list from git rather than the filesystem. | reference |
| [reference_template_versioning](reference_template_versioning.md) | What justifies MAJOR vs MINOR vs PATCH: does adopting it force a human to act? For a gates template most new gates are MAJOR. Includes every change here mapped to a bump, and the release order that keeps the stamp honest. | reference |
| [reference_execution_identity_config](reference_execution_identity_config.md) | The zero-th gate passed keys under an unrelated table and a config no TOML parser can load. Parse it; require keys at top level, refuse `sandbox_mode` at any depth, fail closed both ways — and take identity from the uid, since `getpass.getuser()` is environment-first. | reference |
| [reference_kb_frontmatter_validation](reference_kb_frontmatter_validation.md) | Gates that report green while reading the wrong thing: a regex is not a parser, an unscoped file scan is not a section, an empty parse must raise rather than pass, and a fixture that passes against the broken code tests nothing. | reference |
| [reference_commit_attribution_gate](reference_commit_attribution_gate.md) | No AI attribution in commit messages, enforced at the `commit-msg` stage — which fires only if the clone installed both hook types; a hook with no `stages:` runs at every installed stage, and `run --all-files` never tests a commit-msg gate. | reference |
| [reference_agent_execution_identity](reference_agent_execution_identity.md) | No sandbox account/identity/restricted token; sandbox-bounded sessions escalate every command to the existing operator; unsandboxed sessions retain user-reviewed `untrusted` approvals. | decision |
| [reference_macos_toolchain](reference_macos_toolchain.md) | Silent macOS defects: per-clone pre-commit hook with a baked-in interpreter path, Windows git config, case-insensitive APFS vs case-sensitive git, Microsoft fonts absent, and the per-app consent gate on Downloads/Desktop/Documents that presents as a hung command. | reference |
| [reference_precommit_interpreter](reference_precommit_interpreter.md) | Local hooks declare `language: python` so pre-commit provisions the interpreter; `entry: python …` under `language: system` cannot launch on macOS, which has no bare `python` on PATH, and `python3` only moves the failure to Windows. | reference |
<!-- Add one row per knowledge entry above this line, newest first -->
