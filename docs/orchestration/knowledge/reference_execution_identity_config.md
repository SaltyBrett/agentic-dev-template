---
name: The zero-th gate checks keys where Codex reads them, and identity by uid not environment
description: 'The execution-identity guard checked .codex/config.toml with a whole-file regex, so keys under an unrelated table and a file no TOML parser can load both passed. It now parses with tomllib/tomli: required keys must hold at top level, sandbox_mode is refused at any depth, and both directions fail closed. Separately, every input to its identity check was environment-derived — getpass.getuser() is env-first — so the uid is now the authority. Read before editing the guard or .codex/config.toml.'
teaches: [2026-09-20-005]
verified: 2026-09-20
metadata:
  type: reference
---

# The zero-th gate: check keys where the consumer reads them

> Durable learning. Wikilink: `[[reference_execution_identity_config]]`.
> Companions: [[reference_kb_frontmatter_validation]], [[reference_agent_execution_identity]].

## The failure this closes

`agent_execution_identity_guard.py` validated `.codex/config.toml` with `re.MULTILINE` over the raw
file text. Both of these **passed** the gate:

    [some.unrelated.table]
    approval_policy = "untrusted"        # regex matched; tomllib: top level is EMPTY
    approvals_reviewer = "user"

    approval_policy = "untrusted"
    approvals_reviewer = "user"
    this is not = = valid toml [[[       # regex matched; no TOML parser can load this file

The keys were checked where they were *written*, not where Codex *reads* them — and a file that no
parser can load was certified as compliant. This is the same defect as
[[reference_kb_frontmatter_validation]], in the gate that runs **first**.

## The rule, and why it is asymmetric

- **Required keys** (`approval_policy`, `approvals_reviewer`) must hold their value **at top level**.
  A key found under another table is not compliance. The diagnostic names where it actually is —
  without that, the next reader concludes the key is missing and adds a second copy.
- **`sandbox_mode` is refused at any depth.**

That asymmetry looks inconsistent and is not. **Both directions fail closed:**

1. Whether a nested table is live is external, versioned knowledge about another tool. Codex supports
   profile tables selectable at launch. This gate must not encode a guess about which tables which
   version activates.
2. If a nested `sandbox_mode` is inert, refusing it costs nothing — the remedy is deleting a key that
   does nothing.
3. If it is live, refusing it is the whole point of the gate.
4. Either way, its presence states intent to configure a sandbox mode, which the law forbids outright.

Checking a forbidden key only at top level would have been a **regression**: the old line-based regex
did catch `sandbox_mode` under `[profiles.x]`. A fixture pins that behaviour so the rewrite cannot
quietly lose it.

A nested `approval_policy` or `approvals_reviewer` that contradicts the required value is also
refused — a profile that weakens the approval policy is the exact bypass the gate exists to prevent.

## The identity check: a different defect, worth knowing

Audited alongside the config bug and reported whether or not it was the same shape. **It was not.**
The config bug was an unscoped text scan of a structured file. This is a **provenance** defect:
trusting an input that is not the authority.

`getpass.getuser()` is **environment-first by its own implementation** — LOGNAME, USER, LNAME,
USERNAME, and only then the password database. Read alongside three of those same variables, every
input collapsed into one class. The gate had no authoritative source, and the environment alone
decided the verdict:

    $ USER=sandbox-agent LOGNAME=sandbox-agent python3 -c ...
      identities the guard sees : ['sandbox-agent']
      guard would flag          : True
      authoritative (pwd/uid)   : twdaddy          <- the real user

`pwd.getpwuid(os.getuid())` is the authority on POSIX and is consulted first. The PASS line now
carries its provenance so the distinction is visible at a glance:

    AGENT EXECUTION IDENTITY GATE: PASS (twdaddy [uid]; approval=untrusted; reviewer=user)
    AGENT EXECUTION IDENTITY GATE: PASS (someone [env-only]; …)     # pwd unavailable, e.g. Windows

**What remains true, stated rather than papered over:** name matching is a denylist. It catches an
identity *named* sandbox or offline, not every sandboxed identity, and no local check can prove the
boundary a session was launched under. The guard is defense in depth — but now on an input that is at
least authoritative.

## No parser is not a pass

`tomllib` is stdlib on 3.11+; older interpreters need `tomli`, declared as
`additional_dependencies: [tomli]` on both identity hooks — possible only because the hooks declare
`language: python` ([[reference_precommit_interpreter]]). If neither import succeeds the guard
**exits 2**, never 0, following `kb_frontmatter_scan.py`. A gate that cannot run must not report
success.

## Rules

- Validate a structured config by parsing it, at the path the consuming tool actually reads.
- Decide explicitly, per key, whether "absent where it counts" or "present anywhere" is the failure —
  then fail closed on that. Write the reasoning down; the asymmetry looks like a bug otherwise.
- Ask of any identity or provenance check: *is this input the authority, or merely correlated with
  it?* Environment variables are never the authority for identity.
- Run new fixtures against the broken code first. Six of ten here passed against the old parser and
  were testing nothing ([[reference_kb_frontmatter_validation]] makes the same point).
- A self-test must degrade to FAIL, never raise. The extra assertion here initially threw
  `IndexError` when the parser returned no violations — crashing at exactly the moment it mattered.
