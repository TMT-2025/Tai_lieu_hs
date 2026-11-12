# Troubleshooting

## The formula is still blank in PowerPoint

1. Run structural validation:

```bash
python scripts/validate_office_math.py output.pptx --strict --json
```

2. Check that the slide XML contains both `a14:m` and `m:oMathPara`.
3. Open the file in Microsoft PowerPoint, not only LibreOffice.
4. Simplify the LaTeX formula and retry.
5. If it is presentation-only, render that specific formula as a PNG fallback.

## Pandoc did not produce OMML

Common causes:

- The input includes a full LaTeX document instead of a math expression.
- The formula depends on custom macros not listed in `macros`.
- The formula uses LaTeX packages that Pandoc's math parser does not understand.
- The formula contains complex text/layout environments rather than math syntax.

Fix by expanding macros in `formulas.json`, simplifying the expression, or switching that formula to image fallback.

## Placeholder was not replaced

Check that the placeholder text exactly matches the formula id:

```text
{{OMML:routing_weight}}
```

Formula ids may contain letters, digits, underscore, dot, colon and hyphen. Avoid spaces and Chinese punctuation in ids.

## Existing text style changed around the formula

The injector rebuilds the affected paragraph because a placeholder may be split across multiple runs. It preserves paragraph properties and copies the first run style to rebuilt text runs, but it does not preserve every local run style.

For highest style stability, put formula placeholders in their own text box or paragraph.

## LibreOffice shows different results

LibreOffice's OMML support is not identical to Microsoft Office. Use LibreOffice for rough inspection only. For final delivery, verify in Microsoft Word/PowerPoint.
