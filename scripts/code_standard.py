#!/usr/bin/env python3
"""
code_standard.py — the coding standard's gate: the code a change adds or edits, measured against
docs/standards/coding_standard_v1.0.md, every finding written to the code review audit log.

WHAT IT DOES
------------
A project opts in with `code-profile.yaml` at its root; with none the gate says so and passes.

    profile: python                      # a stack profile this script holds: python, rust or typescript
    code: ["pipeline/**/*.py"]           # production code
    tests: ["tests/**/*.py"]             # test code; only its `test*` functions are test functions
    generated: []                        # generated paths, never measured
    coverage_command: "python -m coverage run -m pytest && python -m coverage json -o coverage.json"
    coverage_report: coverage.json       # coverage.py's JSON report, written by the command
    manifests: [requirements.txt]        # dependency manifests the audit reads; [] when none
    license_command: "pip-licenses --format=json"   # in the project's environment; with manifests
    licenses_allowed: [MIT License, BSD License, Apache Software License]

A Rust project also carries rust-toolchain.toml naming an exact toolchain, which
pins rustfmt and clippy; cargo-llvm-cov 0.9.1 and cargo-deny 0.20.2 are pinned here:

    profile: rust
    code: ["src/**/*.rs"]
    tests: ["tests/**/*.rs"]             # and any `#[test]` function, wherever it lives
    generated: []
    coverage_command: "cargo llvm-cov --lcov --output-path lcov.info"
    coverage_report: lcov.info           # lcov, read as coverage.py's executed and missing lines
    manifests: [Cargo.toml, Cargo.lock]
    licenses_allowed: [MIT, Apache-2.0]  # written into cargo-deny's config for the run

A TypeScript project pins prettier, eslint and typescript at exact versions in
package.json, with a lockfile, which names the manager: npm, pnpm, yarn 1, or yarn 2 and later; pnpm
and yarn also name their exact version in `packageManager`, run through corepack:

    profile: typescript
    code: ["src/**/*.ts", "src/**/*.tsx"]
    tests: ["tests/**/*.ts"]             # and any `it` or `test` callback, wherever it lives
    generated: []
    coverage_command: "npx --no-install vitest run --coverage --coverage.reporter=lcov"
    coverage_report: coverage/lcov.info
    manifests: [package.json, package-lock.json]
    licenses_allowed: [MIT, ISC, Apache-2.0]   # over production dependencies; an `OR` passes on one

On the change (the staged change by default; `--range A..B`, or CODE_STANDARD_RANGE through
`--range-from-env`, in CI), for every code file it touches, findings keyed by where they are:
  recall       the measurer finds as many functions as the file defines (`def` tokens; in Rust, `fn`
               items counted by a lexer of its own; in TypeScript, by typescript 5.9.3's compiler),
               or nothing it reports for the file can be trusted; in Rust and TypeScript, also a
               changed function its parser read with an error
  complexity   a changed function's cyclomatic complexity over 15 (a test function's over 10)
  code_lines   its code lines, blanks, comments and its docstring excluded, over 60 (100)
  parameters   its parameters, a declared `self` included, over 5; in Rust, a Bevy system parameter
               not counted
  suppression  a limit-suppressing comment on a changed line (`noqa: C901`, `pragma: no cover`,
               `jscpd:ignore-start`, `lizard forgives`; in Rust an `allow` of a clippy lint,
               `coverage(off)`; in TypeScript an `eslint-disable`, a `@ts-ignore`,
               `@ts-expect-error` or `@ts-nocheck`, a coverage `ignore`)
  generated-marker  a generated-code marker outside a declared generated path
  clone        a copy of existing code among the change's added lines (jscpd 4.0.5, 50 tokens and 5
               lines, its size caps lifted)
  coverage     a changed function's new executable lines under 80% covered, by the project's tests
  format, lint, types  ruff format, ruff check and mypy --strict, on changed lines only; in Rust,
               cargo fmt --check, and one cargo clippy run, a warning a lint and an error the
               compiler's; in TypeScript, prettier's output compared with the file, ESLint's JSON
               and tsc --noEmit --strict, the project's own copies
  audit, license  pip-audit on each manifest and the license policy, when a manifest changes and
               always over a range; in Rust, cargo-deny's advisories and licenses; in TypeScript,
               the manager's audit and its license listing of production dependencies
  unmeasured   a tool that could not run, so its check was not made
Each finding is logged when a row of the audit log names its place and rule, a value at least the
finding's, and a response from the Chair. The log is append-only: a row the base held, edited or
removed, is the one thing no response clears. It reports, and never pauses on, a production file
grown past 500 lines and the review-trigger paths the change touches.

A function is changed when an added or edited line falls among its own lines, its nested functions'
lines being theirs. Complexity counts each `if`, `elif`, `for`, `while`, `except`, `finally`,
`and`, `or`, conditional expression, comprehension `for` and `if`, and `case`, plus one: the points
the calibration's measurer counted, with Python's `match` added, which it missed.

--self-test   in-memory fixtures for every rule, and this script's own functions held to the limits
Exit 0 every finding logged or not adopted, 1 a finding not yet logged or the log edited, 2 git failing.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It judges no code a change leaves alone, and makes no judgement: names, cohesion and near-copies the
clone detector cannot see are the code reviewer's, logged in the same table. It holds the Python, Rust and TypeScript profiles. The Rust slots assume the Cargo
workspace at the repository's root, and the TypeScript slots the package there.
"""
from __future__ import annotations

import ast
import collections
import contextlib
import datetime
import difflib
import functools
import io
import json
import os
import re
import shlex
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

# The core limits. The self-test holds them equal to the standard's §2.
LIMITS = {"production": {"complexity": 15, "code_lines": 60, "parameters": 5},
          "test": {"complexity": 10, "code_lines": 100, "parameters": 5}}
COVERAGE_FLOOR = 0.80
FILE_SIGNAL = 500
JSCPD = ["npx", "--yes", "jscpd@4.0.5"]
SUFFIXES = {"python": ".py", "rust": ".rs", "typescript": (".ts", ".tsx")}   # the stack profiles this script holds
# The Rust profile's tools installed apart from the toolchain, pinned here;
# rustfmt and clippy are the toolchain's, which the project's rust-toolchain.toml pins.
RUST_PINS = {"cargo-llvm-cov": "0.9.1", "cargo-deny": "0.20.2"}
# clippy's own copies of §2's limits stay off, the measurer holding them, and Bevy's queries make
# `type_complexity` noise.
CLIPPY_ALLOWS = ["-A", "clippy::too_many_arguments", "-A", "clippy::too_many_lines", "-A",
                 "clippy::cognitive_complexity", "-A", "clippy::type_complexity"]

# What a line can carry to switch a check off, each named as its finding says it: a pattern's own
# `|` would split the log's table row.
SUPPRESSIONS = {
    "a `noqa` of a limit rule": re.compile(r"#\s*noqa\b.*\b(C901|PLR091[2-5])\b"),
    "`pragma: no cover`": re.compile(r"#\s*pragma:\s*no\s*cover"),
    "`jscpd:ignore-start`": re.compile(r"jscpd:ignore-start"),
    "`lizard forgives`": re.compile(r"#\s*lizard\s+forgives"),
    "an `allow` or `expect` of a clippy lint or of warnings": re.compile(r"#!?\[\s*(allow|expect)\s*\([^)\]]*\b(clippy::|warnings\b)"),
    "`coverage(off)`": re.compile(r"\bcoverage\s*\(\s*off\s*\)"),
    "an `eslint-disable`": re.compile(r"eslint-disable"),
    "a `@ts-ignore`, `@ts-expect-error` or `@ts-nocheck`": re.compile(r"@ts-(ignore|expect-error|nocheck)\b"),
    "a coverage `ignore`": re.compile(r"\b(istanbul|v8|c8)\s+ignore\b"),
}
GENERATED_MARKER = re.compile(r"@generated\b|GENERATED CODE")

