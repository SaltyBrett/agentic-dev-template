#!/usr/bin/env python3
"""
session_start.py — the cold start runs itself, and compaction gives back what it took.

WHAT IT DOES
------------
A Claude Code SessionStart hook (`.claude/settings.json`, matchers startup, clear and compact). Its
plain-text stdout is added to Claude's context. SessionStart cannot block, so it always exits 0.

startup, clear  runs the identity gate, `git pull --ff-only`, session-verify and doc-queue, the gates
                through pre-commit exactly as `AGENTS.md` runs them, doc-queue's verdict with each
                story queued for the technical writer; reports whether both hook types are
                installed and whether a CLAUDE.md on the path hides `AGENTS.md`; writes the
                journal's start line; prints the results, the persona, the session's kickoff, the
                newest sprint-status entry, and any notes or journal an unfinished session left.
compact         runs nothing that judges the tree, which is dirty mid-session by design (a verify
                there would report the previous session unclosed); prints the working notes, the
                persona, the uncommitted paths, the journal's tail, the kickoff and the newest entry.

The persona: the kickoff names an agent in .claude/agents/. A session started with
`claude --agent <slug>` holds its prompt as the system prompt, and the event's `agent_type` says
so; any other session gets the prompt here, keeping Claude Code's own system prompt, which
`--agent` replaces whole.

The output stays under Claude Code's 10,000-character cap on injected text; past it Claude gets a
2,000-character preview and is not told to read the rest. Sections are cut lowest priority first,
and a cut section names the file that holds it whole.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It never prints `AGENTS.md`: Claude Code already loaded it, and a second copy costs context. It replaces none of the cold start's reading, and it is not
enforcement: the git hooks and CI are. A hook failure prints one line saying the cold start must
be run by hand.

Usage:  (hook)  python3 scripts/session_start.py        # event JSON on stdin
        pre-commit run session-start-selftest --all-files
        python3 scripts/session_start.py --self-test
Exit 0 always as a hook; the self-test exits 1 on a failure.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import session_closeout as closeout  # noqa: E402 — the section parser, the session rule, the verify command
import session_journal as journal  # noqa: E402 — the journal and the notes

BUDGET = 9500          # under the 10,000-character cap, with room for Claude Code's own wrapping
GATE_TIMEOUT = 120     # seconds per command
JOURNAL_TAIL = 25
STATUS_LIMIT = 15
IDENTITY_COMMAND = ["pre-commit", "run", "agent-execution-identity", "--all-files", "--verbose"]
# --no-rebase: with `pull.rebase` set, a pull refuses any dirty tree even when there is nothing to
# pull; a fast-forward needs neither a rebase nor a clean tree (observed in S2).
PULL_COMMAND = ["git", "pull", "--ff-only", "--no-rebase"]
VERIFY_COMMAND = shlex.split(closeout.VERIFY_COMMAND)
# --verbose: pre-commit hides a passing hook's output, and the queue it lists is the report.
QUEUE_COMMAND = ["pre-commit", "run", "doc-queue", "--hook-stage", "manual", "--all-files", "--verbose"]
QUEUE_LINES = 8
# A queued story, or a violation under its lowercase rule; pre-commit's own `[ERROR]` is neither.
QUEUE_ITEM = re.compile(r"^(queued |\[[a-z-]+\] )")
# Each of these, in the working directory or any parent, makes Claude Code read it instead of
# AGENTS.md; the user-level ~/.claude/CLAUDE.md does not count (reference_claude_code_agents_md).
SHADOWS = ("CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md")

Runner = Callable[[list[str], Path], "tuple[int | None, str]"]


class Section(NamedTuple):
    title: str
    body: str
    priority: int   # 1 is cut last
    source: str     # the file that holds the text whole, named when the text is cut


def run(cmd: list[str], root: Path) -> tuple[int | None, str]:
    try:
        out = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=GATE_TIMEOUT, check=False)
        return out.returncode, out.stdout + out.stderr
    except FileNotFoundError:
        return None, f"`{cmd[0]}` is not on PATH"
    except subprocess.TimeoutExpired:
        return None, f"timed out after {GATE_TIMEOUT}s"


def last_line(out: str) -> str:
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "(no output)"


# ==============================================================================
# Pieces
# ==============================================================================

def render(header: str, sections: list[Section]) -> str:
    return header.rstrip() + "\n" + "".join(f"\n## {s.title}\n\n{s.body.rstrip()}\n" for s in sections)


def fit(header: str, sections: list[Section], budget: int = BUDGET) -> str:
    """Render, cutting the lowest-priority sections first until the text fits the budget."""
    secs = list(sections)
    text = render(header, secs)
    for prio in sorted({s.priority for s in secs}, reverse=True):
        for i, s in enumerate(secs):
            over = len(text) - budget
            if over <= 0:
                return text
            if s.priority != prio:
                continue
            marker = f"\n\n[cut to fit the context cap; the whole text is in {s.source}]"
            keep = len(s.body) - over - len(marker)
            body = s.body[:keep].rstrip() + marker if keep >= 200 else f"[omitted to fit the context cap; read {s.source}]"
            secs[i] = s._replace(body=body)
            text = render(header, secs)
    if len(text) > budget:  # the header and the markers alone overflow: a hard cut, never over the cap
        text = text[: budget - 40].rstrip() + "\n[cut at the context cap]\n"
    return text


def shadows(root: Path, home: Path) -> list[Path]:
    found = []
    for d in (root, *root.parents):
        for rel in SHADOWS:
            p = d / rel
            if p.is_file() and not (d == home and rel == ".claude/CLAUDE.md"):
                found.append(p)
    return found


# The hook types the config installs (`default_install_hook_types`), the pre-push gate among them.
HOOK_TYPES = ("pre-commit", "commit-msg", "pre-push")


def missing_hook_types(root: Path) -> list[str] | None:
    out = subprocess.run(["git", "rev-parse", "--git-path", "hooks"], cwd=root, capture_output=True,
                         text=True, check=False)
    if out.returncode != 0:
        return None
    hooks = Path(out.stdout.strip())
    hooks = hooks if hooks.is_absolute() else root / hooks
    return [t for t in HOOK_TYPES if not (hooks / t).is_file()]


def newest_entry(status_text: str) -> str | None:
    _, secs = closeout.sections(status_text)
    for head, body in secs:
        if closeout.STATUS_ENTRY.match(f"## {head}"):
            lines = body.strip().splitlines()
            while lines and lines[-1].strip() in ("---", ""):
                lines.pop()
            return f"## {head}\n\n" + "\n".join(lines)
    return None


def session_number(root: Path, sid: str, journal_text: str, from_journal: bool) -> int | None:
    """After compaction, the journal's start line for this session decides. Otherwise the gate's
    rule: the newest sprint-status entry, plus one when the next kickoff already exists."""
    if from_journal:
        found = None
        for rec in journal.journal_records(journal_text):
            m = re.match(rf"^- \S+ {re.escape(sid)} start S(\d+)\b", rec)
            if m:
                found = int(m.group(1))
        if found is not None:
            return found
    status = root / "sprint" / "sprint-status.md"
    if not status.is_file():
        return None
    return closeout.current_session(status.read_text(encoding="utf-8"),
                                    lambda n: (root / "sprint" / "handoffs" / f"KICKOFF_S{n}.md").is_file())


def read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None


def kickoff_text(root: Path, n: int | None) -> str | None:
    return read(root / "sprint" / "handoffs" / f"KICKOFF_S{n}.md") if n else None


def kickoff_section(root: Path, n: int | None, priority: int) -> Section:
    rel = f"sprint/handoffs/KICKOFF_S{n}.md"
    text = kickoff_text(root, n)
    body = text.strip() if text else f"No `{rel}` exists (a fresh project's S1 starts without one)."
    return Section(f"Kickoff for S{n} ({rel}, verbatim)", body, priority, rel)


def persona_section(root: Path, kickoff: str | None, agent_type: str | None, priority: int) -> Section | None:
    """The kickoff names an agent; the session holds its prompt either as its system prompt (run with
    `claude --agent <slug>`, which Claude Code reports as `agent_type`) or as this section. A plain
    session keeps Claude Code's own system prompt, which `--agent` replaces."""
    slug = closeout.field(kickoff, "Persona") if kickoff else None
    if not slug:
        return None
    rel = f".claude/agents/{slug}.md"
    if agent_type == slug:
        return Section(f"Persona: {slug}", f"The kickoff names `{slug}`, and this session runs as that agent "
                       f"(`claude --agent {slug}`), so its prompt is the system prompt.", priority, rel)
    text = read(root / rel)
    if text is None:
        return Section(f"Persona: {slug}", f"The kickoff names `{slug}`, and `{rel}` does not exist, so no persona "
                       "prompt is in this context; the session gate refuses a kickoff naming an unregistered persona.",
                       priority, rel)
    prompt = closeout.persona_invocation(text)
    running = (f"as `{agent_type}`, not the kickoff's agent, so `{agent_type}`'s prompt is the system prompt and"
               if agent_type else "with no agent, so Claude Code's own system prompt stands and")
    return Section(f"Persona: {slug} ({rel}, its prompt verbatim)",
                   f"The kickoff names `{slug}`. This session runs {running} the persona's prompt follows.\n\n{prompt}",
                   priority, rel)


