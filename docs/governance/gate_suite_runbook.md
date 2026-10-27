---
authority: the gate suite (what each hook blocks, in run order, and how to run it alone)
implements: []
verified: 2026-10-24
---

# Gate-Suite Runbook

One section per hook in `.pre-commit-config.yaml`, in the order pre-commit runs them. Each names
its stage, the self-test it pairs with, what it blocks, and the command that runs it alone.
`scripts/gate_runbook_scan.py` keeps this page and the config in step on every commit: a hook with
no section, a section naming no hook, a section out of run order, or a stage line that disagrees
with the config fails the commit. What a section says a gate blocks is prose the check cannot read.

Every H2 below is a hook id, but the last: `## Version log`, this page's record of its changes,
which `doc-authority-scan` holds to the decisions that name the page.
Prose that is not about one hook belongs here, above the first.

**Running the suite.** `pre-commit run --all-files` runs every `pre-commit`-stage hook and nothing
else. The `manual`-stage hooks are run by hand, most at the session boundaries; the `commit-msg`
hook needs a message file. Both forms are given in their sections. Installing the hooks, once per
clone, is step 3 of the walkthrough in `TEMPLATE_GUIDE.md`; the same suite runs on GitHub on every push. Invoke a gate through `pre-commit`, never a bare interpreter.

**Self-tests.** Every gate script proves its own parser against in-memory fixtures before the gate
runs, as a hook of its own ordered just before it. A self-test blocks the commit when a fixture
fails, which means the gate after it can no longer be trusted to read what it checks. The fixtures
are run against deliberately broken code before they are trusted.

## `agent-execution-identity-selftest`

**Stage:** `pre-commit`
**Pairs with:** `agent-execution-identity`, which it precedes.
**Blocks:** a commit when the identity guard's config parser fails a fixture: keys under an
unrelated table read as present, malformed TOML read as loadable, a diagnostic that names the wrong
table.
**Alone:** `pre-commit run agent-execution-identity-selftest --all-files --verbose`

## `agent-execution-identity`

**Stage:** `pre-commit`
**Pairs with:** `agent-execution-identity-selftest`. The zero-th gate: the first hook, and the
first command of every cold start.
**Blocks:** a commit made under an identity named for a sandbox or offline principal (by uid, with
the environment as a secondary signal), and a `.codex/config.toml` that is unparseable, lacks the
required approval keys at top level, weakens them in any table, or sets `sandbox_mode` at any
depth. Exits 2, never 0, without a TOML parser.
**Alone:** `pre-commit run agent-execution-identity --all-files --verbose` (`--verbose` shows the
PASS line, which names the identity and its source; pre-commit hides a passing hook's output
otherwise).

## `content-rules-selftest`

**Stage:** `pre-commit`
**Pairs with:** `banned-feature-scan`, which it precedes.
**Blocks:** a commit when the scanner fails a fixture: a content rule that stops at `EXCLUDE_FILES`,
the knowledge base falling out of the content rules, a rule without its patterns, fix or allow set,
a feature a project bans missed, or a file with none refused; a home path on macOS, Linux or Windows
missed, or a placeholder, a path under `~` or a URL refused; a text file of any type not scanned, or a
binary one read.
**Alone:** `pre-commit run content-rules-selftest --all-files --verbose`

## `banned-feature-scan`

**Stage:** `pre-commit`
**Pairs with:** `content-rules-selftest`.
**Blocks:** two channels over every text file git would commit, whatever its extension, a binary
file skipped. Banned patterns: the features a project
bans in `BANNED_PATTERNS`, none in the template, filtered by `EXCLUDE_FILES` so the law and the
decisions may name what they ban. Content rules, which bypass that list: a bare-interpreter
invocation of a gate script, and an absolute home-directory path, a placeholder after the home root
allowed. Each violation prints its fix.
**Alone:** `pre-commit run banned-feature-scan --all-files`

## `kb-frontmatter-selftest`

**Stage:** `pre-commit`
**Pairs with:** `kb-frontmatter-scan`, which it precedes.
**Blocks:** a commit when the index cross-check fails a fixture: a filename quoted in the INDEX
header counted as a row, an entry with no row passing, a row whose file is gone passing, a missing
`## Entries` heading read as zero rows.
**Alone:** `pre-commit run kb-frontmatter-selftest --all-files --verbose`

## `kb-frontmatter-scan`

**Stage:** `pre-commit`
**Pairs with:** `kb-frontmatter-selftest`. Runs before `kb-freshness-scan` because it validates the
input that gate consumes.
**Blocks:** a knowledge entry whose frontmatter no YAML parser can load, lacks `teaches:` or
`verified:`, spells `verified:` as anything but an unquoted ISO date, or is read differently by
the freshness gate's parser than by YAML; an entry with no INDEX row, and an INDEX row with no
file. Exits 2, never 0, without PyYAML.
**Alone:** `pre-commit run kb-frontmatter-scan --all-files`

## `kb-freshness-selftest`

