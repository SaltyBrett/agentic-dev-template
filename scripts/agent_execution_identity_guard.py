#!/usr/bin/env python3
"""Block work under a sandbox/offline identity or non-interactive approval policy.

The portable execution-identity law forbids repository commands through a
sandbox account, sandbox identity, restricted token, or private desktop. A
sandbox-bounded session must approve and escalate every local command to the
operator's existing OS identity; an already-unsandboxed session retains
untrusted user approvals.

THE FAILURE THIS CLOSES (decision 2026-09-20-005)
-------------------------------------------------
This guard used to check `.codex/config.toml` with `re.MULTILINE` over the whole
file text. Two false negatives followed, both measured:

    [some.unrelated.table]
    approval_policy = "untrusted"      <- regex matched; tomllib says top level is EMPTY
    approvals_reviewer = "user"

    approval_policy = "untrusted"
    approvals_reviewer = "user"
    this is not = = valid toml [[[     <- regex matched; no TOML parser can load the file

The keys were checked where they were *written*, not where Codex *reads* them.
A regex is not a parser — the same defect the KB freshness gate had.

WHERE THE KEYS ARE CHECKED NOW
------------------------------
Required keys (`approval_policy`, `approvals_reviewer`) must carry the required
value **at top level**, because that is where Codex reads them. Finding one under
another table is not compliance; the diagnostic says where it actually is.

`sandbox_mode` is forbidden **at any depth**, and that asymmetry is deliberate:

  - Whether a nested table is live is external, versioned knowledge about Codex
    (profile tables, for one, are selectable at launch). This gate must not
    encode a guess about which tables another tool activates.
  - If a nested `sandbox_mode` is inert, refusing it costs nothing — the remedy
    is deleting a key that does nothing.
  - If it is live, refusing it is the entire point of the gate.
  - Its presence states intent to configure a sandbox mode regardless, which the
    law forbids outright.

So both directions fail closed: a required key absent from where it counts is a
violation, and a forbidden key present anywhere is a violation. A nested
`approval_policy`/`approvals_reviewer` that *contradicts* the required value is
also a violation, since a profile that weakens the approval policy is exactly the
bypass this gate exists to prevent.

ON THE IDENTITY CHECK (audited, decision 2026-09-20-005)
--------------------------------------------------------
`getpass.getuser()` is **environment-first** by its own implementation: it reads
LOGNAME, USER, LNAME, USERNAME and only then falls back to the password database.
Combined with the three environment variables read alongside it, every input was
environment-derived — so the check had no authoritative source and `USER=…` alone
decided the verdict. That is not the config bug's shape (an unscoped text scan);
it is a provenance defect, trusting an input that is not the authority.

`pwd.getpwuid(os.getuid())` is the authority on POSIX and is now consulted first.
Environment values are still read, as additional signals that cannot be used to
*hide* a real identity. Where `pwd` is unavailable (Windows), the check degrades
to the environment and says so rather than implying a guarantee it cannot make.

Name matching remains a denylist and is still defense in depth: it catches an
identity *named* sandbox/offline, not every sandboxed identity.

Usage:  pre-commit run agent-execution-identity --all-files --verbose
        python3 scripts/agent_execution_identity_guard.py [--self-test]
Exit 0 = pass, 1 = blocked, 2 = cannot run (no TOML parser).
"""

from __future__ import annotations

import getpass
import os
import re
import sys
from pathlib import Path

try:  # Python 3.11+
    import tomllib as toml_reader
except ModuleNotFoundError:  # pragma: no cover - exercised on 3.10 and older
    try:
        import tomli as toml_reader
    except ModuleNotFoundError:
        print(
            "agent_execution_identity_guard: no TOML parser available.\n"
            "    Python 3.11+ provides `tomllib`; older versions need `tomli`.\n"
            "    Through pre-commit this is supplied by additional_dependencies: [tomli]:\n"
            "        pre-commit run agent-execution-identity --all-files\n"
            "    To run directly on an older interpreter: python3 -m pip install tomli",
            file=sys.stderr,
        )
        raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / ".codex" / "config.toml"

