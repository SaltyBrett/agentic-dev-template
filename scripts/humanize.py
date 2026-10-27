#!/usr/bin/env python3
"""
humanize.py - the humanizer's mechanical half: the writing gate's findings for the files named, the
certain fixes, an editor's proposals applied, the guard on meaning, and a custom voice's sample
counted. The `/humanize` skill runs it; the rewriting is the editor's and the keeping the Chair's.

WHAT IT DOES
------------
  --report <path>...    each file's voice and audience and the writing gate's findings for it
  --fix <path>...       the certain fixes, written in place and counted by kind: curly quotes, the
                        ellipsis, the special spaces and invisible characters, the arrows U+2190 and
                        U+2192, box drawing, U+00A7 to `section`, U+00D7, U+2264, U+2265 and U+2212.
                        A character inside an allowed string is left; every other one is the editor's
  --apply <proposals.json> <path> [--keep N,N] [--out <copy>]
                        an editor's numbered proposals, `[{"n": 1, "old": ..., "new": ..., "finding":
                        ...}]`, each old text found exactly once and none overlapping, applied all or
                        none: the kept ones only, to the file or to a copy
  --guard <before> <after> [--production]
                        the code spans, fenced blocks, link targets, wikilinks and numbers of the
                        text before are those of the text after, in both directions; an item that
                        held a flagged character keeps its letters and digits in order; in a
                        production file a development reference removed is excepted
  --sample <file>       a custom voice's sample counted as the gate counts it, 200 words or more
  --self-test           in-memory fixtures for every mode; its own functions held to the coding
                        standard's production limits
Exit 0 clean, 1 a finding, a guard failure, a proposal that does not apply or a short sample, 2
cannot run (the standard, the voices or the profile unreadable, a file missing or unreadable).

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It rewrites no sentence and keeps nothing: the editor proposes and the Chair keeps, in the skill
(`.claude/skills/humanize/SKILL.md`). It judges nothing the gate does not; it reads the gate's law.
"""
from __future__ import annotations

import contextlib
import io
import json
import re
import sys
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import code_standard  # noqa: E402  - the self-test's check and the measurer of its own limits
import writing_standard as ws  # noqa: E402  - the law, the profile and the judging, read once

ROOT = ws.ROOT

# The certain fixes: each a row of the standard's character table with one
# replacement. Box drawing (U+2500 to U+257F) maps by the character's name; U+00A7 by its place.
CERTAIN = {0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"', 0x2026: "...",
           0x00A0: " ", 0x2007: " ", 0x202F: " ", 0x200B: "", 0x200C: "", 0x200D: "", 0x2060: "", 0xFEFF: "",
           0x2190: "<-", 0x2192: "->", 0x00D7: "x", 0x2264: "<=", 0x2265: ">=", 0x2212: "-"}
BOX = (0x2500, 0x257F)
SECTION_SIGN = "\u00a7"
# A mark that closes what came before it, so the word `section` takes no space ahead of it; anything
# else the sign names (a number, a code span, a quoted title, a bracket) does.
CLOSING_MARKS = ".,;:!?)]}"
FIXABLE = re.compile(SECTION_SIGN + SECTION_SIGN + "?[ \u00a0]?|[" + "".join(chr(c) for c in CERTAIN)
                     + chr(BOX[0]) + "-" + chr(BOX[1]) + "]")
LINE_START = re.compile(r"\s*(?:(?:[-*+]|\d+[.)]|#{1,6}|>)\s+)*")
BLOCK_MARKER = re.compile(r"\s*(?:(?:[-*+]|\d+[.)]|#{1,6}|>)\s+)+")
SENTENCE_END = re.compile(r"[.!?][\"')]*\s+$")
ENDS_SENTENCE = re.compile(r"[.!?][\"')]*\s*$")

LINK_TARGET = re.compile(r"\]\(([^)\s]+)[^)]*\)|<(https?://[^>\s]+)>|(?<![(<])\b(https?://[^\s)>\]`]+)")
WIKILINK = re.compile(r"\[\[[^\[\]\n]+\]\]")
NUMBER = re.compile(r"\d+(?:\.\d+)*")


# ==============================================================================
# The certain fixes
# ==============================================================================