**Stage:** `pre-commit`
**Pairs with:** `kb-freshness-scan`, which it precedes.
**Blocks:** a commit when the decision-index parser fails a fixture: a table inside a decision body
read as a decision, a `|`-prefixed body line shaped like an index row accepted, a missing index
heading read as zero decisions, the two logs not read as one set, an ID indexed in both logs not
raising, a missing index in either log not raising.
**Alone:** `pre-commit run kb-freshness-selftest --all-files --verbose`

## `kb-freshness-scan`

**Stage:** `pre-commit`
**Pairs with:** `kb-freshness-selftest`.
**Blocks:** a knowledge entry whose `verified:` date predates a change to a decision it `teaches:`,
where a change is the newest amendment date on the decision's row or the date of a decision recorded as
superseding or amending it; an entry teaching an ID no decision index holds; an unstamped entry; and a decision index that cannot be located in a log that exists. It
flags staleness risk, not wrongness: clearing it means re-verifying and correcting the entry, then
bumping the date.
**Alone:** `pre-commit run kb-freshness-scan --all-files` (add `--list` by direct invocation to see
which entries the gate reaches)

## `doc-authority-selftest`

**Stage:** `pre-commit`
**Pairs with:** `doc-authority-scan`, which it precedes.
**Blocks:** a commit when a fixture of the authority gate fails: frontmatter that claims authority
and does not parse read as no authority, a quoted `verified:` accepted, a version log that is not
the last section or sits in fenced code read as the log, a malformed or out-of-order row accepted,
`fact:` with no fact or a citation of a story that does not cite the row's decision accepted, a
decision from the cutoff without `**Affects:**` passed, an authority's path written bare there
passed, or one also in a code span, a longer path or a decision before the cutoff refused, a Done story or one in an `[EXAMPLE]` epic
read as queueing a change, a hash that did not introduce its row passed, `--stamp` filling a row
whose version no commit holds; in a project, a row read as another repository's and passed
unjudged; a copied document's history read as its own, or a rename's cut. For
`doc-queue`: a story queued in the previous session failed or one queued earlier passed, a Done
story judged, a note quoted in a code span read as a note, a note naming no session, two notes or
a session to come passed, a queued story naming no authority or two, or citing no decision, passed,
no session known or an unreadable index read as nothing queued, an ID indexed in both logs read
rather than failed. For the approval gate: a real
epic passed with no approved PRD or architecture; a first draft, a document with no authority, no
row, another status or outside its folder counted as approved, or a revision reopened with its
authority and rows not standing at its last version; two in one folder passed; an approved
architecture built from an older PRD version or with an unquoted `prd:` passed, or a reopened one
held to the newest; a skip that is not APPROVED or sits in another log counted, a skip of an
ungated stage counted as an approval, or one naming no launch stage passed; the template or a
project before its first real epic judged; the rule left out of the commit's check. For the
starting row each of the template's documents arrives with: one held to a citation, a marker or
a hash, one above another row, a second or one whose version is above the newer row's passed,
`template` in one cell alone or no version read as one, one read as a PRD's approval. A fixture
that raises fails; it never crashes the self-test.
**Alone:** `pre-commit run doc-authority-selftest --all-files --verbose`

## `doc-authority-scan`

**Stage:** `pre-commit`
**Pairs with:** `doc-authority-selftest`.
**Blocks:** for every markdown file git would commit whose frontmatter carries `authority:`: a
frontmatter that does not parse to a scope, an `implements:` list and an unquoted `verified:`
date; two documents claiming one scope; a `verified:` that predates a change to a decision the
document implements; a missing or malformed `## Version log`; a row that is neither `fact:` with
its fact nor the change of a story that cites its decision; a stored commit hash that is not the
commit that introduced the row, following renames but never a copy; a starting row, `template`
in its Decision and Commit cells, that is not the last row or carries `template` in one cell
alone. Each of the template's documents arrives with that one row, its version and date, and a
project's own rows go above it; it cites nothing and stores no hash, so no other rule reads it.
For every decision dated 2026-10-22 or later: a body without
`**Affects:**`; an authority it names whose version log cites it nowhere while no open story
cites both; an authority's path it writes outside a code span only, which would go unread. In a project whose tracker holds a real epic, the
approval gate: no PRD in `docs/prd/` or architecture in `docs/architecture/` standing approved (one
document each with the `authority:` line and a row, `status: approved` or `status: draft` while
reopened for revision, when its newest row stands) where no APPROVED decision of the project's log
carries `**Skips:** prd` or `**Skips:** architecture`; an architecture with `status: approved` whose
`prd:` is not the PRD's newest version; a `**Skips:**` naming no stage of `/project-launch`. A decision index that
cannot be read fails; a shallow clone exits 2.
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
**Alone:** `pre-commit run doc-queue --hook-stage manual --all-files --verbose`

## `session-closeout-selftest`

