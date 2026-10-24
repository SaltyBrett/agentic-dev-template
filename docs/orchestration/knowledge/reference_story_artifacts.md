---
name: A team's handoffs are files a gate judges, and the gate reads its law from the standard
description: 'Why the agentic team hands off through committed artifacts in docs/stories/<ID>/ that story_artifacts.py judges on every commit: what each stage file carries, why the gate reads the role map and the triggers from the team standard at every run rather than copying them, why the release is always a trigger, why a trigger and a finding are judged once the story moves past them, and what a broken-variant run taught about fixtures that trip a neighbouring rule. Read before changing the team standard, the gate or the /story skill.'
teaches: [2026-10-24-004, 2026-10-24-005, 2026-10-24-006, 2026-10-24-013]
verified: 2026-10-24
metadata:
  type: reference
---

# A team's handoffs are files a gate judges, and the gate reads its law from the standard

> Durable learning. Wikilink: `[[reference_story_artifacts]]`. Law:
> `docs/standards/team_standard_v1.0.md`. Gate: `scripts/story_artifacts.py`, hooks
> `story-artifacts-selftest` and `story-artifacts`. Companion: [[reference_code_review_log]].

## Why files

Role agents that hand off in conversation leave nothing to check: a role can start on work the last
one never finished, a builder can verify its own code, a release can ship past a trigger nobody
approved. Decision 2026-10-22-003 made every handoff an artifact; decision 2026-10-24-004 put them in
`docs/stories/<ID>/`, committed, one per stage. A file is what a gate can read, a reviewer can open
later, and the next session can start from.

## Why the gate reads the standard

The role map and the trigger list are the law, and a project may extend both by a decision (a
trigger of its own, a persona at a stage). Copied into the gate they would be two records that drift,
and a project's addition would be refused by the template's copy. So the gate reads §3's table and
§4's list from the project's own standard on every run. A section it cannot read stops it with exit
2: a gate that read an empty role map would refuse nothing, the green-over-nothing failure
[[reference_kb_frontmatter_validation]] names.

## Why the release is always a trigger, and when triggers are judged

Shipping is a decision the Chair owns (decision 2026-10-24-005's "a deploy or release"), so every
story that ships waits for the Chair's approval in `approvals.md`. A trigger hit earlier is judged
only once the story releases or is marked Done: until then the story is paused for the Chair, which
is the skill's job, and a commit of the paused story's artifacts must still be possible. A review or
security finding is judged the same way, once a later stage exists, since the story may not move
past an unanswered finding (decision 2026-10-24-011).

## What the variants taught

Run with a Python that had no PyYAML, every broken variant was "caught" by the same crash and proved
nothing; rerun properly, five variants passed, because each failing fixture also tripped a
neighbouring rule (a missing design also mismatched the build's input; an unknown trigger also went
unapproved at release). A fixture caught by another rule's check tests nothing about its own: each
was rewritten so that only its rule could fail it.

## Rules

- Hand off through a committed artifact in `docs/stories/<ID>/`, never through conversation.
- Extend the role map or the triggers in the team standard, by a decision; never in the gate.
- Run broken variants with the interpreter the hooks use, and make each failing fixture trip its own
  rule alone.