def box(ch: str) -> str:
    """A box-drawing character as ASCII: a horizontal line `-`, a vertical `|`, any join `+`."""
    name = unicodedata.name(ch, "")
    horizontal, vertical = "HORIZONTAL" in name, "VERTICAL" in name
    return "-" if horizontal and not vertical else "|" if vertical and not horizontal else "+"


def opens_sentence(text: str, start: int) -> bool:
    """True where the text at `start` opens a sentence: after a sentence end, after a list, heading
    or quote marker, or at a bare line start that opens a paragraph or follows a sentence end. A
    wrapped line otherwise continues its sentence."""
    line_start = text.rfind("\n", 0, start) + 1
    before = text[line_start:start]
    if SENTENCE_END.search(before) or BLOCK_MARKER.fullmatch(before):
        return True
    if not LINE_START.fullmatch(before):
        return False
    if line_start == 0:
        return True
    previous = text[text.rfind("\n", 0, line_start - 1) + 1: line_start - 1]
    return not previous.strip() or bool(ENDS_SENTENCE.search(previous))


def section_word(text: str, m: re.Match) -> str:
    """U+00A7 as a word: `sections` for two, capitalized where it opens a sentence, a space kept
    before what it names."""
    word = "sections" if m.group(0).startswith(SECTION_SIGN * 2) else "section"
    if opens_sentence(text, m.start()):
        word = word.capitalize()
    nxt = text[m.end(): m.end() + 1]
    return word + (" " if nxt and not nxt.isspace() and nxt not in CLOSING_MARKS else "")


def replacement(text: str, m: re.Match) -> str:
    ch = m.group(0)[0]
    if ch == SECTION_SIGN:
        return section_word(text, m)
    return CERTAIN[ord(ch)] if ord(ch) in CERTAIN else box(ch)


def fix_text(text: str, allow: tuple[str, ...], law: ws.Law) -> tuple[str, Counter]:
    """The text with its certain fixes made, and how many of each kind; an allowed string's
    characters are left as they stand."""
    spans = ws.allowed_spans(text, allow)
    counts: Counter = Counter()

    def sub(m: re.Match) -> str:
        if any(lo <= m.start() and m.end() <= hi for lo, hi in spans):
            return m.group(0)
        cp = ord(m.group(0)[0])
        counts[f"U+{cp:04X} {law.char(cp)[0]}"] += 1
        return replacement(text, m)

    return FIXABLE.sub(sub, text), counts


# ==============================================================================
# An editor's proposals
# ==============================================================================

def read_proposals(text: str) -> list[dict]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ws.LawError(f"the proposals do not parse as JSON: {e}") from e
    if not (isinstance(data, list) and all(isinstance(p, dict) and isinstance(p.get("n"), int)
                                           and isinstance(p.get("old"), str) and p["old"]
                                           and isinstance(p.get("new"), str) for p in data)):
        raise ws.LawError('the proposals must be a list of {"n": <int>, "old": <text>, "new": <text>}')
    return data


def apply_proposals(text: str, proposals: list[dict], keep: set[int] | None) -> tuple[str | None, list[str]]:
    """The text with the kept proposals made, or None and why: each old text found exactly once in
    the text as it stands, none overlapping another, all applied or none."""
    chosen = [p for p in proposals if keep is None or p["n"] in keep]
    problems, places = [], []
    for p in chosen:
        count = text.count(p["old"])
        if count != 1:
            problems.append(f"proposal {p['n']}: its old text occurs {count} times, where it must occur once")
        else:
            places.append((text.index(p["old"]), p))
    places.sort(key=lambda x: x[0])
    for (a, p), (b, q) in zip(places, places[1:]):
        if a + len(p["old"]) > b:
            problems.append(f"proposals {p['n']} and {q['n']} overlap")
    if problems:
        return None, problems
    for start, p in reversed(places):
        text = text[:start] + p["new"] + text[start + len(p["old"]):]
    return text, []


# ==============================================================================
# The guard on meaning
# ==============================================================================

def flagged(value: str) -> bool:
    return any(not (" " <= c <= "~" or c in "\t\n\r") and unicodedata.category(c)[0] not in "LM" for c in value)


