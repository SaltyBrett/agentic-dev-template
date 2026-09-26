---
name: What justifies a MAJOR, MINOR or PATCH bump to this template
description: 'The discriminating question is whether adopting the change forces a human to do something — run a new command, or edit a file to pass a new check. For a gates template that makes most new gates MAJOR, which is the correct and non-obvious answer. Includes every change in this repository mapped to a bump, the tiebreaker for judgement calls, and the release order that keeps the version stamp honest. Read before tagging.'
teaches: [2026-09-20-006]
verified: 2026-09-20
metadata:
  type: reference
---

# What justifies a MAJOR, MINOR or PATCH bump

> Durable learning. Wikilink: `[[reference_template_versioning]]`.
> The mechanics are enforced by `scripts/template_version.py`; **this judgement is not, and cannot be.**
> A gate can check that a tag is well-formed and that its commit agrees with it. It cannot decide
> what a change costs the person who adopts it.

## The discriminating question

> **If a project adopted this version, would a human have to do something?**
> Run a different command, or edit a file to pass a check that did not exist before.

Yes → **MAJOR**. No → MINOR or PATCH, by whether it adds surface or fixes something.

## The three buckets

**MAJOR (`v2.0.0`)** — adopting it requires action.

- A new or changed per-clone command. `pre-commit install --hook-type pre-commit --hook-type commit-msg`
  (decision `2026-09-20-001`) is the canonical example: a clone that does not re-run it is silently
  unprotected.
- A new gate that can fail content a project already has.
- A new prime directive in `AGENTS.md`, or a new rule in `CONSTITUTION.md`, that agents must follow.
- A schema change to knowledge frontmatter or the decision index.
- A renamed or removed script or file that projects reference.

**MINOR (`v1.1.0`)** — new capability, nothing required.

- A new script a project opts into, whose absence breaks nothing.
- A new gate that only ever passes on content the template produces — in practice, a self-test.
- A new standard, knowledge entry, or optional token.

**PATCH (`v1.0.1`)** — something that was wrong is now right, with no new obligations.

- A gate that did not fire now fires correctly: the `language: python` fix, the `--verbose` commit
  scissors truncation, the decision parser reading the whole file instead of the index section.
- Documentation or diagnostic corrections.

## The non-obvious conclusion

**For a compliance template, most new gates are MAJOR.** A gate exists to block commits, so adding one
can block a downstream project's existing content. That feels heavy — it means version numbers climb
quickly — and it is the honest answer: the cost lands on whoever adopts it, unannounced, as a failing
commit they did not cause.

This is why MINOR is narrower here than in a library. A new gate is MINOR only when it cannot fail
anything a project already has, which in practice means a self-test over in-memory fixtures.

## Tiebreaker

**When unsure, go up.** Under-versioning hides a change that costs someone an afternoon.
Over-versioning costs a digit.

## This repository's own history, mapped

Everything below predates the first tag and is folded into the `v1.0.0` baseline. It is recorded
because worked examples decide arguments that definitions do not.

| Change | Bump | Why |
|---|---|---|
| `language: python` interpreter fix | PATCH | Gates that could not launch now launch. Nothing to adopt |
| Attribution gate at `commit-msg` + both hook types | **MAJOR** | Every clone must run a new install command or the gate is inert |
| `CONTENT_RULES` channel (then named `PORTABILITY_RULES`) | **MAJOR** | A new rule that fails a spelling a project may already have in its docs |
| Frontmatter validation + parser cross-check | **MAJOR** | Newly fails entries whose YAML was malformed or spelled unreadably |
| Scoped decision parser, empty parse raises | PATCH | A parser that read the wrong region now reads the right one |
| Identity guard parses TOML, reads uid | **MAJOR** | Newly fails a config whose keys sit under the wrong table |
| `new_project.py` + its self-test | MINOR | Opt-in script; the hook is a self-test that cannot fail a project's content |
| `template_version.py` + its gate | MINOR | Skips entirely in a project with no tags, so nothing can fail |

## Release order, and why it is that order

    python3 scripts/template_version.py --release v1.1.0
    git add -A && git commit -m "release: v1.1.0"
    git tag -a v1.1.0 -m "MINOR: <what changed>"

The constant is set **before** the commit that gets tagged. Tagging first points the tag at a commit
carrying the previous version, every project created from it is stamped wrong, and the gate fails on
your next commit — after the tag is already published.

The annotation must name the bump. Not decoration: the reason a version was chosen is exactly what is
lost first, and the gate refuses a tag without it (except the earliest, which has no predecessor to
be a bump *from*).

## The limit, stated rather than papered over

**Between releases the stamp names the last release.** `gh repo create --template` takes `main`'s HEAD,
and at pre-commit time `git describe` reports the *previous* commit — so no hook can stamp the commit
being made. A project created from an untagged `main` carries newer content than its
`.template-version` claims.

The gate says so when it runs:

    note: main is ahead of the last release (v1.0.0-2-g1a2b3c4).
          Projects created now are stamped v1.0.0 but carry newer content. Tag first if that matters.

**Tag before creating a project from an untagged `main`,** or accept that the stamp names the last
release rather than the exact tree.
