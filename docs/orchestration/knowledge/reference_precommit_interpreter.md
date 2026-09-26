---
name: pre-commit local hooks declare language python, never a bare `python` entry
description: 'A local hook written as `entry: python scripts/x.py` under `language: system` cannot launch on macOS, which ships no bare `python` on PATH — the compliance gate then blocks every commit with an error that reads like a broken script. `language: python` makes pre-commit provision its own interpreter and is the portable fix; documented manual invocations go through `pre-commit run <hook-id>` for the same reason. Read before adding or editing any hook in `.pre-commit-config.yaml`, or before documenting how to run a gate by hand.'
teaches: [2026-09-20-002]
verified: 2026-09-25
metadata:
  type: reference
---

# Pre-commit local hooks: `language: python`, never a bare `python` entry

> Durable learning, captured when the framework was first cloned on macOS (Apple Silicon).
> Wikilink: `[[reference_precommit_interpreter]]`. Companion: [[reference_macos_toolchain]].

## The defect

Every gate in `.pre-commit-config.yaml` is a `repo: local` hook that invokes a Python script:

    entry: python scripts/banned_feature_scan.py

Under `language: system`, pre-commit provisions nothing — it resolves that `entry` against the
ambient `PATH` of the committing shell. On macOS there is no bare `python`:

    $ which python
    python not found
    $ which python3
    /Library/Frameworks/Python.framework/Versions/3.13/bin/python3

Apple removed the bundled Python 2 in macOS 12.3, and neither a python.org installer nor Homebrew's
`python@3.x` puts an unversioned `python` on the default PATH (pyenv shims are the exception, which
is why this can look machine-specific). The hook cannot launch: `Executable python not found`.

The consequence is worse than a broken script. The compliance gate now fails on every commit, and it
fails in a way that reads like the scanner itself is broken — which makes `--no-verify` look like the
reasonable next move. Bypassing the gate is exactly what the prime directives forbid, so a missing
interpreter must never be allowed to present as a failing gate.

## The fix in this repo

Every local hook declares:

    language: python

pre-commit then builds a per-hook virtualenv and runs `entry` inside it. A virtualenv always contains
`python` by definition, so the literal `python` in `entry` resolves identically on macOS, Linux and
Windows. The dependency on the ambient PATH is removed rather than worked around, which is the actual
defect.

All three hook scripts are standard-library only, so no `additional_dependencies:` is needed. A hook
that later grows a third-party import declares it there — never by reaching for the host interpreter's
site-packages.

## Why not simply write `python3`

It relocates the bug instead of removing it. Windows Python installs ship `python.exe` and the `py`
launcher and frequently have no `python3` on PATH at all, so `entry: python3` under `language: system`
is the same failure with the operating systems swapped. A framework meant to travel between machines
cannot pick a winner among ambient interpreter names.

## The same defect in prose: documented manual invocations

Fixing the hooks left the *documentation* broken in exactly the same way. `README.md`, the cold-start
checklist, `AGENTS.md` step 1 and four script docstrings all told the reader to run
`python scripts/<gate>.py` — a command that cannot execute on the machine the framework now lives on.
The hooks were portable and every documented way to run them by hand was not.

This is the sharper half of the lesson. A broken hook announces itself on the next commit. A broken
instruction in a mandatory-read document is discovered by whoever follows it, and what they see is a
compliance gate that appears not to exist — which is precisely the state that makes `--no-verify`
look reasonable.

**The fix is the same principle, not a different one: remove the dependency on the ambient PATH.**
Documented manual invocations go through `pre-commit`, which provisions its own interpreter:

    pre-commit run agent-execution-identity --all-files --verbose
    pre-commit run banned-feature-scan --all-files
    pre-commit run kb-freshness-scan --all-files

`--verbose` is needed when you want the script's own output: pre-commit suppresses a passing hook's
stdout, so without it a passing identity gate prints `Passed` and not
`AGENT EXECUTION IDENTITY GATE: PASS`.

Direct invocation survives only where `pre-commit run` genuinely cannot serve:

- ad-hoc flags a hook does not pass (`banned_feature_scan.py --path`, `kb_freshness_scan.py --list`)
- `md_to_docx.py`, which is not a hook and needs third-party `python-docx`

There, docs write `python3` and **state the Windows form beside it** rather than implying one name is
universal — the whole point of §"Why not simply write `python3`" above. The same gap holds for
`pip`: macOS ships `pip3` and no bare `pip`, so the install line a first-time reader runs is
`python3 -m pip install pre-commit`, never `pip install pre-commit`. Found when the public README's
commands were run as written on a fresh clone and that line alone exited 127. Where a script prints its own
usage line, derive the name instead of hardcoding it:

    print(f"Usage: {Path(sys.executable).name} scripts/md_to_docx.py …")

## Rules

Any hook in `.pre-commit-config.yaml` that runs a Python script declares `language: python`. Do not
use `language: system` with an interpreter name in `entry`. Keep the short comment beside each
`language:` line so the reason survives the next edit.

A bare `python …` appears in this repo in exactly two places, both deliberate: `entry:` lines in
`.pre-commit-config.yaml`, where it resolves inside pre-commit's virtualenv, and quotations of the
broken pattern in this entry. Anywhere else it is a defect.

**This is now mechanically enforced,** not remembered: `CONTENT_RULES` in
`scripts/banned_feature_scan.py` blocks the commit (decision `2026-09-20-002`). The rule is
case-sensitive and `\s+` cannot cross the `3`, so `python3 scripts/…` and prose like "Python scripts"
pass untouched.

Two things about that rule are worth knowing before you add another:

1. **It lives in `CONTENT_RULES`, not `BANNED_PATTERNS`, and that is load-bearing.**
   `BANNED_PATTERNS` is filtered by `EXCLUDE_FILES`, which holds `AGENTS.md`,
   `AGENT_COLDSTART_CHECKLIST.md`, `CONSTITUTION.md` and `TEMPLATE_GUIDE.md` — governance docs that
   legitimately *name* banned Fabric features. Those are exactly the files where the bare-`python`
   defect landed. A rule added to `BANNED_PATTERNS` would have been inert in the files it most needed
   to cover, and would have looked like it was working. `CONTENT_RULES` bypasses `EXCLUDE_FILES`
   and carries a per-rule `allow` set instead, so an exemption is one rule in one file rather than a
   whole file falling out of the scan.
2. **Exempt by adding to that rule's `allow` set, never by adding the file to `EXCLUDE_FILES`** —
   the latter silently drops the file from every banned-feature check too.

Verify on every new machine, before the first commit rather than after:

    pre-commit run --all-files

That same command catches the neighboring defect — a fresh clone has no hook at all until
`pre-commit install --hook-type pre-commit --hook-type commit-msg` runs
([[reference_macos_toolchain]] §1, [[reference_commit_attribution_gate]]).
