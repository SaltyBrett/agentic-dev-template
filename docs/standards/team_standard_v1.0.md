---
authority: the agentic development team (how a story runs through its roles, the artifacts they hand off, the review triggers and the Chair's approvals)
implements: []
verified: 2026-10-25
---

# Team Standard v1.0

**Purpose:** A story built by a team of role agents the way a human team builds one: each role works
from the artifact the last one handed it, every handoff is a file a gate judges, and the Chair is
asked only where a decision is the Chair's. The procedure is the `/story`
skill; the enforcement is the `story-artifacts` gate.

---

## 1. How a story runs

- `/story <ID>` runs one story, in the main session, since only the main session can ask the Chair. It calls each role as a subagent of the
  roster's agent type; where the roster agent cannot be called, a general-purpose subagent carrying
  the persona's prompt.
- Each role reads its input artifact and writes its own. The gate judges it, and it is committed,
  before the next role starts.
- The main session gives each role the model and effort its task needs, chosen per brief, within the operator's mode and never above the session's: `max`
  changes neither, `tuned` the effort only, `efficient` both. The mode is `SUBAGENT_CHOICE` in
  `.claude/settings.json`, and `scripts/subagent_ceiling.py` refuses a spawn or a skill over the
  ceiling.
- The story runs end to end. It stops only at a review trigger (section 4) or when a gate still fails after
  three attempts running, and says what it stopped on.
- Nothing forces a code change: a finding pauses the story only until the Chair responds in the code
  review log, section 5.
- Each story is built on its own branch, `story/<ID>`, in its own worktree, `.worktrees/<ID>`, and
  several run at once, one agent to a worktree. `python3 scripts/story_branch.py start <ID>` sets the
  story In Progress on the integration branch, `main`, and makes the worktree; `finish <ID>` merges it by a squashed pull request once its CI is
  green and sets it Done there. The issues naming the story move with
  it: `start` sets them In Progress, and `finish <ID> --resolution "<what changed>"` sets Resolved
  each one whose stories are then all Done. Before it merges, `finish` refuses an integration
  branch ahead of its origin, and a Done that would leave an issue In Progress with no resolution
  given.
- A protected branch, `main` or `release/*`, takes only the shared records: `sprint/`, the decision
  logs, the knowledge base and the planning outputs, besides a release commit, a project's birth
  and the stamps `finish` writes into version-log rows after the merge.
  A story branch takes the story's own work and never the tracker, sprint-status, the handoffs or the
  issue log, which the integration branch alone writes. The `branch-policy` and `branch-push`
  hooks hold this, the push check run again by CI, since GitHub's branch protection is
  unavailable on a private repository on the current plan; the append-only indexes merge with git's
  union driver, so parallel additions never conflict.

---

## 2. The artifacts

A story's artifacts live in `docs/stories/<ID>/`, the folder named for a story the tracker holds, one
file per stage it passes through: `brief.md`, `design.md`, `build.md`, `verify.md`, `review.md`,
`security.md`, `docs.md`, `release.md`, and `approvals.md` for the Chair's approvals.

Each stage's file opens with frontmatter:

```yaml
---
story: ACME-5.1           # the folder's story
stage: build              # the file's stage
role: software-engineer   # a roster persona the role map allows here
input: design.md          # the artifact the role read: the stage before it; `none` for the brief
status: pass              # pass, fail or needs-operator
triggers: []              # the triggers of section 4 this role's work hits, by name
model: sonnet             # the model the role ran at: an alias or a full ID the ranking places
effort: high              # the effort it ran at: low, medium, high, xhigh or max
---
```

- **brief** also names `type:`, one of section 3's story types, and holds `## Acceptance criteria`, a
  numbered list.
- **build** also lists `commits:`, the commits it made, which the gate reads for trigger paths.
- **verify** holds `## Checks`, a table `| Criterion | Check | Result |`: every criterion of the brief,
  by its number, with the check observed and `pass`.
- **review** and **security** hold `## Findings`, a table `| Where | Finding | Severity | Fix |`, or
  the line `None.`; each finding, its Where a place (`path:function`) and its Finding opening with a
  rule and a value as the code review log writes them (`cohesion 1 - two jobs in one function`), is
  also a row of that log.
- **release** also names `run:`, the CI run observed green, where something ships.

A stage vouches for its input as it stood, so each stage's file is committed alone, after its
input's last change. A change to an artifact, a rebuild above all, removes every stage after it in
the same commit, and each of those stages runs again; the removed files
stay in git history.

---

## 3. Story types and the role map

A story's type, set in its brief, picks its stages and the roles each allows. A cell reading `none` is a stage the type does not have.

| Type | brief | design | build | verify | review | security | docs | release |
|------|-------|--------|-------|--------|--------|----------|------|---------|
| software | `product-manager`, `business-analyst` | `solution-architect`, `ux-designer` | `software-engineer`, `frontend-engineer`, `backend-engineer`, `web-developer` | `qa-engineer` | `code-reviewer` | `security-engineer` | `technical-writer` | `devops-engineer` |
| data | `business-analyst` | `solution-architect`, `data-platform-engineer` | `data-engineer`, `analytics-engineer`, `bi-developer`, `ml-engineer`, `data-scientist`, `data-analyst`, `reporting-analyst` | `data-quality-engineer` | `code-reviewer` | `security-engineer` | `technical-writer` | `devops-engineer` |
| document | `business-analyst`, `product-manager` | `information-architect` | `business-writer`, `technical-writer` | `editor` | `document-reviewer` | none | none | `document-controller` |
| game | `game-producer` | `game-designer`, `narrative-designer`, `game-ui-ux-designer` | `game-engine-developer`, `game-artist`, `game-audio-designer` | `game-qa-tester` | `code-reviewer` | none | none | `devops-engineer` |
| media | `product-manager` | none | `generative-video-engineer`, `image-video-editor`, `blender-artist` | `image-video-editor` | none | none | none | `devops-engineer` |

- The verifier and the reviewer are never the builder.
- A security stage joins any type whose story hits an auth or crypto change or an external service,
  before its release, by `security-engineer`.
- Optional: a game's review where its build changed no code, and a media story's release where
  nothing ships. Every other stage of the type is required, in order.
- `delivery-manager` writes the plan and `framework-maintainer` the template's gates, outside the
  per-story flow.

---

## 4. Review triggers

The points at which a story stops for the Chair:

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
- `writing-profile.yaml` is a trigger path of a gate or CI change in every stack, since its allow
  list exempts text from the writing gate.
- Each hit trigger needs a row in `approvals.md`, `| Trigger | What was approved | Chair's words | Date |`,
  before the story's release, or its Done in the tracker. The Chair's words are the approval; the
  story waits for them and for nothing else.

---

## 5. Findings and the code review log

The review and security stages write every finding to `docs/code_review_log.md`, beside the coding
standard's gate's (`docs/standards/coding_standard_v1.0.md` section 4), with the change made in response.
A finding pauses the story until the Chair's response is in the log; the next stage does not start
before. No finding forces a code change.

---

## 6. The security audit

The security stage's brief for `security-engineer`: the change read against
the OWASP Top 10 and the CWE Top 25 for its stack; secrets, authorization, input handling and data
flows; the dependency and license audit's results. Each finding with its exploit path, severity and
fix. A high or critical finding open, or one the auditor cannot clear, is a trigger the Chair answers.

---

## 7. What the gate holds and cannot judge

`story-artifacts` holds every rule above that a file shows: the folder's story, the frontmatter
with each role's model and effort, the stage order and each input passing before the next role
started, each stage committed after its input's last change, the roles against the map and the
roster, the verifier and reviewer apart from the builder, the criteria checked, the triggers
approved, the findings answered, the release's run. It cannot judge whether a design is good or a
check was the right one; those are the roles' and the Chair's. Nor
can it tell that a recorded model and effort are what ran: the ceiling hook judged the spawn.

---

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.9 | 2026-10-25 | template | the template's version 1.9 | template |
