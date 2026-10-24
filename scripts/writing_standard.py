#!/usr/bin/env python3
"""
writing_standard.py - the writing standard's gate: every markdown file git tracks, judged whole
against docs/standards/writing_standard_v1.0.md in the voice and audience writing-profile.yaml gives
it.

THE FAILURE THIS CLOSES
-----------------------
Agents leave mechanical tells in what they write: characters no US keyboard types, headings that
read as sentences, stock phrases, and development references in documents for a production reader
(decision 2026-10-24-014). The template held hundreds of U+2014 dashes while a written rule against
them stood, because a rule that nothing checks stops nothing. Every file is judged whole, never its
changed lines, so text that entered unjudged is caught at the next commit (decision 2026-10-24-019).

WHAT IT DOES
------------
The law is read from the standard at every run, so a project's copy judges the project: the
character table (section 5), the phrase tables (section 7) and the built-in voices (section 2). A
table that cannot be read stops the gate, never reads as nothing to check. Then:
  profile      writing-profile.yaml holds `rules`, `template`, `default`, `agents` and `allow` only;
               every voice it names is a file, every agent slug a roster agent; a production glob
               that decides nothing (no tracked file, or only files an earlier rule claims) is
               refused (decision 2026-10-24-026)
  voice        each voice file's `name` is its file's and its `tables` are the standard's; a voice
               section 2 does not name is custom and holds a `## Sample` of 200 words or more
  characters   printable ASCII, tab, newline and letters with their accents, over the whole file
  headings     no comma or semicolon, no closing `.`, `!`, `;` or `:`, at most 8 words, the label
               of a format the gates read not counted
  phrases      the voice's tables, outside code spans and code blocks, across a line break, a
               `list end` phrase only where a sentence, a paragraph or a list item closes
  references   in a production file only: decision, story and session IDs, wikilinks, the Chair,
               sprint and orchestration paths, commit hashes
A finding is exempt where an occurrence of an `allow:` string in the same file holds its text. Each
finding prints its fix and the allow line that would exempt it. The `template:` rules apply ahead
of `rules` only where .project-profile is absent, so the template's README is development there and
production in every project (decision 2026-10-24-025).

--which <path>       the file's voice and audience and the rule that gave them, or the rule to add
--text <file> [--source <path>]
                     a produced deliverable's text: .docx, .pptx and .xlsx read with the standard
                     library, .txt or .md already extracted (as a PDF's is), judged as production in
                     the voice the source's rule names (decisions 2026-10-24-022 and -026)
--self-test          in-memory fixtures for every rule; this gate's own functions held to the coding
                     standard's production limits
Exit 0 clean, 1 a finding, 2 cannot run (the standard, the voices or the profile unreadable, git
failing, a file the text mode cannot read).

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It makes no judgement: tone, filler, hedging and colon subtitles are the document reviewer's,
against .claude/rules/writing.md (decision 2026-10-24-020). It fixes nothing; the humanizer does.
It cannot tell who wrote a file, so it judges a document by the document's voice.
"""
from __future__ import annotations

import contextlib
import io
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import code_standard  # noqa: E402  - the root, the self-test's check and the measurer of its own limits
import session_closeout  # noqa: E402  - the one glob translation the path rules here share

ROOT = code_standard.ROOT
STANDARD = "docs/standards/writing_standard_v1.0.md"
PROFILE_FILE = "writing-profile.yaml"
VOICES = "docs/standards/voices"
ROSTER = ".claude/agents"
TEMPLATE_MARK = ".project-profile"      # absent in the template alone (decision 2026-10-24-025)
PROFILE_KEYS = ("rules", "template", "default", "agents", "allow")
RULE_KEYS = {"paths", "voice", "audience"}
AUDIENCES = ("production", "development")
PLACES = ("anywhere", "list end")
SAMPLE_WORDS = 200
HEADING_WORDS = 8
RULES = ("profile", "voice", "characters", "headings", "phrases", "references")
MASK = "\x01"     # stands in for a code span's characters: not a word, not whitespace

FIXES = {
    "headings": "Make it a label: no comma or semicolon, no closing mark but a question mark, 8 words or "
                "fewer, a code span counting as one (section 6).",
    "anywhere": "Cut it, or say the fact it stands in for (section 7).",
    "list end": "Name the rest, or end the list with its last item (section 7).",
    "references": "Say what it means to this reader, or cut it (section 8).",
    "idle": "Correct the glob, or move the rule above the rule that claims its files: a production glob "
            "that decides nothing lets the file it meant fall to a later rule (section 4).",
    "profile": "Correct writing-profile.yaml to section 4 of the writing standard.",
    "voice": "Give the voice file the shape of section 2 of the writing standard.",
}
ALLOW_NOTE = ("An allow line goes under `allow:` in writing-profile.yaml and exempts that exact string in "
              "every file; a longer string exempts less. A change to the list is a gate change the Chair "
              "approves (section 9).")


class LawError(Exception):
    """The standard, the voices, the profile or a produced file cannot be read, or git fails. Exit 2."""


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    line: int
    col: int
    detail: str
    fix: str
    allow: str = ""         # the allow-list line that would exempt it; empty where none can


@dataclass(frozen=True)
class Hit:
    start: int
    end: int
    detail: str
    fix: str
    allow: str | None = None   # the string to allow; the flagged text widened to its word when None


@dataclass(frozen=True)
class Law:
    chars: dict[int, tuple[str, str]]          # code point -> (its name, its replacement)
    other: tuple[str, str]                     # the `any other` row
    tables: dict[str, tuple[tuple[str, str], ...]]   # table key -> ((phrase, where), ...)
    builtins: tuple[str, ...]                  # section 2's voices

    def char(self, cp: int) -> tuple[str, str]:
        return self.chars.get(cp, self.other)


@dataclass(frozen=True)
class Rule:
    paths: tuple[str, ...]
    voice: str
    audience: str
    origin: str             # where the profile holds it: `rules[0]`, `template[0]`


@dataclass(frozen=True)
class Profile:
    rules: tuple[Rule, ...]
    template: tuple[Rule, ...]
    default: str
    agents: dict
    allow: tuple[str, ...]

    def effective(self, in_template: bool) -> tuple[Rule, ...]:
        return self.template + self.rules if in_template else self.rules


@dataclass(frozen=True)
class Assignment:
    voice: str
    audience: str
    by: str                 # the rule and glob that gave it, or "" for a file no rule names


@dataclass(frozen=True)
class Setup:
    law: Law
    voices: dict[str, tuple[str, ...]]          # voice -> the phrase tables it takes
    profile: Profile
    in_template: bool
    findings: tuple[Finding, ...]               # the profile's and the voices'


@dataclass(frozen=True)
class Doc:
    blank: str              # the text with its code blocks blanked, offsets and newlines kept
    prose: str              # blank with its code spans masked too
    body: int               # where the body starts, after any frontmatter


# ==============================================================================
# The law, read from the standard
# ==============================================================================

