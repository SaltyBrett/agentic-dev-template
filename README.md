# Agentic Development Project Template

A GitHub template for software projects built with AI coding agents. Every agent reads one
instruction file, `AGENTS.md`; a constitution, `CONSTITUTION.md`, sets the rules it obeys; the
project's state lives in plain files in the repository, so work carries from one session to the
next; and a suite of pre-commit gates refuses a commit that breaks a rule they check. The
template's own gates are scripts, each with a self-test. Claude Code runs the whole framework, its
session hooks and skills included; Codex reads `AGENTS.md` and is held by the same gates and CI.

[TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md), which every project carries, holds the rest of the
walkthrough, from the first commit to taking a newer template release, and the catalog of commands,
scripts, session hooks and gates.


## Requirements

Every clone needs these:

| Tool | Version | What it is for |
|------|---------|----------------|
| git | any recent | the repository and its hooks |
| Python | 3.11 or later | the initializer, the gates and the other scripts |
| pre-commit | any recent | installs the hooks and runs the gates. Install it with `brew install pre-commit` on macOS, or `pipx install pre-commit` elsewhere. It builds each hook's own environment, so the Python tools the gates use (PyYAML, ruff, mypy, pip-audit, tree-sitter) install themselves as `.pre-commit-config.yaml` declares them |
| GitHub CLI (`gh`) | any recent, logged in with `gh auth login` | creating and cloning the repository, and watching CI |
| Claude Code | v2.1.295 or later | reads `AGENTS.md` and runs the session hooks and the skills |

A project that adopts the coding standard, by adding a `code-profile.yaml` for its stack, also needs
its profile's tools:

| Profile | It also needs |
|---------|---------------|
| every profile | Node.js with `npx`, which runs jscpd 4.0.5 to find copied code |
| `python` | the project's coverage command (coverage.py) and `pip-licenses`, in the project's own environment |
| `rust` | `rustup`, with the toolchain the project's `rust-toolchain.toml` names and its `clippy`, `rustfmt` and `llvm-tools-preview` components; `cargo-llvm-cov` 0.9.1 and `cargo-deny` 0.20.2 (`cargo install --locked cargo-llvm-cov@0.9.1 cargo-deny@0.20.2`); all of them on `PATH`. Homebrew's `rustup` keeps its shims in `/opt/homebrew/opt/rustup/bin`, which is off the path until you add it |
| `typescript` | Node.js with `npm`; `prettier`, `eslint` and `typescript` in `package.json` at exact versions and installed, with an ESLint configuration; a lockfile; for pnpm or yarn, `packageManager` naming the exact version, which corepack, shipped with Node.js, runs; a coverage command that writes lcov, such as vitest with `@vitest/coverage-v8`. The gate fetches typescript 5.9.3 through `npx` once, to count each file's functions |

A tool the coding gate cannot find is reported as `unmeasured`, never passed in silence.

## Walkthrough

### 1. Create the repository

`<owner>` is your account; `<template-owner>` is the account that publishes this template, shown at
the top of its GitHub page. Either press **Use this template** on that page, choose **Private**, and
clone the new repository:

```bash
gh repo clone <owner>/<name>
cd <name>
```

or create and clone it in one command:

```bash
gh repo create <owner>/<name> --template <template-owner>/agentic-dev-template --private --clone
cd <name>
```

Make it private: the template is public, the projects made from it are not, and step 3 refuses a
public repository unless you pass `--public`. The repository holds one commit, "Initial commit", and
GitHub runs the `gates` workflow on it before you have run anything; that run is green.

### 2. Install the hooks

```bash
pre-commit install
```

It installs the three hook types the configuration names (pre-commit, commit-msg and pre-push) into
`.git/hooks/` and prints a line for each. From then on every commit and every push runs the gates.

### 3. Initialize it

```bash
python3 scripts/new_project.py --name "<Project>" --platform "<stack>" --scope "<one line>" \
    --prefix <ABC>
python3 scripts/new_project.py --name "<Project>" --platform "<stack>" --scope "<one line>" \
    --prefix <ABC> --apply
```

`--prefix` is the short code, a few capital letters, that starts every story and decision ID of
the project. `--platform` is one line on the stack as far as you know it; the project's architecture
settles it later.

The first command prints the plan and writes nothing. The second fills the project's values into
the files that carry `{{PLACEHOLDER}}` tokens, regenerates the documents that track the project's
work, writes `.template-version`, the file that marks a project and names the template
release it came from, replaces this page with the project's own front page (its name, platform and
scope, and a link to the guide), and runs the whole gate suite, ending
`PASSED: project initialized and every gate is green.` It refuses to run in the template itself,
without pre-commit installed, or in a public repository unless you pass `--public`. What it does,
refuses and leaves to you: [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md#the-initializer).

The walkthrough continues in the guide, at
[step 4, committing the birth](TEMPLATE_GUIDE.md#4-commit-the-birth).
