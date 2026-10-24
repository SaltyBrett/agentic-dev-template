---
authority: writing - the voices a document is written in and the mechanical and judged rules its text obeys
implements: [2026-10-24-014, 2026-10-24-016, 2026-10-24-017, 2026-10-24-018, 2026-10-24-019, 2026-10-24-020, 2026-10-24-022, 2026-10-24-025]
verified: 2026-10-24
---

# Writing Standard v1.0

**Purpose:** Prose that reads as written by a careful person for its reader, held by a gate where a
pattern shows the fault and by a reviewer where only judgement can. Agents leave mechanical tells in
what they write: characters no US keyboard types, headings that read as sentences, stock phrases,
and development references in documents for a production reader (decision 2026-10-24-014). A rule
written down and left unchecked stops none of them.

---

## 1. Scope

- The standard governs every markdown file git tracks, frontmatter and code blocks included. Each
  file is judged whole at every commit and in CI, never its changed lines only, so text that entered
  unjudged (a commit without the hooks, a template update, a first push judged at its tip) is caught
  at the next commit (decision 2026-10-24-019).
- The template opts in. Its tree is swept before `v2.1.0` is published, and each project is swept
  with the humanizer when it adopts that release; a project born from it has no finding.
- The mechanical rules (sections 5 to 9) are the writing gate's, which refuses. Judgement (section
  10) is held by `.claude/rules/writing.md` and the document reviewer. Text already in the tree is
  fixed through the humanizer skill.
- A Word, Excel, PDF or PowerPoint deliverable is judged as section 11 says.

---

## 2. Voices

A voice is how a document sounds: its sentence length, person, register and contractions, and what
it never does. Seven are built in, one file each in `docs/standards/voices/` (decision
2026-10-24-016).

| Voice | For |
|-------|-----|
| [`technical`](voices/technical.md) | READMEs, runbooks, standards, references and the development records |
| [`business`](voices/business.md) | Briefings, proposals and statements of work, in the house style |
| [`simple`](voices/simple.md) | Help text and application copy for a general reader |
| [`professional`](voices/professional.md) | Correspondence and reports for readers outside the team |
| [`academic`](voices/academic.md) | Papers, literature reviews and research write-ups |
| [`streamlined`](voices/streamlined.md) | Release notes, status updates and summaries read at a glance |
| [`creative`](voices/creative.md) | Fiction, game text, narrative and other expressive writing |

A voice file has this shape:

```markdown
---
name: <slug, equal to the file name>
tables: [ai, marketing]
---

# <Name> voice

## Traits

- Sentence length: ...
- Person: ...
- Register: ...
- Contractions: ...
- Never: ...

## Use it for

...
```

- `tables:` names the phrase tables of section 7 that apply, `ai`, `marketing` or both. Every
  built-in voice takes both but `creative`, which takes `ai` alone (decision 2026-10-24-018). A voice
  holds no phrase list of its own until a decision adds one on shown need.
- **A custom voice** is a project's own, made from a sample of the Chair's writing: the same file
  with a `## Sample` section after the traits, holding the Chair's words in one fenced block, 200
  words or more, the reference a rewrite imitates. Its words are kept as written and its characters
  obey section 5 like any text. The traits are drawn from the sample and approved by the Chair
  before the file is kept.
- A custom voice lives in its project, private. The template ships the built-in voices only, and the
  updater leaves a project's own voice file alone. The humanizer's voice mode captures one.

---

## 3. Audiences

A document's audience is set apart from its voice, so one voice serves a runbook and a decision log
alike (decision 2026-10-24-017).

- **Development:** written for the people and agents building the project, as the standards, the
  sprint documents, the knowledge base and the personas, skills and rules are. It may cite
  development references.
- **Production:** written for the project's users or operators, as a project's README, a runbook,
  help text or a deliverable is. It cites none (section 8).
- A file no rule of the profile names is production. A development default would let a production
  document in a new folder pass while checking nothing, so the gate's message prints the rule that
  declares a path development instead.

---

## 4. The writing profile

`writing-profile.yaml`, at the repository root beside `code-profile.yaml`, gives each governed file
its voice and audience. A document's frontmatter never does (decision 2026-10-24-017).

```yaml
rules:                    # ordered: the first rule matching a file wins
  - paths: ["docs/runbooks/**", "docs/user-guide.md"]
    voice: technical
    audience: production
template:                 # ahead of rules, only where .project-profile is absent
  - paths: ["README.md"]
    voice: technical
    audience: development
default: technical        # the voice of a file no rule names
agents:                   # a roster slug and its voice
  technical-writer: technical
allow: []                 # section 9
```