FORBIDDEN_IDENTITY = re.compile(r"sandbox|codex.*offline", re.IGNORECASE)

# Must hold this value at TOP LEVEL, where Codex reads it.
REQUIRED_TOP_LEVEL = {
    "approval_policy": "untrusted",
    "approvals_reviewer": "user",
}

# Forbidden at ANY depth — see the module docstring for why the rule is asymmetric.
FORBIDDEN_ANYWHERE = ("sandbox_mode",)


def add_violation(violations: list[str], message: str) -> None:
    if message not in violations:
        violations.append(message)


def walk(obj, path: tuple = ()):
    """Yield (path, value) for every key at every depth of a parsed TOML mapping."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield path + (key,), value
            yield from walk(value, path + (key,))


def check_config(text: str | None) -> list[str]:
    """Validate .codex/config.toml. `text=None` means the file is absent.

    Pure function over the file's text so the self-test can exercise it in memory.
    """
    violations: list[str] = []

    if text is None:
        add_violation(violations, f"required project config is missing: {CONFIG_PATH}")
        return violations

    try:
        data = toml_reader.loads(text)
    except toml_reader.TOMLDecodeError as exc:
        add_violation(
            violations,
            f".codex/config.toml is not valid TOML and cannot be trusted: {exc}",
        )
        return violations

    for key, want in REQUIRED_TOP_LEVEL.items():
        got = data.get(key)
        if got == want:
            continue
        if got is None:
            elsewhere = [
                ".".join(path) for path, _ in walk(data) if len(path) > 1 and path[-1] == key
            ]
            hint = (
                f" (found at {', '.join(elsewhere)}, where Codex does not read it)"
                if elsewhere
                else ""
            )
            add_violation(
                violations, f'.codex/config.toml must set top-level {key} = "{want}"{hint}'
            )
        else:
            add_violation(
                violations,
                f'.codex/config.toml sets top-level {key} = {got!r}, must be "{want}"',
            )

    for path, value in walk(data):
        name = path[-1]
        where = "top level" if len(path) == 1 else f"[{'.'.join(path[:-1])}]"
        if name in FORBIDDEN_ANYWHERE:
            add_violation(
                violations,
                f".codex/config.toml must not set {name} ({where}) — "
                "no forced sandbox or Full-access mode, at any depth",
            )
        if len(path) > 1 and name in REQUIRED_TOP_LEVEL and value != REQUIRED_TOP_LEVEL[name]:
            add_violation(
                violations,
                f".codex/config.toml sets {name} = {value!r} under {where}, contradicting the "
                f"required {REQUIRED_TOP_LEVEL[name]!r} — a table that weakens the approval "
                "policy is the bypass this gate exists to prevent",
            )

    return violations


def collect_identities() -> tuple[set[str], str | None]:
    """Return (identities to check, authoritative name or None).

    The authoritative name comes from the process uid via `pwd`. Environment values are
    included as additional signals, but they cannot be used to hide the uid-derived name.
    """
    authoritative: str | None = None
    try:
        import pwd  # POSIX only

        authoritative = pwd.getpwuid(os.getuid()).pw_name
    except Exception:  # pragma: no cover - Windows, or no passwd entry for the uid
        authoritative = None

    candidates = {
        authoritative or "",
        getpass.getuser() if authoritative is None else "",
        os.environ.get("USERNAME", ""),
        os.environ.get("USER", ""),
        os.environ.get("LOGNAME", ""),
    }
    # getpass.getuser() is environment-first; when pwd gave us the authority we still want the
    # environment names as signals, so read it explicitly rather than relying on the fallback.
    try:
        candidates.add(getpass.getuser())
    except OSError:
        pass

    return {value for value in candidates if value}, authoritative


def check_identities(identities: set[str]) -> list[str]:
    violations: list[str] = []
    for identity in sorted(identities):
        if FORBIDDEN_IDENTITY.search(identity):
            add_violation(violations, f"forbidden execution identity detected: {identity!r}")
    return violations


# ==============================================================================
# SELF-TEST — the config parser proves itself on every commit
# ==============================================================================
#
# Fixtures are in-memory. They exist because the previous parser passed both a
# config whose keys sat under an unrelated table and a config no TOML parser can
# load. Run any new fixture against the OLD regex parser before trusting it: five
# of these seven passed there, and a fixture that passes under the bug tests nothing.

_OK = 'approval_policy = "untrusted"\napprovals_reviewer = "user"\n'

SELF_TEST_CASES = [
    ("a correct config passes", _OK, True),
    (
        "keys under an unrelated table are NOT compliance",
        '[some.unrelated.table]\napproval_policy = "untrusted"\napprovals_reviewer = "user"\n',
        False,
    ),
    ("a missing required key fails", 'approval_policy = "untrusted"\n', False),
    ("a required key with the wrong value fails", 'approval_policy = "never"\napprovals_reviewer = "user"\n', False),
    ("sandbox_mode at top level fails", _OK + 'sandbox_mode = "workspace-write"\n', False),
    (
        "sandbox_mode under a non-top-level table fails too",
        _OK + '[profiles.x]\nsandbox_mode = "workspace-write"\n',
        False,
    ),
    (
        "a table that weakens approval_policy fails",
        _OK + '[profiles.x]\napproval_policy = "never"\n',
        False,
    ),
    ("malformed TOML fails", _OK + "this is not = = valid toml [[[\n", False),
    ("an absent config file fails", None, False),
]


def run_self_test() -> int:
    print("\nExecution Identity Config Parser Self-Test")
    print("=" * 60)
    failures = 0
    for label, text, should_pass in SELF_TEST_CASES:
        try:
            violations = check_config(text)
        except Exception as exc:  # a parser crash is a failure, not an error to propagate
            print(f"  FAIL  {label}\n        raised {type(exc).__name__}: {exc}")
            failures += 1
            continue
        passed = not violations
        if passed == should_pass:
            print(f"  ok    {label}")
        else:
            print(
                f"  FAIL  {label}\n"
                f"        expected {'pass' if should_pass else 'fail'}, got "
                f"{'pass' if passed else 'fail'}"
                + (f" ({violations[0]})" if violations else "")
            )
            failures += 1

    # The "unrelated table" diagnostic must SAY where the key actually is, or the next
    # reader concludes the key is missing and adds a second copy.
    # Must degrade to FAIL, never raise: a self-test that crashes on a broken parser reports
    # nothing useful at exactly the moment it matters.
    misplaced = check_config(SELF_TEST_CASES[1][1])
    msg = misplaced[0] if misplaced else "(no violation reported at all)"
    if misplaced and "some.unrelated.table" in msg:
        print("  ok    the misplaced-key diagnostic names the table it found")
    else:
        print(f"  FAIL  the misplaced-key diagnostic names the table it found\n        {msg}")
        failures += 1

    total = len(SELF_TEST_CASES) + 1
    print(f"\n{'PASSED' if not failures else 'FAILED'}: {total - failures}/{total} parser checks")
    return 1 if failures else 0


def main() -> int:
    if "--self-test" in sys.argv:
        return run_self_test()

    identities, authoritative = collect_identities()
    violations = check_identities(identities)

    text = CONFIG_PATH.read_text(encoding="utf-8") if CONFIG_PATH.is_file() else None
    violations.extend(check_config(text))

    if violations:
        print("AGENT EXECUTION IDENTITY GATE: BLOCKED", file=sys.stderr)
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)
        print(
            "Do not run repository commands through a sandbox identity. Request "
            "operator approval and execute under the existing signed-in OS identity.",
            file=sys.stderr,
        )
        return 1

    identity_display = authoritative or (", ".join(sorted(identities)) or "current OS identity")
    source = "uid" if authoritative else "env-only"
    print(
        "AGENT EXECUTION IDENTITY GATE: PASS "
        f"({identity_display} [{source}]; approval=untrusted; reviewer=user)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
