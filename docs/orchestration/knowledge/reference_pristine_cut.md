---
name: Why the pristine cut runs in the order it does, and what keeps two repositories apart
description: 'The reasons behind each step of the pristine cut under decision 2026-09-23-003, whose steps are the pristine-cut skill: the sanitize check read first and every item judged against what the reset clears; the GitHub rename before anything else; the sanitizer run while the local clone''s origin still names the template; only tracked files copied; the old clone''s origin switched to the archive name BEFORE the new repository is created, because the old URL redirects only until a repository with the old name exists again; the commit-msg gate proved with zero commits behind it; why v1.0.0 is the sanitized tree alone and the cut''s record follows it. Read before the next cut or before renaming a repository a clone still pushes to.'
teaches: [2026-09-23-003, 2026-09-25-004]
verified: 2026-10-23
metadata:
  type: reference
---

# Why the pristine cut runs in the order it does

> Durable learning. Wikilink: `[[reference_pristine_cut]]`.
> Decision 2026-09-23-003. The steps: `.claude/skills/pristine-cut/SKILL.md`. Tools:
> `scripts/sanitize_template.py` ([[reference_template_sanitizer]]), `scripts/template_version.py`
> ([[reference_template_versioning]]). The archive is `SaltyBrett/agentic-dev-template-archive`; its
> final tag names the new lineage's `v1.0.0`.

## What forces each step

1. **The check is read before anything is touched**, because only the items inside the files the
   reset clears (the two sprint documents, the pairs, the archives) go away by themselves; any other
   item is the sweep's, by hand, and has to be committed before the cut. At the cut every item was
   inside the reset's files, the probe mentions included, so there was nothing to sweep.
2. **The rename on GitHub comes first.** The new repository needs the old name, so the old one must
   give it up before the new one can be created. A rename is reversible.
3. **The sanitizer runs while the local clone's origin still names the template.** Its refusal
   judges the URL string, which a rename on GitHub does not change. The reset stays uncommitted in
   the clone, and `git checkout -- .` restores it once the copy is taken, because the sanitizer
   deletes and rewrites but never creates.
4. **Tracked files only.** The working tree carries ignored files a plain copy would put into the
   first commit: `.DS_Store`, `__pycache__/`, the `egg-info/` a local `pip install .` left, a tool's
   `settings.local.json`.
5. **The old clone's origin moves to the archive name before the new repository exists.** GitHub
   redirects the old name to the renamed repository only until a repository with the old name exists
   again. Once the new one is created, the old URL points at it, and a push from a clone whose origin
   was never switched lands in the wrong lineage.
6. **In the fresh directory the constant is set before the commit that gets tagged**, and the
   `commit-msg` gate is proved with zero commits in the repository, the case no older clone can
   test. The earliest tag is exempt from the bump rule; its annotation names MAJOR anyway and names
   the archive repository, so the two lineages point at each other.
7. **Both `gates` runs are read to the end**, not assumed.
8. **The archive closes out last**, because the story its closeout marks Done says the new
   lineage's `gates` runs were observed. Its last tag is a PATCH naming `v1.0.0` and the new
   repository; then it is archived on GitHub.

## What v1.0.0 is, and what is carried after it

At the cut, `v1.0.0` was the sanitized tree and nothing else: the fixed constant was its one change
from the sanitizer's output. The record of the cut itself, this entry and the decision's amendment,
exists only once the cut is done, so it was carried in as a commit after the tag, leaving `main`
one commit ahead of its release, the ordinary state between releases.

Then the go-live work followed (the template flag, the visibility decision and its control, the
license, the public README, the rulesets), and the operator asked that the *finished* template's
first release be `v1.0.0` (decision 2026-09-25-004). So the cut's tag and the three that followed
it were removed, the finished tree was sanitized again to S1 with the same script, and one
`v1.0.0` was cut on it. History was kept; only tags moved, before any outside consumer existed.
Do not read that as a precedent: a published tag is permanent once anyone else can have taken it.
The sanitizer's job is the same each time, which is the point of having it as a script.

## Where the session that performed the cut records itself

In the archive: its sprint-status entry, the tracker row, and the pair it scaffolds for the next
session. The next session runs in the new lineage at S1, under the entry the sanitizer wrote, with
no incoming pair, which `session-verify` accepts; its kickoff, read from the archive, says so and
names the new repository. The first maintenance session on the new lineage opens its first story
before it can scaffold S2, as any fresh project does ([[reference_derived_project_start]]).

## Rules

- A rename on GitHub does not change a clone's origin, and a redirect from the old name lasts only
  until the name is reused. Switch every clone that will push before reusing the name.
- Copy a tree by its tracked file list, never by directory.
- The cut's own record goes into both lineages; the tag carries neither.