# The paths that show the review triggers in a Python or a Rust project.
TRIGGER_PATHS = {
    "a new dependency": ["requirements*.txt", "**/requirements*.txt", "pyproject.toml", "setup.py", "setup.cfg",
                         "Pipfile", "Pipfile.lock", "poetry.lock", "uv.lock", "Cargo.toml", "**/Cargo.toml", "Cargo.lock",
                         "package.json", "**/package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"],
    "a schema change": ["**/migrations/**", "**/*.sql", "**/schema*"],
    "an auth or crypto change": ["**/*auth*", "**/*crypt*", "**/*secret*", "**/*token*"],
    "a cost": ["**/*.tf", "**/*.bicep", "infra/**", "**/Dockerfile*"],
    # The writing profile is a gate change in every stack: its allow list exempts text from the gate.
    "a gate or CI change": [".github/**", ".pre-commit-config.yaml", "scripts/**", "writing-profile.yaml",
                            "build.rs", "**/build.rs", "rust-toolchain.toml", "rust-toolchain", "clippy.toml",
                            ".clippy.toml", "rustfmt.toml", ".rustfmt.toml", ".cargo/**", "tsconfig*.json",
                            "eslint.config.*", ".eslintrc*", "prettier.config.*", ".prettierrc*", ".yarnrc.yml", ".npmrc"],
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
    "format": "Run the stack's formatter on the file (`ruff format`, `cargo fmt`).",
    "lint": "Fix what the linter reports on the changed lines (ruff, clippy).",
    "types": "Make the changed lines pass the type check (mypy --strict, the Rust compiler).",
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
    error_line: int = 0          # the first line its parser read with an error in its own code; 0 if none
    test: bool = False           # marked a test by its language (Rust's `#[test]`), wherever it lives


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
# The Rust profile's measurer, on tree-sitter-rust
# ==============================================================================

RUST_FUNCTIONS = ("function_item", "function_signature_item")
RUST_SCOPES = {"impl_item": "type", "trait_item": "name", "mod_item": "name"}
RUST_BRANCHES = ("if_expression", "while_expression", "for_expression", "match_arm")
RUST_COMMENTS = ("line_comment", "block_comment")
# A parameter of one of Bevy's system parameter types, or an `Option` of one, is not counted toward
# the parameter limit: a Bevy system takes its world access as parameters.
BEVY_SYSTEM_PARAMS = frozenset({
    "Commands", "Query", "Res", "ResMut", "Local", "EventReader", "EventWriter", "MessageReader",
    "MessageWriter", "ParamSet", "NonSend", "NonSendMut", "Single", "Populated", "Gizmos",
    "RemovedComponents", "Deferred", "In", "InRef", "InMut", "Trigger", "On",
})


@functools.lru_cache(maxsize=1)
def _rust_parser():
    import tree_sitter
    import tree_sitter_rust
    return tree_sitter.Parser(tree_sitter.Language(tree_sitter_rust.language()))


def _rows(node) -> set[int]:
    return set(range(node.start_point[0] + 1, node.end_point[0] + 2))


# Shared by the measurers on tree-sitter (Rust, TypeScript): each takes the stack's test of what is a
# function of its own, whose code, lines and errors are its and never its parent's.

def _tree_code_lines(root, comments: tuple[str, ...]) -> set[int]:
    """Lines holding a token that is not a comment."""
    lines: set[int] = set()
    stack = [root]
    while stack:
        node = stack.pop()
        if node.type in comments:
            continue
        if node.child_count == 0:
            lines |= _rows(node)
        stack.extend(node.children)
    return lines


def _tree_decisions(node, weight: Callable, is_fn: Callable) -> int:
    """Decision points in a function's own code, a nested function's excluded."""
    return sum(weight(c) + _tree_decisions(c, weight, is_fn) for c in node.children if not is_fn(c))


def _tree_own_lines(fn, is_fn: Callable) -> frozenset[int]:
    lines = _rows(fn)
    stack = list(fn.named_children)
    while stack:
        node = stack.pop()
        if is_fn(node):
            lines -= _rows(node)
        else:
            stack.extend(node.named_children)
    return frozenset(lines)


def _tree_own_error(fn, is_fn: Callable) -> int:
    """The first line of a parse error in a function's own code, a nested function's excluded; 0 if
    none. tree-sitter marks an error where it is, so the rest of the file is still read."""
    if not fn.has_error:
        return 0
    stack, rows = list(fn.children), []
    while stack:
        node = stack.pop()
        if node.type == "ERROR" or node.is_missing:
            rows.append(node.start_point[0] + 1)
        elif node.has_error and not is_fn(node):
            stack.extend(node.children)
    return min(rows, default=0)


def _is_rust_fn(node) -> bool:
    return node.type in RUST_FUNCTIONS


def _rust_weight(node) -> int:
    if node.type in RUST_BRANCHES:
        return 1
    if node.type == "match_pattern" and node.child_by_field_name("condition") is not None:
        return 1                                   # a match guard
    if node.type == "binary_expression":
        return int(node.child_by_field_name("operator").type in ("&&", "||"))
    if node.type == "let_chain":
        return sum(1 for c in node.children if c.type == "&&")
    return 0


def _type_name(node) -> tuple[str, object]:
    """A type's last path segment and its first type argument: `bevy::prelude::Res<Time>` is `Res`, `Time`."""
    if node is None:
        return "", None
    if node.type == "generic_type":
        args = node.child_by_field_name("type_arguments")
        first = next(iter(args.named_children), None) if args else None
        return _type_name(node.child_by_field_name("type"))[0], first
    if node.type == "scoped_type_identifier":
        return node.child_by_field_name("name").text.decode(), None
    return (node.text.decode(), None) if node.type == "type_identifier" else ("", None)


def bevy_param(node) -> bool:
    name, first = _type_name(node)
    return name in BEVY_SYSTEM_PARAMS or (name == "Option" and first is not None and bevy_param(first))


def _rust_parameters(fn) -> int:
    """`self` and every parameter, a Bevy system parameter excepted."""
    params = fn.child_by_field_name("parameters")
    kept = [c for c in (params.named_children if params else [])
            if c.type in ("self_parameter", "variadic_parameter")
            or (c.type == "parameter" and not bevy_param(c.child_by_field_name("type")))]
    return len(kept)


def _rust_scope(node) -> str:
    target = node.child_by_field_name(RUST_SCOPES[node.type])
    return _type_name(target)[0] or (target.text.decode() if target else "?")


def _rust_is_test(fn) -> bool:
    """An attribute before the fn whose path ends in `test`, `#[test]` or `#[tokio::test]`: test code
    wherever it lives. `#[cfg(test)]` marks a module, not a test."""
    node = fn.prev_named_sibling
    while node is not None and node.type in ("attribute_item", *RUST_COMMENTS):
        attr = next((c for c in node.named_children if c.type == "attribute"), None)
        path = attr.named_children[0].text.decode() if attr is not None and attr.named_children else ""
        if path.split("::")[-1].endswith("test"):
            return True
        node = node.prev_named_sibling
    return False


def measure_rust(text: str) -> list[Function]:
    """Every `fn`, a trait's and an extern block's signatures included, its metrics from its own lines."""
    tree = _rust_parser().parse(text.encode("utf-8"))
    code = _tree_code_lines(tree.root_node, RUST_COMMENTS)
    found: list[Function] = []

    def visit(node, prefix: str) -> None:
        for child in node.named_children:
            if child.type in RUST_FUNCTIONS:
                name = prefix + child.child_by_field_name("name").text.decode()
                own = _tree_own_lines(child, _is_rust_fn)
                found.append(Function(name, child.start_point[0] + 1, child.end_point[0] + 1,
                                      1 + _tree_decisions(child, _rust_weight, _is_rust_fn), len(own & code),
                                      _rust_parameters(child), own, _tree_own_error(child, _is_rust_fn),
                                      _rust_is_test(child)))
                visit(child, name + "::")
            else:
                visit(child, prefix + _rust_scope(child) + "::" if child.type in RUST_SCOPES else prefix)

    visit(tree.root_node, "")
    return found


def _block_end(text: str, i: int) -> int:
    """Past a block comment opening at i; Rust's nest."""
    depth = 0
    while i < len(text):
        if text.startswith("/*", i):
            depth, i = depth + 1, i + 2
        elif text.startswith("*/", i):
            depth, i = depth - 1, i + 2
            if depth == 0:
                return i
        else:
            i += 1
    return i


def _string_end(text: str, i: int) -> int:
    """Past a string whose body starts at i, escapes honoured."""
    while i < len(text) and text[i] != '"':
        i += 2 if text[i] == "\\" else 1
    return i + 1


def _raw_end(text: str, i: int) -> int | None:
    """Past a raw string whose hashes start at i (`r#"…"#`), or None if none starts there."""
    j = i
    while j < len(text) and text[j] == "#":
        j += 1
    if not text.startswith('"', j):
        return None
    close = text.find('"' + "#" * (j - i), j + 1)
    return len(text) if close < 0 else close + 1 + (j - i)


def _quote_end(text: str, i: int) -> int:
    """Past a character literal at i, or past a lifetime or a label, which has no closing quote."""
    if text.startswith("\\", i + 1):
        close = text.find("'", i + 2)
        return len(text) if close < 0 else close + 1
    if text.startswith("'", i + 2):
        return i + 3
    return _word_end(text, i + 1)


def _word_end(text: str, i: int) -> int:
    while i < len(text) and (text[i].isalnum() or text[i] == "_"):
        i += 1
    return i


def _skip(text: str, i: int) -> int | None:
    """Past whitespace, a comment, a string or a quote at i; None if a word or a symbol starts there."""
    if text[i].isspace():
        return i + 1
    if text.startswith("//", i):
        end = text.find("\n", i)
        return len(text) if end < 0 else end
    if text.startswith("/*", i):
        return _block_end(text, i)
    if text[i] == '"':
        return _string_end(text, i + 1)
    return _quote_end(text, i) if text[i] == "'" else None


def fn_count(text: str) -> int:
    """`fn` items, read by a lexer of the gate's own, never the parser: the recall check's independent
    count. A `fn` followed by a name is an item; one followed by `(` is a pointer type."""
    count, i, pending = 0, 0, False
    while i < len(text):
        past = _skip(text, i)
        if past is not None:                      # whitespace and comments keep a pending `fn`; a literal ends it
            trivia = text[i].isspace() or text.startswith(("//", "/*"), i)
            pending, i = pending and trivia, past
            continue
        if not (text[i].isalpha() or text[i] == "_"):
            pending, i = False, i + 1
            continue
        end = _word_end(text, i)
        word = text[i:end]
        raw = _raw_end(text, end) if word in ("r", "br", "cr") else None
        if raw is not None:
            pending, i = False, raw
            continue
        if word == "r" and text.startswith("#", end):
            end = _word_end(text, end + 1)        # a raw identifier, `r#type`: a name, never the keyword
            word = "r#"
        count += pending
        pending, i = word == "fn", end
    return count


# ==============================================================================
# The TypeScript profile's measurer, on tree-sitter-typescript
# ==============================================================================

TS_COMMENTS = ("comment",)
TS_BRANCHES = ("if_statement", "for_statement", "for_in_statement", "while_statement", "do_statement",
               "switch_case", "catch_clause", "ternary_expression")
TS_LOGICAL = ("&&", "||", "??", "&&=", "||=", "??=")
# Declarations and methods always have a body here: an overload, an abstract method and an interface's
# member are other node types (`function_signature`, `abstract_method_signature`, `method_signature`).
TS_BODIED = ("function_declaration", "generator_function_declaration", "method_definition")
TS_EXPRESSIONS = ("arrow_function", "function_expression", "generator_function")
# Where an arrow or a function expression is bound to a name, and the field naming it.
TS_BINDINGS = {"variable_declarator": "name", "public_field_definition": "name", "pair": "key",
               "assignment_expression": "left", "export_statement": None}
TS_SCOPES = ("class_declaration", "abstract_class_declaration", "class")
TS_TESTS = ("it", "test")              # a callback passed to one is a test function
TS_RECALL = "typescript@5.9.3"          # the last release whose package exposes the compiler API
# The recall count: TypeScript's own parser counting the same named functions.
TS_COUNT_JS = r"""
const fs = require("fs"), path = require("path");
const bin = process.env.PATH.split(path.delimiter).find((d) => fs.existsSync(path.join(d, "tsc")));
const ts = require(path.join(bin, "..", "typescript"));
const name = process.argv[2], text = fs.readFileSync(0, "utf8");
const sf = ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true,
                               /\.tsx$/.test(name) ? ts.ScriptKind.TSX : ts.ScriptKind.TS);
const runner = (call) => { let e = call.expression;
  while (ts.isPropertyAccessExpression(e) || ts.isCallExpression(e)) e = e.expression;
  return ts.isIdentifier(e) && (e.text === "it" || e.text === "test"); };
const named = (n) => { const p = n.parent;
  return (ts.isVariableDeclaration(p) || ts.isPropertyDeclaration(p) || ts.isPropertyAssignment(p)) && p.initializer === n
    || ts.isBinaryExpression(p) && p.operatorToken.kind === ts.SyntaxKind.EqualsToken && p.right === n
    || ts.isExportAssignment(p)
    || ts.isCallExpression(p) && p.arguments.includes(n) && runner(p); };
let count = 0;
const visit = (n) => {
  if ((ts.isFunctionDeclaration(n) || ts.isMethodDeclaration(n) || ts.isConstructorDeclaration(n)
       || ts.isGetAccessorDeclaration(n) || ts.isSetAccessorDeclaration(n)) && n.body) count++;
  else if ((ts.isArrowFunction(n) || ts.isFunctionExpression(n)) && named(n)) count++;
  ts.forEachChild(n, visit);
};
visit(sf);
process.stdout.write(String(count));
"""


@functools.lru_cache(maxsize=2)
def _ts_parser(tsx: bool):
    import tree_sitter
    import tree_sitter_typescript
    language = tree_sitter_typescript.language_tsx() if tsx else tree_sitter_typescript.language_typescript()
    return tree_sitter.Parser(tree_sitter.Language(language))


def ts_binding(node) -> str | None:
    """The name a function measured on its own goes by: a declaration, method, constructor or accessor
    with a body, or an arrow or function expression bound to a name. None for anything else, an inline
    callback included, whose code is the function's around it."""
    if node.type in TS_BODIED:
        name = node.child_by_field_name("name")
        return name.text.decode() if name else "default"
    parent = node.parent
    if node.type not in TS_EXPRESSIONS or parent is None:
        return None
    if parent.type in TS_BINDINGS:
        naming = TS_BINDINGS[parent.type]
        return parent.child_by_field_name(naming).text.decode() if naming else "default"
    return ts_test_name(node)


def _ts_runner(call) -> str | None:
    """The test runner a call is, `it` or `test`, through `.only`, `.skip` or `.each(table)`; None if none."""
    callee = call.child_by_field_name("function")
    while callee is not None and callee.type in ("member_expression", "call_expression"):
        callee = callee.child_by_field_name("object" if callee.type == "member_expression" else "function")
    name = callee.text.decode() if callee is not None and callee.type == "identifier" else ""
    return name if name in TS_TESTS else None


def ts_test_name(node) -> str | None:
    """A callback passed to `it` or `test` is a test function, named by its runner and its title; None for any other callback."""
    args = node.parent
    call = args.parent if args is not None and args.type == "arguments" else None
    runner = _ts_runner(call) if call is not None and call.type == "call_expression" else None
    if runner is None:
        return None
    first = args.named_children[0] if args.named_children else None
    title = first.text.decode()[1:-1] if first is not None and first.type in ("string", "template_string") else "?"
    return f"{runner} {title}"


def _is_ts_fn(node) -> bool:
    return ts_binding(node) is not None


def _ts_weight(node) -> int:
    if node.type in TS_BRANCHES:
        return 1
    if node.type in ("binary_expression", "augmented_assignment_expression"):
        op = node.child_by_field_name("operator")
        return int(op is not None and op.type in TS_LOGICAL)
    return 0


def _ts_parameters(fn) -> int:
    """Every parameter, a `this` annotation, which is a type and no parameter, excepted."""
    params = fn.child_by_field_name("parameters")
    if params is None:                    # `x => x`: one bare parameter
        return int(fn.child_by_field_name("parameter") is not None)
    return sum(1 for c in params.named_children if c.type in ("required_parameter", "optional_parameter")
               and getattr(c.child_by_field_name("pattern"), "type", "") != "this")


def _ts_scope(node) -> str:
    """The prefix a class, or an object bound to a name, gives the functions inside it."""
    if node.type in TS_SCOPES and node.child_by_field_name("name") is not None:
        return node.child_by_field_name("name").text.decode() + "."
    if node.type == "object" and node.parent is not None and node.parent.type == "variable_declarator":
        return node.parent.child_by_field_name("name").text.decode() + "."
    return ""


def measure_typescript(text: str, path: str = "") -> list[Function]:
    """Every named function, its metrics from its own lines; `.tsx` read with the TSX grammar."""
    tree = _ts_parser(path.endswith(".tsx")).parse(text.encode("utf-8"))
    code = _tree_code_lines(tree.root_node, TS_COMMENTS)
    found: list[Function] = []

    def visit(node, prefix: str) -> None:
        for child in node.named_children:
            name = ts_binding(child)
            if name is None:
                visit(child, prefix + _ts_scope(child))
                continue
            own = _tree_own_lines(child, _is_ts_fn)
            found.append(Function(prefix + name, child.start_point[0] + 1, child.end_point[0] + 1,
                                  1 + _tree_decisions(child, _ts_weight, _is_ts_fn), len(own & code),
                                  _ts_parameters(child), own, _tree_own_error(child, _is_ts_fn),
                                  ts_test_name(child) is not None))
            visit(child, prefix + name + ".")

    visit(tree.root_node, "")
    return found


def ts_count(text: str, path: str = "") -> int:
    """The recall count, by TypeScript's own compiler through npx; Unmeasured where it cannot run."""
    if shutil.which("npx") is None:
        raise Unmeasured("npx is not installed, so TypeScript's compiler cannot count the file's functions")
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "count.js"
        script.write_text(TS_COUNT_JS, encoding="utf-8")
        name = Path(path).name or "file.ts"
        out = subprocess.run(["npx", "--yes", "-p", TS_RECALL, "-c", f"node {shlex.quote(str(script))} {shlex.quote(name)}"],
                             input=text, capture_output=True, text=True, check=False)
    if out.returncode != 0 or not out.stdout.strip().isdigit():
        raise Unmeasured(f"{TS_RECALL} could not count the file's functions (exit {out.returncode}): "
                         f"{(out.stdout + out.stderr).strip()[-200:]}")
    return int(out.stdout.strip())


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
LISTS_LICENSES = ("rust", "typescript")   # profiles whose audit lists the licenses itself, so no license_command


def load_profile(text: str) -> tuple[dict, list[Finding]]:
    import yaml
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return {}, [Finding("profile", PROFILE_FILE, 1, f"does not parse as YAML: {e}")]
    if not isinstance(data, dict):
        return {}, [Finding("profile", PROFILE_FILE, 1, "is not a mapping")]
    problems = [f"`{k}` must be a {t.__name__}" for k, t in REQUIRED.items() if not isinstance(data.get(k), t)]
    if data.get("profile") not in (None, *SUFFIXES):
        problems.append(f"profile {data.get('profile')!r} is not built here; this gate holds {', '.join(SUFFIXES)}")
    if isinstance(data.get("code"), list) and not data["code"]:
        problems.append("`code` names no path: a profile with an empty slot is not adoptable")
    needs = {"licenses_allowed": list} if data.get("profile") in LISTS_LICENSES else {"license_command": str, "licenses_allowed": list}
    if data.get("manifests") and not all(isinstance(data.get(k), t) for k, t in needs.items()):
        problems.append(f"manifests need {' and '.join(f'`{k}`' for k in needs)}")
    return data, [Finding("profile", PROFILE_FILE, 1, "; ".join(problems))] if problems else []


EXACT = r"\d+\.\d+\.\d+"
TS_PINNED = ("prettier", "eslint", "typescript")       # the tools the gate runs from the project's own copies
LOCKFILES = {"package-lock.json": "npm", "pnpm-lock.yaml": "pnpm", "yarn.lock": "yarn"}


def _package(read: Callable[[str], str | None]) -> dict | None:
    try:
        pkg = json.loads(read("package.json") or "")
    except json.JSONDecodeError:
        return None
    return pkg if isinstance(pkg, dict) else None


def ts_manager(read: Callable[[str], str | None]) -> str | None:
    """The package manager the lockfile names, `yarn1` for yarn 1 by its `packageManager`; None if none."""
    manager = next((m for f, m in LOCKFILES.items() if read(f) is not None), None)
    if manager == "yarn" and str((_package(read) or {}).get("packageManager", "")).startswith("yarn@1."):
        return "yarn1"
    return manager


def _ts_toolchain(read: Callable[[str], str | None]) -> list[Finding]:
    """A TypeScript project pins prettier, eslint and typescript exactly, with a lockfile; pnpm and yarn
    also name their exact version in `packageManager`, which corepack runs."""
    pkg = _package(read)
    if pkg is None:
        return [Finding("profile", "package.json", 1, "the TypeScript profile needs a package.json that parses")]
    deps = {**(pkg.get("dependencies") or {}), **(pkg.get("devDependencies") or {})}
    needs = [f"`{n}` at an exact version, not {deps.get(n)!r}" for n in TS_PINNED if not re.fullmatch(EXACT, str(deps.get(n, "")))]
    manager = ts_manager(read)
    if manager is None:
        needs.append("a lockfile: package-lock.json, pnpm-lock.yaml or yarn.lock")
    elif manager != "npm" and not re.fullmatch(rf"{manager.rstrip('1')}@{EXACT}(\+\S+)?", str(pkg.get("packageManager", ""))):
        needs.append(f"`packageManager` naming {manager.rstrip('1')} at an exact version")
    return [Finding("profile", "package.json", 1, "the TypeScript profile needs " + "; ".join(needs))] if needs else []


def toolchain_problems(profile: dict, read: Callable[[str], str | None]) -> list[Finding]:
    """What a stack's project must pin before its profile is adopted; Python's tools are the hooks'."""
    check = {"rust": _rust_toolchain, "typescript": _ts_toolchain}.get(profile.get("profile") or "python")
    return check(read) if check else []


def _rust_toolchain(read: Callable[[str], str | None]) -> list[Finding]:
    """A Rust project pins its toolchain, and with it rustfmt and clippy, to an exact version in
    rust-toolchain.toml."""
    import tomllib
    text, legacy = read("rust-toolchain.toml"), read("rust-toolchain")
    try:
        channel = (tomllib.loads(text).get("toolchain") or {}).get("channel") if text is not None \
            else (legacy or "").strip() or None
    except tomllib.TOMLDecodeError as e:
        channel = f"unreadable: {e}"
    if isinstance(channel, str) and re.fullmatch(r"\d+\.\d+\.\d+", channel):
        return []
    found = f"not {channel!r}" if channel else "and none names one"
    return [Finding("profile", "rust-toolchain.toml", 1, f"the Rust profile needs rust-toolchain.toml naming an exact "
                                                         f"toolchain (channel = \"1.99.0\"), {found}")]


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
    """A function its language marks a test, or a `test*` function in a test path."""
    return fn.test or (matches(path, profile.get("tests", [])) and re.split(r"\.|::", fn.name)[-1].startswith("test"))


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
        sup += [(place, f"line {n}: {name}") for name, p in SUPPRESSIONS.items() if p.search(row)]
        if GENERATED_MARKER.search(row) and not generated:
            gen.append((place, f"line {n}: a generated-code marker outside a generated path"))
    return tally("suppression", sup) + tally("generated-marker", gen)


# Each stack's (measurer, recall count), both given the file's text and path.
MEASURERS = {"python": (lambda text, path: measure_python(text), lambda text, path: def_count(text)),
             "rust": (lambda text, path: measure_rust(text), lambda text, path: fn_count(text)),
             "typescript": (measure_typescript, ts_count)}


def judge_file(path: str, text: str, lines: set[int], profile: dict) -> tuple[list[Finding], list[Function]]:
    """Recall first: a file the measurer under-reads proves nothing about its functions."""
    measure, count = MEASURERS[profile.get("profile") or "python"]
    try:
        functions, defined = measure(text, path), count(text, path)
    except SyntaxError as e:              # Python's parser refuses a file whole; tree-sitter marks errors in place
        return [Finding("recall", path, 1, f"Python cannot parse it: {e.msg} at line {e.lineno}")], []
    except ImportError as e:
        return [Finding("unmeasured", path, 1, f"the measurer's parser is not installed: {e}")], []
    except Unmeasured as e:
        return [Finding("unmeasured", path, 1, str(e))], []
    if len(functions) != defined:
        return [Finding("recall", path, 1, f"measured {len(functions)} functions of {defined} defined")], functions
    found: list[Finding] = []
    for fn in (f for f in functions if f.own_lines & lines):
        if fn.error_line:
            found.append(Finding("recall", f"{path}:{fn.name}", 1, f"its parser reads an error at line "
                                                                   f"{fn.error_line}, so its metrics cannot be trusted"))
        else:
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


def lcov_report(text: str) -> dict:
    """lcov's `SF:` and `DA:<line>,<hits>` in coverage.py's shape; a line reported twice, as generic code
    is, keeps its most hits."""
    hits: dict[str, dict[int, int]] = {}
    current: dict[int, int] | None = None
    for line in text.splitlines():
        if line.startswith("SF:"):
            current = hits.setdefault(line[3:], {})
        elif line.startswith("DA:") and current is not None:
            n, count = (int(x) for x in line[3:].split(",")[:2])
            current[n] = max(current.get(n, 0), count)
    return {"files": {path: {"executed_lines": sorted(n for n, c in lines.items() if c),
                             "missing_lines": sorted(n for n, c in lines.items() if not c)}
                      for path, lines in hits.items()}}


COVERAGE_READERS = {"python": json.loads, "rust": lcov_report, "typescript": lcov_report}


def pinned(run: Runner, tool: str) -> None:
    """A tool the Rust profile installs apart, at its pinned version, or the check is not made."""
    _, text = run(["cargo", tool.removeprefix("cargo-"), "--version"], None)
    if f"{tool} {RUST_PINS[tool]}" not in text:
        raise Unmeasured(f"{tool} {RUST_PINS[tool]} is pinned; found {text.strip()[:60] or 'none'}")


def run_coverage(profile: dict, run: Runner) -> dict:
    stack = profile.get("profile") or "python"
    if stack == "rust":
        pinned(run, "cargo-llvm-cov")
    code, text = run([], profile["coverage_command"])
    report = ROOT / profile["coverage_report"]
    if code != 0 or not report.is_file():
        raise Unmeasured(f"the coverage command failed (exit {code}) or wrote no {profile['coverage_report']}: "
                         f"{text.strip()[-200:]}")
    try:
        return COVERAGE_READERS[stack](report.read_text(encoding="utf-8"))
    except ValueError as e:                # a JSON or an lcov report that does not read
        raise Unmeasured(f"the coverage report {profile['coverage_report']} did not parse: {e}") from e


def placed(rule: str, rows: list[tuple[str, int, str]], touched: dict[str, set[int]],
           measured: dict[str, list[Function]]) -> list[Finding]:
    hits = [(f"{p}:{function_at(measured.get(p, []), n)}", f"line {n}: {msg}")
            for p, n, msg in rows if n in touched.get(p, set())]
    return tally(rule, hits)


FORMAT_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+\d+(?:,(\d+))? @@")


def diff_hunks(diff: str) -> list[tuple[str, int, list[str]]]:
    """A unified diff's hunks as (path, first old line, body), each body read to the header's counts,
    so a removed line that reads like a file header stays in its hunk."""
    hunks: list[tuple[str, int, list[str]]] = []
    path, old, new = None, 0, 0
    for line in diff.splitlines():
        if old > 0 or new > 0:
            hunks[-1][2].append(line)
            old -= line[:1] in ("-", " ", "")
            new -= line[:1] in ("+", " ", "")
        elif line.startswith("--- "):
            path = line[4:].removeprefix("a/").split("\t")[0]
        elif (m := FORMAT_HUNK.match(line)) and path:
            hunks.append((path, int(m.group(1)), []))
            old, new = int(m.group(2) or 1), int(m.group(3) or 1)
    return hunks


def formatter_lines(start: int, body: list[str]) -> list[int]:
    """The current file's lines one hunk changes: a line rewritten or removed
    at its own number; a run of lines only inserted once, against the line it precedes, or at the
    file's end its last line; a context line never."""
    found, n, inserted, removed = [], start, False, False
    for line in body:
        tag = line[:1]
        if tag == "-":
            found.append(n)
            n, inserted, removed = n + 1, False, True
        elif tag == "+":
            inserted = inserted or not removed
        elif tag != "\\":                      # context; `\ No newline at end of file` is no line
            found += [n] if inserted else []
            n, inserted, removed = n + 1, False, False
    return found + ([max(n - 1, 1)] if inserted else [])


def format_rows(diff: str) -> list[tuple[str, int, str]]:
    """`ruff format --diff`: the current file's lines the formatter would change."""
    return [(path, n, "not as ruff formats it") for path, start, body in diff_hunks(diff)
            for n in formatter_lines(start, body)]


RUSTFMT_HUNK = re.compile(r"^Diff in (.+):(\d+):$")


def rustfmt_rows(output: str) -> list[tuple[str, int, str]]:
    """`cargo fmt --check`: `Diff in <path>:<line>:` then a diff body with no `@@` header, its first line
    being <line>; read as `formatter_lines` reads ruff's hunks, so no context line counts."""
    hunks: list[tuple[str, int, list[str]]] = []
    for line in output.splitlines():
        m = RUSTFMT_HUNK.match(line)
        if m:
            hunks.append((_rel(m.group(1)), int(m.group(2)), []))
        elif hunks and line[:1] in (" ", "-", "+", "\\", ""):
            hunks[-1][2].append(line)
    return [(path, n, "not as rustfmt formats it") for path, start, body in hunks for n in formatter_lines(start, body)]


def clippy_rows(output: str) -> tuple[list[tuple[str, int, str]], list[tuple[str, int, str]]]:
    """`cargo clippy --message-format=json`: (lint rows, type rows), a warning a lint and an error the
    compiler's; the test build's repeat of a library lint counted once."""
    seen: set[tuple] = set()
    rows: dict[str, list[tuple[str, int, str]]] = {"warning": [], "error": []}
    for line in (l for l in output.splitlines() if l.startswith("{")):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            raise Unmeasured(f"clippy's report did not parse: {e}") from e
        msg = (record.get("message") or {}) if record.get("reason") == "compiler-message" else {}
        span = next((s for s in msg.get("spans", []) if s.get("is_primary")), None)
        if span is None or msg.get("level") not in rows:
            continue
        code = (msg.get("code") or {}).get("code") or msg["level"]
        row = (_rel(span["file_name"]), int(span["line_start"]), f"{code} {msg.get('message', '')}")
        if row not in seen:
            seen.add(row)
            rows[msg["level"]].append(row)
    return rows["warning"], rows["error"]


def run_rust_checkers(files: list[str], touched: dict[str, set[int]], measured: dict[str, list[Function]],
                      run: Runner, read: Callable | None = None) -> list[Finding]:
    """rustfmt, clippy and the compiler over the workspace, their findings kept to the changed lines."""
    code, fmt = run(["cargo", "fmt", "--check"], None)
    if code not in (0, 1):
        raise Unmeasured(f"cargo fmt could not check the workspace (exit {code}): {fmt.strip()[-200:]}")
    code, out = run(["cargo", "clippy", "--quiet", "--message-format=json", "--all-targets", "--", *CLIPPY_ALLOWS], None)
    if code != 0 and '"compiler-message"' not in out:
        raise Unmeasured(f"cargo clippy could not run (exit {code}): {out.strip()[-200:]}")
    lint, types = clippy_rows(out)
    return (placed("format", rustfmt_rows(fmt), touched, measured) + placed("lint", lint, touched, measured)
            + placed("types", types, touched, measured))


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
                 run: Runner, read: Callable | None = None) -> list[Finding]:
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


