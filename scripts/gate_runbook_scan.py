#!/usr/bin/env python3
"""
gate_runbook_scan.py — every hook in `.pre-commit-config.yaml` has a section in the gate-suite
runbook, every section names a hook, and the page tells the truth about order and stage.

THE FAILURE THIS CLOSES
-----------------------
`TEMPLATE_GUIDE.md` Step 6 carried a table of the gates. It was written by hand, keyed by script
rather than by hook id, and nothing compared it to the config. By the time it was replaced it
was already a hook behind and had never named a stage. A page that describes the suite is what the
next reader consults instead of the config, so a stale page is a fossil in the one place that
claims to be the map (`CONSTITUTION.md` §6.3, decision 2026-09-23-001).

WHAT IT CHECKS
--------------
The hook ids are read from `.pre-commit-config.yaml` with a YAML parser, every repo included.
The sections are the H2 headings of `docs/governance/gate_suite_runbook.md`, outside fenced code.

  no-section   a hook id in the config has no `## \\`<id>\\`` section
  no-hook      a section names no hook id in the config
  order        the sections are not in the config's run order
  stage        a section's `**Stage:**` line is missing or disagrees with the config
  no-stages    a hook declares no `stages:` — it would run at every installed stage
               (decision 2026-09-20-001 required this of every hook; this is the control)
  config       the config cannot be parsed or holds no hooks — never read as zero hooks
  no-page      the runbook is missing

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It cannot read prose. What a section says a gate blocks, and why, is the author's to keep true.
It proves the page's shape follows the config: nothing listed that does not exist, nothing that
exists left out, and the stage a reader will pass to `--hook-stage` is the one the hook declares.

Usage:  pre-commit run gate-runbook --all-files            # portable; pre-commit provides pyyaml
        python3 scripts/gate_runbook_scan.py [--config PATH] [--page PATH]
        python3 scripts/gate_runbook_scan.py --self-test
Exit 0 = clean, 1 = violations (blocks the commit), 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".pre-commit-config.yaml"
PAGE = ROOT / "docs" / "governance" / "gate_suite_runbook.md"
WORKFLOW = ROOT / ".github" / "workflows" / "gates.yml"
# A `pre-commit run` in a workflow step covers the stage it names, or the pre-commit stage when
# it names none. The CI backstop (decision 2026-09-22-001) is the same suite with a second
# trigger, so every non-manual stage the config declares needs one of these.
PRE_COMMIT_RUN = re.compile(r"\bpre-commit\s+run\b([^\n|&;]*)")
HOOK_STAGE = re.compile(r"--hook-stage[\s=]+([a-z][a-z-]*)")

H2 = re.compile(r"^## (.+?)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
STAGE = re.compile(r"^\*\*Stage:\*\*\s*`?([a-z][a-z-]*)`?", re.M)

try:
    import yaml
except ModuleNotFoundError:
    print(
        "gate_runbook_scan: PyYAML is not installed in this interpreter.\n"
        "    This gate is normally run through pre-commit, which provisions it via\n"
        "    `additional_dependencies: [pyyaml]`:\n"
        "        pre-commit run gate-runbook --all-files\n"
        "    To run it directly instead: python3 -m pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)

FIXES = {
    "no-section": (
        "Add a `## `<hook-id>`` section to docs/governance/gate_suite_runbook.md at the hook's\n"
        "    position in run order: its **Stage:**, the self-test it pairs with, what it blocks,\n"
        "    why it exists (link the decision and the knowledge entry), and the command to run it alone."
    ),
    "no-hook": (
        "The runbook has a section for a hook id that is not in .pre-commit-config.yaml.\n"
        "    Remove the section, or rename it to the hook's id exactly as `id:` spells it.\n"
        "    Every H2 on that page is a hook id; prose that is not about one hook goes above the first H2."
    ),
    "order": (
        "Reorder the sections to match the order of the hooks in .pre-commit-config.yaml,\n"
        "    which is the order pre-commit runs them. The page is read as a run sequence."
    ),
    "stage": (
        "Give the section a line `**Stage:** `<stage>`` naming the stage the hook declares in\n"
        "    .pre-commit-config.yaml (pre-commit, commit-msg or manual). A reader passes that value\n"
        "    to --hook-stage; a wrong one runs nothing."
    ),
    "no-stages": (
        "Declare `stages: [pre-commit]` (or commit-msg, or manual) on the hook. A hook with no\n"
        "    `stages:` runs at every installed stage — twice per commit with both hook types\n"
        "    installed (decision 2026-09-20-001)."
    ),
    "config": (
        ".pre-commit-config.yaml must parse as YAML and hold at least one hook under repos[].hooks[].\n"
        "    An unreadable config is never treated as an empty suite."
    ),
    "no-page": (
        "Create docs/governance/gate_suite_runbook.md with one `## `<hook-id>`` section per hook,\n"
        "    in run order. TEMPLATE_GUIDE.md Step 6 links to it."
    ),
    "no-ci-step": (
        "Add a step to .github/workflows/gates.yml that runs `pre-commit run --hook-stage <stage> ...`\n"
        "    for this stage (the pre-commit stage is covered by a plain `pre-commit run --all-files`).\n"
        "    A stage the workflow never runs is present in config and absent on CI\n"
        "    (decision 2026-09-22-001, reference_ci_backstop)."
    ),
    "workflow": (
        ".github/workflows/gates.yml must exist and parse as YAML with at least one job step.\n"
        "    It is the backstop for a clone that never installed hooks; restore it from the template."
    ),
}


class ConfigError(Exception):
    """The hook config cannot be read as a suite."""


# ==============================================================================
# Pure functions over text — the self-test needs no files
# ==============================================================================

def config_hooks(text: str) -> list[tuple[str, list[str] | None]]:
    """[(hook id, stages or None)] in run order, every repo included."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ConfigError(f"YAML error: {getattr(e, 'problem', None) or str(e).splitlines()[0]}") from e
    if not isinstance(data, dict) or not isinstance(data.get("repos"), list):
        raise ConfigError("no `repos:` list")
    hooks: list[tuple[str, list[str] | None]] = []
    for repo in data["repos"]:
        for hook in (repo or {}).get("hooks") or []:
            hid = hook.get("id") if isinstance(hook, dict) else None
            if not hid:
                raise ConfigError("a hook has no `id:`")
            stages = hook.get("stages")
            hooks.append((str(hid), [str(s) for s in stages] if isinstance(stages, list) else None))
    if not hooks:
        raise ConfigError("no hooks under repos[].hooks[]")
    return hooks


