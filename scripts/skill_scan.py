#!/usr/bin/env python3
"""
skill_scan.py — every skill under `.claude/skills/` loads the way its frontmatter says, names only
hooks, stages, commands and personas that exist, and is listed in `AGENTS.md` for an agent that is
not Claude; a connection the team-selection skill offers is written only where it was chosen.

THE FAILURE THIS CLOSES
-----------------------
Decision 2026-10-23-001 makes a skill's `SKILL.md` the one home of a procedure. A procedure names
commands, and commands drift: a hook renamed or restaged in `.pre-commit-config.yaml` leaves the
skill naming one that runs nothing, which is what the runbook page did before its gate (decision
2026-09-23-001). And Claude Code fails silently on a skill: a frontmatter that does not parse loads
the skill with no fields, so a `context: fork` or a `disable-model-invocation` is lost without a
word; a key it does not know is ignored; a directory with no `SKILL.md` is not a skill at all.
Team presets name library personas the same way, so a rename would leave a preset pointing at
nothing; and an MCP connection runs code on the operator's machine, so it belongs only in a project
that activated its persona and said yes (decision 2026-10-23-012).

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
  preset       the team-selection skill holds no single fenced `yaml` block with `presets:`, or
               one that does not parse, or a preset that is not a list of personas `personas/`
               holds, each once
  connection   a connection in that block that names no library persona, is not a server with a
               `command` and `args`, or pins no exact version; or `.mcp.json` holding it in the
               template, in a project whose roster lacks its persona, or other than the skill
               gives it; or `.mcp.json` that does not parse

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
Commands are read from inline code spans and fenced blocks only; a command written as bare prose
is not seen. It cannot tell whether the steps are right, only that what they name exists and runs
at the stage they say. A skill's `paths:` globs are not checked; no skill here sets one. Whether a
preset is the right team is the Chair's judgement; whether the operator approved the connection in
Claude Code is per clone and outside the repository.

Usage:  pre-commit run skill-scan --all-files            # portable; pre-commit provides pyyaml
        python3 scripts/skill_scan.py
        python3 scripts/skill_scan.py --self-test
Exit 0 = clean, 1 = violations (blocks the commit), 2 = cannot run.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import textwrap
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
LIBRARY_DIR = "personas/"                # the persona library a preset names from
TEAM_SKILL = "team-selection"            # the skill holding the presets and connections
MCP_CONFIG = ".mcp.json"                 # Claude Code's project-scoped MCP servers
PROFILE = ROOT / ".project-profile"      # present in a project, absent in the template

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
# An argument that pins one release: `name==1.2.3` for pip and uv, `name@1.2.3` for uvx's short form,
# or a git source at a full commit (`git+https://host/repo.git@<40 hex>#subdirectory=…`); a tag or a
# branch can move, so it is no pin.
PINNED = re.compile(r"^(?:(?P<package>[A-Za-z0-9][A-Za-z0-9._-]*)(?:==|@)\d+(?:\.\d+)*"
                    r"|(?P<repo>git\+https://[^@\s#]+)@[0-9a-f]{40}(?:#\S+)?)$")
PACKAGE = re.compile(r"[=<>~!@\[]")      # where a requirement's package name ends
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
    "preset": (
        "Keep one fenced ```yaml block in the team-selection skill whose `presets:` maps each preset's\n"
        "    name to a list of persona slugs, each a file in personas/ and named once. A persona renamed\n"
        "    in the library is renamed in the presets in the same commit (decision 2026-10-23-012)."
    ),
    "connection": (
        "A connection is keyed by a library persona and gives a server with a `command`, `args` and an\n"
        "    exact version (`<package>==<version>`, `<package>@<version>`, or `git+https://…@<full commit>`).\n"
        "    It is written to .mcp.json\n"
        "    only in a project whose roster holds the persona, on the operator's yes, exactly as the skill\n"
        "    gives it; the template enables none. To change it, change the skill and re-vet."
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


def yaml_blocks(body: str) -> list[str]:
    """The text of each fenced block whose info string is `yaml`. YAML reads a block indented
    under a list item as it is."""
    out: list[str] = []
    block: list[str] | None = None
    fenced = False
    for line in body.splitlines():
        if FENCE.match(line):
            if block is not None:
                out.append("\n".join(block))
            fenced = not fenced
            block = [] if fenced and line.strip()[3:].strip() == "yaml" else None
            continue
        if block is not None:
            block.append(line)
    return out


def team_block(text: str) -> tuple[dict | None, list[tuple[str, str]]]:
    """The team-selection skill's one `presets:` block. A yaml block that does not parse is
    refused, since it may be the one; none or two is refused, never read as no presets."""
    where = f"{SKILLS}{TEAM_SKILL}/SKILL.md"
    found: list[dict] = []
    for block in yaml_blocks(frontmatter(text)[1]):
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError as e:
            return None, [("preset", f"{where}: a fenced yaml block does not parse: "
                                     f"{getattr(e, 'problem', None) or str(e).splitlines()[0]}")]
        if isinstance(data, dict) and "presets" in data:
            found.append(data)
    if len(found) != 1:
        return None, [("preset", f"{where}: {len(found)} fenced yaml blocks hold `presets:`; it needs one")]
    return found[0], []


def preset_violations(data: dict, library: set[str]) -> list[tuple[str, str]]:
    where = f"{SKILLS}{TEAM_SKILL}/SKILL.md"
    presets = data.get("presets")
    if not isinstance(presets, dict) or not presets:
        return [("preset", f"{where}: `presets:` is not a mapping of preset names to persona lists")]
    v: list[tuple[str, str]] = []
    for name, members in presets.items():
        if not isinstance(members, list) or not members or not all(isinstance(m, str) for m in members):
            v.append(("preset", f"{where}: preset `{name}` is not a list of persona slugs"))
            continue
        v.extend(("preset", f"{where}: preset `{name}` names `{m}`, which {LIBRARY_DIR} lacks")
                 for m in members if m not in library)
        v.extend(("preset", f"{where}: preset `{name}` names `{m}` twice")
                 for m in sorted({m for m in members if members.count(m) > 1}))
    return v


def documented_connections(data: dict, library: set[str]) -> tuple[list[tuple[str, str, dict, str]], list]:
    """([(persona, server name, server, package)], violations) from the block's `connections:`."""
    where = f"{SKILLS}{TEAM_SKILL}/SKILL.md"
    conns = data.get("connections", {})
    if not isinstance(conns, dict):
        return [], [("connection", f"{where}: `connections:` is not a mapping of personas to servers")]
    out: list[tuple[str, str, dict, str]] = []
    v: list[tuple[str, str]] = []
    for persona, servers in conns.items():
        if persona not in library:
            v.append(("connection", f"{where}: connection `{persona}` names no persona in {LIBRARY_DIR}"))
        if not isinstance(servers, dict) or not servers:
            v.append(("connection", f"{where}: connection `{persona}` gives no server"))
            continue
        for name, server in servers.items():
            args = server.get("args") if isinstance(server, dict) else None
            if not (isinstance(server, dict) and isinstance(server.get("command"), str) and isinstance(args, list)
                    and all(isinstance(a, str) for a in args)):
                v.append(("connection", f"{where}: `{name}` is not a server with a `command` and a list of `args`"))
                continue
            pins = [m.group("package") or m.group("repo") for m in map(PINNED.match, args) if m]
            if not pins:
                v.append(("connection", f"{where}: `{name}` pins no exact version in its args {args}"))
                continue
            out.append((persona, name, server, pins[0]))
    return out, v