def run_audit(profile: dict, run: Runner, read: Callable | None = None) -> list[Finding]:
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


LICENSE_CODES = {"rejected", "unlicensed"}


def deny_findings(output: str) -> list[Finding]:
    """cargo-deny's JSON diagnostics: an advisory an `audit` finding, a license outside the policy a
    `license` finding, each at the crate its graph names."""
    found = []
    for line in (l for l in output.splitlines() if l.startswith("{")):
        fields = (json.loads(line).get("fields") or {}) if '"diagnostic"' in line else {}
        if fields.get("severity") != "error":
            continue
        krate = ((fields.get("graphs") or [{}])[0].get("Krate") or {})
        where = f"{krate.get('name', '?')} {krate.get('version', '')}".strip()
        if fields.get("code") in LICENSE_CODES:
            found.append(Finding("license", where, 1, f"{fields.get('message', '')}, outside licenses_allowed"))
        elif fields.get("advisory"):
            found.append(Finding("audit", where, 1, f"{fields['advisory'].get('id')}: {fields.get('message', '')}"))
    return found


def run_rust_audit(profile: dict, run: Runner, read: Callable | None = None) -> list[Finding]:
    """cargo-deny's advisories and licenses, its policy written from `licenses_allowed`, the profile's one
    home for it."""
    pinned(run, "cargo-deny")
    with tempfile.TemporaryDirectory() as tmp:
        config = Path(tmp) / "deny.toml"
        config.write_text(f"[licenses]\nallow = {json.dumps(profile.get('licenses_allowed', []))}\n", encoding="utf-8")
        code, text = run(["cargo", "deny", "--format", "json", "--config", str(config), "check", "advisories",
                          "licenses"], None)
    try:
        found = deny_findings(text)
    except json.JSONDecodeError as e:
        raise Unmeasured(f"cargo-deny's report did not parse: {e}") from e
    if code != 0 and not found:
        raise Unmeasured(f"cargo-deny could not check the crate graph (exit {code}): {text.strip()[-200:]}")
    return found


