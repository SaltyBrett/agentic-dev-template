# Document Production Standard v1.0

**Version:** 1.0
**Created:** {{DATE}}
**Status:** Active. **AUTHORITATIVE** for all Word, Excel, PDF, and PowerPoint deliverables.
**Brand assets:** `resources/branding/` (logos, color palette, typeface guide) — populate per project.

> **Template note.** Sections 1 through 6 carry `{{TOKENS}}` for per-project brand values. Fill them
> from the project's own brand source before first use, and record the source in §15. Sections 7
> through 14 are portable craft rules and apply as written in any project.

---

# Document Production Style Guide

**What this is.** The complete formatting, typography, color, structure, and writing standard for
producing this project's documents and presentations, so any agent (Claude Code, Codex, or another)
reproduces the same look and feel. Align it to the project's official brand assets before relying on it.

**Label key:**
- **[Brand official]** Taken directly from the project's official brand guidelines. Authoritative.
- **[Locked]** A confirmed working standard, established across prior documents.
- **[Suggested]** A reasonable default not yet confirmed against a finished document.
- **[Get from source]** Deliberately unfilled. Retrieve from the brand asset named.

**Production note.** The polish comes from generating real, theme-styled Word and PowerPoint files
(true heading styles, a defined theme, consistent spacing, tables instead of walls of text), not
markdown converted crudely. Build actual .docx and .pptx with the theme values below applied at the
document and theme level. Display and web fonts may not be installed in Office; see the fallback in §1.

---

## 1. Typography

**Official brand typefaces [Brand official]:**
- **Primary (headings, titles, hero text):** `{{FONT_HEADING}}`
- **Secondary (body, paragraphs, captions):** `{{FONT_BODY}}`

**Office fallback [Locked].** When the brand fonts are not installed or cannot be embedded (common in
everyday Word and PowerPoint), use the established substitutes:
- **Headings:** `{{FONT_HEADING_FALLBACK}}`
- **Body:** `{{FONT_BODY_FALLBACK}}`

Choose fallbacks that ship with the target operating systems. A fallback that is absent on macOS or
Windows silently substitutes at render time and breaks the house look without warning.

**Starter Word templates [Locked].** Two ready-to-clone templates belong in
`resources/branding/templates/`, one per pairing; the folder ships empty and the project populates
it. **Clone the matching one instead of building from scratch** (each carries the theme, branded
heading styles, triangle bullets, logo header, sensitivity banner, and the standard footer):
- `{{TEMPLATE_BRANDFONT}}` — brand pairing. Outward-facing, designed, contractual. If the recipient may
  not have the brand fonts, embed them (Word: Save, "Embed fonts in the file") or use the fallback.
- `{{TEMPLATE_FALLBACK}}` — fallback pairing. Routine internal documents; fully portable.

**Type scale [Suggested]** (confirm against a finished document; brand assets rarely specify point sizes):

| Role | Size | Weight |
|------|------|--------|
| Title | 28 pt | Bold |
| Subtitle | 14 pt | Italic |
| H1 | 20 pt | Bold |
| H2 | 16 pt | Bold |
| H3 | 13 pt | Bold |
| Body | 11 pt | Regular |
| Caption / table text | 9–10 pt | Regular |

---

## 2. Color Palette

All values below come from the project's palette source. Compute hex from the official RGB rather than
eyeballing it. **[Brand official]** once filled; **[Get from source]** until then.

| Role | Hex | RGB | CMYK | PMS |
|------|-----|-----|------|-----|
| Primary | `{{HEX_PRIMARY}}` | `{{RGB_PRIMARY}}` | `{{CMYK_PRIMARY}}` | `{{PMS_PRIMARY}}` |
| Secondary | `{{HEX_SECONDARY}}` | `{{RGB_SECONDARY}}` | `{{CMYK_SECONDARY}}` | `{{PMS_SECONDARY}}` |
| Accent | `{{HEX_ACCENT}}` | `{{RGB_ACCENT}}` | `{{CMYK_ACCENT}}` | `{{PMS_ACCENT}}` |
| Deep anchor | `{{HEX_ANCHOR}}` | `{{RGB_ANCHOR}}` | `{{CMYK_ANCHOR}}` | `{{PMS_ANCHOR}}` |
| Neutral gray | `{{HEX_NEUTRAL}}` | `{{RGB_NEUTRAL}}` | `{{CMYK_NEUTRAL}}` | `{{PMS_NEUTRAL}}` |

**Primary vs secondary grouping [Brand official].** Record which colors the brand treats as the primary
signature set and which are secondary support. Series colors in charts draw from the secondary set;
structure and neutrals come from the anchor and gray.

**Palette discrepancies [Brand official].** Brand sources disagree more often than people expect: a logo
file guide and a palette document can render the same PMS at different RGB values. When they conflict,
record which source wins for document design and which applies to logo art, and note it here. Do not
silently average them.

---

## 3. Color Roles in Documents