**Stage:** `pre-commit`
**Pairs with:** `session-closeout-check`, `session-closeout` and `session-verify`, all three of
which share its linters.
**Blocks:** a commit when a linter fails a fixture: an unfilled scaffold passing, an extra handoff
section accepted, a kickoff's section 1 that does not name the agent accepted, a U+2014 form of an
entry heading, a pair's title or a changelog item read, an unindexed decision citation passing or
a prefixed ID or a log's `**Deletes:**` line read as one, an allow-set decision ID an index holds or
an allow-set slug naming a knowledge entry passing, an agent file whose frontmatter does not parse or whose list item is a mapping accepted,
the module needing PyYAML to read a prompt, an unscoped, dead or restating rule passing, a glob
reading `*` across directories, a kickoff task citing no story passing, tracker
statistics that do not reconcile passing, a Done story on an undone dependency passing, an example
row in a live sprint passing, a fresh project's closeout producing no pair, an entry being closed
still headed `emergency checkpoint` or holding the initializer's `### Next` passing, or a mention
in a title, a fenced `### Next`, an older entry or an unreadable heading refused.
**Alone:** `pre-commit run session-closeout-selftest --all-files --verbose`

## `session-closeout-check`

**Stage:** `pre-commit`
**Pairs with:** `session-closeout-selftest`. The per-commit state gate.
**Blocks:** a stray file in `sprint/handoffs/`, an incomplete or non-consecutive pair, more than
two session numbers outside `archive/`, a handoff or kickoff with the wrong headings, an unfilled
token, an unresolved wikilink or unindexed decision ID, a kickoff naming a persona the roster
lacks, a kickoff whose section 1 is not the scaffold's line naming the agent, or naming a persona
version the persona never held (above the roster's, absent from its changelog, or none), a task
citing a story absent from
the tracker, an agent file in `.claude/agents/` or `personas/` of the wrong shape (frontmatter that does not parse
as YAML, which Claude Code would skip silently; a `name` that is not the filename stem; a list that
is not strings), a persona whose body (the Invocation) differs from the committed copy without a
higher `version:`, a version that went down or has no changelog item, a roster persona that
differs from its library copy at the same version or runs ahead of it (one the library has moved
past is noted, not blocked), tracker Summary Statistics that do not equal the counted rows, a story `In Progress` or
`Done` whose listed dependency is not `Done` (`dependency-order`), in a project whose tracker holds
a non-example epic an unfilled `{{TOKEN}}` in the tracker, sprint-status or the decision log
outside inline or fenced code (`live-placeholder`; the template, with no `.template-version`, is
exempt, and an `[EXAMPLE]` entry, numbered zero, stays as each log's form), a sprint-status whose newest entry is not headed
`## S<N> - date - title` with hyphens, or that holds more than ten, a `[[slug]]` in any text file git would
commit that resolves to no knowledge entry and is not in the gate's allow set (the convention's
own placeholders and the fixture slug), an unprefixed decision ID in such a file outside `sprint/`
that no decision index holds (`decision-citation`; a decision log's `**Deletes:**` line, the record
of what a decision deleted, and the fixtures' invented IDs excepted), a decision ID in that allow
set that a decision index holds or a slug in the wikilink allow set that names a knowledge entry
(`allow-set`: every check and the strip pass what the sets hold), an `AGENTS.md` over the Codex
project-doc cap, and a rule
under `.claude/rules/` whose `paths:` does not parse as a list of globs (Claude Code would load it
in every session), that no file git would commit matches (it would never load), or that repeats a
sentence of `AGENTS.md`.
**Alone:** `pre-commit run session-closeout-check --all-files`

## `session-closeout`

**Stage:** `manual`
**Pairs with:** `session-closeout-selftest`. Run once, at session end, by the agent.
**Blocks:** ending a session that produced no pair for the next one, or whose produced pair fails
any rule of `session-closeout-check`; or whose sprint-status entry is still headed `emergency
checkpoint`, or still holds the initializer's `### Next`, a record saying the session is still
open. It first archives every pair older than the session being closed, so the folder holds at
most the consumed pair and the produced one.
**Alone:** `pre-commit run session-closeout --hook-stage manual --all-files`. The flag is
load-bearing: without it pre-commit stashes unstaged edits to tracked files first and the gate
judges the last commit's tracker and sprint-status.

## `session-verify`

**Stage:** `manual`
**Pairs with:** `session-closeout-selftest`. Run once, at cold start, before any build work.
**Blocks:** starting a session whose predecessor did not close out: the pair for this session is
missing or fails a rule, a stale pair sits outside `archive/`, or the tree is dirty. A fresh project
at S1 with no incoming pair passes.
**Alone:** `pre-commit run session-verify --hook-stage manual --all-files`. The flag is
load-bearing here too: without it pre-commit stashes an unstaged edit to a tracked file, the tree
the gate reads is clean, and a dirty tree passes.

## `issue-log-selftest`

**Stage:** `pre-commit`
**Pairs with:** `issue-log`, which shares its rules. It reads nothing from the tree but section 12
of the sprint management standard, so it passes in every derived project.
**Blocks:** a commit when an issue-log rule fails a fixture: an entry's field out of order or
missing, a kind, severity, status, date, reporter, ID list or commit outside the template's form,
a bug without steps to reproduce or a request with them, an empty section; a status its stories
or links do not bear out, each status tried both ways; a story or decision that does not exist, a
code review log naming an issue the log lacks or the example's; an index row missing, extra,
doubled or disagreeing with its entry; a heading that is neither the index nor an issue; an ID
gap, an ID filed twice, two prefixes; the writer's next ID, its prefix, a filed issue that would
fail the gate, an update that leaves the index behind; a field outside a terminal not named as
missing, a choice in a terminal not asked again; the report's counts. And when the fields, kinds,
severities, statuses or sections differ from the standard's section 12.
**Alone:** `pre-commit run issue-log-selftest --all-files --verbose`

## `issue-log`

**Stage:** `pre-commit`
**Pairs with:** `issue-log-selftest`.
**Blocks:** a commit whose `sprint/issue-log.md` holds an entry that departs from the template's
form, an index row that disagrees with its entry, an ID out of sequence, a status the named
stories' status in the tracker does not bear out, or a named story or decision that does not
exist; or whose `docs/code_review_log.md` names an issue the log does not hold. A project with no
issue log has no issues and passes. The example entry is held to the form alone. A change through
`python3 scripts/issue_log.py --file` or `--update <ID>` is refused before it is written if it
would fail here.
**Alone:** `pre-commit run issue-log --all-files`

## `session-journal-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. `scripts/session_journal.py` is a Claude Code `PostToolUse` and
`PostToolUseFailure` hook (`.claude/settings.json`), context rather than enforcement.
**Blocks:** a commit when the journal writer loses or tears a line under concurrent appends, writes
its header twice, misreads a Bash exit code, or records a tool it should not; when the notes'
three-section shape stops being checked; or when `.gitignore` no longer covers the journal and the
notes, which keeps them out of pre-commit's stash and out of the scanners.
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
**Alone:** `pre-commit run session-start-selftest --all-files --verbose`

## `session-stop-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. `scripts/session_stop.py` is the Claude Code `Stop` hook.
**Blocks:** a commit when the stop check lets a turn end with a tracked sprint file uncommitted or
the working notes older than the newest uncommitted file, sends a turn back twice, sends one back in
plan mode, or counts the journal as uncommitted work (which would make the notes stale forever).
**Alone:** `pre-commit run session-stop-selftest --all-files --verbose`

## `subagent-ceiling-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. `scripts/subagent_ceiling.py` is the Claude Code `PreToolUse` hook on
`Agent` and `Skill`, and the `SessionStart` and `PostModelSwitch` hooks that keep the session's
model; it declares `onFailure: block`, so a crash or a timeout refuses the call.
**Blocks:** a commit when a fixture of the ceiling fails: a model family misread from a full ID or
an alias, or an unknown name placed; an indented line or a file with no frontmatter read as a key;
the kept model not preferred to the transcript's, or the transcript's oldest request read in place
of its newest; a spawn's model or effort resolved out of the documented order, or a built-in agent
with no model passed; a spawn or a skill above the session's model or effort allowed, `tuned`
allowing a model change, `max` an effort change, or a call keeping the session's model and effort
refused; an unknown mode, model or effort allowed to change anything; a change allowed while the
session's model is unknown; a refusal that does not name the mode and the ceiling. And when one of
the script's functions is over the coding standard's production limits.
**Alone:** `pre-commit run subagent-ceiling-selftest --all-files --verbose`

## `new-project-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. The initializer runs once, at a derived project's birth, and never on a
commit here; only its guards are proved.
**Blocks:** a commit when an initializer guard fails a fixture: a token fill that would rewrite a
`${{ secrets.X }}` expression or the convention's own `{{PLACEHOLDER}}`, the decision log or the
knowledge base appearing in a mutating list, a regenerated tracker that still carries real stories
or statistics that do not reconcile at zero, the template's own origin not refused, a public
project not refused without `--public` or an unreadable visibility treated as a verdict, a mutating
list reaching `.claude/` or the session's local files, a local file the repository's own
`.gitignore` does not cover (read from the tree, global excludes off), an S1 entry whose one next
step is not `/project-launch`, or a born `README.md` that is filled rather than regenerated, does
not name the project, its scope, its platform and the guide, or that the writing gate refuses as
a production document; `--apply` let through with pre-commit not installed, or refused with no
command that installs it; an S1 entry claiming hooks the initializer never installed.
**Alone:** `pre-commit run new-project-selftest --all-files --verbose`





## `template-update-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. The updater runs in a derived project, never on a commit here; the
self-test is what lets a project trust the copy it fetches.
**Blocks:** a commit when the updater's map or a merge fails a fixture: a path classified against
the initializer's lists, the project's decision log merged rather than kept, an unedited copy of a file a release no
longer ships kept or an edited one removed, a keyed insert landing at the table's end instead of
the top, both-sides-changed lines silently taking the template's, a conflict reported clean, a
`.claude/` path or a local file classified other than decided, a path in a class beside keep,
merge, three-way and special, the roster's or the library's path differing among the state gate,
the initializer and this map; a target release planned by an updater other than its own, or one
that carries none accepted; a `.gitignore` changed on both sides merged other than by union, the
project's lines first, or any other path merged by union.
**Alone:** `pre-commit run template-update-selftest --all-files`



## `gate-runbook-selftest`

**Stage:** `pre-commit`
**Pairs with:** `gate-runbook`, which it precedes.
**Blocks:** a commit when this page's checker fails a fixture: a hook id in a second repo entry
missed, an H2 inside a fenced block counted as a section, sections out of order passing, a stage
line that disagrees with the config passing, an unparsable or empty config read as an empty suite.
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
**Alone:** `pre-commit run gate-runbook --all-files`

## `skill-scan-selftest`

**Stage:** `pre-commit`
**Pairs with:** `skill-scan`, which it precedes.
**Blocks:** a commit when the skill checker fails a fixture: a command read from prose, a
frontmatter that does not parse or an unknown key passing, a hook id the config lacks or a stage it
does not declare passing, a `pre-commit run` without `--all-files` passing, a flag its script never
names passing, a hook's entry run bare passing, a skill missing from `AGENTS.md` passing, a skill
missing from the guide's catalog or named only outside its section passing, a catalog path with no
skill passing, a guide with no catalog, an empty guide or no guide at all read as an empty catalog,
an unreadable config read as an empty suite; a preset naming a persona the library lacks, an
unparsable or second presets block, a connection pinned to a tag, a branch or nothing, or a
connection in the template's `.mcp.json` or in a project without its persona passing. A fixture
that raises is a failure.
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
exist, or a hook's entry run bare; a skill `AGENTS.md` does not name by path, or a path it names
with no skill; and a skill the `## Catalog` section of `TEMPLATE_GUIDE.md` does not name by path, a
path it names with no skill, a guide with no such section, or no guide at all. Only that section is
read, so a path the walkthrough mentions catalogues nothing. In the team-selection skill, its one fenced `yaml` block: a preset that is not a
list of personas `personas/` holds, each named once; a connection that names no library persona or
is pinned to no exact release (a version, or a git source at a full commit). And `.mcp.json`
holding a connection in the template, in a project whose roster lacks its persona, or other than
the skill gives it. Prose is not read. Exits 2, never 0, without PyYAML.
**Alone:** `pre-commit run skill-scan --all-files`

## `code-standard-selftest`

**Stage:** `pre-commit`
**Pairs with:** `code-standard` and `code-standard-range`, which share its rules.
**Blocks:** a commit when a fixture of the coding standard's gate fails: a `case`, an `and`, a
comprehension's `if` or a nested function's decisions miscounted; a docstring or a nested
function's lines counted as the parent's code; a parameter kind dropped; a measurer that misses a
function, or a file Python cannot parse, passing recall; in Rust, a match arm, a guard, an `&&` of a
let chain, a closure's decisions or a nested `fn`'s miscounted, a bare `loop` counted, a comment or
a nested `fn`'s lines read as code, `self` or a trait's signature dropped, a Bevy system parameter
counted (an `Option` of one, a path to one), the recall lexer fooled by a raw string, a nested
comment, a quote character, a lifetime, a pointer type or a raw name, a function read with a parse
error judged or its error given to its parent, or a missing parser passed; an unchanged function judged, or a helper
in a test file held to the test limits; a worse finding, or a row with no response from the Chair,
read as logged; an edited audit log, or one with other columns, accepted; a stray generated marker
passed; a deletion touching nothing; a clone, an uncovered line or a linter finding outside the
change counted; a `ruff format --diff` hunk's context line counted, a replacement read as an
insertion, an inserted run counted at no line, at the wrong one or past the file's end, the
no-newline marker read as a line, or a removed line that reads like a file header taken for one; a
tool failure raised instead of recorded as `unmeasured`; the audit run on a commit
that touches no manifest; a profile not built here read as Python; in Rust's slots, rustfmt's
context lines counted, clippy's repeat counted twice, a compiler error read as a lint or a
secondary span read, lcov's last report of a line winning over its most hits, a cargo-deny warning
counted or a rejected license missed, `#[tokio::test]` or `#[cfg(test)]` misread, a toolchain not
pinned to an exact version or a Python profile held to one, a clippy `allow` passed, `Cargo.lock`
or `build.rs` no trigger, a tool off its pinned version run, a failing cargo read as clean, or a
report that does not parse crashing; a suggested log row split by a `|` in its detail, or a
suppression named by its pattern; in TypeScript, an inline callback measured on its own or a named
arrow, a field, an object property or a default export left unnamed, a `??`, a logical assignment
or a `catch` missed, a `default` counted as a case, a `this` annotation counted, a `.tsx` file read
with the TypeScript grammar, a class's or an object's prefix dropped, a parse error ignored, or a
compiler that cannot count passed; in TypeScript's slots, an `it` or `test` callback, through
`.each` or `.only`, not measured as a test, a `.tsx` file not judged, a range or a missing lockfile
or `packageManager` accepted, yarn 1 read as yarn 2, an `eslint-disable` passed, `tsconfig.json` no
trigger, prettier's context lines counted, ESLint's absolute path kept or a message with no line
read, a failing prettier, tsc, audit or license listing read as clean, an audit report without its
key or yarn 1's summary read as clean, an `OR` or `AND` license misread, a dev dependency's license
judged, a dependency's dependencies not walked, npm's license object or yarn 1's table misread, or
lcov not read as the coverage report. And when a number the gate holds
differs from the standard's section 2, or one of the gate's own functions is over the production limits.
A fixture that raises fails; it never crashes the self-test.
**Alone:** `pre-commit run code-standard-selftest --all-files --verbose`

## `code-standard`

**Stage:** `pre-commit`
**Pairs with:** `code-standard-selftest`.
**Blocks:** in a project with `code-profile.yaml`, a commit whose staged change holds a finding
`docs/code_review_log.md` does not yet answer: a changed function over complexity 15, 60 code lines
or 5 parameters (a test function over 10 or 100); a file the measurer could not read in full; a
suppressing comment or a stray generated-code marker on a changed line; a clone of existing code
among the added lines; a changed function's new lines under 80% covered by the project's own tests;
a ruff format, ruff or mypy `--strict` finding on a changed line, a format finding being a line
ruff rewrites or removes, or the line a run it inserts precedes, never a hunk's context line; a
vulnerability or a license outside the policy when a manifest changes; a tool that could not run.
In a Rust project (`profile: rust`, `rust-toolchain.toml` naming an exact toolchain or the profile
refused), the same over `.rs` files: `cargo fmt --check`, one `cargo clippy` run (a warning a lint,
an error the compiler's), cargo-llvm-cov 0.9.1's lcov and cargo-deny 0.20.2's advisories and
licenses, a `#[test]` function held to the test limits. In a TypeScript project (`profile:
typescript`, `package.json` pinning prettier, eslint and typescript exactly with a lockfile, and
for pnpm or yarn an exact `packageManager`, or the profile refused), the same over `.ts` and `.tsx`
files: prettier's output compared with each changed file, ESLint's JSON, `tsc --noEmit --strict`,
the project's lcov, and the audit and license listing of the manager the lockfile names, licenses
judged over production dependencies; an `it` or `test` callback held to the test limits. A finding
is answered by a log row naming its place and rule, a value at least its own and the Chair's
response: no code change is ever required. And always a log whose base rows were edited or
removed. Reports, never pauses on, a file grown past 500 lines and the review-trigger paths
touched. Without the profile it says the standard is not adopted and passes.
**Alone:** `pre-commit run code-standard --all-files` (it judges the staged change whatever files are named)

## `code-standard-range`

**Stage:** `manual`
**Pairs with:** `code-standard-selftest`. Run by CI over the commits a push or pull request carries:
for a normal push those it carried, for a pull request those past its base. Where the push's
`before` is unknown (a new repository, a new branch or a force-push), the default branch's whole
history from the empty tree, or another ref's commits the default branch lacks; never the tip
alone.
**Blocks:** what `code-standard` blocks, over the range `CODE_STANDARD_RANGE` names instead of the
staged change, and the dependency and license audit every time, so a vulnerability published since
the last manifest change still surfaces.
**Alone:** `CODE_STANDARD_RANGE=<base>..<head> pre-commit run code-standard-range --hook-stage manual --all-files`

## `story-artifacts-selftest`

**Stage:** `pre-commit`
**Pairs with:** `story-artifacts`, which it precedes.
**Blocks:** a commit when a fixture of the team's gate fails: a team standard whose role-map section
holds no table, or whose triggers section holds no list, read as empty; a folder no tracker story
names, an artifact naming another story, a file whose `stage:` is not its name, a stage recording
no `model` or `effort` or one the ceiling's ranking cannot place, a file that is no stage or a
stage the type lacks passed; a stage written before a required earlier one, an input not
the stage just before, or a role started from a failed input passed; a stage older than its input's
last change, in one commit with it, or made on a branch that never saw it passed, or a stage in the
commit being made over a committed input, or a rebuild that removes every stage after it, refused; a
role the map does not allow
or the roster lacks, or the builder verifying or reviewing its own work, passed; a brief with no
numbered criteria, or a passing verify that misses or fails one, passed; a release or Done past a
trigger the Chair has not approved, a trigger named outside the standard, a build commit's trigger
path missed, a commit the repository lacks, or a release past an auth, crypto or external-service
trigger with no security stage, passed, or a trigger demanded before the release; a review finding
unanswered in the log once the story moves on passed, or demanded before; a release with no CI run,
or a story marked Done without its last stage, passed; an optional stage required. And when one of
the gate's own functions is over the coding standard's production limits. A fixture that raises
fails; it never crashes the self-test.
**Alone:** `pre-commit run story-artifacts-selftest --all-files --verbose`

## `story-artifacts`

**Stage:** `pre-commit`
**Pairs with:** `story-artifacts-selftest`.
**Blocks:** for every folder under `docs/stories/`, a story the team standard does not allow: a
folder or artifact naming no tracker story; a brief missing or its type unknown; a stage file whose
frontmatter does not parse with `story`, `stage`, `role`, `input`, `status`, `triggers`, `model`
and `effort`, its model one `scripts/subagent_ceiling.py` ranks and its effort a level; a stage
the type lacks; a stage written before a required earlier one, an input other than the stage just
before, or a role started from an input that did not pass; a stage not committed after its input's
last change, read from git history: the commit that last changed the stage must hold the input's
last change and not be that commit, a file differing from `HEAD` belonging to the commit being made,
so a rebuild removes every stage after it in its own commit; a role the standard's role map does not
allow at the stage or the roster does not hold; the builder as verifier or reviewer; a brief with
no numbered acceptance criteria, or a passing verify that does not check each; a trigger named
outside the standard's list, a build commit the repository lacks; once the story releases or is
Done, a hit trigger (declared, a build commit on a stack profile trigger path, or the release
itself) with no approval from the Chair in `approvals.md`, or a release past an auth, crypto or
external-service trigger with no security stage; once the story moves past its review or security
stage, a finding there unanswered in `docs/code_review_log.md`; a release with no `run:`; a story
the tracker marks Done whose last stage is not passing. The role map and the triggers are read from
`docs/standards/team_standard_v1.0.md`, which, unreadable, stops the gate with exit 2, as does a
shallow clone, whose cut history cannot date a stage. With no `docs/stories/` it passes.
**Alone:** `pre-commit run story-artifacts --all-files`

## `writing-standard-selftest`

**Stage:** `pre-commit`
**Pairs with:** `writing-standard`, which it precedes.
**Blocks:** a commit when a fixture of the writing gate fails: a character table, phrase table or
voice table that cannot be read, or one with no `any other` row, read as empty; a profile key,
voice, audience, agent slug or allow entry the standard does not allow passed, or a profile that
does not parse read; a production glob that decides nothing passed, or a development one refused;
the `template:` rules applied in a project or never in the template; a voice whose `name` is not
its file's, whose `tables` the standard lacks, or a custom voice whose sample is missing, in two
blocks or under 200 words, passed; a character off the allowed set passed, or an accented letter,
a carriage return before a newline or a run counted twice refused; a heading with a comma, a
semicolon, a closing mark or over 8 words passed, or a label, a code span, a link or a dash
counted; a phrase missed across a line break, in the frontmatter or with U+2019, or found in a code
span, a code block or across a paragraph break, or a `list end` phrase flagged mid-sentence; a
development reference passed in production or refused in development; an allowed string not
exempting the text inside it, exempting across case, or printing a line unwidened or unescaped; a
Word heading style, a footer, a slide title or a sheet's strings unread by the text mode, or a PDF
read as text. And when one of the gate's own functions is over the coding standard's production
limits, or the script holds a character off ASCII. A fixture that raises fails; it never crashes
the self-test.
**Alone:** `pre-commit run writing-standard-selftest --all-files --verbose`

## `writing-standard`

**Stage:** `pre-commit`
**Pairs with:** `writing-standard-selftest`.
**Blocks:** every markdown file git tracks, judged whole in the voice and audience
`writing-profile.yaml` gives it: a character off printable ASCII, tab, newline and letters; a
heading with a comma or a semicolon, a closing `.`, `!`, `;` or `:`, or over 8 words, the label of
a format the gates read not counted; a phrase of the voice's tables outside code spans and code
blocks; in a production file, a development reference. The closed records, `sprint/archive/` and
`sprint/handoffs/archive/`, are not judged: each was judged whole while it was live. A finding an
occurrence of an `allow:` string holds is exempt; each prints its fix and the allow line. Before
any file, the profile and the voices are judged: a key, voice, audience or agent the standard does
not allow, a production glob that decides nothing, a custom voice without its sample. The
standard, the voices or the profile unreadable stops the gate with exit 2. `--which <path>` prints
a file's voice and audience; `--text <file> --source <draft.md>` judges a produced deliverable as
production.
**Alone:** `pre-commit run writing-standard --all-files --verbose`

## `humanize-selftest`

**Stage:** `pre-commit`
**Pairs with:** no gate. `scripts/humanize.py` is the humanizer's mechanical half, which the
`/humanize` skill runs by hand; its self-test runs on every commit.
**Blocks:** a commit when a fixture of the humanizer fails: a certain fix that is no row of the
writing standard's character table, or U+2014, U+2013 or U+00B7 fixed by script; a curly quote,
the ellipsis, a special space, an invisible character, an arrow, a box-drawing character, U+00D7,
U+2264, U+2265 or U+2212 not given its one replacement, or U+00A7 not made `section` or `sections`
with its capital and its space; a character inside an allowed string fixed; the fixes uncounted;
an editor's proposal applied where its old text occurs twice or not at all, where two overlap, or
where the Chair did not keep it, or proposals read that are not numbered replacements; the guard
passing a code span, fenced block, link target, wikilink or number lost or added, refusing a
development reference removed from a production file or a flagged character replaced inside a
code span, or passing one whose letters changed; a sample under 200 words counted enough; a
folder that names nothing, or a path that names no tracked file, accepted. And when one of its own
functions is over the coding standard's production limits, or it holds a character off ASCII.
**Alone:** `pre-commit run humanize-selftest --all-files --verbose`

## `commit-attribution`

**Stage:** `commit-msg`
**Pairs with:** no self-test; the patterns are literal and the message is one file.
**Blocks:** a commit message carrying AI attribution: a `Co-Authored-By:` naming an agent, model
or vendor address, an agent session trailer, a generated-with line, or the robot emoji. Comment
lines and everything below the `--verbose` scissors line are ignored. It refuses; it never rewrites
the message. This stage exists only in a clone that installed both hook types; CI runs it over each
commit of the range `code-standard-range` judges, prints how many, and fails when git cannot list
them.
**Alone:** write a message to a file and run the stage against it, in both directions:

```bash
printf 'checkpoint: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n' > /tmp/msg
pre-commit run --hook-stage commit-msg --commit-msg-filename /tmp/msg --all-files   # must FAIL
printf 'checkpoint: x\n\nClean body.\n' > /tmp/msg
pre-commit run --hook-stage commit-msg --commit-msg-filename /tmp/msg --all-files   # must PASS
```

`pre-commit run --all-files` never exercises this stage; a green suite says nothing about it.

## `story-branch-selftest`

**Stage:** `pre-commit`
**Pairs with:** `branch-policy` and `branch-push`, which share its rules. It
reads nothing from the tree, so it passes in every derived project.
**Blocks:** a commit when a workflow rule fails a fixture: code on a protected branch passed, a path
that only begins like a record taken for one, a release commit changing more than the version
constant, a commit that changes `.template-version` without adding it taken for a birth; a story branch whose story is not In Progress or that changes the tracker,
sprint-status, a handoff or the issue log passed, a branch outside the team's names passed; a
direct push of code passing provenance, or a record asking GitHub; the story's status or the
statistics written wrong; `start` taken from a story branch, a dirty tree, a story already started,
waiting or branched; the pull request's title cut wrong; `start` leaving a Triaged issue of its
story behind or moving another story's; `finish` resolving an issue with a story still open,
leaving one In Progress once every story is Done, or beginning with no resolution for it or with
the integration branch ahead of its origin.
**Alone:** `pre-commit run story-branch-selftest --all-files --verbose`

## `branch-policy`

**Stage:** `commit-msg`
**Pairs with:** `story-branch-selftest`, `branch-push`.
**Blocks:** a commit on `main` or a `release/*` branch that changes anything but the shared records
(`sprint/`, the decision logs, the knowledge base, `docs/prd/`, `docs/architecture/`,
`.claude/agents/`), besides filling a version-log row's `pending` cell with a hash, read from the
diff line by line; unless it is a `release: vX.Y.Z` commit changing the version constant too, a
repository's first commit or a project's birth (the commit adding `.template-version`).
A commit on `story/<ID>` whose story is not In Progress, or
that changes the tracker, sprint-status, the handoffs or the issue log. A commit on a branch that is
neither protected, a story's nor `update/vX.Y.Z`. A merge in progress is left to the push and
provenance checks.
**Alone:** `pre-commit run --hook-stage commit-msg --commit-msg-filename <file> branch-policy --all-files`

## `branch-push`

**Stage:** `pre-push`
**Pairs with:** `branch-policy`. The `gates` workflow runs it too, on a push to `main` or a
`release/*` branch, over the push's range, with the run's token, read-only.
**Blocks:** in a clone, a push to `main` or a `release/*` branch carrying a commit that is not
records, a release, a birth or a repository's first commit, a local merge of a story branch among
them: story work reaches a protected branch only as a merged pull request, which GitHub makes, so
nothing pushed from a clone carries it. In CI, the same, except a commit GitHub names as a merged
pull request's: a direct push the clone's hooks did not stop turns the run red, which GitHub's
branch protection, unavailable on a private repository on the current plan, would have refused. A
push to any other branch passes. Installed by `pre-commit install`, the config naming `pre-push`
among its default hook types.
**Alone:** runs on `git push`; pre-commit hands it the refs being pushed.

## `gitleaks`

**Stage:** `pre-commit`
**Pairs with:** no self-test; an upstream hook, pinned by `rev:`.
**Blocks:** a hardcoded secret entering the tree. GitHub scans public repositories only, so on a
private one this is the only secret control. The explicit `stages:` is mandatory: the upstream
manifest declares none, and a hook without one runs at every installed stage.
**Alone:** `pre-commit run gitleaks --all-files` (the first run in a fresh clone builds the
gitleaks environment and needs the network once)

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.47 | 2026-10-26 | template | the template's version 1.47 | template |