PROFILE_REL = "writing-profile.yaml"


def voice_traits(text: str) -> str:
    """A voice file's `## Traits` section; a custom voice's sample stays in its file."""
    m = re.search(r"^## Traits[ \t]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def profile_voice(text: str, slug: str) -> tuple[str | None, str]:
    """The voice the writing profile gives an agent and where it came from, or None and why."""
    try:
        import yaml
    except ImportError:
        return None, "PyYAML is not in this python3, so the profile was not read"
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        data = None
    if not isinstance(data, dict):
        return None, "the profile does not parse, which the writing gate reports"
    agents = data.get("agents") if isinstance(data.get("agents"), dict) else {}
    if agents.get(slug):
        return str(agents[slug]), "its `agents:` entry"
    return (str(data["default"]), "the profile's `default:`") if data.get("default") else (None, "the profile names no default")


def voice_section(root: Path, slug: str | None, priority: int) -> Section | None:
    """The session persona's voice, with its traits; a document's own voice
    wins in the document."""
    text = read(root / PROFILE_REL)
    if not slug or text is None:
        return None
    voice, source = profile_voice(text, slug)
    if voice is None:
        return Section("Voice", f"`{slug}`'s voice is its `agents:` entry in `{PROFILE_REL}`, or the profile's "
                       f"`default:`; {source}: read it.", priority, PROFILE_REL)
    rel = f"docs/standards/voices/{voice}.md"
    traits = voice_traits(read(root / rel) or "") or f"`{rel}` holds no `## Traits` section."
    return Section(f"Voice: {voice} ({rel}, its traits)",
                   f"`{slug}` writes in the `{voice}` voice, by {source} in `{PROFILE_REL}`: its commit messages, "
                   "pull request descriptions and replies. In a document the document's own voice wins: "
                   f"`python3 scripts/writing_standard.py --which <path>` names it.\n\n{traits}", priority, rel)


def entry_section(root: Path, priority: int) -> Section | None:
    text = read(root / "sprint" / "sprint-status.md")
    entry = newest_entry(text) if text else None
    return Section("Newest sprint-status entry (sprint/sprint-status.md)", entry, priority,
                   "sprint/sprint-status.md") if entry else None


def journal_tail(text: str) -> str:
    recs = journal.journal_records(text)
    shown = recs[-JOURNAL_TAIL:]
    more = f"({len(recs) - len(shown)} earlier lines in the file)\n" if len(recs) > len(shown) else ""
    return more + "\n".join(shown)


def ensure_notes(root: Path) -> str:
    path = root / journal.NOTES_REL
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(journal.notes_skeleton(), encoding="utf-8")
    return path.read_text(encoding="utf-8")


# ==============================================================================
# The two reports
# ==============================================================================

def roster_lines(root: Path) -> list[str]:
    """The roster against the library: each persona the library has moved
    past. The state gate only notes it, and pre-commit hides a passing hook's output, so the note
    reaches the session here or nowhere. The parser needs PyYAML, which this hook does not."""
    roster = root / closeout.PERSONAS.relative_to(closeout.ROOT)
    library = root / closeout.LIBRARY.relative_to(closeout.ROOT)
    if not roster.is_dir() or not library.is_dir():
        return []
    try:
        import yaml  # noqa: F401 — the persona parser's dependency, checked before it is needed
    except ImportError:
        return ["- Roster: not compared with the library (no PyYAML in this python3); "
                "`pre-commit run session-closeout-check --all-files --verbose` shows it."]
    lines = []
    for p in sorted(roster.glob("*.md")):
        twin = library / p.name
        if twin.is_file():
            state = closeout.library_state(p.read_text(encoding="utf-8"), twin.read_text(encoding="utf-8"))
            if state and state[0] in closeout.NOTE_RULES:
                lines.append(f"- Roster: `{p.stem}`: {state[1]}")
    return lines


def queue_lines(rc: int | None, out: str) -> list[str]:
    """The doc-queue verdict: the gate's summary, each queued story with
    the drain that clears it, and on a failure each violation and what it means."""
    said = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("doc_queue: S") or QUEUE_ITEM.match(ln.strip())]
    summary = next((ln.split(": ", 1)[1] for ln in said if ln.startswith("doc_queue: S")), last_line(out))
    items = [f"  {ln}" for ln in said if QUEUE_ITEM.match(ln)][:QUEUE_LINES]
    if rc == 0:
        return [f"- doc-queue: PASS (exit 0). {summary}.", *items]
    if rc is None or not said:   # pre-commit or the hook is missing: the gate itself never spoke
        return [f"- doc-queue: {'did not run' if rc is None else f'FAILED (exit {rc})'}. {last_line(out)}"]
    return [f"- doc-queue: FAILED (exit {rc}). {summary}.", *items,
            "  A story in the technical writer's queue is overdue or malformed: drain its document with the "
            "doc-drain skill, or correct the row as the gate's output says, before build work."]