- **Primary heading / H1:** `{{HEX_PRIMARY}}` for branded documents, or `{{HEX_ANCHOR}}` (the deepest
  anchor) for covers, dark backgrounds, and dark headers.
- **Secondary heading / H2, accent rules, table header fills:** `{{HEX_SECONDARY}}`.
- **Signature pop, used sparingly:** `{{HEX_ACCENT}}`.
- **Body text:** near-black `#1A1A1A`, or `{{HEX_ANCHOR}}` for a branded feel.
- **Neutrals, rules, secondary table fills:** `{{HEX_NEUTRAL}}` and tints of it.
- **Data visualization:** draw series colors from the secondary and accent families; reserve the anchor
  and gray for structure and neutrals.

**Callout accent [Locked].** Most brand palettes have no dedicated callout color. Designate one that sits
outside the palette's dominant temperature so it reads instantly as emphasis without competing: if the
palette is cool, an amber such as `#D97706` works well. Use it only for genuine callouts, for example
threading a document's one or two north-star objectives across content slides. Its impact depends on
rarity: one callout element on a page or slide works, several do not. A callout accent never takes a
structural role; the brand colors still carry headings, accents, and neutrals.

---

## 4. Logo Usage

**Versions:** a full logo lockup and a mark-only version. Choose the full lockup by default; use
mark-only where space or context calls for it.

**File type by use:**
- **Print / scalable:** EPS or SVG.
- **Screen / embedded in documents:** PNG with transparency.
- Never upscale a raster logo. Never recolor outside the approved variants.

**Clear space:** `{{LOGO_CLEAR_SPACE_RULE}}` — take the exact rule from the logo guide. Do not crowd the
logo. **[Get from source]**

**Placement:** logo in the header for branded documents (see §6). Keep the logo image files with the
template. **[Get from source]**

---

## 5. Classification and Sensitivity Banners

- Apply the banner the project's handling rules require, at the top of every page, centered, bold, caps.
- Common internal markings: `INTERNAL // BUSINESS SENSITIVE`, `CONFIDENTIAL`.
- Government and regulated work carries its own mandatory marking scheme. **Use the program's marking
  guide, not this template**, and never invent or approximate a control marking.
- Branded or contractual documents typically carry no classification banner but do carry a
  confidentiality footer (see §6).
- **The banner is not a substitute for handling controls.** A marked document still has to live in an
  environment authorized for that marking.

---

## 6. Headers, Footers, Revisions

- **Branded header [Locked]:** project logo, with the clear-space rule respected.
- **Branded footer [Locked]:** `{{CONFIDENTIALITY_FOOTER}}`.
- **Page numbering:** "Page X of Y" in the footer for any document over two pages.
- **Revision labeling [Locked]:** documents that iterate carry an explicit revision marker (Rev A, Rev B,
  and so on) on the cover and in the changelog. Do not rely on file dates.
- **Changelog:** a table at the end of the document, version / date / author / summary.

---

## 7. Document Structure and BLUF

- **BLUF opening [Locked]:** lead with the bottom line. Where a labeled lead-in is used, the label is "Overview," not "BLUF," "Summary," or "Abstract."
- **Flow:** Overview/BLUF, then substance organized by decision value, then supporting detail, matrices, and a glossary where warranted. Organized by usefulness, not chronology.
- **Locked closing lines by type [Locked]:** several document types have an agreed exact closing sentence; reuse it verbatim. Known examples: Informational briefing documents for leadership close with only "Draft for internal leadership review."; tool/assessment documents use a non-recommendation closer such as "This document is informational and is not intended to recommend approval or mandate adoption of any tool." Confirm the current locked closer for a given type before finalizing.

---

## 8. Bullets and Lists

- **Triangle bullets** are the house bullet style. **[Locked]**
- Bullets should be substantive (a full sentence or more), not fragments.
- Prefer tables and matrices over long bulleted runs for comparative or repeating content.
- Do not over-format; use the minimum structure that makes the content clear.

---

## 9. Writing Mechanics (House Style)

Absolute. **[Locked]**
- **No em dashes anywhere.** Use commas, colons, parentheses, or separate sentences.
- **Vendor and product names** are spelled exactly as the vendor spells them, including internal capitals. Record the project's recurring ones in the list below and never vary them.
- **Depersonalized framing** for organizationally sensitive topics: frame gaps as process or system gaps, never as an individual's failure (for example, an implementation shortfall is an implementation and process-alignment gap, not someone's mistake).
- **Direct, structured, executive-ready prose:** enough to act on, no filler, no padded caveats, clear recommendation and decision logic.
- **Consistency over cleverness:** once a term or convention is locked, it holds across every downstream artifact.

---

## 10. Locked Terminology and Phrases