def mcp_violations(documented: list[tuple[str, str, dict, str]], mcp: str | None, roster: set[str],
                   project: bool) -> list[tuple[str, str]]:
    """Each server in .mcp.json that is a documented connection, by its name or by running its
    package, is written only in a project, with its persona in the roster, exactly as documented."""
    if mcp is None or not documented:
        return []
    try:
        config = json.loads(mcp)
    except json.JSONDecodeError as e:
        return [("connection", f"{MCP_CONFIG} does not parse as JSON: {e}")]
    servers = config.get("mcpServers", {}) if isinstance(config, dict) else None
    if not isinstance(servers, dict):
        return [("connection", f"{MCP_CONFIG} is not an object whose `mcpServers` maps names to servers")]
    v: list[tuple[str, str]] = []
    for persona, key, server, package in documented:
        for name, entry in servers.items():
            args = entry.get("args") if isinstance(entry, dict) else None
            runs = isinstance(args, list) and any(isinstance(a, str) and PACKAGE.split(a, 1)[0] == package for a in args)
            if name != key and not runs:
                continue
            if not project:
                v.append(("connection", f"{MCP_CONFIG}: `{name}` is the {persona} connection; the template enables none"))
            elif persona not in roster:
                v.append(("connection", f"{MCP_CONFIG}: `{name}` is the {persona} connection, and the roster holds no {persona}"))
            elif name != key or entry != server:
                v.append(("connection", f"{MCP_CONFIG}: `{name}` differs from the `{key}` server the skill gives"))
    return v


def team_violations(files: dict[str, str], library: set[str], roster: set[str], mcp: str | None,
                    project: bool) -> list[tuple[str, str]]:
    text = files.get(f"{SKILLS}{TEAM_SKILL}/SKILL.md")
    if text is None:
        return []
    data, v = team_block(text)
    if data is None:
        return v
    documented, cv = documented_connections(data, library)
    return preset_violations(data, library) + cv + mcp_violations(documented, mcp, roster, project)


