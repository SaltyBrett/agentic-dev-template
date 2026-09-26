# Gate-Suite Runbook

One section per hook in `.pre-commit-config.yaml`, in the order pre-commit runs them. Each names
its stage, the self-test it pairs with, what it blocks, why it exists, and the command that runs it
alone. `scripts/gate_runbook_scan.py` keeps this page and the config in step on every commit: a
hook with no section, a section naming no hook, a section out of run order, or a stage line that
disagrees with the config fails the commit. What a section says a gate blocks, and why, is prose
the check cannot read; the decision and knowledge entry each section links hold the reasoning, and
this page does not restate it.

Every H2 below is a hook id. Prose that is not about one hook belongs here, above the first.

**Running the suite.** `pre-commit run --all-files` runs every `pre-commit`-stage hook and nothing
else. The two `manual`-stage hooks are run by the agent at the session boundaries; the `commit-msg`
hook needs a message file. Both forms are given in their sections. Installing the hooks, once per
clone, is `TEMPLATE_GUIDE.md` Step 6; the same suite runs on GitHub on every push
([[reference_ci_backstop]]). Invoke a gate through `pre-commit`, never a bare interpreter
([[reference_precommit_interpreter]]).

**Consuming these gates elsewhere.** `.pre-commit-hooks.yaml` publishes three of them for another
repository to pin by `rev`: `persona-lint` (the persona rule of `session-closeout-check`, alone),
`kb-frontmatter-scan` and `commit-attribution`. The sections below describe this repository's own
config, where the same scripts run as local hooks; what publishing changed and why is in
[[reference_published_hooks]].

**Self-tests.** Every gate script proves its own parser against in-memory fixtures before the gate
runs, as a hook of its own ordered just before it. A self-test blocks the commit when a fixture
fails, which means the gate after it can no longer be trusted to read what it checks. The fixtures
are run against deliberately broken code before they are trusted; the decision each pair links
records what broke.

## `agent-execution-identity-selftest`

**Stage:** `pre-commit`
**Pairs with:** `agent-execution-identity`, which it precedes.
**Blocks:** a commit when the identity guard's config parser fails a fixture: keys under an
unrelated table read as present, malformed TOML read as loadable, a diagnostic that names the wrong
table.
**Why:** decision 2026-09-20-005; [[reference_execution_identity_config]].
**Alone:** `pre-commit run agent-execution-identity-selftest --all-files --verbose`

## `agent-execution-identity`

**Stage:** `pre-commit`
**Pairs with:** `agent-execution-identity-selftest`. The zero-th gate: the first hook, and the
first command of every cold start.
**Blocks:** a commit made under an identity named for a sandbox or offline principal (by uid, with
the environment as a secondary signal), and a `.codex/config.toml` that is unparseable, lacks the
required approval keys at top level, weakens them in any table, or sets `sandbox_mode` at any
depth. Exits 2, never 0, without a TOML parser.
**Why:** decisions 2026-07-30-001 and 2026-09-20-005; [[reference_agent_execution_identity]],
[[reference_execution_identity_config]].
**Alone:** `pre-commit run agent-execution-identity --all-files --verbose` (`--verbose` shows the
PASS line, which names the identity and its source; pre-commit hides a passing hook's output
otherwise).

## `project-profile-selftest`

**Stage:** `pre-commit`
**Pairs with:** `project-profile`, which it precedes.
**Blocks:** a commit when profile stripping fails a fixture: the wrong half kept, an unclosed marker
swallowing the rest of a document, nested or unknown markers accepted.
**Why:** decision 2026-09-20-009; [[reference_project_profiles]].
**Alone:** `pre-commit run project-profile-selftest --all-files --verbose`

## `project-profile`

**Stage:** `pre-commit`
**Pairs with:** `project-profile-selftest`.
**Blocks:** a profile marker that is unbalanced or nested, an unknown value in `.project-profile`,
and, in a derived project, a block for a foreign profile that survived initialization. The template
itself has no profile and keeps every block.
**Why:** decision 2026-09-20-009; [[reference_project_profiles]].
**Alone:** `pre-commit run project-profile --all-files`