Reuse exactly where they apply. **[Locked]**
- "manually keyed" for manual data entry, in preference to "hand-entered" or "manual entry."
- "Why it matters:" as a recurring labeled lead-in.
- A single agreed name for the destination of record in data narratives (for example "Data Warehouse"), used consistently rather than varied for style.
- "Advanced Shipment Notification (ASN)" spelled out on first use, then ASN, in cross-dock material.
- `{{PREFERRED_TERM}}` rather than `{{DEPRECATED_TERM}}` — record each substitution the project has agreed and the reason.
- Product and architecture names used consistently once fixed. List the project's canonical set here so agents do not paraphrase them.

Record new locked terminology as it is established so it carries forward unchanged.

---

## 11. Document-Type Templates

**PRD [Locked pattern]:** revision-labeled; Overview/BLUF; scope; requirements; architecture reference; open questions; organized for decision value. Reaches multiple revisions (Rev A through Rev D seen).

**Architecture Document [Locked pattern]:** revision-labeled; layered architecture; data model and integration points; constraints (for example the portability requirements of `CONSTITUTION.md` §5); open questions.

**Functional Swimlanes / Audit Document [Locked pattern]:** multi-section (an example ran to 11 sections), including an access-rights remediation matrix, a role-to-screen grid, an auditor-facing control narrative, and a glossary. Swimlanes separate responsibilities cleanly with a named handoff artifact.

**Risk Briefing [Locked pattern]:** sensitivity banner (for example INTERNAL // BUSINESS SENSITIVE); a subtitle stating the exposure; a BLUF box labeled "Overview"; the locked closing line for that briefing.

**Statement of Work [Locked pattern]:** full brand treatment (brand font pairing, `{{HEX_PRIMARY}}` H1, `{{HEX_SECONDARY}}` H2, accent rules, logo header, confidentiality footer); scope of work; named roles and consultation contacts; deliverables.

**Assessment / Compliance Document [Locked pattern]:** company-neutral tone; comparison matrix; a non-recommendation closing sentence; an explicit compatibility dimension where relevant (for example GCC Moderate / FedRAMP).

---

## 12. Presentation (PPTX) Conventions

- Matched design language across a deck family so related decks read as a set. **[Locked]**
- Brand palette from §2: anchor and primary for structure, secondary for accents and rules, accent color as the signature pop, gray as neutral. Brand font pairing where the fonts can be embedded, fallback pairing otherwise. **[Brand official palette and type]**
- Amber `#D97706` is the designated selective callout accent (see Section 3), used for genuine emphasis such as threading the north-star objectives across content slides. Use it sparingly. **[Locked]**
- Leadership-facing structure: a clear narrative spine, one idea per slide, "Why it matters:" framing where used, PMBOK-aligned program-management framing where the deck calls for it. **[Locked]**
- Produced programmatically for consistency (Node.js with pptxgenjs has been the tool), which keeps spacing, fonts, and color roles uniform across the deck family. **[Locked approach]**
- Keep slide text tight; the deck supports the talk, it is not the document.

---

## 13. General Document-Craft Defaults

- Real styles and a real theme, not manual formatting per element, so documents stay consistent and editable.
- Clear visual hierarchy: headings that differ in weight and size, generous whitespace, aligned elements.
- Tables and matrices for comparative or repeating content; prose for reasoning and narrative.
- Restraint with emphasis: bold and color carry meaning, so use them sparingly and consistently.
- Every deliverable is immediately actionable: a clear recommendation, the reasoning, the tradeoffs, and the next step.

---

## 14. Still Worth Capturing for a Pixel-Exact Match

The brand assets now supply typography, the full color palette, and logo rules. To get from close to exact, still capture:
- **Exact heading and body point sizes and spacing:** open a finished, approved document and read the styles. The brand assets do not specify sizes. **[Get from source]**
- **The actual logo image files** (PNG, EPS, SVG; full lockup and mark-only) to keep alongside the template. **[Get from source]**
- **Word templates:** two theme-embedded starter templates in `resources/branding/templates/` (brand-font and fallback pairings; see Section 1), a **.potx theme for PowerPoint** and an **Excel template** with named brand cell styles. **[Get from source]**
- **Confirmation of the primary and secondary** swatch mapping if exactness matters (Section 2). **[Get from source]**
- **The current locked closing sentence** for each document type (Section 7). **[Get from source]**

With those in hand, this guide plus the official brand values should let the new agent reproduce your document style closely and consistently.

---

## 15. Related

- `resources/branding/` — the raw brand asset files (logos, color palette REV2 PDF, typeface guide) this standard references.
- `resources/README.md` — quick-reference index of those assets (subset of this standard; this standard governs).
<!-- profile:gcc -->
- `CONSTITUTION.md` — platform/compliance law (GCC portability referenced in several document types above).
<!-- /profile:gcc -->
<!-- profile:commercial -->
- `CONSTITUTION.md` — platform/compliance law (§5 names the target environments).
<!-- /profile:commercial -->

---

## 16. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {{DATE}} | — | Initial version. Adopted the project document production style guide as the authoritative standard. |