def scan(files: dict[str, str], config_text: str, brain: str, agents: set[str],
         scripts: dict[str, str], library: set[str] | None = None, mcp: str | None = None,
         project: bool = False) -> tuple[int, list[tuple[str, str]]]:
    """(skills found, violations). `files` maps every path under .claude/skills/ git would commit
    to its text; `agents` holds the agent names in .claude/agents/, the roster; `scripts` maps each
    file in scripts/ to its source; `library` holds the persona slugs in personas/; `mcp` is the
    text of .mcp.json, None when there is none; `project` is true outside the template."""
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
    v.extend(team_violations(files, library or set(), agents, mcp, project))
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
        library = {Path(p).stem for p in would_commit(LIBRARY_DIR) if p.endswith(".md")}
        scripts = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / "scripts").glob("*.py")}
        brain = BRAIN.read_text(encoding="utf-8") if BRAIN.is_file() else ""
        mcp = (ROOT / MCP_CONFIG).read_text(encoding="utf-8") if would_commit(MCP_CONFIG) else None
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"skill_scan: cannot read the tree: {e}", file=sys.stderr)
        return 2
    count, found = scan(files, config_text, brain, agents, scripts, library, mcp, PROFILE.is_file())

    print("\nSkill Scan Results")
    print("=" * 60)
    print(f"Skills: {count}   Violations: {len(found)}")
    if found:
        print("\n" + "!" * 60)
        print("BLOCKED: a skill would load differently than written, or names what the suite lacks\n")
        for rule, detail in found:
            print(f"  Rule:    {rule}\n  Detail:  {detail}\n  Fix:     {FIXES[rule]}\n")
        return 1
    print("\nPASSED: every skill parses, names real hooks, stages, scripts and personas, and AGENTS.md lists it")
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

_PRESETS = """presets:
  Application development: [product-manager, backend-engineer]
  Imaging, video and 3D: [blender-artist, image-video-editor]
"""

_CONNECTIONS = """connections:
  blender-artist:
    blender:
      command: uvx
      args: [blender-mcp==1.4.0]
"""

_TEAM = f"""---
name: team-selection
description: Build the roster.
---

# Team selection

Offer a preset first; activate with `cp personas/<slug>.md .claude/agents/<slug>.md`.

```yaml
{_PRESETS}{_CONNECTIONS}```
"""

