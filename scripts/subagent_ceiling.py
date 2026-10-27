#!/usr/bin/env python3
"""
subagent_ceiling.py — no subagent runs above the session: every spawn and every skill call held to
the model and effort the operator set.

WHAT IT DOES
------------
One script, registered in .claude/settings.json on three events:
  SessionStart     keeps the session's `model`, when the event names it, in the session's scratchpad
  PostModelSwitch  keeps the switch's `to_model` there
  PreToolUse       on `Agent` and `Skill`: resolves the call's model and effort and judges them
A spawn's model is CLAUDE_CODE_SUBAGENT_MODEL when forced, then the spawn's `model`, the agent
file's `model:` (`inherit` is the session's), then CLAUDE_CODE_SUBAGENT_MODEL; a spawn of an agent
type with no file and no `model` is refused, since a built-in's default cannot be known. Its effort
is CLAUDE_CODE_EFFORT_LEVEL, the spawn's `effort`, the agent file's `effort:`, then the session's.
A skill's are its frontmatter's `model:` and `effort:`, the session's where it names none. The
session's effort is the event's `effort.level`; its model is the kept one, else the newest
`api-request` record in the transcript, observed and undocumented.

A call keeping the session's model family and effort passes in every mode. Otherwise
SUBAGENT_CHOICE decides: `max` changes nothing, `tuned` the effort only, `efficient` both, never
above the session's, models ranked haiku < sonnet < opus < fable and efforts low < medium < high
< xhigh < max. An unknown mode, an unplaced model or an unknown effort is refused.

Exit 0 allows; exit 2 refuses, its stderr the reason the model reads. The PreToolUse registration
declares `onFailure: block`, so a crash or a timeout refuses as well.
--self-test   in-memory fixtures for every rule; this script held to the coding standard's limits

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It cannot see a plugin's agent or skill, which lives outside .claude/: a plugin spawn must name its
model, and a plugin skill is not judged. It rewrites no call: a refused spawn is spawned again
within the ceiling. It reads frontmatter as `key: value` lines, for the
two scalar keys it needs, since the hook runs under any python3; a frontmatter it cannot read names
nothing, as Claude Code then loads it with no fields.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Callable, Mapping

MODELS = ("haiku", "sonnet", "opus", "fable")               # lowest first
EFFORTS = ("low", "medium", "high", "xhigh", "max")          # Claude Code's levels, lowest first
MODES = {"max": (False, False), "tuned": (False, True), "efficient": (True, True)}   # (model, effort) may change
CHOICE = "SUBAGENT_CHOICE"
STATE = "subagent-ceiling.json"
SESSION = "the session's"                                    # a call that inherits the session's value
FAMILY = re.compile(rf"(?<![a-z])({'|'.join(MODELS)})(?![a-z])")

Reader = Callable[[Path], "str | None"]


# ==============================================================================
# Reading: model families, frontmatter, definitions, the session's model
# ==============================================================================

def family(model: str | None) -> str | None:
    """`claude-opus-5-5`, `opus` and `claude-opus-5-5[1m]` are all `opus`; anything else is unplaced."""
    found = set(FAMILY.findall((model or "").lower()))
    return found.pop() if len(found) == 1 else None


def frontmatter(text: str | None) -> dict[str, str]:
    """The top-level `key: value` scalars between a file's opening `---` fences; nothing if none."""
    lines = (text or "").splitlines()
    end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if not lines or lines[0].strip() != "---" or end is None:
        return {}
    out = {}
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if m and m.group(2):
            out[m.group(1)] = m.group(2).strip("'\"")
    return out


def definition(tool: str, name: str, roots: list[Path], read: Reader) -> dict[str, str] | None:
    """An agent's or a skill's frontmatter from the project's or the user's .claude/, or None if neither holds it."""
    if not re.fullmatch(r"[\w.-]+", name or ""):
        return None                                # a plugin's (`plugin:name`) or no name at all
    rel = Path(".claude", "agents", f"{name}.md") if tool == "Agent" else Path(".claude", "skills", name, "SKILL.md")
    for root in roots:
        text = read(root / rel)
        if text is not None:
            return frontmatter(text)
    return None


def transcript_model(text: str | None) -> str | None:
    """The newest `api-request` record's `params.model` in a transcript."""
    newest = None
    for line in (text or "").splitlines():
        if '"api-request"' not in line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("type") == "api-request":
            newest = (record.get("params") or {}).get("model") or newest
    return newest


