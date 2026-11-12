# Recommended Workflow

## Contents

- Generated Word reports
- Generated PowerPoint decks
- Formula JSON policy
- Formula routing policy
- Validation policy

## Generated Word reports

1. Generate the document with placeholders.
2. Keep standalone formulas in their own paragraphs.
3. Use `insert_word_omml.py` after the DOCX is created.
4. Run `validate_office_math.py --strict`.
5. Open in Microsoft Word and click a formula to confirm editability.

## Generated PowerPoint decks

1. Generate the deck with normal text boxes.
2. Use one placeholder per formula where possible.
3. Avoid mixing heavily styled text and formula placeholders in one paragraph.
4. Use `inject_ppt_omml.py` after the PPTX is created.
5. Validate with `--strict`.
6. Open in Microsoft PowerPoint and confirm visibility/editability.

## Formula JSON policy

Use stable ASCII IDs:

```json
{
  "macros": {
    "\\E": "\\mathbb{E}"
  },
  "formulas": [
    {
      "id": "routing_weight",
      "latex": "\\alpha_{i,m}=\\frac{\\exp(z_{i,m})}{\\sum_{m'}\\exp(z_{i,m'})}",
      "display": true,
      "mode": "omml",
      "alt": "softmax routing weight over modalities"
    }
  ]
}
```

Avoid spaces, Chinese punctuation, and slashes in formula IDs.

## Formula routing policy

Use this default policy:

```text
simple inline/display math        → OMML
fractions/sums/integrals/matrices → OMML, then inspect
custom macros                     → expand macros first
dense derivations                 → split into multiple formulas
TikZ/minipage/text-heavy blocks   → image fallback
unreliable PowerPoint rendering   → image fallback only if editability is not required
```

The goal is not to force every LaTeX expression into OMML. The goal is to maximize editability while preserving delivery reliability.

## Validation policy

Run structural validation after every mutation:

```bash
python scripts/validate_office_math.py output.pptx --strict --json
```

A clean validation means the OOXML structure is plausible. It does not replace opening the file in Microsoft Office for final visual verification.