def gate_lines(root: Path, runner: Runner, n: int | None, home: Path) -> str:
    lines = []
    rc, out = runner(IDENTITY_COMMAND, root)
    verdict = "PASS" if rc == 0 else ("did not run" if rc is None else "FAILED")
    hit = next((ln.strip() for ln in out.splitlines() if "AGENT EXECUTION IDENTITY GATE" in ln), last_line(out))
    lines.append(f"- Identity gate: {verdict} (exit {rc}). {hit}")
    if rc != 0:
        lines.append("  `AGENTS.md` stops all work until this gate passes.")
    rc, out = runner(PULL_COMMAND, root)
    lines.append(f"- `{' '.join(PULL_COMMAND)}`: exit {rc}. {last_line(out)}")
    rc, out = runner(VERIFY_COMMAND, root)
    if rc == 0:
        lines.append(f"- session-verify: PASS (exit 0). The previous session closed out; this is S{n}.")
    else:
        detail = [ln.strip() for ln in out.splitlines() if ln.strip().startswith(("Rule:", "Detail:"))]
        why = "; ".join(detail[:8]) or last_line(out)
        lines.append(f"- session-verify: FAILED (exit {rc}). {why}")
        lines.append("  `AGENTS.md` makes completing the previous session's closeout this session's first task.")
    lines.extend(queue_lines(*runner(QUEUE_COMMAND, root)))
    lines.extend(roster_lines(root))
    missing = missing_hook_types(root)
    if missing is None:
        lines.append("- Hook types: not a git repository, not checked.")
    elif missing:
        lines.append(f"- Hook types: {', '.join(missing)} NOT installed in this clone. Install with "
                     "`pre-commit install`, which installs every type the config names.")
    else:
        lines.append(f"- Hook types: {', '.join(HOOK_TYPES)} installed in this clone.")
    found = shadows(root, home)
    if found:
        names = ", ".join(str(p) for p in found)
        lines.append(f"- Instruction files: {names} found. Claude Code reads that instead of `AGENTS.md`, so "
                     "`AGENTS.md` is NOT in this context: read it with the Read tool, and remove or rename the "
                     "file.")
    else:
        lines.append("- Instruction files: no CLAUDE.md on the path, so Claude Code loaded `AGENTS.md` itself.")
    return "\n".join(lines)


