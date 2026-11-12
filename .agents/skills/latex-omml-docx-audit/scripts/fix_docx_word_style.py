from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = WORD_NS["w"]

ET.register_namespace("w", W)


@dataclass
class FixReport:
    input_file: str
    output_file: str
    updated_styles: list[str]
    created_rpr_styles: list[str]
    summary: str


def qn(tag: str) -> str:
    return f"{{{W}}}{tag}"


def ensure_child(parent: ET.Element, tag: str) -> ET.Element:
    child = parent.find(f"w:{tag}", WORD_NS)
    if child is None:
        child = ET.SubElement(parent, qn(tag))
    return child


def ensure_style_rpr(style: ET.Element) -> tuple[ET.Element, bool]:
    rpr = style.find("w:rPr", WORD_NS)
    created = False
    if rpr is None:
        rpr = ET.SubElement(style, qn("rPr"))
        created = True
    return rpr, created


def apply_body_style(rpr: ET.Element) -> None:
    fonts = ensure_child(rpr, "rFonts")
    fonts.set(qn("ascii"), "Times New Roman")
    fonts.set(qn("hAnsi"), "Times New Roman")
    fonts.set(qn("eastAsia"), "SimSun")
    fonts.set(qn("cs"), "Times New Roman")

    color = ensure_child(rpr, "color")
    color.set(qn("val"), "000000")


def apply_heading_style(rpr: ET.Element) -> None:
    fonts = ensure_child(rpr, "rFonts")
    fonts.set(qn("ascii"), "HeiTi")
    fonts.set(qn("hAnsi"), "HeiTi")
    fonts.set(qn("eastAsia"), "HeiTi")
    fonts.set(qn("cs"), "HeiTi")

    color = ensure_child(rpr, "color")
    color.set(qn("val"), "000000")

    italic = ensure_child(rpr, "i")
    italic.set(qn("val"), "0")

    italic_cs = rpr.find("w:iCs", WORD_NS)
    if italic_cs is not None:
        italic_cs.set(qn("val"), "0")


def update_styles(styles_root: ET.Element) -> tuple[list[str], list[str]]:
    updated_styles: list[str] = []
    created_rpr_styles: list[str] = []

    normal_style = styles_root.find(".//w:style[@w:styleId='Normal']", WORD_NS)
    if normal_style is not None:
        rpr, created = ensure_style_rpr(normal_style)
        apply_body_style(rpr)
        updated_styles.append("Normal")
        if created:
            created_rpr_styles.append("Normal")

    heading_ids = ["Title"] + [f"Heading{i}" for i in range(1, 10)] + [str(i) for i in range(1, 10)]
    seen: set[str] = set()
    for style_id in heading_ids:
        if style_id in seen:
            continue
        seen.add(style_id)
        style = styles_root.find(f".//w:style[@w:styleId='{style_id}']", WORD_NS)
        if style is None:
            continue
        rpr, created = ensure_style_rpr(style)
        apply_heading_style(rpr)
        updated_styles.append(style_id)
        if created:
            created_rpr_styles.append(style_id)

    return updated_styles, created_rpr_styles


def fix_docx_styles(input_docx: Path, output_docx: Path) -> FixReport:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        with zipfile.ZipFile(input_docx) as zf:
            zf.extractall(tmp)

        styles_path = tmp / "word" / "styles.xml"
        if not styles_path.exists():
            raise FileNotFoundError("word/styles.xml not found in DOCX")

        styles_root = ET.parse(styles_path).getroot()
        updated_styles, created_rpr_styles = update_styles(styles_root)
        ET.ElementTree(styles_root).write(styles_path, encoding="utf-8", xml_declaration=True)

        if output_docx.resolve() == input_docx.resolve():
            backup_path = input_docx.with_suffix(input_docx.suffix + ".bak")
            shutil.copy2(input_docx, backup_path)

        with zipfile.ZipFile(output_docx, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in tmp.rglob("*"):
                if path.is_file():
                    zf.write(path, path.relative_to(tmp).as_posix())

    summary = "updated" if updated_styles else "no-target-styles-found"
    return FixReport(
        input_file=str(input_docx),
        output_file=str(output_docx),
        updated_styles=updated_styles,
        created_rpr_styles=created_rpr_styles,
        summary=summary,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix DOCX style defaults for body and heading fonts, colors, and heading italics."
    )
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.input_docx.exists():
        print(f"File not found: {args.input_docx}", file=sys.stderr)
        return 2

    try:
        report = fix_docx_styles(args.input_docx, args.output)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    else:
        print(f"Input: {report.input_file}")
        print(f"Output: {report.output_file}")
        print(f"Summary: {report.summary}")
        print(f"Updated styles: {', '.join(report.updated_styles) if report.updated_styles else 'none'}")
        if report.created_rpr_styles:
            print(f"Created rPr on: {', '.join(report.created_rpr_styles)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
