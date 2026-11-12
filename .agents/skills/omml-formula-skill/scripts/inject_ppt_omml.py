#!/usr/bin/env python3
"""Replace {{OMML:id}} placeholders in PPTX text paragraphs with editable Office Math.

PowerPoint is context-sensitive: m:oMath is wrapped in a14:m and injected into
DrawingML paragraphs after the slide deck has already been generated.
"""
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path
from typing import Dict, Iterable, Mapping, Pattern

from lxml import etree

from omml_utils import (
    NS,
    clone,
    convert_all,
    copy_zip_with_replacements,
    ensure_mc_ignorable,
    find_placeholders,
    load_formulas,
    select_formulas_for_placeholders,
    parse_xml,
    qn,
    split_by_placeholders,
    tostring_xml,
)

SCOPE_PATTERNS: dict[str, Pattern[str]] = {
    "slides": re.compile(r"^ppt/slides/slide\d+\.xml$"),
    "notes": re.compile(r"^ppt/notesSlides/notesSlide\d+\.xml$"),
    "masters": re.compile(r"^ppt/slideMasters/slideMaster\d+\.xml$"),
    "layouts": re.compile(r"^ppt/slideLayouts/slideLayout\d+\.xml$"),
}


def part_in_scope(name: str, scopes: Iterable[str]) -> bool:
    return any(SCOPE_PATTERNS[scope].match(name) for scope in scopes)


def paragraph_text(paragraph: etree._Element) -> str:
    # Handles placeholders split across multiple a:r/a:t runs.
    return "".join(t.text or "" for t in paragraph.xpath(".//a:t", namespaces=NS))


def first_run_rpr(paragraph: etree._Element) -> etree._Element | None:
    rpr = paragraph.find(".//a:rPr", namespaces=NS)
    return clone(rpr) if rpr is not None else None


def make_a_run(text: str, base_rpr: etree._Element | None = None) -> etree._Element:
    run = etree.Element(qn("a", "r"))
    if base_rpr is not None:
        run.append(clone(base_rpr))
    else:
        rpr = etree.SubElement(run, qn("a", "rPr"))
        rpr.set("lang", "en-US")
    t = etree.SubElement(run, qn("a", "t"))
    t.text = text
    return run


def make_a14_math(omath_para: etree._Element) -> etree._Element:
    # a14:m is the DrawingML Office 2010 math wrapper used by PowerPoint.
    wrapper = etree.Element(qn("a14", "m"), nsmap={"a14": NS["a14"], "m": NS["m"]})
    wrapper.append(clone(omath_para))
    return wrapper


def default_end_para_rpr() -> etree._Element:
    end = etree.Element(qn("a", "endParaRPr"))
    end.set("lang", "en-US")
    return end


def rebuild_ppt_paragraph(
    paragraph: etree._Element,
    omml_by_id: Mapping[str, object],
    *,
    keep_run_style: bool,
) -> int:
    text = paragraph_text(paragraph)
    ids = find_placeholders(text)
    if not ids:
        return 0

    for formula_id in ids:
        if formula_id not in omml_by_id:
            raise KeyError(f"Placeholder references missing formula id: {formula_id}")

    ppr = paragraph.find(qn("a", "pPr"))
    end = paragraph.find(qn("a", "endParaRPr"))
    saved_ppr = clone(ppr) if ppr is not None else None
    saved_end = clone(end) if end is not None else default_end_para_rpr()
    base_rpr = first_run_rpr(paragraph) if keep_run_style else None

    for child in list(paragraph):
        paragraph.remove(child)
    if saved_ppr is not None:
        paragraph.append(saved_ppr)

    for kind, value in split_by_placeholders(text):
        if kind == "text" and value:
            paragraph.append(make_a_run(value, base_rpr))
        elif kind == "formula":
            paragraph.append(make_a14_math(omml_by_id[value].o_math_para))

    paragraph.append(saved_end)
    return len(ids)


def collect_pptx_placeholder_ids(input_path: Path, *, scopes: Iterable[str] = ("slides",)) -> list[str]:
    ids: list[str] = []
    scopes = tuple(scopes)
    with zipfile.ZipFile(input_path, "r") as zin:
        for name in zin.namelist():
            if not part_in_scope(name, scopes):
                continue
            tree = parse_xml(zin.read(name))
            root = tree.getroot()
            for paragraph in root.xpath(".//a:p", namespaces=NS):
                ids.extend(find_placeholders(paragraph_text(paragraph)))
    return list(dict.fromkeys(ids))


def inject_pptx(
    input_path: Path,
    formulas_path: Path,
    output_path: Path,
    *,
    scopes: Iterable[str] = ("slides",),
    keep_run_style: bool = True,
) -> int:
    scopes = tuple(scopes)
    invalid = [scope for scope in scopes if scope not in SCOPE_PATTERNS]
    if invalid:
        raise ValueError(f"Invalid scope(s): {invalid}. Choose from {sorted(SCOPE_PATTERNS)}")

    needed_ids = collect_pptx_placeholder_ids(input_path, scopes=scopes)
    omml_by_id = convert_all(select_formulas_for_placeholders(formulas_path, needed_ids))
    replacements: Dict[str, bytes] = {}
    total = 0

    with zipfile.ZipFile(input_path, "r") as zin:
        for name in zin.namelist():
            if not part_in_scope(name, scopes):
                continue
            tree = parse_xml(zin.read(name))
            root = tree.getroot()
            count = 0
            for paragraph in root.xpath(".//a:p", namespaces=NS):
                count += rebuild_ppt_paragraph(paragraph, omml_by_id, keep_run_style=keep_run_style)
            if count:
                ensure_mc_ignorable(tree, "a14")
                replacements[name] = tostring_xml(tree)
                total += count

    copy_zip_with_replacements(input_path, output_path, replacements)
    return total


def parse_scopes(value: str) -> tuple[str, ...]:
    if value.strip().lower() == "all":
        return tuple(SCOPE_PATTERNS)
    scopes = tuple(s.strip().lower() for s in value.split(",") if s.strip())
    return scopes or ("slides",)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inject editable OMML formulas into PPTX placeholders.")
    parser.add_argument("--input", required=True, help="Input PPTX containing {{OMML:id}} placeholders.")
    parser.add_argument("--formulas", required=True, help="Formula JSON file.")
    parser.add_argument("--output", required=True, help="Output PPTX.")
    parser.add_argument(
        "--scope",
        default="slides",
        help="Comma-separated: slides,notes,masters,layouts or all. Default: slides.",
    )
    parser.add_argument("--no-run-style", action="store_true", help="Do not copy the first run style to rebuilt text runs.")
    parser.add_argument("--dry-run", action="store_true", help="Only report placeholder ids that would be processed.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args()

    input_path = Path(args.input)
    scopes = parse_scopes(args.scope)
    if args.dry_run:
        needed_ids = collect_pptx_placeholder_ids(input_path, scopes=scopes)
        payload = {"mode": "inject-pptx", "input": str(input_path), "scope": scopes, "formula_ids": needed_ids, "count": len(needed_ids)}
        if args.json:
            import json
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"Would replace {len(needed_ids)} unique formula id(s): {', '.join(needed_ids) if needed_ids else '(none)'}")
        return

    total = inject_pptx(
        input_path,
        Path(args.formulas),
        Path(args.output),
        scopes=scopes,
        keep_run_style=not args.no_run_style,
    )
    print(f"Replaced {total} formula placeholder(s). Wrote {args.output}")


if __name__ == "__main__":
    main()