def session_model(event: Mapping, read: Reader) -> str | None:
    """The kept model (SessionStart, PostModelSwitch), else the transcript's newest request, else None."""
    if event.get("scratchpad_dir"):
        try:
            kept = json.loads(read(Path(event["scratchpad_dir"], STATE)) or "{}").get("model")
        except (json.JSONDecodeError, AttributeError):
            kept = None
        if kept:
            return kept
    return transcript_model(read(Path(event["transcript_path"]))) if event.get("transcript_path") else None


# ==============================================================================
# Resolving a call and judging it
# ==============================================================================

def resolve_spawn(tool_input: Mapping, agent: dict[str, str] | None, env: Mapping) -> tuple[str | None, str]:
    """(model, effort) of an Agent call, SESSION where it inherits; model None where it cannot be known."""
    forced = env.get("CLAUDE_CODE_SUBAGENT_MODEL") if env.get("CLAUDE_CODE_SUBAGENT_MODEL_FORCE") else None
    file_model = (agent or {}).get("model")
    if forced or tool_input.get("model"):
        model: str | None = forced or tool_input["model"]
    elif file_model:
        model = SESSION if file_model == "inherit" else file_model
    elif agent is not None:
        model = env.get("CLAUDE_CODE_SUBAGENT_MODEL") or SESSION
    else:
        model = None
    effort = env.get("CLAUDE_CODE_EFFORT_LEVEL") or tool_input.get("effort") or (agent or {}).get("effort") or SESSION
    return model, effort


def resolve_skill(skill: dict[str, str] | None) -> tuple[str, str]:
    skill = skill or {}
    return (SESSION if skill.get("model") in (None, "inherit") else skill["model"]), skill.get("effort") or SESSION


def changes(model: str, effort: str, session: tuple[str | None, str | None]) -> tuple[bool, bool]:
    """Whether the call's model family and effort differ from the session's."""
    same_model = model == SESSION or (family(model) is not None and family(model) == family(session[0]))
    return not same_model, not (effort == SESSION or effort == session[1])


def over(value: str, ceiling: str | None, order: tuple[str, ...], what: str) -> str | None:
    if ceiling not in order:
        return f"the session's {what} is not known here ({ceiling}); run `/model` once to name it"
    return f"{what} {value} is above the session's {ceiling}" if order.index(value) > order.index(ceiling) else None


def judge(model: str, effort: str, session: tuple[str | None, str | None], mode: str | None) -> str | None:
    """None if the call may run; else the reason it may not."""
    new_model, new_effort = changes(model, effort, session)
    if not (new_model or new_effort):
        return None
    if new_model and family(model) is None:
        return f"model {model!r} is not one the ranking places ({', '.join(MODELS)})"
    if new_effort and effort not in EFFORTS:
        return f"effort {effort!r} is not a level ({', '.join(EFFORTS)})"
    if mode not in MODES:
        return f"{CHOICE} is {repr(mode) if mode else 'not set'}, and it must be one of {', '.join(MODES)}"
    may_model, may_effort = MODES[mode]
    if new_model:
        if not may_model:
            return f"{mode} keeps the session's model; this call asks for {model}"
        reason = over(family(model) or "", family(session[0]), MODELS, "model")
        if reason:
            return reason
    if new_effort:
        return over(effort, session[1], EFFORTS, "effort") if may_effort else \
            f"{mode} keeps the session's effort; this call asks for {effort}"
    return None


def decide(event: Mapping, env: Mapping, read: Reader, home: Path) -> tuple[int, str]:
    """A PreToolUse event -> (exit code, reason): 0 to allow, 2 to refuse."""
    tool, tool_input = event.get("tool_name"), event.get("tool_input") or {}
    if tool not in ("Agent", "Skill"):
        return 0, ""
    roots = [Path(env.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or "."), home]
    name = tool_input.get("subagent_type", "general-purpose") if tool == "Agent" else tool_input.get("skill", "")
    found = definition(tool, name, roots, read)
    model, effort = resolve_spawn(tool_input, found, env) if tool == "Agent" else resolve_skill(found)
    if model is None:
        return 2, (f"Subagent ceiling: agent type {name!r} has no agent file here, so its default model "
                   f"cannot be known; name the model in the call (`model`), at or below the session's.")
    session = (session_model(event, read), (event.get("effort") or {}).get("level"))
    mode = env.get(CHOICE)
    reason = judge(model, effort, session, mode)
    if reason is None:
        return 0, ""
    return 2, (f"Subagent ceiling ({mode or 'no mode set'}): {reason}. The session runs {session[0] or 'an unknown model'} at "
               f"{session[1]}; call again within it, or the operator changes {CHOICE} or the session.")


