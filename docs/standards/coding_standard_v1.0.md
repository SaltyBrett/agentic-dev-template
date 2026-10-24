---
authority: the coding standard — the core limits on code a change adds or edits, how their findings are recorded, and how each stack measures them
implements: [2026-10-22-003, 2026-10-24-007, 2026-10-24-008, 2026-10-24-009, 2026-10-24-011]
verified: 2026-10-24
---

# Coding Standard v1.0

**Purpose:** Code that a reviewer can read, a test can pin down and a later change can safely touch,
measured by gates rather than by goodwill. Agents write verbose, run-on, repetitive code when
nothing measures them, and a standard that is prose measures nothing (decision 2026-10-22-003). It
advises and documents, and never forces a code change: the Chair can always acknowledge a finding
and proceed (decision 2026-10-24-011).

---

## 1. Scope

- A project opts in by choosing a stack profile at its planning session (§6). The standard judges
  the code a change adds or edits, never the codebase as it stood: a function is changed when the
  change adds it or edits a line of it.
- An edited function already over a limit is a finding like any other, fixed or answered in the
  code review log (§4). Untouched code is not judged.
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
- Generated code is declared by path in the profile; a generated-code marker anywhere else is a
  finding.
- A tool that cannot run is a finding, `unmeasured`: never a silent pass, never a wall.

---

## 4. Findings and the code review log

- Every finding, the gate's, the code reviewer's and the security auditor's, is recorded in
  `docs/code_review_log.md`, one table, appended to and never edited:

  | Date | Change | Where | Finding | Source | Change made | Chair's response |
  |------|--------|-------|---------|--------|-------------|------------------|

  Where is the place, `path:function`; Finding opens with the rule and its value (`complexity
  21`); Source is `gate`, `code-reviewer` or `security-engineer`; Change made says what changed in
  response, or `none`.
- A finding pauses the commit, or the story, only until the log holds it with the Chair's response;
  "acknowledged, proceed" is enough, and no code change is ever required. A finding answered at a
  value pauses nothing again unless it gets worse at the same place and rule.
- The Chair's acknowledgement is the exception; there is no separate exceptions file. The response
  may name a category: data or table, parser or state machine, exhaustive dispatch over a closed
  set, generated code, measured hot path.
- A tool's suppression comment on a changed line is a finding of its own.
- Rows are appended, never edited or removed: a base row changed is the one thing no response
  clears, since the log is the audit record.

---

## 5. What the gate runs on a change

1. The function limits of §2 over every changed function, after the recall check of §3.
2. The clone check: clones of existing code among the change's added lines.
3. Coverage of the change's new lines, by the project's own tests.
4. The formatter, the linter and the type checker, their findings counted on changed lines only.
5. The dependency and license audit, when a manifest changes and always over a pushed range.
6. The file-length signal and the review-trigger paths, reported, never a finding.

Each finding is then looked up in the code review log (§4); one not yet answered pauses the change.

---

## 6. Stack profiles: the mapping rule

A stack profile names one pinned tool for each slot. A stack with an empty slot is not adoptable;
the planning session chooses the profile.

| Slot | What the tool does |
|------|--------------------|
| Function measurer | complexity, code lines and parameters per function, proved per §3 |
| Clone detector | clones among the change's added lines |
| Formatter | the stack's canonical format, checked, not rewritten, by the gate |
| Linter | the stack's linter; a §2 limit it also measures is left to the function measurer, so one finding is never asked twice |
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
  it first checks that the gate measured the change, and records each finding in the code review
  log. A blocking finding pauses the story until the Chair responds there, never until the code
  changes, and taste is never blocking (decisions 2026-10-24-009 and 2026-10-24-011).
- The security audit is `security-engineer`'s brief in the team's security stage, its findings in
  the same log under the same rule (decisions 2026-10-24-009 and 2026-10-24-011).

---

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.1 | 2026-10-24 | 2026-10-24-011 | The standard advises and documents: every finding recorded in `docs/code_review_log.md` with the Chair's response, the exceptions file merged into it, a tool that cannot run a finding (TMPL-4.3) | pending |
| 1.0 | 2026-10-24 | 2026-10-24-007, 2026-10-24-008, 2026-10-24-009, 2026-10-22-003 | Written as the authority for the coding standard (TMPL-4.2): the core limits, their scope, the exceptions file, proved measurement and the stack profiles' mapping rule | 1389fa9 |
