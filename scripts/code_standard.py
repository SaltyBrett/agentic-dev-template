#!/usr/bin/env python3
"""
code_standard.py — the coding standard's gate: the code a change adds or edits, measured against
docs/standards/coding_standard_v1.0.md, every finding written to the code review audit log.

THE FAILURE THIS CLOSES
-----------------------
Agents write verbose, run-on, repetitive code when nothing stops them, and a standard that is prose
stops nothing (decision 2026-10-22-003). The limits were calibrated on industry code that must pass
and the refactoring katas that must fail (decision 2026-10-24-007); the first measuring tool tried
silently skipped whole files of Rust and TypeScript, so a gate built on it would have reported
green over code it never read (decision 2026-10-24-008, [[reference_coding_standard_calibration]]).

The standard advises and documents; it never forces a code change (decision 2026-10-24-011). A
finding pauses the commit only until the audit log, `docs/code_review_log.md`, holds a row for it
with the Chair's response, "acknowledged, proceed" being enough. An acknowledged finding pauses
nothing again unless it gets worse.

WHAT IT DOES
------------
A project opts in with `code-profile.yaml` at its root; with none the gate says so and passes.

    profile: python                      # a stack profile this script holds (TMPL-4.3: python)
    code: ["pipeline/**/*.py"]           # production code
    tests: ["tests/**/*.py"]             # test code; only its `test*` functions are test functions
    generated: []                        # generated paths, never measured
    coverage_command: "python -m coverage run -m pytest && python -m coverage json -o coverage.json"
    coverage_report: coverage.json       # coverage.py's JSON report, written by the command
    manifests: [requirements.txt]        # dependency manifests the audit reads; [] when none
    license_command: "pip-licenses --format=json"   # in the project's environment; with manifests
    licenses_allowed: [MIT License, BSD License, Apache Software License]

On the change (the staged change by default; `--range A..B`, or CODE_STANDARD_RANGE through
`--range-from-env`, in CI), for every code file it touches, findings keyed by where they are:
  recall       the measurer finds as many functions as the file defines (`def` tokens), or nothing
               it reports for the file can be trusted
  complexity   a changed function's cyclomatic complexity over 15 (a test function's over 10)
  code_lines   its code lines, blanks, comments and its docstring excluded, over 60 (100)
  parameters   its parameters, a declared `self` included, over 5
  suppression  a limit-suppressing comment on a changed line (`noqa: C901`, `pragma: no cover`,
               `jscpd:ignore-start`, `lizard forgives`)
  generated-marker  a generated-code marker outside a declared generated path
  clone        a copy of existing code among the change's added lines (jscpd 4.0.5, 50 tokens and 5
               lines, its size caps lifted)
  coverage     a changed function's new executable lines under 80% covered, by the project's tests
  format, lint, types  ruff format, ruff check and mypy --strict, on changed lines only
  audit, license  pip-audit on each manifest and the license policy, when a manifest changes and
               always over a range
  unmeasured   a tool that could not run, so its check was not made
Each finding is logged when a row of the audit log names its place and rule, a value at least the
finding's, and a response from the Chair. The log is append-only: a row the base held, edited or
removed, is the one thing no response clears. It reports, and never pauses on, a production file
grown past 500 lines and the review-trigger paths the change touches (decision 2026-10-24-005).

A function is changed when an added or edited line falls among its own lines, its nested functions'
lines being theirs. Complexity counts each `if`, `elif`, `for`, `while`, `except`, `finally`,
`and`, `or`, conditional expression, comprehension `for` and `if`, and `case`, plus one: the points
the calibration's measurer counted, with Python's `match` added, which it missed.

--self-test   in-memory fixtures for every rule, and this script's own functions held to the limits
Exit 0 every finding logged or not adopted, 1 a finding not yet logged or the log edited, 2 git failing.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It judges no code a change leaves alone, and makes no judgement: names, cohesion and near-copies the
clone detector cannot see are the code reviewer's, logged in the same table (decision
2026-10-24-009). It holds the Python profile only; Rust and TypeScript are TMPL-4.4 and TMPL-4.5.
"""
from __future__ import annotations

import ast
import contextlib
import datetime
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import session_closeout  # noqa: E402  — its glob translation is the rule gate's, one reading of `**`