def kept(event: Mapping) -> tuple[Path, str] | None:
    """What SessionStart or PostModelSwitch keeps: (the state file, its text), or None."""
    model = event.get("model") if event.get("hook_event_name") == "SessionStart" else event.get("to_model")
    if not (model and event.get("scratchpad_dir")):
        return None
    return Path(event["scratchpad_dir"], STATE), json.dumps({"model": model})


# ==============================================================================
# The hook
# ==============================================================================

def read_file(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    event = json.loads(sys.stdin.read() or "{}")
    if event.get("hook_event_name") in ("SessionStart", "PostModelSwitch"):
        keep = kept(event)
        if keep:
            tmp = keep[0].with_suffix(".tmp")
            tmp.write_text(keep[1], encoding="utf-8")
            os.replace(tmp, keep[0])
        return 0
    code, reason = decide(event, os.environ, read_file, Path.home())
    if reason:
        print(reason, file=sys.stderr)
    return code


# ==============================================================================
# SELF-TEST — every rule against a passing and a failing fixture, in memory
# ==============================================================================

AGENT_FILE = "---\nname: cheap\ndescription: x\nmodel: haiku\neffort: low\n---\n\nBody.\n"
SKILL_FILE = "---\nname: big\ndescription: 'x'\ncontext: fork\nmodel: fable\n---\n\nBody.\n"
REQUEST = '{"type": "api-request", "params": {"model": "%s"}}'


def _files(extra: dict[str, str] | None = None) -> Reader:
    files = {"/p/.claude/agents/cheap.md": AGENT_FILE, "/p/.claude/skills/big/SKILL.md": SKILL_FILE,
             "/p/.claude/skills/plain/SKILL.md": "---\nname: plain\n---\n", "/t.jsonl": REQUEST % "claude-sonnet-5-5",
             **(extra or {})}
    return lambda path: files.get(str(path))


def _event(tool: str = "Agent", level: str = "high", **tool_input: str) -> dict:
    """A PreToolUse event in a session at effort `level`, its model sonnet by the transcript."""
    return {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input, "effort": {"level": level},
            "transcript_path": "/t.jsonl", "scratchpad_dir": "/s", "cwd": "/p"}


def _run(event: dict, mode: str | None = "efficient", files: Reader | None = None, **env: str) -> int:
    return decide(event, {**({CHOICE: mode} if mode else {}), **env}, files or _files(), Path("/home"))[0]


def _t_reading(check) -> None:
    check("a full ID, an alias and a suffixed ID each name their family",
          [family(m) for m in ("claude-opus-5-5", "sonnet", "claude-haiku-5-5[1m]", "us.anthropic.claude-fable-5-1")]
          == ["opus", "sonnet", "haiku", "fable"])
    check("an unknown or an ambiguous name is unplaced", [family(m) for m in ("gpt-5", "opusplan", "", None)] == [None] * 4)
    fm = frontmatter(AGENT_FILE + "  model: fable\n")
    check("the frontmatter's top-level scalars are read", fm.get("model") == "haiku" and fm.get("effort") == "low", str(fm))
    check("an indented line is no top-level key", frontmatter("---\ndescription: |\n  model: opus\n---\n").get("model") is None)
    check("a file with no frontmatter names nothing", frontmatter("model: opus\n") == {})
    check("a plugin's agent is outside .claude/ and found nowhere", definition("Agent", "kit:cheap", [Path("/p")], _files()) is None)
    state = _files({"/s/" + STATE: '{"model": "claude-opus-5-5"}'})
    check("the kept model comes first", session_model(_event(), state) == "claude-opus-5-5")
    check("with nothing kept, the transcript's newest request names it",
          session_model(_event(), _files({"/t.jsonl": f"{REQUEST % 'opus'}\nnot json\n{REQUEST % 'haiku'}\n"})) == "haiku")
    check("with neither, the session's model is unknown", session_model(_event(), _files({"/t.jsonl": "{}"})) is None)


def _t_resolve(check) -> None:
    agent = frontmatter(AGENT_FILE)
    check("the spawn's model outranks the agent file's", resolve_spawn({"model": "opus"}, agent, {}) == ("opus", "low"))
    check("the agent file's model and effort apply where the spawn names none", resolve_spawn({}, agent, {}) == ("haiku", "low"))
    check("`model: inherit` is the session's", resolve_spawn({}, {"model": "inherit"}, {})[0] == SESSION)
    check("a forced CLAUDE_CODE_SUBAGENT_MODEL outranks the spawn's",
          resolve_spawn({"model": "haiku"}, None, {"CLAUDE_CODE_SUBAGENT_MODEL": "fable",
                                                   "CLAUDE_CODE_SUBAGENT_MODEL_FORCE": "1"})[0] == "fable")
    check("CLAUDE_CODE_EFFORT_LEVEL outranks the spawn's effort",
          resolve_spawn({"effort": "low"}, agent, {"CLAUDE_CODE_EFFORT_LEVEL": "max"})[1] == "max")
    check("an agent with no file and no model cannot be resolved", resolve_spawn({}, None, {})[0] is None)
    check("a skill naming neither key inherits both", resolve_skill(frontmatter("---\nname: x\n---\n")) == (SESSION, SESSION))


def _t_modes(check) -> None:
    check("a spawn below the session passes in efficient", _run(_event(model="haiku", effort="low")) == 0)
    check("a spawn above the session's model is refused", _run(_event(model="fable")) == 2)
    check("a spawn above the session's effort is refused", _run(_event(level="medium", model="sonnet", effort="max")) == 2)
    check("tuned refuses a model change, even downward", _run(_event(model="haiku"), mode="tuned") == 2)
    check("tuned allows a lower effort on the session's model",
          _run(_event(model="claude-sonnet-5-5", effort="low"), mode="tuned") == 0)
    check("max refuses an effort change, even downward", _run(_event(model="sonnet", effort="low"), mode="max") == 2)
    check("max allows the session's model and effort", _run(_event(model="sonnet", effort="high"), mode="max") == 0)
    check("a call keeping the session's model and effort passes even with no mode set", _run(_event(model="sonnet"), mode=None) == 0)
    check("an unknown mode refuses a change", _run(_event(model="haiku"), mode="cheap") == 2)
    code, reason = decide(_event(model="haiku"), {}, _files(), Path("/home"))
    check("no mode set refuses a change, saying it is not set", code == 2 and "not set" in reason, reason)
    check("an unplaced model is refused", _run(_event(model="gpt-5")) == 2)
    check("an unknown effort is refused", _run(_event(model="haiku", effort="extreme")) == 2)
    check("a model change with the session's model unknown is refused",
          _run(_event(model="haiku"), files=_files({"/t.jsonl": "{}"})) == 2)


def _t_calls(check) -> None:
    check("a built-in agent type with no model named is refused", _run(_event(subagent_type="general-purpose")) == 2)
    check("a roster agent below the ceiling passes on its file alone", _run(_event(subagent_type="cheap")) == 0)
    check("a skill whose frontmatter names a model above the session is refused", _run(_event("Skill", skill="big")) == 2)
    check("a skill naming neither key passes, even with no mode set", _run(_event("Skill", skill="plain"), mode=None) == 0)
    check("a plugin's skill is not judged", _run(_event("Skill", skill="kit:big")) == 0)
    check("another tool is never judged", _run(_event("Bash", command="ls")) == 0)
    code, reason = decide(_event(model="fable"), {CHOICE: "efficient"}, _files(), Path("/home"))
    check("a refusal names the mode, the ceiling and the session", code == 2 and "efficient" in reason
          and "claude-sonnet-5-5" in reason and "high" in reason, reason)
    start = {"hook_event_name": "SessionStart", "model": "claude-opus-5-5", "scratchpad_dir": "/s"}
    check("SessionStart's model is kept", kept(start) == (Path("/s", STATE), '{"model": "claude-opus-5-5"}'))
    check("a switch's to_model is kept", (kept({"hook_event_name": "PostModelSwitch", "to_model": "haiku",
                                                "scratchpad_dir": "/s"}) or ("", ""))[1] == '{"model": "haiku"}')
    check("a SessionStart naming no model keeps nothing", kept({"hook_event_name": "SessionStart", "scratchpad_dir": "/s"}) is None)


def _t_own_limits(check) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import code_standard
    own = code_standard.measure_python(Path(__file__).read_text(encoding="utf-8"))
    over_ = [f"{f.name} ({f.complexity}c/{f.code_lines}l/{f.parameters}p)" for f in own
             if code_standard.judge_function("", f, "production")]
    check("this script's functions meet the coding standard's production limits", not over_, ", ".join(over_))


def run_self_test() -> int:
    print("\nSubagent Ceiling Self-Test")
    print("=" * 60)
    state = {"failures": 0, "total": 0}

    def check(label: str, ok: bool, detail: str = "") -> None:
        state["total"] += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok:
            state["failures"] += 1
            if detail:
                print(f"        {detail}")

    for group in (_t_reading, _t_resolve, _t_modes, _t_calls, _t_own_limits):
        try:
            group(check)
        except Exception as e:   # a crash is a failed fixture, never a crashed self-test
            check(f"{group.__name__} ran without raising", False, f"{type(e).__name__}: {e}")
    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 0 if not state["failures"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
