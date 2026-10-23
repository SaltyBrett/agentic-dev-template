---
paths:
  - "scripts/**"
  - ".pre-commit-config.yaml"
  - ".pre-commit-hooks.yaml"
  - "pyproject.toml"
  - ".github/workflows/**"
  - "docs/governance/gate_suite_runbook.md"
---

# Changing a gate, its fixtures or the suite

- Each rule a gate enforces has a passing and a failing fixture in its `--self-test`, pure and in memory. A fixture is trusted only after it fails against a deliberately broken copy of the code ([[reference_kb_frontmatter_validation]]).
- Structured input is read with a parser, never a regex, and an unreadable or empty parse raises: a gate that reads nothing reports green.
- A new check runs on the real tree as well as on its fixtures, which ask only the questions their author thought of ([[reference_session_closeout]]).
- Exit 0 is clean, 1 a violation, 2 cannot run; each violation prints its fix.
- A hook declares `stages:` ([[reference_commit_attribution_gate]]); a local one declares `language: python`, so pre-commit provisions the interpreter its `entry:` runs ([[reference_precommit_interpreter]]), and its self-test is a hook of its own placed just before it.
- Adding, renaming, moving or restaging a hook changes `docs/governance/gate_suite_runbook.md` in the same commit; `gate-runbook` refuses the commit otherwise ([[reference_gate_runbook]]).
- A module that `.pre-commit-hooks.yaml` publishes is a console script in `pyproject.toml` and finds its repository through `git rev-parse --show-toplevel`, never `__file__` ([[reference_published_hooks]]).
- A manual-stage gate runs with `--all-files`, or pre-commit stashes unstaged edits and judges the last commit ([[reference_precommit_stash]]).
- An exit code is read without a pipe after the command; in zsh, `${pipestatus[1]}` ([[reference_macos_toolchain]]).
