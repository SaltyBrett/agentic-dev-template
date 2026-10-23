---
name: team-selection
description: 'Build or extend this project''s persona roster from the template''s library: ask which specializations the project needs, recommend personas from personas/, draft any the library lacks, and activate the chosen into .claude/agents/. Use at a project''s first session, when the work needs a specialization no active persona covers, or when the cold-start report notes that the library holds a newer version of an active persona.'
---

# Team selection

The library, `personas/`, holds every persona the template ships, and none is active there. The
roster, `.claude/agents/`, holds only the personas this project activated or drafted. Each roster
file is a live Claude Code agent whose description loads in every session and which Claude may
delegate to unprompted, so activate what the work needs and no more (decision 2026-10-23-003).

1. **Read the project and the library.** The project's line in `AGENTS.md`, its PRD in `docs/prd/`
   if there is one, and the current roster. For each file in `personas/`, its frontmatter: `name`,
   `description`, `expertise` and `version`. The body is the prompt and need not be read to choose.
2. **Ask the operator** which specializations the project needs. Offer the library's personas
   grouped by area (software lifecycle, data science, document management, writing, quality
   control) and leave room for a need the library does not name. Ask which persona leads the
   sessions: that is the one the next kickoff names.
3. **Recommend** the library persona that covers each need and why, and name every need no library
   persona covers. Wait for the operator's yes or changes.
4. **Activate** each chosen library persona by copying it whole:
   `cp personas/<slug>.md .claude/agents/<slug>.md`. Never edit the copy. The state gate refuses a
   roster copy that differs from the library at its version or runs ahead of it; the cold-start
   report names one the library has moved past, and copying it again takes the newer text.
5. **Draft** a persona for each uncovered need as `.claude/agents/<slug>.md`, the project's own,
   and show it to the operator before writing it:
   - frontmatter: `name` equal to the slug (lowercase words joined by hyphens, never a library
     slug), `description`, `version: 1`, and `expertise`, `insists_on` and `changelog` as YAML
     lists of strings, quoting any item that holds `: `; the changelog's item is
     `1 — <date> — first version`;
   - body: the Invocation, a short paragraph addressing the agent as who it is and what it insists on.

   A drafted persona stays in this project. The library holds only the personas the template
   builds and releases.
6. **Deactivate** a persona the work no longer needs by deleting its roster file, unless the current
   kickoff names it.
7. **Prove and commit:** `pre-commit run session-closeout-check --all-files` exits 0, then commit
   `checkpoint: team — <slugs>`.
