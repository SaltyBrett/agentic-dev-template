---
name: Ground rules for deriving a release bump from commit messages
description: 'Design constraints for classifying each commit and computing the release bump from the window, established before the work was attempted and then closed won''t-do by decision 2026-09-23-004: the decision that introduces a change already names its bump, and the windows are small. Records two findings that are easy to get wrong if it is ever reopened: the commit-msg hook does fire on merge commits, so a naive type-prefix rule blocks every merge, and a window where every commit is exempt must fail rather than default to PATCH. Also measures why `checkpoint:` cannot simply be exempted.'
teaches: [2026-09-23-004]
verified: 2026-09-23
metadata:
  type: reference
---

# Ground rules for deriving a release bump from commit messages

> Durable learning. Wikilink: `[[reference_commit_classification]]`.
> Companion: [[reference_template_versioning]], which holds the bump *policy* this would automate.
> Written before the work was attempted, so the traps are known rather than discovered.
> Closed won't-do by decision 2026-09-23-004; the constraints stand for the day it is reopened.

## The idea, and why it was not built

The MAJOR/MINOR/PATCH choice is made at release time, which means reconstructing it by reading
back over every commit since the last tag. That looked like judgement deferred to recall — the
pattern this repository removed everywhere else.

The alternative: classify each commit **when the change is fresh**, enforced at `commit-msg`,
and have `--release` *compute* the bump as the highest classification in the window.

It was carried for four sessions and then measured rather than built. The windows between the
ten tags held between one and ten commits, and every change that moved the version was
introduced by a decision whose body names the bump. The judgement is already made while the
change is fresh; it lives in the decision log, which the freshness gate reads, not in the commit
message, which nothing reads back. A type on every commit in every repository carrying the hook
would cost more than the one reading it replaces. Decision 2026-09-23-004 says what would reopen
it: a window one reading no longer covers, or two maintainers who classify it differently.

## Four constraints, two of them measured

### 1. `commit-msg` fires on merge commits

Demonstrated in a scratch repository, not reasoned about:

    $ git merge side --no-ff -m "Merge branch 'side'"
      [commit-msg hook FIRED on: Merge branch 'side']

Git's own auto-generated message carries no type prefix, so **a naive "require a type prefix"
rule blocks every merge.** That is not hypothetical here: the multi-agent worktree workflow
merges `agent/claude`, `agent/codex` and similar branches into `main` by design.

Merge, revert, squash and amend each need a decided treatment, and each needs verifying rather
than assuming — the behaviour differs between them and between git versions.

### 2. A window with no typed commit must fail

If every commit in a range is exempt, the computed bump is undefined. It must **raise**, not
default to PATCH.

This is the same rule as decision `2026-09-20-004`, where an empty parse had to fail rather
than pass: an unreadable decision index is not zero decisions. A release that silently picks
the smallest bump because it found nothing to measure is the identical failure wearing a
different hat.

### 3. `checkpoint:` cannot simply be exempted

Measured on 2026-09-21: **11 of 17 commits (64%)** use this repository's own `checkpoint:`
convention; 3 are `release:`.

So exempting untyped commits leaves the derived bump computing over a near-empty set — a gate
that reports confidently and checks nothing. Either `checkpoint:` carries a type, or it maps
to one by rule, but it cannot simply fall outside the computation.

### 4. The policy is not up for revision

`[[reference_template_versioning]]` defines what MAJOR, MINOR and PATCH mean here, including
the non-obvious conclusion that most new gates are MAJOR. This work **automates** that policy.
Changing what the words mean is a separate decision with its own justification.

## The open choice

**Prefix vocabulary:** conventional-commits (`feat:` / `fix:` / `BREAKING CHANGE:`) or the
policy's own words (`MAJOR:` / `MINOR:` / `PATCH:`). The second maps directly and needs no
translation table; the first is more familiar to anyone arriving from another codebase. Neither
is obviously right, which is why it is a decision to record rather than a detail to settle in
passing.

## Rules

- Verify hook behaviour on merge, revert, squash and amend by running them. This entry's first
  constraint exists because the behaviour was surprising.
- An undefined bump fails the release. Never default to the smallest.
- Automate the policy; do not quietly redefine it while automating it.
