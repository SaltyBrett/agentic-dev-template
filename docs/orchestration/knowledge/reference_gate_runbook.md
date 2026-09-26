---
name: The gate-suite runbook is verified against the hook config, not maintained beside it
description: 'A page describing the pre-commit suite is what the next reader consults instead of the config, and the hand-written table it replaced was keyed by script, silent on stages and already one hook behind. `scripts/gate_runbook_scan.py` reads the hook ids from `.pre-commit-config.yaml` with a YAML parser and the H2s from `docs/governance/gate_suite_runbook.md`, and fails on a missing or extra section, wrong order, a stage line that disagrees, or a hook with no `stages:`. Why the page lives in governance and not in runbooks, why the bump is MAJOR, and what the check cannot see. Read before adding a hook.'
teaches: [2026-09-23-001, 2026-09-22-001]
verified: 2026-09-23
metadata:
  type: reference
---

# The gate-suite runbook is verified against the hook config

> Durable learning. Wikilink: `[[reference_gate_runbook]]`.
> Page: `docs/governance/gate_suite_runbook.md`. Check: `scripts/gate_runbook_scan.py`.
> Companions: [[reference_commit_attribution_gate]] (why every hook declares a stage),
> [[reference_template_update]] (why the page lives where it does).

## The shape of the failure

A table of the gates in `TEMPLATE_GUIDE.md` was written once and edited by memory. It named
scripts, not hook ids, so a script with two hooks had one row; it named no stage, so a reader
could not tell which command runs a hook alone; and it was already missing the updater's self-test
one session after that hook was added. Nothing compared it to `.pre-commit-config.yaml`. That is
the teaching-document fossil of `CONSTITUTION.md` §6.3, sitting in the page whose whole purpose
is to be the map of the suite.

## What the check proves, and what it cannot

The page's H2s are hook ids, every one, in the config's order; anything that is not about one
hook goes above the first H2. The check reads the ids with a YAML parser from every repo entry in
the config, reads the H2s outside fenced code, and compares both ways. A section's `**Stage:**`
line must equal the hook's declared `stages:`, because that is the value a reader passes to
`--hook-stage`, and a wrong one runs nothing. A hook with no `stages:` fails: decision
2026-09-20-001 required the declaration in prose, and this is where it became mechanical.

It cannot read what a section says a gate blocks or why. Those lines link the decision and the
knowledge entry, and the decision wins when they disagree. The check keeps the page's shape
honest; the author keeps its sentences honest.

Since 2026-09-23 the same check reads `.github/workflows/gates.yml` too: every non-manual stage
a hook declares must be run by a `pre-commit run` in some step, a plain one covering the
pre-commit stage and `--hook-stage <stage>` any other. The rule had lived in two knowledge
entries since the workflow was written ([[reference_ci_backstop]]); the scanner already had the
stages in hand, so the control cost one function. A missing or unparsable workflow is refused,
never read as covering nothing.

## Where the page lives, and why it is not `docs/runbooks/`

The updater's ownership map keeps `docs/runbooks/` for the project: operational procedures the
template never writes. A page that must track the template's own hook config has to travel with
the config, so it lives under a three-way path, `docs/governance/`, beside the document-control
standard. Three-way is the right mechanism for it: a project that adds a hook must add a section,
and the merge lets the project's sections and the template's coexist.

## Why the bump is MAJOR

The gate reads a project's config and page. A project that added its own hook, which is a
supported edit of a three-way merged file, fails until it writes the section; one whose hook
declares no `stages:` fails outright. For an unedited project the updater carries the page and
the config together and the gate passes. The bump is judged by the case it can fail, and under
[[reference_template_versioning]] the tiebreaker goes up.

## Rules

- Adding a hook to `.pre-commit-config.yaml` means adding its section to the runbook in the same
  commit, at its position in run order, with a `**Stage:**` line. The gate refuses the commit
  otherwise.
- Declare `stages:` on every hook, including hooks pulled from other repositories.
- Do not restate a decision or a knowledge entry in a section. Link it. The runbook is a map of
  the suite, not a second home for its reasoning.