def startup_report(root: Path, event: dict, runner: Runner, home: Path) -> str:
    source = event.get("source", "startup")
    n = session_number(root, journal.short_session(event), "", from_journal=False)
    jtext = read(root / journal.JOURNAL_REL) or ""
    notes = ensure_notes(root)
    header = (f"Session start: Claude Code ran `scripts/session_start.py` as its SessionStart hook "
              f"(source: {source}). It ran the mechanical steps of the `AGENTS.md` cold start; the "
              f"reading steps remain.")
    secs = [Section("Cold-start gates", gate_lines(root, runner, n, home), 1, "the gate output (re-run the command)")]
    kickoff = kickoff_text(root, n)
    persona = persona_section(root, kickoff, event.get("agent_type"), 1)
    voice = voice_section(root, closeout.field(kickoff, "Persona") if kickoff else None, 1)
    secs += [s for s in (persona, voice) if s]
    secs.append(kickoff_section(root, n, 2))
    entry = entry_section(root, 3)
    if entry:
        secs.append(entry)
    if not journal.notes_blank(notes):
        secs.append(Section(f"Working notes left by an unfinished session ({journal.NOTES_REL})",
                            notes.strip(), 4, journal.NOTES_REL))
    if journal.journal_records(jtext):
        secs.append(Section(f"Journal left by an unfinished session ({journal.JOURNAL_REL}, newest last)",
                            journal_tail(jtext), 5, journal.JOURNAL_REL))
    text = fit(header, secs)
    journal.append(root / journal.JOURNAL_REL,
                   journal.note_line(event, f"start S{n} ({source})", datetime.datetime.now(datetime.timezone.utc)))
    return text


def compact_report(root: Path, event: dict, runner: Runner) -> str:
    jtext = read(root / journal.JOURNAL_REL) or ""
    n = session_number(root, journal.short_session(event), jtext, from_journal=True)
    notes = ensure_notes(root)
    rc, out = runner(["git", "status", "--short"], root)
    paths = [ln for ln in out.splitlines() if ln.strip()] if rc == 0 else []
    status = ("\n".join(paths[:STATUS_LIMIT]) + (f"\n({len(paths) - STATUS_LIMIT} more)" if len(paths) > STATUS_LIMIT else "")
              if paths else ("Nothing uncommitted." if rc == 0 else f"`git status` failed: {last_line(out)}"))
    header = (f"Context restored after compaction: Claude Code ran `scripts/session_start.py` as its "
              f"SessionStart hook (source: compact). This is still S{n}. The conversation was summarized; "
              f"the sections below are the files that hold what it held.")
    kickoff = kickoff_text(root, n)
    persona = persona_section(root, kickoff, event.get("agent_type"), 1)
    voice = voice_section(root, closeout.field(kickoff, "Persona") if kickoff else None, 1)
    secs = [Section(f"Working notes ({journal.NOTES_REL})", notes.strip(), 1, journal.NOTES_REL),
            *[s for s in (persona, voice) if s],
            kickoff_section(root, n, 2),
            Section("Uncommitted paths (git status --short)", status, 3, "`git status`"),
            Section(f"Journal tail ({journal.JOURNAL_REL}, newest last)",
                    journal_tail(jtext) or "No journal lines yet.", 4, journal.JOURNAL_REL)]
    entry = entry_section(root, 5)
    if entry:
        secs.append(entry)
    text = fit(header, secs)
    journal.append(root / journal.JOURNAL_REL,
                   journal.note_line(event, f"compact S{n}", datetime.datetime.now(datetime.timezone.utc)))
    return text


