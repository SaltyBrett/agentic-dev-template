---
name: document-production
description: 'Produce a Word, Excel, PDF or PowerPoint deliverable in the project''s house style, from the values in the document production standard. Use before generating any .docx, .xlsx, .pdf or .pptx document, report, briefing or deck.'
---

# Document production

The values are the law: `docs/standards/document_production_standard_v1.0.md` holds the typography,
palette, color roles, logo rules, banners, structure, writing mechanics, locked terms and the
document-type patterns. This skill is how a deliverable is made from them.

1. **Read the standard whole** this session; do not work from memory of it.
2. **Resolve every value the document needs.** One still a `{{TOKEN}}` or marked [Get from source]
   comes from `resources/branding/`, and the standard's §15 records which file supplied it. If the
   asset is not there, stop and ask. Never invent a brand value, and never invent or approximate a
   control marking (§5).
3. **Choose the type and the pairing.** The type's pattern is in §11. The brand-font pairing serves
   outward-facing, designed and contractual work; the fallback pairing serves routine internal
   documents (§1).
4. **Start from the matching starter** in `resources/branding/templates/` when it exists, never from
   scratch, and build a real file with styles and a theme applied at the document level:
   - a Word document from the starter, or from a markdown draft with
     `python3 scripts/md_to_docx.py <input.md> <output.docx>`, which needs `python-docx` in a real
     interpreter, not one pre-commit provides;
   - a deck programmatically, as §12 locks it;
   - never markdown converted crudely.
5. **Check it before handing it over**, against the standard:
   - it opens with the bottom line, labeled "Overview" where a label is used (§7);
   - the banner its handling rules require, the header logo and the footer (§5, §6);
   - "Page X of Y" on anything over two pages, a revision marker on the cover, a changelog table at
     the end (§6);
   - no em dashes anywhere: search the document's text for the character (§9);
   - the locked terms and vendor spellings (§9, §10);
   - the type's locked closing line, confirmed current with the user (§7).
6. **Report** the file's path, the type, the pairing and the starter used, and each deviation from
   the standard with its reason.
