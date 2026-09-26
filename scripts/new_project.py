#!/usr/bin/env python3
"""
new_project.py — initialize a project created from this template.

WHAT THIS REPLACES
------------------
`TEMPLATE_GUIDE.md` Step 8 was a checklist: fill the tokens, clear the example
rows, clear the handoff folder. A checklist is a convention, and this repository
spent 20 September 2026 converting conventions into controls. This is that
conversion for project initialization.

WHAT IT WILL NOT DO, AND WHY
----------------------------
**It never touches `docs/governance/framework_decisions.md`, `sprint/decision-log.md`
bodies, or `docs/orchestration/knowledge/`.** Clearing the decisions is the intuitive
move on a new project and it breaks the first commit. Every knowledge entry declares
`teaches: [<decision-id>]`, and the freshness gate fails when an ID is in neither
decision index:

    UNKNOWN: reference_commit_attribution_gate.md teaches 2026-09-20-001,
             which is in neither decision index                ... exit 1

The framework decisions are not another project's clutter. They are the
provenance explaining why each gate is shaped the way it is, and the knowledge
entries are unreadable without them. Since decision 2026-09-23-003 they live in
`docs/governance/framework_decisions.md`, and `sprint/decision-log.md` ships with
the `[EXAMPLE]` entry alone: the project's log is the project's from birth, its
header filled here and nothing else. A self-test fixture pins this: the NEVER_RESET
paths must not appear in any mutating list.

TWO TOKENS THAT MUST SURVIVE
----------------------------
A naive `{{...}}` replacement corrupts two things in this tree:

    ${{ secrets.AZURE_CLIENT_ID }}   GitHub Actions expression, not a token
    {{PLACEHOLDER}}                  the convention's own name, in prose

Both are left alone, and both have fixtures.

SCOPE OF THE FILL
-----------------
Only files whose tokens are genuinely per-project values are filled. Tokens in
`docs/standards/` and `resources/README.md` are either documentation of the
skeleton or brand values deferred until the project actually produces documents
(decision 2026-09-19-001). Those are reported, never guessed at.

PRIVATE BY DEFAULT
------------------
The template is public (decision 2026-09-25-001); a project made from it is not, unless
it says so. Before writing anything the initializer asks GitHub whether the project's
repository is private and refuses a public one without `--public`. GitHub's own "Use
this template" flow lets the visibility be picked either way at creation time, so the
check lives here, at the first command every project runs. When the visibility cannot
be read (no `gh`, or origin is not on GitHub) it says so and goes on: an unreadable
answer is not a public repository.

Usage:
    python3 scripts/new_project.py --name "..." --platform "..." --scope "..." --prefix ABC
    python3 scripts/new_project.py ... --apply        # writes; without it, dry run
    python3 scripts/new_project.py ... --public       # this project is meant to be public
    python3 scripts/new_project.py --self-test
Exit 0 = clean, 1 = refused or a check failed, 2 = cannot run.
"""

from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import project_profile  # noqa: E402 — shared profile resolution

ROOT = Path(__file__).resolve().parents[1]

# The template's own repository. Running this here would wipe the template's state.
TEMPLATE_REPO_NAME = "agentic-dev-template"

# Bumped when a release is tagged. Written to .template-version so a project can
# answer "which template version am I on" — `--template` squashes history, so
# nothing else records it.
TEMPLATE_VERSION = "v1.0.0"

# Files whose {{TOKENS}} are per-project values. Everything else is documentation
# of the skeleton, or brand values deferred to first document production.
FILL_FILES = [
    "AGENTS.md",
    "CONSTITUTION.md",
    "sprint/decision-log.md",   # header only; ships with the [EXAMPLE] entry alone, the project's from birth
]

# Regenerated from a skeleton rather than edited, because each accumulates the
# template's own state, which means nothing to a new project: session updates in
# sprint-status, and the template's own epics in the tracker. The first derived
# project (TMPL-2.3) started with ten stories, eight of them done, none of them its
# own — and its Summary Statistics described the template's backlog.
REGENERATE_FILES = ["sprint/sprint-status.md", "sprint/story-tracker.md"]