_LIBRARY = {"product-manager", "backend-engineer", "blender-artist", "image-video-editor"}
_MCP = '{"mcpServers": {"blender": {"command": "uvx", "args": ["blender-mcp==1.4.0"]}}}'


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
            extra: dict | None = None, agents: set | None = None, team: str | None = None,
            library: set = _LIBRARY, mcp: str | None = None, project: bool = False) -> list:
        files = {f"{SKILLS}closeout/SKILL.md": fork, f"{SKILLS}release/SKILL.md": inline, **(extra or {})}
        if team is not None:
            files[f"{SKILLS}{TEAM_SKILL}/SKILL.md"] = team
            brain += f"| `{SKILLS}{TEAM_SKILL}/SKILL.md` | team |\n"
        try:
            return scan(files, config, brain, agents if agents is not None else {"framework-maintainer"},
                        _SCRIPTS, library, mcp, project)[1]
        except Exception as e:  # a fixture that raises is a failure, never a crash of the self-test
            return [("raised", f"{type(e).__name__}: {e}")]

    def team(old: str = "", new: str = "", **kw) -> list:
        return run(team=_TEAM.replace(old, new) if old else _TEAM, **kw)

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
    # presets (decision 2026-10-23-012)
    expect("presets naming library personas and a pinned connection pass", team())
    block = team_block(_TEAM)[0] or {}
    check_("the block is read by a parser, a preset name holding a comma kept whole",
           block.get("presets", {}).get("Imaging, video and 3D") == ["blender-artist", "image-video-editor"], str(block))
    expect("a preset naming a persona the library lacks fails",
           team(library=_LIBRARY - {"backend-engineer"}), "preset")
    expect("a preset left on an old slug fails", team("backend-engineer]", "backend-engineers]"), "preset")
    expect("an empty preset fails", team("[product-manager, backend-engineer]", "[]"), "preset")
    expect("a preset member that is not a slug fails",
           team("[product-manager, backend-engineer]", "[product-manager, [backend-engineer]]"), "preset")
    expect("a persona named twice in one preset fails",
           team("[product-manager, backend-engineer]", "[product-manager, product-manager]"), "preset")
    expect("`presets:` that is not a mapping fails", team(_PRESETS, "presets: [product-manager]\n"), "preset")
    expect("a skill with no presets block fails, never read as no presets", team("```yaml", "```text"), "preset")
    expect("two presets blocks fail", team("```\n", "```\n\n```yaml\n" + _PRESETS + "```\n"), "preset")
    expect("a yaml block that does not parse fails", team("[blender-mcp==1.4.0]", "[blender-mcp==1.4.0"), "preset")
    expect("a second yaml block that does not parse fails, since it may be the presets",
           team("```\n", "```\n\n```yaml\npresets: [\n```\n"), "preset")
    expect("an unclosed yaml block is never read", team(_CONNECTIONS + "```\n", _CONNECTIONS), "preset")
    expect("a yaml block indented under a list item is read",
           team("```yaml\n" + _PRESETS + _CONNECTIONS + "```",
                "1. Offer:\n\n   ```yaml\n" + textwrap.indent(_PRESETS + _CONNECTIONS, "   ") + "   ```"))
    expect("a presets block in another skill is not judged",
           run(inline=_INLINE + "\n```yaml\npresets:\n  X: [ghost]\n```\n"))
    # connections
    expect("a connection keyed by no library persona fails",
           team("  blender-artist:\n    blender:", "  blender-artiste:\n    blender:"), "connection")
    expect("a connection that pins no version fails", team("[blender-mcp==1.4.0]", "[blender-mcp]"), "connection")
    expect("`@latest` is no pin", team("[blender-mcp==1.4.0]", "[blender-mcp@latest]"), "connection")
    expect("a range is no pin", team("[blender-mcp==1.4.0]", "['blender-mcp>=1.4.0']"), "connection")
    expect("the `name@version` pin is accepted", team("[blender-mcp==1.4.0]", "[blender-mcp@1.4.0]"))
    git = "git+https://example.org/lab/server.git"
    sha = "2cea8d566dde07fbac28a61d698909d69724e853"
    expect("a git source at a full commit is a pin",
           team("[blender-mcp==1.4.0]", f"[--from, '{git}@{sha}#subdirectory=mcp', blender-mcp]"))
    for rev in ("v1.0.3", "main", sha[:12]):
        expect(f"a git source at `{rev}` is no pin, since it can move or is not whole",
               team("[blender-mcp==1.4.0]", f"[--from, '{git}@{rev}#subdirectory=mcp', blender-mcp]"), "connection")
    expect("a project's git source at another commit fails",
           team("[blender-mcp==1.4.0]", f"[--from, '{git}@{sha}', blender-mcp]", project=True, agents={"blender-artist"},
                mcp=f'{{"mcpServers": {{"b3d": {{"command": "uvx", "args": ["--from", "{git}@{"0" * 40}", "blender-mcp"]}}}}}}'),
           "connection")
    expect("a server with no command fails", team("      command: uvx\n", ""), "connection")
    expect("args that are not a list fail", team("[blender-mcp==1.4.0]", "blender-mcp==1.4.0"), "connection")
    expect("`connections:` that is not a mapping fails", team(_CONNECTIONS, "connections: [blender]\n"), "connection")
    expect("a block with no connections passes", team(_CONNECTIONS, ""))
    # .mcp.json
    expect("the template holding the connection in .mcp.json fails, its persona active or not",
           team(mcp=_MCP, agents={"blender-artist"}), "connection")
    expect("the template's .mcp.json with another server passes",
           team(mcp='{"mcpServers": {"docs": {"command": "npx", "args": ["docs-mcp@2.0.0"]}}}'))
    expect("a project with the persona and the server as the skill gives it passes",
           team(mcp=_MCP, project=True, agents={"blender-artist"}))
    expect("a project whose roster lacks the persona fails", team(mcp=_MCP, project=True), "connection")
    expect("a project's server at another version fails",
           team(mcp=_MCP.replace("1.4.0", "1.5.0"), project=True, agents={"blender-artist"}), "connection")
    expect("a project's server with an env the skill does not give fails",
           team(mcp=_MCP.replace("]}", '], "env": {"X": "1"}}'), project=True, agents={"blender-artist"}), "connection")
    expect("the package run unpinned under another name fails",
           team(mcp='{"mcpServers": {"b3d": {"command": "uvx", "args": ["blender-mcp"]}}}', project=True,
                agents={"blender-artist"}), "connection")
    expect("the package found after `--from` is still the connection",
           team(mcp='{"mcpServers": {"b3d": {"command": "uvx", "args": ["--from", "blender-mcp==1.4.0", "x"]}}}'),
           "connection")
    expect("a .mcp.json that does not parse fails", team(mcp="{"), "connection")
    expect("a .mcp.json that is not an object fails", team(mcp="[]"), "connection")
    expect("a .mcp.json with no servers passes", team(mcp="{}"))

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Every skill parses, names real hooks and scripts, and is listed")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()
    return run_self_test() if args.self_test else check()


if __name__ == "__main__":
    sys.exit(main())
