---
name: The template is a pre-commit hook repository, and what that forced
description: 'Another repository consumes the persona linter, the frontmatter gate and the attribution gate from `.pre-commit-hooks.yaml`, pinned by `rev`, instead of copying a script. Publishing forced three mechanics: pre-commit pip-installs a python hook repository, so `pyproject.toml` exists and every entry is a console script; a remote hook runs from the consumer''s root, so the gates read their root from git rather than `__file__`, which would have judged the virtualenv; and the packaging leaves a project at birth because a Python project owns its own pyproject. Also why the content gates are `files:`-gated, why gitleaks stays upstream, and what a private hook repository costs a consumer: pre-commit clones into ~/.cache, outside every per-directory git config, so only an ssh host alias worked; the template is public since 2026-09-25 and the consumer pins plain https.'
teaches: [2026-09-23-002, 2026-09-23-005, 2026-09-25-001]
verified: 2026-09-25
metadata:
  type: reference
---

# The template is a pre-commit hook repository

> Durable learning. Wikilink: `[[reference_published_hooks]]`.
> Manifest: `.pre-commit-hooks.yaml`. Packaging: `pyproject.toml`. Consumer: `dev-resources`.
> Companions: [[reference_commit_attribution_gate]] (the gate that was being copied),
> [[reference_precommit_interpreter]] (why `language: python` and never a bare interpreter).

## Why a manifest and not a copy

`dev-resources` held a copy of `commit_attribution_scan.py`, its README calling the duplication
known. A copy drifts the day the original changes, and nothing compares them. A hook repository
is consumed by `rev`: the consumer names the release it runs, `pre-commit autoupdate` moves it,
and the script has one home.

## What pre-commit does with a python hook repository

It clones the repository at `rev` and runs `pip install .` into a virtualenv of its own. Three
things follow, each found by running it rather than reading about it:

- **The repository must be a package.** `pyproject.toml` lists the four modules the manifest
  needs, flat from `scripts/`, and takes its version from `new_project.TEMPLATE_VERSION` so the
  tag gate's one value is not maintained twice. `pip install .` reported `5.0.0` from `v5.0.0`;
  a leading `v` is a valid PEP 440 spelling.
- **`entry:` is a console script, never a path.** A remote hook runs from the *consuming*
  repository's root, where `scripts/…` does not exist. `repo: local` hooks are different: they
  are not installed at all, which is why the same scripts run by their path under `scripts/` here.
- **`__file__` is the wrong root.** Every gate derived its repository from the script's parent
  directory. Installed, that is `site-packages`, and the persona linter would have judged the
  virtualenv and found nothing. The published gates now ask git for the top level of the working
  directory and fall back to the working directory itself. pre-commit runs hooks from the root;
  the documented direct commands run from it too.

## Why the content gates are `files:`-gated

`persona-lint` and `kb-frontmatter-scan` judge one directory each. A consumer that does not hold
that directory yet, which `dev-resources` does not until the registry moves in, would otherwise
show the hooks as Passed over nothing. With `files:` set, pre-commit shows them as Skipped, which
is what happened. Once the content exists a consumer may add `always_run: true`, as this
template's own config does, so that a deletion still triggers the index cross-check. The
attribution gate has no content to gate on and is `always_run`.

## Why gitleaks is not re-published

A manifest can publish only the hooks that live in its repository. A consumer takes gitleaks from
upstream, pinned by its own `rev`, with `stages: [pre-commit]` declared because the upstream
manifest declares none ([[reference_commit_attribution_gate]]).

## Why the packaging leaves a project at birth

A project created from the template is not a hook repository, and a Python project has a
`pyproject.toml` of its own. Left in place, the updater's three-way merge would conflict on it at
every release. `new_project.TEMPLATE_ONLY` removes both files at birth and `template_update.KEEP`
never writes them; a fixture in the updater cross-checks the two lists, as it does for every
other ownership rule.

## What a private hook repository costs a consumer

The template was private until decision 2026-09-25-001, and the cost was measured. pre-commit
clones the hook repository with git into `~/.cache/pre-commit`, and that directory is outside
every per-directory git config. On a machine that separates identities with
`includeIf.gitdir:~/code/personal/` and an `insteadOf` rewrite to an ssh host alias, the rewrite
does not apply there. From that directory, by exit code without a pipe:

- https: refused, "could not read Username", since the keychain holds no github.com credential
- plain `git@github.com:`: accepted, by whichever agent key GitHub recognized first, which the
  operator's environment runbook names as the wrong-identity failure mode
- `git@github.com-personal:`: accepted, deterministically

So while private, the consumer's config named the alias URL, and a GitHub Actions run in the
consumer could not read the template with its default token, so `dev-resources` had no `gates`
workflow. Public, the consumer pins `https://github.com/SaltyBrett/agentic-dev-template` at a
tag, which needs no credential anywhere, and has the workflow; proved by `pre-commit clean` and a
full run from the empty cache. Anyone consuming a private hook repository has the list above:
the alias locally, and in CI a read-only deploy key scoped to the hook repository, never an
expiring token, with the alias recreated in the job.

The first version of this section said the keychain served the https URL. It did not; the
check that said so read the exit code of `head` at the end of a pipe, the exact trap
[[reference_macos_toolchain]] §7 records. Recorded here because the wrong claim was released in
`v5.1.0` before it was caught, and the decision is amended.

## Rules

- A consumer keeps the layout the gates judge: `docs/personas/` and
  `docs/orchestration/knowledge/` with its `INDEX.md`.
- Adding a hook to the manifest means a console script in `pyproject.toml` for it, and its
  module must find the repository through git, not `__file__`.
- Never run `pip install .` from inside the repository without cleaning up: setuptools writes
  `build/lib/` beside the sources, and `git add -A` at the next checkpoint commits it. That
  happened in `v5.1.0`; the first derived project to adopt the next release received four stray
  scripts as `add`. `build/` and `dist/` are ignored since `v6.0.1`. Install from a scratch
  directory, or use `pre-commit try-repo`, which builds in a temporary clone.
- Test a published hook by `pre-commit try-repo <path-to-template> <hook-id> --all-files` from
  inside the consumer, before the release that pins it. Stage the template's changes first:
  `try-repo` builds its temporary clone from staged and tracked changes only, and an untracked
  manifest fails it with "`.pre-commit-hooks.yaml` is not a file".
