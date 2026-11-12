# Agent Integration Guide

## Contents

- Triggering and non-triggering cases
- Recommended call sequence
- Dry-run planning
- Error handling policy
- User-facing reporting

## Triggering cases

Use this skill when a user asks to create, repair, or validate formulas in Word or PowerPoint documents, especially when they mention:

- LaTeX to Word/PPT formulas
- editable equations
- OMML
- blank formulas in PPT
- `{{OMML:id}}` placeholders
- python-docx, python-pptx, or PptxGenJS formula insertion

Do not trigger this skill for ordinary math tutoring or symbolic solving unless the output must be placed into DOCX/PPTX.

## Recommended call sequence

For an existing target file:

```bash
python scripts/preflight_check.py --json
python scripts/insert_word_omml.py --input input.docx --formulas formulas.json --output output.docx --dry-run --json
python scripts/insert_word_omml.py --input input.docx --formulas formulas.json --output output.docx
python scripts/validate_office_math.py output.docx --strict --json
```

For PPTX, substitute `inject_ppt_omml.py` and use `--scope all` only if placeholders may be outside normal slide XML.

## Dry-run planning

Use `--dry-run --json` before mutation when:

- the user supplied a large formula manifest;
- the target file may contain only a subset of formulas;
- some formulas are marked `mode=image`;
- the agent needs a concise summary of what will change.

The dry-run output lists unique placeholder IDs found in the target file.

## Error handling policy

- Missing Pandoc or packages: run `preflight_check.py` and report the install hint.
- Missing formula ID: tell the user which placeholder ID is absent from `formulas.json`.
- `mode=image` referenced by an OMML placeholder: either change mode to `omml`/`auto` or generate PNG assets.
- Pandoc conversion failure: simplify the LaTeX, expand macros, or mark that formula as image fallback.
- Strict validation failure: report unresolved placeholders and bad PowerPoint contexts before handing off the file.

## User-facing reporting

Report these items after a successful run:

- output file path;
- number of placeholders replaced;
- validation result;
- explicit caveat that structural validation is not GUI rendering validation;
- recommendation to open the file in Microsoft Word/PowerPoint when final delivery matters.
