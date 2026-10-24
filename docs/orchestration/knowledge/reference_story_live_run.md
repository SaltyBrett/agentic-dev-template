---
name: The /story skill run live, brief to release, and what it found
description: 'The record of TMPL-3.3''s proof: one story run by /story on a scratch copy of Comfy, each role a general-purpose subagent carrying its persona, from brief to a release pushed to a private scratch repository. Why roles never commit or ask, why a finding reaches the code review log once with the Chair''s words, why the build commits twice, and the three gaps the run found (stale artifacts passing, a first push judged at its tip only, a format check counting diff context). Read before changing /story, the story-artifacts gate or the review stages.'
teaches: [2026-10-24-004, 2026-10-24-011, 2026-10-24-015]
verified: 2026-10-24
metadata:
  type: reference
---

# The /story skill run live, brief to release, and what it found

> Durable learning. Wikilink: `[[reference_story_live_run]]`. Story: TMPL-3.3. Procedure:
> `.claude/skills/story/SKILL.md`. Law: `docs/standards/team_standard_v1.0.md`. Companions:
> [[reference_story_artifacts]], [[reference_code_review_log]].

## The run

A clone of Comfy, its remote removed, was taken to a scratch `v2.1.0` tag by `template_update.py`
(no conflict; the suite green at `--apply`), eight roles activated, a Python `code-profile.yaml`
with the project's own `.venv` for coverage, and one story added to its tracker: the per-stage times
in `watch_run.py`'s finished-run summary. `/story` ran it from the template's conversation, so every
role was a general-purpose subagent whose prompt opened with the persona's, as decision
2026-10-24-012 foresaw: the procedure and the gates are proved, the roster's wiring in a session
opened in the project is not. The Chair answered three stops in chat: two review findings and the
release.

## Why the roles never commit or ask

A subagent cannot ask the Chair, and several committers would interleave. So a role writes its
artifact and stops; the main session runs the gates itself, rather than trusting the role's report
of them, commits, and asks. Every role's reply also claimed its own gate run; the main session's
re-run agreed each time, which is the point of running it, not a reason to stop.

## Why a finding reaches the log once

The code review log is append-only, and a row's Chair's response cannot be filled in later without
editing it, which the gate refuses. The persona the library shipped told the code reviewer to append
its own rows, which in a story would write them before the Chair answered; it is now version 3. The
answer recorded is the option the Chair chose in chat, word for word.

## Why the build commits twice

`build.md` lists the commits it made, and no file can name the commit that holds it. The code is
committed first, then the artifact naming it; a fix after review is a third commit, added to the
list.

## What the run found

- **A brief written without the code profile** planned its checks in a script under the production
  path, where the gate's coverage could never count them; every role's brief now carries the profile.
- **Stale artifacts pass:** after the rebuild, the earlier verify and review, judging the old build,
  still passed `story-artifacts`, which checks an input's status, not whether it changed after the
  next stage was written. The skill reruns them; the gate cannot yet tell (TMPL-3.4).
- **A first push is judged at its tip only:** the release's push created the repository, so CI's
  range fell back to `HEAD~1..HEAD`; the commit-msg and coding-standard steps read one commit of
  seventy, and the story's code went unjudged in CI though the run was green (TMPL-2.10).
- **The format check counts diff context:** `ruff format --diff` hunks carry three context lines a
  side, and the gate flags every line of the hunk, so a correct changed line beside legacy
  unformatted code is a `format` finding. The architect placed the new code away from the old
  constants to avoid it (TMPL-4.7).
- **Not exercised:** a CI range holding code, whose coverage command names a `.venv` the runner
  lacks, would be `unmeasured`; this run's range held none.

## Rules

- Re-run the gates in the main session; a role's report of them is a claim.
- Append a finding to the log only with the Chair's response in it.
- Give every role the project's code profile before it plans a check.
- Read a green CI run for what its range held before calling the change judged.
