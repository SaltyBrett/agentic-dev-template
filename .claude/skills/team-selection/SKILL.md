---
name: team-selection
description: 'Build or extend this project''s persona roster from the template''s library: ask which specializations the project needs, recommend personas from personas/, draft any the library lacks, and activate the chosen into .claude/agents/. Use at a project''s first session, when the work needs a specialization no active persona covers, or when the cold-start report notes that the library holds a newer version of an active persona.'
---

# Team selection

The library, `personas/`, holds every persona the template ships, and none is active there. The
roster, `.claude/agents/`, holds only the personas this project activated or drafted. Each roster
file is a live Claude Code agent whose description loads in every session and which Claude may
delegate to unprompted, so activate what the work needs and no more.

1. **Read the project and the library.** The project's line in `AGENTS.md`, its PRD in `docs/prd/`
   if there is one, and the current roster. For each file in `personas/`, its frontmatter: `name`,
   `description`, `expertise` and `version`. The body is the prompt and need not be read to choose.
2. **Ask the operator** which specializations the project needs. Offer the team presets below
   first, each as one choice the operator may then add to or drop from; then the library's personas
   grouped by area (software lifecycle; data science, BI and reporting; document management;
   writing; quality control; game development; imaging, video and 3D; other specialists), leaving
   room for a need the library does not name. Ask which persona leads the sessions: that is the
   one the next kickoff names. Run by `/project-launch`, the expertise the PRD's section 9 names is the
   operator's first answer: recommend from it, and ask only what it leaves open.
3. **Recommend** the library persona that covers each need and why, and name every need no library
   persona covers. Wait for the operator's yes or changes.
4. **Activate** each chosen library persona by copying it whole, making the roster folder first,
   since git keeps no empty folder and a new project has none:
   `mkdir -p .claude/agents && cp personas/<slug>.md .claude/agents/<slug>.md`. Never edit the
   copy. The state gate refuses a roster copy that differs from the library at its version or runs
   ahead of it; the cold-start report names one the library has moved past, and copying it again
   takes the newer text.
5. **Offer a connection** for each activated persona that has one under `connections:` below:
   say what it runs and what the operator installs (Connections, below), and write it only on the
   operator's yes, into `.mcp.json` at the repository root under `mcpServers`, exactly as given
   (a new file is `{"mcpServers": {}}` first). Off unless chosen; never in the template.
6. **Draft** a persona for each uncovered need as `.claude/agents/<slug>.md`, the project's own,
   and show it to the operator before writing it:
   - frontmatter: `name` equal to the slug (lowercase words joined by hyphens, never a library
     slug), `description`, `version: 1`, and `expertise`, `insists_on` and `changelog` as YAML
     lists of strings, quoting any item that holds `: `; the changelog's item is
     `1 - <date> - first version`;
   - body: the Invocation, a short paragraph addressing the agent as who it is and what it insists on.

   A drafted persona stays in this project. The library holds only the personas the template
   builds and releases.
7. **Deactivate** a persona the work no longer needs by deleting its roster file, and its
   connection from `.mcp.json`, unless the current kickoff names it.
8. **Prove and commit:** `pre-commit run session-closeout-check --all-files` and
   `pre-commit run skill-scan --all-files` exit 0, then commit `checkpoint: team - <slugs>`.

## Team presets

A preset is a team offered as one choice, each member a library persona; the operator may add to it
or drop from it. The presets are in the block at the end.

## Connections

A connection is an MCP server that gives an activated persona a live tool. Each one runs code on the
operator's machine, so it is offered only with its persona, written only on the operator's yes, and
pinned to one vetted release; moving the pin means vetting the new release and changing it here.

**`blender-artist`: Blender, through the Blender Lab MCP server**, the Blender Foundation's own
(GPL-3.0-or-later), pinned at release v1.0.3. It sends no telemetry and calls no outside service.
What the operator installs and approves:

1. Blender 5.1 or newer, with Allow Online Access on in its System preferences; the add-on will
   not start without it.
2. The add-on, from `https://projects.blender.org/lab/blender_mcp/releases/download/v1.0.3/mcp-1.0.3.zip`:
   `shasum -a 256 mcp-1.0.3.zip` must print
   `a7a9da816192502e5a0a202a396444e266b47d8fc4f74ad4698048bd43040707`; then install it from disk
   in Blender's preferences and enable it.
3. `uv`, which runs the server from the pinned commit on `localhost:9876`.
4. The `blender` server in `.mcp.json`. Claude Code asks once in each clone before using it; a
   headless run (`claude -p`, the Agent SDK) does not ask.

The server's `execute_blender_code` runs any Python inside Blender, and so can anything on the
machine that reaches its port: keep the add-on's server running only while working, and save the
file before asking for a change.

## The presets and connections as data

`skill-scan` reads this block: it refuses a preset or a connection naming a persona `personas/`
lacks, a connection pinned to no exact release, and `.mcp.json` holding a connection in the
template, in a project whose roster lacks its persona, or other than written here. A persona renamed in the library is renamed here in the same
commit.

```yaml
presets:
  Application development: [product-manager, solution-architect, ux-designer, frontend-engineer,
    backend-engineer, qa-engineer, devops-engineer, security-engineer]
  Website: [ux-designer, web-developer, business-writer, qa-engineer]
  Imaging, video and 3D: [blender-artist, image-video-editor, generative-video-engineer]
connections:
  blender-artist:
    blender:
      command: uvx
      args: [--from, "git+https://projects.blender.org/lab/blender_mcp.git@2cea8d566dde07fbac28a61d698909d69724e853#subdirectory=mcp", blender-mcp]
```
