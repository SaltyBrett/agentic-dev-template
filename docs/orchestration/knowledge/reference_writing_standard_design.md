---
name: The writing standard's design and why
description: 'Why the writing standard is shaped as it is: voice and audience kept apart, assigned in writing-profile.yaml and never in frontmatter, a file no rule names judged as production, exact phrases and never bare words, a sweep and then whole files rather than changed lines, mechanical findings refused and judgement paused, the formats the gates read moved to ASCII with parsers reading both, and why the humanizer stops for the Chair only over text already in the tree. And the gate: an idle glob refused only in a production rule, Office files read by the text mode, a custom voice told by section 2, the allow list wrap-tolerant, and what its build found. Read before building or changing any part of TMPL-6.'
teaches: [2026-10-24-017, 2026-10-24-018, 2026-10-24-019, 2026-10-24-020, 2026-10-24-021, 2026-10-24-025, 2026-10-24-026]
verified: 2026-10-24
metadata:
  type: reference
---

# The writing standard's design and why

> Durable learning. Wikilink: `[[reference_writing_standard_design]]`. The law, once built:
> `docs/standards/writing_standard_v1.0.md`. The values and the measurements behind them are in
> decisions 2026-10-24-016 to 2026-10-24-023; this entry explains the choices.

## Voice and audience are separate

A voice is how a document sounds; its audience says whether it may cite development references.
Kept apart, one voice serves a runbook and a decision log alike, and only the runbook refuses a
story ID.

## Why a profile and not frontmatter

Most of the template's markdown already carries frontmatter that Claude Code or a gate owns:
skills, rules, agents, personas, knowledge entries, authorities. An unknown key in a skill fails
silently ([[reference_claude_code_skills]]), and the knowledge and persona gates refuse keys they do
not expect. GitHub shows a README's frontmatter to its production reader as a table. So every
assignment lives in `writing-profile.yaml`, and the gate prints a file's assignment on request.

## Why a file no rule names is production

The audience rule fires only on development references. A development default would let a
production document in a new folder pass while checking nothing, the green-over-nothing failure
([[reference_kb_frontmatter_validation]]). The starter profile declares the framework's development
paths, so a project is born clean, and the updater merges the profile three-way rather than keeping
it, so a development path a release adds reaches the project.

## Why the README is development in the template alone

The template's `writing-profile.yaml` is also the starter every project is born with, and the
updater carries it into a project at adoption, so a rule the template needs for itself reaches every
project. The template's `README.md` is written for an adopter of a development framework, whose
product vocabulary (S1, the Chair, `sprint/`) is the audience rule's list; a project's README is
written for its users. A development rule everywhere would leave a project's README unjudged, and
allow-list entries would exempt those strings everywhere and need emptying at birth. So the
`template:` list holds rules the gate applies only where `.project-profile` is absent, inert in a
project, and nothing rewrites the profile at birth or at an update.

## Why phrases skip code blocks and a list ends with its paragraph

A custom voice's sample sits in a fenced block and is the Chair's own words, which no rewrite may
change, so phrase matching skips code blocks as well as code spans; the character rule still judges
both. Markdown here is wrapped near 100 columns, so a phrase may cross a line break, and closing a
list cannot mean ending a line: `and more` at the end of a wrapped line would flag "and more
complex".

## Why exact phrases and no bare words

Measured on the template before the lists were set, every hit of a single AI or marketing word was
legitimate: a browser's audio unlock, Claude Code's harness, an elevated sandbox. Noise is what gets
a gate switched off. So the tables hold exact phrases, a phrase joins only once seen in an agent's
writing and leaves at its first false positive, and a project's collisions go in its allow list.
The tables live in the standard and the gate reads them there, as `story-artifacts` reads the team
standard ([[reference_story_artifacts]]), so there is no copy to drift.

## Why a sweep then whole files

The coding standard judges changed lines because legacy code is costly to clean
([[reference_code_review_log]]). Prose is cheap to clean with the humanizer, and the Chair named the
risk: the off-keyboard characters exist because drift bypassed rules already in place. In a clean
tree, whole files and changed lines agree on new work. They part on text that entered unjudged, by a
commit without the hooks, a template update or a first push judged at its tip, which changed lines
never see again and whole files catch at the next commit.

## Why mechanical refuses and judgement pauses

A mechanical finding has a cheap and certain fix, and its rare real exception is an exact string.
So it refuses, and the allow list is the only way past: each line is a visible commit and a gate
change the Chair approves. Tone is taste, so it takes the path a code review finding takes, the
story pausing until the Chair answers.

## Why the formats move and parsers read both

The headings the gates read (the sprint-status entry, the handoff and kickoff, a persona's
changelog, an epic) carry U+2014 and would fail the character rule on every new line. They move to
a hyphen, and the parsers read both forms, because `template_update.py` never writes a project's
`sprint/` ([[reference_template_update]]), which keeps the old form until the project's own sweep.

## When the humanizer stops for the Chair

A rewrite of text already in the tree changes words someone kept, so the Chair sees each file
before it is kept. An agent's own draft that the gate refuses is the agent's to fix, as a failing
test is; stopping there would halt every document story over a comma. A guard holds every code
span, link and number through a rewrite, so meaning cannot drift unseen.

## Why the gate refuses only an idle production glob

A glob decides nothing when it matches no tracked file, or only files an earlier rule claims. A
missed development path is judged as production, the stricter way, so its documents fail loudly.
A missed production path can fall to a later development rule and pass unjudged, the silent pass
again. So the gate refuses the second and never the first, and the starter's project paths
(`docs/prd/**` and the rest), which match nothing in the template or a newborn project, pass.

## Why the text mode reads Office files itself

A Word, PowerPoint or Excel file is zipped XML that the standard library reads, so the check step
is one command a person can run, with no extraction improvised per document. The first real run
paid for it: a file made by `scripts/md_to_docx.py` failed on a U+2014 its source never held,
written into every footer by the converter. A check on the source alone would never have seen it.

## Why section 2 names the built-in voices

A voice file the standard's table does not name must carry its sample, so a custom voice written
without the Chair's words is refused rather than passing in the built-in shape. A project that adds
its voice to the table opts out on purpose, in a visible commit.

## Why the allow list tolerates a wrap

Markdown here is wrapped near 100 columns, so an allowed `Amazon S3` can break across a line; a
space in an allowed string matches any whitespace. Each finding prints the flagged text widened to
its word, escaped to ASCII, as the line to add: the narrowest string a person can recognize.

## What the build found

- Writing the broken-copy harness, before running it, found three fixtures that passed with their
  rule removed: closing hashes, a dash counted as a word, a link's comma. A fixture is the check
  only once a broken copy fails it ([[reference_kb_frontmatter_validation]]).
- A scratch birth was refused by `session-closeout-check` over a fixture's literal wikilink to no
  entry. A fixture that writes a wikilink names a real slug.

## Rules

- Assign voice and audience in `writing-profile.yaml`, never in a document's frontmatter.
- Name a character by its code point in any rule, fixture or entry about it.
- Add a phrase only on evidence, and remove it at its first false positive.
- Never loosen a gate for the sweep; settle an append-only conflict with the Chair.
