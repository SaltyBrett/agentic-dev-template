---
authority: the agentic development team — how a story runs through its roles, the artifacts they hand off, the review triggers and the Chair's approvals
implements: [2026-10-22-003, 2026-10-24-004, 2026-10-24-005, 2026-10-24-006, 2026-10-24-009, 2026-10-24-011, 2026-10-24-013]
verified: 2026-10-24
---

# Team Standard v1.0

**Purpose:** A story built by a team of role agents the way a human team builds one: each role works
from the artifact the last one handed it, every handoff is a file a gate judges, and the Chair is
asked only where a decision is the Chair's (decision 2026-10-22-003). The procedure is the `/story`
skill; the enforcement is the `story-artifacts` gate.

---

## 1. How a story runs

- `/story <ID>` runs one story, in the main session, since only the main session can ask the Chair
  (decision 2026-10-24-004, [[reference_claude_code_skills]]). It calls each role as a subagent of the
  roster's agent type; where the roster agent cannot be called, a general-purpose subagent carrying
  the persona's prompt.
- Each role reads its input artifact and writes its own. The gate judges it, and it is committed,
  before the next role starts.
- The story runs end to end. It stops only at a review trigger (§4) or when a gate still fails after
  three attempts running, and says what it stopped on.
- Nothing forces a code change: a finding pauses the story only until the Chair responds in the code
  review log (§5, decision 2026-10-24-011).

---

## 2. The artifacts

A story's artifacts live in `docs/stories/<ID>/`, the folder named for a story the tracker holds, one
file per stage it passes through: `brief.md`, `design.md`, `build.md`, `verify.md`, `review.md`,
`security.md`, `docs.md`, `release.md`, and `approvals.md` for the Chair's approvals.

Each stage's file opens with frontmatter:

```yaml
---
story: CU-5.1             # the folder's story
stage: build              # the file's stage
role: software-engineer   # a roster persona the role map allows here
input: design.md          # the artifact the role read: the stage before it; `none` for the brief
status: pass              # pass, fail or needs-operator
triggers: []              # the triggers of §4 this role's work hits, by name
---
```

- **brief** also names `type:`, one of §3's story types, and holds `## Acceptance criteria`, a
  numbered list.
- **build** also lists `commits:`, the commits it made, which the gate reads for trigger paths.
- **verify** holds `## Checks`, a table `| Criterion | Check | Result |`: every criterion of the brief,
  by its number, with the check observed and `pass`.
- **review** and **security** hold `## Findings`, a table `| Where | Finding | Severity | Fix |`, or
  the line `None.`; each finding, its Where a place (`path:function`) and its Finding opening with a
  rule and a value as the code review log writes them (`cohesion 1 — two jobs in one function`), is
  also a row of that log.
- **release** also names `run:`, the CI run observed green, where something ships.

---

## 3. Story types and the role map

A story's type, set in its brief, picks its stages and the roles each allows (decision
2026-10-24-006). A dash is a stage the type does not have.

| Type | brief | design | build | verify | review | security | docs | release |
|------|-------|--------|-------|--------|--------|----------|------|---------|
| software | `product-manager`, `business-analyst` | `solution-architect`, `ux-designer` | `software-engineer`, `frontend-engineer`, `backend-engineer`, `web-developer` | `qa-engineer` | `code-reviewer` | `security-engineer` | `technical-writer` | `devops-engineer` |
| data | `business-analyst` | `solution-architect`, `data-platform-engineer` | `data-engineer`, `analytics-engineer`, `bi-developer`, `ml-engineer`, `data-scientist`, `data-analyst`, `reporting-analyst` | `data-quality-engineer` | `code-reviewer` | `security-engineer` | `technical-writer` | `devops-engineer` |
| document | `business-analyst`, `product-manager` | `information-architect` | `business-writer`, `technical-writer` | `editor` | `document-reviewer` | — | — | `document-controller` |
| game | `game-producer` | `game-designer`, `narrative-designer`, `game-ui-ux-designer` | `game-engine-developer`, `game-artist`, `game-audio-designer` | `game-qa-tester` | `code-reviewer` | — | — | `devops-engineer` |
| media | `product-manager` | — | `generative-video-engineer`, `image-video-editor`, `blender-artist` | `image-video-editor` | — | — | — | `devops-engineer` |

- The verifier and the reviewer are never the builder.
- A security stage joins any type whose story hits an auth or crypto change or an external service,
  before its release, by `security-engineer`.
- Optional: a game's review where its build changed no code, and a media story's release where
  nothing ships. Every other stage of the type is required, in order.
- `delivery-manager` writes the plan and `framework-maintainer` the template's gates, outside the
  per-story flow.

---

## 4. Review triggers

The points at which a story stops for the Chair (decision 2026-10-24-005):

- a new dependency
- a schema change
- an auth or crypto change
- an external service
- a cost
- a security finding the auditor cannot clear
- anything a gate cannot judge
- a deploy or release
- a gate or CI change
- data loss
- a license change

A project adds its own here, by a decision, and removes none.

- A trigger is hit when a role declares it in its artifact's `triggers:`, when a commit the build
  lists touches one of the stack profile's trigger paths, or, for a deploy or release, when the story
  has a release that ships.
- Each hit trigger needs a row in `approvals.md`, `| Trigger | What was approved | Chair's words | Date |`,
  before the story's release, or its Done in the tracker. The Chair's words are the approval; the
  story waits for them and for nothing else.

---

## 5. Findings and the code review log

The review and security stages write every finding to `docs/code_review_log.md`, beside the coding
standard's gate's (`docs/standards/coding_standard_v1.0.md` §4), with the change made in response.
A finding pauses the story until the Chair's response is in the log; the next stage does not start
before. No finding forces a code change.

---

## 6. The security audit

The security stage's brief for `security-engineer` (decision 2026-10-24-009): the change read against
the OWASP Top 10 and the CWE Top 25 for its stack; secrets, authorization, input handling and data
flows; the dependency and license audit's results. Each finding with its exploit path, severity and
fix. A high or critical finding open, or one the auditor cannot clear, is a trigger the Chair answers.

---

## 7. What the gate holds, and what it cannot

`story-artifacts` holds every rule above that a file shows: the folder's story, the frontmatter, the
stage order and each input passing before the next role started, the roles against the map and the
roster, the verifier and reviewer apart from the builder, the criteria checked, the triggers
approved, the findings answered, the release's run. It cannot judge whether a design is good or a
check was the right one; those are the roles' and the Chair's ([[reference_story_artifacts]]).

---

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.0 | 2026-10-24 | 2026-10-24-004, 2026-10-24-005, 2026-10-24-006, 2026-10-24-009, 2026-10-24-011, 2026-10-24-013 | Written as the authority for the agentic team (TMPL-3.2): the orchestration, the artifacts, the role map by story type, the review triggers and the Chair's approvals, findings in the code review log, the security audit | a2d1a78 |
