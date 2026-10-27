---
name: humanize
description: 'Fix what the writing gate flags in markdown already in the tree: the certain fixes by script, the rest rewritten by the editor in the document''s voice as numbered proposals, the gate and a guard on meaning run again up to three times, and the Chair keeping, trimming or rejecting each file before anything is committed. Also `voice <name>`, a custom voice made from a sample of the Chair''s writing. Use when the writing gate refuses text already in the tree, or the Chair names files. Arguments: the files or folders, or `voice <name>`.'
argument-hint: '<path>... | voice <name>'
---

# Humanize

This runs in the main session, never forked: only the main session can ask the Chair, and nothing
is kept without the Chair's answer. The law is
`docs/standards/writing_standard_v1.0.md` and the judgement `.claude/rules/writing.md`. Another
agent reads this file and follows it as instructions.

Arguments: $ARGUMENTS

## When it runs

- On text already in the tree: the template's sweep, a project's adoption, or files the Chair
  names. An agent's own uncommitted draft that the gate refuses is the agent's to fix, as a failing
  test is, and does not come here.
- From a clean tree (`git status --short` lists nothing), so `git restore` returns a rejected file
  whole.

## 1. Judge

`python3 scripts/humanize.py --report <path>` prints each file's voice and audience and the gate's
findings in it. A profile or voice finding stops the run: the profile is fixed first.

## 2. The certain fixes

`python3 scripts/humanize.py --fix <path>` makes every fix with one right answer, in place, and
counts each file's fixes by kind; keep the counts for the review. Copy each fixed file to a scratch
file outside the repository, its snapshot: the text the editor's proposals are checked against.
Run `--report` again. What is left is the editor's.

## 3. The editor

For each file with findings left, call the roster's `editor` as a subagent; where the roster has
none, a general-purpose subagent whose prompt opens with the text below the frontmatter of
`personas/editor.md`. Its brief:

- the file's path, voice and audience, and the voice file's path in `docs/standards/voices/`,
  whose traits it writes to and, for a custom voice, whose sample it imitates;
- `.claude/rules/writing.md`, and sections 5 to 8 of the writing standard;
- each finding: its line, rule, detail and fix, and the sentence or heading it sits in;
- rewrite only the flagged text, in the document's voice; keep every code span, fenced block,
  link, wikilink and number, a development reference removed from a production document excepted;
  propose a change of substance in words and never make it;
- edit no file of the repository: write the proposals as JSON to the scratch file the brief names,
  `[{"n": 1, "old": "<exact text, found once in the file>", "new": "<its replacement>", "finding":
  "<line and rule>"}]`, each old text checked to occur once and none overlapping.

## 4. Check up to three tries

1. Apply the proposals to the file: `python3 scripts/humanize.py --apply <proposals.json> <path>`. A proposal whose old text is not
   found exactly once, or that overlaps another, applies nothing; send it back.
2. `python3 scripts/humanize.py --report <path>` for what is still flagged, and
   `python3 scripts/humanize.py --guard <snapshot> <path>`, with `--production` for a production
   file, for every code span, fenced block, link, wikilink and number lost or added.
3. Copy the snapshot back over the file. Anything still flagged, or failed by the guard, goes back
   to the editor with the output, for a whole new set of proposals. After the third try, what is
   still open goes to the Chair with the rest.

## 5. The Chair's review

Up to four files a round, one question each. For each file: the certain fixes as counts by kind,
then the proposals, then any finding still open after three tries. The Chair keeps all of it,
keeps some (naming the numbers to drop), or rejects the file. A fragment is not reviewable, so:

- each proposal is shown as the whole sentence, table row or heading it changes, before and after,
  exactly as the reader sees it, never cut short with an ellipsis;
- proposals are grouped by the decision they ask (cut a citation, write a range as `to`, delete a
  row), each group one yes or no that names what the Chair is deciding;
- a change that could alter meaning (a fact, a step, a name an operator must find) is asked on its
  own, its risk named.

## 6. Keep what the Chair kept

- **Kept, all or some:** `python3 scripts/humanize.py --apply <proposals.json> <path> --keep <n,n>`,
  then `--report` and `--guard` once more; what is still open is told to the Chair, never fixed
  silently.
- **Rejected:** `git restore <path>`, the certain fixes with it.
- Commit only the kept files, once `pre-commit run --all-files` passes, as
  `checkpoint: humanize <what>`.

## The voice mode

`voice <name>` makes a custom voice from a sample of the Chair's own writing (section 2 of the
writing standard).

1. Save the Chair's sample to a scratch file. `python3 scripts/humanize.py --sample <file>` counts
   it as the gate does: 200 words or more, or ask the Chair for more.
2. Draft the five traits from what the sample shows: sentence length, person, register,
   contractions, and what it never does. Show them to the Chair.
3. Once the Chair approves, write `docs/standards/voices/<name>.md` in section 2's shape: `name`
   and `tables` (the Chair says which), `## Traits`, `## Use it for`, and `## Sample` holding the
   sample in one fenced block, its words as written; only its characters change, by `--fix`.
4. Stage the file with `git add`, since the gate reads what git tracks, and
   `python3 scripts/humanize.py --report <path>` passes: the gate's voice rule counts the sample.
5. Ask the Chair which paths or agents take the voice, and write them into `writing-profile.yaml`;
   a change to the profile is a gate change the Chair approves. Commit.
