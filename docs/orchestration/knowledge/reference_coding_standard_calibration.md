---
name: How the coding standard's numbers were calibrated, and why a measurer must prove itself
description: 'Why the coding standard''s core limits are complexity 15, 60 code lines and 5 parameters per changed function with no new clones: calibrated on pinned industry codebases (ripgrep, packaging, zod) that must pass and the refactoring katas that must fail, from published defaults, with an independent reviewer agent. Why our own code was not the reference, why the gate judges changed code, why file length and a duplication percentage are not gates, and the silent defects that make an unproved measurer report green (lizard on Rust and TypeScript, its forgive comment, jscpd''s size caps). Read before changing a limit, adding a stack profile or choosing a measuring tool.'
teaches: [2026-10-24-007, 2026-10-24-008]
verified: 2026-10-24
metadata:
  type: reference
---

# How the coding standard's numbers were calibrated, and why a measurer must prove itself

> Durable learning. Wikilink: `[[reference_coding_standard_calibration]]`. Story: TMPL-4.1.
> Decisions: 2026-10-24-007 (the limits and their evidence), 2026-10-24-008 (proved measurement and
> the mapping rule), 2026-10-24-009 (the judgement page and the briefs).

## Why not our own code

The framework's codebases were written by agents, which is the population the standard exists to
correct, and they are few: the template's scripts, two projects. Calibrated on them, the numbers
would encode their habits. So the known-good is industry code pinned at release tags, one per
language (ripgrep for Rust, packaging for Python, zod for TypeScript), and the known-bad is the
code the industry writes badly on purpose to teach refactoring, the Gilded Rose and Tennis katas,
in the same three languages. All measured, none run. Our code was measured last, only to see what
adopting would cost: at the chosen limits the template's scripts had 25 of 304 functions over,
which is why the gate judges changed code, not the codebase.

## Why these numbers

Each started from a published default (NIST SP 500-235's 10 and 15, SonarQube's 80% and 3%,
clippy's, pylint's and ESLint's defaults) and was kept only where it separated the two sets.
Complexity 15 catches every kata's central function and leaves about 1% of good functions over,
half of which an independent reviewer judged should have been split anyway; 20 lets Gilded Rose
pass and 10 flags dozens of good functions. Length 60 catches the long katas; 80 catches none. A
limit that catches no kata (parameters) stays as a design signal, said so. One kata variant passes
every limit and only a reviewer catches it: the mechanical layer has a floor, and the judgement page
and the reviewer stand above it.

File length and a duplication percentage do not separate the sets: good code holds large
declarative files and deliberate parallel implementations. So file length is a reviewer signal, and
duplication is judged as clones a change adds, not as a rate that is noisy on a small change.

## A measurer that skips code reports green

The first tool, lizard 1.17.10, chosen because one tool counts every language alike, silently skips
code. Rust lifetimes and some raw strings break its tokenizer, so in ripgrep it measured 1,196 of
2,673 functions and none of one 58-function file. A TypeScript class method with a return type
disappears, which hid zod's worst function (complexity 53) and a complexity-40 kata method; the
kata looked clean. It ignores Python's `match`. Its `#lizard forgives` drops a function from every
metric with no reason kept, and a `GENERATED CODE` comment stops measurement for the rest of the
file. jscpd skips files over 1,000 lines or 100 KB by default and finds exact copies only. None of
this prints a warning.

The reviewer agent found it by measuring before reading and noticing files that reported zero
functions; the session reproduced two cases before relying on them. Hence decision 2026-10-24-008:
a measurer counts only after it passes its language's fixture, and on every run its function count
must equal the file's definitions, or the file is a `recall` finding, never a pass. A finding
advises and is recorded; it never forces a code change (decision 2026-10-24-011).

## Rules

- Calibrate a limit against code that must pass and code that must fail, both pinned, never against
  the code the limit will judge.
- Start from a published default and keep the number only where it separates the two sets; say so
  where a limit catches nothing.
- Never trust a measurer's silence: prove it on its language's hard cases, and check its function
  count against the file on every run.
- Treat a tool's suppression comment as a finding of its own, never as a silent exception; a
  finding is answered in the code review log ([[reference_code_review_log]]).
