---
name: planning-session
description: 'Build or materially re-plan the sprint from an approved PRD and architecture: dependency layers, epics, stories, the three sprint documents and the planning decisions. Use when a project''s first session plans its work, or when the user asks to plan or re-plan a sprint.'
---

# Planning session

The sprint-creation counterpart to the cold start. The law it builds to is
`docs/standards/sprint_management_standard_v1.0.md`: the three documents and their roles (§2), the
hierarchy and naming (§3), what a well-formed story is (§4), the status lifecycle (§7). Read it
whole before step 1.

## Preconditions

Do not start until all hold; say which one fails and stop.

- The PRD is approved in `docs/prd/` by `docs/templates/README.md`, or the Chair's skip of it is
  logged, an APPROVED decision headed `**Skips:** prd`.
- The architecture is approved in `docs/architecture/`, built from the PRD's newest version, or its
  skip is logged as `**Skips:** architecture`. `doc-authority-scan` refuses the first real epic
  otherwise.
- You have read both in full this session. References do not load themselves.
- You have read `CONSTITUTION.md` and the sprint standard this session.

## Steps

1. **Derive the dependency layers** from the architecture (for example
   `INFRA --> DATA_INGEST --> TRANSFORM --> SERVE --> VALIDATE`) and record them in the tracker's
   Dependency Order block.
2. **Group the PRD's requirements into epics**, one coherent capability within a layer each, with
   an `{PREFIX}-{Epic#}` ID.
3. **Decompose each epic into stories** by the standard's §4 rules, each one testable and
   session-sized, with an `{PREFIX}-{Epic#}.{Story#}` ID.
4. **For each story set** its Dependencies (story IDs that must be Done first, or `—`), its Required
   Standards from `docs/standards/`, and its PRD Ref.
5. **Populate `sprint/story-tracker.md`:** Summary Statistics, Dependency Order, one table per epic.
   Remove the `[EXAMPLE]` epic. Set its `**Source:**` line to the versions the plan is built from,
   each document's newest version-log version, as `**Source:** PRD 1.1, architecture 1.0`, a skipped
   one written `skipped`: `/project-launch` reads it to flag a plan built on an older architecture.
6. **Initialize `sprint/sprint-status.md`:** Current Phase, Current Focus, and this session's entry
   headed `## S<N> — YYYY-MM-DD — <title>`. Replace every `{{PLACEHOLDER}}`.
7. **Seed `sprint/decision-log.md`** with the planning decisions (layering, scope boundaries,
   framework and technology choices), each with its rationale and an ID prefixed by the project's
   story prefix. Remove the `[EXAMPLE]` entry once a real one exists.
8. **Confirm the plan with the user** before any build work begins (`CONSTITUTION.md` §1).
9. Commit `checkpoint: planning — <scope>` once `pre-commit run --all-files` exits 0; the state
   gate recounts the tracker and refuses a live `[EXAMPLE]` row or token in a project.

## Done when

- Every PRD requirement maps to at least one story, and no story lacks a PRD Ref.
- Every story has a status, dependencies or `—`, and Required Standards or a justified `—`.
- The Dependency Order is recorded and no story depends on a story in a later layer.
- The tracker's `**Source:**` line names the PRD and architecture versions the plan is built from.
- The Summary Statistics match the rows.
- `sprint-status.md` holds no `{{PLACEHOLDER}}` and this session's entry is written.
- The planning decisions are logged and the `[EXAMPLE]` entries are gone.
- The user has confirmed the plan.
