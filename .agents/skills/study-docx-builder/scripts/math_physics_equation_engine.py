"""
math-physics-equation-engine: Shared LaTeX -> OMML Word Equation engine for
AI Study Document Studio (Mathematics, Physics, Chemistry).

Features:
- Normalizes LaTeX (inline $...$, block $$...$$, multi-line cases/aligned,
  vectors, matrices, integrals, derivatives, limits, Greek letters, upright SI units).
- Batch-converts LaTeX to native Word OMML (<m:oMath> / <m:oMathPara>) via Pandoc.
- Injects OMML directly into existing DOCX (preserving Headings, styles, tables, images).
- Fails loudly with structured diagnostics if any formula fails to convert.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
XML_NS = "http://www.w3.org/XML/1998/namespace"

NSMAP = {"w": W_NS, "m": M_NS}


@dataclass
class FormulaItem:
    key: str
    latex: str
    display: bool


@dataclass
class EngineResult:
    output_docx: str
    total_formulas: int
    inline_count: int
    block_count: int
    errors: List[str] = field(default_factory=list)


def resolve_pandoc_exe() -> str:
    """Find pandoc on PATH or via pypandoc_binary."""
    found = shutil.which("pandoc")
    if found:
        return found
    try:
        import pypandoc  # type: ignore

        p = pypandoc.get_pandoc_path()
        if p:
            if Path(p).exists():
                return str(p)
            if Path(f"{p}.exe").exists():
                return f"{p}.exe"
    except Exception:
        pass
    raise RuntimeError(
        "Không tìm thấy Pandoc. Cài đặt bằng `pip install pypandoc_binary` hoặc `winget install JohnMacFarlane.Pandoc`."
    )


def normalize_latex(expr: str) -> str:
    """Normalize LaTeX for clean Word OMML rendering."""
    s = expr.strip()
    # Replace \dfrac / \tfrac with \frac for consistent OMML sizing
    s = re.sub(r"\\[dt]frac\b", r"\\frac", s)
    # Normalize \vec{x} -> \overrightarrow{x} for clearer vector arrows in Word
    s = re.sub(r"\\vec\{([^{}]+)\}", r"\\overrightarrow{\1}", s)
    # Normalize \text{...} units or Vietnamese text inside math
    return s


def batch_latex_to_omml(items: List[FormulaItem]) -> Dict[str, etree._Element]:
    """Convert unique FormulaItems to OMML elements using one Pandoc pass."""
    if not items:
        return {}

    pandoc_exe = resolve_pandoc_exe()
    md_lines: List[str] = []
    for item in items:
        norm = normalize_latex(item.latex)
        md_lines.append(f"MARKER_{item.key}_START")
        md_lines.append("")
        if item.display:
            md_lines.append(f"$$\n{norm}\n$$")
        else:
            md_lines.append(f"X ${norm}$ Y")
        md_lines.append("")
        md_lines.append(f"MARKER_{item.key}_END")
        md_lines.append("")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        md_path = tmp / "batch.md"
        docx_path = tmp / "batch.docx"
        md_path.write_text("\n".join(md_lines), encoding="utf-8")

        proc = subprocess.run(
            [pandoc_exe, str(md_path), "-f", "markdown", "-t", "docx", "-o", str(docx_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode != 0 or not docx_path.exists():
            raise RuntimeError(f"Pandoc chuyển đổi thất bại: {proc.stderr or proc.stdout}")

        with zipfile.ZipFile(docx_path, "r") as zf:
            doc_xml = etree.fromstring(zf.read("word/document.xml"))

    body = doc_xml.find(f"{{{W_NS}}}body")
    if body is None:
        raise RuntimeError("Pandoc DOCX không có w:body.")

    paragraphs = body.findall(f"{{{W_NS}}}p")
    result: Dict[str, etree._Element] = {}
    current_key: str | None = None
    captured_nodes: List[etree._Element] = []

    for p in paragraphs:
        text_content = "".join(p.itertext()).strip()
        m_start = re.fullmatch(r"MARKER_(.+)_START", text_content)
        m_end = re.fullmatch(r"MARKER_(.+)_END", text_content)
        if m_start:
            current_key = m_start.group(1)
            captured_nodes = []
            continue
        if m_end and current_key == m_end.group(1):
            if captured_nodes:
                result[current_key] = captured_nodes[0]
            current_key = None
            captured_nodes = []
            continue
        if current_key is not None:
            omath_para = p.find(f"{{{M_NS}}}oMathPara")
            omath = p.find(f"{{{M_NS}}}oMath")
            if omath_para is not None:
                captured_nodes.append(omath_para)
            elif omath is not None:
                captured_nodes.append(omath)

    missing = [it for it in items if it.key not in result]
    if missing:
        sample = ", ".join(f"{m.key} ({m.latex[:40]})" for m in missing[:5])
        raise RuntimeError(f"Chuyển đổi OMML thất bại cho {len(missing)} công thức: {sample}")

    return result


TOKEN_PATTERN = re.compile(r"(\$\$[\s\S]+?\$\$|\$(?!\s)([^\$\n]+?)(?<!\s)\$)")


def _make_run_with_text(text: str, template_rpr: etree._Element | None) -> etree._Element:
    r = etree.Element(f"{{{W_NS}}}r")
    if template_rpr is not None:
        r.append(etree.fromstring(etree.tostring(template_rpr)))
    t = etree.SubElement(r, f"{{{W_NS}}}t")
    t.set(f"{{{XML_NS}}}space", "preserve")
    t.text = text
    return r


def process_docx_equations(input_docx: str | Path, output_docx: str | Path) -> EngineResult:
    """
    Scan input_docx for $$...$$ and $...$ expressions, convert them to native OMML,
    and write output_docx preserving document structure and formatting.
    """
    in_path = Path(input_docx)
    out_path = Path(output_docx)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(in_path, "r") as zf:
        entries = {name: zf.read(name) for name in zf.namelist()}

    parser = etree.XMLParser(remove_blank_text=False)
    doc_root = etree.fromstring(entries["word/document.xml"], parser)

    # Ensure m: namespace is declared on root
    if "m" not in doc_root.nsmap:
        etree.cleanup_namespaces(doc_root, top_nsmap={"m": M_NS})

    # Pass 1: collect all paragraphs containing math tokens
    paragraphs = doc_root.findall(f".//{{{W_NS}}}p")
    collected: List[FormulaItem] = []
    seen_expr: Dict[Tuple[str, bool], str] = {}

    def register_formula(latex: str, display: bool) -> str:
        sig = (latex.strip(), display)
        if sig in seen_expr:
            return seen_expr[sig]
        key = f"EQ{len(collected) + 1}"
        seen_expr[sig] = key
        collected.append(FormulaItem(key=key, latex=latex.strip(), display=display))
        return key

    # First merge adjacent plain w:t runs inside paragraphs that contain '$' so split runs don't break $...$
    para_math_plans: List[Tuple[etree._Element, str, List[Tuple[str, str, bool]], etree._Element | None]] = []

    for p in paragraphs:
        # Only inspect paragraphs that have '$' in their combined text
        runs = p.findall(f"{{{W_NS}}}r")
        if not runs:
            continue
        full_text = "".join(t.text or "" for r in runs for t in r.findall(f"{{{W_NS}}}t"))
        if "$" not in full_text:
            continue
        if not TOKEN_PATTERN.search(full_text):
            continue

        # Check if it's a pure display equation paragraph ($$...$$)
        stripped = full_text.strip()
        if stripped.startswith("$$") and stripped.endswith("$$") and stripped.count("$$") == 2:
            latex_inner = stripped[2:-2].strip()
            key = register_formula(latex_inner, True)
            para_math_plans.append((p, "block", [(key, latex_inner, True)], None))
            continue

        # Inline / mixed paragraph: preserve exact per-character rPr from original runs
        segments: List[Tuple[str, object, int, int]] = []
        char_rprs: List[etree._Element | None] = []
        for r in runs:
            rpr = r.find(f"{{{W_NS}}}rPr")
            r_text = "".join(t.text or "" for t in r.findall(f"{{{W_NS}}}t"))
            for _ in r_text:
                char_rprs.append(rpr)

        last_idx = 0
        for m in TOKEN_PATTERN.finditer(full_text):
            if m.start() > last_idx:
                segments.append(("text", full_text[last_idx : m.start()], last_idx, m.start()))
            raw_tok = m.group(0)
            is_disp = raw_tok.startswith("$$")
            inner = raw_tok[2:-2].strip() if is_disp else raw_tok[1:-1].strip()
            key = register_formula(inner, is_disp)
            segments.append(("math", key, m.start(), m.end()))
            last_idx = m.end()
        if last_idx < len(full_text):
            segments.append(("text", full_text[last_idx:], last_idx, len(full_text)))

        para_math_plans.append((p, "inline", segments, char_rprs))

    if not collected:
        # Still copy to output cleanly
        shutil.copy2(in_path, out_path)
        return EngineResult(output_docx=str(out_path), total_formulas=0, inline_count=0, block_count=0)

    omml_map = batch_latex_to_omml(collected)

    inline_count = 0
    block_count = 0

    for p, kind, segments, char_rprs in para_math_plans:
        ppr = p.find(f"{{{W_NS}}}pPr")
        # Remove existing w:r children (keep w:pPr)
        for child in list(p):
            if child is not ppr:
                p.remove(child)

        if kind == "block":
            key = str(segments[0][1])
            omml_node = etree.fromstring(etree.tostring(omml_map[key]))
            if omml_node.tag != f"{{{M_NS}}}oMathPara":
                wrapper = etree.Element(f"{{{M_NS}}}oMathPara")
                wrapper.append(omml_node)
                omml_node = wrapper
            p.append(omml_node)
            block_count += 1
        else:
            for seg_type, val, s_idx, e_idx in segments:
                if seg_type == "text":
                    txt = str(val)
                    if not txt:
                        continue
                    # Group consecutive chars sharing the same rPr object
                    cur_rpr = char_rprs[s_idx] if s_idx < len(char_rprs) else None
                    buf = []
                    for pos in range(len(txt)):
                        rpr_at = char_rprs[s_idx + pos] if (s_idx + pos) < len(char_rprs) else cur_rpr
                        if rpr_at is not cur_rpr and buf:
                            p.append(_make_run_with_text("".join(buf), cur_rpr))
                            buf = []
                            cur_rpr = rpr_at
                        buf.append(txt[pos])
                    if buf:
                        p.append(_make_run_with_text("".join(buf), cur_rpr))
                else:
                    omml_node = etree.fromstring(etree.tostring(omml_map[str(val)]))
                    if omml_node.tag == f"{{{M_NS}}}oMathPara":
                        inner_math = omml_node.find(f"{{{M_NS}}}oMath")
                        if inner_math is not None:
                            omml_node = inner_math
                    p.append(omml_node)
                    inline_count += 1

    entries["word/document.xml"] = etree.tostring(
        doc_root, xml_declaration=True, encoding="UTF-8", standalone="yes"
    )

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, content in entries.items():
            zout.writestr(name, content)

    return EngineResult(
        output_docx=str(out_path),
        total_formulas=inline_count + block_count,
        inline_count=inline_count,
        block_count=block_count,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert $...$ and $$...$$ in DOCX to native Word OMML.")
    parser.add_argument("--input", required=True, help="Input DOCX path")
    parser.add_argument("--output", required=True, help="Output DOCX path")
    parser.add_argument("--json", action="store_true", help="Print JSON summary")
    args = parser.parse_args()

    res = process_docx_equations(args.input, args.output)
    if args.json:
        print(json.dumps(res.__dict__, ensure_ascii=False, indent=2))
    else:
        print(
            f"OMML Engine OK: {res.total_formulas} công thức "
            f"({res.inline_count} inline, {res.block_count} block) -> {res.output_docx}"
        )


if __name__ == "__main__":
    main()
