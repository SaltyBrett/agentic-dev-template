# Resources

Reference documentation and external inputs for the project.

---

## Branding Assets (`branding/`)

> **AUTHORITATIVE REFERENCE:** `resources/branding/`
> Agents generating any documents, reports, presentations, or exports MUST follow these brand guidelines.
>
> **The authoritative written standard is [`docs/standards/document_production_standard_v1.0.md`](../docs/standards/document_production_standard_v1.0.md)**
> — it governs typography, color roles, structure, writing mechanics, and per-document-type patterns.
> The quick-reference tables below are a subset for convenience; where they and the standard differ, the
> standard wins.

**This directory ships empty in the template.** Populate it per project with that project's own brand
assets, then fill in the tables below. Do not carry one organization's brand assets into another
organization's repo.

### Logos

| File | Use Case |
|------|----------|
| `{{LOGO_LIGHT_BG}}` | **Light backgrounds** — full-color logo, transparent background. Documents, slides, and web on white or light surfaces. |
| `{{LOGO_DARK_BG}}` | **Dark backgrounds** — reversed logo. Dark surfaces, headers, banners. |

### Brand Guidelines

| File | Contents | When to Reference |
|------|----------|-------------------|
| `{{LOGO_GUIDE_PDF}}` | Logo versions (full lockup vs mark-only), file-type guidance (EPS/SVG/PNG), clear-space rules, color-variant treatments | Any time a logo is placed in a generated document |
| `{{COLOR_PALETTE_PDF}}` | Complete palette with RGB, CMYK, and PMS values, plus gradient definitions | Any time colors are applied to documents, charts, themes, or UI elements |
| `{{TYPEFACE_PDF}}` | Typography standards, primary and secondary families | Any time fonts are selected for documents or reports |

### Quick Reference — Brand Colors

Fill from the project's palette source. Keep hex computed from the official RGB, not eyeballed.

| Role | Color | RGB | Hex |
|------|-------|-----|-----|
| Primary | `{{PMS_PRIMARY}}` | `{{RGB_PRIMARY}}` | `{{HEX_PRIMARY}}` |
| Secondary | `{{PMS_SECONDARY}}` | `{{RGB_SECONDARY}}` | `{{HEX_SECONDARY}}` |
| Accent | `{{PMS_ACCENT}}` | `{{RGB_ACCENT}}` | `{{HEX_ACCENT}}` |
| Deep anchor | `{{PMS_ANCHOR}}` | `{{RGB_ANCHOR}}` | `{{HEX_ANCHOR}}` |
| Neutral gray | `{{PMS_NEUTRAL}}` | `{{RGB_NEUTRAL}}` | `{{HEX_NEUTRAL}}` |

### Quick Reference — Typography

| Role | Font Family | Usage |
|------|-------------|-------|
| **Primary** | `{{FONT_HEADING}}` | Headings, titles, hero text |
| **Secondary** | `{{FONT_BODY}}` | Body text, paragraphs, captions |
| **Fallback pair** | `{{FONT_HEADING_FALLBACK}}` / `{{FONT_BODY_FALLBACK}}` | When brand fonts are unavailable or cannot be embedded |

### Document Templates (`branding/templates/`)

Ships empty. Populate it with two Word templates carrying the theme, heading styles, logo header,
triangle bullets, and footer, then **clone these rather than building from scratch** (see
[`document_production_standard_v1.0.md`](../docs/standards/document_production_standard_v1.0.md) §1).

| File | Fonts | Use |
|------|-------|-----|
| `{{TEMPLATE_BRANDFONT}}` | `{{FONT_HEADING}}` / `{{FONT_BODY}}` | Outward-facing, designed, contractual (embed fonts on save) |
| `{{TEMPLATE_FALLBACK}}` | `{{FONT_HEADING_FALLBACK}}` / `{{FONT_BODY_FALLBACK}}` | Routine internal documents; portable, no embedding needed |

---

## Other Resources

Place additional reference materials here:
- Source system data dictionaries
- External specification documents
- Baseline configuration files
- Vendor-provided reference materials

**Rule:** Do not store generated artifacts here. Use the appropriate `docs/` subdirectory for
project-created documentation.
