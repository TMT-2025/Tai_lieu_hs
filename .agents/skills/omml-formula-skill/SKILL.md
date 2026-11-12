---
name: omml-formula-skill
description: Convert LaTeX equations into editable Office Math (OMML) in Microsoft Word DOCX and PowerPoint PPTX files; replace {{OMML:id}} placeholders, repair blank PowerPoint formulas caused by raw m:oMath insertion, validate equation XML, and generate PNG fallback assets when OMML is unsafe. Use for LaTeX, equations, formulas, OMML, DOCX, PPTX, Word, PowerPoint, python-docx, python-pptx, or PptxGenJS formula workflows.
license: MIT
compatibility: Requires Python 3.10+, Pandoc on PATH, and Python packages in requirements.txt; intended for Claude Code or agents with filesystem and bash access.
metadata:
  version: "3.0.0"
  domain: office-math
  supports: "docx,pptx,latex,omml"
---

# OMML Formula Skill

## What this skill does

Use this skill to make formulas in generated Word or PowerPoint files **visible and editable as Office Math**, not just pasted as plain text.

The stable workflow is:

```text
LaTeX → Pandoc temporary DOCX → extract OMML → replace {{OMML:id}} placeholders in target DOCX/PPTX → validate
```

## Do not use this skill for

- Explaining math concepts without editing a DOCX/PPTX.
- Rendering web MathJax/KaTeX HTML.
- Full LaTeX documents, TikZ diagrams, or publication typesetting.
- Guaranteed LibreOffice/WPS rendering. Final validation should be in Microsoft Word/PowerPoint.

## Core rule

Never directly append a bare PowerPoint formula like this:

```xml
<a:p>
  <m:oMath>...</m:oMath>
</a:p>
```

For PPTX, insert formula placeholders first, then post-process into PowerPoint's recognized math context:

```xml
<a:p>
  <a14:m>
    <m:oMathPara>
      <m:oMath>...</m:oMath>
    </m:oMathPara>
  </a14:m>
</a:p>
```

For DOCX, inject `m:oMathPara` for formula-only paragraphs and `m:oMath` for inline formulas.

## Agent workflow

1. Check dependencies when setting up or after errors:

```bash
python scripts/preflight_check.py
```

2. Put formulas in a JSON file using `examples/formulas.json` as the schema.

3. Generate the target DOCX/PPTX with placeholders such as:

```text
{{OMML:eq1}}
{{OMML:routing_weight}}
```

4. For Word:

```bash
python scripts/insert_word_omml.py \
  --input input.docx \
  --formulas formulas.json \
  --output output.docx
```

5. For PowerPoint:

```bash
python scripts/inject_ppt_omml.py \
  --input input.pptx \
  --formulas formulas.json \
  --output output.pptx
```

Use `--scope all` only when placeholders may exist in notes, masters, or layouts.

6. Validate every generated Office file:

```bash
python scripts/validate_office_math.py output.docx --strict
python scripts/validate_office_math.py output.pptx --strict
```

7. For final delivery, open the file in Microsoft Word/PowerPoint and confirm formulas render and can be edited.

## Formula routing policy

Default to OMML for ordinary math expressions:

```text
simple inline/display math        → OMML
fractions, sums, integrals        → OMML, then validate
matrices                          → OMML, then inspect in Office
custom macros                     → expand in formulas.json macros first
TikZ/minipage/text-heavy blocks   → PNG/SVG fallback, not editable
PowerPoint rendering uncertainty  → keep OMML if editable is required; use image only if visibility matters more
```

`mode` values in `formulas.json`:

- `omml`: convert and inject editable OMML.
- `auto`: currently treated as OMML, reserved for future routing.
- `image`: do not inject as editable math; generate fallback asset only.

## File map

- `scripts/preflight_check.py` — verify Pandoc and Python dependencies.
- `scripts/latex_to_omml.py` — convert one LaTeX expression to OMML XML.
- `scripts/insert_word_omml.py` — replace DOCX placeholders with editable Word math.
- `scripts/inject_ppt_omml.py` — replace PPTX placeholders with editable PowerPoint math.
- `scripts/validate_office_math.py` — structural validation; supports `--strict` and `--json`.
- `scripts/extract_office_math.py` — extract OMML snippets for debugging.
- `scripts/render_latex_assets.py` — optional PNG fallback assets.
- `scripts/smoke_test.py` — end-to-end DOCX/PPTX smoke test.
- `references/workflow.md` — detailed user workflow.
- `references/implementation-notes.md` — OOXML implementation details.
- `references/troubleshooting.md` — fixes for common failures.
- `references/agent-integration.md` — guidance for agent callers.

## Required behavior for agents

- Prefer placeholder-first generation over direct XML mutation during document creation.
- Convert only formulas referenced by placeholders when an input file is provided.
- Run validation after injection and report unresolved placeholders or bad PPT math contexts.
- Be explicit that structural validation is not the same as Microsoft Office GUI rendering validation.
- Use image fallback only when editability is not required or when the user accepts display-only formulas.
