#!/usr/bin/env python3
"""
skill_scan.py — every skill under `.claude/skills/` loads the way its frontmatter says, names only
hooks, stages and commands that exist, and is listed in `AGENTS.md` for an agent that is not Claude.

THE FAILURE THIS CLOSES
-----------------------
Decision 2026-10-23-001 makes a skill's `SKILL.md` the one home of a procedure. A procedure names
commands, and commands drift: a hook renamed or restaged in `.pre-commit-config.yaml` leaves the
skill naming one that runs nothing, which is what the runbook page did before its gate (decision
2026-09-23-001). And Claude Code fails silently on a skill: a frontmatter that does not parse loads
the skill with no fields, so a `context: fork` or a `disable-model-invocation` is lost without a
word; a key it does not know is ignored; a directory with no `SKILL.md` is not a skill at all.

WHAT IT CHECKS
--------------
  frontmatter  the first line is not `---`, the block never closes, or it is not a YAML mapping
  key          a key Claude Code does not know, which it would ignore without a word
  name         the directory is not a plain lowercase name, or `name:` is missing or differs from it
  description  missing or empty, or past the 1,536-character listing cap with `when_to_use`
  field        `context` other than `fork`; `agent` or `background` without it; an `agent` that is
               no built-in and no `.claude/agents/<name>.md`; a flag that is not a boolean
  body         no instructions after the frontmatter
  no-skill     a directory under `.claude/skills/` with no `SKILL.md`
  hook         a `pre-commit run <id>` names a hook the config lacks
  stage        `--hook-stage` is not a stage the named hook declares (none given means
               `pre-commit`), or names a stage no hook declares
  all-files    a `pre-commit run` without `--all-files`: pre-commit stashes unstaged edits first
  script       a `scripts/<name>.py` that does not exist, or a `--flag` its source never names
  bare-gate    a script invoked with exactly a hook's entry: run it through `pre-commit run <id>`
  unlisted     a skill `AGENTS.md` does not name by path, or a path it names with no skill
  config       the config cannot be read as a suite — never read as zero hooks

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
Commands are read from inline code spans and fenced blocks only; a command written as bare prose
is not seen. It cannot tell whether the steps are right, only that what they name exists and runs
at the stage they say. A skill's `paths:` globs are not checked; no skill here sets one.

Usage:  pre-commit run skill-scan --all-files            # portable; pre-commit provides pyyaml
        python3 scripts/skill_scan.py
        python3 scripts/skill_scan.py --self-test
Exit 0 = clean, 1 = violations (blocks the commit), 2 = cannot run.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    print(
        "skill_scan: PyYAML is not installed in this interpreter.\n"
        "    This gate is normally run through pre-commit, which provisions it via\n"
        "    `additional_dependencies: [pyyaml]`:\n"
        "        pre-commit run skill-scan --all-files\n"
        "    To run it directly instead: python3 -m pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
# The runbook gate's reader, so both gates read the hook ids and stages the same way.
from gate_runbook_scan import ConfigError, config_hooks  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ".claude/skills/"
AGENTS_DIR = ".claude/agents/"
CONFIG = ROOT / ".pre-commit-config.yaml"
BRAIN = ROOT / "AGENTS.md"

# The frontmatter reference of https://code.claude.com/docs/en/skills.md, read 2026-10-23.
KNOWN_KEYS = {
    "name", "description", "when_to_use", "argument-hint", "arguments", "disable-model-invocation",
    "user-invocable", "allowed-tools", "disallowed-tools", "model", "effort", "context", "agent",
    "background", "hooks", "paths", "shell", "metadata", "license", "compatibility",
}
BOOLEAN_KEYS = ("disable-model-invocation", "user-invocable", "background")
BUILTIN_AGENTS = {"general-purpose", "Explore", "Plan", "claude"}
LISTING_CAP = 1536
RESERVED = {"synced", "anthropic-skills"}
SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE = re.compile(r"`([^`\n]+)`")
SPLIT = re.compile(r"&&|\|\||;|\|")
PRE_COMMIT_RUN = re.compile(r"\bpre-commit\s+run\b(.*)")
SCRIPT = re.compile(r"(?<![\w/.-])(?:(python3?|py)\s+)?(?:\./)?scripts/([A-Za-z0-9_]+\.py)\b(.*)")
LISTED = re.compile(r"\.claude/skills/([A-Za-z0-9_-]+)/SKILL\.md")
# `pre-commit run` options that take a value, so the value is never read as a hook id.
VALUED = {"--hook-stage", "--from-ref", "--to-ref", "--commit-msg-filename", "--color",
          "--remote-branch", "--local-branch", "--remote-name", "--remote-url", "--source", "--origin"}

FIXES = {
    "frontmatter": (
        "Open SKILL.md with `---` on line 1, close the block with `---`, and keep YAML between them\n"
        "    that parses as a mapping. Otherwise Claude Code loads the skill with no fields, silently."
    ),
    "key": (
        "Spell the key as the skills reference does (hyphens, except `when_to_use`), or remove it.\n"
        "    Claude Code ignores a key it does not know without a word."
    ),
    "name": (
        "Name the directory in lowercase words joined by hyphens, and set `name:` to exactly that\n"
        "    name, so the command, the path and AGENTS.md agree."
    ),
    "description": (
        "Give the skill a `description:` that says what it does and when to use it, key use first;\n"
        "    with `when_to_use` it is cut at 1,536 characters in the listing Claude reads."
    ),
    "field": (
        "`context` takes only `fork`; `agent` and `background` apply only with it; `agent` names a\n"
        "    built-in (general-purpose, Explore, Plan, claude) or a file in .claude/agents/; the flags\n"
        "    disable-model-invocation, user-invocable and background are `true` or `false`."
    ),
    "body": "Write the procedure below the frontmatter; a skill with no body does nothing when it runs.",
    "no-skill": (
        "Add SKILL.md to the directory or remove the directory. Claude Code loads only\n"
        "    .claude/skills/<name>/SKILL.md."
    ),
    "hook": (
        "Name a hook id that .pre-commit-config.yaml declares, exactly as `id:` spells it. If the hook\n"
        "    was renamed, the skill changes in the same commit."
    ),
    "stage": (
        "Pass `--hook-stage <stage>` with the stage the hook declares (none for `pre-commit`). A\n"
        "    wrong stage runs nothing: pre-commit finds no hook with that id at that stage."
    ),
    "all-files": (
        "Add `--all-files`. Without it pre-commit stashes unstaged edits to tracked files first and\n"
        "    the hook judges the last commit (reference_precommit_stash)."
    ),
    "script": (
        "Name a script that exists under scripts/ and only flags its source defines. If the script\n"
        "    or the flag was renamed, the skill changes in the same commit."
    ),
    "bare-gate": (
        "This command is a hook's entry. Run it as `pre-commit run <id> --all-files` (with its\n"
        "    --hook-stage), so pre-commit provisions the interpreter (reference_precommit_interpreter)."
    ),
    "unlisted": (
        "AGENTS.md names every skill by its path, `.claude/skills/<name>/SKILL.md`, so an agent that\n"
        "    is not Claude can find it (decision 2026-10-23-001); and names no path without a skill."
    ),
    "config": (
        ".pre-commit-config.yaml must parse as YAML and hold at least one hook under repos[].hooks[].\n"
        "    An unreadable config is never treated as an empty suite."
    ),
}


# ==============================================================================
# Pure functions over text — the self-test needs no files
# ==============================================================================

def hook_entries(text: str) -> dict[str, str]:
    """{hook id: entry} for the hooks that declare one. `config_hooks` has already proved the text
    is a suite, so this pass only reads."""
    out: dict[str, str] = {}
    for repo in (yaml.safe_load(text) or {}).get("repos") or []:
        for hook in (repo or {}).get("hooks") or []:
            if isinstance(hook, dict) and hook.get("id") and isinstance(hook.get("entry"), str):
                out[str(hook["id"])] = hook["entry"]
    return out


def frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """(fields, body, error). Claude Code reads frontmatter only when line 1 is `---`."""
    lines = text.split("\n")
    if lines[0].rstrip("\r") != "---":
        return None, text, "line 1 is not `---`, so Claude Code reads the whole file as the body"
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r") == "---":
            body = "\n".join(lines[i + 1:])
            try:
                data = yaml.safe_load("\n".join(lines[1:i]))
            except yaml.YAMLError as e:
                return None, body, f"YAML error: {getattr(e, 'problem', None) or str(e).splitlines()[0]}"
            if not isinstance(data, dict):
                return None, body, "the block is not a YAML mapping"
            return data, body, None
    return None, text, "the frontmatter never closes"


def code_segments(body: str) -> list[str]:
    """Lines inside fenced blocks and the contents of inline code spans."""
    out: list[str] = []
    fenced = False
    for line in body.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        out.extend([line] if fenced else INLINE.findall(line))
    return out


def commands(body: str) -> list[str]:
    return [c.strip() for seg in code_segments(body) for c in SPLIT.split(seg) if c.strip()]


def flags_of(rest: str) -> list[str]:
    """The `--flag` tokens of a command, `=value` dropped; a `<placeholder>` is never a flag."""
    return [f for f in (t.split("=", 1)[0] for t in rest.split() if t.startswith("--")) if "<" not in f]


def precommit_violations(cmd: str, stages: dict[str, list[str]]) -> list[tuple[str, str]]:
    m = PRE_COMMIT_RUN.search(cmd)
    if not m:
        return []
    tokens = m.group(1).split()
    hook = stage = None
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.startswith("--hook-stage="):
            stage = t.split("=", 1)[1]
        elif t == "--hook-stage" and i + 1 < len(tokens):
            stage = tokens[i + 1]
            i += 1
        elif t == "--files":
            break
        elif t in VALUED:
            i += 1
        elif not t.startswith("-") and hook is None:
            hook = t
        i += 1
    v: list[tuple[str, str]] = []
    if "--all-files" not in tokens and "-a" not in tokens:
        v.append(("all-files", f"`{cmd}`"))
    if hook is not None and "<" in hook:
        return v
    if hook is not None:
        if hook not in stages:
            v.append(("hook", f"`{cmd}` names `{hook}`, which the config does not declare"))
        elif (stage or "pre-commit") not in (stages[hook] or []):
            v.append(("stage", f"`{cmd}` runs `{hook}` at `{stage or 'pre-commit'}`; it declares {stages[hook]}"))
    elif stage is not None and stage not in {s for st in stages.values() for s in st or []}:
        v.append(("stage", f"`{cmd}` names stage `{stage}`, which no hook declares"))
    return v


def script_violations(cmd: str, scripts: dict[str, str], entries: dict[str, str]) -> list[tuple[str, str]]:
    m = SCRIPT.search(cmd)
    if not m:
        return []
    interpreter, name, rest = m.group(1), m.group(2), m.group(3)
    if name not in scripts:
        return [("script", f"`{cmd}` names scripts/{name}, which does not exist")]
    v = [("script", f"`{cmd}`: scripts/{name} never names `{f}`")
         for f in flags_of(rest) if f'"{f}"' not in scripts[name] and f"'{f}'" not in scripts[name]]
    if interpreter:
        named = sorted(flags_of(rest))
        for hid, entry in entries.items():
            e = SCRIPT.search(entry)
            if e and e.group(2) == name and sorted(flags_of(e.group(3))) == named:
                v.append(("bare-gate", f"`{cmd}` is the entry of hook `{hid}`"))
    return v


def lint_skill(name: str, text: str, agents: set[str], stages: dict[str, list[str]],
               entries: dict[str, str], scripts: dict[str, str]) -> list[tuple[str, str]]:
    where = f"{SKILLS}{name}/SKILL.md"
    v: list[tuple[str, str]] = []
    if not SKILL_NAME.match(name) or name in RESERVED:
        v.append(("name", f"{SKILLS}{name}/ is not a plain lowercase name, or is reserved"))
    fm, body, error = frontmatter(text)
    if error:
        v.append(("frontmatter", f"{where}: {error}"))
    fm = fm or {}
    for key in sorted(set(fm) - KNOWN_KEYS):
        v.append(("key", f"{where}: `{key}` is not a skill frontmatter key"))
    if fm.get("name") != name and not error:
        v.append(("name", f"{where}: `name:` is {fm.get('name')!r}; the directory is `{name}`"))
    desc, when = fm.get("description"), fm.get("when_to_use") or ""
    if not error and (not isinstance(desc, str) or not desc.strip()):
        v.append(("description", f"{where}: no description"))
    elif isinstance(desc, str) and len(desc) + len(str(when)) > LISTING_CAP:
        v.append(("description", f"{where}: {len(desc) + len(str(when))} characters; the listing cuts at {LISTING_CAP}"))
    for key in BOOLEAN_KEYS:
        if key in fm and not isinstance(fm[key], bool):
            v.append(("field", f"{where}: `{key}: {fm[key]!r}` is not a boolean"))
    fork = fm.get("context") == "fork"
    if "context" in fm and not fork:
        v.append(("field", f"{where}: `context: {fm['context']!r}`; the only value is `fork`"))
    for key in ("agent", "background"):
        if key in fm and not fork:
            v.append(("field", f"{where}: `{key}` applies only with `context: fork`"))
    if fork and "agent" in fm and fm["agent"] not in BUILTIN_AGENTS | agents:
        v.append(("field", f"{where}: `agent: {fm['agent']}` is no built-in and no {AGENTS_DIR}<name>.md"))
    if not body.strip():
        v.append(("body", f"{where}: nothing after the frontmatter"))
    for cmd in commands(body):
        v.extend((r, f"{where}: {d}") for r, d in precommit_violations(cmd, stages))
        v.extend((r, f"{where}: {d}") for r, d in script_violations(cmd, scripts, entries))
    return v


def scan(files: dict[str, str], config_text: str, brain: str, agents: set[str],
         scripts: dict[str, str]) -> tuple[int, list[tuple[str, str]]]:
    """(skills found, violations). `files` maps every path under .claude/skills/ git would commit
    to its text; `agents` holds the agent names in .claude/agents/; `scripts` maps each file in
    scripts/ to its source."""
    try:
        stages = {h: s or [] for h, s in config_hooks(config_text)}
        entries = hook_entries(config_text)
    except ConfigError as e:
        return 0, [("config", f".pre-commit-config.yaml: {e}")]
    dirs: dict[str, str | None] = {}
    for path, text in files.items():
        parts = path[len(SKILLS):].split("/")
        dirs.setdefault(parts[0], None)
        if parts[1:] == ["SKILL.md"]:
            dirs[parts[0]] = text
    v: list[tuple[str, str]] = []
    for name in sorted(dirs):
        if dirs[name] is None:
            v.append(("no-skill", f"{SKILLS}{name}/ holds no SKILL.md"))
            continue
        v.extend(lint_skill(name, dirs[name], agents, stages, entries, scripts))
    listed = set(LISTED.findall(brain))
    skills = {n for n, t in dirs.items() if t is not None}
    v.extend(("unlisted", f"AGENTS.md does not name {SKILLS}{n}/SKILL.md") for n in sorted(skills - listed))
    v.extend(("unlisted", f"AGENTS.md names {SKILLS}{n}/SKILL.md, which does not exist") for n in sorted(listed - skills))
    return len(skills), v


# ==============================================================================
# Real tree
# ==============================================================================

def would_commit(prefix: str) -> list[str]:
    """Files under `prefix` that git would commit: tracked, or untracked and not ignored."""
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", prefix],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return sorted({p for p in out.splitlines() if (ROOT / p).is_file()})


def check() -> int:
    try:
        config_text = CONFIG.read_text(encoding="utf-8")
        files = {p: (ROOT / p).read_text(encoding="utf-8") for p in would_commit(SKILLS)}
        agents = {Path(p).stem for p in would_commit(AGENTS_DIR) if p.endswith(".md")}
        scripts = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / "scripts").glob("*.py")}
        brain = BRAIN.read_text(encoding="utf-8") if BRAIN.is_file() else ""
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"skill_scan: cannot read the tree: {e}", file=sys.stderr)
        return 2
    count, found = scan(files, config_text, brain, agents, scripts)

    print("\nSkill Scan Results")
    print("=" * 60)
    print(f"Skills: {count}   Violations: {len(found)}")
    if found:
        print("\n" + "!" * 60)
        print("BLOCKED: a skill would load differently than written, or names what the suite lacks\n")
        for rule, detail in found:
            print(f"  Rule:    {rule}\n  Detail:  {detail}\n  Fix:     {FIXES[rule]}\n")
        return 1
    print("\nPASSED: every skill parses, names real hooks, stages and scripts, and AGENTS.md lists it")
    return 0


# ==============================================================================
# SELF-TEST — every rule has a passing and a failing case
# ==============================================================================

_CONFIG = """repos:
  - repo: local
    hooks:
      - id: alpha-selftest
        entry: scripts/alpha.py --self-test
        language: python
        stages: [pre-commit]
      - id: alpha
        entry: scripts/alpha.py
        language: python
        stages: [pre-commit]
      - id: closeout
        entry: scripts/closer.py --closeout
        language: python
        stages: [manual]
      - id: attribution
        entry: scripts/attr.py
        language: python
        stages: [commit-msg]