def blank_references(text: str) -> str:
    """The text with every development reference blanked, offsets kept, and a code span holding one
    blanked whole: in a production file a reference removed is no loss."""
    spans = [m.span() for _, pattern in ws.REFERENCES for m in pattern.finditer(text)]
    spans += [m.span() for m in ws.CODE_SPAN.finditer(ws.read_doc(text).blank)
              if any(m.start() <= a and b <= m.end() for a, b in spans)]
    chars = list(text)
    for a, b in spans:
        chars[a:b] = [c if c == "\n" else " " for c in chars[a:b]]
    return "".join(chars)


def items(text: str, production: bool) -> list[tuple[str, str]]:
    """What a rewrite must keep: code spans, fenced blocks, link targets, wikilinks and numbers."""
    if production:
        text = blank_references(text)
    doc = ws.read_doc(text)
    found = [("fenced block", text[a:b].strip()) for a, b in ws.fence_spans(text, doc.body)]
    found += [("code span", m.group(0)) for m in ws.CODE_SPAN.finditer(doc.blank) if m.group(2).strip()]
    found += [("link", next(g for g in m.groups() if g)) for m in LINK_TARGET.finditer(doc.prose)]
    found += [("wikilink", m.group(0)) for m in WIKILINK.finditer(doc.prose)]
    found += [("number", m.group(0)) for m in NUMBER.finditer(doc.prose)]
    return found


def skeleton(value: str) -> str:
    return "".join(c for c in value if c.isalnum())


def frontmatter_lost(before: str, after: str) -> list[tuple[str, str]]:
    """A frontmatter that parsed before a rewrite still parses after it, with the same keys: the
    other guards read only the body, and a colon written for a dash in an unquoted value breaks the
    YAML a gate or Claude Code reads."""
    was = ws.parse_frontmatter(before)
    if was is None:
        return []
    now = ws.parse_frontmatter(after)
    if now is None:
        return [("frontmatter", "it no longer parses as YAML")]
    changed = sorted(set(was) ^ set(now))
    return [("frontmatter", f"its keys changed: {', '.join(map(str, changed))}")] if changed else []


def guard(before: str, after: str, production: bool) -> tuple[list, list]:
    """The items lost and the items added: exact where the item held no flagged character, by its
    letters and digits in order where it did, since the editor replaces a flagged character; and a
    frontmatter broken by the rewrite, as lost."""
    left = Counter(items(after, production))
    lost = []
    loose = []
    for item in items(before, production):
        if left[item]:
            left[item] -= 1
        elif flagged(item[1]):
            loose.append(item)
        else:
            lost.append(item)
    for kind, value in loose:
        match = next((k for k in left if left[k] and k[0] == kind and skeleton(k[1]) == skeleton(value)), None)
        if match:
            left[match] -= 1
        else:
            lost.append((kind, value))
    lost += frontmatter_lost(before, after)
    return lost, sorted(k for k, n in left.items() for _ in range(n))


# ==============================================================================
# The modes
# ==============================================================================

def markdown_paths(root: Path, args: list[str]) -> list[str]:
    """The tracked markdown files the arguments name, a folder for every file under it."""
    tracked = ws.tracked_markdown(root)
    paths = []
    for arg in args:
        arg = arg.rstrip("/")
        hits = [p for p in tracked if p == arg or p.startswith(arg + "/")]
        if not hits:
            raise ws.LawError(f"{arg} names no tracked markdown file")
        paths += [p for p in hits if p not in paths]
    return paths


def run_report(root: Path, args: list[str]) -> int:
    paths = markdown_paths(root, args)
    s = ws.setup(root, ws.tracked_markdown(root))
    if s.findings:
        return ws.report(list(s.findings), {}, len(paths))
    for path in paths:
        a = ws.assign(path, s.profile, s.in_template)
        print(f"{path}: voice {a.voice} ({ws.VOICES}/{a.voice}.md), audience {a.audience}")
    found = [f for p in paths for f in ws.judge_text(p, (root / p).read_text(encoding="utf-8"),
                                                       ws.assign(p, s.profile, s.in_template), s)]
    return ws.report(found, {}, len(paths))