## `content-rules-selftest`

**Stage:** `pre-commit`
**Pairs with:** `banned-feature-scan`, which it precedes.
**Blocks:** a commit when the scanner's content-rule channel fails a fixture: an identifier spelling
that does not collapse to its hash, a multi-word identifier missed across punctuation, a content
rule that stops at `EXCLUDE_FILES`, an `allow` set that is not empty where it must be.
**Why:** decisions 2026-09-20-002 and 2026-09-20-007; [[reference_content_provenance]].
**Alone:** `pre-commit run content-rules-selftest --all-files --verbose`

## `banned-feature-scan`

**Stage:** `pre-commit`
**Pairs with:** `content-rules-selftest`.
**Blocks:** two channels over every file git would commit. Banned patterns: the GCC-incompatible
feature set under the `gcc` profile, the always-banned set under every profile, both filtered by
`EXCLUDE_FILES` so governance documents may name what they ban. Content rules, which bypass that
list: a bare-interpreter invocation of a gate script, and any employer identifier, matched by hash
so the rule never publishes the name. Each violation prints its fix.
**Why:** decisions 2026-09-20-002, 2026-09-20-007 and 2026-09-20-009; [[reference_content_provenance]],
[[reference_precommit_interpreter]], [[reference_project_profiles]].
**Alone:** `pre-commit run banned-feature-scan --all-files`

## `kb-frontmatter-selftest`

**Stage:** `pre-commit`
**Pairs with:** `kb-frontmatter-scan`, which it precedes.
**Blocks:** a commit when the index cross-check fails a fixture: a filename quoted in the INDEX
header counted as a row, an entry with no row passing, a row whose file is gone passing, a missing
`## Entries` heading read as zero rows.
**Why:** decision 2026-09-20-003, with the boundary rule of 2026-09-20-004;
[[reference_kb_frontmatter_validation]].
**Alone:** `pre-commit run kb-frontmatter-selftest --all-files --verbose`

## `kb-frontmatter-scan`

**Stage:** `pre-commit`
**Pairs with:** `kb-frontmatter-selftest`. Runs before `kb-freshness-scan` because it validates the
input that gate consumes.
**Blocks:** a knowledge entry whose frontmatter no YAML parser can load, lacks `teaches:` or
`verified:`, spells `verified:` as anything but an unquoted ISO date, or is read differently by
the freshness gate's parser than by YAML; an entry with no INDEX row, and an INDEX row with no
file. Exits 2, never 0, without PyYAML.
**Why:** decision 2026-09-20-003; [[reference_kb_frontmatter_validation]].
**Alone:** `pre-commit run kb-frontmatter-scan --all-files`

## `kb-freshness-selftest`

**Stage:** `pre-commit`
**Pairs with:** `kb-freshness-scan`, which it precedes.
**Blocks:** a commit when the decision-index parser fails a fixture: a table inside a decision body
read as a decision, a `|`-prefixed body line shaped like an index row accepted, a missing index
heading read as zero decisions, the two logs not read as one set, a duplicate ID not taken from
the framework file, a missing index in either log not raising.
**Why:** decisions 2026-09-20-004 and 2026-09-23-003; [[reference_kb_frontmatter_validation]].
**Alone:** `pre-commit run kb-freshness-selftest --all-files --verbose`

## `kb-freshness-scan`

**Stage:** `pre-commit`
**Pairs with:** `kb-freshness-selftest`.
**Blocks:** a knowledge entry whose `verified:` date predates a change to a decision it `teaches:`,
where a change is an amendment date on the decision's row or the date of a decision recorded as
superseding or amending it; an entry teaching an ID in neither decision index (the project's
`sprint/decision-log.md` and the template's `docs/governance/framework_decisions.md`, read as one
set); an unstamped entry; and a decision index that cannot be located in a log that exists. It
flags staleness risk, not wrongness: clearing it means re-verifying and correcting the entry, then
bumping the date.
**Why:** `CONSTITUTION.md` §6.3 and decisions 2026-09-20-004 and 2026-09-23-003;
[[reference_kb_frontmatter_validation]], [[reference_framework_decisions]].
**Alone:** `pre-commit run kb-freshness-scan --all-files` (add `--list` by direct invocation to see
which entries the gate reaches)