def repo_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False)
    return Path(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip() else Path.cwd()


ROOT = repo_root()
PROFILE_FILE = "code-profile.yaml"
LOG_FILE = "docs/code_review_log.md"
STANDARD = "docs/standards/coding_standard_v1.0.md"
LOG_COLUMNS = ["Date", "Change", "Where", "Finding", "Source", "Change made", "Chair's response"]
NO_RESPONSE = {"", "-", "—", "pending", "tbd"}

# The core limits (decision 2026-10-24-007). The self-test holds them equal to the standard's §2.
LIMITS = {"production": {"complexity": 15, "code_lines": 60, "parameters": 5},
          "test": {"complexity": 10, "code_lines": 100, "parameters": 5}}
COVERAGE_FLOOR = 0.80
FILE_SIGNAL = 500
JSCPD = ["npx", "--yes", "jscpd@4.0.5"]

# What a line can carry to switch a check off.
SUPPRESSIONS = [re.compile(r"#\s*noqa\b.*\b(C901|PLR091[2-5])\b"), re.compile(r"#\s*pragma:\s*no\s*cover"),
                re.compile(r"jscpd:ignore-start"), re.compile(r"#\s*lizard\s+forgives")]
GENERATED_MARKER = re.compile(r"@generated\b|GENERATED CODE")

# The paths that show decision 2026-10-24-005's triggers in a Python project.
TRIGGER_PATHS = {
    "a new dependency": ["requirements*.txt", "**/requirements*.txt", "pyproject.toml", "setup.py", "setup.cfg",
                         "Pipfile", "Pipfile.lock", "poetry.lock", "uv.lock"],
    "a schema change": ["**/migrations/**", "**/*.sql", "**/schema*"],
    "an auth or crypto change": ["**/*auth*", "**/*crypt*", "**/*secret*", "**/*token*"],
    "a cost": ["**/*.tf", "**/*.bicep", "infra/**", "**/Dockerfile*"],
    "a gate or CI change": [".github/**", ".pre-commit-config.yaml", "scripts/**"],
    "a license change": ["LICENSE*", "COPYING*"],
}

ADVICE = {
    "profile": "Write `code-profile.yaml` as this script's docstring shows; a profile names every slot.",
    "recall": "The measurer could not read every function in the file; nothing it reported for the file holds.",
    "complexity": "Split the function by responsibility.",
    "code_lines": "Split the function by responsibility.",
    "parameters": "Group the parameters into a value the function takes whole.",
    "suppression": "A suppressed check is a finding of its own; say why in the log.",
    "generated-marker": "Declare the path under `generated:` in `code-profile.yaml`, or remove the marker.",
    "clone": "Extract the shared code into one function both call.",
    "coverage": "Test the new lines.",
    "format": "Run `ruff format` on the file.",
    "lint": "Fix what ruff reports on the changed lines.",
    "types": "Type the changed lines so mypy --strict accepts them.",
    "audit": "Upgrade or replace the vulnerable dependency.",
    "license": "Replace the dependency, or add its license to `licenses_allowed` by a decision.",
    "unmeasured": "Install the tool, or let CI make the check.",
}


class GateError(Exception):
    """The gate cannot read the change at all: git failing. Exit 2."""


@dataclass(frozen=True)
class Finding:
    rule: str
    where: str
    value: int
    detail: str


@dataclass(frozen=True)
class Function:
    name: str
    start: int
    end: int
    complexity: int
    code_lines: int
    parameters: int
    own_lines: frozenset[int]


@dataclass(frozen=True)
class LogRow:
    cells: tuple[str, ...]

    @property
    def where(self) -> str:
        return self.cells[2].strip("` ")

    @property
    def rule_value(self) -> tuple[str, int]:
        m = re.match(r"`?([a-z_-]+)`?\s+(\d+)", self.cells[3])
        return (m.group(1), int(m.group(2))) if m else ("", 0)

    @property
    def answered(self) -> bool:
        return self.cells[6].strip().lower() not in NO_RESPONSE


@dataclass
class Change:
    """What a change touches: the lines added or edited per file, and each file before and after."""
    touched: dict[str, set[int]]
    read_new: Callable[[str], str | None]
    read_old: Callable[[str], str | None]
    files: list[str] = field(default_factory=list)
    is_range: bool = False


# ==============================================================================
# The Python profile's measurer, on Python's own parser
# ==============================================================================

NESTED = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
DECISIONS = (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.match_case)


def _weight(node: ast.AST) -> int:
    if isinstance(node, DECISIONS):
        return 1
    if isinstance(node, ast.BoolOp):
        return len(node.values) - 1
    if isinstance(node, ast.comprehension):
        return 1 + len(node.ifs)
    if isinstance(node, ast.Try) and node.finalbody:
        return 1
    return 0


def _decisions(node: ast.AST) -> int:
    """Decision points in a function's own code, its nested functions and classes excluded."""
    total = 0
    for child in ast.iter_child_nodes(node):
        if not isinstance(child, NESTED):
            total += _weight(child) + _decisions(child)
    return total


def code_line_map(text: str) -> set[int]:
    """Lines holding a code token; blanks and comments are not code, and a docstring is removed later."""
    lines: set[int] = set()
    skip = {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
            tokenize.ENCODING, tokenize.ENDMARKER}
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type not in skip:
            lines.update(range(tok.start[0], tok.end[0] + 1))
    return lines


def def_count(text: str) -> int:
    """`def` keywords, read by the tokenizer, never the parser: the recall check's independent count."""
    return sum(1 for t in tokenize.generate_tokens(io.StringIO(text).readline)
               if t.type == tokenize.NAME and t.string == "def")


def _docstring_lines(node: ast.AST) -> set[int]:
    body = getattr(node, "body", [])
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        return set(range(body[0].lineno, (body[0].end_lineno or body[0].lineno) + 1))
    return set()


def _own_lines(node: ast.AST) -> frozenset[int]:
    lines = set(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    for child in ast.walk(node):
        if child is not node and isinstance(child, NESTED):
            lines -= set(range(child.lineno, (child.end_lineno or child.lineno) + 1))
    return frozenset(lines)


def _parameters(args: ast.arguments) -> int:
    return len(args.posonlyargs) + len(args.args) + len(args.kwonlyargs) + bool(args.vararg) + bool(args.kwarg)


def measure_python(text: str) -> list[Function]:
    """Every function and method in the file, its metrics taken from its own lines."""
    tree = ast.parse(text)
    code = code_line_map(text)
    found: list[Function] = []

    def visit(node: ast.AST, prefix: str) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                own = _own_lines(child)
                lines = (own & code) - _docstring_lines(child)
                found.append(Function(prefix + child.name, child.lineno, child.end_lineno or child.lineno,
                                      1 + _decisions(child), len(lines), _parameters(child.args), own))
                visit(child, f"{prefix}{child.name}.")
            elif isinstance(child, ast.ClassDef):
                visit(child, f"{prefix}{child.name}.")
            else:
                visit(child, prefix)

    visit(tree, "")
    return found


# ==============================================================================
# The change, from git
# ==============================================================================

HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def parse_diff(text: str) -> dict[str, set[int]]:
    """{path: lines added or edited} from `git diff -U0`; a pure deletion touches the lines around it."""
    touched: dict[str, set[int]] = {}
    path: str | None = None
    for line in text.splitlines():
        if line.startswith("+++ "):
            path = None if line[4:] == "/dev/null" else line[4:].removeprefix("b/")
            if path is not None:
                touched.setdefault(path, set())
            continue
        m = HUNK.match(line)
        if m and path is not None:
            start, count = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
            touched[path].update(range(start, start + count) if count else (start, start + 1))
    return touched


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise GateError(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def _show(spec: str) -> str | None:
    out = subprocess.run(["git", "show", spec], cwd=ROOT, capture_output=True, text=True, check=False)
    return out.stdout if out.returncode == 0 else None


def staged_change() -> Change:
    diff = git("diff", "--cached", "-U0", "--no-color", "--no-ext-diff", "--find-renames")
    has_head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=ROOT, capture_output=True).returncode == 0
    files = git("ls-files").splitlines()
    return Change(parse_diff(diff), lambda p: _show(f":{p}"),
                  (lambda p: _show(f"HEAD:{p}")) if has_head else (lambda p: None), files)


def range_change(spec: str) -> Change:
    if ".." not in spec:
        raise GateError(f"a range is BASE..HEAD, not {spec!r}")
    base, head = spec.split("..", 1)
    diff = git("diff", "-U0", "--no-color", "--no-ext-diff", "--find-renames", base, head)
    files = git("ls-tree", "-r", "--name-only", head).splitlines()
    return Change(parse_diff(diff), lambda p: _show(f"{head}:{p}"), lambda p: _show(f"{base}:{p}"), files, True)


# ==============================================================================
# The profile and the audit log
# ==============================================================================

REQUIRED = {"profile": str, "code": list, "tests": list, "coverage_command": str, "coverage_report": str,
            "manifests": list}


def load_profile(text: str) -> tuple[dict, list[Finding]]:
    import yaml
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return {}, [Finding("profile", PROFILE_FILE, 1, f"does not parse as YAML: {e}")]
    if not isinstance(data, dict):
        return {}, [Finding("profile", PROFILE_FILE, 1, "is not a mapping")]
    problems = [f"`{k}` must be a {t.__name__}" for k, t in REQUIRED.items() if not isinstance(data.get(k), t)]
    if data.get("profile") not in (None, "python"):
        problems.append(f"profile {data.get('profile')!r} is not built here; this gate holds `python`")
    if isinstance(data.get("code"), list) and not data["code"]:
        problems.append("`code` names no path: a profile with an empty slot is not adoptable")
    if data.get("manifests") and not (isinstance(data.get("license_command"), str)
                                       and isinstance(data.get("licenses_allowed"), list)):
        problems.append("manifests need `license_command` and `licenses_allowed`")
    return data, [Finding("profile", PROFILE_FILE, 1, "; ".join(problems))] if problems else []


def parse_log(text: str | None) -> tuple[list[LogRow], str | None]:
    """The audit log's rows, or why it cannot be read: a log that does not parse acknowledges nothing."""
    if text is None:
        return [], None
    lines = [l for l in text.splitlines() if l.startswith("|")]
    if not lines:
        return [], f"{LOG_FILE} holds no table"
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    if header != LOG_COLUMNS:
        return [], f"{LOG_FILE}'s columns must be: {' | '.join(LOG_COLUMNS)}"
    rows = [tuple(c.strip() for c in l.strip("|").split("|")) for l in lines[2:]]
    bad = [n for n, r in enumerate(rows, 1) if len(r) != len(LOG_COLUMNS)]
    if bad:
        return [], f"{LOG_FILE} row {bad[0]} does not have {len(LOG_COLUMNS)} cells"
    return [LogRow(r) for r in rows], None


def log_edited(new: list[LogRow], old: list[LogRow]) -> list[str]:
    """An append-only log keeps every row the base held, unchanged and in order."""
    return [f"row {n} of the base was edited or removed" for n, r in enumerate(old, 1)
            if n > len(new) or new[n - 1] != r][:3]


def logged(finding: Finding, rows: list[LogRow]) -> bool:
    return any(r.answered and r.where == finding.where and r.rule_value[0] == finding.rule
               and r.rule_value[1] >= finding.value for r in rows)


# ==============================================================================
# Measuring a file's changed functions
# ==============================================================================

def matches(path: str, globs: list[str]) -> bool:
    return any(session_closeout.glob_regex(g).fullmatch(path) for g in globs)


def is_test(path: str, fn: Function, profile: dict) -> bool:
    return matches(path, profile.get("tests", [])) and fn.name.rsplit(".", 1)[-1].startswith("test")


def judge_function(path: str, fn: Function, kind: str) -> list[Finding]:
    values = {"complexity": fn.complexity, "code_lines": fn.code_lines, "parameters": fn.parameters}
    return [Finding(metric, f"{path}:{fn.name}", value, f"{metric.replace('_', ' ')} {value} over the {kind} "
                                                       f"limit {LIMITS[kind][metric]}")
            for metric, value in values.items() if value > LIMITS[kind][metric]]


def function_at(functions: list[Function], line: int) -> str:
    inner = [f for f in functions if line in f.own_lines]
    return inner[0].name if inner else "<module>"


def tally(rule: str, hits: list[tuple[str, str]]) -> list[Finding]:
    """One finding per place, its value the count of hits there: [(where, what)] -> findings."""
    by_place: dict[str, list[str]] = {}
    for where, what in hits:
        by_place.setdefault(where, []).append(what)
    return [Finding(rule, where, len(whats), "; ".join(whats[:4])) for where, whats in by_place.items()]


def judge_markers(path: str, text: str, lines: set[int], functions: list[Function], generated: bool) -> list[Finding]:
    """Suppression comments and generated-code markers on the changed lines."""
    rows = text.splitlines()
    sup, gen = [], []
    for n in sorted(lines):
        row = rows[n - 1] if 0 < n <= len(rows) else ""
        place = f"{path}:{function_at(functions, n)}"
        sup += [(place, f"line {n}: `{p.pattern}`") for p in SUPPRESSIONS if p.search(row)]
        if GENERATED_MARKER.search(row) and not generated:
            gen.append((place, f"line {n}: a generated-code marker outside a generated path"))
    return tally("suppression", sup) + tally("generated-marker", gen)


def judge_file(path: str, text: str, lines: set[int], profile: dict) -> tuple[list[Finding], list[Function]]:
    """Recall first: a file the measurer under-reads proves nothing about its functions."""
    try:
        functions = measure_python(text)
    except SyntaxError as e:
        return [Finding("recall", path, 1, f"Python cannot parse it: {e.msg} at line {e.lineno}")], []
    if len(functions) != def_count(text):
        return [Finding("recall", path, 1, f"measured {len(functions)} functions of {def_count(text)} defined")], functions
    found: list[Finding] = []
    for fn in functions:
        if fn.own_lines & lines:
            found += judge_function(path, fn, "test" if is_test(path, fn, profile) else "production")
    return found + judge_markers(path, text, lines, functions, matches(path, profile.get("generated", []))), functions


def signals(change: Change, prod: list[str]) -> list[str]:
    out = []
    for path in prod:
        new, old = len((change.read_new(path) or "").splitlines()), len((change.read_old(path) or "").splitlines())
        if new > FILE_SIGNAL and new > old:
            out.append(f"file length: {path} grew to {new} lines, past {FILE_SIGNAL}; for the reviewer")
    for trigger, globs in TRIGGER_PATHS.items():
        hit = sorted(p for p in change.touched if matches(p, globs))
        if hit:
            out.append(f"trigger: {trigger}: {', '.join(hit[:5])}")
    return out


# ==============================================================================
# The tools: clones, coverage, format, lint, types, audit
# ==============================================================================

Runner = Callable[[list[str], str | None], tuple[int, str]]


class Unmeasured(Exception):
    """A tool could not run, so its check was not made: a finding the Chair can acknowledge."""


def run_tool(argv: list[str], shell: str | None = None) -> tuple[int, str]:
    """One tool, run from the root; `shell` runs a project's own command line instead."""
    if shell is None and argv and argv[0] != sys.executable and shutil.which(argv[0]) is None:
        raise Unmeasured(f"{argv[0]} is not installed")
    out = subprocess.run(shell if shell is not None else argv, cwd=ROOT, capture_output=True, text=True,
                         check=False, shell=shell is not None)
    return out.returncode, out.stdout + out.stderr


def _rel(name: str) -> str:
    return os.path.relpath(name, ROOT) if os.path.isabs(name) else name


def judge_clones(report: dict, touched: dict[str, set[int]], prod: set[str],
                 measured: dict[str, list[Function]]) -> list[Finding]:
    found = []
    for dup in report.get("duplicates", []):
        for side, other in (("firstFile", "secondFile"), ("secondFile", "firstFile")):
            here, there = dup.get(side, {}), dup.get(other, {})
            path, span = _rel(here.get("name", "")), set(range(int(here.get("start", 0)), int(here.get("end", 0)) + 1))
            if path in prod and span & touched.get(path, set()):
                place = f"{path}:{function_at(measured.get(path, []), int(here.get('start', 0)))}"
                found.append(Finding("clone", place, int(dup.get("lines", 0)),
                                     f"{dup.get('lines')} lines copied from {_rel(there.get('name', ''))}:{there.get('start')}"))
                break
    return found


def run_clones(files: list[str], run: Runner) -> dict:
    with tempfile.TemporaryDirectory() as out:
        code, text = run([*JSCPD, "--silent", "--min-tokens", "50", "--min-lines", "5", "--max-lines", "100000000",
                          "--max-size", "1gb", "--reporters", "json", "--output", out, *files], None)
        report = Path(out) / "jscpd-report.json"
        if not report.is_file():
            raise Unmeasured(f"jscpd wrote no report (exit {code}): {text.strip()[-200:]}")
        return json.loads(report.read_text(encoding="utf-8"))


def judge_coverage(report: dict, touched: dict[str, set[int]], prod: set[str],
                   measured: dict[str, list[Function]]) -> list[Finding]:
    """Per changed function, its new executable lines; under the floor, a finding valued in lines missed."""
    places: dict[str, list[int]] = {}
    for name, data in report.get("files", {}).items():
        path = _rel(name)
        new = touched.get(path, set()) if path in prod else set()
        for n, hit in [(n, True) for n in data.get("executed_lines", []) if n in new] + \
                      [(n, False) for n in data.get("missing_lines", []) if n in new]:
            places.setdefault(f"{path}:{function_at(measured.get(path, []), n)}", []).append(0 if hit else n)
    found = []
    for place, lines in places.items():
        missed = [n for n in lines if n]
        if missed and (len(lines) - len(missed)) / len(lines) < COVERAGE_FLOOR:
            found.append(Finding("coverage", place, len(missed), f"{len(lines) - len(missed)} of {len(lines)} new lines "
                                                                 f"covered; missed {missed[:6]}"))
    return found


def run_coverage(profile: dict, run: Runner) -> dict:
    code, text = run([], profile["coverage_command"])
    report = ROOT / profile["coverage_report"]
    if code != 0 or not report.is_file():
        raise Unmeasured(f"the coverage command failed (exit {code}) or wrote no {profile['coverage_report']}: "
                         f"{text.strip()[-200:]}")
    return json.loads(report.read_text(encoding="utf-8"))


def placed(rule: str, rows: list[tuple[str, int, str]], touched: dict[str, set[int]],
           measured: dict[str, list[Function]]) -> list[Finding]:
    hits = [(f"{p}:{function_at(measured.get(p, []), n)}", f"line {n}: {msg}")
            for p, n, msg in rows if n in touched.get(p, set())]
    return tally(rule, hits)


def format_rows(diff: str) -> list[tuple[str, int, str]]:
    """`ruff format --diff`: each hunk's lines in the current file are lines the formatter would change."""
    found, path = [], None
    for line in diff.splitlines():
        if line.startswith("--- "):
            path = line[4:].removeprefix("a/").split("\t")[0]
        m = re.match(r"^@@ -(\d+)(?:,(\d+))? ", line)
        if m and path:
            start, count = int(m.group(1)), int(m.group(2) or 1)
            found += [(path, n, "not as ruff formats it") for n in range(start, start + max(count, 1))]
    return found


def lint_rows(output: str) -> list[tuple[str, int, str]]:
    try:
        rows = json.loads(output or "[]")
        return [(_rel(r["filename"]), r["location"]["row"], f"{r['code']} {r['message']}") for r in rows]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise Unmeasured(f"ruff's report did not parse: {e}") from e


def type_rows(output: str) -> list[tuple[str, int, str]]:
    pattern = re.compile(r"^(?P<path>[^:\n]+):(?P<line>\d+):(?:\d+:)? error: (?P<msg>.*)$")
    return [(m["path"], int(m["line"]), m["msg"]) for m in map(pattern.match, output.splitlines()) if m]


def run_checkers(files: list[str], touched: dict[str, set[int]], measured: dict[str, list[Function]],
                 run: Runner) -> list[Finding]:
    py = [sys.executable, "-m"]
    _, fmt = run([*py, "ruff", "format", "--diff", "--no-cache", *files], None)
    # The linter's own limit rules (C901, PLR0913) stay off: the measurer holds §2, and one finding is
    # never asked of the Chair twice.
    _, lint = run([*py, "ruff", "check", "--no-cache", "--output-format", "json", *files], None)
    with tempfile.TemporaryDirectory() as cache:
        _, types = run([*py, "mypy", "--strict", "--ignore-missing-imports", "--follow-imports", "silent",
                        "--no-error-summary", "--show-column-numbers", "--cache-dir", cache, *files], None)
    return (placed("format", format_rows(fmt), touched, measured) + placed("lint", lint_rows(lint), touched, measured)
            + placed("types", type_rows(types), touched, measured))


def run_audit(profile: dict, run: Runner) -> list[Finding]:
    found = []
    for manifest in profile.get("manifests", []):
        code, text = run([sys.executable, "-m", "pip_audit", "-r", manifest, "--progress-spinner", "off"], None)
        m = re.search(r"Found (\d+) known vulnerabilit", text)
        if code != 0:
            found.append(Finding("audit", manifest, int(m.group(1)) if m else 1, text.strip()[-300:]))
    if profile.get("manifests"):
        code, text = run([], profile["license_command"])
        if code != 0:
            raise Unmeasured(f"the license command failed (exit {code}): {text.strip()[-200:]}")
        try:
            packages = json.loads(text)
        except json.JSONDecodeError as e:
            raise Unmeasured(f"the license command's output is not JSON: {e}") from e
        allowed = set(profile.get("licenses_allowed", []))
        found += [Finding("license", p.get("Name", "?"), 1, f"license {p.get('License')!r} is not in licenses_allowed")
                  for p in packages if p.get("License") not in allowed]
    return found


def attempt(tool: str, check: Callable[[], list[Finding]]) -> list[Finding]:
    """A tool that cannot run is a finding, never a silent pass and never a wall."""
    try:
        return check()
    except Unmeasured as e:
        return [Finding("unmeasured", tool, 1, str(e))]


# ==============================================================================
# The gate
# ==============================================================================

def code_files(change: Change, profile: dict) -> tuple[list[str], list[str]]:
    """(changed Python files judged, of them the production ones)."""
    globs = profile["code"] + profile["tests"]
    judged = sorted(p for p in change.touched if p.endswith(".py") and matches(p, globs)
                    and not matches(p, profile.get("generated", [])) and change.read_new(p) is not None)
    return judged, [p for p in judged if matches(p, profile["code"]) and not matches(p, profile["tests"])]


def judge_change(change: Change, profile: dict, run: Runner) -> list[Finding]:
    judged, prod = code_files(change, profile)
    measured: dict[str, list[Function]] = {}
    found: list[Finding] = []
    for path in judged:
        here, measured[path] = judge_file(path, change.read_new(path) or "", change.touched[path], profile)
        found += here
    if judged:
        found += attempt("ruff and mypy", lambda: run_checkers(judged, change.touched, measured, run))
    if prod:
        everything = [p for p in change.files if p.endswith(".py") and matches(p, profile["code"])]
        found += attempt("jscpd", lambda: judge_clones(run_clones(everything, run), change.touched, set(prod), measured))
        found += attempt("coverage", lambda: judge_coverage(run_coverage(profile, run), change.touched, set(prod), measured))
    if change.is_range or any(m in change.touched for m in profile.get("manifests", [])):
        found += attempt("pip-audit and the license command", lambda: run_audit(profile, run))
    return found


def suggested_row(f: Finding) -> str:
    today = datetime.date.today().isoformat()
    return f"| {today} | — | `{f.where}` | {f.rule} {f.value} — {f.detail} | gate | none |  |"


def report(open_: list[Finding], answered: list[Finding], notes: list[str], broken: list[str]) -> int:
    print("\nCoding Standard Gate")
    print("=" * 60)
    for note in notes + [f"logged: {f.rule} {f.value} at {f.where}" for f in answered]:
        print(f"  note  {note}")
    for problem in broken:
        print(f"  LOG   {problem}: append a row instead; the audit log is never edited")
    if not open_ and not broken:
        print("PASSED" if not answered else f"PASSED: {len(answered)} finding(s) already in {LOG_FILE}")
        return 0
    if open_:
        print(f"PAUSED: {len(open_)} finding(s) not yet in {LOG_FILE}. Fix them, or append a row each with the "
              "Chair's response; no code change is required.\n")
        for f in open_:
            print(f"  {f.where}\n    Rule:    {f.rule} {f.value}\n    Detail:  {f.detail}\n    Advice:  {ADVICE.get(f.rule, '')}\n")
        print(f"Rows to append to {LOG_FILE}, the Chair's response in the last cell:\n")
        print("\n".join(suggested_row(f) for f in open_))
    return 1


def gate(change: Change, profile: dict, profile_findings: list[Finding], run: Runner) -> int:
    rows, unreadable = parse_log(change.read_new(LOG_FILE))
    old_rows, _ = parse_log(change.read_old(LOG_FILE))
    broken = ([unreadable] if unreadable else []) + log_edited(rows, old_rows)
    found = profile_findings + (judge_change(change, profile, run) if not profile_findings else [])
    notes = signals(change, code_files(change, profile)[1]) if not profile_findings else []
    if not profile_findings and not profile.get("manifests"):
        notes.append("audit: no manifest declared, so the dependency and license audit had nothing to judge")
    open_ = [f for f in found if not logged(f, rows)]
    return report(open_, [f for f in found if f not in open_], notes, broken)


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    profile_path = ROOT / PROFILE_FILE
    if not profile_path.is_file():
        print(f"Coding Standard Gate: no {PROFILE_FILE}, so this repository has not adopted the coding standard.")
        return 0
    profile, problems = load_profile(profile_path.read_text(encoding="utf-8"))
    try:
        spec = os.environ.get("CODE_STANDARD_RANGE", "") if "--range-from-env" in argv else \
            (argv[argv.index("--range") + 1] if "--range" in argv else "")
        change = range_change(spec) if spec else staged_change()
        return gate(change, profile, problems, run_tool)
    except GateError as e:
        print(f"code_standard: cannot read the change: {e}", file=sys.stderr)
        return 2


# ==============================================================================
# SELF-TEST — every rule against a passing and a failing fixture, in memory
# ==============================================================================

PROFILE = {"profile": "python", "code": ["src/**/*.py"], "tests": ["tests/**/*.py"], "generated": ["src/gen/**"],
           "coverage_command": "true", "coverage_report": "coverage.json", "manifests": []}
GOOD = '''import re


def small(a, b):
    """A docstring is not code."""
    if a and b:
        return a
    return b


class K:
    def method(self, x):
        return [y for y in x if y]

    async def later(self):
        def inner():
            return 1
        return inner()


def matcher(v):
    match v:
        case 1:
            return "one"
        case 2:
            return "two"
        case _:
            return "many"
'''
HEADER = "| " + " | ".join(LOG_COLUMNS) + " |\n|" + "---|" * len(LOG_COLUMNS) + "\n"


def _branchy(n: int, name: str = "branchy") -> str:
    body = "".join(f"    if x == {i}:\n        return {i}\n" for i in range(n))
    return f"def {name}(x):\n{body}    return -1\n"


def _long(n: int, name: str = "long") -> str:
    return f"def {name}():\n" + "".join(f"    v{i} = {i}\n" for i in range(n)) + "    return 0\n"


def _row(where: str, finding: str, response: str = "acknowledged, proceed") -> str:
    return f"| 2026-10-24 | — | `{where}` | {finding} | gate | none | {response} |\n"


def _change(files: dict[str, str], touched: dict[str, set[int]], old: dict[str, str] | None = None,
            is_range: bool = False) -> Change:
    old = old or {}
    return Change(touched, files.get, old.get, sorted(files), is_range)


class _Run:
    """A fake runner: canned output per tool, the calls recorded."""

    def __init__(self, outputs: dict[str, tuple[int, str]] | None = None) -> None:
        self.outputs, self.calls = outputs or {}, []

    def __call__(self, argv: list[str], shell: str | None) -> tuple[int, str]:
        key = shell if shell is not None else next((a for a in ("format", "check", "mypy", "pip_audit", "jscpd@4.0.5")
                                                    if a in argv), "?")
        self.calls.append(key)
        return self.outputs.get(key, (0, "[]" if key == "check" else ""))


def _check_factory():
    state = {"failures": 0, "total": 0}

    def check(label: str, ok: bool, detail: str = "") -> None:
        state["total"] += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok:
            state["failures"] += 1
            if detail:
                print(f"        {detail}")
    return check, state


def _rules(found: list[Finding]) -> set[str]:
    return {f.rule for f in found}


def _t_measurer(check) -> None:
    fns = {f.name: f for f in measure_python(GOOD)}
    check("the measurer finds every function, methods and a nested one included",
          set(fns) == {"small", "K.method", "K.later", "K.later.inner", "matcher"}, str(sorted(fns)))
    check("complexity counts `if` and `and`: small is 3", fns["small"].complexity == 3, str(fns["small"]))
    check("a comprehension's `for` and `if` count: method is 3", fns["K.method"].complexity == 3, str(fns["K.method"]))
    check("each `case` counts, which lizard missed: matcher is 4", fns["matcher"].complexity == 4, str(fns["matcher"]))
    check("a nested function's code is its own, not its parent's",
          fns["K.later"].code_lines == 2 and fns["K.later.inner"].code_lines == 2, str(fns["K.later"]))
    check("a docstring is not a code line: small has 4", fns["small"].code_lines == 4, str(fns["small"]))
    check("a declared `self` is a parameter", fns["K.method"].parameters == 2 and fns["small"].parameters == 2)
    check("the recall count reads `def` tokens, not the parser", def_count(GOOD) == 5 and def_count("x = 'def f(): pass'") == 0)
    check("a decorator is not the function's first line", measure_python("@dec\ndef f():\n    return 1\n")[0].start == 2)
    nested = {f.name: f for f in measure_python("def p():\n    def q(x):\n        if x or not x:\n            return 1\n    return q\n")}
    check("a nested function's decisions are its own: p is 1, p.q is 3",
          nested["p"].complexity == 1 and nested["p.q"].complexity == 3, str(nested))
    check("`*args`, keyword-only and `**kwargs` each count as a parameter",
          measure_python("def f(a, /, b, *c, d, **e):\n    return 1\n")[0].parameters == 5)


def _t_limits(check) -> None:
    def rules(path: str, text: str, lines: set[int]) -> set[str]:
        return _rules(judge_file(path, text, lines, PROFILE)[0])
    every = set(range(1, 120))
    check("complexity 16 over the production limit is a finding", rules("src/a.py", _branchy(15), every) == {"complexity"})
    check("complexity 15 is not", not rules("src/a.py", _branchy(14), every))
    check("61 code lines, the `def` line among them, are a finding", rules("src/a.py", _long(59), every) == {"code_lines"})
    check("60 code lines are not", not rules("src/a.py", _long(58), every))
    check("6 parameters are a finding", rules("src/a.py", "def f(a, b, c, d, e, f):\n    return 1\n", {1}) == {"parameters"})
    check("a test function at complexity 11 is over the test limit",
          rules("tests/t.py", _branchy(10, "test_b"), every) == {"complexity"})
    check("a test function at 81 code lines is within the test limit of 100", not rules("tests/t.py", _long(80, "test_l"), every))
    check("a helper in a test file is held to production limits: 13 passes", not rules("tests/t.py", _branchy(12, "helper"), every))


def _t_scope(check) -> None:
    text = _branchy(20) + "\n\ndef ok():\n    return 1\n"
    found, _ = judge_file("src/a.py", text, {len(text.splitlines())}, PROFILE)
    check("an over-limit function the change leaves alone is not judged", not found, str(found))
    found, _ = judge_file("src/a.py", text, {3}, PROFILE)
    check("editing one line of it judges it", _rules(found) == {"complexity"}, str(found))
    nested = "def outer():\n" + "".join(f"    if a{i}:\n        pass\n" for i in range(16)) + \
             "    def inner():\n        return 1\n    return inner\n"
    found, _ = judge_file("src/a.py", nested, {35}, PROFILE)
    check("editing a nested function does not judge its parent", not found, str(found))


def _t_recall(check) -> None:
    global measure_python
    real = measure_python
    try:
        measure_python = lambda text: real(text)[:-1]   # noqa: E731  — a measurer that drops one function
        found, _ = judge_file("src/a.py", GOOD, {1}, PROFILE)
        check("a measurer that misses a function is a recall finding", _rules(found) == {"recall"}, str(found))
    finally:
        measure_python = real
    found, _ = judge_file("src/a.py", "def broken(:\n", {1}, PROFILE)
    check("a file Python cannot parse is a recall finding, never a pass", _rules(found) == {"recall"}, str(found))
    found, _ = judge_file("src/a.py", GOOD, {1}, PROFILE)
    check("a file read in full passes recall", not found, str(found))


def _t_log(check) -> None:
    f = Finding("complexity", "src/a.py:branchy", 21, "x")
    rows, err = parse_log(HEADER + _row("src/a.py:branchy", "complexity 21 — a parser"))
    check("a finding the Chair answered at its value is logged", not err and logged(f, rows), str(err))
    rows, _ = parse_log(HEADER + _row("src/a.py:branchy", "complexity 18"))
    check("a finding that got worse than its row is open again", not logged(f, rows))
    rows, _ = parse_log(HEADER + _row("src/a.py:branchy", "complexity 25"))
    check("a finding that got better stays logged", logged(f, rows))
    rows, _ = parse_log(HEADER + _row("src/a.py:branchy", "complexity 21", response="pending"))
    check("a row with no response from the Chair logs nothing", not logged(f, rows))
    rows, _ = parse_log(HEADER + _row("src/a.py:other", "complexity 21"))
    check("a row for another place logs nothing", not logged(f, rows))
    _, err = parse_log("| Date | Where |\n|---|---|\n")
    check("a log with other columns cannot be read, never read as empty", err is not None)
    old, _ = parse_log(HEADER + _row("src/a.py:b", "complexity 21"))
    new, _ = parse_log(HEADER + _row("src/a.py:b", "complexity 30"))
    check("an edited row is refused; an appended one is not",
          bool(log_edited(new, old)) and not log_edited(old + new, old))


def _t_markers(check) -> None:
    text = "def f():\n    return 1  # noqa: C901\n\n\ndef g():\n    return 2  # pragma: no cover\n# GENERATED CODE\n"
    found, _ = judge_file("src/a.py", text, {2, 6, 7}, PROFILE)
    check("suppressions and a stray generated marker are findings, one per place",
          _rules(found) == {"suppression", "generated-marker"} and len(found) == 3, str(found))
    found, _ = judge_file("src/gen/a.py", text, {7}, PROFILE)
    check("a generated marker under a declared generated path is not", not found, str(found))
    found, _ = judge_file("src/a.py", text, {1}, PROFILE)
    check("a suppression on an unchanged line is not this change's", not found, str(found))


def _t_diff(check) -> None:
    diff = ("diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -3,0 +4,2 @@\n+x\n+y\n"
            "@@ -10,2 +12,0 @@\n-gone\n-gone\n--- /dev/null\n+++ b/src/new.py\n@@ -0,0 +1,3 @@\n+a\n+b\n+c\n"
            "--- a/src/old.py\n+++ /dev/null\n@@ -1,2 +0,0 @@\n-a\n-b\n")
    t = parse_diff(diff)
    check("a diff's added lines, a deletion's neighbours, a new file whole, a deleted file none",
          t == {"src/a.py": {4, 5, 12, 13}, "src/new.py": {1, 2, 3}}, str(t))
    ch = _change({"src/a.py": "x = 1\n" * 600}, {"src/a.py": {1}, "requirements.txt": {1}}, {"src/a.py": "x = 1\n"})
    notes = signals(ch, ["src/a.py"])
    check("a file grown past 500 lines and a manifest touched are reported, not findings",
          any("file length" in n for n in notes) and any("a new dependency" in n for n in notes), str(notes))


def _t_clones(check) -> None:
    rep = {"duplicates": [{"lines": 8, "firstFile": {"name": "src/a.py", "start": 10, "end": 17},
                           "secondFile": {"name": "src/b.py", "start": 1, "end": 8}}]}
    measured = {"src/a.py": measure_python(_long(30))}
    found = judge_clones(rep, {"src/a.py": {12}}, {"src/a.py"}, measured)
    check("a clone among the added lines is a finding valued in lines",
          _rules(found) == {"clone"} and found[0].value == 8 and found[0].where == "src/a.py:long", str(found))
    check("a clone the change does not touch is not this change's", not judge_clones(rep, {"src/a.py": {40}}, {"src/a.py"}, measured))


def _t_coverage(check) -> None:
    measured = {"src/a.py": measure_python(_long(10))}
    rep = {"files": {"src/a.py": {"executed_lines": [2, 3, 4, 5], "missing_lines": [6, 7]}}}
    found = judge_coverage(rep, {"src/a.py": {2, 3, 4, 5, 6}}, {"src/a.py"}, measured)
    check("4 of 5 new lines covered (80%) is not a finding", not found, str(found))
    found = judge_coverage(rep, {"src/a.py": {3, 4, 6, 7}}, {"src/a.py"}, measured)
    check("2 of 4 new lines covered is a finding valued in lines missed",
          _rules(found) == {"coverage"} and found[0].value == 2, str(found))
    check("new lines in test files are not counted", not judge_coverage(rep, {"src/a.py": {6, 7}}, set(), measured))


def _t_checkers(check) -> None:
    fmt = "--- src/a.py\n+++ src/a.py\n@@ -3,2 +3,2 @@\n-x=1\n+x = 1\n"
    lint = json.dumps([{"filename": "src/a.py", "location": {"row": 7}, "code": "F401", "message": "unused"},
                       {"filename": "src/a.py", "location": {"row": 40}, "code": "F841", "message": "old debt"}])
    types = "src/a.py:8:5: error: Function is missing a type annotation  [no-untyped-def]\nsrc/a.py:50: error: old  [x]\n"
    run = _Run({"format": (1, fmt), "check": (1, lint), "mypy": (1, types)})
    found = run_checkers(["src/a.py"], {"src/a.py": {3, 7, 8}}, {}, run)
    check("format, lint and type findings on changed lines are findings", _rules(found) == {"format", "lint", "types"}, str(found))
    check("findings on lines the change leaves alone are old debt, not counted",
          not run_checkers(["src/a.py"], {"src/a.py": {20}}, {}, run))
    found = attempt("ruff and mypy", lambda: run_checkers(["src/a.py"], {"src/a.py": {7}}, {}, _Run({"check": (2, "not json")})))
    check("a tool whose report cannot be read is an unmeasured finding, never a pass", _rules(found) == {"unmeasured"}, str(found))


def _t_audit(check) -> None:
    prof = dict(PROFILE, manifests=["requirements.txt"], license_command="lic", licenses_allowed=["MIT License"])
    run = _Run({"pip_audit": (1, "Found 2 known vulnerabilities in 1 package"),
                "lic": (0, json.dumps([{"Name": "flask", "License": "BSD License"}]))})
    found = run_audit(prof, run)
    check("vulnerabilities and a license outside the policy are findings",
          _rules(found) == {"audit", "license"} and found[0].value == 2, str(found))
    ch = _change({"src/a.py": "x = 1\n", "requirements.txt": "flask\n"}, {"src/a.py": {1}})
    quiet = _Run()
    judge_change(ch, prof, quiet)
    check("at commit, an untouched manifest is not audited", "pip_audit" not in quiet.calls, str(quiet.calls))
    ch.is_range = True
    judge_change(ch, prof, quiet)
    check("over a range the audit always runs", "pip_audit" in quiet.calls, str(quiet.calls))


def _t_gate(check) -> None:
    def quiet_gate(ch: Change) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return gate(ch, PROFILE, [], _Run())
    files = {"tests/t.py": _branchy(12, "test_b")}   # a test file: no clone or coverage run is needed
    ch = _change(files, {"tests/t.py": {3}})
    check("an unlogged finding pauses the change", quiet_gate(ch) == 1)
    files[LOG_FILE] = HEADER + _row("tests/t.py:test_b", "complexity 13")
    check("the same finding answered in the log lets it proceed, no code changed", quiet_gate(ch) == 0)
    ch = _change(dict(files, **{LOG_FILE: HEADER}), {"tests/t.py": {3}}, {LOG_FILE: files[LOG_FILE]})
    check("a log whose base row was removed is refused whatever else holds", quiet_gate(ch) == 1)
    check("a change with no finding passes", quiet_gate(_change({"tests/t.py": "def test_ok():\n    return 1\n"},
                                                                 {"tests/t.py": {1}})) == 0)


def _t_profile(check) -> None:
    import yaml
    check("a complete profile loads", not load_profile(yaml.safe_dump(PROFILE))[1])
    check("a profile not built here is a finding, never read as python",
          _rules(load_profile(yaml.safe_dump(dict(PROFILE, profile="rust")))[1]) == {"profile"})
    check("a profile with an empty slot is not adoptable", _rules(load_profile(yaml.safe_dump(dict(PROFILE, code=[])))[1]) == {"profile"})
    check("manifests without a license policy are a finding",
          _rules(load_profile(yaml.safe_dump(dict(PROFILE, manifests=["requirements.txt"])))[1]) == {"profile"})
    check("a profile that does not parse is a finding", _rules(load_profile("profile: [unclosed")[1]) == {"profile"})


def standard_limits(text: str) -> dict[str, int]:
    """The numbers in the standard's §2 table, read so the gate cannot drift from its law."""
    section = text.split("## 2. The core limits", 1)[-1].split("\n## ", 1)[0]
    rows = {r.split("|")[1].strip(): r for r in section.splitlines() if r.startswith("| ") and r.count("|") >= 3}
    num = lambda key, cell: int(re.findall(r"\d+", rows[key].split("|")[cell])[0])  # noqa: E731
    complexity, lines = "Cyclomatic complexity per function", "Code lines per function, blanks and comments excluded"
    return {"complexity": num(complexity, 2), "test_complexity": num(complexity, 3), "code_lines": num(lines, 2),
            "test_code_lines": num(lines, 3), "parameters": num("Parameters per function, a declared receiver (`self`) included", 2),
            "coverage": num("Coverage of the change's new lines", 2), "file_signal": num("File length", 2)}


def _t_law(check) -> None:
    path = ROOT / STANDARD
    if not path.is_file():
        check(f"{STANDARD} exists to hold the numbers", False)
        return
    law = standard_limits(path.read_text(encoding="utf-8"))
    mine = {"complexity": LIMITS["production"]["complexity"], "test_complexity": LIMITS["test"]["complexity"],
            "code_lines": LIMITS["production"]["code_lines"], "test_code_lines": LIMITS["test"]["code_lines"],
            "parameters": LIMITS["production"]["parameters"], "coverage": round(COVERAGE_FLOOR * 100),
            "file_signal": FILE_SIGNAL}
    check("every number the gate holds equals the standard's §2", law == mine, f"standard {law}, gate {mine}")
    own = measure_python(Path(__file__).read_text(encoding="utf-8"))
    over = [f"{f.name} ({f.complexity}c/{f.code_lines}l/{f.parameters}p)" for f in own if judge_function("", f, "production")]
    check("this gate's own functions meet the production limits", not over, ", ".join(over))


def run_self_test() -> int:
    print("\nCoding Standard Self-Test")
    print("=" * 60)
    check, state = _check_factory()
    for group in (_t_measurer, _t_limits, _t_scope, _t_recall, _t_log, _t_markers, _t_diff, _t_clones,
                  _t_coverage, _t_checkers, _t_audit, _t_gate, _t_profile, _t_law):
        try:
            group(check)
        except Exception as e:   # a crash is a failed fixture, never a crashed self-test
            check(f"{group.__name__} ran without raising", False, f"{type(e).__name__}: {e}")
    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 0 if not state["failures"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
