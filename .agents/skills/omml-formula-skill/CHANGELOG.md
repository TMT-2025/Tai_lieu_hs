# Changelog

## v3.0.0

- Reworked package layout to match Agent Skills conventions more closely: concise `SKILL.md`, deterministic `scripts/`, and on-demand `references/`.
- Ensured root directory name matches the `name` frontmatter field: `omml-formula-skill`.
- Expanded `SKILL.md` metadata with stronger trigger terms for agent selection: LaTeX, equations, formulas, OMML, DOCX, PPTX, Word, PowerPoint, python-docx, python-pptx, and PptxGenJS.
- Added `compatibility`, `license`, and `metadata.version` frontmatter fields.
- Added `scripts/preflight_check.py` for dependency diagnostics.
- Added `--dry-run` and `--json` to DOCX/PPTX injectors for agent planning.
- Changed injectors to convert only formulas referenced by placeholders in the target file.
- Added clearer errors for placeholders referencing missing IDs or formulas marked `mode=image`.
- Fixed PowerPoint namespace handling so `mc:Ignorable="a14"` has the `a14` prefix in scope on the root element.
- Added `references/agent-integration.md` for calling-agent behavior.

## v2.0

- Rewrote DOCX injection to patch OOXML directly instead of relying on python-docx paragraph traversal only.
- DOCX injector scans document body, tables, headers, footers, footnotes, endnotes, comments and glossary parts.
- Reworked PPTX injector to preserve `a:pPr`, preserve/copy `a:endParaRPr`, copy first run style, and add `mc:Ignorable="a14"` when using `a14:m`.
- Added `--scope` for PowerPoint parts: `slides`, `notes`, `masters`, `layouts`, or `all`.
- Added stricter formula JSON validation, duplicate id checks, and simple macro preprocessing.
- Added `validate_office_math.py --json --strict --expect-min-omath`.
- Added bad PowerPoint context detection for `m:oMath` not wrapped by `a14:m`.
- Added `extract_office_math.py` for debugging generated OMML.
- Added optional PNG fallback renderer via `render_latex_assets.py`.
- Added `smoke_test.py` to create placeholder DOCX/PPTX, inject OMML, and validate end-to-end.