POINTS = re.compile(r"U\+([0-9A-F]{4,6})(?: to U\+([0-9A-F]{4,6}))?")
PHRASE_TABLE = re.compile(r"^### (\w+) phrases[ \t]*$", re.M)


def section(text: str, number: int) -> str:
    m = re.search(rf"^## {number}\. .*$", text, re.M)
    if not m:
        raise LawError(f"{STANDARD} has no section {number}")
    end = text.find("\n## ", m.end())
    return text[m.end(): end if end != -1 else len(text)]


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []


def table(body: str, header: list[str]) -> list[list[str]]:
    """The rows of the first table in `body` headed `header`; a table absent or empty raises."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if cells(line) == header:
            rows = [cells(r) for r in _takewhile_rows(lines[i + 2:])]
            if not rows or any(len(r) != len(header) for r in rows):
                raise LawError(f"{STANDARD}'s `{' | '.join(header)}` table holds no row it can read")
            return rows
    raise LawError(f"{STANDARD} has no `{' | '.join(header)}` table")


def _takewhile_rows(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        if not line.startswith("|"):
            break
        out.append(line)
    return out


def read_characters(body: str) -> tuple[dict[int, tuple[str, str]], tuple[str, str]]:
    chars: dict[int, tuple[str, str]] = {}
    other = None
    for points, name, fix in table(body, ["Code points", "Characters", "Replace with"]):
        if points == "any other":
            other = (name, fix)
            continue
        for part in points.split(","):
            m = POINTS.fullmatch(part.strip())
            if not m or int(m.group(2) or m.group(1), 16) < int(m.group(1), 16):
                raise LawError(f"{STANDARD} section 5: cannot read the code points {points!r}")
            chars.update({cp: (name, fix) for cp in range(int(m.group(1), 16), int(m.group(2) or m.group(1), 16) + 1)})
    if other is None:
        raise LawError(f"{STANDARD} section 5 has no `any other` row")
    return chars, other


def read_phrases(body: str) -> dict[str, tuple[tuple[str, str], ...]]:
    heads = list(PHRASE_TABLE.finditer(body))
    if not heads:
        raise LawError(f"{STANDARD} section 7 holds no `### <Name> phrases` table")
    tables = {}
    for i, head in enumerate(heads):
        chunk = body[head.end(): heads[i + 1].start() if i + 1 < len(heads) else len(body)]
        rows = []
        for phrase, where in table(chunk, ["Phrase", "Where"]):
            m = re.fullmatch(r"`([^`]+)`", phrase)
            if not m or where not in PLACES:
                raise LawError(f"{STANDARD} section 7: a row must be a code span and one of {', '.join(PLACES)}, "
                               f"not {phrase!r} | {where!r}")
            rows.append((m.group(1), where))
        tables[head.group(1).lower()] = tuple(rows)
    return tables


def read_builtins(body: str) -> tuple[str, ...]:
    names = []
    for voice, _ in table(body, ["Voice", "For"]):
        m = re.search(r"`([a-z0-9-]+)`", voice)
        if not m:
            raise LawError(f"{STANDARD} section 2: cannot read the voice {voice!r}")
        names.append(m.group(1))
    return tuple(names)


def read_law(text: str) -> Law:
    chars, other = read_characters(section(text, 5))
    return Law(chars, other, read_phrases(section(text, 7)), read_builtins(section(text, 2)))


# ==============================================================================
# The voices and the profile
# ==============================================================================

FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)^---[ \t]*$\n?", re.S | re.M)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def split_frontmatter(text: str) -> tuple[str | None, int]:
    """The frontmatter's YAML and where the body starts, or (None, 0) for a file with none."""
    m = FRONTMATTER.match(text)
    return (m.group(1), m.end()) if m else (None, 0)


def parse_frontmatter(text: str) -> dict | None:
    import yaml
    head, _ = split_frontmatter(text)
    try:
        meta = yaml.safe_load(head) if head is not None else None
    except yaml.YAMLError:
        return None
    return meta if isinstance(meta, dict) else None


def sample_problems(body: str) -> list[str]:
    m = re.search(r"^## Sample[ \t]*$(.*?)(?=^## |\Z)", body, re.S | re.M)
    if not m:
        return ["is a custom voice, since section 2 does not name it, and holds no `## Sample` section"]
    blocks = fence_spans(m.group(1), 0)
    if len(blocks) != 1:
        return [f"its `## Sample` holds {len(blocks)} fenced blocks, where a custom voice holds one"]
    lines = m.group(1)[blocks[0][0]: blocks[0][1]].splitlines()
    inner = lines[1:-1] if len(lines) > 1 and FENCE.match(lines[-1]) else lines[1:]
    words = len(" ".join(inner).split())
    return [] if words >= SAMPLE_WORDS else [f"its sample holds {words} words, where a custom voice's holds "
                                              f"{SAMPLE_WORDS} or more"]


def judge_voices(files: dict[str, str], law: Law) -> tuple[dict[str, tuple[str, ...]], list[Finding]]:
    """Each voice file by its name: the phrase tables it takes, and what is wrong with it."""
    voices, found = {}, []
    for stem, text in sorted(files.items()):
        meta = parse_frontmatter(text) or {}
        tables = meta.get("tables")
        problems = [] if meta.get("name") == stem else [f"`name` is {meta.get('name')!r}, not its file's `{stem}`"]
        if not (isinstance(tables, list) and tables and all(t in law.tables for t in tables)):
            problems.append(f"`tables` must list one or more of {', '.join(law.tables)}")
        if stem not in law.builtins:
            problems += sample_problems(text[split_frontmatter(text)[1]:])
        voices[stem] = tuple(t for t in tables if t in law.tables) if isinstance(tables, list) else ()
        found += [Finding("voice", f"{VOICES}/{stem}.md", 1, 1, p, FIXES["voice"]) for p in problems]
    found += [Finding("voice", f"{VOICES}/{name}.md", 1, 1, "is named in section 2 and has no file", FIXES["voice"])
              for name in law.builtins if name not in files]
    return voices, found


def read_rules(value: object, key: str, voices: set[str]) -> tuple[list[Rule], list[str]]:
    if not isinstance(value, list):
        return [], [f"`{key}` must be a list of rules"]
    rules, problems = [], []
    for i, r in enumerate(value):
        where = f"{key}[{i}]"
        if not isinstance(r, dict) or set(r) != RULE_KEYS:
            problems.append(f"{where} must hold exactly `paths`, `voice` and `audience`")
        elif not (isinstance(r["paths"], list) and r["paths"] and all(isinstance(p, str) and p for p in r["paths"])):
            problems.append(f"{where}'s `paths` must be a list of globs")
        elif r["voice"] not in voices:
            problems.append(f"{where}'s voice {r['voice']!r} is no file in {VOICES}/")
        elif r["audience"] not in AUDIENCES:
            problems.append(f"{where}'s audience {r['audience']!r} is not {' or '.join(AUDIENCES)}")
        else:
            rules.append(Rule(tuple(r["paths"]), r["voice"], r["audience"], where))
    return rules, problems


