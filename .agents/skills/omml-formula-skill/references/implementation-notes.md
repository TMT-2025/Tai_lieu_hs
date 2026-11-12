# Implementation Notes

## Contents

- Conversion strategy
- Word injection
- PowerPoint injection
- Namespace handling
- Why not python-pptx directly
- Validation limits

## Conversion strategy

The skill does not implement a LaTeX parser. It delegates LaTeX math parsing to Pandoc, asks Pandoc to create a temporary DOCX, then extracts Office Math nodes from `word/document.xml`.

This is pragmatic: Pandoc emits OMML for many common LaTeX math expressions, and Microsoft Office uses OMML as the modern editable equation representation.

## Word injection

WordprocessingML can contain Office Math inside paragraphs.

The injector scans these parts:

- `word/document.xml`
- `word/header*.xml`
- `word/footer*.xml`
- `word/footnotes.xml`
- `word/endnotes.xml`
- `word/comments.xml`
- `word/glossary/document.xml`

For formula-only paragraphs, the script inserts `m:oMathPara`. For inline placeholders embedded in text, it inserts `m:oMath`.

The affected paragraph is rebuilt. Paragraph-level properties (`w:pPr`) are preserved. The first run's style (`w:rPr`) is copied to rebuilt text runs unless `--no-run-style` is used.

## PowerPoint injection

PowerPoint formulas are injected into DrawingML paragraphs as:

```xml
<a14:m>
  <m:oMathPara>
    <m:oMath>...</m:oMath>
  </m:oMathPara>
</a14:m>
```

The script also sets `mc:Ignorable="a14"` on modified slide/notes/master/layout roots and ensures both `mc` and `a14` prefixes are declared on that root element.

The affected paragraph is rebuilt. Paragraph-level properties (`a:pPr`) and `a:endParaRPr` are preserved. The first run's style (`a:rPr`) is copied to rebuilt text runs unless `--no-run-style` is used.

## Namespace handling

PowerPoint markup-compatibility attributes are prefix-sensitive. If the root contains `mc:Ignorable="a14"`, the `a14` namespace must be in scope on that same root. A namespace declaration only on a child `a14:m` element is not enough for the root attribute.

The v3 injector rebuilds the XML root with required namespace declarations when necessary.

## Why not python-pptx directly?

`python-pptx` can author text boxes and shapes, but it does not provide a first-class API for PowerPoint Office Math. Directly appending raw OMML may produce legal XML that PowerPoint still ignores. The safer workflow is to create a normal deck first and patch the generated OOXML afterward.

## Validation limits

`validate_office_math.py` checks structural conditions:

- whether OMML nodes exist;
- whether placeholders remain unresolved;
- whether PowerPoint `m:oMath` nodes are outside `a14:m` wrappers.

It cannot prove that Microsoft PowerPoint will render every formula exactly as intended. Always open important outputs in Microsoft Office before final delivery.