def run_fix(root: Path, args: list[str]) -> int:
    paths = markdown_paths(root, args)
    s = ws.setup(root, ws.tracked_markdown(root))
    total: Counter = Counter()
    for path in paths:
        text = (root / path).read_text(encoding="utf-8")
        fixed, counts = fix_text(text, s.profile.allow, s.law)
        if fixed != text:
            (root / path).write_text(fixed, encoding="utf-8")
        total += counts
        print(f"{path}: {sum(counts.values())} certain fix(es)" + (": " + ", ".join(f"{k} x{n}" for k, n in sorted(counts.items()))
                                                                    if counts else ""))
    print(f"\n{sum(total.values())} certain fix(es) in {len(paths)} file(s). What is left is the editor's: run --report.")
    return 0


def _flag(argv: list[str], flag: str) -> str | None:
    return ws._argument(argv, flag) if flag in argv else None


def run_apply(argv: list[str]) -> int:
    i = argv.index("--apply")
    if len(argv) < i + 3:
        raise ws.LawError("--apply needs the proposals file and the file they change")
    proposals = read_proposals(Path(argv[i + 1]).read_text(encoding="utf-8"))
    target = Path(argv[i + 2])
    keep_arg = _flag(argv, "--keep")
    keep = {int(n) for n in keep_arg.split(",") if n.strip()} if keep_arg else None
    text, problems = apply_proposals(target.read_text(encoding="utf-8"), proposals, keep)
    if text is None:
        print("NOT APPLIED, nothing written:\n" + "\n".join(f"  {p}" for p in problems))
        return 1
    out = Path(_flag(argv, "--out") or target)
    out.write_text(text, encoding="utf-8")
    print(f"applied {len(proposals) if keep is None else len(keep)} proposal(s) to {out}")
    return 0


def run_guard(argv: list[str]) -> int:
    i = argv.index("--guard")
    if len(argv) < i + 3:
        raise ws.LawError("--guard needs the text before and the text after")
    before, after = (Path(argv[i + k]).read_text(encoding="utf-8") for k in (1, 2))
    lost, added = guard(before, after, "--production" in argv)
    if not lost and not added:
        print("GUARD PASSED: every code span, fenced block, link, wikilink and number survived")
        return 0
    print("GUARD FAILED: a rewrite changed what the text says")
    for label, found in (("lost", lost), ("added", added)):
        for kind, value in found:
            print(f"  {label} {kind}: {value[:120]!r}")
    return 1


