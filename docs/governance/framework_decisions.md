# Framework Decisions

**Purpose:** The decisions that shaped this template — why every gate, script and rule is the way it is
**Source:** `agentic-dev-template`; carried to a project by `scripts/template_update.py`, merged by decision ID
**Last Updated:** 2026-10-22

> **READ SELECTIVELY (index-first).** Do NOT read this file whole. Read the **Decision Index**, then only
> the entries a task, a handoff or a knowledge entry's `teaches:` points at. Markdown only (never JSON).
>
> **This is the template's log, not the project's.** A project's own decisions go in
> `sprint/decision-log.md`, which ships with the `[EXAMPLE]` entry only. `scripts/kb_freshness_scan.py`
> and `scripts/session_closeout.py` read both indexes as one set, so a knowledge entry may `teaches:` an
> ID from either and a handoff may cite either. Never edit this file in a project: the updater replaces
> an unedited row or body when a release changes it and reports an edited one. IDs here are bare dates;
> a project prefixes its own (`ACME-2026-09-24-001`) so the two sets cannot collide — on a duplicate ID
> this file's row wins (decision 2026-09-23-003, [[reference_framework_decisions]]).
>
> In the template itself, a session that makes a framework decision logs it **here**: a new index row at
> the top of the table, its body at the end of the file, format `[YYYY-MM-DD-NNN]`.

---

## Decision Index

| ID | Date | Title | Status |
|----|------|-------|--------|
| 2026-10-23-003 | 2026-10-23; amended 2026-10-23 | Personas ship as a library in the template, inactive; a project activates the ones it needs into `.claude/agents/` at its first session, where a skill recommends from the library and drafts what it lacks; the full team ships in `v2.0.0`; `dev-resources` retires; a project's own personas stay in it; the updater converts a `v1.0.0` project's `docs/personas/`; built as TMPL-1.8 to TMPL-1.10 | APPROVED |
| 2026-10-23-002 | 2026-10-23 | The Claude Code paths and the session's local files are owned by decision: the registry kept for the sync, the skills, rules and settings merged three-way, the journal, notes and local settings untouched and ignored by the repository itself; a project's `docs/personas/` reaches `.claude/agents/` through `dev-resources`, never by conversion in the project | APPROVED; SUPERSEDED (bullets 1, 4 and 5) by 2026-10-23-003 |
| 2026-10-23-001 | 2026-10-23 | Procedures are skills, and a skill is repository markdown: one `SKILL.md` per procedure, listed by path in `AGENTS.md` for any agent; the closeout forked with the brief in its arguments, the release and the pristine cut the operator's alone; the standards keep the law; `skill-scan` keeps every hook, stage and command a skill names in step with the config | APPROVED |
| 2026-10-22-006 | 2026-10-22 | Rules under `.claude/rules/` are path-scoped judgement only and gated: `paths:` that parse and match a tracked file, no sentence of `AGENTS.md` repeated; `CONSTITUTION.md` §6.3 becomes a knowledge entry for the why and two rules for the instructions, and the knowledge index sheds its frontmatter block to a rule | APPROVED |
| 2026-10-22-005 | 2026-10-22 | Personas are agent files in `.claude/agents/`, the body the Invocation and the rest in frontmatter; the session takes its persona from the `SessionStart` hook, `claude --agent` optional because it replaces Claude Code's built-in prompt; the kickoff names the agent; `dev-resources` holds both trees until TMPL-2.4; amends 2026-10-22-001 | APPROVED; SUPERSEDED (dev-resources holding the registry) by 2026-10-23-003 |
| 2026-10-22-004 | 2026-10-22 | The session journal and the working notes are local and gitignored: the journal records raw commands that must not enter a public history, an ignored file is outside pre-commit's stash, and the Stop hook excludes both by path as well; the closeout gate clears them | APPROVED |
| 2026-10-22-003 | 2026-10-22 | `v2.1.0`: an agentic development team of role subagents whose handoffs are gated artifacts, and a coding standard built as mechanical limits, a process layer and one page of judgement; each opens with a design session, the standard proved against real code before adoption; MINOR | APPROVED |
| 2026-10-22-002 | 2026-10-22 | Authoritative documents stop going stale: `authority:` frontmatter and a version log on each source of truth, `Affects:` on every decision, a gate that accepts a version-log row or an open tracker story and nothing else, the commit stamped after the fact and verified, a technical-writer agent draining the queue at cold start; part of `v2.0.0` | APPROVED |
| 2026-10-22-001 | 2026-10-22; amended 2026-10-22 | `v2.0.0`: the framework runs on Claude Code's native machinery where that removes overhead without removing a control: one cold start run by a SessionStart hook, a Stop hook for checkpoint discipline, a journal and working notes against compaction, personas as subagents, procedures as forked skills, path-scoped rules, the constitution and checklist slimmed, the interop contract retired; git hooks and CI stay the enforcement; MAJOR | APPROVED |
| 2026-09-25-004 | 2026-09-25 | The public template's versioning starts at `v1.0.0` on the finished go-live tree: the four go-live tags removed, the tree sanitized to S1, one tag cut; history kept, nothing force-pushed; the earlier "released as" notes read as folded into it | APPROVED |
| 2026-09-25-003 | 2026-09-25 | A ruleset on `main` in both public repositories blocks deletion and force-push; no required status check, because every checkpoint is a direct push by one developer; revisit at the first second contributor | APPROVED |
| 2026-09-25-002 | 2026-09-25 | MIT license, copyright Brett Bennett, in the template and in `dev-resources`; a project receives it at birth and owns it from then on, the updater never writes it; PATCH | APPROVED |
| 2026-09-25-001 | 2026-09-25 | The template and `dev-resources` are public; a project made from the template is private by default, refused by the initializer when public unless `--public`; the archive stays private; branch protection still not enabled; `dev-resources` pins https and gets a `gates` workflow; MINOR | APPROVED |
| 2026-09-24-001 | 2026-09-24; amended 2026-09-24 | Rules with no control found in the fossil sweep: the tracker's dependency and placeholder rules get a gate (TMPL-5.5, built: `dependency-order` and `live-placeholder`, MAJOR); the pull-request workflow, review checklist and manifest are deleted; evidence capture is procedure, marked ungated; PATCH for the sweep | APPROVED |
| 2026-09-23-008 | 2026-09-23 | A knowledge entry is a resource entry when it teaches no decision and explains a machine, a tool or a workflow rather than this repository; the macOS toolchain entry moves, every gate entry stays | APPROVED |
| 2026-09-23-007 | 2026-09-23; amended 2026-09-23 | The registry and resource entries are synced from `dev-resources` by `resources_sync.py`: verdicts decided by version, conflicts never picked silently, growth only through `--publish`, the updater keeps those paths, the closeout refuses an unpublished persona; MAJOR | SUPERSEDED by 2026-10-23-003 |
| 2026-09-23-006 | 2026-09-23 | Personas are append-only, gated: `version:` and a `## Changelog` in every persona, an Invocation change refused without a bump against the committed copy, the kickoff names the version; MAJOR | APPROVED |
| 2026-09-23-005 | 2026-09-23; amended 2026-09-23; amended 2026-09-25 | The template is a pre-commit hook repository: `.pre-commit-hooks.yaml` publishes the persona linter, the frontmatter gate and the attribution gate as console scripts of a `pyproject.toml` package that leaves a project at birth; the gates read their root from git | APPROVED |
| 2026-09-23-004 | 2026-09-23 | Commit classification is not built: the release bump stays a documented judgement, because the decision that introduces a change already names its bump and the windows it would compute over are small | APPROVED |
| 2026-09-23-003 | 2026-09-23; amended 2026-09-24 | The template is sanitized to a pristine `v1.0.0` from a fresh init after its build history is archived; framework decisions move to `docs/governance/framework_decisions.md` (built as TMPL-4.1, MAJOR); the sanitizer and the sweep (built as TMPL-4.2, MINOR); the archive repository named; the cut done (TMPL-4.4), this repository archived and the new lineage at `v1.0.0` | APPROVED |
| 2026-09-23-002 | 2026-09-23 | `dev-resources` is the durable home for personas and reference knowledge: projects hold a stamped snapshot synced at closeout, ownership is disjoint from the template's, personas are append-only and enhanced by version | APPROVED; SUPERSEDED (personas and shared knowledge in dev-resources) by 2026-10-23-003 |
| 2026-09-23-001 | 2026-09-23 | The gate suite is described by one runbook page that a gate keeps in step with the config; every hook declares its stage; released MAJOR | APPROVED |
| 2026-09-22-004 | 2026-09-22; amended 2026-09-24 | A derived project takes a newer release through `template_update.py`: ownership by path as the initializer's inverse, keyed merges for the index and the framework decisions file (the project's decision log until 2026-09-23-003 was built), three-way for the rest | APPROVED |
| 2026-09-22-003 | 2026-09-22; amended 2026-10-22 | The closeout command runs with `--all-files`, because pre-commit stashes unstaged edits and the gate then judges the wrong tree; amended: the cold-start verify too, where the stash made a dirty tree pass | APPROVED |
| 2026-09-22-002 | 2026-09-22 | The derived-project probe: the initializer regenerates the tracker; CI restores annotated tags; the version gate names a lightweight tag | APPROVED |
| 2026-09-22-001 | 2026-09-22; amended 2026-09-22; amended 2026-09-23; amended 2026-09-25 | CI runs the gate suite on every push and pull request; a reporting backstop; branch protection not enabled, first for want of a plan, then (public, 2026-09-25-001) because checkpoints push straight to `main` | APPROVED |
| 2026-09-21-001 | 2026-09-21; amended 2026-09-24 | Session closeout is a gate; handoff and kickoff prompt are one-session repo artifacts; personas are shape-gated; every wikilink in the tree resolves | APPROVED |
| 2026-09-20-009 | 2026-09-20 | A project starts on the `gcc` or `commercial` profile; the toggle is mechanical | APPROVED |
| 2026-09-20-008 | 2026-09-20 | gitleaks joins the suite; a private repo has no other secret control | APPROVED |
| 2026-09-20-007 | 2026-09-20 | Employer identifiers are refused by hash, not by name; channel renamed | APPROVED |
| 2026-09-20-006 | 2026-09-20 | Template version is verified against its tags; bump type is a documented judgement | APPROVED |
| 2026-09-20-005 | 2026-09-20 | Parse `.codex/config.toml`; required keys at top level, `sandbox_mode` forbidden at any depth | APPROVED |
| 2026-09-20-004 | 2026-09-20 | Scope the decision-index parser, fail loudly on an unreadable index, self-test it | APPROVED |
| 2026-09-20-003 | 2026-09-20 | Validate KB frontmatter with a parser, and cross-check both readers agree | APPROVED; SUPERSEDED (table-in-body constraint only) by 2026-09-20-004 |
| 2026-09-20-002 | 2026-09-20; amended 2026-09-20 | Content rules are a second scanner channel that bypasses `EXCLUDE_FILES` | APPROVED |
| 2026-09-20-001 | 2026-09-20 | Every clone installs both pre-commit hook types (`pre-commit` + `commit-msg`) | APPROVED |
| 2026-09-19-001 | 2026-09-19 | Split the template from employer-specific brand and program content | APPROVED |
| 2026-07-30-001 | 2026-07-30 | Portable execution identity: no sandbox execution + user-reviewed approvals | APPROVED |

---

## Decision 2026-07-30-001: Portable execution identity and approval boundary

**Date:** 2026-07-30
**Made By:** Chair + AI
**Status:** APPROVED

### Context

Requiring Codex Full access as a precondition conflates two separate controls: command sandbox scope
and approval policy. It also turns `read-only` / `workspace-write` metadata into a false hard stop even
when the client can request approved execution under the operator's existing identity.

### Decision

- Never create or use a sandbox account, sandbox identity, restricted sandbox token, private sandbox
  desktop, or native Windows sandbox execution for repository commands.
- If a session exposes a sandbox boundary, request user-reviewed escalation before every local
  command; never try the sandbox first.
- Treat `read-only` / `workspace-write` metadata as a reason to escalate, not a reason to abandon the
  session.
- If already unsandboxed under the existing operator identity, retain
  `approval_policy = "untrusted"` and `approvals_reviewer = "user"`.
- Stop when escalation is unavailable or still executes through a sandbox/offline identity.

### Enforcement

`.codex/config.toml`, the canonical `AGENTS.md`, `AGENT_INTEROP.md`, `CONSTITUTION.md`, the cold-start
checklist, `scripts/agent_execution_identity_guard.py`, and the first local pre-commit hook.

### Official basis

- <https://learn.chatgpt.com/docs/agent-approvals-security.md>
- <https://learn.chatgpt.com/docs/permission-modes.md>
- <https://learn.chatgpt.com/docs/config-file/config-reference.md>
- <https://learn.chatgpt.com/docs/windows/windows-sandbox.md>

---

## Decision 2026-09-19-001: Split the template from employer-specific brand and program content

**Date:** 2026-09-19
**Made By:** Chair + AI
**Status:** APPROVED

### Context

The framework was developed inside an employer repository and its origin pointed at that employer's
GitHub Enterprise instance. An audit before porting it to a personal machine found employer-specific
content in exactly three locations, with every other file already generic:

- `resources/branding/` — logos, typeface guide, color palette, two branded Word templates
- `resources/README.md` — brand palette values and template filenames
- `docs/standards/document_production_standard_v1.0.md` — brand values plus internal product,
  platform, and program names

`AGENTS.md`, `CONSTITUTION.md`, `AGENT_INTEROP.md`, all four scripts, the sprint scaffolding, and the
other three standards carried no employer identifiers.

The governance machinery is the reusable contribution. The brand assets and program names are not,
and they should not travel to a personal account where they would sit in a private repository that
receives no secret scanning on a free plan.

### Decision

- Maintain two lineages. The employer repository keeps brand assets and program-specific content and
  stays on the employer's GitHub Enterprise instance. The personal template carries only the
  governance machinery.
- Tokenize rather than delete the contaminated documents. `resources/README.md` and the document
  production standard keep their structure, section order, label key (`[Brand official]`, `[Locked]`,
  `[Suggested]`, `[Get from source]`), and craft rules, with brand values replaced by `{{TOKENS}}`.
  The method is the reusable part; the values are per-project.
- Ship `resources/branding/` empty with a scaffold, so the shape is obvious and the assets are not.
- Sections 7 through 14 of the document production standard remain portable craft rules and apply as
  written in any project. Sections 1 through 6 require token fill before first use.
- Start the personal lineage from a fresh `git init`. The prior history is not carried across, which
  also removes the employer remote and the stale generated pre-commit hook.

### Rationale

Splitting on content rather than on file boundaries keeps the framework's value intact. A de-branded
template is in fact more reusable than the original, because §6 of `AGENT_INTEROP.md` already
describes the framework as a template meant to travel between repositories with per-project content
swapped out. This decision makes the existing intent literal.

### Enforcement

`resources/README.md` and `docs/standards/document_production_standard_v1.0.md` carry a template note
directing token fill before first use. No mechanical gate enforces de-branding; adding one is an open
question below.

### Open questions

- ~~Should `banned_feature_scan.py` gain a rule that fails the commit when a known employer
  identifier appears in the personal lineage?~~ **RESOLVED by 2026-09-20-007** — yes. Identifiers are
  matched by hash rather than listed by name, so the rule does not publish what it suppresses.

---

## Decision 2026-09-20-001: Every clone installs both pre-commit hook types

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`scripts/commit_attribution_scan.py` blocks AI attribution trailers in commit messages. It must run at
the `commit-msg` stage, because the commit message does not exist when pre-commit-stage hooks fire.

`pre-commit install` writes only `.git/hooks/pre-commit`. A clone that ran the old command has the
attribution gate in `.pre-commit-config.yaml` and no `.git/hooks/commit-msg` to invoke it. The gate is
then **present in config and absent in practice** — a config file that reads as protected while every
commit passes unchecked. That is strictly worse than having no gate, because it removes the reason to
look.

`.git/hooks/` is never committed, so no repo-side change can fix this. It is a per-clone action, and
the only defense is that the documented command be correct everywhere it appears.

### Decision

- The per-clone install command is, repo-wide and without exception:

      pre-commit install --hook-type pre-commit --hook-type commit-msg

- Every hook in `.pre-commit-config.yaml` declares an explicit `stages:`. A hook with no `stages:` key
  runs at *every installed stage*, so installing the `commit-msg` hook type would otherwise re-run the
  identity, banned-feature and KB-freshness gates a second time on each commit. The three existing
  gates are pinned to `stages: [pre-commit]`; the attribution gate is pinned to `stages: [commit-msg]`.
- The cold-start checklist verifies both hook files exist (`ls .git/hooks/`) rather than asking whether
  "pre-commit is installed", which is the question that passes while the gate is inert.

### Consequences

- **Every existing clone must re-run the install command.** Pulling this change does not install the
  commit-msg hook. Until an operator runs it on a given machine, that machine's attribution gate does
  not exist.
- `pre-commit run --all-files` exercises the pre-commit stage only, so it will report a clean suite on
  a machine where the attribution gate is not installed. Verifying a commit-msg gate requires
  `pre-commit run --hook-stage commit-msg --commit-msg-filename <file>` or a real trial commit.
- Any future commit-msg-, pre-push- or post-checkout-stage gate inherits this problem. Adding a hook at
  a new stage means updating the documented install command in the same work unit.

### Enforcement

`.pre-commit-config.yaml` (header comment + explicit `stages:` on every hook), `TEMPLATE_GUIDE.md`
Step 6, `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md` Part A, `sprint/sprint-status.md`, and the
knowledge entries [[reference_commit_attribution_gate]], [[reference_macos_toolchain]] §1,
[[reference_precommit_interpreter]].

### Related

- `AGENTS.md` prime directive forbidding AI attribution in commit messages
- `CONSTITUTION.md` §6.2 (pre-commit hooks are the primary gate; do not bypass)

---

## Decision 2026-09-20-002: Content rules are a second scanner channel, not more banned patterns

**Amended 2026-09-20 by 2026-09-20-007:** the channel was renamed `PORTABILITY_RULES` -> `CONTENT_RULES`
when a provenance rule joined it. The decision's substance — a second channel that bypasses
`EXCLUDE_FILES`, with per-rule `allow` sets — is unchanged.

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

Every documented way to run a gate by hand invoked the gate script with a bare `python`, which cannot
execute on macOS. The hooks were portable; only the prose was broken. It was corrected across `README.md`,
`AGENTS.md`, the cold-start checklist, four script docstrings and the Claude allow-list — but as a
convention it would return, because the rule lived only in a knowledge entry.

The obvious enforcement was a new entry in `BANNED_PATTERNS` in `scripts/banned_feature_scan.py`.
**That would not have worked, and it would have looked like it was working.** `BANNED_PATTERNS` is
filtered through `EXCLUDE_FILES`, which exempts `AGENTS.md`, `AGENT_COLDSTART_CHECKLIST.md`,
`CONSTITUTION.md` and `TEMPLATE_GUIDE.md` so that governance docs may legitimately *name* banned
Fabric features. Two of those four are where this defect actually landed. The gate would have been
inert in exactly the files it most needed to cover, and a green scan would have certified them.

