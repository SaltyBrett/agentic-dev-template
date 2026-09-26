---
name: actions/checkout flattens the pushed annotated tag
description: 'On a tag push, actions/checkout re-fetches the ref as +<sha>:refs/tags/<tag> with --no-tags, replacing the annotated tag with a lightweight one. %(contents:subject) then returns the commit subject, and a gate that reads annotations fails with a misleading message. The workflow fetches the tag objects back; the version gate names a lightweight tag as such.'
teaches: [2026-09-22-002]
verified: 2026-09-24
metadata:
  type: reference
---

# actions/checkout flattens the pushed annotated tag

> Durable learning. Wikilink: `[[reference_ci_annotated_tags]]`.
> Workflow: `.github/workflows/gates.yml`. Gate: `scripts/template_version.py`. Companion:
> [[reference_ci_backstop]].

## What happened

The first release pushed after the CI backstop existed (`v4.1.0`, pushed with `--follow-tags`)
produced two `gates` runs. The branch run was green. The tag run failed the version gate:

    annotation does not name MAJOR, MINOR or PATCH: 'release: v4.1.0'

That string is the commit subject, not the annotation. The checkout step's log shows the cause:

    git fetch --prune ... origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
    git fetch --no-tags ... origin +<sha>...:refs/tags/v4.1.0
    git checkout --progress --force refs/tags/v4.1.0

The first fetch brings the annotated tag. The second, which `actions/checkout` runs for the ref
that triggered the workflow, points `refs/tags/v4.1.0` straight at the commit. The tag object is
gone from the checkout, and `git tag -l --format=%(contents:subject)` prints the commit subject for
a lightweight tag.

## The two fixes, and why both

- **The workflow fetches the tag objects back** with `git fetch --force --tags origin` right
  after checkout. The tag-push run is the one event whose purpose is to verify the tag as pushed,
  so it must see the tag as pushed.
- **The gate reads `%(objecttype)`** and reports `lightweight-tag` when it is `commit`, with a fix
  that names both causes: retag locally, or restore the tag objects in CI. It never also reports
  `no-bump-type` for the same tag, because that rule would print the commit subject as if it were
  an annotation that forgot the bump, and send the reader to re-annotate a tag that was annotated
  all along. The earliest tag is exempt, as it is from the bump rule: no predecessor, no bump to
  name, no annotation required.

The workflow fix alone would leave the misdiagnosis waiting for the next checkout change. The gate
fix alone would leave every release red.

## Rules

- A workflow that reads tag annotations fetches tags back after `actions/checkout`.
- A gate that reads an annotation checks the object type first. A lightweight tag has no
  annotation, and what looks like one is the commit message.
- A release pushed with `--follow-tags` costs two runs. That is a known, accepted duplicate.
