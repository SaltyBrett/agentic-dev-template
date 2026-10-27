# Issue Log

**Purpose:** Every issue reported against the project, from filing to resolution

> **GOVERNED BY** `docs/standards/sprint_management_standard_v1.0.md` section 12: the fields, the statuses and their links.
>
> **READ SELECTIVELY (index-first).** Read the **Issue Index**, then only the entries the task
> needs. File through the writer, which allocates the ID and keeps the index and the entries in step:
> `python3 scripts/issue_log.py --file`, run by a person in a terminal or by an agent through the
> `/issue` skill. `--update <ID>` changes an issue; `--report` reports. The `[EXAMPLE]` entry shows
> the template every entry follows, and the `issue-log` gate refuses one that departs from it.

---

## Issue Index

| ID | Reported | Title | Kind | Severity | Status | Stories |
|----|----------|-------|------|----------|--------|---------|
| [EXAMPLE] ACME-ISS-0 | 2025-01-15 | The nightly export drops rows with no region | bug | high | Resolved | ACME-2.3 |

---

## Issue [EXAMPLE] ACME-ISS-0

**Title:** The nightly export drops rows with no region
**Reported:** 2025-01-15
**Reporter:** Chair (human)
**Kind:** bug
**Severity:** high
**Status:** Resolved
**Stories:** ACME-2.3
**Decisions:** none
**Resolved by:** 1a2b3c4

### What happened

The nightly export wrote 9,812 of 10,000 rows. The 188 missing rows had no region.

### Expected

Every row exported, a missing region written as an empty field.

### Steps to reproduce

1. Load a table holding a row with no region.
2. Run the export.
3. Count the rows in the file.

### Impact

The downstream totals undercount by about 2% each night.

### Resolution

ACME-2.3 writes a missing region as an empty field and adds a test holding one.

---

<!-- File issues with `python3 scripts/issue_log.py --file` or `/issue`; the writer keeps the index and the entries in step. -->