# The TypeScript profile's slots: the project's own pinned tools through npx.
ESLINT_OFF = json.dumps({"complexity": "off", "max-lines-per-function": "off", "max-params": "off"})
TSC_ERROR = re.compile(r"^(?P<path>[^\n(]+)\((?P<line>\d+),\d+\): error (?P<msg>TS\d+: .*)$")


def prettier_rows(path: str, text: str, formatted: str) -> list[tuple[str, int, str]]:
    """prettier names a file and no line, so the file is compared with prettier's output, three lines of
    context as ruff's diff carries, and read by `formatter_lines`."""
    diff = "\n".join(difflib.unified_diff(text.splitlines(), formatted.splitlines(), path, path, lineterm=""))
    return [(p, n, "not as prettier formats it") for p, start, body in diff_hunks(diff) for n in formatter_lines(start, body)]


def eslint_rows(output: str) -> list[tuple[str, int, str]]:
    """ESLint's JSON report, its last line; an ESLint that could not run writes none, and is unmeasured."""
    report = next((l for l in reversed(output.splitlines()) if l.startswith("[")), None)
    try:
        files = json.loads(report or "")
    except json.JSONDecodeError as e:
        raise Unmeasured(f"ESLint's report did not parse: {e}") from e
    return [(_rel(f["filePath"]), int(m["line"]), f"{m.get('ruleId') or 'parse'} {m.get('message', '')}")
            for f in files for m in f.get("messages", []) if m.get("line")]


def run_ts_checkers(files: list[str], touched: dict[str, set[int]], measured: dict[str, list[Function]],
                    run: Runner, read: Callable | None = None) -> list[Finding]:
    """prettier, ESLint and the compiler, the project's own copies, their findings kept to the changed lines."""
    fmt: list[tuple[str, int, str]] = []
    for path in files:
        code, formatted = run(["npx", "--no-install", "prettier", "--log-level", "error", path], None)
        if code != 0:
            raise Unmeasured(f"prettier could not format {path} (exit {code}): {formatted.strip()[-200:]}")
        fmt += prettier_rows(path, (read or (lambda p: None))(path) or "", formatted)
    _, lint = run(["npx", "--no-install", "eslint", "--format", "json", "--rule", ESLINT_OFF, *files], None)
    code, types = run(["npx", "--no-install", "tsc", "--noEmit", "--strict", "--pretty", "false"], None)
    type_rows = [(m["path"], int(m["line"]), m["msg"]) for m in map(TSC_ERROR.match, types.splitlines()) if m]
    if code != 0 and not type_rows:
        raise Unmeasured(f"tsc could not check the project (exit {code}): {types.strip()[-200:]}")
    return (placed("format", fmt, touched, measured) + placed("lint", eslint_rows(lint), touched, measured)
            + placed("types", type_rows, touched, measured))


def _json_lines(output: str) -> list[dict]:
    """The JSON objects a tool writes one a line, its warnings between them skipped."""
    out = []
    for line in (l for l in output.splitlines() if l.startswith("{")):
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _json_report(output: str) -> dict:
    """The one JSON object a tool writes, from its first line that opens one; warnings before it skipped."""
    lines = output.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("{")), None)
    try:
        report = json.loads("\n".join(lines[start:])) if start is not None else None
    except json.JSONDecodeError as e:
        raise Unmeasured(f"the report did not parse: {e}") from e
    if not isinstance(report, dict):
        raise Unmeasured(f"no JSON report: {output.strip()[-200:]}")
    return report


def _json_key(output: str, key: str) -> dict:
    """An audit's report, its `key` the proof it ran: an error report lacks it."""
    report = _json_report(output)
    if key not in report:
        raise Unmeasured(f"the report holds no `{key}`: {output.strip()[-200:]}")
    return report[key] or {}


def _advisory(a: dict) -> tuple[str, str]:
    """pnpm and yarn 1 write npm's old advisory record."""
    return a.get("module_name", "?"), f"{a.get('severity')}: {a.get('title')} ({a.get('github_advisory_id')})"


def _npm_advisories(output: str) -> list[tuple[str, str]]:
    """An advisory is a `via` record of the package it is in; a `via` that names a package is its dependent's."""
    return [(name, f"{x.get('severity')}: {x.get('title')} ({x.get('url')})")
            for name, v in _json_key(output, "vulnerabilities").items() for x in v.get("via", []) if isinstance(x, dict)]


def _yarn1_advisories(output: str) -> list[tuple[str, str]]:
    """yarn 1 ends every audit with its summary, the proof it ran."""
    rows = _json_lines(output)
    if not any(r.get("type") == "auditSummary" for r in rows):
        raise Unmeasured(f"yarn's audit wrote no summary: {output.strip()[-200:]}")
    return [_advisory(r["data"]["advisory"]) for r in rows if r.get("type") == "auditAdvisory"]


def _yarn_advisories(output: str) -> list[tuple[str, str]]:
    """yarn 2 and later write nothing on a clean audit, so its exit code is the proof it ran."""
    return [(r.get("value", "?"), f"{r['children'].get('Severity')}: {r['children'].get('Issue')}")
            for r in _json_lines(output) if isinstance(r.get("children"), dict) and "Issue" in r["children"]]


# (package, advisory) from each manager's audit, its format its own
ADVISORY_READERS: dict[str, Callable[[str], list[tuple[str, str]]]] = {
    "npm": _npm_advisories,
    "pnpm": lambda output: [_advisory(a) for a in _json_key(output, "advisories").values()],
    "yarn1": _yarn1_advisories,
    "yarn": _yarn_advisories,
}


def _npm_licenses(output: str, package: dict) -> list[tuple[str, str]]:
    found, stack = [], [_json_report(output)]
    while stack:
        node = stack.pop()
        for name, dep in (node.get("dependencies") or {}).items():
            licence = dep.get("license")
            found.append((f"{name}@{dep.get('version')}", licence.get("type", "") if isinstance(licence, dict) else str(licence or "")))
            stack.append(dep)
    return found


def _yarn_licenses(output: str, package: dict) -> list[tuple[str, str]]:
    """yarn 2 and later list every package's manifest, dev tools included: production is walked from
    `package.json`'s `dependencies`."""
    entries = {r["value"]: r["children"] for r in _json_lines(output) if isinstance(r.get("children"), dict)}
    names = set(package.get("dependencies") or {})
    root = next((c for v, c in entries.items() if "@workspace:" in v), {})
    todo = [d["locator"] for d in root.get("Dependencies", []) if d["descriptor"].rsplit("@", 1)[0] in names]
    found, seen = [], set()
    while todo:
        locator = todo.pop()
        if locator in seen or locator not in entries:
            continue
        seen.add(locator)
        found.append((locator, str((entries[locator].get("Manifest") or {}).get("License") or "")))
        todo += [d["locator"] for d in entries[locator].get("Dependencies", [])]
    return found


def _pnpm_licenses(output: str, package: dict) -> list[tuple[str, str]]:
    return [(f"{p['name']}@{','.join(p.get('versions', []))}", licence)
            for licence, pkgs in _json_report(output).items() for p in pkgs]


def _yarn1_licenses(output: str, package: dict) -> list[tuple[str, str]]:
    table = next((r["data"] for r in _json_lines(output) if r.get("type") == "table"), {"head": [], "body": []})
    col = {h: i for i, h in enumerate(table["head"])}
    return [(f"{r[col['Name']]}@{r[col['Version']]}", r[col["License"]]) for r in table["body"]] if col else []


# (package, license) for each production dependency, from each manager's listing and package.json
LICENSE_READERS: dict[str, Callable[[str, dict], list[tuple[str, str]]]] = {
    "npm": _npm_licenses, "pnpm": _pnpm_licenses, "yarn1": _yarn1_licenses, "yarn": _yarn_licenses}