"""

_SCRIPTS = {
    "alpha.py": 'parser.add_argument("--self-test")\n',
    "closer.py": 'parser.add_argument("--closeout")\nparser.add_argument("--scaffold")\n'
                 "parser.add_argument('--persona')\n",
    "attr.py": "",
}

_FORK = """---
name: closeout
description: 'Close the session: scaffold, gate, commit, push.'
argument-hint: <persona> <brief>
context: fork
agent: general-purpose
background: false
---

# Closeout

1. `python3 scripts/closer.py --scaffold --persona <slug>` writes the pair.
2. Run the gate:

   ```
   pre-commit run closeout --hook-stage manual --all-files
   git add -A && pre-commit run --all-files
   ```

Prose may say pre-commit run closeout without a stage; only code is read.
"""

_INLINE = """---
name: release
description: Cut a release. Operator only.
disable-model-invocation: true
---

Run `pre-commit run alpha --all-files`; its self-test is `pre-commit run alpha-selftest --all-files`.
"""

_BRAIN = """# Brain

| `.claude/skills/closeout/SKILL.md` | session end |
| `.claude/skills/release/SKILL.md` | release |
"""


def run_self_test() -> int:
    print("\nSkill Scan Self-Test")
    print("=" * 60)
    failures = total = 0

    def check_(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    def run(fork: str = _FORK, inline: str = _INLINE, brain: str = _BRAIN, config: str = _CONFIG,
            extra: dict | None = None, agents: set | None = None) -> list:
        files = {f"{SKILLS}closeout/SKILL.md": fork, f"{SKILLS}release/SKILL.md": inline, **(extra or {})}
        return scan(files, config, brain, agents if agents is not None else {"framework-maintainer"}, _SCRIPTS)[1]

    def expect(label: str, found: list, *rules: str) -> None:
        got = sorted(r for r, _ in found)
        check_(label, got == sorted(rules), f"rules={got} expected={sorted(rules)}  {found}")

    check_("commands are read from fences and code spans, split at && and ;, never from prose",
           commands(_FORK) == ["python3 scripts/closer.py --scaffold --persona <slug>",
                               "pre-commit run closeout --hook-stage manual --all-files",
                               "git add -A", "pre-commit run --all-files"], str(commands(_FORK)))
    check_("the frontmatter is read as YAML, booleans as booleans",
           frontmatter(_FORK)[0]["background"] is False and frontmatter(_FORK)[2] is None)
    expect("a fork skill and an inline skill that match the config pass", run())

    # frontmatter
    expect("line 1 not `---` fails", run(fork="\n" + _FORK), "frontmatter")
    expect("a frontmatter that never closes fails", run(fork=_FORK.replace("background: false\n---", "background: false\n")), "frontmatter")
    expect("YAML that does not parse fails (Claude Code would drop `context: fork` silently)",
           run(fork=_FORK.replace("argument-hint: <persona> <brief>", "argument-hint: [persona")), "frontmatter")
    expect("a frontmatter that is not a mapping fails", run(inline="---\n- a\n---\nbody\n"), "frontmatter")
    # keys and fields
    expect("an unknown key fails (Claude Code ignores it)",
           run(inline=_INLINE.replace("disable-model-invocation", "disable_model_invocation")), "key")
    expect("`name:` differing from the directory fails", run(inline=_INLINE.replace("name: release", "name: cut")), "name")
    expect("`name:` missing fails", run(inline=_INLINE.replace("name: release\n", "")), "name")
    expect("a directory name with capitals fails",
           run(extra={f"{SKILLS}Bad/SKILL.md": "---\nname: Bad\ndescription: x\n---\nbody\n"},
               brain=_BRAIN + ".claude/skills/Bad/SKILL.md\n"), "name")
    expect("a missing description fails", run(inline=_INLINE.replace("description: Cut a release. Operator only.\n", "")), "description")
    expect("a description past the listing cap fails",
           run(inline=_INLINE.replace("Cut a release.", "x" * 1600)), "description")
    expect("a flag that is not a boolean fails", run(inline=_INLINE.replace("invocation: true", "invocation: 'true'")), "field")
    expect("`background` that is not a boolean fails", run(fork=_FORK.replace("background: false", "background: 'false'")), "field")
    expect("`context` other than fork fails", run(fork=_FORK.replace("context: fork", "context: forked")), "field", "field", "field")
    expect("`agent` without `context: fork` fails", run(inline=_INLINE.replace("---\n\nRun", "agent: Explore\n---\n\nRun")), "field")
    expect("an `agent` that is no built-in and no agent file fails",
           run(fork=_FORK.replace("agent: general-purpose", "agent: closer")), "field")
    expect("a project agent from .claude/agents/ is accepted",
           run(fork=_FORK.replace("agent: general-purpose", "agent: framework-maintainer")))
    expect("an empty body fails", run(inline=_INLINE.split("\n\nRun")[0] + "\n"), "body")
    expect("a directory with no SKILL.md fails", run(extra={f"{SKILLS}draft/notes.md": "x"}), "no-skill")
    expect("a supporting file beside SKILL.md is not a skill", run(extra={f"{SKILLS}closeout/reference.md": "x"}))
    expect("a SKILL.md one level too deep is no skill",
           run(extra={f"{SKILLS}draft/sub/SKILL.md": "---\nname: sub\ndescription: x\n---\nbody\n"}), "no-skill")
    # hooks and stages
    expect("a hook id the config lacks fails",
           run(fork=_FORK.replace("pre-commit run closeout", "pre-commit run close-out")), "hook")
    expect("a stage the hook does not declare fails",
           run(fork=_FORK.replace("--hook-stage manual", "--hook-stage commit-msg")), "stage")
    expect("a manual hook run without --hook-stage fails", run(fork=_FORK.replace(" --hook-stage manual", "")), "stage")
    expect("a pre-commit hook run at another stage fails",
           run(inline=_INLINE.replace("pre-commit run alpha --all-files", "pre-commit run alpha --hook-stage manual --all-files")), "stage")
    expect("`--hook-stage=` is read like the spaced form",
           run(fork=_FORK.replace("--hook-stage manual", "--hook-stage=manual")))
    expect("a whole-suite run at a stage no hook declares fails",
           run(fork=_FORK.replace("pre-commit run --all-files", "pre-commit run --hook-stage pre-push --all-files")), "stage")
    expect("a run without --all-files fails", run(fork=_FORK.replace("--hook-stage manual --all-files", "--hook-stage manual")), "all-files")
    expect("an option's value is never read as a hook id (the CI's commit-msg form passes)",
           run(fork=_FORK.replace("pre-commit run --all-files",
                                  "pre-commit run --hook-stage commit-msg --commit-msg-filename msg.txt --all-files")))
    expect("a placeholder hook id is not judged", run(inline=_INLINE.replace("run alpha --all", "run <hook-id> --all")))
    # scripts
    expect("a script that does not exist fails", run(fork=_FORK.replace("scripts/closer.py --scaffold", "scripts/closure.py --scaffold")), "script")
    expect("a flag the script never names fails", run(fork=_FORK.replace("--scaffold", "--scafold")), "script")
    expect("a flag in the `--flag=value` form is read as the flag, here one named in single quotes",
           run(fork=_FORK.replace("--persona <slug>", "--persona=<slug>")))
    expect("a flag in the `--flag=value` form the script never names fails",
           run(fork=_FORK.replace("--persona <slug>", "--persons=<slug>")), "script")
    expect("a hook's entry run with an interpreter fails",
           run(inline=_INLINE + "\n`python3 scripts/alpha.py --self-test`\n"), "bare-gate")
    expect("a hook's entry with no flags, run bare, fails", run(inline=_INLINE + "\n`python3 scripts/alpha.py`\n"), "bare-gate")
    expect("a script mentioned without an interpreter is not a bare gate", run(inline=_INLINE + "\n`scripts/alpha.py`\n"))
    # AGENTS.md
    expect("a skill AGENTS.md does not name fails", run(brain=_BRAIN.replace("| `.claude/skills/release/SKILL.md` | release |\n", "")), "unlisted")
    expect("a path AGENTS.md names with no skill fails", run(brain=_BRAIN + "`.claude/skills/ghost/SKILL.md`\n"), "unlisted")
    # config
    for label, text in (("unparsable YAML", "repos: [\n"), ("zero hooks", "repos:\n  - repo: local\n    hooks: []\n")):
        expect(f"a config with {label} is refused, never read as an empty suite", run(config=text), "config")

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Every skill parses, names real hooks and scripts, and is listed")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()
    return run_self_test() if args.self_test else check()


if __name__ == "__main__":
    sys.exit(main())
