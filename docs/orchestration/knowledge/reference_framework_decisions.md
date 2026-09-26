---
name: The framework's decisions live beside the project's, in two logs read as one
description: 'Why the template''s decisions moved from sprint/decision-log.md to docs/governance/framework_decisions.md with their IDs unchanged: the project''s log had become a merge target and the pristine reset could not clear it. How the freshness gate and the session gate read both indexes as one set, which row wins a duplicate ID and why, where a template session and a project session each log, what the updater merges and keeps, and why a project prefixes its IDs. Read before logging a decision in either file or touching a gate that reads them.'
teaches: [2026-09-23-003]
verified: 2026-09-24
metadata:
  type: reference
---

# The framework's decisions live beside the project's, in two logs read as one

> Durable learning. Wikilink: `[[reference_framework_decisions]]`.
> Files: `docs/governance/framework_decisions.md` (the template's), `sprint/decision-log.md` (the
> project's). Readers: `scripts/kb_freshness_scan.py`, `scripts/session_closeout.py`. Carrier:
> `scripts/template_update.py`. Decision 2026-09-23-003.

## The failure this closes

Every knowledge entry declares `teaches: [<decision-id>]`, and the freshness gate refuses an ID in
no index. So the template's decisions had to reach every project, and they did so by living in
`sprint/decision-log.md` and travelling with it: the initializer never cleared the log, and the
updater inserted each new framework decision into the project's append-only log by ID. Two costs
followed. The project's own log was a merge target, the one file under `sprint/` the template
still wrote, and a project decision could collide with a framework ID. And the template could not
be reset to a pristine state, because clearing its log broke the first commit.

## The mechanism

- **Two files, one shape.** `docs/governance/framework_decisions.md` carries the template's
  decisions, index and bodies, IDs unchanged from the day they were logged. `sprint/decision-log.md`
  ships with the `[EXAMPLE]` entry alone and is the project's from birth.
- **Read as one set.** `kb_freshness_scan.parse_logs` takes the logs in order, the project's then
  the framework's, and unions their index rows before resolving decision-to-decision changes, so a
  row in one log may name an ID in the other. An entry may `teaches:` either; a handoff may cite
  either. `session_closeout.decision_ids` calls the same function.
- **A missing index still raises, naming the log.** A log that exists without a locatable
  `## Decision Index` is never read as "the other log's decisions only"; the exception carries the
  label so the report says which file. A log whose only row is the example parses to zero
  decisions without error, which is the state every project starts in.
- **The framework file wins a duplicate ID.** It is the maintained copy. A project that took a
  release before `v11.0.0` still holds framework rows in its own log from the old insertion, and
  those may be older than the framework's, so the later log's row replaces the earlier's.
- **The updater merges the framework file by ID and keeps the log.** `sprint/decision-log.md` is
  under `sprint/` and is never written again; the framework file is merged exactly as the log used
  to be, rows at the top, bodies at the end, an edited row or body reported and left. The old
  copies in a pre-`v11.0.0` project's log are not removed: the updater removes nothing from a
  project's file, and the duplicate rule makes them harmless.
- **The initializer fills the log's header and nothing else.** The example entry stays until the
  planning session writes the first real epic, when the live-placeholder rule refuses it
  ([[reference_session_closeout]]).

## Observed on adoption

A scratch project initialized from `v10.0.0` took `v11.0.0` through the updater: the framework
file and this entry arrived as `add`, the three sprint documents were named `not applied`, the
suite went green, and the project's log still held its 25 old framework copies. The freshness
gate indexed 25 decisions, none UNKNOWN, and read the amendment date of 2026-09-23-003 from the
framework file rather than from the older copy in the log, which is the duplicate rule doing
its one job.

## Where a decision goes

In the template itself, a session that decides something about the framework logs it in
`docs/governance/framework_decisions.md`: a new index row at the top, its body at the end. In a
project, every decision goes in `sprint/decision-log.md`. The gates do not care which; the files
do, because only the framework file travels.

## Prefix a project's IDs

The framework's IDs are bare dates. A project decision written as `2026-09-24-001` can be the ID
the framework's next decision takes, and on a duplicate the framework's row wins, so the project's
would be silently shadowed at the next release. A project writes its own as
`<PREFIX>-2026-09-24-001`; the gates read IDs literally, so any prefix works
([[reference_derived_project_start]]).

## Rules

- Never edit `docs/governance/framework_decisions.md` in a project. The updater replaces an
  unedited row or body when a release changes it and reports an edited one; a project that needs
  to depart from a framework decision supersedes it in its own log, naming the framework ID.
- An amendment to a framework decision is made in the framework file, and the freshness gate
  reads it there, so the sweep it forces ([[reference_kb_frontmatter_validation]]) is unchanged.