def license_ok(expression: str, allowed: list[str]) -> bool:
    """An SPDX expression passes when one `OR` alternative's licenses are all allowed."""
    options = expression.replace("(", "").replace(")", "").split(" OR ")
    return any(all(part.strip() in allowed for part in option.split(" AND ")) for option in options)


TS_AUDIT = {"npm": ["npm", "audit", "--json"], "pnpm": ["corepack", "pnpm", "audit", "--json"],
            "yarn1": ["corepack", "yarn", "audit", "--json"],
            "yarn": ["corepack", "yarn", "npm", "audit", "--json", "--all", "--recursive"]}
TS_LICENSES = {"npm": ["npm", "ls", "--all", "--json", "--long", "--omit=dev"],
               "pnpm": ["corepack", "pnpm", "licenses", "list", "--json", "--prod"],
               "yarn1": ["corepack", "yarn", "licenses", "list", "--json", "--prod"],
               "yarn": ["corepack", "yarn", "info", "--all", "--recursive", "--json", "--manifest"]}


def run_ts_audit(profile: dict, run: Runner, read: Callable | None = None) -> list[Finding]:
    """Every dependency's advisories, and each production dependency's license against `licenses_allowed`,
    by the manager the lockfile names."""
    read = read or (lambda p: None)
    manager = ts_manager(read)
    if manager is None:
        raise Unmeasured("no lockfile names the package manager")
    code, audit = run(TS_AUDIT[manager], None)
    by_package: dict[str, list[str]] = {}
    for name, advisory in ADVISORY_READERS[manager](audit):
        by_package.setdefault(name, []).append(advisory)
    if code != 0 and not by_package:       # every manager exits non-zero on an advisory, and only then
        raise Unmeasured(f"the {manager} audit could not run (exit {code}): {audit.strip()[-200:]}")
    found = [Finding("audit", name, len(items), "; ".join(items)[:300]) for name, items in by_package.items()]
    code, listing = run(TS_LICENSES[manager], None)
    if code != 0:
        raise Unmeasured(f"the {manager} license listing could not run (exit {code}): {listing.strip()[-200:]}")
    allowed = profile.get("licenses_allowed", [])
    listed = dict(LICENSE_READERS[manager](listing, _package(read) or {}))
    return found + [Finding("license", name, 1, f"license {licence!r} is not in licenses_allowed")
                    for name, licence in listed.items() if not license_ok(licence, allowed)]


CHECKERS = {"python": ("ruff and mypy", run_checkers), "rust": ("cargo fmt and clippy", run_rust_checkers),
            "typescript": ("prettier, ESLint and tsc", run_ts_checkers)}
AUDITS = {"python": ("pip-audit and the license command", run_audit), "rust": ("cargo-deny", run_rust_audit),
          "typescript": ("the package manager's audit and license listing", run_ts_audit)}


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
    """(changed code files of the profile's language judged, of them the production ones)."""
    globs, suffix = profile["code"] + profile["tests"], SUFFIXES[profile.get("profile") or "python"]
    judged = sorted(p for p in change.touched if p.endswith(suffix) and matches(p, globs)
                    and not matches(p, profile.get("generated", [])) and change.read_new(p) is not None)
    return judged, [p for p in judged if matches(p, profile["code"]) and not matches(p, profile["tests"])]


def judge_change(change: Change, profile: dict, run: Runner) -> list[Finding]:
    stack = profile.get("profile") or "python"
    judged, prod = code_files(change, profile)
    measured: dict[str, list[Function]] = {}
    found: list[Finding] = []
    for path in judged:
        here, measured[path] = judge_file(path, change.read_new(path) or "", change.touched[path], profile)
        found += here
    if judged:
        tool, checkers = CHECKERS[stack]
        found += attempt(tool, lambda: checkers(judged, change.touched, measured, run, change.read_new))
    if prod:
        everything = [p for p in change.files if p.endswith(SUFFIXES[stack]) and matches(p, profile["code"])]
        found += attempt("jscpd", lambda: judge_clones(run_clones(everything, run), change.touched, set(prod), measured))
        found += attempt("coverage", lambda: judge_coverage(run_coverage(profile, run), change.touched, set(prod), measured))
    if change.is_range or any(m in change.touched for m in profile.get("manifests", [])):
        tool, audit = AUDITS[stack]
        found += attempt(tool, lambda: audit(profile, run, change.read_new))
    return found


def suggested_row(f: Finding) -> str:
    """One row of the log; a `|` in a tool's message, which would split the row, becomes a `/`. Its own
    text is ASCII, since the log is markdown the writing gate judges at every commit."""
    today = datetime.date.today().isoformat()
    return f"| {today} | none | `{f.where.replace('|', '/')}` | {f.rule} {f.value} - {f.detail.replace('|', '/')} | gate | none |  |"


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
    problems += toolchain_problems(profile, lambda rel: (ROOT / rel).read_text(encoding="utf-8")
                                   if (ROOT / rel).is_file() else None)
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
        if argv[:1] == ["cargo"]:                      # `cargo fmt`, `cargo deny --version`, …
            key = argv[1] + (" --version" if "--version" in argv else "")
        elif argv[:1] == ["npx"]:                      # `npx --no-install prettier`, jscpd
            key = argv[2]
        elif argv[:1] in (["npm"], ["corepack"]):      # `npm audit`, `corepack pnpm licenses`, …
            key = " ".join(argv[1:3] if argv[0] == "corepack" else argv[:2])
        else:
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


RUST_HARD = r'''//! Crate docs mention fn fake() {}
use std::fmt;

/* outer /* nested fn hidden() {} */ still comment fn gone() */
const RAW: &str = r#"fn not_a_function() { "quoted" }"#;
const BYTES: &[u8] = br"fn nor_this()";
const QUOTE: char = '"';
const BRACE: char = '{';

pub struct Wrapper<'a> {
    inner: &'a str,
}

impl<'a> Wrapper<'a> {
    /// A doc comment: fn in docs is not code.
    pub fn new(inner: &'a str) -> Self {
        Wrapper { inner }
    }

    pub fn classify(&self, n: i32) -> &'static str {
        // a comment line is not code
        if n < 0 && self.inner.is_empty() {
            "negative"
        } else if n == 0 || n == 1 {
            "small"
        } else {
            match n {
                2 => "two",
                x if x % 2 == 0 => "even",
                _ => "odd",
            }
        }
    }
}

pub trait Shape {
    fn area(&self) -> f64;
    fn describe(&self) -> String {
        format!("area {}", self.area())
    }
}

fn outer(values: &[i32]) -> i32 {
    fn inner(v: i32) -> i32 {
        if v > 0 { v } else { 0 }
    }
    let total = values.iter().map(|v| if *v > 10 { inner(*v) } else { 0 }).sum::<i32>();
    for v in values {
        while total > *v {
            break;
        }
    }
    total
}

extern "C" {
    fn abs(input: i32) -> i32;
}

async fn fetch<'b>(label: &'b str, retries: u8) -> Result<&'b str, ()> {
    'outer: loop {
        if retries == 0 {
            break 'outer;
        }
        return Ok(label);
    }
    Err(())
}
'''   # Rust's hard cases: lifetimes, raw strings, nested comments, a quote character

BEVY = r'''use bevy::prelude::*;

#[derive(Component)]
struct Velocity(Vec3);

fn movement(
    time: Res<Time>,
    mut query: Query<(&mut Transform, &Velocity), With<Player>>,
    keys: Res<ButtonInput<KeyCode>>,
    mut commands: Commands,
    mut events: EventWriter<Moved>,
    settings: Option<Res<Settings>>,
    mut local: Local<u32>,
    gizmos: Gizmos,
) {
    for (mut transform, velocity) in &mut query {
        transform.translation += velocity.0 * time.delta_secs();
    }
}

fn helper(a: f32, b: f32, c: f32, d: f32, e: f32, f: f32, time: Res<Time>) -> f32 {
    a + b + c + d + e + f + time.delta_secs()
}

fn scoped(time: bevy::prelude::Res<Time>, q: Query<'_, '_, &Transform>, x: u8) {}
'''
RUST_PROFILE = dict(PROFILE, profile="rust", code=["src/**/*.rs"], tests=["tests/**/*.rs"])


def _t_rust_measurer(check) -> None:
    fns = {f.name: f for f in measure_rust(RUST_HARD)}
    check("the Rust measurer finds every fn: methods, a trait's signature and default, a nested and an extern fn",
          set(fns) == {"Wrapper::new", "Wrapper::classify", "Shape::area", "Shape::describe", "outer", "outer::inner",
                       "abs", "fetch"}, str(sorted(fns)))
    check("`if`, `else if`, `&&`, `||`, each match arm and a guard count: classify is 9",
          fns["Wrapper::classify"].complexity == 9, str(fns["Wrapper::classify"]))
    check("a closure's `if` counts to its fn, a nested fn's does not: outer 4, outer::inner 2",
          fns["outer"].complexity == 4 and fns["outer::inner"].complexity == 2, str(fns["outer"]))
    check("a `loop` with no condition is no decision: fetch is 2", fns["fetch"].complexity == 2, str(fns["fetch"]))
    chain = measure_rust("fn chain(x: Option<u8>, y: Option<u8>) -> u8 {\n"
                         "    if let Some(a) = x && let Some(b) = y { a + b } else { 0 }\n}\n")[0]
    check("each `&&` of a let chain counts: chain is 3", chain.complexity == 3, str(chain))
    check("a comment line and a nested fn's lines are not code: classify 13, outer 9",
          fns["Wrapper::classify"].code_lines == 13 and fns["outer"].code_lines == 9, str(fns["outer"]))
    check("`self` is a parameter", fns["Wrapper::classify"].parameters == 2
          and getattr(fns.get("Shape::area"), "parameters", None) == 1)
    check("the recall lexer counts the parser's 8 fns past raw strings, nested comments, a quote and lifetimes",
          fn_count(RUST_HARD) == 8, str(fn_count(RUST_HARD)))
    cases = {'r#"fn a()"#': 0, "/* /* fn a() */ fn b() */": 0, "let c = '\"'; fn real() {}": 1,
             "fn f<'a>(x: &'a str) {}": 1, "let f: fn(u8) -> u8 = g;": 0, "fn r#type() {}": 1,
             "fn /* c */ named() {}": 1, 'let s = "fn x()"; fn y() {}': 1, "use x::r#fn as y;": 0,
             r'let p = r"C:\"; fn real() {}': 1}
    got = {s: fn_count(s) for s in cases}
    check("the lexer tells strings, comments, a quote, a lifetime, a pointer type and a raw name apart", got == cases, str(got))
    bevy = {f.name: f.parameters for f in measure_rust(BEVY)}
    check("a Bevy system parameter is not counted, an `Option` of one and a path to one included",
          bevy == {"movement": 0, "helper": 6, "scoped": 1}, str(bevy))


def _t_rust_judge(check) -> None:
    global _rust_parser
    found, _ = judge_file("src/game.rs", BEVY, set(range(1, 30)), RUST_PROFILE)
    check("a parameter that is no Bevy system parameter still counts against 5",
          [(f.rule, f.where) for f in found] == [("parameters", "src/game.rs:helper")], str(found))
    found, _ = judge_file("src/m.rs", "macro_rules! m { () => { fn hidden() {} } }\nfn shown() {}\n", {1, 2}, RUST_PROFILE)
    check("a fn inside a macro's body, which no parser sees, is a recall finding", _rules(found) == {"recall"}, str(found))
    app = "fn main() {\n    app.add_plugins((A, #[cfg(x)] B));\n}\n\nfn system(a: u8) {\n    if a > 1 {}\n}\n"
    errors = {f.name: f.error_line for f in measure_rust(app)}
    check("a parse error is the fn's that holds it: main reads one at line 2, system none",
          errors == {"main": 2, "system": 0}, str(errors))
    found, _ = judge_file("src/main.rs", app, {2}, RUST_PROFILE)
    check("a touched fn the parser read with an error is a recall finding at that fn",
          [(f.rule, f.where) for f in found] == [("recall", "src/main.rs:main")], str(found))
    found, _ = judge_file("src/main.rs", app, {6}, RUST_PROFILE)
    check("the same file's other fns are measured as usual", not found, str(found))
    nested = {f.name: f.error_line for f in measure_rust("fn outer() {\n    fn inner() { let x = ; }\n    inner()\n}\n")}
    check("an error in a nested fn is not its parent's", nested == {"outer": 0, "outer::inner": 2}, str(nested))
    found, _ = judge_file("src/h.rs", RUST_HARD, set(range(1, 70)), RUST_PROFILE)
    check("a Rust file read in full, its fns within the limits, passes", not found, str(found))
    real = _rust_parser
    try:
        _rust_parser = lambda: (_ for _ in ()).throw(ImportError("no tree_sitter"))   # noqa: E731  — the parser absent
        found, _ = judge_file("src/h.rs", RUST_HARD, {1}, RUST_PROFILE)
        check("a parser that is not installed is an unmeasured finding, never a pass", _rules(found) == {"unmeasured"}, str(found))
    finally:
        _rust_parser = real


