---
name: The registry is a cache of dev-resources, synced at closeout and grown only by publishing
description: 'Why the persona registry and resource knowledge entries are refreshed from `dev-resources` by a script in the updater''s idiom rather than merged by the template: verdicts decided by version, a same-version or unversioned difference is a conflict never picked silently, a resource entry is told from the template''s own by a frontmatter declaration the updater honours, the closeout refuses a persona the synced ref lacks, and the first sync seeded an empty registry through --publish. Read before editing a persona or a resource entry in any project.'
teaches: [2026-09-23-002, 2026-09-23-007]
verified: 2026-09-23
metadata:
  type: reference
---

# The registry is a cache of `dev-resources`

> Durable learning. Wikilink: `[[reference_resources_sync]]`.
> Script: `scripts/resources_sync.py`. Procedure: `session_handoff_standard_v2.0.md` §7 step 4.
> Companions: [[reference_template_update]] (the idiom and the ownership split),
> [[reference_session_closeout]] (the append-only rule the publish path relies on),
> [[reference_published_hooks]] (the linter `dev-resources` judges contributions with).

## Why a cache and not a pointer

The session gate proves a kickoff's persona block equals the registry file, and CI reads local
files, so the registry must be in every project's tree. A submodule is not initialized by
`gh repo create --template` and needs a checkout flag in CI; a subtree is a second merge channel
over paths the updater already handles. So the project holds a copy, one script refreshes it, and
`.resources-version` says which ref it matches: the repository's own single-source-of-truth law,
one level up.

## How a verdict is decided

The sync has the fetched copy and the local copy, and nothing else. Personas carry `version:`, so
the higher one wins in the direction it points: fetched higher is `update`, local higher is
`ahead`. The same version with different text is a `CONFLICT`, since the append-only rule says
that cannot happen legitimately. Resource knowledge entries carry no version, so any difference
is a conflict too, resolved by `--take <path>` (the fetched copy) or `--publish` (yours). Nothing
is ever picked silently, for the same reason the updater conflicts on overlapping edits.

## How a resource entry is told from the template's own

Both kinds live in `docs/orchestration/knowledge/`. A resource entry declares
`source: dev-resources` in its frontmatter; `template_update.resource_owned` reads it and the
updater keeps the file whichever side changed it, and the sync imports that one function rather
than keeping a second rule. A fetched entry without the declaration is refused as `unmarked`,
because a synced copy the updater does not recognize would be three-way merged at the next
release. Resource entries carry `teaches: []`: they explain no project decision.

## What the closeout refuses, and why the sync runs there

A persona this project holds that `dev-resources` lacks at the synced ref, or holds at a lower
version, blocks the closeout with `unpublished`. The registry grows only through `--publish`,
which writes into a local clone of `dev-resources` for commit there under its own persona
linter. The sync runs at closeout, before the scaffold, so the pair the next session consumes was
scaffolded from the registry as just synced; a cold-start sync could change the registry under a
kickoff already written against it. A project that has never synced has no stamp and is not held
to the rule, which is what let the migration land.

## The stamp is the project's, and a moved entry costs one `--take`

`.resources-version` names the ref this repository last synced. The template's own stamp
travelled to the first derived project that took `v7.1.0`, as an `add`, because nothing had
told the updater otherwise; it now keeps the file and the initializer clears it at birth, like
`.project-profile`. And a project whose copy of a moved entry predates the mark holds an
unmarked file the updater keeps (any of the three copies marked means keep), so its first sync
sees a fetched marked copy against a local unmarked one: a conflict by the rule above, resolved
by `--take <path>` once. The probe recorded both.

## The first run

`dev-resources` held no registry. The first sync reported both personas `unpublished`,
`--apply --publish` wrote them into the clone, the clone's commit ran its `persona-lint` on real
content for the first time, and the sync back found both `up-to-date` and wrote the stamp. A
project created from the template starts with the template's cached copy and syncs from there.

## Rules

- Never edit a persona or a resource entry in place. Bump the persona's version and publish; for
  a resource entry, publish the edit and take it back by sync.
- Run the sync before every closeout; the gate refuses a stamp whose ref is not fetched.
- A conflict is a decision: `--take <path>` or `--publish`, never a hand-merge that leaves the
  file equal to neither side.
