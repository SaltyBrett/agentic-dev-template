---
name: A project starts under GCC/Gov constraints or under none, and the toggle is mechanical
description: 'The GCC compliance regime is the law of one kind of engagement, not of every project. `.project-profile` holds one word and drives two things from it: profile-fenced prose is stripped from the governance documents, and the scanner applies the GCC pattern set or does not. The gate and CONSTITUTION.md read the same file, so they cannot disagree. No profile means the template itself, which keeps every block and enforces the union. Read before adding profile-specific content or a new profile.'
teaches: [2026-09-20-009]
verified: 2026-09-20
metadata:
  type: reference
---

# A project starts under GCC constraints or under none

> Durable learning. Wikilink: `[[reference_project_profiles]]`.
> Companion: [[reference_content_provenance]].

## Why a toggle and not a note

The GCC regime — banned Direct Lake, Dataflows Gen2, DirectQuery, OLS, mandatory Power BI Import
mode, RLS + DAX masking — is the law of one kind of engagement. A purely commercial project inherits
rules that do not apply to it.

The tempting fix is a sentence: *"ignore §5 if this is commercial."* **That sentence is the fossil
`CONSTITUTION.md` §6.3 exists to prevent** — a governance document stating a rule nobody enforces,
read by the next agent *instead of* the source. The rule has to leave the document, not be annotated
as inapplicable.

## How it works

`.project-profile` holds one word, `gcc` or `commercial`, written by `new_project.py --profile`,
which **requires** the flag. Two things follow from that single value:

**1. Documents are stripped.** Profile-specific prose is fenced in HTML comments, invisible when
rendered and obvious in the raw file:

    <!-- profile:gcc -->
    ...GCC-only law...
    <!-- /profile:gcc -->
    <!-- profile:commercial -->
    ...its commercial counterpart...
    <!-- /profile:commercial -->

The initializer keeps one side, drops the other, and removes the marker lines themselves. Sections
have counterparts rather than simply vanishing, so §4, §5 and §7 stay coherent and the numbering does
not jump.

**2. The scanner switches.** `GCC_BANNED_PATTERNS` applies only when the profile is `gcc`;
`ALWAYS_BANNED_PATTERNS` applies everywhere. **The gate and the constitution read the same file**, so
the enforced rule and the written rule cannot drift apart — which is the whole point.

Measured on two real projects built from one template:

| | `gcc` | `commercial` |
|---|---|---|
| `CONSTITUTION.md` §5 | GCC Portability Requirements | Portability Requirements |
| `AGENTS.md` banned-features bullet | present | absent |
| `{"mode": "DirectLake"}` in a file | **blocked**, exit 1 | **allowed**, exit 0 |
| markers left behind | none | none |

## The template has no profile, and that is not an oversight

No `.project-profile` means *this is the template*. It keeps **every** profile's blocks and enforces
the **union** of the rules — the strictest reading. That is fail-closed, and it is what lets the
template carry GCC law it does not impose on every descendant.

An unknown value in the file is an **error, never a default**. A toggle that silently picks a side is
not a toggle.

## Why marker balance is a gate

An unclosed `<!-- profile:gcc -->` swallows the entire rest of the file when the other profile is
stripped. A fixture demonstrates exactly that, so the failure is a red test rather than a governance
document that quietly lost its second half. The gate also refuses nesting — it makes "which profile
owns this line" ambiguous — and refuses an unknown profile name.

In a derived project the gate additionally refuses any block belonging to a *different* profile,
which catches a half-finished initialization.

## Adding a new profile

1. Add the name to `PROFILES` in `scripts/project_profile.py`.
2. Fence its content, and give every existing `gcc`/`commercial` section a counterpart so the
   documents stay coherent under the new profile.
3. If it needs its own banned-feature set, add a dict beside `GCC_BANNED_PATTERNS` and extend
   `active_banned_patterns()`.

For consulting, one profile per engagement type is the obvious shape — and it composes with the
provenance rule in [[reference_content_provenance]], which is where per-client identifiers belong.

## Rules

- Profile-specific law lives inside markers, never behind a note saying it may not apply.
- Every `gcc` block that removes a numbered section gets a `commercial` counterpart, and vice versa.
- Never add a default profile. The absence of the file means "template", and an unknown value is an
  error.
- A script that *explains* banned features will name them; add it to `EXCLUDE_FILES`, as
  `project_profile.py` is. `CONTENT_RULES` still covers it, because `EXCLUDE_FILES` does not reach
  that channel.