# Removed. The template's own handoff pairs and archive are session state that
# means nothing to a new project; it starts at S1 with no incoming pair, which
# `session_closeout.py --verify` accepts as a fresh project.
CLEAR_GLOBS = ["sprint/handoffs/*.md", "sprint/handoffs/archive/*.md",
               # The resources sync's stamp names the ref THIS repository last synced; a new
               # project starts unsynced and stamps at its first closeout (decision 2026-09-23-007).
               ".resources-version"]

# The template's hook-repository role: the packaging that lets another repository consume its
# gates through `.pre-commit-hooks.yaml` (decision 2026-09-23-005). A project is not a hook
# repository, and a Python project has a pyproject.toml of its own, so both are removed at birth
# and the updater never writes them (its map keeps them; a fixture cross-checks).
TEMPLATE_ONLY = ["pyproject.toml", ".pre-commit-hooks.yaml"]

# Never reset, never regenerated, never deleted. Asserted by a self-test fixture.
# Personas are reusable across projects; a new one is added when a task needs it.
NEVER_RESET = [
    "docs/governance/framework_decisions.md",
    "sprint/decision-log.md",
    "docs/orchestration/knowledge/",
    "docs/personas/",
]

# Left for the project to fill when it needs them. Reported, not an error.
DEFERRED_TOKENS = {
    "TOKENS", "TEMPLATE_FALLBACK", "TEMPLATE_BRANDFONT", "TYPEFACE_PDF",
    "COLOR_PALETTE_PDF", "LOGO_LIGHT_BG", "LOGO_DARK_BG", "LOGO_GUIDE_PDF",
    "LOGO_CLEAR_SPACE_RULE", "CONFIDENTIALITY_FOOTER", "PREFERRED_TERM",
    "DEPRECATED_TERM", "KEYVAULT_NAME", "SPN_NAME", "APP_ID",
}
DEFERRED_PREFIXES = ("HEX_", "RGB_", "PMS_", "CMYK_", "FONT_")

# The convention's own name, written in prose. Filling it rewrites the docs that
# explain the convention.
NEVER_FILL = {"PLACEHOLDER"}

# `{{...}}` NOT preceded by `$`. The negative lookbehind is what protects
# GitHub Actions expressions such as ${{ secrets.AZURE_CLIENT_ID }}.
TOKEN = re.compile(r"(?<!\$)\{\{\s*([^}]+?)\s*\}\}")


def fill(text: str, values: dict[str, str]) -> str:
    """Replace known tokens. Unknown, deferred and protected tokens are left as-is."""
    def swap(match: re.Match) -> str:
        name = match.group(1)
        if name in NEVER_FILL:
            return match.group(0)
        return values.get(name, match.group(0))

    return TOKEN.sub(swap, text)


def remaining_tokens(text: str) -> tuple[set[str], set[str]]:
    """Return (deferred, unknown) token names still present."""
    deferred, unknown = set(), set()
    for match in TOKEN.finditer(text):
        name = match.group(1)
        if name in NEVER_FILL:
            continue
        if name in DEFERRED_TOKENS or name.startswith(DEFERRED_PREFIXES):
            deferred.add(name)
        else:
            unknown.add(name)
    return deferred, unknown


def is_template_repo(origin_url: str | None) -> bool:
    """True when origin points at the template itself. Running here would wipe it."""
    if not origin_url:
        return False
    tail = origin_url.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
    return tail.removesuffix(".git") == TEMPLATE_REPO_NAME


def repo_slug(origin_url: str | None) -> str | None:
    """`owner/name` from an ssh or https remote URL; None when the URL has no such shape."""
    if not origin_url:
        return None
    # The last two path segments, after whatever precedes the final colon: that reads
    # `git@host:owner/name.git`, `https://host/owner/name`, `ssh://git@host:22/owner/name.git`
    # and `https://user:token@host/owner/name` alike.
    path = origin_url.strip().rstrip("/").rsplit(":", 1)[-1]
    parts = [p for p in path.split("/") if p]
    if len(parts) < 2:
        return None
    return f"{parts[-2]}/{parts[-1].removesuffix('.git')}"


