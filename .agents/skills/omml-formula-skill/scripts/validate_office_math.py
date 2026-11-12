#!/usr/bin/env python3
"""Validate Office Math presence and obvious context mistakes in DOCX/PPTX files."""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict

from lxml import etree

from omml_utils import NS, find_placeholders, has_ancestor, qn

PPT_CONTENT_RE = re.compile(
    r"^ppt/(slides/slide\d+|notesSlides/notesSlide\d+|slideMasters/slideMaster\d+|slideLayouts/slideLayout\d+)\.xml$"
)
WORD_CONTENT_RE = re.compile(
    r"^word/(document|footnotes|endnotes|comments|glossary/document)\.xml$|^word/(header|footer)\d+\.xml$"
)


def include_part(file_type: str, name: str, deep: bool) -> bool:
    if not name.endswith(".xml"):
        return False
    if file_type == ".pptx":
        return bool(PPT_CONTENT_RE.match(name)) if deep else bool(re.match(r"^ppt/slides/slide\d+\.xml$", name))
    if file_type == ".docx":
        return bool(WORD_CONTENT_RE.match(name)) if deep else name == "word/document.xml"
    return False


def scan(path: Path, *, deep: bool = True) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "file": str(path),
        "type": path.suffix.lower(),
        "xml_files_scanned": 0,
        "omath": 0,
        "omath_para": 0,
        "ppt_a14_m": 0,
        "ppt_bad_context_omath": [],
        "placeholders": [],
        "parts": {},
    }
    with zipfile.ZipFile(path, "r") as zf:
        for name in zf.namelist():
            if not include_part(result["type"], name, deep):
                continue
            data = zf.read(name)
            try:
                root = etree.fromstring(data)
            except etree.XMLSyntaxError as exc:
                result["parts"][name] = {"xml_error": str(exc)}
                continue

            omath_nodes = root.xpath(".//m:oMath", namespaces=NS)
            omath_para_nodes = root.xpath(".//m:oMathPara", namespaces=NS)
            a14_m_nodes = root.xpath(".//a14:m", namespaces=NS)
            text = "".join(root.itertext())
            placeholders = find_placeholders(text)

            bad_contexts = []
            if result["type"] == ".pptx":
                for idx, node in enumerate(omath_nodes, start=1):
                    if not has_ancestor(node, qn("a14", "m")):
                        bad_contexts.append(idx)
                for idx in bad_contexts:
                    result["ppt_bad_context_omath"].append({"file": name, "index": idx})

            result["xml_files_scanned"] += 1
            result["omath"] += len(omath_nodes)
            result["omath_para"] += len(omath_para_nodes)
            result["ppt_a14_m"] += len(a14_m_nodes)
            for formula_id in placeholders:
                result["placeholders"].append({"file": name, "id": formula_id})
            result["parts"][name] = {
                "omath": len(omath_nodes),
                "omath_para": len(omath_para_nodes),
                "ppt_a14_m": len(a14_m_nodes),
                "placeholders": placeholders,
                "bad_context_omath": bad_contexts,
            }
    return result


def print_human(result: Dict[str, Any]) -> None:
    print(f"File: {result['file']}")
    print(f"Type: {result['type']}")
    print(f"XML files scanned: {result['xml_files_scanned']}")
    print(f"m:oMath: {result['omath']}")
    print(f"m:oMathPara: {result['omath_para']}")
    print(f"a14:m: {result['ppt_a14_m']}")
    print(f"PowerPoint m:oMath outside a14:m: {len(result['ppt_bad_context_omath'])}")
    print(f"Unresolved placeholders: {len(result['placeholders'])}")
    for item in result["placeholders"]:
        print(f"  - {item['file']}: {{OMML:{item['id']}}}")
    for item in result["ppt_bad_context_omath"]:
        print(f"  - bad PPT math context: {item['file']} m:oMath[{item['index']}]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan DOCX/PPTX for Office Math and unresolved placeholders.")
    parser.add_argument("file", help="DOCX or PPTX file to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of human-readable output.")
    parser.add_argument("--shallow", action="store_true", help="Only scan main document.xml or slide XML parts.")
    parser.add_argument("--expect-min-omath", type=int, default=None, help="Fail unless at least this many m:oMath nodes exist.")
    parser.add_argument("--fail-on-placeholder", action="store_true")
    parser.add_argument("--fail-on-no-math", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Fail on unresolved placeholders, no math, or bad PPT context.")
    args = parser.parse_args()

    result = scan(Path(args.file), deep=not args.shallow)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)

    failed = False
    if (args.fail_on_placeholder or args.strict) and result["placeholders"]:
        failed = True
    if (args.fail_on_no_math or args.strict) and result["omath"] == 0:
        failed = True
    if args.expect_min_omath is not None and result["omath"] < args.expect_min_omath:
        failed = True
    if args.strict and result["ppt_bad_context_omath"]:
        failed = True
    if failed:
        sys.exit(2)


if __name__ == "__main__":
    main()
