from __future__ import annotations

import argparse
import json
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET

WORD_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

SIMSUN_ALIASES = {"SimSun", "宋体"}
HEITI_ALIASES = {"HeiTi", "黑体", "SimHei"}
TIMES_NEW_ROMAN_ALIASES = {"Times New Roman"}
BLACK_ALIASES = {"000000", "auto"}


@dataclass
class RuleCheck:
    status: str
    expected: str
    actual: str
    note: str


@dataclass
class StyleAuditReport:
    file: str
    normal_chinese_font: RuleCheck
    normal_english_font: RuleCheck
    heading_font: RuleCheck
    body_color: RuleCheck
    heading_color: RuleCheck
    heading_italic: RuleCheck
    summary: str


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def read_xml_from_docx(docx_path: Path, member: str) -> Optional[ET.Element]:
    with zipfile.ZipFile(docx_path) as zf:
        try:
            data = zf.read(member)
        except KeyError:
            return None
    return ET.fromstring(data)


def find_style(root: ET.Element, style_ids: list[str]) -> Optional[ET.Element]:
    for style_id in style_ids:
        style = root.find(f".//w:style[@w:styleId='{style_id}']", WORD_NS)
        if style is not None:
            return style
    return None


def child_rpr(style: Optional[ET.Element]) -> Optional[ET.Element]:
    if style is None:
        return None
    return style.find("w:rPr", WORD_NS)


def extract_fonts(rpr: Optional[ET.Element]) -> dict[str, str]:
    if rpr is None:
        return {}
    fonts = rpr.find("w:rFonts", WORD_NS)
    if fonts is None:
        return {}
    result: dict[str, str] = {}
    for key, value in fonts.attrib.items():
        result[local_name(key)] = value
    return result


def extract_color(rpr: Optional[ET.Element]) -> Optional[str]:
    if rpr is None:
        return None
    color = rpr.find("w:color", WORD_NS)
    if color is None:
        return None
    return color.attrib.get(f"{{{WORD_NS['w']}}}val") or color.attrib.get("val")


def extract_italic(rpr: Optional[ET.Element]) -> Optional[bool]:
    if rpr is None:
        return None
    italic = rpr.find("w:i", WORD_NS)
    if italic is None:
        return False
    val = italic.attrib.get(f"{{{WORD_NS['w']}}}val") or italic.attrib.get("val")
    if val is None:
        return True
    return val.lower() not in {"0", "false", "off"}


def make_check(
    ok: bool,
    expected: str,
    actual: str,
    note: str = "",
) -> RuleCheck:
    return RuleCheck(
        status="pass" if ok else "fail",
        expected=expected,
        actual=actual,
        note=note,
    )


def audit_docx_styles(docx_path: Path) -> StyleAuditReport:
    styles_root = read_xml_from_docx(docx_path, "word/styles.xml")
    if styles_root is None:
        missing = make_check(False, "styles.xml present", "missing", "The DOCX has no word/styles.xml entry.")
        return StyleAuditReport(
            file=str(docx_path),
            normal_chinese_font=missing,
            normal_english_font=missing,
            heading_font=missing,
            body_color=missing,
            heading_color=missing,
            heading_italic=missing,
            summary="missing-styles",
        )

    normal_style = find_style(styles_root, ["Normal"])
    heading_style = find_style(styles_root, ["Heading1", "1", "Title"])

    normal_fonts = extract_fonts(child_rpr(normal_style))
    heading_fonts = extract_fonts(child_rpr(heading_style))

    normal_east_asia = normal_fonts.get("eastAsia", "")
    normal_ascii = normal_fonts.get("ascii", "") or normal_fonts.get("hAnsi", "")
    heading_east_asia = heading_fonts.get("eastAsia", "")
    heading_ascii = heading_fonts.get("ascii", "") or heading_fonts.get("hAnsi", "")

    normal_color = (extract_color(child_rpr(normal_style)) or "").lower()
    heading_color = (extract_color(child_rpr(heading_style)) or "").lower()
    heading_italic = extract_italic(child_rpr(heading_style))

    normal_cn_check = make_check(
        normal_east_asia in SIMSUN_ALIASES,
        "SimSun / 宋体",
        normal_east_asia or "missing",
        "Checked Normal style eastAsia font.",
    )
    normal_en_check = make_check(
        normal_ascii in TIMES_NEW_ROMAN_ALIASES,
        "Times New Roman",
        normal_ascii or "missing",
        "Checked Normal style ascii/hAnsi font.",
    )

    heading_actual = ", ".join(x for x in [heading_east_asia, heading_ascii] if x) or "missing"
    heading_ok = heading_east_asia in HEITI_ALIASES or heading_ascii in HEITI_ALIASES
    heading_font_check = make_check(
        heading_ok,
        "HeiTi / 黑体",
        heading_actual,
        "Checked Heading1, fallback 1 or Title style font.",
    )

    body_color_check = make_check(
        normal_color in BLACK_ALIASES,
        "black (000000 or auto)",
        normal_color or "missing",
        "Checked Normal style color.",
    )
    heading_color_check = make_check(
        heading_color in BLACK_ALIASES,
        "black (000000 or auto)",
        heading_color or "missing",
        "Checked heading style color.",
    )
    heading_italic_check = make_check(
        heading_italic is False,
        "not italic",
        "italic" if heading_italic else "not italic",
        "Checked heading style italic setting.",
    )

    checks = [
        normal_cn_check,
        normal_en_check,
        heading_font_check,
        body_color_check,
        heading_color_check,
        heading_italic_check,
    ]
    summary = "pass" if all(check.status == "pass" for check in checks) else "needs-fix"

    return StyleAuditReport(
        file=str(docx_path),
        normal_chinese_font=normal_cn_check,
        normal_english_font=normal_en_check,
        heading_font=heading_font_check,
        body_color=body_color_check,
        heading_color=heading_color_check,
        heading_italic=heading_italic_check,
        summary=summary,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit whether a DOCX follows the expected Word font and color rules."
    )
    parser.add_argument("docx", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.docx.exists():
        print(f"File not found: {args.docx}", file=sys.stderr)
        return 2

    report = audit_docx_styles(args.docx)
    if args.json:
        print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
    else:
        print(f"DOCX: {report.file}")
        print(f"Summary: {report.summary}")
        for label, check in [
            ("Normal Chinese font", report.normal_chinese_font),
            ("Normal English font", report.normal_english_font),
            ("Heading font", report.heading_font),
            ("Body color", report.body_color),
            ("Heading color", report.heading_color),
            ("Heading italic", report.heading_italic),
        ]:
            print(f"{label}: {check.status}")
            print(f"  expected: {check.expected}")
            print(f"  actual: {check.actual}")
            if check.note:
                print(f"  note: {check.note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
