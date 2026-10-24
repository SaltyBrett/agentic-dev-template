---
authority: the gate suite — what each hook blocks, in run order, and how to run it alone
implements: [2026-09-23-001, 2026-09-22-001, 2026-10-22-002]
verified: 2026-10-23
---

# Gate-Suite Runbook

One section per hook in `.pre-commit-config.yaml`, in the order pre-commit runs them. Each names
its stage, the self-test it pairs with, what it blocks, why it exists, and the command that runs it
alone. `scripts/gate_runbook_scan.py` keeps this page and the config in step on every commit: a
hook with no section, a section naming no hook, a section out of run order, or a stage line that
disagrees with the config fails the commit. What a section says a gate blocks, and why, is prose
the check cannot read; the decision and knowledge entry each section links hold the reasoning, and
this page does not restate it.

Every H2 below is a hook id, but the last: `## Version log`, this page's record of its changes,
which `doc-authority-scan` holds to the decisions that name the page (decision 2026-10-23-011).
Prose that is not about one hook belongs here, above the first.

**Running the suite.** `pre-commit run --all-files` runs every `pre-commit`-stage hook and nothing
else. The `manual`-stage hooks are run by hand, most at the session boundaries; the `commit-msg`
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
**Why:** [[reference_kb_freshness]] (once `CONSTITUTION.md` §6.3) and decisions 2026-09-20-004 and
2026-09-23-003; [[reference_kb_frontmatter_validation]], [[reference_framework_decisions]].
**Alone:** `pre-commit run kb-freshness-scan --all-files` (add `--list` by direct invocation to see
which entries the gate reaches)

## `doc-authority-selftest`

**Stage:** `pre-commit`
**Pairs with:** `doc-authority-scan`, which it precedes.
**Blocks:** a commit when a fixture of the authority gate fails: frontmatter that claims authority
and does not parse read as no authority, a quoted `verified:` accepted, a version log that is not
the last section or sits in fenced code read as the log, a malformed or out-of-order row accepted,
`fact:` with no fact or a citation of a story that does not cite the row's decision accepted, a
decision from the cutoff without `**Affects:**` passed, a Done story or one in an `[EXAMPLE]` epic
read as queueing a change, a hash that did not introduce its row passed, `--stamp` writing a row
that is not this repository's; in a project, the template's rows or decisions judged there, or the
project's own passed unjudged; a copied document's history read as its own, or a rename's cut. For
`doc-queue`: a story queued in the previous session failed or one queued earlier passed, a Done
story judged, a note quoted in a code span read as a note, a note naming no session, two notes or
a session to come passed, a queued story naming no authority or two, or citing no decision, passed,
no session known or an unreadable index read as nothing queued. For the approval gate: a real
epic passed with no approved PRD or architecture, a draft, a reopened draft, a document with no
authority or outside its folder counted as approved, two approved in one folder passed, an
architecture built from an older PRD version or with an unquoted `prd:` passed, a skip that is not
APPROVED or sits in the framework's log counted, a skip naming another stage passed, the template or
a project before its first real epic judged, and the rule left out of the commit's check. A fixture
that raises fails; it never crashes the self-test.
**Why:** decision 2026-10-22-002 and the build's decisions 2026-10-23-010, 2026-10-23-015,
2026-10-23-019 and 2026-10-23-020; [[reference_doc_authority]].
**Alone:** `pre-commit run doc-authority-selftest --all-files --verbose`

## `doc-authority-scan`

**Stage:** `pre-commit`
**Pairs with:** `doc-authority-selftest`.
**Blocks:** for every markdown file git would commit whose frontmatter carries `authority:`: a
frontmatter that does not parse to a scope, an `implements:` list and an unquoted `verified:`
date; two documents claiming one scope; a `verified:` that predates a change to a decision the
document implements; a missing or malformed `## Version log`; a row that is neither `fact:` with
its fact nor the change of a story that cites its decision; a stored commit hash that is not the
commit that introduced the row, following renames but never a copy. For every decision dated 2026-10-22 or later: a body without
`**Affects:**`, and an authority it names whose version log cites it nowhere while no open story
cites both. In a project, what the template wrote is judged in the template: a row citing only
framework decisions is held to neither its marker nor its hash, and a framework decision to
neither its `**Affects:**` nor its record. In a project whose tracker holds a real epic, the
approval gate: no approved PRD in `docs/prd/` or architecture in `docs/architecture/` (one document
each, `status: approved` with the `authority:` line) where no APPROVED decision of the project's
log carries `**Skips:** prd` or `**Skips:** architecture`; an approved architecture whose `prd:` is
not the approved PRD's newest version; a `**Skips:**` naming another stage. A decision index that
cannot be read fails; a shallow clone exits 2.
**Why:** decisions 2026-10-22-002, 2026-10-23-010 and 2026-10-23-015; the approval gate, 2026-10-23-008,
2026-10-23-014 and 2026-10-23-020; [[reference_doc_authority]], [[reference_kb_freshness]].
**Alone:** `pre-commit run doc-authority-scan --all-files` (by direct invocation: `--list` for the
registry and the gate's reach, `--stamp` to fill each committed `pending` row, `--history <doc>`
for the commit git derives for each row)

