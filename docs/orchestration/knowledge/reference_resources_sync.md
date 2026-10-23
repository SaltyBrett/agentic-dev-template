---
name: The persona registry was a cache of dev-resources, and why the sync was retired
description: 'Until v2.0.0, personas and shared knowledge entries lived in dev-resources and reached each project by resources_sync.py: verdicts decided by version, a same-version difference a conflict never picked silently, growth only through --publish, the closeout refusing an unpublished persona. Decision 2026-10-23-003 retired it: the template ships the persona library itself and each project keeps its own roster. Why the sync was the wrong shape for that, what still holds for a project on v1.0.0, and what any future cache inherits. Read before reviving a cross-repository sync, or when a v1.0.0 project syncs.'
teaches: [2026-09-23-002, 2026-09-23-007, 2026-10-22-005, 2026-10-23-003]
verified: 2026-10-23
metadata:
  type: reference
---

# The registry was a cache of `dev-resources`, and why the sync was retired

> Durable learning. Wikilink: `[[reference_resources_sync]]`.
> The script was `scripts/resources_sync.py`, removed from the template by decision 2026-10-23-003;
> a project on `v1.0.0` keeps running its own copy until it adopts `v2.0.0`.
> Companions: [[reference_session_closeout]] (the roster rule that replaced it),
> [[reference_template_update]] (the ownership map), [[reference_claude_code_agents_md]].

## What it was

Decisions 2026-09-23-002 and 2026-09-23-007. Personas, and knowledge entries that belonged to no
one project, lived in `dev-resources`; each project held a copy refreshed at closeout by a script
in the updater's idiom: fetch a ref, judge every owned path, write, stamp `.resources-version`. A
persona carried `version:`, so a higher fetched version was an update and a higher local one was
ahead; the same version with different text was a conflict, never picked silently, and so was any
difference in an unversioned knowledge entry. The closeout refused a persona `dev-resources` lacked,
and the registry grew only through `--publish` into a clone of `dev-resources`, judged there by the
published `persona-lint`. A synced knowledge entry declared `source: dev-resources`, and the updater
kept any entry so marked. Decision 2026-10-22-005 moved the registry into `.claude/agents/` and left
`dev-resources` holding the old tree beside it for the projects still on `v1.0.0`.

## Why it was retired

Decision 2026-10-23-003, the operator's: the public template ships a persona library itself, inactive
in `personas/`, and each project activates what it needs into `.claude/agents/`, its roster. The sync
was the wrong shape for that, three ways:

- **Every file in `.claude/agents/` is a live agent.** A sync that writes the whole registry into
  every project activates every persona everywhere: a description in every session's context, and
  delegation Claude may choose unprompted ([[reference_claude_code_agents_md]]).
- **Growth ran the wrong way for a public template.** `--publish` carried a project's persona into a
  public repository, while a project is private by default (decision 2026-09-25-001). The library
  now grows only by template release, and a project's own persona stays in the project.
- **A second repository was a second channel.** Personas reached a project by sync and everything
  else by release: two stamps, two update paths, and a window in which `dev-resources` held two
  trees. One release now carries the library like any template file.

## What still holds

- A project on `v1.0.0` keeps its own copy of the script, its stamp and its closeout rule until it
  adopts `v2.0.0`; `dev-resources` keeps serving it and is archived once all have adopted (TMPL-2.4).
  The `v2.0.0` updater still keeps an entry marked `source: dev-resources`, and TMPL-1.10 settles
  what adoption does with those entries and with `docs/personas/`.
- The version verdicts live on in the closeout's roster rule: a roster copy above its library
  version is a fork, the same version with other text is drift, a lower one is noted
  ([[reference_session_closeout]]).
- What any future cache inherits: refresh it by a script that judges by version, never by hand; a
  conflict is a decision for one side, never a hand-merge that equals neither; tell a copy from an
  original by a declaration in the file, never by guessing from its path.
