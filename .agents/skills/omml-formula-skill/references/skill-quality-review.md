# Skill Quality Review

## Contents

- User perspective
- Agent matching perspective
- Anthropic Skills format perspective
- Remaining risks

## User perspective

Strengths:

- The workflow matches how users actually generate Office files: create normal DOCX/PPTX first, then replace placeholders.
- Users get editable OMML for supported formulas instead of screenshot-only math.
- Validation scripts make failure visible instead of silently producing blank formulas.
- PNG fallback exists for delivery-critical display cases.

Weaknesses and mitigations:

- Users still need Pandoc installed. `preflight_check.py` makes this explicit.
- PowerPoint rendering cannot be fully proven by XML validation. The skill tells agents to recommend Microsoft PowerPoint GUI inspection.
- Mixed styled text and formulas in the same paragraph may lose some local styling. The workflow recommends one formula per paragraph/textbox.

## Agent matching perspective

The v3 description contains concrete trigger terms: LaTeX, equations, formulas, OMML, DOCX, PPTX, Word, PowerPoint, python-docx, python-pptx, and PptxGenJS. This improves retrieval compared with a vague description like "handles formulas".

The SKILL.md also states non-trigger cases so agents do not use it for ordinary math explanation tasks.

## Anthropic Skills format perspective

The package follows the core skill pattern:

```text
omml-formula-skill/
├── SKILL.md
├── scripts/
├── references/
├── examples/
└── requirements.txt
```

`SKILL.md` is concise and acts as an overview. Long implementation details are moved to `references/`, while deterministic operations live in `scripts/`.

## Remaining risks

- OMML coverage depends on Pandoc's LaTeX math support.
- PowerPoint may render some valid OMML differently across Office versions.
- The injectors rebuild affected paragraphs and preserve only paragraph properties plus first-run style.
- Image fallback is visible but not editable.