## `doc-queue`

**Stage:** `manual`
**Pairs with:** `doc-authority-selftest`, whose queue fixtures it reads by. Run at cold start by the
`SessionStart` hook, which reports its verdict and each queued story, and by the closeout skill,
which reports it and never waits on it; never on a commit, since its verdict depends on the session
at work.
**Blocks:** nothing on a commit. Run, it exits 1 for a story not Done whose row carries a bare
`Queued: S<N>` note, the technical writer's queue, when the session at work is later than S<N+1>,
or the note names a session to come, or names none or appears twice, or the story names other than
exactly one authority in a code span or cites no indexed decision; and when no session can be read
from sprint-status or a decision index cannot be read. A note quoted in a code span is the
convention, not a note. The session at work is the newest sprint-status entry, plus one while the
next kickoff exists. A passing run lists each queued story with the drain that clears it, the
doc-drain skill run on its document.
**Why:** decisions 2026-10-22-002, 2026-10-23-016 and 2026-10-23-019; [[reference_doc_authority]].
**Alone:** `pre-commit run doc-queue --hook-stage manual --all-files --verbose`

## `session-closeout-selftest`

**Stage:** `pre-commit`
**Pairs with:** `session-closeout-check`, `session-closeout` and `session-verify`, all three of
which share its linters.
**Blocks:** a commit when a linter fails a fixture: an unfilled scaffold passing, an extra handoff
section accepted, a kickoff's section 1 that neither names the agent nor copies its prompt
accepted, an agent file whose frontmatter does not parse or whose list item is a mapping accepted,
the module needing PyYAML to read a prompt, an unscoped, dead or restating rule passing, a glob
reading `*` across directories, a kickoff task citing no story passing, tracker
statistics that do not reconcile passing, a Done story on an undone dependency passing, an example
row in a live sprint passing, a fresh project's closeout producing no pair.
**Why:** decisions 2026-09-21-001 and 2026-10-22-005; [[reference_session_closeout]].
**Alone:** `pre-commit run session-closeout-selftest --all-files --verbose`

## `session-closeout-check`