def report(event: dict, runner: Runner = run, home: Path | None = None) -> str:
    root = journal.project_root(event)
    source = event.get("source", "startup")
    if source == "compact":
        return compact_report(root, event, runner)
    if source in ("startup", "clear"):
        return startup_report(root, event, runner, home or Path.home())
    return ""  # resume and fork restore the conversation itself


# ==============================================================================
# Self-test
# ==============================================================================

_KICKOFF = ("# Kickoff - S3\n\n**For session:** S3\n**Persona:** framework-maintainer\n\n"
            f"## 1. Persona\n\n{closeout.persona_line('framework-maintainer')}\n\n"
            "## 2. Cold start\n\nRun the cold start in `AGENTS.md`.\n")
_PROMPT = "You are a senior platform engineer. Your canary is QUINCE."
_AGENT = ("---\nname: framework-maintainer\ndescription: builds gates\nversion: 1\nexpertise:\n  - gates\n"
          f"insists_on:\n  - proof\nchangelog:\n  - 1 - 2026-10-22 - seeded\n---\n\n{_PROMPT}\n")
_QUEUE_OUT = ("Doc Queue....Passed\n- hook id: doc-queue\n- duration: 0.1s\n\n"
              "doc_queue: S3; 1 story(ies) queued for the technical writer\n"
              "  queued ACME-9.3 (Queued: S2, due by S3): `docs/a.md`; drain with `/doc-drain docs/a.md`\n")
_STATUS = ("# Sprint Status\n\n---\n\n## S2 - 2026-10-22 - Second\n\n**Status:** two.\n\n### Done\n\n1. X\n\n---\n\n"
           "## S1 - 2026-10-21 - First\n\n**Status:** one.\n\n---\n")


def _voices(root: Path, profile: str) -> None:
    """A writing profile and two voice files, one of them custom with its sample."""
    (root / PROFILE_REL).write_text(profile, encoding="utf-8")
    voices = root / "docs" / "standards" / "voices"
    voices.mkdir(parents=True, exist_ok=True)
    (voices / "technical.md").write_text("---\nname: technical\ntables: [ai, marketing]\n---\n\n# Technical voice\n\n"
                                         "## Traits\n\n- Register: plain.\n\n## Use it for\n\nRunbooks.\n", encoding="utf-8")
    (voices / "chair.md").write_text("---\nname: chair\ntables: [ai, marketing]\n---\n\n# Chair voice\n\n## Traits\n\n"
                                     "- Sentence length: short.\n\n## Sample\n\n```text\nSAMPLE-CANARY words\n```\n", encoding="utf-8")