# The Rust tools' own output, captured from a scratch crate at S27.
RUSTFMT_OUT = ("Diff in src/lib.rs:1:\n pub fn classify(n: i32) -> &'static str {\n"
               "-    if n < 0 { \"negative\" } else { \"positive\" }\n+    if n < 0 {\n+        \"negative\"\n"
               "+    } else {\n+        \"positive\"\n+    }\n }\n \n pub fn shout(s: &str) -> String {\n"
               "Diff in src/lib.rs:6:\n-   let x = s.to_uppercase();\n+    let x = s.to_uppercase();\n     return x;\n }\n \n")


def _clippy(level: str, code: str | None, line: int, primary: bool = True) -> str:
    spans = [{"file_name": "src/lib.rs", "line_start": line, "is_primary": primary}]
    return json.dumps({"reason": "compiler-message", "message": {"level": level, "message": "m",
                                                                 "code": {"code": code} if code else None, "spans": spans}})


CLIPPY_OUT = "\n".join([_clippy("warning", "clippy::needless_return", 7), _clippy("warning", "clippy::needless_return", 7),
                        _clippy("error", "E0308", 3), _clippy("warning", None, 0, primary=False),
                        _clippy("note", None, 4), "   Compiling probe v0.1.0", '{"reason": "build-finished"}'])
LCOV_OUT = ("SF:/abs/src/lib.rs\nDA:1,1\nDA:2,3\nDA:2,0\nDA:5,0\nLF:3\nLH:2\nend_of_record\n"
            "SF:/abs/src/other.rs\nDA:9,0\nend_of_record\n")


def _deny(code: str, crate: str, advisory: str | None = None, severity: str = "error") -> str:
    fields = {"severity": severity, "code": code, "message": f"{code} message",
              "graphs": [{"Krate": {"name": crate, "version": "1.0.0"}}], **({"advisory": {"id": advisory}} if advisory else {})}
    return json.dumps({"type": "diagnostic", "fields": fields})


DENY_OUT = "\n".join([_deny("rejected", "probe"), _deny("vulnerability", "smallvec", "RUSTSEC-2021-0003"),
                      _deny("unmaintained", "old", "RUSTSEC-2020-0001", severity="warning"),
                      '{"type": "summary", "fields": {}}'])
RUST_SLOTS = dict(RUST_PROFILE, manifests=["Cargo.toml", "Cargo.lock"], licenses_allowed=["MIT"],
                  coverage_command="cargo llvm-cov --lcov --output-path lcov.info", coverage_report="lcov.info")


def _t_rust_readers(check) -> None:
    rows = [(p, n) for p, n, _ in rustfmt_rows(RUSTFMT_OUT)]
    check("rustfmt's hunks count only what it changes, from the line its header names",
          rows == [("src/lib.rs", 2), ("src/lib.rs", 6)], str(rows))
    lint, types = clippy_rows(CLIPPY_OUT)
    check("a clippy warning is a lint row, its test build's repeat counted once",
          [(p, n) for p, n, _ in lint] == [("src/lib.rs", 7)], str(lint))
    check("a compiler error is a type row; a note, a span-less summary and cargo's progress are none",
          [(p, n) for p, n, _ in types] == [("src/lib.rs", 3)], str(types))
    report = lcov_report(LCOV_OUT)["files"]
    check("lcov reads as executed and missing lines, a line reported twice keeping its most hits",
          report["/abs/src/lib.rs"] == {"executed_lines": [1, 2], "missing_lines": [5]}
          and report["/abs/src/other.rs"]["missing_lines"] == [9], str(report))
    found = deny_findings(DENY_OUT)
    check("cargo-deny's rejected license and advisory are findings at their crates; a warning is none",
          [(f.rule, f.where) for f in found] == [("license", "probe 1.0.0"), ("audit", "smallvec 1.0.0")], str(found))
    tests = {f.name: f.test for f in measure_rust("#[test]\nfn a() {}\n#[tokio::test]\n// why\nasync fn b() {}\n"
                                                 "#[cfg(test)]\nfn c() {}\n#[cfg(test)]\nmod tests {\n    fn helper() {}\n}\n")}
    check("`#[test]` and `#[tokio::test]` mark test functions, past a comment; `#[cfg(test)]` marks none",
          tests == {"a": True, "b": True, "c": False, "tests::helper": False}, str(tests))


def _t_rust_profile(check) -> None:
    import yaml
    check("a Rust profile loads, its manifests needing a license list and no license command",
          not load_profile(yaml.safe_dump(RUST_SLOTS))[1], str(load_profile(yaml.safe_dump(RUST_SLOTS))[1]))
    check("a Rust profile's manifests without `licenses_allowed` are a finding",
          _rules(load_profile(yaml.safe_dump({k: v for k, v in RUST_SLOTS.items() if k != "licenses_allowed"}))[1]) == {"profile"})
    files = {"rust-toolchain.toml": '[toolchain]\nchannel = "1.99.0"\n'}
    check("rust-toolchain.toml naming an exact version passes", not toolchain_problems(RUST_SLOTS, files.get))
    check("the legacy rust-toolchain file naming one passes", not toolchain_problems(RUST_SLOTS, {"rust-toolchain": "1.99.0\n"}.get))
    for label, read in (("a channel of `stable`", {"rust-toolchain.toml": '[toolchain]\nchannel = "stable"\n'}.get),
                        ("no toolchain file", {}.get), ("a toolchain file that does not parse", {"rust-toolchain.toml": "[x"}.get)):
        check(f"{label} is a profile finding", _rules(toolchain_problems(RUST_SLOTS, read)) == {"profile"})
    check("a Python profile needs no toolchain file", not toolchain_problems(PROFILE, {}.get))
    sup = judge_markers("src/a.rs", "#[allow(clippy::needless_return)]\nfn f() {}\n#[allow(dead_code)]\nfn g() {}\n",
                        {1, 3}, measure_rust("fn f() {}\nfn g() {}\n"), False)
    check("an `#[allow(clippy::…)]` on a changed line is a suppression; `#[allow(dead_code)]` is not",
          [f.rule for f in sup] == ["suppression"] and sup[0].value == 1, str(sup))
    check("Cargo.lock is a new dependency and build.rs a gate change",
          matches("Cargo.lock", TRIGGER_PATHS["a new dependency"]) and matches("build.rs", TRIGGER_PATHS["a gate or CI change"]))


def _judged(ch: Change, profile: dict, run: _Run) -> list[Finding]:
    """judge_change, a crash read as a finding so the fixture that asked fails, not the group."""
    try:
        return judge_change(ch, profile, run)
    except Exception as e:   # noqa: BLE001  — any crash is the fixture's failure
        return [Finding("crash", "", 0, f"{type(e).__name__}: {e}")]


def _t_rust_gate(check) -> None:
    ch = _change({"src/lib.rs": "fn classify() {}\n\nfn shout() {\n    let x = 1;\n    x\n}\n", "Cargo.lock": "x\n"},
                 {"src/lib.rs": {2, 6, 7}, "Cargo.lock": {1}})
    run = _Run({"fmt": (1, RUSTFMT_OUT), "clippy": (0, CLIPPY_OUT), "deny --version": (0, "cargo-deny 0.20.2"),
                "deny": (2, DENY_OUT), "llvm-cov --version": (0, "cargo-llvm-cov 0.9.1")})
    found = _judged(ch, RUST_SLOTS, run)
    check("the Rust slots report format, lint, types, audit and license findings on the change",
          {"format", "lint", "audit", "license"} <= _rules(found) and "fmt" in run.calls and "clippy" in run.calls, str(found))
    run = _Run({"fmt": (0, ""), "clippy": (0, ""), "deny --version": (0, "cargo-deny 0.19.0"), "deny": (0, "")})
    found = _judged(ch, RUST_SLOTS, run)
    check("a cargo-deny at another version than the pin is unmeasured, never run",
          any(f.rule == "unmeasured" and "0.20.2" in f.detail for f in found) and "deny" not in run.calls, str(found))
    test_file = _change({"tests/t.rs": "fn f() {}\n"}, {"tests/t.rs": {1}})   # judged, so no clone or coverage run
    for label, outputs in (("cargo fmt", {"fmt": (101, "error: no Cargo.toml"), "clippy": (0, "")}),
                           ("cargo clippy", {"fmt": (0, ""), "clippy": (101, "error: could not find Cargo.toml")})):
        found = _judged(test_file, RUST_SLOTS, _Run(outputs))
        check(f"{label} that cannot run is unmeasured, never a pass", _rules(found) == {"unmeasured"}, str(found))
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "lcov.info").write_text(LCOV_OUT, encoding="utf-8")
        prof = dict(RUST_SLOTS, coverage_report=str(Path(tmp) / "lcov.info"))
        try:
            got = run_coverage(prof, _Run({"llvm-cov --version": (0, "cargo-llvm-cov 0.9.1")}))["files"]
        except Unmeasured as e:
            got = {"unmeasured": str(e)}
        check("the Rust profile's coverage report is read as lcov", got.get("/abs/src/lib.rs", {}).get("missing_lines") == [5], str(got))
        (Path(tmp) / "lcov.info").write_text("{not lcov", encoding="utf-8")
        try:
            found = attempt("coverage", lambda: run_coverage(dict(prof, profile="python"), _Run()))
        except Exception as e:   # noqa: BLE001  — a crash is this fixture's failure
            found = [Finding("crash", "", 0, f"{type(e).__name__}: {e}")]
        check("a coverage report that does not parse is unmeasured, never a crash", _rules(found) == {"unmeasured"}, str(found))
    long_test = "#[test]\nfn t() {\n" + "    let a = 1;\n" * 70 + "}\n"
    found, _ = judge_file("src/lib.rs", long_test, set(range(1, 80)), RUST_SLOTS)
    check("a `#[test]` fn in src/ takes the test limits: 72 lines pass", not found, str(found))


TS_HARD = r'''// fn in a comment: function fake() {}
const template = `function notReal() { ${1 + 1} }`;
const re = /function\s+x\(\)/g;

export class ZodLike<T extends { id: string }> {
  private items: T[] = [];
  constructor(private readonly name: string) {}

  /** A doc comment */
  parse(input: unknown, strict = false): T | undefined {
    if (typeof input !== "object" || input === null) {
      return undefined;
    } else if (strict && !("id" in input)) {
      throw new Error("no id");
    }
    switch (this.name) {
      case "a":
        return input as T;
      case "b":
        return undefined;
      default:
        break;
    }
    try {
      return this.items.find((item) => item.id === (input as T).id || !strict) ?? undefined;
    } catch {
      // a comment line is not code
      return undefined;
    }
  }

  get count(): number {
    return this.items.length;
  }

  onEvent = (e: Event): void => {
    const nested = (x: number) => (x > 1 ? x : 0);
    nested(1);
  };
}

export function outer(this: Window, values: number[]): number {
  let total = 0;
  for (const v of values) {
    while (total < v) {
      total ||= 1;
      total += 1;
    }
  }
  return total;
}

export const arrow = async <T,>(a: T, b?: T, ...rest: T[]): Promise<T> => a ?? b ?? rest[0];
const handlers = { start() { return 1; }, stop: function () { return 2; } };
export default function () { return handlers; }
function overload(a: string): string;
function overload(a: number): number;
function overload(a: unknown) { return a; }
'''   # TypeScript's hard cases: a method with a return type, a bare `catch`
TS_PROFILE = dict(PROFILE, profile="typescript", code=["src/**/*.ts"], tests=["tests/**/*.ts"])