**Stage:** `pre-commit`
**Pairs with:** `session-closeout-selftest`. The per-commit state gate.
**Blocks:** a stray file in `sprint/handoffs/`, an incomplete or non-consecutive pair, more than
two session numbers outside `archive/`, a handoff or kickoff with the wrong headings, an unfilled
token, an unresolved wikilink or unindexed decision ID, a kickoff naming a persona the roster
lacks, a kickoff whose section 1 is neither the scaffold's line naming the agent nor a verbatim copy
of its prompt, or naming a persona version the roster is not at, a task citing a story absent from
the tracker, an agent file in `.claude/agents/` or `personas/` of the wrong shape (frontmatter that does not parse
as YAML, which Claude Code would skip silently; a `name` that is not the filename stem; a list that
is not strings), a persona whose body (the Invocation) differs from the committed copy without a
higher `version:`, a version that went down or has no changelog item, a roster persona that
differs from its library copy at the same version or runs ahead of it (one the library has moved
past is noted, not blocked), tracker Summary Statistics that do not equal the counted rows, a story `In Progress` or
`Done` whose listed dependency is not `Done` (`dependency-order`), in a project whose tracker holds
a non-example epic an `[EXAMPLE]` row or heading or an unfilled `{{TOKEN}}` in the tracker,
sprint-status or the decision log outside inline or fenced code (`live-placeholder`; the template,
with no `.project-profile`, is exempt), a sprint-status whose newest entry is not headed
`## S<N> — date — title` or that holds more than ten, a `[[slug]]` in any text file git would
commit that resolves to no knowledge entry and is not in the gate's allow set (the convention's
own placeholders and the fixture slug), an `AGENTS.md` over the Codex project-doc cap, and a rule
under `.claude/rules/` whose `paths:` does not parse as a list of globs (Claude Code would load it
in every session), that no file git would commit matches (it would never load), or that repeats a
sentence of `AGENTS.md`.
**Why:** decisions 2026-09-21-001 (amended for the tree-wide wikilink rule), 2026-09-23-002,
2026-09-24-001 (the tracker's two rules), 2026-10-22-005 (agent files), 2026-10-22-006 (rules) and
2026-10-23-003 (the library and the roster);
[[reference_session_closeout]].
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
**Why:** decisions 2026-09-21-001 and 2026-09-22-003 (amended); [[reference_session_closeout]],
[[reference_precommit_stash]].
**Alone:** `pre-commit run session-verify --hook-stage manual --all-files`. The flag is
load-bearing here too: without it pre-commit stashes an unstaged edit to a tracked file, the tree
the gate reads is clean, and a dirty tree passes.

## `session-journal-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. `scripts/session_journal.py` is a Claude Code `PostToolUse` and
`PostToolUseFailure` hook (`.claude/settings.json`), context rather than enforcement.
**Blocks:** a commit when the journal writer loses or tears a line under concurrent appends, writes
its header twice, misreads a Bash exit code, or records a tool it should not; when the notes'
three-section shape stops being checked; or when `.gitignore` no longer covers the journal and the
notes, which keeps them out of pre-commit's stash and out of the scanners.
**Why:** decisions 2026-10-22-001 and 2026-10-22-004; [[reference_claude_code_hooks]].
**Alone:** `pre-commit run session-journal-selftest --all-files --verbose`

## `session-start-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. `scripts/session_start.py` is the Claude Code `SessionStart` hook.
**Blocks:** a commit when the start report can exceed Claude Code's 10,000-character context cap,
cuts a high-priority section before a low one, runs a gate or a pull after compaction, runs the
verify without `--all-files`, counts the user-level `~/.claude/CLAUDE.md` as a shadow, takes
the session number from another session's journal line, leaves the kickoff's persona out of a
session not run as that agent (or repeats it in one that is), or leaves out a roster persona the
library has moved past (or repeats a drift `session-verify` already fails, or crashes where
PyYAML is absent).
**Why:** decisions 2026-10-22-001, 2026-10-22-005 and 2026-10-23-003; [[reference_claude_code_hooks]].
**Alone:** `pre-commit run session-start-selftest --all-files --verbose`

## `session-stop-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. `scripts/session_stop.py` is the Claude Code `Stop` hook.
**Blocks:** a commit when the stop check lets a turn end with a tracked sprint file uncommitted or
the working notes older than the newest uncommitted file, sends a turn back twice, sends one back in
plan mode, or counts the journal as uncommitted work (which would make the notes stale forever).
**Why:** decision 2026-10-22-001; [[reference_claude_code_hooks]].
**Alone:** `pre-commit run session-stop-selftest --all-files --verbose`

## `new-project-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. The initializer runs once, at a derived project's birth, and never on a
commit here; only its guards are proved.
**Blocks:** a commit when an initializer guard fails a fixture: a token fill that would rewrite a
`${{ secrets.X }}` expression or the convention's own `{{PLACEHOLDER}}`, the framework decisions,
the decision log or the knowledge base appearing in a mutating list, a regenerated tracker that still carries real stories
or statistics that do not reconcile at zero, the template's own origin not refused, a public
project not refused without `--public` or an unreadable visibility treated as a verdict, a mutating
list reaching `.claude/` or the session's local files, or a local file the repository's own
`.gitignore` does not cover (read from the tree, global excludes off).
**Why:** decisions 2026-09-20-009, 2026-09-22-002, 2026-09-25-001 and 2026-10-23-002; [[reference_derived_project_start]], [[reference_template_update]].
**Alone:** `pre-commit run new-project-selftest --all-files --verbose`

## `birth-probe-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate on a commit. The probe, `scripts/birth_probe.py`, makes a scratch project
from a committed revision through that revision's initializer, whose suite run is the verdict; a
birth takes minutes, so GitHub runs it in the `birth` job of `.github/workflows/gates.yml`, once per
profile, skipped in a project, and an operator runs it by hand.
**Blocks:** a commit when a probe rule fails a fixture over a stub initializer: a refused birth
reported green, a birth from the working tree or holding an untracked file instead of the committed
tree, a scratch that is not a fresh repository with one commit, the initializer run without
`--apply` or the profile asked for, the source's index written or a `GIT_*` variable or
`CLAUDE_PROJECT_DIR` reaching the birth, the scratch left behind, a profile skipped when none is
named, a project's revision born instead of refused, an unknown revision judged.
**Why:** decision 2026-10-23-017; [[reference_ci_backstop]].
**Alone:** `pre-commit run birth-probe-selftest --all-files --verbose`; the probe itself,
`python3 scripts/birth_probe.py [--rev <revision>] [--profile commercial|gcc]`

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
knowledge base, the personas, the sync stamp, a filled file, a profile file, anything under
`.claude/` or the session's local files; the refusal not the initializer's inverse.
**Why:** decisions 2026-09-23-003 and 2026-10-23-002; [[reference_template_sanitizer]].
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
project that runs it by mistake is told so and nothing is judged. The reset, and the cut around
it, are the pristine-cut skill.
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
reported clean, template markdown compared without the profile strip, a `.claude/` path or a
local file classified other than decided, the roster's or the library's path differing among the
state gate, the initializer, the sanitizer and this map; a `v1.0.0` persona converted to anything
but the agent file, or a file the shape cannot hold converted rather than refused; the roster
overwritten, the sync's stamp kept, or a marked entry's body touched at adoption; a `.gitignore`
changed on both sides merged other than by union, the project's lines first, or any other path
merged by union.
**Why:** decisions 2026-09-22-004, 2026-09-23-003, 2026-10-23-002, 2026-10-23-005 and 2026-10-23-007; [[reference_template_update]].
**Alone:** `pre-commit run template-update-selftest --all-files`

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

## `skill-scan-selftest`

**Stage:** `pre-commit`
**Pairs with:** `skill-scan`, which it precedes.
**Blocks:** a commit when the skill checker fails a fixture: a command read from prose, a
frontmatter that does not parse or an unknown key passing, a hook id the config lacks or a stage it
does not declare passing, a `pre-commit run` without `--all-files` passing, a flag its script never
names passing, a hook's entry run bare passing, a skill missing from `AGENTS.md` passing, an
unreadable config read as an empty suite; a preset naming a persona the library lacks, an
unparsable or second presets block, a connection pinned to a tag, a branch or nothing, or a
connection in the template's `.mcp.json` or in a project without its persona passing. A fixture
that raises is a failure.
**Why:** decisions 2026-10-23-001 and 2026-10-23-013; [[reference_claude_code_skills]],
[[reference_blender_mcp]].
**Alone:** `pre-commit run skill-scan-selftest --all-files --verbose`

## `skill-scan`

**Stage:** `pre-commit`
**Pairs with:** `skill-scan-selftest`.
**Blocks:** a skill under `.claude/skills/` that would load differently than written (line 1 not
`---`, YAML that does not parse, a key Claude Code does not know, `name:` other than the
directory, no description or one past the listing cap, `context` other than `fork`, an `agent` or
`background` without it, an `agent` that names no agent, a flag that is not a boolean, no body, a
directory with no `SKILL.md`); a command in its code that names a hook the config lacks, a stage
the hook does not declare, a `pre-commit run` without `--all-files`, a script or flag that does not
exist, or a hook's entry run bare; and a skill `AGENTS.md` does not name by path, or a path it names
with no skill. In the team-selection skill, its one fenced `yaml` block: a preset that is not a
list of personas `personas/` holds, each named once; a connection that names no library persona or
is pinned to no exact release (a version, or a git source at a full commit). And `.mcp.json`
holding a connection in the template, in a project whose roster lacks its persona, or other than
the skill gives it. Prose is not read. Exits 2, never 0, without PyYAML.
**Why:** decisions 2026-10-23-001 and 2026-10-23-013; [[reference_claude_code_skills]],
[[reference_blender_mcp]].
**Alone:** `pre-commit run skill-scan --all-files`

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

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.5 | 2026-10-23 | 2026-10-23-020, 2026-10-23-008 | `doc-authority-selftest` and `doc-authority-scan` hold the approval gate: in a project with a real epic, an approved PRD and architecture or a logged `**Skips:**` (TMPL-5.3) | d7ad4d7 |
| 1.4 | 2026-10-23 | 2026-10-23-019, 2026-10-23-016 | `doc-queue` added after `doc-authority-scan`, a manual hook run at cold start over the stories marked `Queued: S<N>`; `doc-authority-selftest` holds its fixtures; the preamble no longer counts the manual hooks (TMPL-2.2) | 0dcccd2 |
| 1.3 | 2026-10-23 | 2026-10-23-018, 2026-10-23-017 | `birth-probe-selftest` added after `new-project-selftest`: the probe's rules over a stub initializer, the probe itself run on GitHub once per profile (TMPL-2.7) | 19537c4 |
| 1.2 | 2026-10-23 | 2026-10-23-013 | `skill-scan-selftest` and `skill-scan` hold the team presets and the connections of the team-selection skill, and `.mcp.json` (TMPL-5.6) | 8180f9e |
| 1.1 | 2026-10-23 | 2026-10-23-015 | `doc-authority-selftest` and `doc-authority-scan` say that in a project the template's rows and decisions are judged in the template, and that a row's commit is found following renames but never a copy (TMPL-2.6) | e155edf |
| 1.0 | 2026-10-23 | 2026-10-23-011, 2026-10-22-002, 2026-10-23-001, 2026-10-23-003, 2026-10-23-005, 2026-10-23-007, 2026-10-23-010 | Marked as the authority for the gate suite (TMPL-2.3); reflects the skill gate, the persona library, the adoption fixtures, the `.gitignore` union and the authority gate. The README catalog's change to `skill-scan` (2026-10-23-009) is queued in TMPL-5.5 | 515f1a5 |