- **`rules`:** each rule a list of `paths` globs with a `voice` and an `audience`, `production` or
  `development`. A glob may name a single file. In a glob, `**/` is any run of directories or none,
  `**` anything, and `*` and `?` stay inside one path segment.
- **`template`:** rules in the same shape, applied ahead of `rules` only in the template, where
  `.project-profile` is absent, and inert in a project. The template's `README.md`, written for an
  adopter of a development framework, is development there and production in every project
  (decision 2026-10-24-025).
- **`default`:** the voice of a file no rule names, whose audience is production.
- **`agents`:** a map from a roster slug to a voice, the voice the agent writes everything in:
  documents, commit messages, pull request descriptions and replies. In a document the profile
  assigns, the document's voice wins, and the agent's brief says so. An agent the map does not name
  writes in the default voice. The gate judges a document by its own voice, since it cannot tell
  who wrote a file.
- **`allow`:** the exact strings of section 9.
- Every voice the profile names is a file in `docs/standards/voices/`. The gate prints any file's
  voice and audience on request.
- The updater merges the profile three-way, so a development path a release adds reaches a project
  and the project's own rules are kept.

---

## 5. Characters

Every voice and audience. A governed file holds printable ASCII (U+0020 to U+007E), tab and
newline, and letters and their accents (Unicode categories L and M), so a name keeps its spelling.
Code blocks are judged too, a pasted tree or arrow being the same tell (decision 2026-10-24-018). A
rule, fixture or entry about a character names it by its code point, never by the character itself.

Each finding names the character by its code point with its ASCII replacement:

| Code points | Characters | Replace with |
|-------------|------------|--------------|
| U+2014 | em dash | a comma, a colon, parentheses or two sentences |
| U+2013 | en dash | a hyphen, or `to` in a range |
| U+2212 | minus sign | a hyphen |
| U+2018, U+2019 | single curly quotes | a straight apostrophe |
| U+201C, U+201D | double curly quotes | a straight double quote |
| U+2026 | horizontal ellipsis | three full stops |
| U+00A7 | section sign | the word `section` |
| U+00B7, U+2022 | middle dot, bullet | a comma, a hyphen or a list item |
| U+00D7 | multiplication sign | the letter `x` |
| U+2264, U+2265 | less-than or equal, greater-than or equal | `<=`, `>=` |
| U+00B0 | degree sign | the word `degrees` |
| U+2190 to U+21FF | arrows | `->`, `<-` |
| U+2500 to U+257F | box drawing | `+--`, `-` and a vertical bar |
| U+25A0 to U+25FF | geometric shapes | `v`, `>`, `^` or words |
| U+00A0, U+2007, U+202F | non-breaking spaces | a space |
| U+200B to U+200D, U+2060, U+FEFF | invisible characters | nothing |
| any other | symbols and emoji | words, or nothing |

The fixes with one right answer (curly quotes, the ellipsis, the spaces and invisible characters,
arrows and box drawing) are made by script in the humanizer; the rest are rewritten (decision
2026-10-24-021).

---

## 6. Headings

Every voice and audience. A heading, a line opening with one to six `#` outside a code block, reads
as a sentence and is refused when it:

- holds a comma or a semicolon;
- ends in a full stop, an exclamation mark, a semicolon or a colon;
- runs over 8 words, a code span counting as one word.

A question mark is allowed. A colon followed by a subtitle is judgement (section 10), since
`Step 1: Install` and the decision format are sound.

**The label rule:** in the formats the gates read, the label before the title is not counted toward
the 8 words: `S<N> - <date> -` opening a sprint-status entry, `Decision <ID>:` opening a decision,
and `Epic: <ID> -` opening an epic in the tracker (decision 2026-10-24-019). Their parsers read the
U+2014 form those labels held before as well.

---

## 7. Phrases

Two tables of exact phrases, which the gate reads from this section (decision 2026-10-24-018).

- The AI table applies to every voice. The marketing table applies to every voice whose `tables:`
  names it, every built-in voice but `creative`.
- Matching is case-insensitive at word boundaries, outside code spans and code blocks, where a
  phrase is quoted rather than used. The space between two words of a phrase matches any
  whitespace, a line break included. Each phrase sits in a code span here, so this standard never
  flags itself.
- **Where** is `anywhere`, or `list end`: the phrase closes a sentence or a list item, followed by
  a full stop, an exclamation mark or a closing parenthesis, or ending its paragraph or list item.
- Every form is listed, and a phrase matches only as written. A phrase joins a table only once it
  is seen in an agent's writing, by a review finding or a humanizer rewrite, and leaves at its first
  false positive. Each change is a version-log row opening `fact:`.

### AI phrases