def _t_ts_measurer(check) -> None:
    blank = Function("absent", 0, 0, 0, 0, 0, frozenset())
    measured = {f.name: f for f in measure_typescript(TS_HARD, "src/hard.ts")}
    fns = collections.defaultdict(lambda: blank, measured)   # a renamed function fails its check, not the group
    check("the named functions are measured: methods, a constructor, an accessor, field, variable, object and default "
          "functions, one overload's body; a comment, a template and a regex hold none",
          set(measured) == {"ZodLike.constructor", "ZodLike.parse", "ZodLike.count", "ZodLike.onEvent", "ZodLike.onEvent.nested",
                       "outer", "arrow", "handlers.start", "handlers.stop", "default", "overload"}, str(sorted(measured)))
    check("a method with a return type and a bare `catch` is measured: `if`, `||`, `else if`, `&&`, each `case`, the "
          "`catch`, `??` and an inline callback's `||` make parse 10", fns["ZodLike.parse"].complexity == 10,
          str(fns["ZodLike.parse"]))
    check("a named arrow inside another is its own: onEvent 1, onEvent.nested 2",
          fns["ZodLike.onEvent"].complexity == 1 and fns["ZodLike.onEvent.nested"].complexity == 2, str(fns["ZodLike.onEvent"]))
    check("`for...of`, `while` and `||=` count: outer 4", fns["outer"].complexity == 4, str(fns["outer"]))
    check("a comment line and a nested function's lines are not code: parse 20, onEvent 3",
          fns["ZodLike.parse"].code_lines == 20 and fns["ZodLike.onEvent"].code_lines == 3, str(fns["ZodLike.parse"]))
    check("a `this` annotation is no parameter; an optional and a rest parameter are",
          fns["outer"].parameters == 1 and fns["arrow"].parameters == 3, str((fns["outer"], fns["arrow"])))
    tsx = "export const App = () => <div onClick={() => go()}>{items.map((i) => <li key={i}>{i}</li>)}</div>;\n"
    check("a `.tsx` file is read with the TSX grammar", [f.name for f in measure_typescript(tsx, "src/App.tsx")] == ["App"])
    bad = {f.name: f.error_line for f in measure_typescript("function ok() { return 1; }\nfunction broken() {\n  const x = ;\n}\n")}
    check("a parse error is its function's alone", bad == {"ok": 0, "broken": 3}, str(bad))


def _t_ts_judge(check) -> None:
    real = MEASURERS["typescript"]
    try:
        for label, count, rule in (("the compiler's count equal to the measurer's passes recall", lambda t, p: 11, set()),
                                   ("a count that differs is a recall finding", lambda t, p: 12, {"recall"})):
            MEASURERS["typescript"] = (real[0], count)
            found, _ = judge_file("src/hard.ts", TS_HARD, {1}, TS_PROFILE)
            check(label, _rules(found) == rule, str(found))

        def missing(text: str, path: str) -> int:
            raise Unmeasured("npx is not installed")
        MEASURERS["typescript"] = (real[0], missing)
        found, _ = judge_file("src/hard.ts", TS_HARD, {1}, TS_PROFILE)
        check("a compiler that cannot run is an unmeasured finding, never a pass", _rules(found) == {"unmeasured"}, str(found))
        MEASURERS["typescript"] = (real[0], lambda t, p: 11)
        found, _ = judge_file("src/hard.ts", TS_HARD.replace("x > 1 ? x : 0", "x > 1 ? x : 0 && a && b && c && d && e && f "
                                                             "&& g && h && i && j && k && l && m && n"), {37}, TS_PROFILE)
        check("a named arrow over the complexity limit is a finding at its own name",
              [(f.rule, f.where) for f in found] == [("complexity", "src/hard.ts:ZodLike.onEvent.nested")], str(found))
    finally:
        MEASURERS["typescript"] = real


TS_TESTS_SRC = '''describe("math", () => {
  it("adds", () => {
    expect(add(1, 2)).toBe(3);
  });
  test.each([{ a: 1, b: 2 }])("adds %i", ({ a, b }) => {
    expect(a < b || a === b).toBe(true);
  });
  it.only(`skips`, async () => {});
  const helper = () => 1;
  [1].map((x) => x);
});
'''


def _t_ts_tests(check) -> None:
    fns = {f.name: f for f in measure_typescript(TS_TESTS_SRC, "tests/math.test.ts")}
    check("a callback passed to `it` or `test`, through `.each` and `.only`, is a test function named by its title; "
          "`describe`'s and `map`'s count to their callers",
          {n: f.test for n, f in fns.items()} == {"it adds": True, "test adds %i": True, "it skips": True, "helper": False},
          str({n: f.test for n, f in fns.items()}))
    check("a test callback's decisions are its own: `test adds %i` is 2",
          fns.get("test adds %i", Function("", 0, 0, 0, 0, 0, frozenset())).complexity == 2, str(fns.get("test adds %i")))
    long_test = 'it("is long", () => {\n' + "  expect(1).toBe(1);\n" * 70 + "});\n"
    real = MEASURERS["typescript"]
    try:
        MEASURERS["typescript"] = (real[0], lambda t, p: 1)
        found, _ = judge_file("src/a.ts", long_test, set(range(1, 72)), TS_PROFILE)
    finally:
        MEASURERS["typescript"] = real
    check("a test callback in src/ takes the test limits: 72 lines pass", not found, str(found))


TS_SLOTS = dict(TS_PROFILE, manifests=["package.json", "package-lock.json"], licenses_allowed=["MIT"],
                coverage_command="npx vitest run --coverage", coverage_report="coverage/lcov.info")
TS_PACKAGE = {"name": "probe", "version": "0.1.0", "license": "UNLICENSED", "dependencies": {"lodash": "4.17.20"},
              "devDependencies": {"is-number": "7.0.0", "prettier": "3.9.10", "eslint": "10.13.0", "typescript": "5.9.3"}}


def _ts_files(lockfile: str, manager: str | None = None, **package) -> Callable[[str], str | None]:
    return {"package.json": json.dumps(dict(TS_PACKAGE, **package, **({"packageManager": manager} if manager else {}))),
            lockfile: "x\n"}.get


def _t_ts_profile(check) -> None:
    import yaml
    check("a TypeScript profile loads, its manifests needing a license list and no license command",
          not load_profile(yaml.safe_dump(TS_SLOTS))[1], str(load_profile(yaml.safe_dump(TS_SLOTS))[1]))
    check("package-lock.json and exact pins pass", not toolchain_problems(TS_SLOTS, _ts_files("package-lock.json")))
    check("pnpm and yarn at an exact `packageManager` pass",
          not toolchain_problems(TS_SLOTS, _ts_files("pnpm-lock.yaml", "pnpm@12.15.0"))
          and not toolchain_problems(TS_SLOTS, _ts_files("yarn.lock", "yarn@1.22.22")))
    for label, read in (("a caret range on prettier", _ts_files("package-lock.json", devDependencies={"prettier": "^3.9.10"})),
                        ("no lockfile", {"package.json": json.dumps(TS_PACKAGE)}.get),
                        ("pnpm with no `packageManager`", _ts_files("pnpm-lock.yaml")),
                        ("yarn at `yarn@4` alone", _ts_files("yarn.lock", "yarn@4")),
                        ("a package.json that does not parse", {"package.json": "{", "package-lock.json": "x"}.get)):
        check(f"{label} is a profile finding", _rules(toolchain_problems(TS_SLOTS, read)) == {"profile"})
    managers = [ts_manager(_ts_files(f, m)) for f, m in (("package-lock.json", None), ("pnpm-lock.yaml", "pnpm@12.15.0"),
                                                         ("yarn.lock", "yarn@1.22.22"), ("yarn.lock", "yarn@4.18.1"))]
    check("the lockfile names the manager, and yarn 1 is told from yarn 2 and later by `packageManager`",
          managers == ["npm", "pnpm", "yarn1", "yarn"], str(managers))
    sup = judge_markers("src/a.ts", "// eslint-disable-next-line\nconst a = 1;\n// @ts-expect-error\nconst b: number = '';\n"
                        "/* v8 ignore next */\nconst c = 1;\n// eslint is fine\n", {1, 3, 5, 7}, [], False)
    check("`eslint-disable`, `@ts-expect-error` and `v8 ignore` on changed lines are suppressions; a plain comment is not",
          [f.rule for f in sup] == ["suppression"] and sup[0].value == 3, str(sup))
    check("a lockfile is a new dependency and tsconfig.json a gate change",
          matches("pnpm-lock.yaml", TRIGGER_PATHS["a new dependency"]) and matches("tsconfig.json", TRIGGER_PATHS["a gate or CI change"]))


# The TypeScript tools' own output, captured from a scratch package at S27.
TS_LIB = ('export function classify(n: number): string {\n  if (n < 0) { return "negative"; } else { return "non-negative"; }\n'
          '}\n\nexport const shout = (s: string): string => {\n     const unused = 1;\n  return s.toUpperCase();\n};\n\n'
          'export function typed(): number {\n  return "not a number";\n}\n')
PRETTIER_OUT = ('export function classify(n: number): string {\n  if (n < 0) {\n    return "negative";\n  } else {\n'
                '    return "non-negative";\n  }\n}\n\nexport const shout = (s: string): string => {\n  const unused = 1;\n'
                '  return s.toUpperCase();\n};\n\nexport function typed(): number {\n  return "not a number";\n}\n')
ESLINT_OUT = "(node:1) ExperimentalWarning: a warning first\n" + json.dumps([{"filePath": str(ROOT / "src/lib.ts"), "messages": [
    {"ruleId": "@typescript-eslint/no-unused-vars", "message": "'unused' is assigned a value but never used.", "line": 6},
    {"ruleId": None, "message": "a fatal error with no line", "line": 0}]}])
TSC_OUT = "src/lib.ts(11,3): error TS2322: Type 'string' is not assignable to type 'number'.\nFound 1 error.\n"
LODASH = {"module_name": "lodash", "severity": "high", "title": "Command Injection in lodash", "github_advisory_id": "GHSA-35jh"}
TS_AUDITS = {   # manager: (audit with lodash's advisory, a clean audit)
    "npm": (json.dumps({"vulnerabilities": {"lodash": {"severity": "high", "via": [{"title": "Command Injection"}, "lodash"]}}}),
            json.dumps({"auditReportVersion": 2, "vulnerabilities": {}})),
    "pnpm": (json.dumps({"advisories": {"1106913": LODASH}}), json.dumps({"advisories": {}, "metadata": {}})),
    "yarn1": ("(node:1) [DEP0169] DeprecationWarning: url.parse()\n" + json.dumps({"type": "auditAdvisory", "data": {"advisory": LODASH}})
              + "\n" + json.dumps({"type": "auditSummary", "data": {}}), json.dumps({"type": "auditSummary", "data": {}})),
    "yarn": (json.dumps({"value": "lodash", "children": {"ID": 1, "Issue": "Command Injection in lodash", "Severity": "high"}}), ""),
}


def _yarn_info(value: str, licence: str, *deps: str) -> str:
    return json.dumps({"value": value, "children": {"Manifest": {"License": licence},
                                                    "Dependencies": [{"descriptor": d, "locator": d} for d in deps]}})


TS_LISTINGS = {  # manager: a listing where lodash is MIT and its dependency gpl-dep is GPL-3.0; is-number, GPL, is dev
    "npm": json.dumps({"name": "probe", "license": "UNLICENSED", "dependencies": {"lodash": {
        "version": "4.17.20", "license": "MIT", "dependencies": {"gpl-dep": {"version": "1.0.0", "license": {"type": "GPL-3.0"}}}}}}),
    "pnpm": json.dumps({"MIT": [{"name": "lodash", "versions": ["4.17.20"]}], "GPL-3.0": [{"name": "gpl-dep", "versions": ["1.0.0"]}]}),
    "yarn1": "\n".join([json.dumps({"type": "progressStart", "data": {}}), "(node:1) [DEP0169] DeprecationWarning",
                        json.dumps({"type": "table", "data": {"head": ["Name", "Version", "License", "URL"], "body": [
                            ["lodash", "4.17.20", "MIT", "u"], ["gpl-dep", "1.0.0", "GPL-3.0", "u"]]}})]),
    "yarn": "\n".join([_yarn_info("is-number@npm:7.0.0", "GPL-3.0"), _yarn_info("lodash@npm:4.17.20", "MIT", "gpl-dep@npm:1.0.0"),
                       _yarn_info("gpl-dep@npm:1.0.0", "GPL-3.0"),
                       _yarn_info("probe@workspace:.", "UNLICENSED", "is-number@npm:7.0.0", "lodash@npm:4.17.20")]),
}
TS_KEYS = {"npm": ("npm audit", "npm ls"), "pnpm": ("pnpm audit", "pnpm licenses"),
           "yarn1": ("yarn audit", "yarn licenses"), "yarn": ("yarn npm", "yarn info")}