def page_sections(text: str) -> list[tuple[str, str | None]]:
    """[(section id, stage named or None)] from the H2 headings outside fenced code."""
    out: list[tuple[str, list[str]]] = []
    fenced = False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        m = None if fenced else H2.match(line)
        if m:
            out.append((m.group(1).strip().strip("`").strip(), []))
        elif out:
            out[-1][1].append(line)
    result = []
    for sid, body in out:
        sm = STAGE.search("\n".join(body))
        result.append((sid, sm.group(1) if sm else None))
    return result


def workflow_stages(text: str) -> set[str]:
    """The stages the workflow's `run:` steps cover. Raises ConfigError when the workflow is not a
    workflow: an unreadable one is never read as covering nothing, because that would fail every
    stage with the wrong diagnosis."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ConfigError(f"not valid YAML: {getattr(e, 'problem', e)}") from None
    jobs = (data or {}).get("jobs") if isinstance(data, dict) else None
    if not isinstance(jobs, dict) or not jobs:
        raise ConfigError("holds no `jobs:`")
    covered: set[str] = set()
    steps_seen = 0
    for job in jobs.values():
        for step in (job or {}).get("steps") or []:
            steps_seen += 1
            run = (step or {}).get("run")
            if not isinstance(run, str):
                continue
            for m in PRE_COMMIT_RUN.finditer(run):
                stage = HOOK_STAGE.search(m.group(1))
                covered.add(stage.group(1) if stage else "pre-commit")
    if not steps_seen:
        raise ConfigError("holds no job steps")
    return covered


def stage_violations(hooks: list[tuple[str, list[str] | None]], covered: set[str]) -> list[tuple[str, str]]:
    """Every non-manual stage a hook declares must be run by the workflow."""
    v: list[tuple[str, str]] = []
    by_stage: dict[str, list[str]] = {}
    for hid, stages in hooks:
        for st in stages or []:
            by_stage.setdefault(st, []).append(hid)
    for st in sorted(by_stage):
        if st != "manual" and st not in covered:
            v.append(("no-ci-step", f"stage `{st}` is declared by {by_stage[st]} and no workflow step runs it"))
    return v


def violations(hooks: list[tuple[str, list[str] | None]],
               sections: list[tuple[str, str | None]]) -> list[tuple[str, str]]:
    v: list[tuple[str, str]] = []
    ids = [h for h, _ in hooks]
    stages = dict(hooks)
    section_ids = [s for s, _ in sections]
    for hid, st in hooks:
        if st is None or not st:
            v.append(("no-stages", f"hook `{hid}` declares no stages"))
    for hid in ids:
        if hid not in section_ids:
            v.append(("no-section", f"hook `{hid}` has no section in the runbook"))
    for sid in section_ids:
        if sid not in ids:
            v.append(("no-hook", f"section `{sid}` names no hook in the config"))
    for sid, stage in sections:
        if sid not in stages:
            continue
        want = stages[sid] or []
        if stage is None:
            v.append(("stage", f"section `{sid}` has no `**Stage:**` line; the hook declares {want}"))
        elif [stage] != want:
            v.append(("stage", f"section `{sid}` says stage `{stage}`; the hook declares {want}"))
    matched_config = [h for h in ids if h in section_ids]
    matched_page = [s for s in section_ids if s in ids]
    if matched_config != matched_page:
        v.append(("order", f"sections run {matched_page}; the config runs {matched_config}"))
    return v


# ==============================================================================
# Real tree
# ==============================================================================

def check(config_path: Path, page_path: Path, workflow_path: Path) -> int:
    found: list[tuple[str, str]] = []
    hooks: list[tuple[str, list[str] | None]] = []
    try:
        hooks = config_hooks(config_path.read_text(encoding="utf-8"))
    except (OSError, ConfigError) as e:
        found.append(("config", f"{config_path.name}: {e}"))
    if not page_path.is_file():
        found.append(("no-page", f"{page_path.relative_to(ROOT) if page_path.is_relative_to(ROOT) else page_path} is missing"))
    elif hooks:
        found.extend(violations(hooks, page_sections(page_path.read_text(encoding="utf-8"))))
    if hooks:
        try:
            found.extend(stage_violations(hooks, workflow_stages(workflow_path.read_text(encoding="utf-8"))))
        except (OSError, ConfigError) as e:
            found.append(("workflow", f"{workflow_path.name}: {e}"))

    print("\nGate Runbook Scan Results")
    print("=" * 60)
    print(f"Hooks in config: {len(hooks)}   Violations: {len(found)}")
    if found:
        print("\n" + "!" * 60)
        print("BLOCKED: the runbook or the workflow does not describe the suite the config runs\n")
        for rule, detail in found:
            print(f"  Rule:    {rule}\n  Detail:  {detail}\n  Fix:     {FIXES[rule]}\n")
        return 1
    print("\nPASSED: one section per hook, in run order, each naming its stage; every stage has a CI step")
    return 0


# ==============================================================================
# SELF-TEST — every rule has a passing and a failing case
# ==============================================================================

_CONFIG = """repos:
  - repo: local
    hooks:
      - id: alpha-selftest
        name: Alpha Self-Test
        entry: alpha --self-test
        language: python
        stages: [pre-commit]
      - id: alpha
        name: Alpha Gate
        entry: alpha
        language: python
        stages: [pre-commit]
      - id: closeout
        name: Manual
        entry: closeout
        language: python
        stages: [manual]
      - id: attribution
        name: Commit message
        entry: attribution
        language: python
        stages: [commit-msg]
  - repo: https://github.com/example/remote
    rev: v1.0.0
    hooks:
      - id: remote-gate
        stages: [pre-commit]