## `session-closeout-selftest`

**Stage:** `pre-commit`
**Pairs with:** `session-closeout-check`, `session-closeout` and `session-verify`, all three of
which share its linters.
**Blocks:** a commit when a linter fails a fixture: an unfilled scaffold passing, an extra handoff
section accepted, a persona copy that drifted from the registry accepted, a kickoff task citing no
story passing, tracker statistics that do not reconcile passing, a Done story on an undone
dependency passing, an example row in a live sprint passing, a fresh project's closeout
producing no pair.
**Why:** decision 2026-09-21-001; [[reference_session_closeout]].
**Alone:** `pre-commit run session-closeout-selftest --all-files --verbose`

## `session-closeout-check`

**Stage:** `pre-commit`
**Pairs with:** `session-closeout-selftest`. The per-commit state gate.
**Blocks:** a stray file in `sprint/handoffs/`, an incomplete or non-consecutive pair, more than
two session numbers outside `archive/`, a handoff or kickoff with the wrong headings, an unfilled
token, an unresolved wikilink or unindexed decision ID, a kickoff naming an unregistered persona,
drifting from its invocation or naming a persona version the registry is not at, a task citing a
story absent from the tracker, a persona file of the wrong shape, a persona whose Invocation differs
from the committed copy without a higher `version:`, a version that went down or has no Changelog
bullet, tracker Summary Statistics that do not equal the counted rows, a story `In Progress` or
`Done` whose listed dependency is not `Done` (`dependency-order`), in a project whose tracker holds
a non-example epic an `[EXAMPLE]` row or heading or an unfilled `{{TOKEN}}` in the tracker,
sprint-status or the decision log outside inline or fenced code (`live-placeholder`; the template,
with no `.project-profile`, is exempt), a sprint-status whose newest entry is not headed
`## S<N> — date — title` or that holds more than ten, a `[[slug]]` in any text file git would
commit that resolves to no knowledge entry and is not in the gate's allow set (the convention's
own placeholders and the fixture slug), and an `AGENTS.md` over the Codex project-doc cap.
**Why:** decisions 2026-09-21-001 (amended for the tree-wide wikilink rule), 2026-09-23-002 and
2026-09-24-001 (the tracker's two rules); [[reference_session_closeout]].
**Alone:** `pre-commit run session-closeout-check --all-files`

## `session-closeout`

**Stage:** `manual`
**Pairs with:** `session-closeout-selftest`. Run once, at session end, by the agent.
**Blocks:** ending a session that produced no pair for the next one, or whose produced pair fails
any rule of `session-closeout-check`. It first archives every pair older than the session being
closed, so the folder holds at most the consumed pair and the produced one.
**Why:** decisions 2026-09-21-001 and 2026-09-22-003; [[reference_session_closeout]],
[[reference_precommit_stash]].
**Alone:** `pre-commit run session-closeout --hook-stage manual --all-files`. The flag is
load-bearing: without it pre-commit stashes unstaged edits to tracked files first and the gate
judges the last commit's tracker and sprint-status.

## `session-verify`

**Stage:** `manual`
**Pairs with:** `session-closeout-selftest`. Run once, at cold start, before any build work.
**Blocks:** starting a session whose predecessor did not close out: the pair for this session is
missing or fails a rule, a stale pair sits outside `archive/`, or the tree is dirty. A fresh project
at S1 with no incoming pair passes.
**Why:** decision 2026-09-21-001; [[reference_session_closeout]].
**Alone:** `pre-commit run session-verify --hook-stage manual` (it requires a clean tree, so there
is nothing for pre-commit to stash)

## `new-project-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. The initializer runs once, at a derived project's birth, and never on a
commit here; only its guards are proved.
**Blocks:** a commit when an initializer guard fails a fixture: a token fill that would rewrite a
`${{ secrets.X }}` expression or the convention's own `{{PLACEHOLDER}}`, the framework decisions,
the decision log or the knowledge base appearing in a mutating list, a regenerated tracker that still carries real stories
or statistics that do not reconcile at zero, the template's own origin not refused, a public
project not refused without `--public` or an unreadable visibility treated as a verdict.
**Why:** decisions 2026-09-20-009, 2026-09-22-002 and 2026-09-25-001; [[reference_derived_project_start]].
**Alone:** `pre-commit run new-project-selftest --all-files --verbose`

## `sanitize-template-selftest`

**Stage:** `pre-commit`
**Pairs with:** `sanitize-template-check`, which is manual. The sanitizer runs once, before the
template's pristine cut, and never on a commit; only its guards are proved, and they read nothing
from the tree, so the hook passes in every derived project.
**Blocks:** a commit when a sanitizer guard fails a fixture: a sprint-status entry above S1, a
`TMPL-` story row, a file in either archive, a pair, or the probe repository's name not named; a
prose mention of a `TMPL-` ID or of the name in the script itself reported; a regenerated
sprint-status not at S1 or a regenerated tracker that carries a story, loses its `{{DATE}}` token
or does not reconcile at zero; a plan that reaches the framework decisions, the decision log, the
knowledge base, the personas, the sync stamp, a filled file or a profile file; the refusal not
the initializer's inverse.
**Why:** decision 2026-09-23-003; [[reference_template_sanitizer]].
**Alone:** `pre-commit run sanitize-template-selftest --all-files --verbose`

## `sanitize-template-check`

**Stage:** `manual`
**Pairs with:** `sanitize-template-selftest`. Run by the template maintainer to prove the tree is
pristine; this repository fails it until the cut, which is why it is not a commit gate.
**Blocks:** nothing on a commit. Run alone it exits 1 while build state remains and names each
item: a sprint-status entry numbered above S1, a `TMPL-` story row in the tracker, a file in
`sprint/archive/` or `sprint/handoffs/archive/`, a handoff or kickoff in `sprint/handoffs/`, and
the probe repository's name in any text file git would commit, the script itself excepted. It
refuses to run where `origin` is not the template, the inverse of the initializer's refusal, so a
project that runs it by mistake is told so and nothing is judged. The reset itself is
`python3 scripts/sanitize_template.py --apply`, dry run without the flag.
**Why:** decision 2026-09-23-003; [[reference_template_sanitizer]].
**Alone:** `pre-commit run sanitize-template-check --hook-stage manual --all-files`

## `template-update-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. The updater runs in a derived project, never on a commit here; the
self-test is what lets a project trust the copy it fetches.
**Blocks:** a commit when the updater's map or a merge fails a fixture: a path classified against
the initializer's lists, the project's decision log merged rather than kept or the framework
decisions kept rather than merged, a keyed insert landing at the table's end instead of the top, an
`[EXAMPLE]` row travelling, both-sides-changed lines silently taking the template's, a conflict
reported clean, template markdown compared without the profile strip.
**Why:** decisions 2026-09-22-004 and 2026-09-23-003; [[reference_template_update]].
**Alone:** `pre-commit run template-update-selftest --all-files`

## `resources-sync-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. The sync runs at session closeout, never on a commit; the closeout gate
(`session-closeout`) is what refuses a persona the synced ref lacks.
**Blocks:** a commit when a sync verdict fails a fixture: a higher fetched version not taken, a
higher local version overwritten, same-version or unversioned differences silently picked, a
fetched entry without `source: dev-resources` accepted, `--take` reaching a path the fetched tree
lacks, or the ownership rule drifting from the updater's.
**Why:** decision 2026-09-23-007; [[reference_resources_sync]].
**Alone:** `pre-commit run resources-sync-selftest --all-files --verbose`

## `template-version-selftest`

**Stage:** `pre-commit`
**Pairs with:** `template-version`, which it precedes.
**Blocks:** a commit when the per-tag judgement fails a fixture: a malformed tag name, a constant
that disagrees with the tag, a missing bump type, a lightweight tag reported as a missing bump
instead of by its cause, the earliest tag wrongly asked for a bump.
**Why:** decisions 2026-09-20-006 and 2026-09-22-002; [[reference_template_versioning]],
[[reference_ci_annotated_tags]].
**Alone:** `pre-commit run template-version-selftest --all-files --verbose`

## `template-version`

**Stage:** `pre-commit`
**Pairs with:** `template-version-selftest`.
**Blocks:** a tag whose name is not `vMAJOR.MINOR.PATCH`, a tag pointing at a commit whose
`TEMPLATE_VERSION` constant differs from it, and, for every tag but the earliest, an annotation
that does not name MAJOR, MINOR or PATCH, or a lightweight tag where an annotated one is expected.
Skips cleanly in a repository with no tags, which is every derived project. Prints a note when
`main` is ahead of the last release.
**Why:** decisions 2026-09-20-006 and 2026-09-22-002; [[reference_template_versioning]],
[[reference_ci_annotated_tags]].
**Alone:** `pre-commit run template-version --all-files`

## `gate-runbook-selftest`

**Stage:** `pre-commit`
**Pairs with:** `gate-runbook`, which it precedes.
**Blocks:** a commit when this page's checker fails a fixture: a hook id in a second repo entry
missed, an H2 inside a fenced block counted as a section, sections out of order passing, a stage
line that disagrees with the config passing, an unparsable or empty config read as an empty suite.
**Why:** decision 2026-09-23-001; [[reference_gate_runbook]].
**Alone:** `pre-commit run gate-runbook-selftest --all-files --verbose`

## `gate-runbook`

**Stage:** `pre-commit`
**Pairs with:** `gate-runbook-selftest`.
**Blocks:** a hook in `.pre-commit-config.yaml` with no section on this page, a section on this
page naming no hook, sections out of the config's run order, a section whose `**Stage:**` line
is missing or disagrees with the hook's `stages:`, a hook that declares no `stages:` at all, a
config that cannot be parsed or holds no hooks, and a non-manual stage that no step of
`.github/workflows/gates.yml` runs (a plain `pre-commit run` covers the pre-commit stage; any
other needs `--hook-stage <stage>`), or a workflow that is missing or unreadable. Exits 2, never
0, without PyYAML.
**Why:** decision 2026-09-23-001, with the stages rule of 2026-09-20-001 and the CI-step rule of
2026-09-22-001; [[reference_gate_runbook]], [[reference_ci_backstop]].
**Alone:** `pre-commit run gate-runbook --all-files`

## `commit-attribution`

**Stage:** `commit-msg`
**Pairs with:** no self-test; the patterns are literal and the message is one file.
**Blocks:** a commit message carrying AI attribution: a `Co-Authored-By:` naming an agent, model
or vendor address, an agent session trailer, a generated-with line, or the robot emoji. Comment
lines and everything below the `--verbose` scissors line are ignored. It refuses; it never rewrites
the message. This stage exists only in a clone that installed both hook types.
**Why:** decision 2026-09-20-001; [[reference_commit_attribution_gate]].
**Alone:** write a message to a file and run the stage against it, in both directions:

```bash
printf 'checkpoint: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n' > /tmp/msg
pre-commit run --hook-stage commit-msg --commit-msg-filename /tmp/msg --all-files   # must FAIL
printf 'checkpoint: x\n\nClean body.\n' > /tmp/msg
pre-commit run --hook-stage commit-msg --commit-msg-filename /tmp/msg --all-files   # must PASS
```

`pre-commit run --all-files` never exercises this stage; a green suite says nothing about it.

## `gitleaks`

**Stage:** `pre-commit`
**Pairs with:** no self-test; an upstream hook, pinned by `rev:`.
**Blocks:** a hardcoded secret entering the tree. GitHub scans public repositories only, so on a
private one this is the only secret control. The explicit `stages:` is mandatory: the upstream
manifest declares none, and a hook without one runs at every installed stage.
**Why:** decision 2026-09-20-008. No knowledge entry; the decision holds the whole rationale.
**Alone:** `pre-commit run gitleaks --all-files` (the first run in a fresh clone builds the
gitleaks environment and needs the network once)