TS_LOCKS = {"npm": ("package-lock.json", None), "pnpm": ("pnpm-lock.yaml", "pnpm@12.15.0"),
            "yarn1": ("yarn.lock", "yarn@1.22.22"), "yarn": ("yarn.lock", "yarn@4.18.1")}


def _ts_audited(manager: str, audit: tuple[int, str], listing: tuple[int, str]) -> list[Finding]:
    run = _Run({TS_KEYS[manager][0]: audit, TS_KEYS[manager][1]: listing})
    return attempt("audit", lambda: run_ts_audit(TS_SLOTS, run, _ts_files(*TS_LOCKS[manager])))


def _t_ts_readers(check) -> None:
    rows = [(p, n) for p, n, _ in prettier_rows("src/lib.ts", TS_LIB, PRETTIER_OUT)]
    check("prettier's output read as a diff counts the lines it rewrites: 2 and 6", rows == [("src/lib.ts", 2), ("src/lib.ts", 6)], str(rows))
    rows = [(p, n) for p, n, _ in eslint_rows(ESLINT_OUT)]
    check("ESLint's report is read past a warning, at the root-relative path; a message with no line is none",
          rows == [("src/lib.ts", 6)], str(rows))
    rows = [(m["path"], m["line"]) for m in map(TSC_ERROR.match, TSC_OUT.splitlines()) if m]
    check("a compiler error is a row at its file and line; the summary is none", rows == [("src/lib.ts", "11")], str(rows))
    for manager, (dirty, clean) in TS_AUDITS.items():
        found = _ts_audited(manager, (1, dirty), (0, TS_LISTINGS[manager]))
        check(f"{manager}: lodash's advisory and gpl-dep's license are findings; the root and a dev dependency are none",
              sorted((f.rule, f.where.split("@")[0]) for f in found) == [("audit", "lodash"), ("license", "gpl-dep")], str(found))
        found = _ts_audited(manager, (0, clean), (0, TS_LISTINGS[manager].replace("GPL-3.0", "MIT")))
        check(f"{manager}: a clean audit and allowed licenses pass", not found, str(found))
    oks = [license_ok(e, ["MIT", "ISC"]) for e in ("MIT", "(MIT OR GPL-3.0)", "MIT AND ISC", "MIT AND GPL-3.0", "GPL-3.0", "")]
    check("an `OR` passes on one allowed alternative, an `AND` needs both, and none is no license", oks == [True, True, True, False, False, False], str(oks))


def _t_ts_unmeasured(check) -> None:
    for label, manager, audit, listing in (
            ("npm's audit with no lockfile", "npm", (1, "npm error code ENOLOCK\n" + json.dumps({"error": {"code": "ENOLOCK"}})), (0, "{}")),
            ("pnpm's audit that wrote no report", "pnpm", (1, "ERR_PNPM_AUDIT_BAD_RESPONSE"), (0, "{}")),
            ("yarn 1's audit with no summary", "yarn1", (0, "error An unexpected error occurred"), (0, "")),
            ("yarn's audit that failed with no advisory", "yarn", (1, "Usage Error: no such command"), (0, "")),
            ("npm's report with no `vulnerabilities`", "npm", (0, json.dumps({"auditReportVersion": 2})), (0, "{}")),
            ("pnpm's report with no `advisories`", "pnpm", (0, json.dumps({"metadata": {}})), (0, "{}")),
            ("a license listing that failed", "npm", (0, TS_AUDITS["npm"][1]),
             (1, json.dumps({"name": "probe", "dependencies": {"lodash": {"missing": True}}, "problems": ["missing: lodash"]})))):
        check(f"{label} is unmeasured, never a pass", _rules(_ts_audited(manager, audit, listing)) == {"unmeasured"},
              str(_ts_audited(manager, audit, listing)))
    clean = _Run({"npm audit": (0, TS_AUDITS["npm"][1]), "npm ls": (0, "{}")})   # so only the lockfile explains it
    found = attempt("audit", lambda: run_ts_audit(TS_SLOTS, clean, {"package.json": json.dumps(TS_PACKAGE)}.get))
    check("a project with no lockfile is unmeasured", _rules(found) == {"unmeasured"} and "lockfile" in found[0].detail, str(found))


def _t_ts_gate(check) -> None:
    ch = _change({"src/lib.ts": TS_LIB, "package-lock.json": "x\n", "package.json": json.dumps(TS_PACKAGE)},
                 {"src/lib.ts": {2, 6, 11}, "package-lock.json": {1}})
    real = MEASURERS["typescript"]
    try:
        MEASURERS["typescript"] = (real[0], lambda t, p: 3)
        run = _Run({"prettier": (0, PRETTIER_OUT), "eslint": (1, ESLINT_OUT), "tsc": (2, TSC_OUT),
                    "npm audit": (1, TS_AUDITS["npm"][0]), "npm ls": (0, TS_LISTINGS["npm"])})
        found = _judged(ch, TS_SLOTS, run)
        check("the TypeScript slots report format, lint, types, audit and license findings on the change",
              {"format", "lint", "types", "audit", "license"} <= _rules(found), str(found))
        source = "export const f = () => 1;\n"
        test_file = _change({"tests/t.ts": source}, {"tests/t.ts": {1}})
        clean = {"prettier": (0, source), "eslint": (0, "[]"), "tsc": (0, "")}   # each case breaks one tool alone
        for label, broken in (("prettier", {"prettier": (2, "[error] No parser could be inferred")}),
                              ("ESLint", {"eslint": (2, "Oops! Something went wrong! ESLint couldn't find a config")}),
                              ("tsc", {"tsc": (1, "error TS5058: The specified path does not exist: 'tsconfig.json'.")})):
            MEASURERS["typescript"] = (real[0], lambda t, p: 1)
            found = _judged(test_file, TS_SLOTS, _Run({**clean, **broken}))
            check(f"{label} that cannot run is unmeasured, never a pass", _rules(found) == {"unmeasured"}, str(found))
    finally:
        MEASURERS["typescript"] = real
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "lcov.info").write_text("TN:\nSF:src/lib.ts\nFN:1,classify\nDA:2,1\nDA:6,0\nend_of_record\n", encoding="utf-8")
        try:
            got = run_coverage(dict(TS_SLOTS, coverage_report=str(Path(tmp) / "lcov.info")), _Run())["files"]
        except Unmeasured as e:
            got = {"unmeasured": str(e)}
        check("vitest's lcov, its paths relative to the root, is the TypeScript coverage report",
              got.get("src/lib.ts") == {"executed_lines": [2], "missing_lines": [6]}, str(got))
    judged = code_files(_change({"src/App.tsx": "x", "src/a.ts": "y", "src/b.js": "z"}, {"src/App.tsx": {1}, "src/a.ts": {1}, "src/b.js": {1}}),
                        dict(TS_PROFILE, code=["src/**"]))[0]
    check("a `.ts` and a `.tsx` file are the profile's code; a `.js` file is not", judged == ["src/App.tsx", "src/a.ts"], str(judged))


def _t_recall(check) -> None:
    real = MEASURERS["python"]
    try:
        MEASURERS["python"] = (lambda text, path: real[0](text, path)[:-1], *real[1:])   # one function dropped
        found, _ = judge_file("src/a.py", GOOD, {1}, PROFILE)
        check("a measurer that misses a function is a recall finding", _rules(found) == {"recall"}, str(found))
    finally:
        MEASURERS["python"] = real
    found, _ = judge_file("src/a.py", "def broken(:\n", {1}, PROFILE)
    check("a file Python cannot parse is a recall finding, never a pass", _rules(found) == {"recall"}, str(found))
    found, _ = judge_file("src/a.py", GOOD, {1}, PROFILE)
    check("a file read in full passes recall", not found, str(found))


def _t_log(check) -> None:
    f = Finding("complexity", "src/a.py:branchy", 21, "x")
    rows, err = parse_log(HEADER + _row("src/a.py:branchy", "complexity 21 — a parser"))
    check("a finding the Chair answered at its value is logged", not err and logged(f, rows), str(err))
    row = suggested_row(f)
    back, err = parse_log(HEADER + row + "\n")
    check("the suggested row is ASCII and reads back to its finding",
          row.isascii() and not err and back[0].rule_value == ("complexity", 21), f"{row} {err}")
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
    check("a suppression is named in words, never by its pattern",
          any("a `noqa` of a limit rule" in f.detail for f in found) and not any("\\b" in f.detail for f in found), str(found))
    found, _ = judge_file("src/gen/a.py", text, {7}, PROFILE)
    check("a generated marker under a declared generated path is not", not found, str(found))
    found, _ = judge_file("src/a.py", text, {1}, PROFILE)
    check("a suppression on an unchanged line is not this change's", not found, str(found))
    found, _ = judge_file("src/a.py", text, {2, 6, 7}, PROFILE)
    found = [Finding(f.rule, f.where, f.value, f.detail + " (a || b)") for f in found]   # a tool's own `|`
    rows, err = parse_log(HEADER + "".join(suggested_row(f).replace("| none |  |", "| none | acknowledged |") + "\n"
                                           for f in found))
    check("each suggested row is one row of the log, a `|` in its detail included, and answers its finding",
          err is None and all(logged(f, rows) for f in found), str(err))


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


RUFF_DIFF = ("--- src/a.py\n+++ src/a.py\n@@ -6,11 +6,13 @@\n \n \n def b():\n-    x=1\n+    x = 1\n     return x\n \n \n"
             " def c():\n     return 3\n+\n+\n def d():\n     return 4\n")   # ruff 0.6.9's own output, 3 context lines a side


def _t_format(check) -> None:
    def lines(diff: str) -> list[int]:
        return [n for _, n, _ in format_rows(diff)]

    check("a hunk counts the line ruff rewrites and the line its insertion precedes, never a context line",
          lines(RUFF_DIFF) == [9, 15], str(lines(RUFF_DIFF)))
    run = _Run({"format": (1, RUFF_DIFF)})
    found = run_checkers(["src/a.py"], {"src/a.py": {6, 8, 10, 14, 16}}, {}, run)
    check("a changed line among a hunk's context lines is no finding", not found, str(found))
    found = run_checkers(["src/a.py"], {"src/a.py": {15}}, {}, run)
    check("a run of inserted lines counts once, against the line it precedes",
          _rules(found) == {"format"} and found[0].value == 1, str(found))
    removed = "--- src/a.py\n+++ src/a.py\n@@ -3,5 +3,4 @@\n a = 1\n \n \n-\n def f():\n"
    check("a line ruff removes counts at its own number", lines(removed) == [6], str(lines(removed)))
    tail = "--- src/a.py\n+++ src/a.py\n@@ -1,2 +1,3 @@\n x = 1\n y = 2\n+z = 3\n"
    check("an insertion that ends the file counts at its last line", lines(tail) == [2], str(lines(tail)))
    newline = "--- src/a.py\n+++ src/a.py\n@@ -1,2 +1,2 @@\n x = 1\n-y = 2\n\\ No newline at end of file\n+y = 2\n"
    check("the no-newline marker is no line", lines(newline) == [2], str(lines(newline)))
    dashes = "--- src/a.py\n+++ src/a.py\n@@ -1,3 +1,2 @@\n x = 1\n--- a rule\n y = 2\n"
    check("a removed line that reads like a file header stays in its hunk",
          format_rows(dashes) == [("src/a.py", 2, "not as ruff formats it")], str(format_rows(dashes)))


def _t_checkers(check) -> None:
    fmt = "--- src/a.py\n+++ src/a.py\n@@ -3 +3 @@\n-x=1\n+x = 1\n"
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
          _rules(load_profile(yaml.safe_dump(dict(PROFILE, profile="go")))[1]) == {"profile"})
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
    for group in (_t_measurer, _t_rust_measurer, _t_rust_judge, _t_rust_readers, _t_rust_profile, _t_rust_gate, _t_ts_measurer, _t_ts_judge, _t_ts_tests, _t_ts_profile, _t_ts_readers, _t_ts_unmeasured, _t_ts_gate, _t_limits, _t_scope, _t_recall, _t_log, _t_markers, _t_diff, _t_clones,
                  _t_coverage, _t_format, _t_checkers, _t_audit, _t_gate, _t_profile, _t_law):
        try:
            group(check)
        except Exception as e:   # a crash is a failed fixture, never a crashed self-test
            check(f"{group.__name__} ran without raising", False, f"{type(e).__name__}: {e}")
    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 0 if not state["failures"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
