#!/usr/bin/env python3
"""Replace {{OMML:id}} placeholders in DOCX with editable Office Math.

This script patches the DOCX zip directly. It scans the main document, tables,
headers, footers, footnotes, endnotes, comments, and glossary document XML parts.
"""
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path
from typing import Dict, Mapping

from docx import Document
from lxml import etree

from omml_utils import (
    NS,
    clone,
    convert_all,
    copy_zip_with_replacements,
    find_placeholders,
    load_formulas,
    select_formulas_for_placeholders,
    parse_xml,
    qn,
    split_by_placeholders,
    tostring_xml,
)

WORD_PART_RE = re.compile(
    r"^word/(document|footnotes|endnotes|comments|glossary/document)\.xml$|^word/(header|footer)\d+\.xml$"
)


def is_word_content_part(name: str) -> bool:
    return bool(WORD_PART_RE.match(name))


def paragraph_text(paragraph: etree._Element) -> str:
    # Only visible text nodes; intentionally not fields/instructions.
    return "".join(t.text or "" for t in paragraph.xpath(".//w:t", namespaces=NS))


def find_base_rpr(paragraph: etree._Element) -> etree._Element | None:
    rpr = paragraph.find(".//w:rPr", namespaces=NS)
    return clone(rpr) if rpr is not None else None


def make_word_run(text: str, base_rpr: etree._Element | None = None) -> etree._Element:
    run = etree.Element(qn("w", "r"))
    if base_rpr is not None:
        run.append(clone(base_rpr))
    t = etree.SubElement(run, qn("w", "t"))
    if text.startswith(" ") or text.endswith(" "):
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    return run


def formula_only(parts: list[tuple[str, str]]) -> bool:
    non_empty = [(k, v) for k, v in parts if not (k == "text" and v.strip() == "")]
    return len(non_empty) == 1 and non_empty[0][0] == "formula"


def rebuild_word_paragraph(paragraph: etree._Element, omml_by_id: Mapping[str, object], *, keep_run_style: bool) -> int:
    text = paragraph_text(paragraph)
    ids = find_placeholders(text)
    if not ids:
        return 0
    for formula_id in ids:
        if formula_id not in omml_by_id:
            raise KeyError(f"Placeholder references missing formula id: {formula_id}")

    ppr = paragraph.find(qn("w", "pPr"))
    saved_ppr = clone(ppr) if ppr is not None else None
    base_rpr = find_base_rpr(paragraph) if keep_run_style else None

    for child in list(paragraph):
        paragraph.remove(child)
    if saved_ppr is not None:
        paragraph.append(saved_ppr)

    parts = split_by_placeholders(text)
    block_math = formula_only(parts)

    for kind, value in parts:
        if kind == "text" and value:
            paragraph.append(make_word_run(value, base_rpr))
        elif kind == "formula":
            result = omml_by_id[value]
            node = result.o_math_para if (block_math and result.display) else result.o_math
            paragraph.append(clone(node))
    return len(ids)


def collect_docx_placeholder_ids(input_path: Path) -> list[str]:
    ids: list[str] = []
    with zipfile.ZipFile(input_path, "r") as zin:
        for name in zin.namelist():
            if not is_word_content_part(name):
                continue
            tree = parse_xml(zin.read(name))
            root = tree.getroot()
            for paragraph in root.xpath(".//w:p", namespaces=NS):
                ids.extend(find_placeholders(paragraph_text(paragraph)))
    return list(dict.fromkeys(ids))


def inject_docx(input_path: Path, formulas_path: Path, output_path: Path, *, keep_run_style: bool = True) -> int:
    needed_ids = collect_docx_placeholder_ids(input_path)
    omml_by_id = convert_all(select_formulas_for_placeholders(formulas_path, needed_ids))
    replacements: Dict[str, bytes] = {}
    total = 0

    with zipfile.ZipFile(input_path, "r") as zin:
        for name in zin.namelist():
            if not is_word_content_part(name):
                continue
            tree = parse_xml(zin.read(name))
            root = tree.getroot()
            count = 0
            for paragraph in root.xpath(".//w:p", namespaces=NS):
                count += rebuild_word_paragraph(paragraph, omml_by_id, keep_run_style=keep_run_style)
            if count:
                replacements[name] = tostring_xml(tree)
                total += count

    copy_zip_with_replacements(input_path, output_path, replacements)
    return total


def create_document_from_formulas(formulas_path: Path, output_path: Path) -> None:
    formulas = load_formulas(formulas_path)
    omml_by_id = convert_all(formulas)
    doc = Document()
    for formula in formulas:
        p = doc.add_paragraph()
        p._p.append(clone(omml_by_id[formula.id].o_math_para))
    doc.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Replace {{OMML:id}} placeholders in a Word DOCX.")
    parser.add_argument("--input", help="Input DOCX. If omitted, create a new DOCX containing all formulas.")
    parser.add_argument("--formulas", required=True, help="Formula JSON file.")
    parser.add_argument("--output", required=True, help="Output DOCX.")
    parser.add_argument("--no-run-style", action="store_true", help="Do not copy the first run style to rebuilt text runs.")
    parser.add_argument("--dry-run", action="store_true", help="Only report placeholder ids that would be processed.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args()

    formulas_path = Path(args.formulas)
    output_path = Path(args.output)

    if args.input is None:
        if args.dry_run:
            formulas = load_formulas(formulas_path)
            payload = {"mode": "create", "formula_ids": [f.id for f in formulas], "count": len(formulas)}
            if args.json:
                import json
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print(f"Would create {output_path} with {len(formulas)} formula(s).")
            return
        create_document_from_formulas(formulas_path, output_path)
        print(f"Created {output_path}")
        return

    input_path = Path(args.input)
    if args.dry_run:
        needed_ids = collect_docx_placeholder_ids(input_path)
        payload = {"mode": "inject-docx", "input": str(input_path), "formula_ids": needed_ids, "count": len(needed_ids)}
        if args.json:
            import json
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"Would replace {len(needed_ids)} unique formula id(s): {', '.join(needed_ids) if needed_ids else '(none)'}")
        return

    total = inject_docx(input_path, formulas_path, output_path, keep_run_style=not args.no_run_style)
    print(f"Replaced {total} formula placeholder(s). Wrote {output_path}")


if __name__ == "__main__":
    main()
