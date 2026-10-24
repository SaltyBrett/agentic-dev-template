---
name: The Blender connection is the Blender Lab server, pinned to a commit and chosen per project
description: 'Why the opt-in Blender connection that team selection offers with blender-artist is the Blender Foundation''s Blender Lab MCP server pinned at v1.0.3''s commit and not the far more popular community server; what each was found to do (telemetry, third-party calls, code execution, advisories); why the pin is a git commit; how Claude Code approves a project-scoped server and where it does not ask; and what skill-scan holds. Read before offering, re-pinning or replacing the connection.'
teaches: [2026-10-23-012, 2026-10-23-013]
verified: 2026-10-23
metadata:
  type: reference
---

# The Blender connection is the Blender Lab server, pinned to a commit and chosen per project

> Durable learning. Wikilink: `[[reference_blender_mcp]]`. The connection's one home, its pin
> included, is the data block of `.claude/skills/team-selection/SKILL.md`; `scripts/skill_scan.py`
> holds it. Vetted 2026-10-23 by reading each candidate's released files as text; neither was run.

## Why a connection is opt-in

An MCP server for Blender exists to run Python inside a running Blender: both candidates expose an
`execute_blender_code` tool, and both listen on `localhost:9876` with no authentication, so anything
on the machine that reaches the port can do the same. Decision 2026-10-23-012 therefore offers the
connection only with the persona that uses it, writes it only on the operator's yes, and never
enables it in the template. `skill-scan` makes the last two mechanical: `.mcp.json` holding the
connection fails in the template, and in a project whose roster lacks `blender-artist`.

## The two candidates

- **Blender Lab** (`projects.blender.org/lab/blender_mcp`), the Blender Foundation's own,
  GPL-3.0-or-later, release v1.0.3 at commit `2cea8d566dde07fbac28a61d698909d69724e853`. Its server
  and its add-on hold no HTTP client and no outbound URL. Its tools are scene queries, screenshots,
  navigation, searches of the bundled API reference and manual, `execute_blender_code`, and a few
  that start `blender --background` or render to a path. It needs Blender 5.1 or newer, and its
  add-on will not start unless Blender's Allow Online Access is on. Its own sandbox file says it is
  not really a sandbox, and its documentation advises a virtual machine.
- **The community server** (`ahujasid/mcp-for-blender`, formerly `blender-mcp`), MIT, with tens of
  thousands of stars, released to PyPI several times a week and never tagged. It was rejected:
  telemetry is on by default, sending an install ID and every tool call's name, duration and
  outcome to a hosted database unless `DISABLE_TELEMETRY` is set, and the configuration holding that
  endpoint is ignored by its git repository and added only to the PyPI builds, so a release cannot
  be checked against the source; the release published on 2026-10-23 held code its repository did
  not. Its add-on fetches its own newest source from GitHub at Blender's start. It downloads assets
  and calls paid generation services when given keys, and four advisories name it (path traversal,
  code injection through `execute_blender_code`, injection and request forgery in a generation
  path), one closed as not planned. And the PyPI name `blender-mcp` is its wrapper, which requires
  the newest release whatever it is pinned at: `uvx blender-mcp` installs the community server, not
  Blender Lab's, whose package carries the same name and is not on PyPI.

## Why the pin is a commit

Blender Lab's server is not on PyPI, so uv runs it from git:
`uvx --from git+https://projects.blender.org/lab/blender_mcp.git@<commit>#subdirectory=mcp blender-mcp`.
A tag can be moved and a branch moves by design, so `skill-scan` accepts a git source only at a full
40-character commit, and a package only at `==` or `@` an exact version. The add-on is pinned by the
SHA-256 of its release zip, which the operator checks before installing it. The pin covers the
server's own code; its dependencies (`mcp`, `docutils`, `pyyaml`) are resolved when uv first runs
it. Re-check the pin against the tag with
`git ls-remote https://projects.blender.org/lab/blender_mcp.git refs/tags/v1.0.3`.

## How Claude Code approves it

A server in `.mcp.json` at the repository root is project-scoped. In each clone, an interactive
session asks once before using it and stores the answer in `.claude/settings.local.json`, which is
the clone's own; a committed setting cannot pre-approve it in a folder not yet trusted, and a
`disabledMcpjsonServers` entry refuses it from any settings file. A headless run (`claude -p`, the
Agent SDK, a cloud session) loads project servers without asking, so once the entry is committed an
unattended run can reach a Blender that is running with the add-on's server started.

## Honest limit

The vetting read released files; it ran neither server. The uv command is the documented form for a
git source with a subdirectory, and the subdirectory, the script name and the defaults were read
from the commit's tree, but the command was not run here. The gate holds where the connection is
written and that it is pinned, not whether the pinned release is safe: that is this vetting, to be
done again before the pin moves.