| Phrase | Where |
|--------|-------|
| `delve into` | anywhere |
| `a testament to` | anywhere |
| `it's worth noting` | anywhere |
| `it is worth noting` | anywhere |
| `it's important to note` | anywhere |
| `it is important to note` | anywhere |
| `plays a pivotal role` | anywhere |
| `plays a crucial role` | anywhere |
| `plays a vital role` | anywhere |
| `in the realm of` | anywhere |
| `let's dive in` | anywhere |
| `I hope this helps` | anywhere |
| `and more` | list end |
| `and much more` | list end |
| `and so much more` | list end |

### Marketing phrases

| Phrase | Where |
|--------|-------|
| `seamless` | anywhere |
| `seamlessly` | anywhere |
| `cutting-edge` | anywhere |
| `game-changer` | anywhere |
| `game-changing` | anywhere |
| `unlock the power` | anywhere |
| `unlock the potential` | anywhere |
| `harness the power` | anywhere |
| `world-class` | anywhere |
| `best-in-class` | anywhere |
| `next-generation` | anywhere |
| `revolutionize` | anywhere |
| `supercharge` | anywhere |
| `effortless` | anywhere |
| `effortlessly` | anywhere |

---

## 8. Development references

Production documents only (decision 2026-10-24-018). A development reference means nothing to a
production reader:

| Reference | Its form |
|-----------|----------|
| A decision ID | `YYYY-MM-DD-NNN`, with or without a project's prefix, as `ACME-2026-09-24-001` |
| A story ID | `<PREFIX>-<epic>.<story>`, as `TMPL-6.2` |
| A session number | `S` and a number standing as a word, as `S19` |
| A wikilink | two square brackets on each side of a slug |
| The Chair | `the Chair` or `The Chair` |
| A sprint or orchestration path | `sprint/` or `docs/orchestration/` |
| A commit hash | 7 to 40 hexadecimal characters holding a digit and a letter |

A reference in a code span or a code block still counts. A production document that must cite one,
as a runbook pinning a commit does, has the exact string in the allow list.

---

## 9. The allow list

`allow:` in `writing-profile.yaml` lists exact strings exempt from all four mechanical rules, one
line per real collision, as `Amazon S3` or a commit a runbook pins (decisions 2026-10-24-018 and
2026-10-24-020).

- A finding is exempt where the text it flags lies inside an occurrence of an allowed string in the
  same file. A heading is exempt when an allowed string holds its whole text.
- The list starts empty, in the template and in every project born from it.
- There is no log of mechanical findings. The list is the record, and each line is a visible commit.
- A change to the list is a gate change: in `/story` it is the trigger of a gate or CI change,
  approved by the Chair before the story closes.

---

## 10. Refusal and judgement

- **A mechanical finding refuses** the commit locally and fails the `gates` run in CI. Each finding
  prints its fix and the allow-list line that would exempt it (decision 2026-10-24-020). No gate is
  loosened for a sweep.
- **An agent's own draft** that the gate refuses is the agent's to fix, as a failing test is. Text
  already in the tree goes through the humanizer, which rewrites only the flagged text, in the
  document's voice, and keeps nothing without the Chair's answer (decision 2026-10-24-021).
- **Judgement** covers what no pattern shows: tone against the voice's traits, filler, hedging,
  flattery, cadence, vague claims and colon subtitles. It is held by `.claude/rules/writing.md`,
  path-scoped to the governed markdown. The `document-reviewer` judges a document against it and
  records each finding, the `editor` rewrites through the humanizer, and the reviewer is never the
  builder.
- **A judgement finding pauses** its story until the Chair answers. It is recorded in
  `docs/code_review_log.md` with the Chair's response, the path every review finding takes; there is
  no new log.

---

## 11. Produced documents

A Word, Excel, PDF or PowerPoint deliverable is judged twice (decision 2026-10-24-022):

- its markdown source, from which `scripts/md_to_docx.py` makes it, by the gate as any governed
  file, in the voice and audience its profile rule gives;
- the produced file's text, by the document-production skill's check step, which runs this
  standard's mechanical rules over it as a production document.

The brand's locked terms and the vendor spelling rule are project data, in section 10 of
`docs/standards/document_production_standard_v1.0.md`; how a deliverable looks is that standard's.

---

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.0 | 2026-10-24 | 2026-10-24-014, 2026-10-24-016, 2026-10-24-017, 2026-10-24-018, 2026-10-24-019, 2026-10-24-020, 2026-10-24-022, 2026-10-24-025 | Written as the authority for writing (TMPL-6.2): the voices and audiences, the profile, the four mechanical rules and the phrase tables, the allow list, refusal and judgement, and produced documents | d1c6ef9 |