def run_sample(argv: list[str]) -> int:
    words = len(Path(ws._argument(argv, "--sample")).read_text(encoding="utf-8").split())
    ok = words >= ws.SAMPLE_WORDS
    print(f"the sample holds {words} words; a custom voice's holds {ws.SAMPLE_WORDS} or more: {'enough' if ok else 'too few'}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_test()
    try:
        for flag, mode in (("--report", run_report), ("--fix", run_fix)):
            if flag in argv:
                return mode(ROOT, [a for a in argv[argv.index(flag) + 1:] if not a.startswith("--")])
        for flag, mode in (("--apply", run_apply), ("--guard", run_guard), ("--sample", run_sample)):
            if flag in argv:
                return mode(argv)
        print(__doc__)
        return 2
    except (ws.LawError, OSError, UnicodeDecodeError) as e:
        print(f"humanize: cannot run: {e}", file=sys.stderr)
        return 2


# ==============================================================================
# SELF-TEST - every mode against a passing and a failing fixture, in memory
# ==============================================================================

def _fix(text: str, allow: tuple[str, ...] = ()) -> str:
    return fix_text(text, allow, ws._law())[0]


def _t_certain(check) -> None:
    law = ws._law()
    named = all(law.char(cp) != law.other for cp in [*CERTAIN, *range(BOX[0], BOX[1] + 1)])
    check("every certain fix is a row of the standard's character table", named)
    check("U+2014, U+2013 and U+00B7 are the editor's, never the script's",
          not any(cp in CERTAIN for cp in (0x2014, 0x2013, 0x00B7, 0x00B0)) and _fix("a\u2014b \u2013 c") == "a\u2014b \u2013 c")
    check("curly quotes, the ellipsis and the arrows take their one replacement",
          _fix("\u201cit\u2019s\u201d \u2018x\u2019 wait\u2026 a \u2192 b \u2190 c") == "\"it's\" 'x' wait... a -> b <- c")
    check("special spaces become a space and invisible characters nothing",
          _fix("a\u00a0b\u2007c\u202fd e\u200bf\u2060g\ufeffh") == "a b c d efgh")
    check("box drawing: a horizontal line, a vertical line and a join",
          _fix("\u250c\u2500\u2510\n\u2502 \u2502\n\u2514\u2500\u2518 \u2550 \u2551 \u253c") == "+-+\n| |\n+-+ - | +")
    check("the multiplication, comparison and minus signs take theirs",
          _fix("3\u00d73, a \u2264 b \u2265 c, \u22121") == "3x3, a <= b >= c, -1")
    found = fix_text("x\u2026 y\u2026 \u2192", (), law)[1]
    check("the fixes are counted by kind", found == Counter({"U+2026 horizontal ellipsis": 2, "U+2192 arrows": 1}), str(found))
    check("a character inside an allowed string is left", _fix("It read 20\u00d73 here.", ("20\u00d73",)) == "It read 20\u00d73 here.")
    fixed = _fix("Say \u201cit\u201d\u2026\n")
    check("text the script fixed holds no finding of the fixed kinds",
          not ws.judge_text("x.md", fixed, ws.Assignment("technical", "development", ""), ws._setup()), fixed)


def _t_section(check) -> None:
    cases = {"see \u00a79": "see section 9", "see \u00a7 9": "see section 9", "\u00a7\u00a73 and 4": "Sections 3 and 4",
             "\u00a79 says": "Section 9 says", "- \u00a79 moved": "- Section 9 moved", "Done. \u00a79 next": "Done. Section 9 next",
             "(\u00a710)": "(section 10)", "| \u00a72 |": "| section 2 |", "per \u00a7`x`": "per section `x`",
             "in \u00a7.": "in section.", "of \u00a7\"Why\" above": "of section \"Why\" above",
             "\u00a7(a) holds": "Section (a) holds", "see \u00a7[3]": "see section [3]", "per \u00a7, then": "per section, then",
             "name it in\n\u00a711. Keep": "name it in\nsection 11. Keep",
             "It ends.\n\u00a79 opens": "It ends.\nSection 9 opens",
             "One paragraph\n\n\u00a79 opens": "One paragraph\n\nSection 9 opens"}
    for before, after in cases.items():
        check(f"the section sign: {after!r}", _fix(before) == after, repr(_fix(before)))


def _t_apply(check) -> None:
    text = "One fine day. Two fine days. A third.\n"
    props = [{"n": 1, "old": "One fine day.", "new": "A day."}, {"n": 2, "old": "A third.", "new": "The third."}]
    check("proposals apply, each at its one place", apply_proposals(text, props, None)[0] == "A day. Two fine days. The third.\n")
    check("only the kept ones are applied", apply_proposals(text, props, {2})[0] == "One fine day. Two fine days. The third.\n")
    twice = [{"n": 1, "old": "fine", "new": "good"}]
    check("an old text found twice applies nothing", apply_proposals(text, twice, None)[0] is None)
    check("an old text not found applies nothing", apply_proposals(text, [{"n": 3, "old": "absent", "new": "x"}], None)[0] is None)
    overlap = [{"n": 1, "old": "Two fine", "new": "x"}, {"n": 2, "old": "fine days", "new": "y"}]
    check("overlapping proposals apply nothing", apply_proposals(text, overlap, None)[0] is None)
    check("proposals that are not a list of n, old and new cannot be read",
          _raises(read_proposals, '[{"old": "a"}]') and _raises(read_proposals, "not json"))


def _raises(fn, *args) -> bool:
    try:
        fn(*args)
    except ws.LawError:
        return True
    return False


GUARDED = "Run `make test` on 3 hosts, see [the guide](https://x.example/a) and [[reference_fixture]].\n\n```\nkeep 7\n```\n"


def _t_guard(check) -> None:
    def passes(after: str, production: bool = False, before: str = GUARDED) -> bool:
        return guard(before, after, production) == ([], [])
    check("a rewrite that keeps every item passes", passes(GUARDED.replace("Run", "Please run").replace(" and ", ", then ")))
    check("a number dropped fails", not passes(GUARDED.replace("3 hosts", "the hosts")))
    check("a number added fails", not passes(GUARDED.replace("on 3 hosts", "on 3 hosts in 2 racks")))
    check("a code span changed fails", not passes(GUARDED.replace("`make test`", "`make check`")))
    check("a link target changed fails, its text free to change",
          not passes(GUARDED.replace("x.example/a", "x.example/b")) and passes(GUARDED.replace("the guide", "the setup guide")))
    check("a fenced block changed fails", not passes(GUARDED.replace("keep 7", "keep 8")))
    check("a wikilink dropped fails in a development file", not passes(GUARDED.replace(" and [[reference_fixture]]", "")))
    check("a development reference removed passes in a production file",
          passes(GUARDED.replace(" and [[reference_fixture]]", ""), production=True))
    held = "Read `docs/orchestration/knowledge/` first.\n"
    check("a code span holding a development reference, removed whole, passes in a production file",
          passes("Read the knowledge base first.\n", production=True, before=held)
          and not passes("Read the knowledge base first.\n", before=held))
    flagged_before = "Use `a\u2192b` here.\n"
    check("a flagged character replaced inside a code span passes", passes("Use `a->b` here.\n", before=flagged_before))
    check("a code span whose letters changed beside its flagged character fails",
          not passes("Use `a->c` here.\n", before=flagged_before))
    # The frontmatter: a colon in an unquoted value is a second mapping to YAML.
    fm = "---\nname: A gate \u2014 its rule\ndescription: 'One line.'\n---\n\nBody.\n"
    check("a frontmatter value rewritten so it still parses passes",
          passes(fm.replace(" \u2014 ", ", "), before=fm) and passes(fm.replace("A gate \u2014 its rule", "'A gate: its rule'"), before=fm))
    check("a frontmatter that no longer parses fails", not passes(fm.replace(" \u2014 ", ": "), before=fm))
    check("a frontmatter whose keys changed fails", not passes(fm.replace("description: 'One line.'\n", ""), before=fm))
    check("a file with no frontmatter is judged on its body alone", passes("Body text.\n", before="Body text.\n"))


def _t_sample(check) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        short, enough = Path(tmp) / "short.txt", Path(tmp) / "enough.txt"
        short.write_text(" ".join(["word"] * (ws.SAMPLE_WORDS - 1)), encoding="utf-8")
        enough.write_text(" ".join(["word"] * ws.SAMPLE_WORDS), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            codes = run_sample(["--sample", str(short)]), run_sample(["--sample", str(enough)])
        check("a sample under 200 words fails and one of 200 passes", codes == (1, 0), str(codes))


def _t_paths(check) -> None:
    try:
        paths = markdown_paths(ROOT, ["docs/standards/voices/"])
    except ws.LawError:
        paths = []
    check("a folder names every tracked markdown file under it",
          f"{ws.VOICES}/technical.md" in paths and all(p.startswith(ws.VOICES + "/") for p in paths))
    check("a path naming no tracked markdown file cannot run", _raises(markdown_paths, ROOT, ["docs/nowhere"]))


def _t_own_limits(check) -> None:
    own = code_standard.measure_python(Path(__file__).read_text(encoding="utf-8"))
    over = [f"{f.name} ({f.complexity}c/{f.code_lines}l/{f.parameters}p)" for f in own
            if code_standard.judge_function("", f, "production")]
    check("this script's own functions meet the coding standard's production limits", not over, ", ".join(over))
    check("this script is ASCII, naming each character by its escape", Path(__file__).read_text(encoding="utf-8").isascii())


def run_self_test() -> int:
    print("\nHumanize Self-Test")
    print("=" * 60)
    check, state = code_standard._check_factory()
    for group in (_t_certain, _t_section, _t_apply, _t_guard, _t_sample, _t_paths, _t_own_limits):
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                group(check)
        except Exception as e:   # a crash is a failed fixture, never a crashed self-test
            check(f"{group.__name__} ran without raising", False, f"{type(e).__name__}: {e}")
    print(f"\n{'PASSED' if not state['failures'] else 'FAILED'}: {state['total'] - state['failures']}/{state['total']} checks")
    return 0 if not state["failures"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