def _tree(tmp: Path, kickoff_next: bool = True) -> Path:
    root = tmp / "repo"
    (root / "sprint" / "handoffs").mkdir(parents=True)
    (root / "sprint" / "sprint-status.md").write_text(_STATUS, encoding="utf-8")
    (root / "sprint" / "handoffs" / "KICKOFF_S2.md").write_text(_KICKOFF.replace("S3", "S2"), encoding="utf-8")
    if kickoff_next:
        (root / "sprint" / "handoffs" / "KICKOFF_S3.md").write_text(_KICKOFF, encoding="utf-8")
    (root / ".claude" / "agents").mkdir(parents=True)
    (root / ".claude" / "agents" / "framework-maintainer.md").write_text(_AGENT, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def run_self_test() -> int:
    # A commit hook in a linked worktree exports GIT_DIR, and git run in a scratch directory with it
    # set acts on the real repository: `git init` made it bare. The
    # self-test's git sees none of the hook's.
    for name in [k for k in os.environ if k.startswith("GIT_")]:
        os.environ.pop(name)
    print("\nSession Start Self-Test")
    print("=" * 60)
    failures = total = 0

    def check_(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures, total
        total += 1
        print(f"  {'ok   ' if ok else 'FAIL '} {label}")
        if not ok and detail:
            print(f"        {detail}")
        failures += 0 if ok else 1

    config = Path(__file__).resolve().parents[1] / ".pre-commit-config.yaml"
    if config.is_file():
        import yaml
        named = tuple(yaml.safe_load(config.read_text(encoding="utf-8")).get("default_install_hook_types") or ())
        check_("the hook types the report checks are the ones the config installs", HOOK_TYPES == named,
               f"checked {HOOK_TYPES}, installed {named}")

    big = [Section("Gates", "g" * 900, 1, "gates"), Section("Kickoff", "k" * 5000, 2, "KICKOFF_S3.md"),
           Section("Entry", "e" * 6000, 3, "sprint-status.md"), Section("Journal", "j" * 4000, 4, "journal.md")]
    text = fit("Header.", big)
    check_("an oversized report fits the budget", len(text) <= BUDGET, str(len(text)))
    check_("the highest-priority sections survive whole while lower ones are cut",
           "g" * 900 in text and "k" * 5000 in text, f"len={len(text)}")
    check_("a cut section names the file that holds it whole",
           "read journal.md" in text or "whole text is in journal.md" in text)
    check_("a report that fits is left exactly as rendered",
           fit("Header.", big[:2]) == render("Header.", big[:2]))
    huge = fit("H" * 20000, [Section("A", "a", 1, "x")])
    check_("even a header past the cap is cut under it", len(huge) <= BUDGET, str(len(huge)))
    check_("the verify runs with --all-files, so the stash cannot hide a dirty tree",
           "--all-files" in VERIFY_COMMAND and VERIFY_COMMAND[:3] == ["pre-commit", "run", "session-verify"])

    ok = queue_lines(0, "Doc Queue....Passed\n- hook id: doc-queue\n\ndoc_queue: S9; nothing queued for the technical writer\n")
    check_("an empty queue is one line saying so", ok == ["- doc-queue: PASS (exit 0). S9; nothing queued for the technical writer."],
           str(ok))
    late = queue_lines(1, _QUEUE_OUT.replace("Passed", "Failed") + "doc_queue: BLOCKED — 1 violation(s)\n"
                       "  [overdue] ACME-9.3: queued in S2 for docs/a.md, due by S3; this is S4\n\nHow to fix:\n  overdue: Drain it.\n")
    check_("an overdue queue reports each violation and what it means, never the fix text as an item",
           late[0].startswith("- doc-queue: FAILED (exit 1).") and any(ln.startswith("  [overdue] ACME-9.3: queued in S2") for ln in late)
           and "doc-drain skill" in late[-1] and not any("Drain it." in ln for ln in late), str(late))
    gone = queue_lines(1, "[ERROR] No hook with id `doc-queue` in stage `manual`\n")
    check_("a config without the hook is reported as pre-commit said it, not as an overdue queue",
           gone == ["- doc-queue: FAILED (exit 1). [ERROR] No hook with id `doc-queue` in stage `manual`"], str(gone))
    tagged = queue_lines(1, _QUEUE_OUT.replace("Passed", "Failed") + "[WARNING] unstaged files\n[overdue] ACME-9.3: late\n")
    check_("pre-commit's own [TAG] lines are never read as queue items", not any("WARNING" in ln for ln in tagged)
           and any("[overdue] ACME-9.3" in ln for ln in tagged), str(tagged))
    check_("a queue that could not run says so", queue_lines(None, "`pre-commit` is not on PATH")
           == ["- doc-queue: did not run. `pre-commit` is not on PATH"])

    entry = newest_entry(_STATUS) or ""
    check_("the newest entry is the first `## S<N>` section, without the trailing rule",
           entry.startswith("## S2 - 2026-10-22 - Second") and "### Done" in entry and "S1" not in entry
           and not entry.rstrip().endswith("---"), entry)

    with tempfile.TemporaryDirectory() as tmp:
        root = _tree(Path(tmp).resolve())
        (root / "personas").mkdir()
        lib = root / "personas" / "framework-maintainer.md"
        lib.write_text(_AGENT, encoding="utf-8")
        check_("roster: a copy equal to the library is not mentioned", roster_lines(root) == [], str(roster_lines(root)))
        lib.write_text(_AGENT.replace("description: builds gates", "description: builds other gates"), encoding="utf-8")
        check_("roster: drift is session-verify's failure to report, never repeated here as a note",
               roster_lines(root) == [], str(roster_lines(root)))
        lib.write_text(_AGENT.replace("version: 1", "version: 2").replace("changelog:\n", "changelog:\n  - 2 - 2026-10-23 - more\n")
                       + "More.\n", encoding="utf-8")
        found = roster_lines(root)
        check_("roster: a persona the library has moved past is named, with the version it holds",
               len(found) == 1 and "framework-maintainer" in found[0] and "version 2" in found[0], str(found))
        probe = ("import sys; sys.modules['yaml'] = None; sys.path.insert(0, sys.argv[1]); import session_start as s; "
                 "from pathlib import Path; print(s.roster_lines(Path(sys.argv[2])))")
        out = subprocess.run([sys.executable, "-I", "-c", probe, str(Path(__file__).resolve().parent), str(root)],
                             capture_output=True, text=True, check=False)
        check_("roster: with no PyYAML the hook says it did not compare, and never crashes",
               out.returncode == 0 and "not compared" in out.stdout, (out.stdout + out.stderr).strip()[-300:])
        gates = gate_lines(root, lambda cmd, where: (0, "Passed\n"), 3, Path(tmp))
        check_("roster: the note reaches the cold-start report, beside a passing session-verify",
               "session-verify: PASS" in gates and "- Roster: `framework-maintainer`" in gates, gates)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp).resolve()
        root = _tree(tmp)
        check_("at startup the session is the newest entry plus one when that kickoff exists",
               session_number(root, "abcd1234", "", from_journal=False) == 3)
        (root / "sprint" / "handoffs" / "KICKOFF_S3.md").unlink()
        check_("mid-session, with no next kickoff yet, the session is the newest entry",
               session_number(root, "abcd1234", "", from_journal=False) == 2)
        jtext = "# Session journal\n\n- 2026-10-22T00:00:00Z abcd1234 start S7 (startup)\n- 2026-10-22T00:00:01Z ffff0000 start S9 (startup)\n"
        check_("after compaction this session's own start line decides, not another session's",
               session_number(root, "abcd1234", jtext, from_journal=True) == 7)

        home = tmp / "home"
        (home / ".claude").mkdir(parents=True)
        (home / ".claude" / "CLAUDE.md").write_text("user-level\n", encoding="utf-8")
        check_("the user-level ~/.claude/CLAUDE.md does not count as a shadow",
               [p for p in shadows(home / "code" / "repo", home) if p.parent.parent == home] == [])
        (tmp / "CLAUDE.md").write_text("parent\n", encoding="utf-8")
        (root / "CLAUDE.local.md").write_text("local\n", encoding="utf-8")
        found = shadows(root, home)
        check_("a CLAUDE.local.md in the project and a CLAUDE.md in a parent are both found",
               root / "CLAUDE.local.md" in found and tmp / "CLAUDE.md" in found, str(found))
        (tmp / "CLAUDE.md").unlink()
        (root / "CLAUDE.local.md").unlink()

        s = persona_section(root, _KICKOFF, None, 1)
        check_("with no agent the kickoff's agent prompt is injected verbatim, and Claude Code's prompt stands",
               s is not None and _PROMPT in s.body and "Claude Code's own system prompt stands" in s.body
               and s.source == ".claude/agents/framework-maintainer.md", str(s))
        s = persona_section(root, _KICKOFF, "framework-maintainer", 1)
        check_("run as the kickoff's agent, the session is told so and the prompt is not repeated",
               s is not None and _PROMPT not in s.body and "runs as that agent" in s.body, str(s))
        s = persona_section(root, _KICKOFF, "data-platform-engineer", 1)
        check_("run as another agent, both are named and the kickoff's prompt is injected",
               s is not None and _PROMPT in s.body and "`data-platform-engineer`" in s.body, str(s))
        copied = _KICKOFF.replace(closeout.persona_line("framework-maintainer"), _PROMPT)
        s = persona_section(root, copied, None, 1)
        check_("a kickoff copying the prompt, a form the session gate refuses, is not read as the persona: "
               "the agent file's prompt is injected all the same",
               s is not None and _PROMPT in s.body and s.source == ".claude/agents/framework-maintainer.md", str(s))
        s = persona_section(tmp / "nowhere", _KICKOFF, None, 1)
        check_("a kickoff naming an agent file that does not exist says so",
               s is not None and "does not exist" in s.body, str(s))
        check_("a kickoff naming no persona adds no section",
               persona_section(root, _KICKOFF.replace("**Persona:** framework-maintainer\n", ""), None, 1) is None)

        # The agent's voice
        check_("voice: with no writing profile there is no voice section", voice_section(root, "framework-maintainer", 1) is None)
        _voices(root, "default: technical\nagents:\n  framework-maintainer: chair\n")
        s = voice_section(root, "framework-maintainer", 1)
        check_("voice: the persona's `agents:` entry names its voice, with that voice's traits and never its sample",
               s is not None and "`chair` voice, by its `agents:` entry" in s.body and "Sentence length: short." in s.body
               and "SAMPLE-CANARY" not in s.body and "the document's own voice wins" in s.body, str(s))
        s = voice_section(root, "data-engineer", 1)
        check_("voice: an agent the map does not name takes the default voice",
               s is not None and "`technical` voice, by the profile's `default:`" in s.body and "Register: plain." in s.body, str(s))
        (root / PROFILE_REL).write_text("agents: [\n", encoding="utf-8")
        s = voice_section(root, "framework-maintainer", 1)
        check_("voice: a profile that does not parse is said so, never a crash", s is not None and "does not parse" in s.body, str(s))
        _voices(root, "default: technical\nagents: {}\n")
        probe = ("import sys; sys.modules['yaml'] = None; sys.path.insert(0, sys.argv[1]); import session_start as s; "
                 "from pathlib import Path; print(s.voice_section(Path(sys.argv[2]), 'framework-maintainer', 1).body)")
        out = subprocess.run([sys.executable, "-I", "-c", probe, str(Path(__file__).resolve().parent), str(root)],
                             capture_output=True, text=True, check=False)
        check_("voice: with no PyYAML the section names the profile to read, and never crashes",
               out.returncode == 0 and "PyYAML is not in this python3" in out.stdout, (out.stdout + out.stderr).strip()[-300:])

        root2 = _tree(tmp / "b")
        _voices(root2, "default: technical\nagents: {}\n")
        calls: list[list[str]] = []

        def fake(cmd: list[str], where: Path) -> tuple[int | None, str]:
            calls.append(cmd)
            if cmd[:3] == ["pre-commit", "run", "agent-execution-identity"]:
                return 0, "AGENT EXECUTION IDENTITY GATE: PASS (probe [uid])\n"
            if cmd[:3] == ["pre-commit", "run", "session-verify"]:
                return 1, "Session Verify....Failed\n    Rule:   dirty-tree\n    Detail: 1 uncommitted path(s)\n"
            if cmd[:3] == ["pre-commit", "run", "doc-queue"]:
                return 0, _QUEUE_OUT
            if cmd[:2] == ["git", "status"]:
                return 0, " M README.md\n"
            return 0, "Already up to date.\n"

        ev = {"session_id": "abcd1234-0000", "source": "startup", "cwd": str(root2)}
        os.environ["CLAUDE_PROJECT_DIR"] = str(root2)
        out = report(ev, fake, home)
        check_("startup runs the identity gate, the pull, the verify and the doc queue, in that order",
               [c[:3] for c in calls] == [["pre-commit", "run", "agent-execution-identity"], ["git", "pull", "--ff-only"],
                                          ["pre-commit", "run", "session-verify"], ["pre-commit", "run", "doc-queue"]]
               and "--no-rebase" in calls[1] and calls[3][3:] == ["--hook-stage", "manual", "--all-files", "--verbose"],
               str(calls))
        check_("startup reports each gate and a failed verify's rule, and says what the failure means",
               "Identity gate: PASS" in out and "session-verify: FAILED (exit 1). Rule:   dirty-tree" in out
               and "first task" in out, out[:600])
        check_("startup reports the doc queue's verdict and each queued story with its drain",
               "- doc-queue: PASS (exit 0). S3; 1 story(ies) queued for the technical writer." in out
               and "  queued ACME-9.3 (Queued: S2, due by S3)" in out and "/doc-drain docs/a.md" in out, out[:900])
        check_("startup prints the persona's prompt, the session's kickoff verbatim and the newest entry",
               _PROMPT in out and "Kickoff for S3" in out and _KICKOFF.strip() in out and "## S2 - 2026-10-22 - Second" in out)
        check_("startup injects the persona's voice beside its prompt", "## Voice: technical" in out and "Register: plain." in out,
               out[:1200])
        calls.clear()
        out_agent = report({**ev, "agent_type": "framework-maintainer"}, fake, home)
        check_("startup under `claude --agent` reads agent_type from the event and does not repeat the prompt",
               _PROMPT not in out_agent and "runs as that agent" in out_agent, out_agent[:600])
        calls.clear()
        (root2 / journal.JOURNAL_REL).unlink()
        out = report(ev, fake, home)
        check_("startup creates the blank notes and writes this session's start line",
               journal.notes_blank((root2 / journal.NOTES_REL).read_text(encoding="utf-8"))
               and "abcd1234 start S3 (startup)" in (root2 / journal.JOURNAL_REL).read_text(encoding="utf-8"))
        check_("blank notes and an empty journal are not shown at startup",
               "unfinished session" not in out)
        calls.clear()
        (root2 / journal.NOTES_REL).write_text(journal.notes_skeleton().replace("## Plan\n\n-", "## Plan\n\n- the plan"),
                                               encoding="utf-8")
        out = report({**ev, "source": "compact"}, fake, home)
        check_("compaction runs no gate, no pull and no verify (the tree is dirty by design)",
               all(c[:2] == ["git", "status"] for c in calls), str(calls))
        check_("compaction re-injects the notes, the persona, the kickoff, the uncommitted paths and the journal",
               "- the plan" in out and _PROMPT in out and "Kickoff for S3" in out and " M README.md" in out
               and "start S3 (startup)" in out and "This is still S3" in out, out[:800])
        check_("compaction re-injects the persona's voice too", "## Voice: technical" in out, out[:1200])
        check_("compaction records itself in the journal",
               "abcd1234 compact S3" in (root2 / journal.JOURNAL_REL).read_text(encoding="utf-8"))
        check_("resume adds nothing: the conversation is restored whole", report({**ev, "source": "resume"}, fake, home) == "")
        os.environ.pop("CLAUDE_PROJECT_DIR", None)

    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        return run_self_test()
    try:
        event = json.load(sys.stdin) if not sys.stdin.isatty() else {}
        text = report(event if isinstance(event, dict) else {})
        if text:
            print(text)
    except Exception as exc:  # noqa: BLE001 — a hook failure is reported to the agent, never raised
        print(f"Session start: `scripts/session_start.py` failed ({type(exc).__name__}: {exc}). "
              "Nothing above was checked; run the `AGENTS.md` cold start by hand.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
