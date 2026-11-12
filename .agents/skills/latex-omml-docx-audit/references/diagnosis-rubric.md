# Diagnosis Rubric

## Labels

- `native-omml`
  - OMML nodes are present
  - raw LaTeX residue is zero or negligible
  - conclusion: Word-native formula storage is working

- `mixed-state`
  - OMML nodes are present
  - raw LaTeX residue also remains in normal text runs
  - conclusion: the document is only partially converted

- `plain-text-latex`
  - OMML nodes are absent
  - raw LaTeX commands or formula-like text remain
  - conclusion: formulas were stored as plain text, not native equations

- `no-formula-evidence`
  - neither OMML nor strong text-formula evidence is found
  - conclusion: either the file has no formulas or the source workflow needs deeper inspection

## Report wording

Always separate:

1. What the XML evidence shows
2. What likely happened in the generation pipeline
3. What workflow should replace it