def read_agents(value: object, voices: set[str], roster: set[str]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, dict):
        return ["`agents` must map a roster slug to a voice"]
    return ([f"`agents` names {slug!r}, which is no agent in {ROSTER}/" for slug in value if slug not in roster]
            + [f"`agents` gives {slug!r} the voice {v!r}, which is no file in {VOICES}/"
               for slug, v in value.items() if v not in voices])


def load_profile(text: str, voices: set[str], roster: set[str]) -> tuple[Profile, list[Finding]]:
    """The profile, and a finding for each value it holds wrongly; one that cannot be read raises."""
    import yaml
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise LawError(f"{PROFILE_FILE} does not parse as YAML: {e}") from e
    if not isinstance(data, dict):
        raise LawError(f"{PROFILE_FILE} is not a mapping")
    problems = [f"`{k}` is no key of the profile; it holds {', '.join(PROFILE_KEYS)}" for k in data if k not in PROFILE_KEYS]
    rules, p1 = read_rules(data.get("rules"), "rules", voices)
    template, p2 = read_rules(data.get("template", []), "template", voices)
    problems += p1 + p2 + read_agents(data.get("agents"), voices, roster)
    if data.get("default") not in voices:
        problems.append(f"`default` {data.get('default')!r} is no file in {VOICES}/")
    allow = data.get("allow", [])
    if not (isinstance(allow, list) and all(isinstance(s, str) and s.strip() for s in allow)):
        problems.append("`allow` must be a list of exact strings")
        allow = []
    profile = Profile(tuple(rules), tuple(template), str(data.get("default")), data.get("agents") or {}, tuple(allow))
    return profile, [Finding("profile", PROFILE_FILE, 1, 1, p, FIXES["profile"]) for p in problems]


@lru_cache(maxsize=None)
def _glob(pattern: str) -> re.Pattern:
    return session_closeout.glob_regex(pattern)


def matches(pattern: str, path: str) -> bool:
    return bool(_glob(pattern).match(path))


def idle_globs(rules: tuple[Rule, ...], files: list[str]) -> list[Finding]:
    """Each production glob that decides nothing: no tracked file, or only files an earlier rule claims."""
    found, claimed = [], {}
    for rule in rules:
        mine = {}
        for g in rule.paths:
            hits = {f for f in files if matches(g, f)}
            if rule.audience == "production" and not hits - set(claimed):
                why = (f"every file it matches is claimed by {claimed[min(hits)]}" if hits
                       else "it matches no tracked markdown file")
                found.append(Finding("profile", PROFILE_FILE, 1, 1, f"{rule.origin} `{g}` is production and decides "
                                     f"nothing: {why}", FIXES["idle"]))
            mine.update({f: rule.origin for f in hits})
        claimed = {**mine, **claimed}
    return found


def assign(path: str, profile: Profile, in_template: bool) -> Assignment:
    for rule in profile.effective(in_template):
        for g in rule.paths:
            if matches(g, path):
                return Assignment(rule.voice, rule.audience, f"{rule.origin} `{g}`")
    return Assignment(profile.default, "production", "")


def development_rule(path: str, voice: str) -> str:
    return f'- {{paths: ["{path}"], voice: {voice}, audience: development}}'


def which_text(path: str, profile: Profile, in_template: bool) -> str:
    a = assign(path, profile, in_template)
    place = "in the template" if in_template else "in a project"
    if a.by:
        return f"{path}: voice {a.voice}, audience {a.audience}, by {a.by} of {PROFILE_FILE} ({place})"
    return (f"{path}: voice {a.voice}, audience production, by no rule: the default voice, and production since no "
            f"rule names it ({place}).\nIf it is written for the people building the project, add to `rules:` "
            f"in {PROFILE_FILE}:\n  {development_rule(path, a.voice)}")


def in_template(root: Path) -> bool:
    return not (root / TEMPLATE_MARK).exists()


# ==============================================================================
# Reading a markdown file
# ==============================================================================

CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`)((?:(?!\n[ \t]*\n).)+?)(?<!`)\1(?!`)", re.S)


def fence_spans(text: str, start: int) -> list[tuple[int, int]]:
    """The fenced code blocks from `start`, fence lines included; an unclosed one runs to the end."""
    spans, opened, pos = [], None, start
    for line in text[start:].splitlines(keepends=True):
        m = FENCE.match(line)
        if opened is None and m:
            opened = (pos, m.group(1))
        elif opened and m and m.group(1)[0] == opened[1][0] and len(m.group(1)) >= len(opened[1]) \
                and not line[m.end():].strip():
            spans.append((opened[0], pos + len(line)))
            opened = None
        pos += len(line)
    if opened:
        spans.append((opened[0], len(text)))
    return spans


def read_doc(text: str) -> Doc:
    scan = text.replace("\r\n", " \n")       # same length, so every offset still points into `text`
    _, body = split_frontmatter(scan)
    chars = list(scan)
    for a, b in fence_spans(scan, body):
        chars[a:b] = [c if c == "\n" else " " for c in chars[a:b]]
    blank = "".join(chars)
    return Doc(blank, CODE_SPAN.sub(lambda m: MASK * len(m.group(0)), blank), body)


def widen(text: str, start: int, end: int) -> str:
    """The flagged text widened to the whitespace around it, its inner whitespace one space."""
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    while end < len(text) and not text[end].isspace():
        end += 1
    return " ".join(text[start:end].split())


# ==============================================================================
# The four mechanical rules
# ==============================================================================

CANDIDATE = re.compile(r"[^\t\n\x20-\x7e]")


def allowed_char(text: str, i: int) -> bool:
    if text[i] == "\r":
        return text[i + 1: i + 2] == "\n"
    return unicodedata.category(text[i])[0] in "LM"


def character_hits(text: str, law: Law) -> list[Hit]:
    """Each run of one character off the allowed set, named by its code point with its replacement."""
    hits: list[Hit] = []
    for m in CANDIDATE.finditer(text):
        i = m.start()
        if allowed_char(text, i) or (hits and hits[-1].end > i):
            continue
        j = i + 1
        while j < len(text) and text[j] == text[i]:
            j += 1
        name, fix = law.char(ord(text[i]))
        run = f" x{j - i}" if j - i > 1 else ""
        hits.append(Hit(i, j, f"U+{ord(text[i]):04X} {name}{run}", f"Replace with {fix}."))
    return hits


HEADING = re.compile(r"^ {0,3}#{1,6}(?=[ \t]|$)(.*)$", re.M)
CLOSING = re.compile(r"(?:^|[ \t]+)#+[ \t]*$")
LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
LABELS = (re.compile("^S\\d+ [-\u2014] \\d{4}-\\d{2}-\\d{2} [-\u2014] "),
          re.compile(r"^Decision (?:\[EXAMPLE\] )?(?:[A-Z][A-Z0-9]*-)?\d{4}-\d{2}-\d{2}-\d{3}: "),
          re.compile("^Epic: [A-Z][A-Z0-9]*-\\d+ [-\u2014] "))
ENDINGS = {".": "a full stop", "!": "an exclamation mark", ";": "a semicolon", ":": "a colon"}


def heading_words(title: str) -> int:
    """Its words, the label of a gate-read format dropped: a token holding a letter or a digit, a code
    span one word, a link its text."""
    for label in LABELS:
        m = label.match(title)
        if m:
            title = title[m.end():]
            break
    tokens = LINK.sub(r"\1", CODE_SPAN.sub(" x ", title)).split()
    return sum(1 for t in tokens if any(c.isalnum() for c in t))


def heading_problems(title: str) -> list[str]:
    quoted_out = LINK.sub(r"\1", CODE_SPAN.sub(" x ", title))     # a code span's commas are quoted, a URL's not text
    problems = [f"holds {name}" for mark, name in ((",", "a comma"), (";", "a semicolon")) if mark in quoted_out]
    if title[-1] in ENDINGS:
        problems.append(f"ends in {ENDINGS[title[-1]]}")
    words = heading_words(title)
    if words > HEADING_WORDS:
        problems.append(f"runs {words} words, over {HEADING_WORDS}")
    return problems


def heading_hits(doc: Doc) -> list[Hit]:
    hits = []
    for m in HEADING.finditer(doc.blank, doc.body):
        title = CLOSING.sub("", m.group(1)).strip()
        if not title:
            continue
        start = m.start(1) + len(m.group(1)) - len(m.group(1).lstrip())
        problems = heading_problems(title)
        if problems:
            hits.append(Hit(start, start + len(title), "the heading " + "; ".join(problems), FIXES["headings"], title))
    return hits


GAP = r"(?:[ \t]+(?:\n[ \t]*)?|\n[ \t]*)"     # whitespace within one paragraph, a line break included
LIST_END = r"(?=[.!)]|[ \t]*(?:\Z|\n[ \t]*(?:\n|\Z|[-*+][ \t]|\d+[.)][ \t]|#{1,6}[ \t])))"


@lru_cache(maxsize=None)
def phrase_regex(phrase: str, where: str) -> re.Pattern:
    words = [re.escape(w).replace("'", "['\u2019]") for w in phrase.split()]
    return re.compile(r"(?<!\w)" + GAP.join(words) + r"(?!\w)" + (LIST_END if where == "list end" else ""), re.I)


def phrase_hits(doc: Doc, law: Law, tables: tuple[str, ...]) -> list[Hit]:
    hits = []
    for key in tables:
        for phrase, where in law.tables[key]:
            hits += [Hit(m.start(), m.end(), f"`{phrase}` ({key} table, {where})", FIXES[where])
                     for m in phrase_regex(phrase, where).finditer(doc.prose)]
    return sorted(hits, key=lambda h: h.start)


REFERENCES = (
    ("a decision ID", re.compile(r"(?<![\w-])(?:[A-Z][A-Z0-9]*-)?\d{4}-\d{2}-\d{2}-\d{3}(?![\w-])")),
    ("a story ID", re.compile(r"(?<![\w-])[A-Z][A-Z0-9]*-\d+\.\d+(?!\w)")),
    ("a session number", re.compile(r"(?<!\w)S\d+(?!\w)")),
    ("a wikilink", re.compile(r"\[\[[^\[\]\n]+\]\]")),
    ("the Chair", re.compile(r"(?<!\w)[Tt]he" + GAP + r"Chair(?!\w)")),
    ("a sprint or orchestration path", re.compile(r"(?<![\w.-])(?:sprint|docs/orchestration)/")),
    ("a commit hash", re.compile(r"(?<![\w-])(?=[0-9a-f]*[0-9])(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}(?![\w-])")),
)


def reference_hits(text: str) -> list[Hit]:
    hits = [Hit(m.start(), m.end(), f"{label} `{' '.join(m.group(0).split())}`", FIXES["references"])
            for label, pattern in REFERENCES for m in pattern.finditer(text)]
    return sorted(hits, key=lambda h: h.start)


# ==============================================================================
# Judging a file
# ==============================================================================

def allowed_spans(text: str, allow: tuple[str, ...]) -> list[tuple[int, int]]:
    """Each occurrence of an allowed string: exact and case-sensitive, a space matching any whitespace."""
    spans = []
    for s in allow:
        pattern = r"\s+".join(re.escape(part) for part in re.split(r" +", s))
        spans += [m.span() for m in re.finditer(pattern, text)]
    return spans


def to_finding(path: str, text: str, rule: str, hit: Hit) -> Finding:
    line = text.count("\n", 0, hit.start) + 1
    col = hit.start - text.rfind("\n", 0, hit.start)
    allow = hit.allow if hit.allow is not None else widen(text, hit.start, hit.end)
    return Finding(rule, path, line, col, hit.detail, hit.fix, json.dumps(allow))


def judge_text(path: str, text: str, a: Assignment, setup: Setup) -> list[Finding]:
    """One file's findings in line order, those an allowed string holds left out."""
    doc = read_doc(text)
    hits = {"characters": character_hits(text, setup.law), "headings": heading_hits(doc),
            "phrases": phrase_hits(doc, setup.law, setup.voices.get(a.voice, ())),
            "references": reference_hits(text.replace("\r\n", " \n")) if a.audience == "production" else []}
    spans = allowed_spans(text, setup.profile.allow)
    found = [to_finding(path, text, rule, h) for rule, found in hits.items() for h in found
             if not any(lo <= h.start and h.end <= hi for lo, hi in spans)]
    return sorted(found, key=lambda f: (f.line, f.col))


# ==============================================================================
# Produced files: the text mode (decision 2026-10-24-026)
# ==============================================================================

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
X = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def as_markdown(paragraphs: list[tuple[int, str]]) -> str:
    """Paragraphs as markdown, a heading at its level; a paragraph that would read as a heading or a
    fence is escaped, since it is neither."""
    out = []
    for level, text in paragraphs:
        if level:
            out.append("#" * level + " " + " ".join(text.split()))
        else:
            out.append("\\" + text if HEADING.match(text) or FENCE.match(text) else text)
    return "\n\n".join(out) + "\n"


def docx_levels(z: zipfile.ZipFile) -> dict[str, int]:
    """Each paragraph style that is a heading, by its id: `heading N` or `Title` by name."""
    if "word/styles.xml" not in z.namelist():
        return {f"Heading{n}": n for n in range(1, 7)}
    levels = {}
    for style in ET.fromstring(z.read("word/styles.xml")).iter(W + "style"):
        name = style.find(W + "name")
        m = re.fullmatch(r"heading ([1-6])|(title)", (name.get(W + "val") if name is not None else "").lower())
        if m:
            levels[style.get(W + "styleId")] = int(m.group(1)) if m.group(1) else 1
    return levels


def docx_paragraph(p: ET.Element) -> str:
    parts = []
    for el in p.iter():
        if el.tag == W + "t":
            parts.append(el.text or "")
        elif el.tag == W + "tab":
            parts.append("\t")
        elif el.tag in (W + "br", W + "cr"):
            parts.append("\n")
    return "".join(parts)


def docx_text(z: zipfile.ZipFile) -> str:
    levels = docx_levels(z)
    parts = sorted((n for n in z.namelist() if re.fullmatch(r"word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml", n)),
                   key=lambda n: (n != "word/document.xml", n))
    paragraphs = []
    for name in parts:
        for p in ET.fromstring(z.read(name)).iter(W + "p"):
            style = p.find(f"{W}pPr/{W}pStyle")
            paragraphs.append((levels.get(style.get(W + "val"), 0) if style is not None else 0, docx_paragraph(p)))
    return as_markdown(paragraphs)


def pptx_text(z: zipfile.ZipFile) -> str:
    """Every slide's paragraphs and then the notes, a title placeholder's read as a heading."""
    names = [n for n in z.namelist() if re.fullmatch(r"ppt/(slides/slide|notesSlides/notesSlide)\d+\.xml", n)]
    paragraphs = []
    for name in sorted(names, key=lambda n: ("notes" in n, int(re.sub(r"\D", "", n.rsplit("/", 1)[1])))):
        root = ET.fromstring(z.read(name))
        titles = {id(p) for sp in root.iter(P + "sp") if _is_title(sp) for p in sp.iter(A + "p")}
        paragraphs += [(1 if id(p) in titles else 0, "".join(t.text or "" for t in p.iter(A + "t")))
                       for p in root.iter(A + "p")]
    return as_markdown([p for p in paragraphs if p[1].strip()])


def _is_title(sp: ET.Element) -> bool:
    ph = sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
    return ph is not None and ph.get("type") in ("title", "ctrTitle")


def xlsx_text(z: zipfile.ZipFile) -> str:
    """The sheet names, the shared strings and each sheet's inline strings, one paragraph each."""
    names = z.namelist()
    paragraphs = []
    if "xl/workbook.xml" in names:
        paragraphs += [(0, s.get("name") or "") for s in ET.fromstring(z.read("xl/workbook.xml")).iter(X + "sheet")]
    holders = (["xl/sharedStrings.xml"] if "xl/sharedStrings.xml" in names else []) + \
        sorted(n for n in names if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n))
    for name in holders:
        tag = X + ("si" if name.endswith("sharedStrings.xml") else "is")
        paragraphs += [(0, "".join(t.text or "" for t in el.iter(X + "t"))) for el in ET.fromstring(z.read(name)).iter(tag)]
    return as_markdown([p for p in paragraphs if p[1].strip()])


def produced_text(path: Path) -> str:
    readers = {".docx": docx_text, ".pptx": pptx_text, ".xlsx": xlsx_text}
    suffix = path.suffix.lower()
    if suffix not in readers and suffix not in (".md", ".txt"):
        raise LawError(f"{path.name}: the text mode reads .docx, .pptx, .xlsx, .txt or .md; extract a PDF's text "
                       f"first (`pdftotext {path.name}`), or check the .docx it was made from")
    try:
        if suffix in readers:
            with zipfile.ZipFile(path) as z:
                return readers[suffix](z)
        return path.read_text(encoding="utf-8")
    except (OSError, zipfile.BadZipFile, KeyError, ET.ParseError, UnicodeDecodeError) as e:
        raise LawError(f"cannot read {path}: {e}") from e


# ==============================================================================
# The real tree
# ==============================================================================

def tracked_markdown(root: Path) -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise LawError(f"git ls-files failed: {out.stderr.strip()}")
    return sorted(p for p in out.stdout.split("\0") if p.lower().endswith(".md"))


def setup(root: Path, files: list[str]) -> Setup:
    """The law, the voices and the profile, each read from the tree; one that cannot be read raises."""
    law_path, voice_dir, profile_path = root / STANDARD, root / VOICES, root / PROFILE_FILE
    for need in (law_path, profile_path):
        if not need.is_file():
            raise LawError(f"{need.relative_to(root)} is missing")
    if not voice_dir.is_dir():
        raise LawError(f"{VOICES}/ is missing")
    law = read_law(law_path.read_text(encoding="utf-8"))
    voices, found = judge_voices({p.stem: p.read_text(encoding="utf-8") for p in voice_dir.glob("*.md")}, law)
    roster = {p.stem for p in (root / ROSTER).glob("*.md")}
    profile, problems = load_profile(profile_path.read_text(encoding="utf-8"), set(voices), roster)
    tmpl = in_template(root)
    return Setup(law, voices, profile, tmpl, tuple(found + problems + idle_globs(profile.effective(tmpl), files)))


def judge_tree(root: Path, files: list[str], s: Setup) -> tuple[list[Finding], dict[str, str]]:
    """Every file's findings, and for a file production by no rule the rule that would declare it
    development."""
    found, notes = [], {}
    for path in files:
        try:
            text = (root / path).read_text(encoding="utf-8")
        except FileNotFoundError:
            continue        # deleted in the working tree; git still lists it until the deletion is staged
        except UnicodeDecodeError:
            found.append(Finding("characters", path, 1, 1, "is not UTF-8 text", "Save it as UTF-8."))
            continue
        a = assign(path, s.profile, s.in_template)
        mine = judge_text(path, text, a, s)
        if not a.by and any(f.rule == "references" for f in mine):
            notes[path] = development_rule(path, a.voice)
        found += mine
    return found, notes


def report(found: list[Finding], notes: dict[str, str], judged: int) -> int:
    print(f"\nWriting Standard Gate ({judged} files)")
    print("=" * 60)
    if not found:
        print("PASSED")
        return 0
    for i, f in enumerate(found):
        print(f"  {f.path}:{f.line}:{f.col}  {f.rule}  {f.detail}\n      fix:   {f.fix}")
        if f.allow:
            print(f"      allow: - {f.allow}")
        if f.path in notes and (i + 1 == len(found) or found[i + 1].path != f.path):
            print(f"  {f.path} is production by no rule. If it is written for the people building the project, "
                  f"add to `rules:` in {PROFILE_FILE}:\n      {notes[f.path]}")
    counts = {r: sum(1 for f in found if f.rule == r) for r in RULES}
    print(f"\nBLOCKED: {len(found)} finding(s) in {len({f.path for f in found})} file(s): "
          + ", ".join(f"{r} {n}" for r, n in counts.items() if n))
    print(ALLOW_NOTE)
    return 1


def _argument(argv: list[str], flag: str) -> str:
    i = argv.index(flag)
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        raise LawError(f"{flag} needs a path")
    return argv[i + 1]


def run(root: Path, argv: list[str]) -> int:
    files = tracked_markdown(root)
    s = setup(root, files)
    if s.findings:
        return report(list(s.findings), {}, len(files))
    if "--which" in argv:
        print(which_text(_argument(argv, "--which"), s.profile, s.in_template))
        return 0
    if "--text" in argv:
        target = Path(_argument(argv, "--text"))
        voice = assign(_argument(argv, "--source"), s.profile, s.in_template).voice if "--source" in argv \
            else s.profile.default
        return report(judge_text(str(target), produced_text(target), Assignment(voice, "production", ""), s), {}, 1)
    return report(*judge_tree(root, files, s), len(files))


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    try:
        return run(ROOT, argv)
    except LawError as e:
        print(f"writing_standard: cannot run: {e}", file=sys.stderr)
        return 2


# ==============================================================================
# SELF-TEST - every rule against a passing and a failing fixture, in memory
# ==============================================================================

def _law() -> Law:
    return read_law((ROOT / STANDARD).read_text(encoding="utf-8"))


def _setup(rules: tuple[Rule, ...] = (), allow: tuple[str, ...] = ()) -> Setup:
    law = _law()
    voices, _ = judge_voices({p.stem: p.read_text(encoding="utf-8") for p in (ROOT / VOICES).glob("*.md")}, law)
    return Setup(law, voices, Profile(rules, (), "technical", {}, allow), True, ())


def _judge(text: str, audience: str = "development", voice: str = "technical", allow: tuple[str, ...] = ()) -> list[Finding]:
    return judge_text("x.md", text, Assignment(voice, audience, ""), _setup(allow=allow))


def _rules(found: list[Finding]) -> set[str]:
    return {f.rule for f in found}


def _raises(fn, *args) -> bool:
    try:
        fn(*args)
    except LawError:
        return True
    return False


def _t_law(check) -> None:
    text = (ROOT / STANDARD).read_text(encoding="utf-8")
    law = read_law(text)
    check("the character table names U+2014 with its replacement",
          law.char(0x2014)[0] == "em dash" and "a comma" in law.char(0x2014)[1], str(law.char(0x2014)))
    check("a range and a list of code points are read whole",
          all(cp in law.chars for cp in (0x2190, 0x21FF, 0x200B, 0x200D, 0x2060, 0xFEFF)))
    check("a character the table does not name takes the `any other` row", law.char(0x1F600) == law.other)
    check("the phrase tables are keyed by their first word",
          ("and more", "list end") in law.tables["ai"] and ("seamless", "anywhere") in law.tables["marketing"])
    check("section 2's voices are the built-ins", {"technical", "creative"} <= set(law.builtins))
    five, seven, two = section(text, 5), section(text, 7), section(text, 2)
    broken = {
        "a code point it cannot read": text.replace("| U+2014 |", "| U+20ZZ |"),
        "a character table with no `any other` row": text.replace("| any other |", "| U+2603 |"),
        "a phrases section with no table": text.replace(seven, "\nNone yet.\n"),
        "a phrase not in a code span": text.replace("| `delve into` |", "| delve into |"),
        "a Where neither anywhere nor list end": text.replace("| `delve into` | anywhere |", "| `delve into` | often |"),
        "a voices section with no table": text.replace(two, "\nSeven.\n"),
        "a standard with no section 5": text.replace(five, "").replace("## 5. Characters", "## 5a"),
    }
    for label, bad in broken.items():
        check(f"{label} raises, never reads as empty", bad != text and _raises(read_law, bad))


def _profile_text() -> str:
    return (ROOT / PROFILE_FILE).read_text(encoding="utf-8")


def _t_profile(check) -> None:
    voices = {p.stem for p in (ROOT / VOICES).glob("*.md")}
    roster = {"framework-maintainer"}
    profile, found = load_profile(_profile_text(), voices, roster)
    check("the real profile loads with no finding", not found and profile.default == "technical", str(found))
    base = "rules:\n  - paths: [\"a/**\"]\n    voice: technical\n    audience: development\ndefault: technical\n"
    broken = {
        "an unknown key": base + "extra: 1\n",
        "a rule's voice with no file": base.replace("voice: technical", "voice: pirate"),
        "an audience neither production nor development": base.replace("audience: development", "audience: everyone"),
        "a rule missing its audience": base.replace("    audience: development\n", ""),
        "a default voice with no file": base.replace("default: technical", "default: pirate"),
        "an agent slug with no roster agent": base + "agents:\n  ghost-writer: technical\n",
        "an agent's voice with no file": base + "agents:\n  framework-maintainer: pirate\n",
        "an allow entry that is not a string": base + "allow: [3]\n",
        "an empty allow entry": base + "allow: [\"\"]\n",
    }
    check("a sound profile passes", not load_profile(base + "agents:\n  framework-maintainer: technical\n", voices, roster)[1])
    for label, bad in broken.items():
        check(f"{label} is a finding", "profile" in _rules(load_profile(bad, voices, roster)[1]))
    check("a profile that does not parse raises", _raises(load_profile, "rules: [\n", voices, roster))
    check("a profile that is not a mapping raises", _raises(load_profile, "- a\n", voices, roster))


def _rule(glob: str, audience: str, origin: str = "rules[0]") -> Rule:
    return Rule((glob,), "technical", audience, origin)


def _t_globs(check) -> None:
    files = ["docs/a.md", "docs/runbooks/r.md", "sprint/x.md"]

    def idle(*rules: Rule) -> list[Finding]:
        return idle_globs(tuple(rules), files)

    check("a development glob matching nothing passes, as the starter's project paths do",
          not idle(_rule("docs/prd/**", "development")))
    check("a production glob matching nothing is refused", bool(idle(_rule("docs/runbook/**", "production"))))
    check("a production glob matching a file passes", not idle(_rule("docs/runbooks/**", "production")))
    check("a production glob whose files an earlier rule claims is refused",
          bool(idle(_rule("docs/**", "development"), _rule("docs/runbooks/**", "production", "rules[1]"))))
    check("a production glob ahead of the development rule passes",
          not idle(_rule("docs/runbooks/**", "production"), _rule("docs/**", "development", "rules[1]")))
    profile, _ = load_profile(_profile_text(), {p.stem for p in (ROOT / VOICES).glob("*.md")}, {"framework-maintainer"})
    check("--which README.md gives development in the template",
          "audience development, by template[0]" in which_text("README.md", profile, True), which_text("README.md", profile, True))
    check("--which README.md gives production with a .project-profile present",
          "audience production, by no rule" in which_text("README.md", profile, False)
          and "audience: development}" in which_text("README.md", profile, False), which_text("README.md", profile, False))
    check("a sprint file is development by the starter's rule", assign("sprint/x.md", profile, False).audience == "development")
    with tempfile.TemporaryDirectory() as tmp:
        absent = in_template(Path(tmp))
        (Path(tmp) / TEMPLATE_MARK).write_text("commercial\n", encoding="utf-8")
        check("the template is where .project-profile is absent", absent and not in_template(Path(tmp)))


def _voice(name: str, tables: str = "[ai, marketing]", sample: str | None = None) -> str:
    text = f"---\nname: {name}\ntables: {tables}\n---\n\n# A voice\n\n## Traits\n\n- Person: the first.\n"
    return text + (f"\n## Sample\n\n```text\n{sample}\n```\n" if sample is not None else "")


def _t_voices(check) -> None:
    law = _law()
    real = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / VOICES).glob("*.md")}
    check("the real voices load with no finding", not judge_voices(real, law)[1], str(judge_voices(real, law)[1]))
    cases = {
        "a name that is not its file's": ("technical", _voice("plain")),
        "a table the standard lacks": ("technical", _voice("technical", "[ai, legal]")),
        "no table": ("technical", _voice("technical", "[]")),
        "no frontmatter": ("technical", "# Technical voice\n"),
        "a custom voice with no sample": ("chair", _voice("chair")),
        "a custom voice whose sample holds 199 words": ("chair", _voice("chair", sample=" ".join(["word"] * 199))),
        "a custom voice whose sample is two blocks":
            ("chair", _voice("chair", sample=" ".join(["word"] * 200)) + "\n```\nmore\n```\n"),
    }
    for label, (stem, text) in cases.items():
        check(f"{label} is a finding", "voice" in _rules(judge_voices({**real, stem: text}, law)[1]))
    check("a custom voice whose sample holds 200 words passes",
          not judge_voices({**real, "chair": _voice("chair", sample=" ".join(["word"] * 200))}, law)[1])
    check("a built-in voice with no file is a finding",
          "voice" in _rules(judge_voices({k: v for k, v in real.items() if k != "technical"}, law)[1]))
    check("creative takes the AI table alone", judge_voices(real, law)[0]["creative"] == ("ai",))


def _t_characters(check) -> None:
    check("ASCII, a tab, an accented letter and a combining accent pass",
          not _judge("plain\ttext caf\u00e9 cafe\u0301\n"))
    found = _judge("a\u2014b\n")
    check("U+2014 is a finding naming its code point and its fix",
          bool(found) and "U+2014 em dash" in found[0].detail and "a comma" in found[0].fix, str(found))
    check("a carriage return before a newline passes", not _judge("line\r\nnext\r\n"))
    check("a carriage return alone is a finding", "characters" in _rules(_judge("a\rb\n")))
    run_ = _judge("\u2500" * 5 + "\n")
    check("a run of one character is one finding", len(run_) == 1 and "x5" in run_[0].detail, str(run_))
    check("a symbol the table does not name takes `any other`", "words, or nothing" in _judge("\U0001F600\n")[0].fix)
    check("a code block is judged too", "characters" in _rules(_judge("```\n\u2192\n```\n")))
    check("the frontmatter is judged too", "characters" in _rules(_judge("---\nname: a\u2026\n---\n\nBody.\n")))


def _heading_flagged(line: str) -> bool:
    return "headings" in _rules(_judge(line + "\n"))


def _t_headings(check) -> None:
    eight = "one two three four five six seven eight"
    for line in ("# A plain label heading", "## Is it ready?", f"## {eight}", "## `a b c d e f g h i j` and four words",
                 "## one two three four - five six seven eight", "## See [the guide](https://x.example/a,b)",
                 f"## S20 - 2026-10-24 - {eight}",
                 f"## Decision 2026-10-24-026: {eight}", f"## Decision [EXAMPLE] 2025-01-15-001: {eight}",
                 f"## Epic: TMPL-6 - {eight}", "## Closing hashes ##", "## The `a, b` pair", "#hashtag, here",
                 "    ## indented, so code"):
        check(f"passes: {line}", not _heading_flagged(line))
    check("the label in its U+2014 form is not counted either",
          "headings" not in _rules(_judge(f"## S20 \u2014 2026-10-24 \u2014 {eight}\n")))
    for line in ("## Install, then run", "## Install; then run", "## Done.", "## Done!", "## Done;", "## Steps:",
                 f"## {eight} nine", "## Closing, hashes ##", "## Steps: ##", f"## S20 - 2026-10-24 - {eight} nine"):
        check(f"refused: {line}", _heading_flagged(line))
    check("a heading in a code block is not judged", not _judge("```\n## In, a fence\n```\n"))
    check("a comment in the frontmatter is not a heading", not _judge("---\nname: x\n# a, comment\n---\n\nBody.\n"))


def _phrase_flagged(text: str, voice: str = "technical") -> bool:
    return "phrases" in _rules(_judge(text, voice=voice))


def _t_phrases(check) -> None:
    for label, text in (("a phrase", "We delve into it.\n"), ("in any case", "We Delve Into it.\n"),
                        ("across a line break", "We delve\ninto it.\n"), ("in the frontmatter", "---\nd: delve into\n---\n"),
                        ("with a U+2019 apostrophe", "So it\u2019s worth noting.\n"),
                        ("a marketing phrase in the technical voice", "A seamless step.\n"),
                        ("`and more` closing a sentence", "Apples, pears and more.\n"),
                        ("`and more` closing a list item", "- apples and more\n- pears\n"),
                        ("`and more` closing a paragraph", "Apples and more\n\nNext.\n"),
                        ("`and more` at the end of the file", "Apples and more"),
                        ("`and more` before a closing parenthesis", "(apples and more)\n")):
        check(f"flagged: {label}", _phrase_flagged(text))
    for label, text in (("a paragraph break between its words", "We delve\n\ninto it.\n"),
                        ("in a code span", "Quote `delve into` here.\n"), ("in a code block", "```\ndelve into\n```\n"),
                        ("a longer word", "Seamlessness.\n"), ("`and more` inside a sentence", "And more complex rules.\n"),
                        ("`and more` wrapped mid-sentence", "A list and more\n  complex text.\n")):
        check(f"passes: {label}", not _phrase_flagged(text))
    check("the creative voice takes no marketing table", not _phrase_flagged("A seamless step.\n", "creative"))


REFERENCE_SAMPLES = ("decision 2026-10-24-026", "decision ACME-2026-09-24-001", "story TMPL-6.2", "session S19",
                     "see [[reference_writing_standard_design]]", "ask the Chair", "ask The\nChair", "in sprint/x", "in docs/orchestration/k",
                     "commit abc1234", "commit 2f64620e1d")


def _t_references(check) -> None:
    for text in REFERENCE_SAMPLES:
        check(f"production refuses: {text!r}", "references" in _rules(_judge(text + "\n", "production")))
    check("development refuses none of them",
          not any("references" in _rules(_judge(t + "\n")) for t in REFERENCE_SAMPLES))
    check("a reference in a code span still counts", "references" in _rules(_judge("Run `TMPL-6.2`.\n", "production")))
    for text in ("the chair by the door", "id 26a6d028-1053-4f94-89fb-c74368a36ec7", "deadbeef", "1234567", "ABC1234",
                 "version v2.1.0", "SCM and S"):
        check(f"production passes: {text!r}", not _judge(text + "\n", "production"), str(_judge(text + "\n", "production")))


def _t_allow(check) -> None:
    text = "Store it in Amazon S3 today.\n"
    check("an unallowed S3 is a finding", bool(_judge(text, "production")))
    check("an allowed string exempts the text inside it", not _judge(text, "production", allow=("Amazon S3",)))
    check("a space in an allowed string matches a line break",
          not _judge("Store it in Amazon\nS3 today.\n", "production", allow=("Amazon S3",)))
    check("an allowed string matches case-sensitively", bool(_judge(text, "production", allow=("amazon S3",))))
    check("an allowed string that does not hold the flagged text exempts nothing",
          bool(_judge(text, "production", allow=("Amazon",))))
    check("a heading is exempt when an allowed string holds its whole text",
          not _judge("## Install, then run\n", allow=("Install, then run",)))
    check("a heading is not exempt by part of its text", bool(_judge("## Install, then run\n", allow=("Install",))))
    found = _judge("It read 20\u00b0C here.\n")
    check("the allow line is the flagged word, off-ASCII written as an escape",
          bool(found) and found[0].allow == '"20\\u00b0C"', str(found))
    check("a heading's allow line is its whole text", _judge("## Install, then run\n")[0].allow == '"Install, then run"')


def _t_output(check) -> None:
    with contextlib.redirect_stdout(io.StringIO()) as out:
        clean = report([], {}, 3)
        blocked = report(_judge("a\u2014b\n## Done.\n"), {}, 3)
    check("no finding exits 0 and a finding exits 1", clean == 0 and blocked == 1)
    check("the report counts the findings by rule", "characters 1, headings 1" in out.getvalue(), out.getvalue())
    check("each finding prints its fix and its allow line", "fix:   Replace with" in out.getvalue() and "allow: - " in out.getvalue())
    with tempfile.TemporaryDirectory() as tmp:
        check("a tree with no standard cannot run", _raises(setup, Path(tmp), []))
        (Path(tmp) / "docs" / "standards").mkdir(parents=True)
        (Path(tmp) / STANDARD).write_text((ROOT / STANDARD).read_text(encoding="utf-8"), encoding="utf-8")
        check("a tree with no profile cannot run", _raises(setup, Path(tmp), []))


def _zip(parts: dict[str, str]) -> zipfile.ZipFile:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, xml in parts.items():
            z.writestr(name, xml)
    return zipfile.ZipFile(buf)


def _w_para(text: str, style: str = "") -> str:
    props = f"<w:pPr><w:pStyle w:val='{style}'/></w:pPr>" if style else ""
    return f"<w:p>{props}<w:r><w:t>{text}</w:t></w:r></w:p>"


def _docx() -> zipfile.ZipFile:
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    styles = f'<w:styles {ns}><w:style w:styleId="Heading1"><w:name w:val="heading 1"/></w:style></w:styles>'
    body = _w_para("Overview, at a glance", "Heading1") + _w_para("Built in S19 by the team.") + \
        _w_para("# Not a heading, though")
    return _zip({"word/styles.xml": styles, "word/document.xml": f"<w:document {ns}><w:body>{body}</w:body></w:document>",
                 "word/footer1.xml": f"<w:ftr {ns}>{_w_para('Page 1 of 2')}</w:ftr>"})


def _p_shape(placeholder: str, text: str) -> str:
    return (f"<p:sp><p:nvSpPr><p:nvPr>{placeholder}</p:nvPr></p:nvSpPr>"
            f"<p:txBody><a:p><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>")


def _pptx() -> zipfile.ZipFile:
    ns = ('xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
          'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"')
    shapes = _p_shape("<p:ph type='title'/>", "Results, in short") + _p_shape("", "A seamless rollout")
    return _zip({"ppt/slides/slide1.xml": f"<p:sld {ns}><p:cSld><p:spTree>{shapes}</p:spTree></p:cSld></p:sld>"})


def _xlsx() -> zipfile.ZipFile:
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    return _zip({"xl/workbook.xml": f'<workbook {ns}><sheets><sheet name="Summary"/></sheets></workbook>',
                 "xl/sharedStrings.xml": f"<sst {ns}><si><t>It is worth noting the total.</t></si></sst>"})


def _t_text(check) -> None:
    s = _setup()

    def judge(text: str, voice: str = "technical") -> list[Finding]:
        return judge_text("out", text, Assignment(voice, "production", ""), s)

    docx = docx_text(_docx())
    check("a Word heading style is read as a heading", "# Overview, at a glance" in docx and "headings" in _rules(judge(docx)), docx)
    check("a Word file's text is production, whatever its source's audience", "references" in _rules(judge(docx)))
    check("a paragraph opening with # is not read as a heading",
          [f.detail for f in judge(docx) if f.rule == "headings"] == ["the heading holds a comma"], str(judge(docx)))
    check("the footer's text is read too", "Page 1 of 2" in docx)
    pptx = pptx_text(_pptx())
    check("a slide title is read as a heading", "# Results, in short" in pptx and "headings" in _rules(judge(pptx)), pptx)
    check("a slide's body is judged for phrases", "phrases" in _rules(judge(pptx)))
    check("the voice comes from the source: creative takes no marketing table", "phrases" not in _rules(judge(pptx, "creative")))
    xlsx = xlsx_text(_xlsx())
    check("a sheet's strings and its name are read", "Summary" in xlsx and "phrases" in _rules(judge(xlsx)), xlsx)
    with tempfile.TemporaryDirectory() as tmp:
        pdf, txt = Path(tmp) / "a.pdf", Path(tmp) / "a.txt"
        pdf.write_bytes(b"%PDF-1.4")
        txt.write_text("Extracted text.\n", encoding="utf-8")
        check("a PDF cannot be read: its text is extracted first", _raises(produced_text, pdf))
        check("extracted text is read as it stands", produced_text(txt) == "Extracted text.\n")


def _t_own_limits(check) -> None:
    own = code_standard.measure_python(Path(__file__).read_text(encoding="utf-8"))
    over = [f"{f.name} ({f.complexity}c/{f.code_lines}l/{f.parameters}p)" for f in own
            if code_standard.judge_function("", f, "production")]
    check("this gate's own functions meet the coding standard's production limits", not over, ", ".join(over))
    check("this gate is ASCII, naming each character by its escape",
          Path(__file__).read_text(encoding="utf-8").isascii())


def run_self_test() -> int:
    print("\nWriting Standard Self-Test")
    print("=" * 60)
    check, state = code_standard._check_factory()
    for group in (_t_law, _t_profile, _t_globs, _t_voices, _t_characters, _t_headings, _t_phrases, _t_references,
                  _t_allow, _t_output, _t_text, _t_own_limits):
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                group(check)
        except Exception as e:   # a crash is a failed fixture, never a crashed self-test
            check(f"{group.__name__} ran without raising", False, f"{type(e).__name__}: {e}")
    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 0 if not state["failures"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
