---
authority: the coding standard — the core limits on code a change adds or edits, their exceptions, and how each stack measures them
implements: [2026-10-22-003, 2026-10-24-007, 2026-10-24-008, 2026-10-24-009]
verified: 2026-10-24
---

# Coding Standard v1.0

**Purpose:** Code that a reviewer can read, a test can pin down and a later change can safely touch,
held by gates rather than by goodwill. Agents write verbose, run-on, repetitive code when nothing
stops them, and a standard that is prose stops nothing (decision 2026-10-22-003).

---

## 1. Scope

- A project opts in by choosing a stack profile at its planning session (§6). The standard judges
  the code a change adds or edits, never the codebase as it stood: a function is changed when the
  change adds it or edits a line of it.
- An edited function already over a limit is brought under it or recorded at its current value
  (§4). Untouched code is not judged.
- Three layers hold it: the mechanical limits (§2), judged by the gate; the process, in the team's
  stages (`/story`, decision 2026-10-24-004); and judgement, in `.claude/rules/code-quality.md` and
  the code reviewer (§7).

---

## 2. The core limits

The same numbers in every stack (decision 2026-10-24-007). A stack's tools are configured to them,
stricter or equal, never looser.

| Limit | Production code | Test code |
|-------|-----------------|-----------|
| Cyclomatic complexity per function | at most 15 | at most 10 |
| Code lines per function, blanks and comments excluded | at most 60 | at most 100 |
| Parameters per function, a declared receiver (`self`) included | at most 5 | at most 5 |
| Clones a change adds (50 tokens and 5 lines, size caps lifted) | none | reported, not gated |
| Coverage of the change's new lines | at least 80% | — |
| File length | a file a change grows past 500 production lines is flagged to the code reviewer, not refused | — |

- A test helper is production code for these limits; only the test functions the profile names are
  test code.
- The codebase's duplication rate never rises.
- The evidence for each number, and what a limit cannot catch, is in decision 2026-10-24-007 and
  [[reference_coding_standard_calibration]].

---

## 3. Measurement is proved

A gate that measures nothing reports green (decision 2026-10-24-008).

- Each stack's measurer passes a fixture of its language's hard cases before it counts: Rust
  lifetimes and raw strings, a TypeScript method with a return type and a bare `catch`, Python's
  `match`. Its version is pinned.
- On every run the gate checks recall: the measurer reports as many functions in each changed file
  as the file defines, or the gate fails. A changed function the measurer did not report is never a
  pass.
- Generated code is declared by path in the profile; a generated-code marker anywhere else is
  refused.

---

## 4. Exceptions

- An exception is an entry in `code-exceptions.yaml` at the repository root naming the file, the
  function, the metric, its recorded value, its category and the reason. The categories: data or
  table, parser or state machine, exhaustive dispatch over a closed set, generated code, measured hot
  path. "It is complex" is no reason.
- The code reviewer approves each new entry in its review. An entry's value may fall and never
  rises; the gate fails a function that grows past it.
- A tool's own suppression comment counts only with a matching entry.

---

## 5. What the gate runs on a change

1. The function limits of §2 over every changed function, after the recall check of §3.
2. The clone check: no clone of existing code among the change's added lines, unless an entry
   records it.
3. Coverage of the change's new lines, by the profile's coverage tool.
4. The formatter, the linter, the type checker and the dependency and license audit, each passing.
5. The file-length signal, reported to the code reviewer.

---

## 6. Stack profiles: the mapping rule

A stack profile names one pinned tool for each slot. A stack with an empty slot is not adoptable;
the planning session chooses the profile.

| Slot | What the tool does |
|------|--------------------|
| Function measurer | complexity, code lines and parameters per function, proved per §3 |
| Clone detector | clones among the change's added lines |
| Formatter | the stack's canonical format, checked, not rewritten, by the gate |
| Linter | the stack's linter, its limits configured to §2 |
| Type checker | the stack's strictest practical type check |
| Coverage | coverage of the change's new lines |
| Dependency and license audit | known vulnerabilities, and licenses against the project's policy |
| Trigger paths | the paths that show decision 2026-10-24-005's triggers: dependency manifests and lockfiles, migrations and schemas, auth and crypto, infrastructure as code, CI and hooks, the license file |

The starting candidates for each slot, Rust, Python and TypeScript, are in decision
2026-10-24-008; each profile's own story proves and pins its tools (TMPL-4.3 to TMPL-4.5).

---

## 7. Judgement and review

- `.claude/rules/code-quality.md` holds the judgement no gate makes, path-scoped to code and opening
  with `CONSTITUTION.md` §4A ([[reference_claude_code_rules]]).
- The code reviewer, `personas/code-reviewer.md`, is never the implementer and never edits the code;
  it first checks that the gate measured the change, and it blocks only on a violation of this
  standard, unmeasured code, an unjustified exception or a new clone, never on taste
  (decision 2026-10-24-009).
- The security audit is `security-engineer`'s brief in the team's security stage (decision
  2026-10-24-009).

---

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.0 | 2026-10-24 | 2026-10-24-007, 2026-10-24-008, 2026-10-24-009, 2026-10-22-003 | Written as the authority for the coding standard (TMPL-4.2): the core limits, their scope, the exceptions file, proved measurement and the stack profiles' mapping rule | pending |
