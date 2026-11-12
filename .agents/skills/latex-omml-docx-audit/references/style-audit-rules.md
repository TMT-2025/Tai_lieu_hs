# Style Audit Rules

The style audit checks the document defaults at the style layer.

## Required defaults

- Chinese body text: SimSun or 宋体
- English body text: Times New Roman
- Headings: HeiTi, 黑体, or SimHei
- Body text color: black
- Heading color: black
- Headings: not italic

## What the script inspects

- `word/styles.xml`
- `Normal` style for body text
- `Heading1`, fallback `1`, fallback `Title` for headings

## Practical limitation

This audit is aimed at template defaults and common heading styles. It does not attempt to compute every run-level override in the entire document. If style audit passes but the document still looks wrong, inspect local overrides in the rendered output.