def repo_visibility(slug: str | None) -> bool | None:
    """True when the GitHub repository is private, False when public, None when it cannot be
    read: no slug, no `gh`, not signed in, or a host `gh` does not serve."""
    if not slug:
        return None
    try:
        out = subprocess.run(
            ["gh", "repo", "view", slug, "--json", "isPrivate", "--jq", ".isPrivate"],
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return None
    if out.returncode != 0:
        return None
    answer = out.stdout.strip()
    return {"true": True, "false": False}.get(answer)


def visibility_verdict(is_private: bool | None, public_intended: bool) -> str:
    """The private-by-default rule over one reading. `refuse` for a public repository the
    operator did not declare public; `unknown` when the visibility could not be read, which
    is reported and not refused; `ok` otherwise."""
    if is_private is None:
        return "unknown"
    if not is_private and not public_intended:
        return "refuse"
    return "ok"


def origin_url() -> str | None:
    try:
        out = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        return out.stdout.strip() or None
    except OSError:  # pragma: no cover - git absent
        return None


def sprint_status_skeleton(values: dict[str, str]) -> str:
    """A clean sprint-status for a new project. Carries no session history."""
    return f"""# Sprint Status

**Current Phase:** Initialization
**Current Focus:** Project setup from template {TEMPLATE_VERSION}
**Last Updated:** {values['DATE']}
**Updated By:** AI Session 1

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` (setup, update cadence, sprint boundaries).
>
> **READ SELECTIVELY (index-first).** Read the header (Current Phase/Focus) and the newest session
> update first; older updates are context, not required reading. Keep the last 10 updates visible and
> archive older ones — `scripts/session_closeout.py --check` enforces the cap. Markdown only (never JSON).
> Every entry is headed `## S<N> — YYYY-MM-DD — <title>`; the gate reads the session number from it.

---

## S1 — {values['DATE']} — Initialized from template {TEMPLATE_VERSION}

**Status:** {values['PROJECT_NAME']} initialized from the agentic-dev-template ({TEMPLATE_VERSION}).

### Done

1. Created the repository from the template and filled the project tokens.
2. Installed both pre-commit hook types and confirmed the full gate suite passes.

### Blockers

- None.

### Next

S1 has no incoming kickoff, so this list stands in for it. From S2 on, next-session tasks live
in the kickoff, not here.

1. Run the Planning Session Protocol in `docs/standards/sprint_management_standard_v1.0.md`
   against the approved PRD and Architecture to populate `story-tracker.md`. The kickoff for S2
   can only cite stories that exist, so S1 opens the first epic before it closes out.
2. Record the first project decision in `decision-log.md`, its ID prefixed
   (`{values['PREFIX'] or 'ACME'}-YYYY-MM-DD-NNN`), and remove the `[EXAMPLE]` entry: the state gate
   refuses it once a real epic exists. The framework's own decisions are in
   `docs/governance/framework_decisions.md`; knowledge entries declare `teaches:` against them.

---

<!-- Add new session updates ABOVE this line, newest first, headed `## S<N> — YYYY-MM-DD — title` -->
<!-- Each entry: Done (by story ID), Blockers. Next-session tasks live in the kickoff, not here. -->
<!-- Keep the last 10 entries visible; move older ones to sprint/archive/ (the gate enforces the cap) -->
"""


def story_tracker_skeleton(values: dict[str, str]) -> str:
    """A clean tracker for a new project. Carries the [EXAMPLE] epic and no real stories.

    The Summary Statistics are zero and must reconcile with the rows: the session
    state gate counts every non-example epic row on every commit.
    """
    return f"""# Story Tracker

**Last Updated:** {values['DATE']}
**Source:** PRD (see `docs/prd/`)

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` — read it before creating or
> updating stories (use its Planning Session Protocol to build this file from the PRD + Architecture).
>
> **READ SELECTIVELY (index-first).** Do NOT read this file whole. Read the **Summary Statistics** and
> **Dependency Order** below, then open only the epic/story rows relevant to the current task. Keep this
> file markdown (never JSON) and do not accrete changelog paragraphs.

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Stories** | 0 |
| **Not Started** | 0 |
| **In Progress** | 0 |
| **Blocked** | 0 |
| **Completed** | 0 |

---

## How to Use This Tracker

1. **Story IDs** follow the pattern: `{{PREFIX}}-{{Epic#}}.{{Story#}}` (e.g., {values['PREFIX'] or 'INFRA'}-1.1 = Epic 1, Story 1)
2. **Dependencies** list other story IDs that must complete first
3. **Status** values: Not Started | In Progress | Blocked | Done
4. **Required Standards** lists standards to consult before implementation
5. **PRD Ref** links to the functional requirement in the PRD

---

## Dependency Order

```
Define your project's dependency layers here. Example:

INFRA --> DATA_INGEST --> TRANSFORM --> SERVE --> VALIDATE
```

No story in a later layer can start until dependencies in earlier layers are complete.

---

## Epic: INFRA-1 — Environment Setup [EXAMPLE]

| Story ID | Title | Status | Dependencies | Required Standards | PRD Ref |
|----------|-------|--------|--------------|-------------------|---------|
| INFRA-1.1 | Provision development environment | Not Started | — | secrets_management_standard_v1.0.md | — |
| INFRA-1.2 | Configure CI/CD pipeline | Not Started | INFRA-1.1 | doc_control_standard.md | — |
| INFRA-1.3 | Set up monitoring | Not Started | INFRA-1.1 | — | — |

---

<!-- Add new epics and stories below, following the table format above -->
<!-- Update status after each work unit per the Checkpoint Protocol -->
"""


# ==============================================================================
# SELF-TEST — in-memory fixtures, run on every commit
# ==============================================================================

_VALUES = {
    "PROJECT_NAME": "Acme Analytics",
    "PLATFORM_DESCRIPTION": "Fabric on GCC",
    "PROJECT_SCOPE": "Replace legacy reporting",
    "PREFIX": "ACME",
    "DATE": "2026-09-20",
}


def run_self_test() -> int:
    print("\nNew Project Initializer Self-Test")
    print("=" * 60)
    failures = 0

    def check(label: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        if ok:
            print(f"  ok    {label}")
        else:
            print(f"  FAIL  {label}")
            if detail:
                print(f"        {detail}")
            failures += 1

    got = fill("Project: {{PROJECT_NAME}}, prefix {{PREFIX}}", _VALUES)
    check("known tokens are filled", got == "Project: Acme Analytics, prefix ACME", got)

    actions = "    client-id: ${{ secrets.AZURE_CLIENT_ID }}"
    check("GitHub Actions expressions survive", fill(actions, _VALUES) == actions,
          fill(actions, _VALUES))

    prose = "replace all `{{PLACEHOLDER}}` values"
    check("the convention's own name survives", fill(prose, _VALUES) == prose,
          fill(prose, _VALUES))

    check("an unknown token is left, not blanked",
          fill("{{NOT_A_REAL_TOKEN}}", _VALUES) == "{{NOT_A_REAL_TOKEN}}")

    deferred, unknown = remaining_tokens("{{HEX_PRIMARY}} {{KEYVAULT_NAME}} {{WAT}} {{PLACEHOLDER}}")
    check("remaining tokens classify deferred vs unknown",
          deferred == {"HEX_PRIMARY", "KEYVAULT_NAME"} and unknown == {"WAT"},
          f"deferred={sorted(deferred)} unknown={sorted(unknown)}")

    urls = [
        ("git@github.com-personal:SaltyBrett/agentic-dev-template.git", True),
        ("https://github.com/SaltyBrett/agentic-dev-template", True),
        ("https://github.com/SaltyBrett/agentic-dev-template/", True),
        ("git@github.com:SaltyBrett/my-real-project.git", False),
        # A substring check would refuse these. They are different repositories.
        ("git@github.com:SaltyBrett/agentic-dev-template-fork.git", False),
        ("git@github.com:someone/my-agentic-dev-template.git", False),
        (None, False),
    ]
    bad = [u for u, want in urls if is_template_repo(u) is not want]
    check("the template's own origin is refused, a project's is not", not bad, f"misjudged {bad}")

    slugs = [
        ("git@github.com-personal:SaltyBrett/my-real-project.git", "SaltyBrett/my-real-project"),
        ("https://github.com/SaltyBrett/my-real-project", "SaltyBrett/my-real-project"),
        ("https://github.com/SaltyBrett/my-real-project.git/", "SaltyBrett/my-real-project"),
        ("ssh://git@github.com:22/SaltyBrett/my-real-project.git", "SaltyBrett/my-real-project"),
        ("https://user:token@github.com/SaltyBrett/my-real-project", "SaltyBrett/my-real-project"),
        ("not-a-remote", None),
        (None, None),
    ]
    bad = [u for u, want in slugs if repo_slug(u) != want]
    check("owner/name is read from ssh and https remotes alike", not bad, f"misjudged {bad}")

    # Private by default: a public repository is refused unless declared; an unreadable
    # visibility is reported, never treated as public, and never as private either.
    verdicts = [
        ((True, False), "ok"), ((False, False), "refuse"), ((False, True), "ok"),
        ((True, True), "ok"), ((None, False), "unknown"), ((None, True), "unknown"),
    ]
    bad = [(a, visibility_verdict(*a)) for a, want in verdicts if visibility_verdict(*a) != want]
    check("a public repository is refused without --public; unreadable is reported, not refused",
          not bad, f"misjudged {bad}")

    mutating = set(FILL_FILES) | set(REGENERATE_FILES) | set(CLEAR_GLOBS) | set(TEMPLATE_ONLY)
    collisions = [p for p in NEVER_RESET if any(m.startswith(p.rstrip("/")) and m != "sprint/decision-log.md"
                                                for m in mutating)]
    knowledge_touched = [m for m in mutating if m.startswith("docs/orchestration/knowledge")]
    check("the knowledge base is in no mutating list", not knowledge_touched and not collisions,
          f"{knowledge_touched or collisions}")

    # The hook-repository packaging is removed, and only removed: a template-only file that
    # were also filled or regenerated would be written and then deleted, or deleted and then
    # reported as missing, depending on list order.
    overlap = set(TEMPLATE_ONLY) & (set(FILL_FILES) | set(REGENERATE_FILES))
    check("the hook-repository packaging is removed at birth and appears in no other list",
          set(TEMPLATE_ONLY) == {"pyproject.toml", ".pre-commit-hooks.yaml"} and not overlap,
          f"overlap={sorted(overlap)}")

    check("decision-log is filled but never regenerated or deleted",
          "sprint/decision-log.md" in FILL_FILES
          and "sprint/decision-log.md" not in REGENERATE_FILES
          and not any("decision-log" in g for g in CLEAR_GLOBS))
    check("the framework decisions file is preserved and in no mutating list",
          "docs/governance/framework_decisions.md" in NEVER_RESET
          and not any("framework_decisions" in m for m in mutating))

    _, unknown_in_skeleton = remaining_tokens(sprint_status_skeleton(_VALUES))
    check("the generated sprint-status carries no unfilled tokens", not unknown_in_skeleton,
          f"{sorted(unknown_in_skeleton)}")

    # The tracker is judged by the gate that will read it on every commit, not by
    # a second opinion. A skeleton that still carried the template's TMPL epics
    # would report real story IDs here and non-zero counts.
    import session_closeout  # noqa: E402 — the state gate's own parser
    tracker = story_tracker_skeleton(_VALUES)
    computed, declared, ids = session_closeout.tracker_counts(tracker)
    _, unknown_in_tracker = remaining_tokens(tracker)
    check("the generated tracker carries no real stories and reconciles at zero",
          not ids and not session_closeout.tracker_violations(computed, declared)
          and "[EXAMPLE]" in tracker,
          f"ids={sorted(ids)} computed={computed} declared={declared}")
    check("the generated tracker carries no unfilled tokens", not unknown_in_tracker,
          f"{sorted(unknown_in_tracker)}")
    check("the tracker is regenerated, never filled in place",
          "sprint/story-tracker.md" in REGENERATE_FILES
          and "sprint/story-tracker.md" not in FILL_FILES)

    check("a template version is set", bool(re.fullmatch(r"v\d+\.\d+\.\d+", TEMPLATE_VERSION)),
          TEMPLATE_VERSION)

    total = 17
    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} checks")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a project created from this template")
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--platform", default="", help="Platform and tech stack")
    parser.add_argument("--scope", default="", help="One-line scope")
    parser.add_argument("--prefix", default="", help="Story ID prefix, e.g. ACME")
    parser.add_argument(
        "--profile", choices=project_profile.PROFILES,
        help="gcc = Government-cloud constraints apply; commercial = none. Required.",
    )
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry run)")
    parser.add_argument("--force", action="store_true", help="Override the template-repo refusal")
    parser.add_argument("--public", action="store_true",
                        help="This project is meant to be public (the default refuses a public repository)")
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fixtures and exit")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.name:
        print("new_project: --name is required (or use --self-test)", file=sys.stderr)
        return 2
    if not args.profile:
        print(
            "new_project: --profile is required. A project starts under Government-cloud\n"
            f"    constraints or under none, and the choice is not guessable:\n"
            f"      --profile gcc         GCC/Gov law applies; banned-feature set enforced\n"
            f"      --profile commercial  no GCC constraints; that law is not carried here\n"
            "    It is written to .project-profile and drives both the documents and the gate.",
            file=sys.stderr,
        )
        return 2

    url = origin_url()
    if is_template_repo(url) and not args.force:
        print(f"new_project: REFUSED — origin is the template itself ({url}).")
        print("  Running here would clear the template's own sprint state.")
        print("  Create a project first:")
        print(f"    gh repo create <name> --template SaltyBrett/{TEMPLATE_REPO_NAME} --private --clone")
        print("  Use --force only if you are deliberately re-scaffolding the template.")
        return 1

    slug = repo_slug(url)
    verdict = visibility_verdict(repo_visibility(slug), args.public)
    if verdict == "refuse":
        print(f"new_project: REFUSED — {slug} is PUBLIC and --public was not given.")
        print("  A project made from this template is private by default (decision 2026-09-25-001).")
        print("  Make it private, or say that public is intended:")
        print(f"    gh repo edit {slug} --visibility private --accept-visibility-change-consequences")
        print("    python3 scripts/new_project.py ... --public")
        return 1
    if verdict == "unknown":
        print(f"new_project: note — the visibility of {slug or 'origin'} could not be read (no gh, "
              "or not a GitHub remote); the private-by-default rule is not checked here.")

    values = {
        "PROJECT_NAME": args.name,
        "PLATFORM_DESCRIPTION": args.platform,
        "PROJECT_SCOPE": args.scope,
        "PREFIX": args.prefix,
        "DATE": datetime.date.today().isoformat(),
    }
    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"\nNew Project Initializer — {mode}")
    print("=" * 60)
    print(f"Project: {args.name}   Template: {TEMPLATE_VERSION}")

    planned: list[str] = []
    # The post-apply content of every managed file, built whether or not we write.
    # A dry run must report the state it WOULD produce; reading them back off disk
    # reports the pre-fill state and claims the fill failed.
    final_texts: dict[str, str] = {}

    for rel in FILL_FILES:
        path = ROOT / rel
        if not path.is_file():
            continue
        before = path.read_text(encoding="utf-8")
        after = fill(before, values)
        final_texts[rel] = after
        if before != after:
            n = sum(1 for _ in TOKEN.finditer(before)) - sum(1 for _ in TOKEN.finditer(after))
            planned.append(f"fill      {rel}  ({n} token(s))")
            if args.apply:
                path.write_text(after, encoding="utf-8")

    skeletons = {
        "sprint/sprint-status.md": (sprint_status_skeleton, "session history cleared"),
        "sprint/story-tracker.md": (story_tracker_skeleton, "the template's own epics cleared"),
    }
    for rel in REGENERATE_FILES:
        build, why = skeletons[rel]
        final_texts[rel] = build(values)
        planned.append(f"regen     {rel}  ({why})")
        if args.apply:
            (ROOT / rel).write_text(final_texts[rel], encoding="utf-8")

    for pattern in CLEAR_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            planned.append(f"remove    {path.relative_to(ROOT)}")
            if args.apply:
                path.unlink()

    for rel in TEMPLATE_ONLY:
        path = ROOT / rel
        if path.is_file():
            planned.append(f"remove    {rel}  (the template's hook-repository role)")
            if args.apply:
                path.unlink()

    stripped = 0
    for path in project_profile.markdown_files(ROOT):
        before = path.read_text(encoding="utf-8")
        after = project_profile.strip_profiles(before, args.profile)
        if before != after:
            stripped += 1
            if args.apply:
                path.write_text(after, encoding="utf-8")
    if stripped:
        planned.append(f"profile   {stripped} document(s) stripped to `{args.profile}`")

    planned.append(f"write     .project-profile  ({args.profile})")
    if args.apply:
        (ROOT / ".project-profile").write_text(args.profile + "\n", encoding="utf-8")

    planned.append(f"write     .template-version  ({TEMPLATE_VERSION})")
    if args.apply:
        (ROOT / ".template-version").write_text(TEMPLATE_VERSION + "\n", encoding="utf-8")

    for line in planned:
        print(f"  {line}")

    print(f"\n  preserved: {', '.join(NEVER_RESET)}")
    print("             (knowledge entries declare `teaches:` against the framework decisions;")
    print("              the project's log ships with the [EXAMPLE] entry alone)")

    # Only MANAGED files can hold an "unknown" token. Tokens elsewhere are either
    # deferred brand/Azure values or documentation of the skeleton itself —
    # `docs/standards/` describes {{DATE}} and {{N}} on purpose. Scanning the whole
    # tree for unknowns reports a filled token as missing, which reads as a failure.
    unknown: set[str] = set()
    deferred_files: dict[str, set[str]] = {}

    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = str(path.relative_to(ROOT))
        # Managed files are judged on what this run produces, not what is on disk.
        text = final_texts.get(rel) or path.read_text(encoding="utf-8", errors="ignore")
        d, u = remaining_tokens(text)
        if rel in final_texts:
            unknown |= u
        if d:
            deferred_files[rel] = d

    if deferred_files:
        total = len({t for s in deferred_files.values() for t in s})
        print(f"\n  {total} deferred token(s), to fill when the project needs them:")
        for rel, names in sorted(deferred_files.items()):
            print(f"    {rel}  ({len(names)})")
    if unknown:
        print(f"\n  UNKNOWN token(s) left in a managed file: {', '.join(sorted(unknown))}")
        print("    These should have been filled. Check the argument list.")

    if not args.apply:
        print("\nDRY RUN — nothing written. Re-run with --apply.")
        return 0

    print("\nRunning the gate suite to prove the new project starts green...")
    result = subprocess.run(["pre-commit", "run", "--all-files"], cwd=ROOT, check=False)
    if result.returncode != 0:
        print("\nBLOCKED: the suite did not pass. Fix before the first commit.")
        return 1
    print("\nPASSED: project initialized and every gate is green.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