"""

_WORKFLOW = """name: gates
on: [push]
jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pre-commit
      - name: Pre-commit-stage gates
        run: pre-commit run --all-files --show-diff-on-failure
      - name: Commit-msg-stage gate
        run: |
          for sha in $(git rev-list HEAD~1..HEAD); do
            git log -1 --format=%B "$sha" > /tmp/msg
            pre-commit run --hook-stage commit-msg --commit-msg-filename /tmp/msg --all-files
          done
"""

_PAGE = """# Gate suite

Prose above the first H2 may mention `alpha` and `remote-gate` freely; only H2s are sections.

## `alpha-selftest`

**Stage:** `pre-commit`
**Pairs with:** `alpha`

## `alpha`

**Stage:** `pre-commit`

```
## `not-a-hook`
**Stage:** `manual`
```

## `closeout`

**Stage:** `manual`

## `attribution`

**Stage:** `commit-msg`

## `remote-gate`

**Stage:** `pre-commit`
"""


def run_self_test() -> int:
    print("\nGate Runbook Self-Test")
    print("=" * 60)
    failures = total = 0

    def check_(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    def expect(label: str, found: list, *rules: str) -> None:
        got = sorted(r for r, _ in found)
        check_(label, got == sorted(rules), f"rules={got} expected={sorted(rules)}")

    hooks = config_hooks(_CONFIG)
    page = page_sections(_PAGE)
    check_("hook ids are read from every repo, in order, with their stages",
           [h for h, _ in hooks] == ["alpha-selftest", "alpha", "closeout", "attribution", "remote-gate"]
           and dict(hooks)["closeout"] == ["manual"], str(hooks))
    check_("sections are the H2s outside fenced code, with the stage each names",
           page == [("alpha-selftest", "pre-commit"), ("alpha", "pre-commit"), ("closeout", "manual"),
                    ("attribution", "commit-msg"), ("remote-gate", "pre-commit")], str(page))
    expect("a page that matches the config passes", violations(hooks, page))
    expect("a hook with no section fails",
           violations(config_hooks(_CONFIG + "      - id: beta\n        stages: [pre-commit]\n"), page), "no-section")
    expect("a section naming no hook fails",
           violations(hooks, page_sections(_PAGE + "\n## `gamma`\n\n**Stage:** `pre-commit`\n")), "no-hook")
    expect("a remote repo's hook is counted like a local one",
           violations(hooks, page_sections(_PAGE.split("## `remote-gate`")[0])), "no-section")
    swapped = _PAGE.replace("## `alpha-selftest`\n\n**Stage:** `pre-commit`\n**Pairs with:** `alpha`\n\n## `alpha`\n\n**Stage:** `pre-commit`\n",
                            "## `alpha`\n\n**Stage:** `pre-commit`\n\n## `alpha-selftest`\n\n**Stage:** `pre-commit`\n**Pairs with:** `alpha`\n")
    check_("fixture: the swap changed the page", swapped != _PAGE)
    expect("sections out of run order fail", violations(hooks, page_sections(swapped)), "order")
    expect("a stage line that disagrees with the config fails",
           violations(hooks, page_sections(_PAGE.replace("## `closeout`\n\n**Stage:** `manual`", "## `closeout`\n\n**Stage:** `pre-commit`"))),
           "stage")
    expect("a missing stage line fails",
           violations(hooks, page_sections(_PAGE.replace("## `attribution`\n\n**Stage:** `commit-msg`\n", "## `attribution`\n\ntext\n"))),
           "stage")
    expect("a hook that declares no stages fails, even with a matching section",
           violations(config_hooks(_CONFIG.replace("        stages: [commit-msg]\n", "")), page), "no-stages", "stage")
    expect("a bare-word H2 is read as the id it names", violations(hooks, page_sections(_PAGE.replace("## `alpha`", "## alpha"))))
    for label, text in (("unparsable YAML", "repos: [\n"), ("no repos list", "hooks: []\n"),
                        ("zero hooks", "repos:\n  - repo: local\n    hooks: []\n")):
        try:
            config_hooks(text)
            check_(f"a config with {label} is refused, never read as an empty suite", False)
        except ConfigError:
            check_(f"a config with {label} is refused, never read as an empty suite", True)

    covered = workflow_stages(_WORKFLOW)
    check_("the workflow's steps cover the pre-commit stage (plain run) and commit-msg (--hook-stage)",
           covered == {"pre-commit", "commit-msg"}, str(covered))
    expect("every non-manual stage with a step passes; manual needs none", stage_violations(hooks, covered))
    expect("a stage the workflow never runs fails",
           stage_violations(config_hooks(_CONFIG + "      - id: pushed\n        stages: [pre-push]\n"), covered), "no-ci-step")
    expect("a workflow that dropped the commit-msg step fails that stage only",
           stage_violations(hooks, workflow_stages(_WORKFLOW.split("      - name: Commit-msg")[0])), "no-ci-step")
    check_("--hook-stage is read whether spaced or with an equals sign, and only from pre-commit run lines",
           workflow_stages(_WORKFLOW.replace("--hook-stage commit-msg", "--hook-stage=commit-msg")) == {"pre-commit", "commit-msg"}
           and workflow_stages("jobs:\n  g:\n    steps:\n      - run: echo --hook-stage pre-push\n") == set())
    for label, text in (("unparsable YAML", "jobs: [\n"), ("no jobs", "name: x\non: push\n"),
                        ("no steps", "jobs:\n  g:\n    runs-on: x\n")):
        try:
            workflow_stages(text)
            check_(f"a workflow with {label} is refused, never read as covering nothing", False)
        except ConfigError:
            check_(f"a workflow with {label} is refused, never read as covering nothing", True)

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Every hook has a runbook section; every section names a hook")
    parser.add_argument("--config", default=str(CONFIG), help="hook config to read (default: the repo's)")
    parser.add_argument("--page", default=str(PAGE), help="runbook page to read (default: the repo's)")
    parser.add_argument("--workflow", default=str(WORKFLOW), help="CI workflow to read (default: the repo's)")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    return check(Path(args.config), Path(args.page), Path(args.workflow))


if __name__ == "__main__":
    sys.exit(main())
