---
name: A rule that bans a name must not write that name down
description: 'The personal lineage must contain no employer identifier, so the rule enforcing that cannot list the identifier in plaintext — it would put the string in the repository it protects and force the scanner to exempt itself. Identifiers are stored as SHA-256 of a normalized form, matched over n-grams so any spelling is caught. Also records why the scanner now takes its file list from git rather than the filesystem. Read before adding a content rule or an identifier.'
teaches: [2026-09-20-007]
verified: 2026-09-20
metadata:
  type: reference
---

# A rule that bans a name must not write that name down

> Durable learning. Wikilink: `[[reference_content_provenance]]`.
> Companions: [[reference_precommit_interpreter]], [[reference_template_versioning]].

## The shape of the problem

Decision `2026-09-19-001` split this template from employer brand and program content, and left an
open question: should a gate fail the commit when an employer identifier appears? The obvious
implementation is a list of names in the scanner.

**That implementation defeats itself.** An identifier this repository must never contain would be
written into `scripts/banned_feature_scan.py` in order to be banned — and the scanner would then have
to exempt itself from its own rule, the way the bare-`python` rule does. The control would publish
exactly what it exists to suppress.

## The fix

Store SHA-256 of the **normalized** identifier: lowercased, stripped to alphanumerics, re-joined
without separators. One hash then covers every spelling:

    "Widget Corp"   "widget-corp"   "WIDGETCORP"   "Widget  Corp"   ->   one hash

Matching sweeps 1- to 3-word n-grams per line and concatenates each, so a multi-word name is caught
whatever punctuation separates its parts. The rule carries an **empty `allow` set** — unlike every
other rule in the channel — because there is no file here where such a name belongs.

Add one without ever writing it down:

    python3 scripts/banned_feature_scan.py --add-identifier "Name"

## The honest limit

**A hash is non-disclosure, not secrecy.** It is unsalted, because a salt stored beside it protects
nothing. Anyone who already guesses a name can confirm it against the hash. The goal is that the
control does not *publish* the name — not that the name is unknowable.

A hashed denylist is also unreadable by design: you cannot audit what is banned by reading it. The
violation message shows the offending line, which contains the name, visible to the author who
already has it and published nowhere.

## Why the channel is called CONTENT_RULES now

It was `PORTABILITY_RULES`. "No employer identifier" is not a portability concern, and filing it under
a name that says otherwise misleads whoever reads it next. **The channel is defined by its scope —
every file, `EXCLUDE_FILES` included — not by a topic.** A rule carries either `patterns` (regex) or
`hashes`, plus its own `allow` set and a `fix` string.

Renaming amended decision `2026-09-20-002` rather than superseding it: the substance — a second
channel that bypasses `EXCLUDE_FILES`, with per-rule exemptions — is unchanged.

## Two defects this turned up, both worth copying

**1. The gate caught its own author.** The comment block explaining *why identifiers must never be
written here* used a real identifier as its worked example. The rule flagged it on the first run after
being written. The examples are fictional now, and the comment says why they must stay that way.

The general lesson: **an example in documentation is content.** A rule about what a repository may
contain applies to the prose explaining the rule, and that is the easiest place to forget.

**2. The scanner blocked a commit over a file git will never take.** `.claude/settings.local.json` is
covered by the global gitignore, so it cannot enter the repository — yet it failed the provenance
rule, naming a file the author could not fix by committing.

`candidate_files()` now takes the list from:

    git ls-files --cached --others --exclude-standard

That is *what git would actually commit* — tracked plus untracked-but-not-ignored — falling back to a
filesystem walk outside a repository. A content gate should judge what can enter the repository, not
what happens to sit in the working directory.

## Rules

- Never add an identifier in plaintext. Use `--add-identifier` and paste the hash.
- Keep every example in this repository's prose and comments **fictional**. The rules apply to the
  documentation that explains them.
- A new rule goes in `CONTENT_RULES` when it must cover the governance docs in `EXCLUDE_FILES`, and in
  `BANNED_PATTERNS` when it is about a forbidden platform feature.
- Exempt by adding to a rule's own `allow` set, never by adding the file to `EXCLUDE_FILES` — that
  drops it from every banned-feature check as well.
