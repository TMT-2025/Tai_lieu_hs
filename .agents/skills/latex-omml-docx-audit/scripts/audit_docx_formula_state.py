from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

WORD_NS = {
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

LATEX_PATTERN = re.compile(
    r"""\\(
    frac|sum|eta|alpha|beta|gamma|theta|lambda|mu|sigma|phi|psi|omega|
    begin|end|left|right|cdot|times|sqrt|text|mathrm|mathbf|operatorname|
    leq|geq|approx|neq|int|lim|max|min|sin|cos|tan
    )\b""",
    re.VERBOSE,
)

SUB_SUP_PATTERN = re.compile(r"(?<!\w)(?:[A-Za-z]+\_\{[^}]+\}|[A-Za-z]+\^\{[^}]+\})")
CAMBRIA_MATH_PATTERN = re.compile(r"Cambria Math", re.IGNORECASE)


@dataclass
class AuditReport:
    file: str
    files_scanned: int
    omath_nodes: int
    omath_para_nodes: int
    raw_latex_hits: int
    sub_sup_text_hits: int
    cambria_math_mentions: int
    diagnosis: str
    likely_cause: str
    suggested_fix: str
    files_with_raw_latex: list[str]


def iter_word_xml(docx_path: Path) -> Iterable[tuple[str, str]]:
    with zipfile.ZipFile(docx_path) as zf:
        for name in zf.namelist():
            if not name.startswith("word/") or not name.endswith(".xml"):
                continue
            yield name, zf.read(name).decode("utf-8", errors="ignore")


def classify(
    omath_nodes: int,
    omath_para_nodes: int,
    raw_latex_hits: int,
    sub_sup_text_hits: int,
    cambria_math_mentions: int,
) -> tuple[str, str, str]:
    total_omml = omath_nodes + omath_para_nodes
    text_formula_evidence = raw_latex_hits + sub_sup_text_hits

    if total_omml > 0 and raw_latex_hits == 0:
        return (
            "native-omml",
            "Formulas are stored as native Word OMML objects.",
            "No formula-format fix is needed. If appearance is off, inspect layout or authoring details.",
        )
    if total_omml > 0 and raw_latex_hits > 0:
        return (
            "mixed-state",
            "The DOCX contains some native OMML formulas, but also retains raw LaTeX-like text in normal Word runs.",
            "Rebuild the document through a single Markdown-to-OMML path and validate the output XML again.",
        )
    if total_omml == 0 and text_formula_evidence > 0:
        if cambria_math_mentions > 0:
            return (
                "plain-text-latex",
                "The file appears to style formula text, possibly with Cambria Math, but does not contain native OMML equations.",
                "Convert the source through Pandoc or another OMML-producing pipeline instead of writing LaTeX text into DOCX runs.",
            )
        return (
            "plain-text-latex",
            "Formula-like content exists only as plain text, so Word has no native equation objects to render.",
            "Route the source through Markdown plus Pandoc or another OMML-producing conversion path.",
        )
    return (
        "no-formula-evidence",
        "No clear OMML math and no strong plain-text formula residue were detected.",
        "Confirm whether the document is expected to contain formulas. If yes, inspect the source authoring workflow.",
    )


def build_report(docx_path: Path) -> AuditReport:
    omath_nodes = 0
    omath_para_nodes = 0
    raw_latex_hits = 0
    sub_sup_text_hits = 0
    cambria_math_mentions = 0
    files_with_raw_latex: list[str] = []
    files_scanned = 0

    for name, xml_text in iter_word_xml(docx_path):
        files_scanned += 1
        root = ET.fromstring(xml_text)
        omath_nodes += len(root.findall(".//m:oMath", WORD_NS))
        omath_para_nodes += len(root.findall(".//m:oMathPara", WORD_NS))

        text_nodes = [
            node.text or ""
            for node in root.findall(".//w:t", WORD_NS)
            if (node.text or "").strip()
        ]
        joined_text = "\n".join(text_nodes)
        joined_xml = xml_text

        latex_hits = len(LATEX_PATTERN.findall(joined_text))
        sub_sup_hits = len(SUB_SUP_PATTERN.findall(joined_text))
        font_hits = len(CAMBRIA_MATH_PATTERN.findall(joined_xml))

        raw_latex_hits += latex_hits
        sub_sup_text_hits += sub_sup_hits
        cambria_math_mentions += font_hits

        if latex_hits > 0:
            files_with_raw_latex.append(name)

    diagnosis, likely_cause, suggested_fix = classify(
        omath_nodes,
        omath_para_nodes,
        raw_latex_hits,
        sub_sup_text_hits,
        cambria_math_mentions,
    )

    return AuditReport(
        file=str(docx_path),
        files_scanned=files_scanned,
        omath_nodes=omath_nodes,
        omath_para_nodes=omath_para_nodes,
        raw_latex_hits=raw_latex_hits,
        sub_sup_text_hits=sub_sup_text_hits,
        cambria_math_mentions=cambria_math_mentions,
        diagnosis=diagnosis,
        likely_cause=likely_cause,
        suggested_fix=suggested_fix,
        files_with_raw_latex=files_with_raw_latex,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit whether a DOCX stores formulas as native OMML or plain text."
    )
    parser.add_argument("docx", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.docx.exists():
        print(f"File not found: {args.docx}", file=sys.stderr)
        return 2

    report = build_report(args.docx)

    if args.json:
        print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    else:
        print(f"DOCX: {report.file}")
        print(f"Scanned XML files: {report.files_scanned}")
        print(f"Word OMML nodes <m:oMath>: {report.omath_nodes}")
        print(f"Word OMML block nodes <m:oMathPara>: {report.omath_para_nodes}")
        print(f"Raw LaTeX hits in text nodes: {report.raw_latex_hits}")
        print(f"Plain-text subscript/superscript hints: {report.sub_sup_text_hits}")
        print(f"Cambria Math mentions in XML: {report.cambria_math_mentions}")
        print(f"Diagnosis: {report.diagnosis}")
        print(f"Likely cause: {report.likely_cause}")
        print(f"Suggested fix: {report.suggested_fix}")
        if report.files_with_raw_latex:
            print("Files with raw LaTeX:")
            for name in report.files_with_raw_latex:
                print(f"  - {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