### Decision

- Add a second channel, `CONTENT_RULES` (originally `PORTABILITY_RULES`), checked by `should_scan_content()` /
  `scan_portability()`. It applies `SCAN_EXTENSIONS` and `EXCLUDE_DIRS` but **not** `EXCLUDE_FILES`.
- Each rule carries its own `allow` set of filenames, so an exemption is one rule in one file rather
  than a whole file dropping out of the scan. The bare-`python` rule allows exactly three:
  `.pre-commit-config.yaml` (resolves inside pre-commit's virtualenv), the knowledge entry that quotes
  the broken pattern to teach it, and the scanner that holds the pattern.
- Each rule carries a `fix` string, printed with the violation. A gate that says only "blocked"
  invites a bypass; one that names the correct command does not.
- Portability matching is **case-sensitive**, unlike `BANNED_PATTERNS`, so prose such as "Python
  scripts" is not a violation. `\s+` cannot cross the `3`, so `python3 scripts/…` passes.

### Consequences

- Exempting a file from a content rule means adding it to that rule's `allow` set. Adding it to
  `EXCLUDE_FILES` instead silently drops it from every banned-feature check as well.
- `EXCLUDE_FILES` now has a narrower meaning than its name suggests: it governs `BANNED_PATTERNS`
  only. The comment above `CONTENT_RULES` records why.
- Future content rules (ambient tool names, absolute paths, OS-specific separators) belong in this
  channel rather than in `BANNED_PATTERNS`.

### Verification

A probe line added to `AGENTS.md` — an `EXCLUDE_FILES` member — exits 1; removing it exits 0. Blocking
was confirmed by exit code, not by console text.

### Enforcement

`scripts/banned_feature_scan.py`, already wired as a pre-commit-stage hook. Taught by
[[reference_precommit_interpreter]].

---

## Decision 2026-09-20-003: Validate KB frontmatter with a parser, and cross-check both readers agree

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`kb_freshness_scan.py` reads frontmatter with two regexes rather than a YAML parser. Regexes match;
they do not validate. An entry whose frontmatter is not loadable YAML still satisfies both patterns,
so the gate reports green on a file no YAML consumer can read — the same shape as the defect the
freshness gate exists to catch, one level down.

Investigating this surfaced a second and harder problem. The two parsers **disagree about several
spellings that are valid YAML**, measured rather than assumed. The unquoted zero-padded form is the
only one they read alike; the full comparison is tabulated in
[[reference_kb_frontmatter_validation]]. In short:

- an unquoted zero-padded date is read identically by both — this is the only agreeing spelling
- a **quoted** date is a clean string to YAML and invisible to the regex, which reports UNSTAMPED
- a **timestamp** is truncated by the regex and kept whole by YAML
- a **non-padded** date is a plain string to YAML and invisible to the regex
- `teaches:` as a **block list** parses correctly and is read as empty by the regex, which silently
  skips the entry altogether
- `teaches:` with **quoted** IDs keeps the quote characters in the regex path, so every ID is UNKNOWN

Two are traps. Quoting the date is the natural response to "make it valid YAML" and makes the
freshness gate report a missing date that is visibly present. A block `teaches:` list is idiomatic,
parses correctly, and makes the entry vanish from the freshness gate while still looking stamped.

A separate coverage gap: an entry with `teaches: []` can never be reported stale, so a green scan
reads as full coverage when it is a fraction of it.

### Decision

- Add `scripts/kb_frontmatter_scan.py`, hooked at `stages: [pre-commit]` per decision
  `2026-09-20-001`, with `additional_dependencies: [pyyaml]` — possible only because hooks declare
  `language: python` (decision context: [[reference_precommit_interpreter]]).
- It fails on: no frontmatter block, a YAML parse error, a missing `teaches` key, a missing
  `verified` key, and a `verified` value that is not an unquoted ISO date.
- **It does not enforce "valid YAML". It enforces the intersection — the one spelling both gates read
  identically.** Valid YAML the freshness gate cannot see is still a defect.
- That last rule is implemented as a **cross-check**, not as an enumerated rule list: the scanner
  imports `kb_freshness_scan.parse_frontmatter`, parses each entry both ways, and fails when the
  results differ. The table above is documentation, not logic, so a future divergence is caught
  without anyone remembering to update a rule.
- It runs **before** the freshness gate in the hook order. Validate the input before trusting the
  check that consumes it.
- `teaches: []` stays legal. `kb_freshness_scan.py --list` reports gate reach and names uncovered
  entries — informational, never a failure. Forcing a decision ID into an entry that explains none
  would manufacture a false link, a worse defect than no link.
- Without PyYAML the scanner exits **2**, never 0. A missing parser must not present as a pass.

### Consequences

- Never quote `verified:` or the IDs in `teaches:`, and never write `teaches:` as a block list. All
  three are valid YAML and all three break the freshness gate.
- The freshness regex's strictness is load-bearing and must not be relaxed to accept a new spelling:
  `kb_freshness_scan` compares dates as **strings**, which is correct only for zero-padded ISO.
- Any future consumer of this frontmatter is added to the cross-check rather than trusted to agree.
- ~~Do not put a markdown table in a decision body if any row's second cell contains an ISO date.~~
  **SUPERSEDED by 2026-09-20-004.** This was a prose constraint guarding an append-only file, which
  is not a control. `load_decisions()` is now scoped to the Decision Index section, so a table in a
  decision body is simply not read. Tables in decision bodies are permitted again.

### Verification

Six malformed entries were injected into `docs/orchestration/knowledge/` one at a time — invalid
YAML, quoted date, block list, missing `teaches`, missing `verified`, non-date `verified`. Each
exited 1; the tree returned to exit 0 after removal. Confirmed by exit code without a pipe, since a
pipe reports the last command's status rather than the scanner's.

### Correction to the report that prompted this

The report cited `reference_precommit_interpreter.md` as having been committed with a malformed
`name:` scalar. It was not: that file parses cleanly under `yaml.safe_load` at every commit in its
history in the archive repository, including the one that introduced it. The **mechanism** is real and was reproduced
with a constructed probe; the specific historical instance was not. Recorded so the next reader does
not go looking for a defect that was never in the tree.

### Enforcement

`.pre-commit-config.yaml` (`kb-frontmatter-scan`, before `kb-freshness-scan`). Taught by
[[reference_kb_frontmatter_validation]].

---

## Decision 2026-09-20-004: Scope the decision-index parser, fail loudly, and self-test it

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED
**Supersedes:** 2026-09-20-003 (the table-in-body prose constraint only; the rest of that decision —
frontmatter validation and the parser cross-check — stays in force)

### Context

`load_decisions()` parsed every `|`-prefixed line in `sprint/decision-log.md`, so a markdown table in
a decision body was absorbed as a phantom decision. Decision 2026-09-20-003 answered that with a
written rule: do not put such tables in decision bodies.

**A prose constraint guarding an append-only file is not a control.** It has no enforcement, and it
sits in the one file that grows without review — every future decision is a fresh chance to violate
it, and the violation is silent. It is also the exact fossil shape `CONSTITUTION.md` §6.3 exists to
catch: a written rule standing in for a mechanism.

The latent failure was worse than the phantom row. Because the parser scanned the whole file, a
rename of the `## Decision Index` heading would have yielded zero decisions with no error. Every
`teaches:` would then report UNKNOWN — or, with nothing stamped, the gate would report **green while
checking nothing**. That is the same failure mode as the regex-not-a-parser defect in 003.

### Decision

- `load_decisions()` reads the **Decision Index section only**. The boundary is taken from the file's
  actual structure: the `## Decision Index` heading, then the contiguous run of `|` lines beneath it,
  ending at the first horizontal rule, the next heading, or the end of the table.
- **An index that cannot be located raises `DecisionIndexNotFound` and exits non-zero** with a
  diagnostic. An unreadable index is never zero decisions. The same applies to a decision log that is
  missing while entries still declare `teaches:` — that now fails instead of returning 0.
- The parser proves its own boundary on every commit. `--self-test` runs nine in-memory fixtures
  covering: index rows parsed, a table inside a decision body, a `|`-prefixed body line shaped to look
  like an index row, `[EXAMPLE]` rows, supersession resolution, an index with zero data rows, a
  missing heading, and a heading with no table. Wired as `kb-freshness-selftest`, `stages:
  [pre-commit]` per 2026-09-20-001, ordered before the gate it validates.
- Tables in decision bodies are permitted again. The constraint from 2026-09-20-003 is withdrawn.

### Consequences

- Renaming the `## Decision Index` heading now breaks the build loudly instead of silently emptying
  the gate. Renaming it deliberately means updating `INDEX_HEADING` in the same work unit.
- Fixtures must **discriminate**. The first draft of the "pipe-prefixed body line" fixture passed
  against the broken parser too — its second cell held no date, so the old code rejected it for an
  unrelated reason. A fixture that passes under the bug is false confidence; it was reshaped to carry
  a date and now fails against the unscoped parser. Verified by running the suite against a
  monkeypatched copy of the original parser: 5/9 pass, and the phantom `` `verified: 2026-09-20` ``
  reappears exactly as it did in the real file.

### Audit: the same shape elsewhere

Every gate script was checked for "scans a whole file for a pattern rather than a scoped region".

- **`commit_attribution_scan.py` — FOUND, FIXED HERE.** `git commit --verbose` appends the staged
  diff below a scissors line, and those diff lines are not comment-prefixed. The scanner read the
  diff as if it were the message, so staging any change touching an attribution example — `AGENTS.md`
  carries one in its prime directive — blocked the commit and told the author to remove a line they
  never wrote. Demonstrated, then fixed by truncating at the scissors line. Re-verified in four
  directions: clean-message-with-dirty-diff passes, dirty-message-above-scissors still blocks, and
  both non-verbose cases are unchanged.
- **`agent_execution_identity_guard.py` — FOUND, NOT FIXED.** It checks `.codex/config.toml` with
  `re.MULTILINE` over the whole file, unscoped by TOML table. A probe config with
  `approval_policy = "untrusted"` under `[some.unrelated.table]` **passes the gate** while
  `tomllib` reports the top-level key as absent — i.e. absent where Codex actually reads it. This is
  a false negative in the zero-th gate. Left for a separate decision because the fix needs one:
  `tomllib` is stdlib only on Python 3.11+, so a clone on 3.10 needs a fallback or a declared
  `additional_dependencies: [tomli]`. Recorded as an open question below.
- **`banned_feature_scan.py` — not this defect.** Whole-file scanning is its purpose; its scoping is
  the per-rule `allow` sets and `EXCLUDE_FILES` (2026-09-20-002).
- **`kb_frontmatter_scan.py` — not this defect.** It parses a delimited frontmatter block, and the
  cross-check against the freshness gate's reader is itself a boundary assertion.
- **`md_to_docx.py`** is a converter, not a gate.

### Open questions

- ~~Should `agent_execution_identity_guard.py` parse `.codex/config.toml` with `tomllib` and assert
  the keys at top level?~~ **RESOLVED by 2026-09-20-005** — yes, with a `tomli` fallback declared via
  `additional_dependencies`.

### Verification

`--self-test` exits 0 against the fixed parser and 1 against a monkeypatched copy of the original,
naming the exact phantom ID the real file produced. The full suite was run with a renamed index
heading (exit 1, diagnostic) and restored (exit 0). All by exit code without a pipe.

### Enforcement

`scripts/kb_freshness_scan.py` (`index_rows`, `DecisionIndexNotFound`, `--self-test`) and
`.pre-commit-config.yaml` (`kb-freshness-selftest`). Taught by
[[reference_kb_frontmatter_validation]].

---

## Decision 2026-09-20-005: Parse the Codex config, and fail closed in both directions

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED
**Resolves:** the open question on 2026-09-20-004

### Context

The zero-th gate checked `.codex/config.toml` with `re.MULTILINE` over the whole file. Two false
negatives, both measured against real probe files:

- keys under `[some.unrelated.table]` — the regex matched; `tomllib` reports top level as empty, so
  the keys were absent exactly where Codex reads them
- a file containing `this is not = = valid toml [[[` — the regex matched; no TOML parser can load it

The second was not in the original audit. It is the regex-is-not-a-parser defect from 2026-09-20-003,
in the one gate that runs first.

### Decision

- Parse with `tomllib` (3.11+), falling back to `tomli`, declared as
  `additional_dependencies: [tomli]` on both identity hooks. **No parser available exits 2, never 0**,
  per the precedent set by `kb_frontmatter_scan.py`. A missing parser must not present as a pass.
- **Required keys are checked at top level**, where Codex reads them. A key found elsewhere is not
  compliance, and the diagnostic names the table it was found in — otherwise the next reader concludes
  the key is missing and adds a second copy.
- **`sandbox_mode` is forbidden at any depth.** See the reasoning below.
- A nested `approval_policy` / `approvals_reviewer` that *contradicts* the required value is also a
  violation. A profile table that weakens the approval policy is precisely the bypass this gate
  exists to prevent.
- `--self-test` with nine in-memory fixtures, wired as `agent-execution-identity-selftest` ahead of
  the gate it validates, per the pattern in 2026-09-20-004.

### Why the rule is asymmetric

Required keys must be where Codex reads them; a forbidden key is refused wherever it appears. The
asymmetry is not an inconsistency — **both directions fail closed**:

- Whether a nested table is live is external, versioned knowledge about another tool. Codex supports
  profile tables selectable at launch, and this gate must not encode a guess about which tables are
  active in which version.
- If a nested `sandbox_mode` is inert, refusing it costs nothing: the remedy is deleting a key that
  does nothing.
- If it is live, refusing it is the entire purpose of the gate.
- Either way its presence states intent to configure a sandbox mode, which the law forbids outright.

Checking a forbidden key only at top level would have been a regression — the old regex, being
line-based and unscoped, did catch `sandbox_mode` under `[profiles.x]`. A fixture pins that.

### Audit: the identity check itself

`getpass.getuser()` plus `USERNAME` / `USER` / `LOGNAME`, matched against `sandbox|codex.*offline`.

**This is not the config bug's shape.** The config bug was an unscoped text scan of a structured file.
This is a **provenance** defect: the inputs are not the authority.

`getpass.getuser()` is environment-first by its own implementation — it reads LOGNAME, USER, LNAME,
USERNAME and only then falls back to the password database. So all four inputs collapsed into one
class, environment, and the gate had no authoritative source at all. Demonstrated: with `USER` and
`LOGNAME` set to `sandbox-agent`, the guard reports a forbidden identity on a machine whose real uid
resolves to `twdaddy`; the environment alone decided the verdict, in both directions.

Fixed here: `pwd.getpwuid(os.getuid())` is consulted first and is the name reported in the PASS line,
which now carries its source — `PASS (twdaddy [uid]; …)` or `[env-only]` where `pwd` is unavailable,
as on Windows. Environment values are still read as additional signals, but they can no longer hide
the uid-derived name.

**What remains, stated plainly:** name matching is a denylist. It catches an identity *named*
sandbox/offline, not every sandboxed identity, and no local check can prove the boundary a session
was launched under. The docstring already called this defense in depth; that remains true, and is now
true of an input that is at least authoritative.

### Verification

Fixtures were run against the **old** regex parser before being trusted: 6 of 10 passed there and
were testing nothing. The three that discriminate are the unrelated table, the weakened profile, and
malformed TOML — plus the diagnostic assertion, which the old parser cannot satisfy.

Then proved on **real probe files** written to `.codex/config.toml`, by exit code without a pipe:
baseline 0; unrelated table 1; malformed TOML 1; `sandbox_mode` under `[profiles.x]` 1; missing key 1;
file absent 1; restored 0, byte-identical.

One harness bug was found and fixed in the process: the extra diagnostic assertion raised `IndexError`
instead of reporting FAIL when the parser returned no violations. A self-test that crashes reports
nothing at the moment it matters most.

### Enforcement

`scripts/agent_execution_identity_guard.py` and `.pre-commit-config.yaml`
(`agent-execution-identity-selftest`, then `agent-execution-identity`). Taught by
[[reference_execution_identity_config]].

---

## Decision 2026-09-20-006: Verify the template version against its tags; keep the bump a judgement

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`new_project.py` stamps `.template-version` into every project it initializes, from a constant in its
own source. Nothing compared that constant to the tag. Tag `v1.1.0`, forget to bump the constant, and
every project created afterwards is labelled `v1.0.0` — silently. The only existing check confirmed
the string *looked* like a version, not that it was the right one.

That was the last hand-maintained value in the repository, and the same convention-instead-of-control
shape as the twelve defects already recorded. It was introduced in the same session that removed the
others, which is why it is being closed rather than noted.

A second question came with it: what justifies `v1.1.0` over `v1.0.1`?

### Decision

**The mechanics are gated. The bump is not, because it cannot be.**

`scripts/template_version.py --check` runs on every commit and verifies, for every tag:

1. the name is `vMAJOR.MINOR.PATCH`
2. the commit it points at carries `TEMPLATE_VERSION` equal to that tag
3. the annotation names the bump — MAJOR, MINOR or PATCH

Rule 3 exempts the earliest tag, and not as a carve-out: a bump is defined relative to a predecessor,
and the first release has none. The gate skips entirely in a repository with no tags, which is every
project created from this template.

The bump *type* stays a documented judgement in [[reference_template_versioning]], keyed to one
question: **would adopting this force a human to do something** — run a different command, or edit a
file to pass a check that did not exist? Yes is MAJOR. The tiebreaker is *when unsure, go up*:
under-versioning hides a change that costs someone an afternoon, over-versioning costs a digit.

A gate can check that a tag is well-formed and that its commit agrees with it. It cannot weigh what a
change costs whoever adopts it. Pretending otherwise would produce a rule that is mechanical and
wrong, which is worse than one that is honest and manual.

### Consequences

- **Releases have an order, and it is not the obvious one.** Set the constant, commit, *then* tag.
  Tagging first points the tag at a commit carrying the previous version; the gate then fails on the
  next commit, after the tag is published. `--release vX.Y.Z` sets the constant and prints the two
  remaining commands in order.
- **For a compliance template, most new gates are MAJOR.** A gate exists to block commits, so adding
  one can block content a project already has. MINOR is therefore narrower here than in a library —
  in practice a self-test, which cannot fail a project's content.
- **Between releases the stamp names the last release.** `gh repo create --template` takes `main`'s
  HEAD, and at pre-commit time `git describe` reports the *previous* commit, so no hook can stamp the
  commit being made. The gate prints a note when `main` is ahead of the last tag. Tag before creating
  a project if the distinction matters.

### Verification

Self-test: 8 in-memory fixtures. The gate itself was proved in a scratch clone by creating a badly
named tag and a tag pointing at a mis-stamped commit with no bump type in its annotation — three
violations reported with fixes, exit 1; exit 0 before they were added.

An incidental confirmation: the scratch clone sits outside `~/code/personal/`, so
`user.useConfigOnly true` refused to create the annotated tag until a local identity was set. Layer 4
of the identity separation working as designed, observed rather than assumed.

### Enforcement

`scripts/template_version.py` and `.pre-commit-config.yaml` (`template-version-selftest`, then
`template-version`). Taught by [[reference_template_versioning]].

---

## Decision 2026-09-20-007: Employer identifiers are refused by hash, not by name

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED
**Resolves:** the open question on 2026-09-19-001
**Amends:** 2026-09-20-002 (channel renamed; substance unchanged)

### Context

Decision `2026-09-19-001` split this template from employer brand and program content, and closed with
an open question: should a rule fail the commit when an employer identifier appears? It stayed
procedural for a day.

It became urgent for a concrete reason. The macOS runbook — about to enter version control — carries
an employer product name in prose. Creating that repository first and adding the rule later would put
the identifier in a permanent git object and then fail the repository against its own gate, with only
a history rewrite or a standing exception to resolve it. Sequencing the rule first avoids rework of
the expensive kind.

### Decision

**The identifiers are stored as hashes, not names.** An identifier this repository must never contain
cannot be written into this repository in order to be banned. Plaintext would put the very string in
`scripts/banned_feature_scan.py` and force the scanner to exempt itself — defeating the rule in the
act of stating it.

- SHA-256 of the normalized form: lowercased, stripped to alphanumerics, re-joined. One hash covers
  every spelling of a name — spaced, hyphenated, camel-cased or upper-cased.
- Matching sweeps 1- to 3-word n-grams per line and concatenates each, so a multi-word identifier is
  caught whatever punctuation separates it.
- The rule has an **empty `allow` set**. There is no file in this repository where such a name belongs.
- `--add-identifier "Name"` prints a hash to paste. The name is never written to any file.

**The channel is renamed** `PORTABILITY_RULES` -> `CONTENT_RULES`, amending `2026-09-20-002`. "No
employer identifier" is not a portability concern, and filing it under a name that says otherwise
misleads the next reader. The channel is defined by its *scope* — every file, `EXCLUDE_FILES` included
— not by a topic. A rule now carries either `patterns` (regex) or `hashes`.

### Honest limit

A hash is **non-disclosure, not secrecy**. It is unsalted, because a salt stored beside it protects
nothing. Anyone who already guesses a name can confirm it. The goal is that the control does not
*publish* the name, not that the name is unknowable.

### Consequences

- Adding an identifier is a two-step: run `--add-identifier`, paste the hash. Slightly more friction
  than a plaintext list, and the friction is the point.
- A hashed denylist is unreadable by design. The violation message shows the offending line, which
  contains the name — visible to the author who already has it, published nowhere.
- Only one identifier is seeded. The others are the operator's to add; the rule is live either way.

### Two defects found while building it

**The scanner caught me writing the identifier into the comment explaining why identifiers must never
be written.** The explanatory block used a real name as its example. The rule flagged it on the first
run. The examples are now fictional and the comment says why.

**The scanner blocked a commit over a gitignored file.** `.claude/settings.local.json` is covered by
the global gitignore and can never be committed, yet it failed the rule — a false positive naming a
file the author cannot fix by committing. `candidate_files()` now takes the file list from
`git ls-files --cached --others --exclude-standard`, i.e. what git would actually commit, falling back
to a filesystem walk outside a repository.

### Verification

Ten in-memory fixtures, including: every spelling collapses to one hash, a multi-word identifier is
found through punctuation, an unrelated line does not match, n-grams cover exactly up to the limit,
the provenance rule's `allow` set is empty, and content rules still bypass `EXCLUDE_FILES`. Live: a
hyphenated occurrence in a committable file exits 1; removing it exits 0.

### Enforcement

`scripts/banned_feature_scan.py` (`CONTENT_RULES`), `.pre-commit-config.yaml`
(`content-rules-selftest`, then `banned-feature-scan`). Taught by [[reference_content_provenance]].

---

## Decision 2026-09-20-008: gitleaks joins the suite

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

GitHub runs secret scanning and push protection free on **public** repositories only. A private
repository on a free personal account gets neither — the inverse of most people's intuition, and the
reason "I made it private" is not a control.

### Decision

Add `gitleaks` from its upstream repository, pinned at `v8.21.2`, with an explicit
`stages: [pre-commit]`.

**That `stages:` line is mandatory and is the whole reason this needed a decision.** Gitleaks'
upstream `.pre-commit-hooks.yaml` declares no `stages:` key — verified by fetching it — and a hook
without one runs at *every installed stage*. With both hook types installed it would scan twice per
commit. `2026-09-20-001` requires an explicit `stages:` on every hook; that rule applies to hooks
pulled from other repositories, not only to local ones.

### Consequences

- First run in a fresh clone downloads and builds the gitleaks environment, so it needs the network
  once — alongside `tomli` and `pyyaml`.
- This is a new gate that can fail content a project already has: a committed secret that previously
  went unnoticed now blocks the commit. MAJOR under [[reference_template_versioning]].

### Enforcement

`.pre-commit-config.yaml`, the `gitleaks` repo entry.

---

## Decision 2026-09-20-009: A project starts on the `gcc` or `commercial` profile

**Date:** 2026-09-20
**Made By:** Chair + AI
**Status:** APPROVED

### Context

The GCC compliance regime is the law of one kind of engagement, not of every project. This template
imposed it on all of them, which is wrong for commercial or personal work — and the machinery around
it (the gates, the decision log, the knowledge base, the versioning) is worth keeping either way.

The tempting fix is a sentence in the constitution saying the section may not apply. **That sentence
is precisely the fossil §6.3 exists to prevent:** a governance document stating a rule nobody
enforces, which the next agent reads *instead of* the source.

### Decision

- `.project-profile` holds one word — `gcc` or `commercial`. `new_project.py --profile` **requires**
  the flag; there is no default, because a toggle that silently picks a side is not a toggle.
- **Documents are stripped, not annotated.** Profile-specific prose is fenced in HTML comments and
  the initializer removes the other side, marker lines included. Removed numbered sections have
  counterparts, so §4, §5 and §7 stay coherent.
- **The scanner reads the same file.** `GCC_BANNED_PATTERNS` applies only under `gcc`;
  `ALWAYS_BANNED_PATTERNS` applies everywhere. The enforced rule and the written rule cannot drift,
  because one value drives both.
- **No `.project-profile` means the template**, which keeps every block and enforces the **union** —
  fail-closed, and what lets the template carry law it does not impose on descendants.
- Marker balance is a gate. An unclosed marker swallows the rest of a file when stripped; a fixture
  demonstrates exactly that. Nesting and unknown profile names are refused too.

### Consequences

- **`--profile` is now required.** Any script or habit that called the initializer without it breaks,
  deliberately.
- Adding profile-specific law means adding a counterpart for every other profile, or the document
  loses a numbered section under one of them.
- A script that *explains* banned features necessarily names them. `project_profile.py` joins
  `EXCLUDE_FILES` for that reason; `CONTENT_RULES` still covers it, since `EXCLUDE_FILES` does not
  reach that channel.
- For consulting, one profile per engagement type is the natural extension, composing with the
  per-client identifiers in [[reference_content_provenance]].

### Verification

Two real projects were built from one template, one per profile. On `gcc`: §5 reads "GCC Portability
Requirements", the banned-features bullet is present, and `{"mode": "DirectLake"}` in a file exits 1.
On `commercial`: §5 reads "Portability Requirements", the commercial bullet replaces the banned one,
and the same file exits 0. Neither carries a leftover marker. Twelve in-memory fixtures cover
stripping, balance, nesting, unknown names, and the swallowed-tail failure.

### Enforcement

`scripts/project_profile.py`, `scripts/banned_feature_scan.py` (`active_banned_patterns()`),
`scripts/new_project.py` (`--profile`), `.pre-commit-config.yaml` (`project-profile-selftest`, then
`project-profile`). Taught by [[reference_project_profiles]].

---

## Decision 2026-09-21-001: Session closeout is a gate, and its artifacts live one session

**Amended 2026-09-24 (TMPL-5.2):** the wikilink rule the handoff linter applied to handoffs
alone now covers every text file git would commit: a `[[slug]]` that resolves to no knowledge
entry blocks the commit, with an allow set (`WIKILINK_ALLOW`) for the convention's own
placeholders and the slug the self-test fixtures use. Released MAJOR as `v9.0.0`, since a
project with a dangling link in any document now fails.

**Date:** 2026-09-21
**Made By:** Chair + AI
**Status:** APPROVED
**Resolves:** the handoff-versus-prompt conflation noted in a commit message in the archive repository's history (never logged)

### Context

The session end protocol (`CONSTITUTION.md` §2.2) is five prose steps. Nothing verifies that a
handoff was written, that sprint-status was updated, that learnings were flushed, or that the next
session has a prompt. The last session decided the kickoff prompt "is not a repo artifact at all and
is handed over as text". That put the next session's instructions in chat only, which is the failure
this repository exists to prevent. The same session left an open question in a commit message body
instead of this log. Both are the convention-instead-of-control shape already recorded twelve times.

Handoffs also accreted: the standard's own template carried durable rules and constraints, so a
handoff became a second knowledge base that nothing indexed and no gate watched.

### Decision

1. **Closeout is mechanical.** `scripts/session_closeout.py` verifies the closeout artifact set. Its
   `--check` mode runs on every commit; `--closeout` runs at session end and performs the rotation
   below; `--verify` runs at the next cold start and refuses build work if the previous session did
   not close out.
2. **Sessions are numbered.** `S1`, `S2`, … The pair `HANDOFF_S{N}.md` + `KICKOFF_S{N}.md` in
   `sprint/handoffs/` is written at the closeout of session N−1 and consumed by session N. The
   sprint-status entry for session N is headed `## S{N} — <date> — <title>`.
3. **Handoffs and kickoffs live one session.** Nothing may exist only in a handoff or kickoff that is
   needed beyond the session that consumes it. Durable facts go to the knowledge base, decisions to
   this log, work to the tracker; the handoff links to them. The templates have no section a durable
   rule could live in, and the linter rejects unknown headings.
4. **Rotation keeps two pairs.** At closeout the script moves every pair older than the consumed one
   into `sprint/handoffs/archive/`. The main folder holds at most two session numbers, consecutive:
   the pair this session consumed and the pair it produced. Archived files are never a mandatory
   read, so anything left only in one is lost by design.
5. **The kickoff prompt is a repo artifact and is standalone.** It names a persona, the cold start,
   a task list where every task cites a story ID present in the tracker, success criteria, and the
   closeout command. It is pasted verbatim into the next chat.
6. **Personas are shape-gated, not list-gated.** `docs/personas/<slug>.md` holds one persona each,
   with required frontmatter and sections. A kickoff names a persona by slug and copies its
   invocation block verbatim; the gate proves the slug exists and the copy matches. A persona is
   written when a task first needs it and registered in the same commit. No list is predicted.
7. **Pre-gate handoffs are archived as-is.** The handoff dated 2026-09-20 and the two `SAMPLE_`
   files predate the structure and are not linted; the samples are deleted because a linted template
   supersedes an unlinted example.
8. **The recovery handoff template is retired.** `sprint/recovery/templates/HANDOFF_TEMPLATE.md`
   competed with the standard for the same concern, which the authority matrix forbids. Recovery
   sessions use the standard handoff plus the validation-evidence template.

### Honest limit

The gate cannot read prose. It proves counts, sequence, structure, that every task cites a real
story, that every persona reference resolves, and that decision IDs and wikilinks resolve. It cannot
prove a sentence in a handoff was not durable. The rotation is what enforces that: a fact left only
in a handoff disappears from mandatory reads one session later.

### Consequences

- Adding this gate is MAJOR under [[reference_template_versioning]]: it fails a project whose
  handoff folder is unstructured. Released as `v4.0.0`.
- `session_handoff_standard` is rewritten as v2.0. The percentage ladder, the "Handoff Prompt
  Template" conflation, and the `HANDOFF_SESSION[N]` naming are removed.
- The initializer clears `sprint/handoffs/` including the archive. A new project starts at S1 with
  no incoming pair, which the gate accepts as a fresh project.

### Enforcement

`scripts/session_closeout.py` and `.pre-commit-config.yaml` (`session-closeout-selftest`,
`session-closeout-check`, and the manual-stage `session-closeout` / `session-verify`). Taught by
[[reference_session_closeout]].

---

## Decision 2026-09-22-001: CI is the backstop for per-clone hooks

**Amended 2026-09-25 (TMPL-1.5, under 2026-09-25-001):** the repository is public. Protection is
now available at no cost and is still not enabled: every checkpoint is a direct push to `main`,
and a required check would force a pull-request flow on one developer for a run that already
reports. The design below stands with its reason changed; the 2026-09-22 resolution of the open
question is superseded.
**Amended 2026-09-22:** the repository stays private and branch protection is not pursued.
The workflow is a reporting backstop; the local hooks are the blocking control. The open question
below is resolved accordingly, and the operator command was removed from the knowledge entry.
**Amended 2026-09-23 (TMPL-5.1):** "a new stage added later needs a matching step in the
same work unit" is now a control: `gate_runbook_scan.py` fails any non-manual stage the config
declares that no workflow step runs, and a missing or unreadable workflow. Released MAJOR as
`v8.0.0`, since a project that added a stage without a step now fails.

**Date:** 2026-09-22
**Made By:** Chair + AI
**Status:** APPROVED

### Context

Every gate in this repository is a git hook, and git hooks are per-clone. A clone that never ran
`pre-commit install --hook-type pre-commit --hook-type commit-msg` commits with no gate at all, and
no file in the repository can detect that (decision 2026-09-20-001 recorded the problem for the
commit-msg stage; it applies to every stage). The suite was therefore only as strong as the last
operator's memory of the install command.

### Decision

- `.github/workflows/gates.yml` runs the full pre-commit-stage suite on every push and pull request,
  and runs the commit-msg gate over every commit the event carries. Same scripts, same config; the
  clone's hook state does not matter.
- Branch protection is not part of the design. It needs GitHub Pro or a public repository; this one
  stays private, and with one developer the blocking value is low. A red run is a report acted on in
  the same session.
- The check is proved in both directions before it is trusted: a commit from a clone with no hooks,
  carrying a violation, turned the run red; the same tree without it turned green.

### Consequences

- A push that fails locally-uninstalled gates now fails on GitHub instead of landing. The first such
  failure in a derived project is expected, not alarming: it is the backstop doing its job.
- **The workflow reports; it does not refuse.** GitHub returned 403 on branch protection: it
  requires GitHub Pro or a public repository, the same plan limit decision 2026-09-20-008 recorded
  for secret scanning. The local hooks remain the only blocking control, and the workflow is the
  visible audit of what they would have caught.
- No branch-and-pull-request convention is imposed. Without enforcement it would be exactly the
  written-rule-as-control shape this repository keeps removing.
- GitHub Actions minutes on a private repository are metered against the free monthly allowance;
  a run of this suite takes about two minutes.

### Open question

- ~~Should this repository be made public so branch protection can be enabled?~~ **RESOLVED
  2026-09-22:** no. The operator is not comfortable publishing the history, and with one
  developer branch protection is not urgent. If that changes, GitHub Pro enables protection on
  private repositories without publishing anything.
- The template-version gate needs the full history, so checkout runs with `fetch-depth: 0`.
- `pre-commit run --all-files` in CI does not cover the commit-msg stage; the workflow's second step
  exists for that reason, and a new stage added later needs a matching step in the same work unit.
- MINOR under [[reference_template_versioning]]: adopting it forces no one to act, and it cannot
  fail content the local suite already passes.

### Enforcement

`.github/workflows/gates.yml`. Taught by [[reference_ci_backstop]].

---

## Decision 2026-09-22-002: What the first derived project found, and the three fixes

**Date:** 2026-09-22
**Made By:** Chair + AI
**Status:** APPROVED

### Context

TMPL-2.3 created a real private repository from the template on GitHub (the derived probe),
initialized it on the `commercial` profile, installed both hook types, pushed, and ran its S1 to
closeout. Three defects surfaced, none of them visible from inside the template because each needs
either a tag push or a second repository to appear.

1. **The template's release run went red.** Pushing `v4.1.0` with `--follow-tags` produced two
   `gates` runs; the tag-triggered one failed the version gate with "annotation does not name
   MAJOR, MINOR or PATCH: 'release: v4.1.0'". The checkout log shows why: `actions/checkout`
   re-fetches the pushed ref as `+<sha>:refs/tags/v4.1.0` with `--no-tags`, which replaces the
   annotated tag with a lightweight one. `%(contents:subject)` on a lightweight tag is the commit
   subject. The gate then told the reader to re-annotate a tag that was annotated all along.
2. **The derived tracker was the template's tracker.** The initializer filled one token in
   `sprint/story-tracker.md` and left the `TMPL-1` and `TMPL-2` epics in place, so the new project
   started with ten stories, eight done, none its own, and Summary Statistics that described the
   template's backlog. Sprint-status was already regenerated for the same reason; the tracker was not.
3. **The clone's remote used the wrong ssh host.** `gh repo create --clone` writes
   `git@github.com:…`; on a machine that separates identities by ssh host alias there is no
   `Host github.com` block, so the first push would have used no personal key. Environment-shaped,
   but the guide names the command, so the entry that teaches it names the follow-up.

### Decision

- **The workflow restores the real tag objects** with `git fetch --force --tags origin` after
  checkout. The tag-push event is the one that exists to verify a tag, so it must see the tag as
  pushed. The trigger is left as `on: push` for every ref; a release costs one duplicate run.
- **The version gate distinguishes a lightweight tag** (`%(objecttype)` is `commit`, not `tag`)
  and reports it as `lightweight-tag` with a fix that names both causes, instead of printing the
  commit subject as a missing bump type. The rule applies exactly where a bump must be named: every
  tag but the earliest, which has no predecessor and so needs no annotation. The per-tag rules are
  a pure function, `judge()`, with seven fixtures; the lightweight fixture was run against the
  previous code in a scratch clone, which reported `no-bump-type` with the commit subject, as
  GitHub did.
- **The initializer regenerates the tracker** from a skeleton with the `[EXAMPLE]` epic and zero
  statistics, exactly as it regenerates sprint-status. The fixture judges the skeleton with the
  state gate's own `tracker_counts()` and `tracker_violations()`: no real story ID, and counts that
  reconcile. A skeleton that still carried the `TMPL` epics fails it.
- **The release is a PATCH (`v4.1.1`).** Adopting it forces no one to act: a derived project with
  its own tags either has none (the gate skips) or had already to pass the bump-type rule on every
  tag but the earliest, and a lightweight tag could pass that rule only if its commit subject
  happened to contain MAJOR, MINOR or PATCH.

### What worked without change, observed

The GitHub-side "Initial commit" triggers a `gates` run before the initializer has run; it was
green, since the template tree passes its own suite. The initializer's dry run and apply matched.
`session-verify` passed at S1 with no incoming pair. The attribution gate refused a
`Co-Authored-By` trailer in the derived clone before the first real commit. The first push's
`gates` run was green. Profile stripping left no marker in any of the four documents.

### Enforcement

`.github/workflows/gates.yml` (the fetch step), `scripts/template_version.py` (`judge`,
`lightweight-tag`, `--self-test`), `scripts/new_project.py` (`story_tracker_skeleton`,
`--self-test`). Taught by [[reference_ci_annotated_tags]] and [[reference_derived_project_start]].

---

## Decision 2026-09-22-003: The closeout command runs with `--all-files`

**Date:** 2026-09-22; amended 2026-10-22
**Made By:** Chair + AI
**Status:** APPROVED

### Amendment 2026-10-22: the verify carries the flag too

The bullet below that left `session-verify` unchanged reasoned that a gate requiring a clean tree
leaves nothing to stash. That is circular: the stash runs before the gate, and an unstaged edit to
a tracked file is exactly what it hides. Measured in S2 on a clone at the S1 closeout commit: clean,
`pre-commit run session-verify --hook-stage manual` passed; with one unstaged edit to `README.md`
the same command printed "Stashing unstaged files" and **passed**; with `--all-files` it failed on
`dirty-tree`. Unlike the closeout case this is a hidden green, not a confusing red: the cold start's
proof that the previous session committed its work passed while work sat uncommitted. A staged edit
was caught either way, since `git status` still lists it under the stash.

`VERIFY_COMMAND` in `scripts/session_closeout.py` is now
`pre-commit run session-verify --hook-stage manual --all-files`; the kickoff scaffold writes it,
and `AGENTS.md`, the handoff standard §5, the gate runbook and the hook comment name this form. The
`SessionStart` hook built in TMPL-1.2 runs it the same way. A kickoff written before the amendment
is not refused; the linter checks section 2 for `AGENTS.md` and the handoff, as before.

### Context

The derived project's S1 closeout ran the documented command, `pre-commit run session-closeout
--hook-stage manual`, with the tracker and sprint-status edited but not yet staged. pre-commit
printed "Unstaged files detected. Stashing unstaged files", ran the hook, and the gate reported
that the kickoff's two stories were not in the tracker. They were in the tracker on disk; the gate
had read the last commit's tracker, because pre-commit stashes unstaged changes to tracked files
before running any hook invoked without `--all-files` or `--files`. The new pair, being untracked,
was not stashed, which is why the gate saw the kickoff and not the stories it cited.

Measured both ways on the same tree with one unstaged edit: without the flag pre-commit stashes;
with `--all-files` it does not. The hook declares `pass_filenames: false` and `always_run: true`,
so the flag changes nothing about what the gate checks, only whether the tree it checks is the
one on disk.

The gate cannot detect that it ran under a stash: the working tree is simply the index, and the
patch files pre-commit writes to its cache persist after restore, so their presence proves nothing.

### Decision

- `CLOSEOUT_COMMAND` is `pre-commit run session-closeout --hook-stage manual --all-files`. The
  scaffold writes it into every kickoff's section 5, and every document that names the command
  names this form. The linter keeps checking for `session-closeout` only, so kickoffs written
  before this decision still pass.
- The scaffold's closeout paragraph also names the push, the `gates` run to confirm, and the
  hand-over of the next kickoff, matching `session_handoff_standard_v2.0.md` §7 steps 6 and 7,
  which the previous text stopped short of.
- `session-verify` is unchanged: it requires a clean tree, so there is nothing to stash.
  (Wrong; see the amendment above.)
- The initializer's S1 sprint-status entry says that its "Next" list stands in for the kickoff S1
  does not have, and that S1 must open an epic before the S2 kickoff can cite a story.

### Honest limit

The failure mode is a spurious failure, not a spurious pass: the stashed files are exactly the ones
that carry the session number and the story IDs, so a stale read produces a violation, and the
per-commit `--check` judges the staged tree regardless. The flag removes a confusing red, not a
hidden green. It is still worth a decision because the confusion sends the reader to fix a tracker
that is already correct.

### Enforcement

`scripts/session_closeout.py` (`CLOSEOUT_COMMAND`, the kickoff scaffold), `.pre-commit-config.yaml`
(the hook comment), `CONSTITUTION.md` §2.2, `README.md`, `TEMPLATE_GUIDE.md`,
`docs/standards/session_handoff_standard_v2.0.md` §5 and §7. Taught by [[reference_precommit_stash]].

---

## Decision 2026-09-22-004: A derived project takes a newer release through an updater

**Date:** 2026-09-22; amended 2026-09-24 (TMPL-4.1: the decision log is kept, the framework decisions file is what is merged by ID)
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`gh repo create --template` squashes history, so a derived project shares no commit with the
template: `git merge` has no base, and `git pull` has nothing to pull. The first derived project
(decision 2026-09-22-002) was told in its second kickoff which files to copy, one by
one, and which decision to append so the freshness gate would accept the new knowledge entries.
That is a checklist, and this repository converts checklists into controls.

Two harder questions sat underneath. What does the template own in a project after birth, given
that the initializer fills some files, regenerates others, strips a profile from the documents
and never touches the decision log or knowledge base? And how does a framework decision reach a
project's decision log, which is the project's append-only record, without rewriting it?

### Decision

- **`scripts/template_update.py` carries a project from its `.template-version` to a named
  release.** It fetches both releases from `--source` into `refs/template/<version>`, outside
  `refs/tags/` so the version gate never sees them, and judges every path in either tree.
- **Ownership is decided by path and is the initializer's inverse.** `keep`: `sprint/` except
  the decision log, `.project-profile`, and the content folders shipped empty; never written.
  `merge`: the knowledge INDEX by slug and the decision log by decision ID; project rows are
  never touched. `three-way`: everything else, through `git merge-file` over the previous
  release, the project's copy and the target. A fixture reads `new_project.py`'s
  `REGENERATE_FILES`, `CLEAR_GLOBS`, `FILL_FILES` and `NEVER_RESET` and checks the map against
  them.
- **One mechanism for files, not two.** Overwriting "template-owned" paths was rejected because
  they are legitimately edited (`TEMPLATE_GUIDE.md` Step 5 adds patterns to the scanner; the
  standards carry tokens the project fills). For an unedited copy the merge reduces to overwrite.
- **The decision log is inserted into, never rewritten.** A framework decision the log lacks
  gets its index row at the top of the table and its body appended at the end, because the
  framework's entries `teaches:` it. An existing row or body changes only when it still equals
  the previous release's; an edited one is reported and left. Nothing is removed. `[EXAMPLE]`
  rows and bodies never travel. This is the answer to the question an earlier kickoff reserved for
  the operator: the design does not rewrite a derived log, it appends to it, and the dry run
  shows every insertion before `--apply`.
- **Template markdown is stripped to the project's profile before comparison and before
  writing**, as at birth. Without it every document with a profile block reads as edited.
- **The target release's copy of the script runs.** The map lives in the file, so the run
  compares the executing file with the target's blob and refuses with the two commands that
  fetch it. A target that predates the updater is accepted with a note.
- **The stamp is written last and withheld on a conflict.** A conflict leaves the file alone and
  names the diff; `--keep <path>` or `--take <path>` settles it on the re-run. `--apply` refuses
  a dirty tree (the updater itself excepted, since first adoption fetches it untracked) so the
  review afterwards is one `git diff`, and then runs the full suite.
- **MINOR (`v4.2.0`)** under [[reference_template_versioning]]: an opt-in script and a self-test
  hook, which cannot fail a project's content.

**Amended 2026-09-24 (TMPL-4.1, under 2026-09-23-003):** the framework decisions live in
`docs/governance/framework_decisions.md`, and that file is the one merged by decision ID, rows and
bodies, with the rules above unchanged. `sprint/decision-log.md` is kept with the rest of
`sprint/`: the updater never writes it again, so the project's append-only record is the project's
alone. A project that took a release before `v11.0.0` keeps the framework rows the old insertion
put in its log; the freshness gate reads both indexes as one set and lets the framework file win
the duplicate IDs ([[reference_framework_decisions]]).

### Verification

Thirty in-memory fixtures. Six deliberately broken variants were run against them in a scratch
harness before the suite was trusted: inserts at the table's end, no profile stripping,
both-sides-changed silently taking the template, `[EXAMPLE]` rows treated as decisions,
conflicts reported clean, and bodies read to end of file. Each failed between one and six
fixtures. On the derived probe, from the archive repository's `v4.1.0` to its `v4.1.2`: the dry run planned 14 updates, 3
additions and 3 merges; `CONSTITUTION.md` merged cleanly across the project's token fill and
profile strip; the two decisions arrived with bodies; `--apply` ran the suite green; the push's
`gates` run was observed.

### Enforcement

`scripts/template_update.py` (`classify`, `verdict`, `merge_rows`, `merge_decisions`,
`--self-test`), `.pre-commit-config.yaml` (`template-update-selftest`), `TEMPLATE_GUIDE.md`
Step 9. Taught by [[reference_template_update]].

---

## Decision 2026-09-23-001: The gate suite is described by a runbook the config verifies

**Date:** 2026-09-23
**Made By:** Chair + AI
**Status:** APPROVED

### Context

`TEMPLATE_GUIDE.md` Step 6 carried a hand-written table of the gates. It was keyed by script
rather than by hook id, named no stage, and by the time it was replaced it already lacked the
updater's self-test added one session earlier. Nothing compared it to `.pre-commit-config.yaml`.
A page that describes the suite is what the next reader consults instead of the config, so a
stale one is the fossil `CONSTITUTION.md` §6.3 exists to catch, in the one place that claims to
be the map. The operator asked for a runbook: one section per hook, in run order, its stage, the
self-test it pairs with, what it blocks, why, and how to run it alone.

Two questions sat underneath. Where does the page live so the updater carries it to derived
projects, given that `classify()` keeps `docs/runbooks/` and three-way merges `docs/governance/`?
And what bump does a check that reads a project's config and page deserve?

### Decision

- **The page is `docs/governance/gate_suite_runbook.md`.** `docs/runbooks/` is project-owned by
  the updater's map: it holds the project's operational procedures and the template never writes
  there, so a page that must track the template's own hook config cannot live in it. Governance is
  where the compliance policy's enforcement belongs, beside the document-control standard. The
  three-way merge is the right mechanism, not a limitation: a project that adds a hook to its
  config must add a section, and the merge lets both sides edit the page.
- **Every H2 on the page is a hook id**, spelled as `id:` spells it, in the config's order. Prose
  that is not about one hook sits above the first H2. Each section carries a `**Stage:**` line.
  What a section says a gate blocks, and why, links the decision and the knowledge entry and does
  not restate them.
- **`scripts/gate_runbook_scan.py` is the control.** It reads the hook ids from the config with a
  YAML parser, every repo included, and the sections from the page outside fenced code. It fails
  on a hook with no section, a section naming no hook, sections out of run order, a stage line
  missing or disagreeing with the hook's `stages:`, and a config that cannot be parsed or holds no
  hooks, which is never read as an empty suite. Wired as `gate-runbook-selftest` then
  `gate-runbook`, `stages: [pre-commit]`, with `additional_dependencies: [pyyaml]`; exit 2, never
  0, without the parser.
- **A hook without `stages:` is a violation.** Decision 2026-09-20-001 required an explicit
  `stages:` on every hook and enforced it by prose. The stage line on the page can only be checked
  against a declared stage, so the check refuses a hook that declares none. The written rule is
  now a control.
- **MAJOR, released as `v5.0.0`.** Under [[reference_template_versioning]] the question is whether
  adopting it forces a human to act. It does, in content a project can already have: a hook the
  project added to its config (the config is three-way merged, and adding a hook is a supported
  edit) has no section until someone writes one, and a project hook declared without `stages:`
  fails outright. For a project that never edited the config the updater carries the page and the
  config together and the gate passes, which is the common case; but the bump is judged by the
  case it can fail, and the tiebreaker goes up. `TMPL-2.7` takes the probe to `v5.0.0` to observe
  which case it is.

### Honest limit

The check cannot read prose. It proves the page's shape follows the config: nothing listed that
does not exist, nothing that exists left out, the run order, and the stage a reader will pass to
`--hook-stage`. Whether a section's account of what a gate blocks is still true is the author's to
keep, and the linked decision is the source when they disagree.

### Verification

Fifteen in-memory fixtures. Six deliberately broken variants were run against them in a scratch
harness before the suite was trusted: H2s inside fenced code counted as sections, the order rule
removed, stage disagreements ignored, only the first repo's hooks read, an unreadable config read
as zero hooks, and a hook without `stages:` accepted. Each failed between one and ten fixtures.
Live, by exit code: a scratch config with an extra hook id exited 1 on `no-section`; a scratch
page with an extra section exited 1 on `no-hook`; a page with the two manual-stage hooks
relabelled `pre-commit` exited 1 on `stage` twice; a config with the attribution hook's `stages:`
removed exited 1 on `no-stages`. The real tree: 22 hooks, 0 violations.

### Enforcement

`scripts/gate_runbook_scan.py` and `.pre-commit-config.yaml` (`gate-runbook-selftest`, then
`gate-runbook`). `TEMPLATE_GUIDE.md` Step 6 links to the page and holds no table. Taught by
[[reference_gate_runbook]].

---

## Decision 2026-09-23-002: `dev-resources` is the durable home for personas and reference knowledge

**Date:** 2026-09-23
**Made By:** Chair + AI
**Status:** APPROVED; SUPERSEDED (personas and shared knowledge in dev-resources) by 2026-10-23-003

### Context

The persona registry lives in `docs/personas/` of every project. The initializer preserves it at
birth and the updater three-way merges it, so a template release reaches every project; nothing
travels the other way. A persona written in a project stays there, and the template never sees
it, so each clone is only as good as the registry it started with. The same holds for reference
knowledge that is not specific to one project. The operator's aspiration: one repository whose
registry and reference documents grow from every project and reach every project.

`dev-handbook` already existed for that purpose in miniature: a README, one runbook, and a copy
of the attribution gate that its README names as a known duplication. It was renamed
`dev-resources` on GitHub and locally on 2026-09-23, keeping its history and the redirect.

### Decision

- **The project holds a synced snapshot, never a pointer.** The session gate proves a kickoff's
  persona block equals the registry file, and CI reads local files, so the registry must be in
  the tree. `dev-resources` is the source; the project's copy is a cache refreshed mechanically,
  which is the repository's own single-source-of-truth law one level up.
- **Sync is a script in the updater's idiom, not a submodule or subtree.** `scripts/resources_sync.py`
  fetches `dev-resources` into `refs/resources/<ref>`, compares blobs, writes, reports, and stamps
  `.resources-version`. Submodules are not initialized by `gh repo create --template` and need a
  checkout flag in CI; a subtree is a second merge channel over the same paths as the updater.
- **Ownership is disjoint.** `dev-resources` owns `docs/personas/` and knowledge entries that
  declare `source: dev-resources` in their frontmatter; the updater's map marks those paths
  `keep`, so only the sync writes them. The template keeps everything version-locked to its own
  config, the gate-suite runbook above all, since `gate-runbook` proves that page against the
  config the project actually has. Resource knowledge entries carry `teaches: []`.
- **Sync runs at closeout, never at cold start.** The produced kickoff is scaffolded from the
  registry as just synced; the consumed kickoff matches the registry as it was at its scaffold.
  A mid-session sync is the only way the two can disagree, and the gate then fails loudly.
- **Personas are append-only.** A persona is added when a task first needs one, as now. An
  Invocation never changes in place: an enhancement bumps `version:` in the frontmatter and
  appends a changelog line, and the persona linter refuses an Invocation change without the bump.
  The kickoff names the version it was written against.
- **Contribution is gated.** At closeout, a persona in the local registry that the fetched
  `dev-resources` ref lacks is a violation; the sync's `--publish` writes it into the local clone
  of `dev-resources` for commit and push. The registry grows only through that path.
- **The template publishes `.pre-commit-hooks.yaml`** so `dev-resources` consumes the persona
  linter, the frontmatter gate, the attribution gate and gitleaks as a hook repository pinned by
  `rev`, replacing the copied script. A registry with no linter is not a registry.

### Consequences

- Epic TMPL-3, four stories, in this order: the published hooks, the append-only rule, the sync
  script with the ownership split and the closeout check, then the move and the proof on the probe.
- Adopting the sync is MAJOR under [[reference_template_versioning]]: the closeout gains a check a
  project must satisfy, and the persona linter gains a required key.
- `dev-resources` becomes a gated repository. Its README's own rule, "prose, not code", still
  holds for its content; the gates it runs are the template's, consumed, not copied.

### Enforcement

To be built: `scripts/resources_sync.py`, the version rule in `session_closeout.lint_persona`,
`.pre-commit-hooks.yaml`, and the `keep` prefixes in `template_update.classify`.

---

## Decision 2026-09-23-003: A pristine `v1.0.0` from a fresh init, with the build history archived

**Date:** 2026-09-23; amended 2026-09-24 (the decisions move built, its enforcement and bump named; the sanitizer built and the sweep done; the archive repository named; the cut done)
**Made By:** Chair + AI
**Status:** APPROVED

### Context

The template carries six sessions of its own construction: sprint-status entries, the `TMPL`
epics, handoff pairs and their archive, and decision bodies that read as a build diary. A
project created from it inherits none of the sprint state, because the initializer regenerates
or clears it, but the template itself is not the pristine artifact the operator wants to clone
from. The operator asked for a sanitized `1.0.0` and for the completed, unsanitized repository
to be kept for reference.

One dependency makes a naive reset break the first commit: every knowledge entry declares
`teaches: [<decision-id>]` and the freshness gate refuses an ID absent from
`sprint/decision-log.md`. The initializer records this as the reason it never clears the log.

### Decision

- **Framework decisions move to `docs/governance/framework_decisions.md`**, same index-and-bodies
  structure, IDs unchanged. The freshness gate and the session gate read both logs. The updater
  merges the framework file by ID instead of inserting into a project's append-only log, which
  removes the least comfortable part of 2026-09-22-004. `sprint/decision-log.md` starts with the
  `[EXAMPLE]` row only. Docstrings that cite decision IDs stay correct.
- **The sanitizer is the initializer's machinery without the fill.** `scripts/sanitize_template.py`
  regenerates sprint-status with the template's own S1 entry, regenerates the tracker, clears the
  handoffs and the sprint archive, keeps every token and both profile blocks, writes no
  `.project-profile`, and runs the suite. Its `--check` fails while build state remains: an
  `S<N>` above 1, a `TMPL-` story, the sprint archive, the probe's name.
- **The sweep is by hand.** Knowledge entries and decision bodies keep their learnings and lose
  incidental session numbers, probe references and commit hashes; where history matters, the
  citation names the archive repository.
- **Ten tags cannot be retagged `v1.0.0`**, because the version gate verifies every tag. So: this
  repository is renamed to an archive name, given a final tag, and archived read-only on GitHub.
  The sanitized tree starts from a fresh `git init` as `agentic-dev-template`, as 2026-09-19-001
  did for the employer split, with `TEMPLATE_VERSION` set to `v1.0.0`, committed, then tagged.
  The version gate exempts the earliest tag from the bump rule. Keeping the name keeps the
  initializer's self-refusal and the guide's URLs correct.
- **Proof before the cut.** The sanitized tree is produced on a scratch clone first; a derived
  project is created from it, initialized, and its S1 verified, before anything is archived.
- **Order.** After epic TMPL-3, because the resources that move out must move before the
  sanitize, and the framework-decisions move is what the sync's `teaches: []` rule relies on.

**Amended 2026-09-24 (TMPL-4.2):** the archive repository is `SaltyBrett/agentic-dev-template-archive`, the name a
citation uses where the build history matters; TMPL-4.4 renames this repository to it. The
sweep left the session numbers that are the numbering convention itself (a fresh project at S1,
the S2 kickoff) and every `TMPL-` story ID a decision cites, since the check reads the tracker's
rows alone. `.resources-version` stays through the reset: it is the template's sync state, read by
the closeout's persona rule, not session state. MINOR for the sanitizer: an opt-in script and a
self-test that reads nothing from a project's tree.

**Amended 2026-09-24 (TMPL-4.4):** the cut is done. The sanitize check named nothing outside the
files the reset clears, so no further sweep preceded it. This repository was renamed to
`SaltyBrett/agentic-dev-template-archive` on GitHub, the sanitizer ran in the local clone while
its origin still named the template, the tracked files of the reset were copied to a fresh
directory, and `SaltyBrett/agentic-dev-template` was created empty and received `release: v1.0.0`
as its first commit, tagged `v1.0.0` with an annotation naming MAJOR and the archive; both of its
`gates` runs were read green before this amendment was written. The order that matters, and the
one hazard met, are taught by [[reference_pristine_cut]]: the old clone's origin is switched to
the archive name before the new repository takes the old one, because GitHub's redirect from the
old name lasts only until it is reused. The record of the cut, this amendment and that entry, is
carried into the new lineage as a commit after its tag, so `v1.0.0` is the sanitized tree alone.
The archive's final tag is a PATCH whose annotation names `v1.0.0` and the new repository; the
derived probe repository is left to the operator, retired or restamped, as the consequences say.

### Consequences

- Epic TMPL-4, four stories: the decisions move, the sanitizer and sweep, the scratch proof,
  the archive and the fresh init.
- The derived probe repository belongs to the archived lineage; its `.template-version` names
  tags the new repository does not have. It is retired with the archive or restamped by hand.
- The new lineage's first MAJOR is `v1.0.0`; the archive's last tag records where it came from.

### Bump

The decisions move (TMPL-4.1) is MAJOR, released as `v11.0.0`: a project adopting it receives a
new file the gates read, and its own log stops receiving framework decisions. The sanitizer and
the fresh init (TMPL-4.2 to TMPL-4.4) are the new lineage's `v1.0.0`.

### Enforcement

Built (TMPL-4.1): `kb_freshness_scan.parse_logs` and `log_texts` read
`sprint/decision-log.md` and `docs/governance/framework_decisions.md` as one set, an index missing
from either raising with the log's name, the framework file winning a duplicate ID;
`session_closeout.decision_ids` reads the same set; `template_update.MERGE` names the framework
file and the project's log falls under `sprint/`, kept; `new_project.NEVER_RESET` names the
framework file and the initializer's fixture keeps it out of every mutating list; the template's
own `sprint/decision-log.md` holds the `[EXAMPLE]` entry alone. Taught by
[[reference_framework_decisions]] and [[reference_template_update]]. Built (TMPL-4.2):
`scripts/sanitize_template.py`, whose `--check` names every sprint-status entry above S1, every
`TMPL-` story row, every file in `sprint/archive/` and `sprint/handoffs/archive/`, every pair in
`sprint/handoffs/` and the probe repository's name in any text file git would commit, the script
itself excepted; whose `--apply` is the initializer's regenerate-and-clear with no fill, no profile
strip and no `.project-profile`, followed by the suite; which refuses to run where `origin` is not
the template. `sanitize-template-selftest` runs on every commit, `sanitize-template-check` at the
manual stage, because this repository fails it until the cut. Taught by
[[reference_template_sanitizer]]. Done (TMPL-4.3, TMPL-4.4): the scratch proof, then the cut,
whose order and hazard are taught by [[reference_pristine_cut]].

---

## Decision 2026-09-23-004: Commit classification is not built; the bump stays a judgement

**Date:** 2026-09-23
**Made By:** AI, under the kickoff's instruction to decide TMPL-2.2 rather than defer it
**Status:** APPROVED
**Closes:** TMPL-2.2, opened under 2026-09-20-006 and carried through four sessions

### Context

Decision 2026-09-20-006 gated the release mechanics and left the bump type a documented judgement.
TMPL-2.2 proposed removing the judgement: type every commit at `commit-msg` time and have
`--release` compute the bump as the highest type in the window since the last tag.
[[reference_commit_classification]] recorded the constraints before the work was attempted:
the hook fires on merge commits, an all-exempt window must fail rather than default to PATCH,
`checkpoint:` is most of the history and cannot simply be exempt, and the policy itself is not
up for revision. Every session since then recorded the same observation in its sprint-status
entry: the commits since the last tag were few and were classified from the log without effort.

Measured on 2026-09-23, the commits between consecutive tags of the archive repository:

| Window | Commits |
|---|---|
| `v1.0.0`..`v1.1.0`, `v1.1.0`..`v2.0.0`, `v2.0.0`..`v3.0.0` | 1 each |
| `v3.0.0`..`v4.0.0` | 10 |
| `v4.0.0`..`v4.1.0` | 5 |
| `v4.1.0`..`v4.1.1`, `v4.1.1`..`v4.1.2` | 2 each |
| `v4.1.2`..`v4.2.0` | 4 |
| `v4.2.0`..`v5.0.0` | 3 |

And every change that moved the version was introduced by a decision whose body names the bump
and its reason (`2026-09-22-002` PATCH, `2026-09-22-004` MINOR, `2026-09-23-001` MAJOR, and so
on back to `2026-09-20-008`). The judgement is already made when the change is fresh. It is
recorded in the decision log, which the freshness gate keys every teaching document to, not in
the commit message, which nothing reads back.

### Decision

**Won't do.** TMPL-2.2 closes. The release bump remains the judgement of 2026-09-20-006, made at
release time from the decisions logged since the last tag, and named in the tag annotation the
version gate verifies.

### The recommendation and its cost, as the kickoff asked

The mechanism would cost the operator a type on every commit in every repository that carries
the `commit-msg` hook, which after TMPL-3.1 includes `dev-resources` and every derived project,
because the hook is one script and the config is three-way merged. It would also need a decided
and verified treatment for merge, revert, squash and amend, and a rule mapping `checkpoint:` to
a type. What it would buy is the automation of a decision that takes one reading of a window
that has held between one and ten commits, over ten releases, and whose answer is already
written in the decision that introduced the change. The gate that matters, that the tag names a
bump and its commit carries the version, already exists. Automating the remaining judgement
would cost more than the judgement.

### What would reopen this

A release window that grows past what one reading covers, or a second maintainer whose
classification disagrees with the first. Either is visible in the sprint-status entry that
precedes a release, which is where every session so far has recorded the count. The constraints
in [[reference_commit_classification]] stand for that day.

### Enforcement

None is added. `scripts/template_version.py` continues to verify the tag, the version constant
and the annotation's bump word. Taught by [[reference_commit_classification]] and
[[reference_template_versioning]].

---

## Decision 2026-09-23-005: The template is a pre-commit hook repository

**Amended 2026-09-23 (same session):** the consequence on consumer access first claimed
that the keychain credential served the https URL locally. It did not; the check that said so
read the exit code of a pipe. What holds is below: ssh from the directory pre-commit clones into.
**Amended 2026-09-23 (with the operator):** the open question is resolved; the
template stays private and `dev-resources` runs its gates as local hooks only.
**Amended 2026-09-25 (under 2026-09-25-001):** the template is public; `dev-resources` pins the
plain https URL and has a `gates` workflow. The ssh-alias reasoning below stays as the record of
what a private hook repository costs a consumer; the open question's resolution is superseded.

**Date:** 2026-09-23; amended 2026-09-23; amended 2026-09-25
**Made By:** Chair + AI (the design in 2026-09-23-002; the mechanics decided here)
**Status:** APPROVED
**Builds:** the last bullet of 2026-09-23-002 (TMPL-3.1)

### Context

`dev-resources` carried a copy of `commit_attribution_scan.py` because the template published
no `.pre-commit-hooks.yaml`, and its README named the duplication. Decision 2026-09-23-002 made
the template publish one, so that repository consumes the persona linter, the frontmatter gate
and the attribution gate pinned by `rev`, with gitleaks from its own repository as here.

Publishing turned up three mechanics the design had not named. pre-commit installs a
`language: python` hook repository with `pip install .`, so the repository must be a package.
A remote hook runs from the consuming repository's root, so an `entry:` naming a path under
`scripts/` resolves to nothing there; the entry must be a console script. And every gate derived its
repository root from `__file__`, which inside pre-commit's virtualenv is a `site-packages`
directory: the persona linter would have judged the virtualenv.

### Decision

- **`pyproject.toml` makes the four modules the manifest needs installable**, flat from
  `scripts/`, with console scripts `session-closeout`, `kb-frontmatter-scan` and
  `commit-attribution-scan`. Its version is read from `new_project.TEMPLATE_VERSION`, the one
  value the tag gate verifies, so no second version is maintained by hand. `pyyaml` is a package
  dependency, so consumers declare nothing.
- **`.pre-commit-hooks.yaml` publishes three hooks:** `persona-lint` (`session-closeout
  --personas`, a new mode that runs the persona rule of `--check` alone), `kb-frontmatter-scan`
  and `commit-attribution`. Every hook declares `stages:` (2026-09-20-001). The two content
  gates carry `files:` for the paths they judge, so a consumer without that content shows them
  Skipped rather than passing over nothing; the attribution gate is `always_run`.
- **gitleaks is not re-published.** A manifest publishes only hooks that live in its repository;
  a consumer takes gitleaks from upstream with an explicit `stages:`, as this config does.
- **The published gates read their root from `git rev-parse --show-toplevel`**, falling back to
  the working directory, in `session_closeout.py` and `kb_frontmatter_scan.py`. pre-commit runs
  every hook from the consuming repository's root, and the documented direct invocations run
  from it too. The unpublished scripts keep `__file__`; they only ever run from `scripts/`.
- **A project is not a hook repository.** `new_project.TEMPLATE_ONLY` removes `pyproject.toml`
  and `.pre-commit-hooks.yaml` at birth, and `template_update.KEEP` never writes them: a Python
  project has a `pyproject.toml` of its own, and the updater's three-way merge would have
  conflicted on it at every release. The updater's fixture cross-checks the two lists.
- **MINOR, released as `v5.1.0`** under [[reference_template_versioning]]. No hook is added to
  the config, no command changes, and a project on the previous release adopts nothing; two
  files leave a new project at birth, which an existing project never had in use.

### Consequences

- The template is private, so a consumer needs read access to clone it, and pre-commit clones
  into `~/.cache/pre-commit`, which no per-directory git config reaches: the `includeIf` that
  rewrites plain ssh URLs to the personal identity inside `~/code/personal` does not apply
  there, and the keychain holds no https credential for github.com. Measured from that
  directory: https refused for want of a username; plain ssh accepted by whichever agent key
  GitHub recognized first, which the operator's environment runbook names as the wrong-identity
  failure; the `github.com-personal` alias accepted deterministically. `dev-resources` pins the
  alias URL. A GitHub Actions run in the consumer needs a deploy key or token secret, or a
  public template; `dev-resources` runs the gates as local hooks only until that is decided.
- A consumer keeps the template's layout for what these gates judge: `docs/personas/` and
  `docs/orchestration/knowledge/` with its `INDEX.md`. TMPL-3.4 moves the registry and the
  resource entries into `dev-resources` under those paths.
- `--personas` passes on a repository with no registry, with the count in its heading. The
  manifest's `files:` keeps that case from presenting as a run.

### Open question

- ~~Should `dev-resources` get a `gates` workflow, and if so how does it read the private
  template: a deploy key or fine-grained token stored as a repository secret, or the template
  made public?~~ **RESOLVED 2026-09-23 (with the operator):** the
  template stays private, including the sanitized lineage TMPL-4.4 will start. `dev-resources`
  gets no `gates` workflow: it has one clone with both hook types installed and proved, and a CI
  run there would duplicate what the local hooks already block while adding a secret to rotate.
  If a workflow is ever wanted, the credential is a read-only deploy key scoped to the template,
  never a token that expires, and the job recreates the `github.com-personal` ssh alias the
  pinned URL names.

### Verification

`pip install .` into a scratch virtualenv reported version `5.0.0` from the constant and the
three console scripts. Run from inside `dev-resources`, the installed scripts judged that tree:
no registry, no knowledge base, the attribution gate refusing a trailer (exit 1) and passing a
clean message (exit 0). A persona lacking `description:` and the `Insists on` and `Invocation`
sections exited 1 on `frontmatter` and `sections`; a well-formed one exited 0; an entry with no
frontmatter exited 1 on `no-frontmatter` and `no-entries-section`. Run from inside the template
with the same installed scripts, the linter found the two personas and the scan seventeen
entries, which proves the root comes from git and not from the virtualenv. Then `pre-commit
try-repo` from `dev-resources` against the template's working tree: the content gates Skipped,
the attribution hook exit 1 on a trailer and 0 on a clean message. The template's own suite
exit 0 with the new fixtures.

### Enforcement

`pyproject.toml`, `.pre-commit-hooks.yaml`, `scripts/session_closeout.py` (`repo_root`,
`--personas`, `cli`), `scripts/kb_frontmatter_scan.py` (`repo_root`),
`scripts/commit_attribution_scan.py` (`main` over the process arguments),
`scripts/new_project.py` (`TEMPLATE_ONLY`, its fixture), `scripts/template_update.py` (`KEEP`,
its fixture). Taught by [[reference_published_hooks]].

---

## Decision 2026-09-23-006: Personas are append-only, and the gate holds them to it

**Date:** 2026-09-23
**Made By:** Chair + AI (the rule in 2026-09-23-002; the mechanics decided here)
**Status:** APPROVED
**Builds:** the append-only bullet of 2026-09-23-002 (TMPL-3.2)

### Context

Decision 2026-09-23-002 ruled that an Invocation never changes in place: an enhancement bumps a
version and appends a changelog line, the linter refuses an Invocation change without the bump,
and the kickoff names the version it was written against. Three mechanics were left open: where
the version and changelog live, what the linter compares against, and what a bump without an
Invocation change means.

### Decision

- **`version:` is a positive integer in the persona's frontmatter**, required alongside `name`
  and `description`; both seeds start at 1. **`## Changelog` is a fourth required section**,
  after Invocation, one bullet per version: `- <version> — <date> — <what changed>`. The
  Invocation is extracted by section, so the changelog does not travel into a kickoff.
- **The comparison is against the committed copy at HEAD** (`git show HEAD:<path>`), which
  every stage of the gate can see, here and in a consumer running the published `persona-lint`.
  An Invocation that differs from it at the same version is `invocation-unbumped`; a lower
  version is `version-order`; a version with no changelog bullet is `changelog`. A new persona,
  or a committed copy from before the rule, constrains nothing, which makes the migration commit
  legal.
- **A bump with no Invocation change is allowed.** Expertise and Insists on may be enhanced too,
  and a bump that records nothing costs one changelog line. The rule guards the text an agent is
  addressed with.
- **The kickoff carries `**Persona version:** <n>`**, written by the scaffold and checked against
  the registry. The copy check already catches a drifted Invocation, so this field is for the
  reader; it is gated so it cannot be wrong. It is required, and the two kickoffs still in the
  folder (the consumed pair and the one being consumed) gained the line in the same commit as the rule.
- **MAJOR, released as `v6.0.0`** under [[reference_template_versioning]]: a required key fails
  every existing persona, a required section fails every existing persona file, and the kickoff
  field fails every existing kickoff. A project adopting it adds `version: 1`, a changelog bullet
  and the kickoff line, once. `dev-resources` moves its `rev` to it.

### Verification

Fixtures: a well-formed persona passes; missing `version:`, a non-integer version, a version with
no changelog bullet, an Invocation change without a bump, a version below the committed one, and
a kickoff naming the wrong or no version each fail on their rule; an Invocation change with its
bump and bullet, a bump with no Invocation change, and a pre-rule committed copy each pass. Six
broken variants run against the fixtures in a scratch harness before the suite was trusted. The
live proof on the real registry had to wait for the migration commit: against a committed copy
with no `version:` the rule constrains nothing, by design, so an Invocation edit before that
commit exited 0; after it, the same edit exited 1. Recorded in the archive repository's sprint-status.

### Enforcement

`scripts/session_closeout.py` (`PERSONA_KEYS`, `PERSONA_SECTIONS`, `CHANGELOG_ENTRY`, `Persona`,
`lint_persona` with `previous`, `persona_version`, `committed_text`, `lint_kickoff`,
`kickoff_skeleton`), `docs/personas/*.md`, `docs/standards/session_handoff_standard_v2.0.md` §5
and §6. Taught by [[reference_session_closeout]].

---

## Decision 2026-09-23-007: The registry and resource entries are synced from `dev-resources`

**Amended 2026-09-23:** `.resources-version` is the project's own state. The first derived
project to take `v7.1.0` received the template's stamp as an `add`; the updater now keeps it and
the initializer clears it at birth, released as `v7.1.1` (PATCH).

**Date:** 2026-09-23; amended 2026-09-23
**Made By:** Chair + AI (the design in 2026-09-23-002; the mechanics decided here)
**Status:** SUPERSEDED by 2026-10-23-003
**Builds:** the sync, ownership and contribution bullets of 2026-09-23-002 (TMPL-3.3)

### Context

Decision 2026-09-23-002 made `dev-resources` the source of the persona registry and of reference
knowledge that belongs to no one project, with the project holding a synced snapshot: a script in
the updater's idiom, ownership disjoint from the template's, sync at closeout, growth only through
a gated publish. Four mechanics were left to the build: how a verdict is decided when both sides
differ, how a resource entry is told from the template's own in the same directory, what the
closeout refuses, and what the first run does when `dev-resources` holds no registry at all.

### Decision

- **`scripts/resources_sync.py` fetches `dev-resources` at `--ref` into `refs/resources/<ref>`**
  and judges every owned path against that tree, exactly as the updater does against a release.
  Owned: every `docs/personas/*.md`; every `docs/orchestration/knowledge/*.md` whose frontmatter
  declares `source: dev-resources`, on either side. `INDEX.md` is merged by slug with the
  updater's own `merge_index`, so a synced entry gets its row the way a released one does.
- **Verdicts are decided by version, never silently.** Fetched only: `add`. Local only:
  `unpublished`. A higher fetched `version:`: `update`. A higher local one: `ahead`. The same
  version with different text, or an unversioned entry edited on either side: `CONFLICT`, kept,
  the stamp withheld; `--take <path>` takes the fetched copy, `--publish` sends the local one.
  A fetched entry without the declaration is `unmarked` and refused, because the declaration is
  what tells the updater to leave the synced copy alone.
- **The updater keeps what the sync owns.** `template_update.KEEP` gains `docs/personas/`, and
  `build_plan` keeps a knowledge entry when any of its three copies declares the source; the
  rule is one function, `resource_owned`, which the sync imports rather than copies. The
  updater's fixtures pin both.
- **The closeout refuses an unpublished persona.** With `.resources-version` present, every local
  persona is looked up in `refs/resources/<ref>`: absent there, or behind the local version, is
  `unpublished`; a stamp whose ref is not fetched in this clone is refused too, so a sync must
  precede every closeout. A project that has never synced is not held to it, which is what lets
  the migration land. Behind locally is the sync's business, not the gate's.
- **`--publish <clone>` writes what is ahead, unpublished or conflicting into a local checkout of
  `dev-resources`** for commit and push there; that clone's gates, the persona linter it consumes
  from this template, judge the contribution. The stamp `<ref> <sha>` is written only when
  nothing remains to publish and nothing conflicts.
- **The first run seeds the registry.** `dev-resources` held no `docs/personas/`; the first sync
  reported both personas `unpublished`, `--publish` wrote them, they were committed there under
  its `persona-lint`, and the sync back found both `up-to-date` and wrote the stamp.
- **MAJOR, released as `v7.0.0`** under [[reference_template_versioning]]: the closeout gains a
  check, and every project's closeout procedure gains a step and a script to run.

### Honest limit

The sync cannot tell an unedited local copy from an edited one without the previous synced blob,
so an unversioned entry that differs on both sides is always a conflict, resolved by hand with
`--take` or `--publish`. Personas carry versions and decide themselves; resource knowledge
entries do not, and the cost is one flag per edit. Adding `version:` to resource entries would
remove it and is the natural next step if the flag proves frequent.

### Verification

Seventeen fixtures over the pure verdicts, ownership and stamp; the updater's suite gained two
fixtures for the keep rule and the sync's session-gate rule three. Live, recorded in the archive
repository's sprint-status: the dry run against `dev-resources` reporting both personas unpublished;
`--apply --publish` writing them into the clone; that clone's commit under its own
`persona-lint`; the sync back up-to-date with the stamp written; and the closeout rule proved
by a scratch persona the ref lacks, by exit code without a pipe.

### Enforcement

`scripts/resources_sync.py`, `scripts/template_update.py` (`KEEP`, `resource_owned`, `build_plan`),
`scripts/session_closeout.py` (`published_state`, `unpublished_personas`, `cmd_closeout`),
`.pre-commit-config.yaml` (`resources-sync-selftest`), `docs/standards/session_handoff_standard_v2.0.md`
§7, `CONSTITUTION.md` §2.2. Taught by [[reference_resources_sync]].

---

## Decision 2026-09-23-008: Which knowledge entries are resource entries

**Date:** 2026-09-23
**Made By:** Chair + AI (the class in 2026-09-23-002; the rule decided here)
**Status:** APPROVED
**Builds:** the "handbook-class knowledge" of 2026-09-23-002 (TMPL-3.4)

### Context

Decision 2026-09-23-002 made `dev-resources` the home for reference knowledge that is not
specific to one project, and 2026-09-23-007 built the sync that carries it. Neither said which
of the knowledge entries here qualify. The template's entries mostly explain its gates and the
decisions behind them, which is exactly what the freshness gate keys to this repository's log.

### Decision

- **An entry is a resource entry when both hold:** it declares `teaches: []`, because a resource
  explains no decision of any one repository; and its subject is a machine, a tool or a workflow
  rather than this template's own mechanisms. It is marked `source: dev-resources` and published.
- **One entry moves now:** [[reference_macos_toolchain]]. It was the only `teaches: []` entry,
  and its subject is the operator's machine.
- **Every gate entry stays,** including the two that teach no decision by content but describe
  this repository's scripts, and every entry with a non-empty `teaches:`. If an entry ever
  qualifies on the first rule but not the second, it stays; the second rule is the one that
  matters.
- **A moved entry keeps its slug, path and INDEX row here.** The sync merges rows from
  `dev-resources`' own `docs/orchestration/knowledge/INDEX.md`, which carries the same table
  shape and only resource rows, so a project's index gains the row without a second format.
- **MINOR, released as `v7.1.0`:** the mark changes which script writes the file, and a project
  on the previous release adopts nothing; the updater keeps the marked entry, and the project's
  first sync after that takes the marked copy with `--take`, once.

### Migration, stated

A project whose copy of a moved entry predates the mark holds an unmarked file; the updater
keeps it (any of the three copies marked means keep), and the sync then sees a fetched marked
copy against a local unmarked one, which is a conflict by 2026-09-23-007's rule. The remedy is
`--take <path>`, once per moved entry per project, and the probe records it under TMPL-3.4.

### Enforcement

`source: dev-resources` in the moved entry's frontmatter, read by `template_update.resource_owned`
and `resources_sync.owned`. Taught by [[reference_resources_sync]].

---

## Decision 2026-10-22-001: `v2.0.0` runs the framework on Claude Code's native machinery

**Amended 2026-10-22 (S3):** a session takes its persona from the `SessionStart` hook, which injects
the agent's prompt unless the session already runs as that agent. `claude --agent` is available, not
required: under it the agent's prompt replaces Claude Code's built-in system prompt whole (decision
2026-10-22-005).

**Date:** 2026-10-22; amended 2026-10-22
**Made By:** Chair + AI
**Status:** APPROVED
**Affects:** `AGENTS.md`, `CLAUDE.md`, `AGENT_INTEROP.md`, `CONSTITUTION.md` §2 and §6, `docs/orchestration/AGENT_COLDSTART_CHECKLIST.md`, `docs/standards/session_handoff_standard_v2.0.md`, `docs/personas/`, `.claude/`

### Context

Claude Code does nearly all the agentic work on this framework, with local models as the only
other reader. Measured on 2026-10-22, the cold start asks an agent to read about 74 KB of
markdown across ten files before building; the cold-start procedure is written in four places
and the closeout in three; the interop contract is a 6 KB rationale for a tool split that no
longer exists. Claude Code's own docs, read the same day: it reads `AGENTS.md` natively from
v2.1.277 (the operator's install is 2.1.267); a `SessionStart` hook can run commands and inject
their output into context, and runs again with a `compact` matcher after compaction; a `Stop`
hook can refuse to end a turn; `PostToolUse` fires after every edit and command; subagents in
`.claude/agents/` carry their own context and can run the main session by `claude --agent`;
skills in `.claude/skills/` run forked into a subagent with `context: fork`; rules under
`.claude/rules/` load only when a matching path is touched. The docs also say that `CLAUDE.md`
and hooks are context, not enforcement, except permissions and `PreToolUse`.

The operator's standing problem is the compaction cliff: a closeout that dies mid-way, and
in-flight plans and judgements lost when the conversation is summarized.

### Decision

- **One cold start, run by a hook.** The procedure lives in `AGENTS.md` alone; `CONSTITUTION.md`
  §2, the checklist and the handoff standard point to it. A `SessionStart` hook runs the identity
  gate, `git pull`, `session-verify` and the document-queue check, and injects their results, the
  current kickoff and the newest sprint-status entry; with the `compact` matcher it re-injects the
  same after compaction. The checklist's comprehension questions, which no script verifies, go.
- **Checkpoint discipline becomes a `Stop` hook** that refuses to end a turn while sprint files are
  modified and uncommitted, or while the working notes are older than the turn's edits.
- **The uncommitted interval is banked mechanically.** A `PostToolUse` hook writes a session
  journal under `sprint/recovery/` (file changed, command run, exit code) without the model's
  cooperation; a working-notes file of fixed small shape (plan, open decisions, half-done work)
  is what the `Stop` hook demands; both are re-injected after compaction and cleared at closeout.
  `PreCompact` is a backstop, tested before it is relied on, since a block when the context is
  already full can wedge a session.
- **Personas are subagents** in `.claude/agents/<slug>.md`: the registry moves there, `persona-lint`
  and `resources_sync.py` follow it, and a kickoff names the agent instead of copying its
  invocation. The main session runs as the named agent.
- **Procedures are skills**, forked where heavy: the closeout, the release cut, the planning
  session, the sanitize-and-cut, document production. The `SKILL.md` is the one home of the
  procedure; the standards shrink to the law. A gate keeps a skill's commands in step with the
  config, as the runbook gate does for hooks.
- **Judgement rules are path-scoped** under `.claude/rules/`, loaded when a matching file is
  touched; the constitution and the checklist shrink accordingly.
- **`AGENT_INTEROP.md` is retired** into `AGENTS.md`; its one law is already a prime directive
  there. `CLAUDE.md` stays as the `@AGENTS.md` bridge until the installed Claude Code is at least
  v2.1.277, then goes; the condition is written into the story.
- **What does not move.** The pre-commit suite, the CI workflow, the sprint files, the decisions,
  the knowledge base and the closeout gate stay as they are: git hooks and CI enforce for any
  agent on any machine; Claude hooks are for context and ergonomics.
- **Settings.** `disableWorkflows` on, so a typed keyword cannot start a multi-agent workflow;
  `ask` rules for the one-way doors met this month: `gh repo delete`, `git push --delete`,
  `gh repo edit --visibility`.
- **MAJOR**, `v2.0.0`, together with 2026-10-22-002: files a project references are removed and
  renamed, and the registry moves, so every derived project acts once at adoption.

### Consequences

- Compaction becomes a slope: committed state, the brain, the kickoff, the journal and the notes
  survive it; only reasoning never written down is lost, and the `Stop` hook narrows that window
  to one turn.
- A derived project's `template_update.py` must carry `.claude/agents/`, `.claude/skills/`,
  `.claude/rules/` and `.claude/settings.json` by the ownership rules; the initializer and the
  sanitizer learn the journal and notes paths.
- The three existing projects take `v2.0.0` through the updater as the release's own proof.

### Enforcement

To be built as epic TMPL-1; each story names its gate. Taught by a knowledge entry written with
the build.

---

## Decision 2026-10-22-002: Authoritative documents stop going stale

**Date:** 2026-10-22
**Made By:** Chair + AI
**Status:** APPROVED
**Affects:** `docs/governance/doc_control_standard.md`, every document that carries `authority:`, this file's body format

### Context

Updates, design changes and reversals land in the decision log and the knowledge base, and the
documents that are supposed to be the source of truth for a scope, the PRD, the architecture,
the runbooks and the standards, are never brought up to date. The document-control standard says
"update the documents and the changelog table" and nothing enforces it. The knowledge base does
not have this problem because `teaches:` and `verified:` are gated; it also cannot catch a
*missing* update, since a new decision names no document.

The operator's two further constraints: an agent rewriting a document inline at decision time
produces patchwork, and the remedy cannot be a closeout item, because closeouts are where
compaction strikes, nor open-ended.

### Decision

- **Authorities declare themselves.** A source-of-truth document carries frontmatter `authority:
  <scope>`, `implements: [decision-ids]`, `verified: <date>`, and ends with a `## Version log`
  table: version, date, decision, summary, commit. The frontmatter is the registry.
- **Decisions declare impact.** Every decision body from this one forward carries `**Affects:**`:
  the authorities it changes, with the sections and the nature of the change, or `none`. Older
  decisions read as `none`.
- **The gate accepts two outcomes and nothing else.** For each decision naming a document, the
  document's version log holds a row citing that decision, or the tracker holds a story citing the
  decision and the document, not Done. A row written by a session other than the technical
  writer must carry a fact marker: a value, a name, a path, a count. Structural changes are queued.
- **The queue drains at cold start, bounded.** A `doc-queue` manual-stage gate, run by the
  `SessionStart` hook, fails while any queued story is older than one session, read from a
  `Queued: S<N>` note on its row. The drain runs as the technical-writer subagent, one document per
  invocation, in its own context, and returns the rows it wrote. The queue is visible at every
  closeout and is never a closeout step.
- **The commit is stamped after the fact and verified.** The newest row reads `pending`;
  `--stamp` fills the hash once the commit exists, and the gate verifies every stored hash against
  git. `--history <doc>` derives the commit for any unstamped row. A stored value with a gate is
  allowed; a hand-maintained one without is not.
- **Scope at introduction.** The standards and the gate runbook are marked first, so the gate has
  real content to prove against; a project marks its PRD, architecture and runbooks.
- **Part of `v2.0.0`.** A new gate that can fail content a project already has.

### Consequences

- The document-control standard is rewritten around the gate and loses its "stays private" fossil.
- The `technical-writer` is the second subagent in the registry, published to `dev-resources`.
- The batching is the anti-patchwork control: one writer pass per document over every pending
  change, instead of one paragraph per deciding session.

### Enforcement

To be built as epic TMPL-2: `scripts/doc_authority_scan.py` with fixtures proved against broken
variants, the `doc-queue` gate, the writer agent and its forked drain skill.

---

## Decision 2026-10-22-003: `v2.1.0` is the development team and the coding standard, designed first

**Date:** 2026-10-22
**Made By:** Chair + AI
**Status:** APPROVED
**Affects:** none yet; the design sessions name them

### Context

Where a project's task is software, the operator wants a trained team of role agents that hand
off to each other as a human team does and produce code that passes a security audit, running
autonomously until something needs the operator. Separately, agents write verbose, run-on,
repetitive code when nothing stops them, and a coding standard that is prose stops nothing.

### Decision

- **The team is built on the `v2.0.0` substrate, not with it.** Roles are subagents with isolated
  context and narrow briefs (product owner, architect, planner, implementer, test engineer, code
  reviewer, security auditor, technical writer, release manager). Every handoff is an artifact in
  the repository that a gate judges, never a conversation between agents; a role may not start
  until its input artifact exists and passes. The operator's checkpoints are a written list of
  review triggers the orchestrating skill stops at: a new dependency, a schema, auth or crypto
  change, an external service, a cost, a security finding the auditor cannot clear, anything a gate
  cannot judge. Orchestration is a saved workflow invoked deliberately, one story at a time.
- **The coding standard has three layers.** Mechanical, in the gate suite: function and file
  length, complexity ceilings, duplicate detection, formatter and linter, type checks, a coverage
  floor, dependency audit; a core of numbers with a rule that every stack maps each to a tool,
  chosen per project at its planning session. Process, in the team: design before code, stories
  the size of a module, a reviewer whose brief is structure and duplication and who is not the
  implementer, plan mode forced on for implementation skills. Judgement: one page under
  `.claude/rules/`, path-scoped to code, opening with `CONSTITUTION.md` §4A.
- **Each opens with a design session.** The team's: roles, artifacts, triggers, orchestration,
  with the operator. The standard's: with a specialized reviewer agent, the core limits proved
  against a known-good and a known-bad codebase before adoption, because this standard is the
  hardest thing in the framework to unwind once development starts.
- **MINOR**, `v2.1.0`: agents and a stack profile a project opts into.

### Enforcement

Epics TMPL-3 and TMPL-4; the design sessions log their own decisions.

---

## Decision 2026-09-25-004: The first public release is `v1.0.0`, cut on the finished tree

**Date:** 2026-09-25
**Made By:** Chair (the ask) + AI (the mechanics)
**Status:** APPROVED
**Builds on:** 2026-09-23-003 (the pristine cut and the sanitizer)

### Context

The pristine cut tagged the sanitized tree `v1.0.0` before the go-live work: the template flag,
the hook pin, the birth probe, the visibility decision and its control, the license, the public
README and the rulesets. Those three sessions cut `v1.0.1`, `v1.1.0` and `v1.1.1`, so the first
version anyone outside the owner's account could take was a `v1.1.1` whose predecessors had never
been usable by them. The operator asked that the finished template's first release be `v1.0.0`.

### Decision

- **The four tags are removed**, locally and on GitHub, and the finished tree is sanitized with
  `sanitize_template.py --apply`, which regenerates the two sprint documents to the template's own
  S1 and clears the handoff pairs and their archive, as the cut did. Then `--release v1.0.0`, one
  commit `release: v1.0.0`, one annotated tag `v1.0.0`. The version gate sees one tag, the earliest,
  exempt from the bump rule, and the constant it verifies reads `v1.0.0`.
- **History is kept.** No force-push, no rewritten commits: the go-live sessions' commits and their
  `release:` messages stay in `git log`, and the rulesets of 2026-09-25-003 stay in force. A
  reader who wants the go-live diary has the commits; the sprint documents describe the pristine
  state, as they did after the cut.
- **The consumer follows.** `dev-resources` pins the new `v1.0.0`; nothing it consumes changed
  between the removed tags and this one. No derived project exists that carries a removed tag.
- **Earlier "released as" notes are read as folded in.** Decisions 2026-09-25-001 and -002 name
  `v1.1.0` and `v1.1.1`; those tags no longer exist and both changes are part of `v1.0.0`. The
  notes are amended to say so rather than rewritten, because a decision body is a record.
- No bump type: the earliest tag has no predecessor. Everything after this is judged from
  `v1.0.0` by [[reference_template_versioning]].

### Consequences

- The next session on this repository is S1 with no pair, as after the cut; it opens its first
  story before it can close out. The go-live epics are in the git history, not the tracker.
- A tag, once published, is meant to be permanent. This is the one time it was not, before any
  outside consumer existed; it is not a precedent, and [[reference_pristine_cut]] says so.

### Enforcement

`scripts/template_version.py --check` (one tag, its commit stamped `v1.0.0`),
`sanitize_template.py --check` exit 0 and `session-verify` exit 0 at S1, both recorded at the cut.
Taught by [[reference_pristine_cut]].

---

## Decision 2026-09-25-003: The default branch is protected against deletion and force-push, and nothing more

**Date:** 2026-09-25
**Made By:** Chair + AI
**Status:** APPROVED
**Builds on:** 2026-09-22-001 (protection not pursued while private), 2026-09-25-001 (public)

### Context

With both repositories public, branch protection is available at no cost. Two of its rules guard
against loss that nothing else can undo: a deleted default branch and a rewritten history. The
third common rule, a required status check before anything lands on `main`, would end the direct
push that every checkpoint and closeout here is, and force a pull-request flow on one developer
for a workflow that already reports within two minutes.

### Decision

- A repository ruleset named `protect main`, enforcement active, on the default branch of
  `SaltyBrett/agentic-dev-template` and `SaltyBrett/dev-resources`, with two rules: `deletion`
  and `non_fast_forward`. Created through the REST API; the archive is read-only and needs none.
- No required status check and no pull-request requirement. The `gates` workflow keeps reporting;
  the local hooks keep blocking (2026-09-22-001).
- Revisit when a second contributor exists: that is the day a required check earns its cost.

### Consequences

- The Claude-only `settings.json` deny of `git push --force` is now backed by the server for the
  default branch; a force-push from any clone or tool is refused by GitHub.
- A mistaken push to `main` is still corrected by a new commit, never by rewriting.

### Enforcement

GitHub, server-side. Nothing in the tree; `gh api repos/<owner>/<repo>/rulesets` lists it. Taught
by [[reference_ci_backstop]].

---

## Decision 2026-09-25-002: MIT, under the operator's name

**Date:** 2026-09-25
**Made By:** Chair (the license) + AI (the mechanics)
**Status:** APPROVED

### Context

A public repository with no license file is all rights reserved: anyone who creates a project from
the template infringes. Neither public repository had one after decision 2026-09-25-001.

### Decision

- **MIT**, copyright 2026 Brett Bennett, as `LICENSE` in the root of the template and of
  `dev-resources`, identical text. MIT because the template exists to be copied into private
  commercial projects, and MIT asks nothing of them beyond keeping the notice.
- **A project owns its license from birth.** The initializer leaves `LICENSE` in place (it is in
  no mutating list), and `template_update.KEEP` names it so a release never rewrites the license
  a project chose. A project born before this decision receives no license by update; adding one
  is that project's own act.
- **PATCH**, released as `v1.1.1` with the public README (TMPL-2.2): no project must act. That tag
  was folded into the first public `v1.0.0` by 2026-09-25-004.

### Enforcement

`LICENSE`; `scripts/template_update.py` (`KEEP`). Verified by both self-tests and a scratch birth
whose dry run lists no `remove LICENSE`; GitHub reports the license on both repositories.

---

## Decision 2026-09-25-001: The template is public; a project made from it is private by default

**Date:** 2026-09-25
**Made By:** Chair (the visibility) + AI (the control and the mechanics)
**Status:** APPROVED
**Supersedes:** the "stays private" resolutions in 2026-09-22-001 and 2026-09-23-005

### Context

After the pristine cut the live repository's history begins at the sanitized tree, which removed
the operator's original reason for keeping it private. Two consequences of privacy remained in
force: `dev-resources` could have no `gates` workflow, because a consumer's Actions run cannot
clone a private hook repository without a secret, and its pin had to name an ssh host alias that
only the operator's machines resolve. The operator decided: the template and `dev-resources` go
public, and every project created from the template is private unless it is meant otherwise.

"Private by default" cannot be set on GitHub's side for a personal account: the "Use this
template" flow and `gh repo create --template` both take the visibility at creation time, and
nothing stops a public choice. A written rule in the guide would be the convention-as-control
shape this repository removes.

### Decision

- **`SaltyBrett/agentic-dev-template` and `SaltyBrett/dev-resources` are public.** Before the
  flip, gitleaks scanned the full history of both (13 and 9 commits) and found nothing. The
  archive, `SaltyBrett/agentic-dev-template-archive`, stays private: it is the build diary.
- **The initializer enforces private by default.** `new_project.py` reads the project's
  visibility from GitHub (`gh repo view --json isPrivate`) before it plans anything and refuses a
  public repository unless `--public` is given, printing the one command that makes it private.
  A visibility it cannot read (no `gh`, or a remote that is not GitHub) is reported and not
  refused: an unreadable answer is neither public nor private. `--force` does not bypass this;
  the two refusals are separate flags because they are separate intentions.
- **Branch protection is still not enabled** on the template, though it is now free. Every
  checkpoint is a direct push to `main`; a required status check would force a pull-request flow
  on one developer for a workflow that already reports, and a red run is fixed in the session
  that caused it (2026-09-22-001).
- **`dev-resources` pins the https URL** at the current template tag and gains the same `gates`
  workflow, which its public template now lets it run without a credential.
- **MINOR**, released as `v1.1.0`: a project already born never re-runs the initializer, so
  nothing existing has to act; a new refusal at birth is new capability. That tag was folded into
  the first public `v1.0.0` by 2026-09-25-004.

### Consequences

- A project's first command tells its operator when the repository is public. The web flow's
  visibility picker is no longer the only control.
- A consumer of the published hooks no longer needs the ssh host alias or a credential; the
  measured cost of a private hook repository stays recorded in [[reference_published_hooks]] for
  anyone who consumes a private one.
- The initializer now shells out to `gh`. Where `gh` is absent the rule is not checked, and the
  run says so; it never fails for want of the tool.

### Verification

Self-test fixtures for the slug parser and the verdict over every reading, proved against
broken variants before they were trusted; live, the initializer refusing the public template
clone itself before the template refusal is reached is not possible (the template refusal comes
first), so the live proof is a scratch project: refused while public, accepted with `--public`,
accepted once private. `dev-resources` ran its suite from a cleared pre-commit cache against the
https pin and its first `gates` run was observed. Recorded in the S2 sprint-status entry.

### Enforcement

`scripts/new_project.py` (`repo_slug`, `repo_visibility`, `visibility_verdict`, `--public`, three
fixtures), `TEMPLATE_GUIDE.md` Step 8. Taught by [[reference_ci_backstop]] and
[[reference_published_hooks]], both re-verified.

---

## Decision 2026-09-24-001: Rules with no control, found in the fossil sweep: which get one, which go

**Date:** 2026-09-24; amended 2026-09-24 (TMPL-5.5 built, its enforcement and bump named)
**Made By:** Chair + AI
**Status:** APPROVED
**Builds:** TMPL-5.3 and TMPL-5.4 (epic TMPL-5, opened for exactly this shape); TMPL-5.5 after them

### Context

The three standards and `sprint/recovery/` predate every gate and no session since had read them
whole. TMPL-5.4 read them, with `CONSTITUTION.md` §6.2 and `doc_control_standard.md` under
TMPL-5.3, for two shapes: a checklist standing in for a control, and a GCC line a commercial
project inherits. Fossils were fixed in the same work unit (the archive repository's sprint-status names
each). What remains is every written rule that no script enforces. The kickoff's instruction was
to decide, per rule, whether it gets a control or is deleted, and to build nothing here.

### Decision

| Rule | Where | Verdict |
|------|-------|---------|
| Never start a story whose dependencies are not `Done` | sprint standard §7 | **Gets a control: TMPL-5.5.** The state gate already parses the tracker for its statistics; a story `In Progress` or `Done` with a dependency not `Done` is one more row check. |
| No `[EXAMPLE]` or `{{PLACEHOLDER}}` content in a live sprint | sprint standard §6, §5.3, §11.2 | **Gets a control: TMPL-5.5**, in a project (a `.project-profile` exists) once a non-example epic exists, so a fresh project's shipped example epic does not fail it at birth. |
| Agents change documents through pull requests only; feature branch, reviewers, merge | doc control, Change Workflow and Agentic vs Human | **Deleted.** Withdrawn by 2026-09-22-001 ("no branch-and-pull-request convention is imposed") and contradicted by every `checkpoint:` commit since. The section now states what is enforced. |
| PR Review Checklist: linting clean, governance header, changelog, manifest/tag plan, evidence path, agentic usage documented | doc control | **Deleted.** The items the suite judges are the suite's (the runbook names them); the rest name things this repository does not define: a linter, a governance header, a manifest. |
| Maintain a manifest with pointers and tag references | doc control, Tagging | **Deleted.** No manifest exists; `template_version.py` verifies the template's tags, and a project's baseline uses the same form. |
| Validation evidence must be captured with the template | recovery README rule 3; doc control, Evidence | **Not a control, and now says so.** The trigger, a validation run, is not observable from the tree, so no gate can prove it happened. Reworded from *must* to where a result goes, marked ungated. |
| Update the authority matrix on supersession; STOP and escalate when two artifacts claim CURRENT | recovery README, `AUTHORITY_MATRIX.md` | **Instruction, kept.** Behaviour in a situation, the class of `CONSTITUTION.md` §8, not a claim that a check exists. |
| Prohibited practices, rotation schedule, audit, emergency procedures | secrets standard §7 to §10 | **Kept, outside a repository gate's reach.** They govern the project's runtime. gitleaks covers the committable subset (a secret in code). |
| Planning protocol preconditions and output checklist | sprint standard §5.1, §5.3 | **Kept as the protocol's own output check.** Its mechanical items are gated (statistics reconcile, the entry cap) or go to TMPL-5.5; the rest (PRD coverage, user confirmation) are judgement. |
| `[Locked]` craft rules | document production standard §7 to §14 | **Kept.** Style for produced Office documents, not repository state. |

### Bump

PATCH for the sweep. No enforced rule changes: the deletions remove prose a decision had already
withdrawn or that named a control that never existed, and the fences move GCC lines to where the
profile already governs. Released as `v8.0.1`.

MAJOR for TMPL-5.5: a project's tracker can now fail on rows it already has, a `Done` story
whose dependency was never finished, or the shipped example epic left beside a real one. Released
as `v10.0.0`.

### Enforcement

`scripts/session_closeout.py --check`, on every commit: `dependency-order` (a story `In Progress`
or `Done` whose listed dependency is not `Done`, or is no story) and `live-placeholder` (in a
project whose tracker holds a non-example epic, an `[EXAMPLE]` row or heading or an unfilled
token in the tracker, sprint-status or the decision log, outside inline or fenced code). The
sprint standard §7 and §11 say the rules are gated; the runbook's `session-closeout-check` section
lists them. `doc_control_standard.md` and `sprint/recovery/README.md` name this decision where a
rule is stated as ungated. Taught by [[reference_session_closeout]] for the two controls and by
[[reference_project_profiles]] for the fences; the sweep itself is recorded in the archive
repository's sprint-status.

---

## Decision 2026-10-22-004: The session journal and the working notes are local, never committed

**Date:** 2026-10-22
**Made By:** AI (S2), within decision 2026-10-22-001; put to the operator at the S2 handover
**Status:** APPROVED
**Affects:** `.gitignore`, `scripts/session_journal.py`, `scripts/session_stop.py`, `scripts/session_start.py`, `scripts/session_closeout.py` (`--closeout`)

### Context

TMPL-1.2 builds the journal (`sprint/recovery/journal.md`, one line per Edit, Write or Bash event,
written by a `PostToolUse` hook) and the working notes (`sprint/recovery/WORKING_NOTES.md`, which
the `Stop` hook demands). Decision 2026-10-22-001 says both are cleared at closeout and that the
journal writer must be safe beside the gate suite; it does not say whether they are committed.

Tracked, the journal would carry every command an agent ran into the history of a public
repository, where one command holding a token is a leak that rewriting history cannot fully undo,
and a command naming a banned feature fails the scanner on the next commit. pre-commit stashes
unstaged edits to tracked files around a hook run, so a journal line appended by a parallel tool
call inside that window would land between the stash and its restore. And every tracked sprint
file the agent touches each turn would trip the `Stop` hook's own rule against uncommitted sprint
files.

### Decision

- Both files are gitignored. `session_journal.py` owns their paths and the notes' shape; the
  `SessionStart` hook creates the notes when they are missing; the closeout gate (`--closeout`)
  resets both when it passes.
- The `Stop` hook leaves both out of "uncommitted work" by path as well as by `.gitignore`, so its
  rule holds even if the ignore lines are lost; the journal self-test fails if they are.
- What survives a lost clone or a move to another machine is the committed state, as before. The
  journal and notes bank the interval against compaction and a dead session on the same clone,
  which is the failure the decision names.

### Consequences

- The writer is safe beside the suite by construction: an ignored file is outside the stash, and
  the scanners, gitleaks and the sanitize check read only what git would commit.
- The notes are reasoning in flight, a cache under the prime directive; anything durable in them
  still goes to the tracker, the decision log or a knowledge entry.
- The initializer and the updater carry the two `.gitignore` lines with the file; TMPL-1.6 confirms
  the ownership.

### Enforcement

`scripts/session_journal.py --self-test` (`session-journal-selftest`) checks that the repository's
`.gitignore` covers both paths and that concurrent appends keep every line whole;
`scripts/session_stop.py --self-test` that the notes never count as the newest change. Taught by
[[reference_claude_code_hooks]].

---

## Decision 2026-10-22-005: Personas are agent files, and the start hook gives the session its persona

**Date:** 2026-10-22
**Made By:** Chair + AI (S3): the persona's path to the session and the `dev-resources` window by
the operator, put as questions; the format by the AI
**Status:** APPROVED; SUPERSEDED (dev-resources holding the registry) by 2026-10-23-003
**Amends:** 2026-10-22-001 (its personas bullet: the main session no longer runs as the agent by default)
**Builds:** the personas bullet of 2026-10-22-001 (TMPL-1.3)
**Affects:** `.claude/agents/`, `docs/personas/` (removed), `scripts/session_closeout.py`, `scripts/session_start.py`, `scripts/resources_sync.py`, `scripts/template_update.py`, `scripts/new_project.py`, `scripts/sanitize_template.py`, `.pre-commit-hooks.yaml`, `.pre-commit-config.yaml`, `docs/standards/session_handoff_standard_v2.0.md` §3, §5 and §6, `dev-resources`

### Context

Decision 2026-10-22-001 moved the persona registry to `.claude/agents/` and said the main session
runs as the named agent. The sub-agents reference, read whole on 2026-10-22 (Claude Code 2.1.308),
settles the mechanics: the file's body is the agent's system prompt; only `name` and `description`
are required, and a key Claude Code does not know is ignored without a word; a frontmatter that
does not parse makes Claude Code skip the file, also without a word; `name` is the identity hooks
receive as `agent_type`. And under `claude --agent <name>` a non-empty prompt **replaces Claude
Code's built-in system prompt whole**, as `--system-prompt` does, while `AGENTS.md` still loads.

A probe in a scratch clone of the committed hooks: `claude --agent framework-maintainer -p` gave back
a canary from the agent's body, quoted the heading of `AGENTS.md`, saw the kickoff the start hook
injected, and the hook's input carried `agent_type: framework-maintainer`. Its prompt was about
2,500 tokens smaller than a control run without `--agent`, whose hook input carried no `agent_type`
and whose answer had no persona.

Separately, `dev-resources` pins `persona-lint` at `v1.0.0`, and the three projects on `v1.0.0`
sync `docs/personas/` from its `main`. Two of them hold a sync stamp, so if the folder left
`dev-resources`, their next closeout would refuse every persona as unpublished, and the remedy it
prints (`--publish`) would write the old folder back.

### Decision

- **The format.** `.claude/agents/<slug>.md`. The frontmatter holds `name` (the slug, equal to the
  filename stem), `description`, `version` (a positive integer) and `expertise`, `insists_on` and
  `changelog` as YAML lists of strings. The body is the Invocation, verbatim, and nothing else,
  because the body is the prompt. `slug:` and the human title go: `name` is the slug. The five
  personas move with their text unchanged, so each keeps its version and the S3 kickoff's copy
  still matches.
- **The linter parses the frontmatter as YAML**, since Claude Code skips a file whose frontmatter
  does not parse and says nothing. The import is lazy, so the session hook, which imports the
  closeout module, needs no PyYAML. The append-only rules of 2026-09-23-006 carry over unchanged
  against the committed copy at HEAD, the body standing for the Invocation. A moved file has no
  committed copy at its new path and constrains nothing, which makes the move commit legal.
- **The session takes its persona from the start hook, not from `--agent`** (the operator's
  choice). The kickoff names the agent, and `session_start.py` reads `agent_type`: equal to the
  kickoff's persona, it says so; otherwise it injects the agent's prompt as context, at startup and
  after compaction. A plain `claude` session, the VS Code extension and `claude --agent` all end
  with the persona in context; only `--agent` also drops Claude Code's built-in prompt, so it is
  available, not required.
- **The kickoff names the agent.** Section 1 is one line, written by the scaffold, naming
  `.claude/agents/<slug>.md`. The linter accepts that line or a verbatim copy of the prompt, so
  `KICKOFF_S3.md`, written under the old rule, stays valid. `**Persona version:**` stays and is
  still checked against the registry.
- **`dev-resources` holds both trees until TMPL-2.4** (the operator's choice). It gains
  `.claude/agents/`, judged by `persona-lint` at a template commit that reads the new location, and
  keeps `docs/personas/` frozen, still judged by `persona-lint` at `v1.0.0`, so a project on
  `v1.0.0` keeps syncing unchanged. TMPL-2.4, which takes the three projects to `v2.0.0`, removes the
  old tree. The template pushes first; `dev-resources` then pins that commit by its SHA, there being
  no `v2` tag yet. Between the two pushes neither repository's gates read the other's new state.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001): the registry's path, the persona's shape and
  the kickoff's section 1 change for every project.

### Consequences

- A persona enhanced during the window is published by the template to `.claude/agents/`. A
  `v1.0.0` project's publish writes `docs/personas/` and reaches `.claude/agents/` only when
  TMPL-2.4 ports it, so TMPL-2.4 compares the two trees before removing the old one.
- A project adopting `v2.0.0` must carry its own `docs/personas/` into `.claude/agents/`; the
  ownership rules (TMPL-1.6) and the adoption (TMPL-2.4) own that migration.
- Claude may delegate to a persona agent by its description, as to any project agent; that is the
  reuse the role agents of 2026-10-22-003 will build on.

### Verification

Fixtures: the closeout self-test (87 checks) covers the agent shape, the YAML refusals, the
append-only rules, both forms of section 1 and a module load with PyYAML blocked; the start
self-test (28) the four persona cases at startup and after compaction; the sync self-test (18)
pins the owned path. Twenty-two broken variants, each failing at least one fixture. Live, in a
scratch clone of the committed template: `claude --agent framework-maintainer -p` answered in the
persona, its hook input carried `agent_type: framework-maintainer` and the hook said the session
ran as that agent; a plain `claude -p` got the prompt injected verbatim and answered as Claude Code
holding the persona; a body edited without a bump exited 1 (`invocation-unbumped`), with the bump 0.
In `dev-resources`, both pins ran (five personas in each tree), the published hook refused the same
unbumped edit, and its `gates` run was green; the template's sync then reported every agent
`up-to-date`, and a `v1.0.0` project's own sync, in a scratch clone, still resolved every persona
from the frozen tree.

### Enforcement

`scripts/session_closeout.py` (`PERSONAS`, `PERSONA_KEYS`, `persona_frontmatter`, `lint_persona`,
`persona_line`, `lint_kickoff`, `kickoff_skeleton`), `scripts/session_start.py` (the persona
section), `scripts/resources_sync.py` (`PERSONAS`), `.pre-commit-hooks.yaml` (`persona-lint`'s
`files:`), and in `dev-resources` its `.pre-commit-config.yaml`. Taught by
[[reference_session_closeout]] and [[reference_resources_sync]].

---

## Decision 2026-10-22-006: Rules are path-scoped judgement, and a gate keeps them so

**Date:** 2026-10-22
**Made By:** AI (S3), within decision 2026-10-22-001; reported to the operator at the S3 handover
**Status:** APPROVED
**Builds:** the path-scoped rules bullet of 2026-10-22-001 (TMPL-1.5)
**Affects:** `.claude/rules/`, `CONSTITUTION.md` §6.3, `docs/orchestration/knowledge/INDEX.md`, `scripts/session_closeout.py` (`--check`), `AGENTS.md` (governance map)

### Context

Decision 2026-10-22-001 moves judgement that applies only when certain files are touched into
`.claude/rules/`. The memory reference, read 2026-10-22: a rule with `paths:` loads when Claude
reads, writes or edits a matching file; a rule without `paths:` loads in every session, like
`CLAUDE.md`; a frontmatter that does not parse is ignored and the rule loads as if it had no
`paths:`; a glob that matches nothing makes a rule that never loads. Claude Code reports none of
these. And a rule is Claude's alone: Codex reads `AGENTS.md` and what it points to.

### Decision

- **A rule here is path-scoped or it is refused.** Always-loaded text belongs in `AGENTS.md`, the
  one brain; an unscoped rule would be a second one. The session state gate refuses a rule whose
  `paths:` does not parse as a list of globs, a rule no file git would commit matches, and a rule
  that repeats a sentence of `AGENTS.md`.
- **Rules are repository markdown and the home of their instructions.** `AGENTS.md`'s governance
  map tells any agent to read the rules whose `paths:` match what it edits, so the instructions stay
  portable. A rule points to the knowledge entry that holds the why, and never restates it.
- **Three subjects, four files:** gate scripts and the suite, knowledge entries, decision logs and
  the sprint documents. `CONSTITUTION.md` §6.3 becomes a pointer: its reasoning moves to a
  knowledge entry and its reading and writing rules to the knowledge-entry and decision-log rules.
  The knowledge index keeps its reading rule and sheds its frontmatter block, and its template
  (which had no frontmatter at all), to the knowledge-entry rule.
- Part of `v2.0.0` (decision 2026-10-22-001): a project's own unscoped rules fail the new check.

### Consequences

- A project that kept instructions in an unscoped rule moves them to `AGENTS.md` or scopes them.
- The sprint documents keep their own headers: the generators write them, and the header is read
  at cold start, when the reading rule matters.
- TMPL-1.6 carries `.claude/rules/` through the initializer, the updater and the sanitizer.

### Enforcement

`scripts/session_closeout.py` (`RULES`, `lint_rule`, `glob_regex`, `expand_braces`, `sentences`,
`restatements`) in `session-closeout-check`. Taught by [[reference_claude_code_rules]]; the moved
section by [[reference_kb_freshness]].

### Verification

Fixtures in the closeout self-test for every refusal and the glob translation; fifteen broken
variants, each failing one. Live, in a scratch clone: an unscoped and a dead rule each failed the
check by name; a canary rule scoped to one knowledge entry was absent from a session that used no
tool and from one that read `README.md`, and present in one that read the entry. The first version
compared whole sentences and let a rule copying a clause of `AGENTS.md` pass; the check now finds a
sentence inside the other text either way, and the plant fails it.

---

## Decision 2026-10-23-001: Procedures are skills, and a skill is repository markdown

**Date:** 2026-10-23
**Made By:** Chair + AI (S4): how the forked closeout receives the session's judgement, and which
skills are the operator's alone, by the operator, put as questions; the rest by the AI
**Status:** APPROVED
**Builds:** the procedures bullet of 2026-10-22-001 (TMPL-1.4)
**Affects:** `.claude/skills/`, `AGENTS.md` (How I work, Conventions, the governance map, the procedures section), `CONSTITUTION.md` §2.4, `docs/standards/session_handoff_standard_v2.0.md` §4, §5, §7 and §11, `docs/standards/sprint_management_standard_v1.0.md` §1, §5, §6 and §8, `docs/standards/document_production_standard_v1.0.md`, `scripts/skill_scan.py`, `scripts/session_closeout.py` (the kickoff's section 5), `scripts/new_project.py` (the S1 entry and the tracker header), `.pre-commit-config.yaml`, `docs/governance/gate_suite_runbook.md`, `.claude/rules/sprint-documents.md`, `TEMPLATE_GUIDE.md` Step 7, `README.md`

### Context

Decision 2026-10-22-001 makes each procedure a skill whose `SKILL.md` is its one home. `AGENTS.md`
said the opposite in its section "Workflows are portable markdown, not tool skills": a skill was a
per-tool accelerator, never the source of truth. That section was written when a skill meant a
copy in one tool's private folder. A `SKILL.md` committed under `.claude/skills/` is repository
markdown, as a rule under `.claude/rules/` is (decision 2026-10-22-006); what another agent lacks
is a way to find it.

The skills reference, read whole on 2026-10-23 (Claude Code 2.1.308): a skill with `context: fork`
runs as the subagent its `agent:` names, `general-purpose` by default, with the skill's body as
its task. That subagent sees none of the conversation; it loads `AGENTS.md` and a git-status
snapshot (Explore and Plan skip both), not the persona the start hook injected. A fork runs in the
background, with a narrower tool set, unless `background: false`; under `claude -p` it is waited
for either way. `disable-model-invocation: true` takes the description out of Claude's context, and
Claude Code blocks Claude's own call and tells it not to do the steps another way. All silent: a
frontmatter that does not parse loads the skill with no fields, so `context: fork` is lost; a key
Claude Code does not know is ignored; a directory with no `SKILL.md` is no skill.

### Decision

- **A skill is repository markdown and the one home of its procedure.** `AGENTS.md` lists each by
  path; Claude Code runs it by name or by its description, and any other agent opens the file and
  follows the body, the frontmatter being Claude Code's settings. It is never copied into another
  tool's folder. The standard that held the procedure keeps its law and points to the skill.
- **Five skills.** `closeout`, forked, `agent: general-purpose`, `background: false`, so the session
  waits for the kickoff it hands the user. `planning-session` and `document-production` run inline,
  because the first needs the user's confirmation and the second the conversation's content.
  `release` and `pristine-cut` run inline and are the operator's alone (`disable-model-invocation`),
  being one-way doors on GitHub; each refuses outside the template.
- **The forked closeout takes the session's judgement as arguments** (the operator's choice): the
  next persona's slug, then a brief of the next session's tasks, success criteria, reads and open
  questions. Before invoking it the session commits everything durable, as checkpoint discipline
  already requires; the fork refuses an uncommitted tree, reads the rest from git, syncs, scaffolds,
  fills, gates, commits, pushes, watches the run and returns the kickoff.
- **The emergency close moves to `AGENTS.md`**: it is what the main session does when its context is
  critical, and `AGENTS.md` is the file always loaded. The kickoff's section 5, written by the
  scaffold, points to the skill instead of restating the procedure.
- **`scripts/skill_scan.py` keeps the skills honest**, as `gate_runbook_scan.py` keeps the runbook:
  every silent frontmatter failure above is refused; every `pre-commit run` a skill's code names must
  name a hook the config declares, at a stage it declares, with `--all-files`; every script and flag
  must exist; a hook's entry run bare is refused; and `AGENTS.md` must list every skill and no
  missing one. It reads the config with the runbook gate's own reader.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001): the procedures move and a new gate can fail a
  project's own skills.

### Consequences

- TMPL-1.6 decides how the initializer, the updater and the sanitizer own `.claude/skills/`, the
  template-only skills included.
- A project's own skill must be listed in `AGENTS.md` and pass the gate.
- TMPL-1.7 proves a forked closeout end to end.

### Enforcement

`scripts/skill_scan.py` (`frontmatter`, `lint_skill`, `precommit_violations`, `script_violations`,
`scan`) in `skill-scan`, after `skill-scan-selftest`. Taught by [[reference_claude_code_skills]].

### Verification

Fixtures in the skill self-test for every rule, among them an option's value never read as a hook
id and a `SKILL.md` one level too deep; thirty-eight broken variants of the gate, each failing at
least one fixture without crashing (the first draft of one variant changed nothing and passed; it
was rewritten to break the code). On the tree the gate reads five skills and the commands in each.
Live plants in a skill, a hook id and then a stage the config lacks, each failed
`pre-commit run skill-scan --all-files` and a real commit. A grep over the markdown, decision
records and handoff pairs aside, finds each procedure's distinctive command in its skill alone.
`claude -p "/closeout framework-maintainer <brief>"` in a scratch clone ran the skill as a
`general-purpose` subagent whose first command was step 1's `git status --short`; it read step 2
from git and stopped at step 3, whose sync needed an approval `-p` cannot give, the tree untouched.

---

## Decision 2026-10-23-002: The Claude Code paths and the local files are owned by decision; personas adopt through `dev-resources`

**Date:** 2026-10-23
**Made By:** AI (S4), within decisions 2026-10-22-001 and 2026-10-22-005; reported to the operator
at the S4 handover
**Status:** APPROVED; SUPERSEDED (bullets 1, 4 and 5) by 2026-10-23-003
**Builds:** the ownership consequence of 2026-10-22-001 and the adoption consequence of 2026-10-22-005 (TMPL-1.6)
**Affects:** `scripts/new_project.py` (`LOCAL_STATE`, the self-test), `scripts/template_update.py` (`KEEP`, the docstring, the self-test), `scripts/sanitize_template.py` (`LOCAL_STATE`, the self-test), `.gitignore`

### Context

Decision 2026-10-22-001 left the initializer, the updater and the sanitizer to learn the new
paths: `.claude/agents/`, `.claude/skills/`, `.claude/rules/`, `.claude/settings.json`, the
journal and the working notes. TMPL-1.3 renamed the registry from `docs/personas/` in three lists
with no fixture to say they agree. Decision 2026-10-22-005 left a project's own `docs/personas/`
to be carried into `.claude/agents/` when it adopts `v2.0.0`.

Reading the tree for this found `.claude/settings.local.json`, one operator's permissions, ignored
on the template's machine only by that operator's global excludes file: the repository's
`.gitignore` lacked it, so on any other machine it could be committed, and a release would then
have carried one person's grants into every project. `git check-ignore` reads the global file too,
so the journal's own ignore check could not have seen the gap; with `-c core.excludesFile=` it can.

### Decision

- **The registry, `.claude/agents/`, is kept**, being the resources sync's alone: preserved at
  birth, kept by the sanitizer, never written by a release. It is one path in five places (the
  closeout gate reads it, the sync writes it, the initializer, the sanitizer and the updater keep
  it), and a fixture holds all five to the same string.
- **`.claude/skills/`, `.claude/rules/` and `.claude/settings.json` are merged three-way**: the
  template's, which a project may edit and extend. A skill or rule the project added is in
  neither release and never touched. The initializer and the sanitizer leave them as shipped. The
  template-only skills stay in a project: each says it runs only in the template and stops
  elsewhere, and neither's description enters Claude's context.
- **The journal, the notes and `.claude/settings.local.json` are the running session's**
  (`new_project.LOCAL_STATE`): gitignored by the repository's own `.gitignore`, checked with the
  global excludes off; never written or removed by the initializer or the sanitizer, which may run
  from inside a session; kept by the updater.
- **A project's `docs/personas/` reaches `.claude/agents/` through `dev-resources`**, in this
  order: (1) before adopting, the project publishes every persona `dev-resources` lacks with its
  own `v1.0.0` sync; (2) TMPL-2.4 ports `dev-resources`' frozen `docs/personas/` into
  `.claude/agents/` before any project adopts; (3) `template_update.py` deletes the template's
  unedited `docs/personas/` copies, now an ordinary three-way path the target release removed, and
  reports the edited ones; (4) the project's `v2.0.0` `resources_sync.py --apply` writes
  `.claude/agents/`, which the suite needs before it can pass, since the current kickoff's persona
  is looked for there; (5) the project removes what is left of `docs/personas/` once every slug in
  it is in `.claude/agents/` at an equal or higher version. A persona left behind cannot pass
  silently: the closeout gate refuses a kickoff whose persona `.claude/agents/` lacks.
- **Not converted in the project**, because the registry grows only through `--publish` (decision
  2026-09-23-007) and a conversion per project would make copies outside it; the conversion met
  YAML traps when it was done once by hand (decision 2026-10-22-005), and one conversion in
  `dev-resources` serves every project.
- Part of `v2.0.0` (MAJOR, decision 2026-10-22-001).

### Consequences

- TMPL-2.4 runs the adoption in that order on a scratch project first. The updater's own suite
  run after `--apply` fails until step 4 has run; TMPL-2.4 judges whether the updater should say so.
- A machine whose global excludes already cover a local file no longer hides a gap in the
  repository's own `.gitignore`.

### Verification

Fixtures: the initializer's self-test gained five, the updater's four, the sanitizer's one.
Nineteen broken variants across the three scripts, the sync's and the gate's registry path and
`.gitignore`, each failing at least one fixture and none crashing; one was first written so that
it never applied, and was rewritten. On the real tree every tracked `.claude/` path and the three
local files classify as decided: ten three-way, eight kept. Before the `.gitignore` line,
`git -c core.excludesFile= check-ignore` reported `.claude/settings.local.json` not ignored, while
the plain command reported it ignored.

### Enforcement

`scripts/new_project.py` (`LOCAL_STATE`, `--self-test`), `scripts/template_update.py` (`KEEP`,
`--self-test`: the decided paths, the registry across five places, the initializer's agreement),
`scripts/sanitize_template.py` (`LOCAL_STATE`, `--self-test`). Taught by [[reference_template_update]].

---

## Decision 2026-10-23-003: Personas ship as a library in the template, activated per project at its first session

**Amended 2026-10-23 (S5): the four open questions, answered by the operator.**

- **The full team ships in `v2.0.0`.** The roles across the software development lifecycle, data
  science, document management, writing including technical writing, and quality control are
  designed with the operator and written into the library before the release (TMPL-1.9). TMPL-3
  keeps the orchestration, the gated handoffs and the review triggers that build on them.
- **`dev-resources` is retired.** `v2.0.0` carries no sync: `scripts/resources_sync.py`, its
  closeout step and the closeout's unpublished-persona rule go, and the shared knowledge entries
  become the template's own (TMPL-1.10). `dev-resources` keeps serving the projects still on
  `v1.0.0` and is archived once all three have adopted (TMPL-2.4).
- **A project's own personas stay in the project.** The library holds only the personas built and
  released in the template; nothing travels from a project to the template.
- **The updater converts a `v1.0.0` project's `docs/personas/`** into agent files in
  `.claude/agents/`, every one, and removes the old folder (TMPL-1.10). Chosen over a judgement step
  at adoption, with the cost named: every converted persona becomes a live subagent, and the project
  deactivates what it does not use. The conversion is proved against the real `v1.0.0` persona
  files, whose conversion by hand under decision 2026-10-22-005 is the expected output.
- The library's folder is `personas/` at the repository's root, each file in the agent-file shape,
  so activation is a copy (the AI's choice of mechanics). The mechanism is TMPL-1.8.

**Date:** 2026-10-23; amended 2026-10-23
**Made By:** Chair (S4, after its closeout): the library in the template and activation at the first
session, approved as proposed; the mechanics by the AI, to be settled in the build
**Status:** APPROVED
**Supersedes:** 2026-09-23-007; 2026-09-23-002 (personas and shared knowledge in `dev-resources`);
2026-10-22-005 (`dev-resources` holding the registry); 2026-10-23-002 (its first, fourth and fifth
bullets)
**Affects:** `personas/`, `.claude/agents/`, `.claude/skills/team-selection/`, `.claude/skills/closeout/`,
`scripts/session_closeout.py`, `scripts/resources_sync.py` (removed), `.resources-version` (removed),
`scripts/new_project.py`, `scripts/template_update.py`, `scripts/sanitize_template.py`,
`.pre-commit-config.yaml`, `.pre-commit-hooks.yaml`, `AGENTS.md`, `CONSTITUTION.md`, `README.md`,
`TEMPLATE_GUIDE.md`, `docs/standards/session_handoff_standard_v2.0.md`,
`docs/governance/gate_suite_runbook.md`, `.claude/rules/knowledge-entries.md`

### Context

Since decision 2026-09-23-002 the personas have lived in `dev-resources`, a second repository, and
reached each project through a sync that judges versions and grows only through `--publish`
(decision 2026-09-23-007). Decision 2026-10-22-005 moved them into `.claude/agents/` and left
`dev-resources` holding two trees until the three projects adopt `v2.0.0`. The operator wants the
public template itself to ship a base library: a full team covering the software development
lifecycle, data science, document management, writing including technical writing, and quality
control across all three.

Every file in `.claude/agents/` is a live subagent: its description is listed in every session's
context, and Claude may delegate to it unprompted. A full team in that folder would cost context in
every session of every project and make delegation unpredictable.

### Decision

- **The template ships a persona library**, outside `.claude/agents/` and inactive, versioned by
  template releases. Adding a persona to it forces no project to act, so it is a MINOR change: the
  library is how the template grows to cover new use cases without loading every project.
- **`.claude/agents/` is a project's roster**: only the personas that project activated. The
  session's persona, the kickoff's persona and a delegated subagent all come from the roster.
- **At a project's first session a skill builds the roster:** it asks the operator which
  specializations the project needs, scans the library, recommends personas, drafts new ones for
  any gap, and copies the chosen ones into `.claude/agents/`. More can be activated later the same way.
- **The gates follow:** the closeout keeps refusing a kickoff whose persona the roster lacks; a
  roster persona taken from the library is held to a library version, and a newer library version
  is reported. The append-only rule of decision 2026-09-23-006 holds in both places.
- **Part of `v2.0.0`** (MAJOR, decision 2026-10-22-001), built as TMPL-1.8 before TMPL-1.7 proves
  the substrate, since it changes the birth that proof observes.

### Open, to settle with the operator at the start of TMPL-1.8

- How much of the library ships in `v2.0.0`. Recommended: the mechanism and a starter set, the full
  team designed in TMPL-3.1's design session and shipped as MINOR releases.
- Whether `dev-resources` is retired, its few shared knowledge entries folded into the template,
  or kept for knowledge alone.
- Whether a persona a project drafts for itself can be proposed back to the library, and how.
- How a `v1.0.0` project's `docs/personas/` reaches its roster when it adopts `v2.0.0`.

### Supersession

Marked on both sides by TMPL-1.8, with the code: decisions 2026-09-23-007 (the sync, whole),
2026-09-23-002 (personas and shared knowledge in `dev-resources`; its append-only rule and the
published hooks stand), 2026-10-22-005 (`dev-resources` holding the registry; the agent-file shape
and the persona from the start hook stand) and 2026-10-23-002 (its first, fourth and fifth bullets,
the registry as the sync's and the adoption through `dev-resources`).

### Consequences

- TMPL-1.8 is opened; TMPL-1.7 depends on it.
- TMPL-2.2's technical writer becomes a library persona; TMPL-2.4's port of `dev-resources`' frozen
  tree is replaced by whatever the adoption question settles; TMPL-3.1's design session designs the
  full team as library personas.

### Verification

Fixtures: the closeout gate's library rules, the start hook's roster notes, and the initializer's,
the updater's and the sanitizer's checks on the roster and the library. Twenty broken variants
across those five scripts, each failing at least one fixture without crashing; three were first
written wrong (one changed nothing, one targeted a line already rewritten, one crashed instead of
failing) and were rewritten. Live plants in the real tree: a roster copy edited at the same version
failed `session-closeout-check` as `library-drift` and was refused by a real commit; one bumped ahead
of the library failed as `library-fork`, and was refused too. The library bumped past the roster
passed and printed nothing, because pre-commit hides a passing hook's output; that is why the start
hook now names such a persona itself. A scratch birth from the committed template:
`new_project.py --apply` exit 0 with the suite green, the template's roster removed and the library
whole, `session-verify` exit 0 at S1, and a `claude -p` session whose init event listed only the
built-in agents, with the `team-selection` skill available.

### Enforcement

`scripts/session_closeout.py` (`LIBRARY`, `library_state`, `NOTE_RULES`, `library_findings`) in
`session-closeout-check`; `scripts/session_start.py` (`roster_lines`); `scripts/new_project.py`
(`CLEAR_GLOBS`), `scripts/sanitize_template.py` (`NEVER_RESET`) and `scripts/template_update.py`
(`KEEP`), cross-checked in the updater's self-test; `.claude/skills/team-selection/SKILL.md`, held by
`skill-scan`. Taught by [[reference_session_closeout]], [[reference_claude_code_agents_md]],
[[reference_resources_sync]] and [[reference_template_update]].
