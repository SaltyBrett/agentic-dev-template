---
name: A regex is not a parser — validate frontmatter before trusting the freshness gate
description: 'Two gates that reported green while reading the wrong thing. kb_freshness_scan.py parsed frontmatter with regexes, so malformed YAML passed; it also scanned the whole decision log rather than the index section, so a table in a decision body became a phantom decision and a renamed heading would have emptied the gate silently. Covers the parser cross-check, the scoped index boundary, why an empty parse must raise, and why a fixture that passes against the broken code is worthless. Read before editing a knowledge entry''s frontmatter or any gate parser.'
teaches: [2026-09-20-003, 2026-09-20-004]
verified: 2026-09-24
metadata:
  type: reference
---

# A regex is not a parser: validating knowledge-entry frontmatter

> Durable learning. Wikilink: `[[reference_kb_frontmatter_validation]]`.
> Companion: [[reference_precommit_interpreter]].

## The failure this closes

`kb_freshness_scan.py` never parsed YAML. It matched two regexes against the frontmatter text:

    ^teaches:\s*\[([^\]]*)\]
    ^verified:\s*(\d{4}-\d{2}-\d{2})

Regexes match; they do not validate. An entry whose frontmatter is not loadable YAML still satisfies
both, so the gate passes a file that no YAML consumer can read. Measured on a probe:

    name: pre-commit language: python interpreter portability   # unquoted scalar, second colon

    yaml.safe_load                      -> ScannerError: mapping values are not allowed here
    kb_freshness_scan.parse_frontmatter -> {'teaches': ['2026-09-20-001'], 'verified': '2026-09-20'}

**A gate that reports green on a file it cannot actually parse is worse than no gate**, because the
green is precisely what stops anyone from looking. This is the same shape as the defect the freshness
gate itself exists to catch — an artifact that is trusted *instead of* the source — one level down.

## The harder half: valid YAML the gate still cannot see

Fixing this is not "run `yaml.safe_load` and accept what parses". The two parsers disagree about
several spellings that are perfectly valid YAML. All measured, none assumed:

| frontmatter line | freshness-gate regex | `yaml.safe_load` | |
|---|---|---|---|
| `verified: 2026-09-20` | `'2026-09-20'` | `date(2026, 9, 20)` | agree |
| `verified: "2026-09-20"` | `None` → **UNSTAMPED** | `'2026-09-20'` | differ |
| `verified: 2026-09-20T10:00:00` | `'2026-09-20'` (truncated) | `datetime(…10:00)` | differ |
| `verified: 2026-9-20` | `None` → **UNSTAMPED** | `'2026-9-20'` | differ |
| `teaches:` + `  - 2026-09-20-001` | `[]` → **entry skipped** | `['2026-09-20-001']` | differ |
| `teaches: ["2026-09-20-001"]` | `['"2026-09-20-001"']` → **UNKNOWN** | `['2026-09-20-001']` | differ |

Two of these are traps rather than mere inconsistencies:

- **The quoted date.** Quoting is the natural reaction to "make this valid YAML", it *is* valid YAML,
  and it makes the freshness gate read the entry as unstamped — failing the commit with a message
  about a missing date that is plainly present in the file.
- **The block list.** `teaches:` as a YAML block list is idiomatic and parses correctly, and it makes
  the entry vanish from the freshness gate while still looking stamped to a human reading the file.
  Silent loss of coverage, which is the exact failure mode being fixed.

So the gate does not enforce "valid YAML". **It enforces the intersection — the one spelling both
gates read identically:** unquoted zero-padded ISO dates, inline unquoted `teaches:` lists.

## How the cross-check works, and why it is built that way

Rather than enumerate the divergences above as six rules, `kb_frontmatter_scan.py` imports
`kb_freshness_scan.parse_frontmatter` and parses every entry **both ways**, failing when the results
differ. The table above is documentation, not logic. A future edit to either parser that reintroduces
a divergence is caught without anyone remembering to update a rule list.

This is worth copying whenever two consumers must read one file: assert agreement between them rather
than describing what agreement looks like.

`additional_dependencies: [pyyaml]` on the hook is what makes a real parser available at all, and it
is only possible because the hooks declare `language: python` rather than `language: system` — see
[[reference_precommit_interpreter]]. Under `language: system` there is no environment to install into.
Run directly without PyYAML and the script exits 2 with the `pre-commit run` command, never 0; a
missing parser must not present as a pass.

## Coverage is reported, never enforced

An entry carrying `teaches: []` is invisible to the freshness gate — there is no decision to check it
against, so it can never be reported stale. That is **not** an error. An entry explaining no ratified
decision is legitimate, and forcing an ID into it would manufacture a false link, which is a worse
defect than no link.

But a green scan must not read as full coverage when it is a fraction of it.
`kb_freshness_scan.py --list` now names the uncovered entries:

    gate reach: 3/4 entries checkable (1 carries `teaches: []` and cannot go stale by this gate)
      UNCOVERED: reference_macos_toolchain.md
      (informational, not a failure — verify these by reading, not by scanning)

**Read those entries. Do not scan them** — nothing is watching them for you.

## The sequel: a prose rule is not a control

Scoping this gate produced a second defect and a better lesson. `load_decisions()` parsed **every**
`|`-prefixed line in `sprint/decision-log.md`, so the comparison table above — when it briefly lived
in a decision body — was absorbed as a phantom decision ID, `` `verified: 2026-09-20` ``.

The first fix was a written rule: *do not put tables in decision bodies*. That rule was wrong in
kind. **A prose constraint guarding an append-only file is not a control** — it has no enforcement,
and it sits in the one file that grows without review, so every future decision is a fresh chance to
violate it silently. It is the same fossil shape `CONSTITUTION.md` §6.3 exists to catch.

The latent failure was worse than the phantom row. Because the parser scanned the whole file, renaming
the `## Decision Index` heading would have yielded **zero decisions with no error** — every `teaches:`
reporting UNKNOWN, or, with nothing stamped, a gate reporting green while checking nothing.

So the parser is now scoped to the index section, an unlocatable index raises rather than returning
empty, and `--self-test` proves the boundary on every commit from in-memory fixtures.

**Two things to copy from this:**

1. **An empty parse must never be indistinguishable from a clean one.** Any parser that can return
   "nothing found" should be asked whether nothing-found is a legitimate state or a structural break,
   and the break must raise.
2. **A fixture that passes against the broken code is false confidence.** One fixture here — a
   `|`-prefixed body line — passed under the unscoped parser too, because its second cell had no date
   and the old code rejected it for an unrelated reason. It was reshaped to carry a date so it
   actually discriminates. Always run new fixtures against the bug they are meant to catch; if they
   pass, they are testing nothing.

## Rules

- Frontmatter keys are spelled the way both gates read alike: `verified: 2026-09-20` unquoted and
  zero-padded, `teaches: [id, id]` inline and unquoted. Never quote either.
- `teaches: []` is a legitimate declaration, not a placeholder to fill in. Leave it when it is true.
- Never relax a check by loosening the freshness regex to accept a new spelling. Fix the entry — the
  regex's strictness is load-bearing: `kb_freshness_scan` compares dates as **strings**, which is only
  correct for zero-padded ISO.
- Adding a consumer of this frontmatter means adding it to the cross-check, not trusting it to agree.
- Tables in decision bodies are fine. `load_decisions()` reads the Decision Index section only, so a
  body table is not read at all — see the section below, and decision `2026-09-20-004`. Since
  decision 2026-09-23-003 it reads two logs that way, the project's and the framework's, as one
  set; an index missing from either still raises, naming the log ([[reference_framework_decisions]]).
