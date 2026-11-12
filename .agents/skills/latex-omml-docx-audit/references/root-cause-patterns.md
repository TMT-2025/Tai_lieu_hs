# Root Cause Patterns

## Pattern 1: Font-only formula styling

Signals:

- OMML count is zero
- Cambria Math mentions are present
- raw LaTeX or plain-text formula syntax remains

Interpretation:

- The pipeline changed appearance, not structure.

Fix:

- Re-run conversion through Markdown plus Pandoc or another OMML-producing path.

## Pattern 2: Raw LaTeX inserted with python-docx

Signals:

- OMML count is zero
- `\frac`, `\sum`, `\eta`, `\sqrt` remain in `w:t` nodes

Interpretation:

- The generator likely wrote formula strings directly into paragraph runs.

Fix:

- Stop using `add_run()` for formulas. Convert from Markdown math to OMML instead.

## Pattern 3: Partial conversion

Signals:

- OMML count is non-zero
- raw LaTeX residue is also non-zero

Interpretation:

- Some formulas were converted, others were left as text.

Fix:

- Normalize the entire source into one conversion pass and validate again.

## Pattern 4: Missing formula stage

Signals:

- OMML count is zero
- raw LaTeX residue is low or absent
- author expected formulas

Interpretation:

- The formula conversion stage may have been skipped, stripped, or flattened upstream.

Fix:

- Inspect the intermediate Markdown or source export step before DOCX generation.
