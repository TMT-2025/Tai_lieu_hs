#!/usr/bin/env python3
"""End-to-end smoke test for the OMML formula skill.

Creates placeholder DOCX/PPTX files, injects editable OMML, then validates the
resulting Office files. This does not prove Microsoft Office rendering, but it
catches broken zip/XML packaging and obvious context errors.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from docx import Document
from pptx import Presentation
from pptx.util import Inches, Pt


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def create_word_placeholder(path: Path) -> None:
    doc = Document()
    doc.add_heading("OMML Formula Skill Smoke Test", level=1)
    doc.add_paragraph("Inline routing weight: {{OMML:routing_weight}} should be editable.")
    doc.add_paragraph("Block formula below:")
    doc.add_paragraph("{{OMML:eq1}}")
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Table formula"
    table.cell(0, 1).text = "{{OMML:bce_loss}}"
    table.cell(1, 0).text = "Evidence"
    table.cell(1, 1).text = "{{OMML:evidence_fusion}}"
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)


def create_ppt_placeholder(path: Path) -> None:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    title = slide.shapes.title
    title.text = "OMML Formula Skill Smoke Test"
    box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8.5), Inches(1.0))
    tf = box.text_frame
    tf.text = "{{OMML:eq1}}"
    p = tf.add_paragraph()
    p.text = "Routing: {{OMML:routing_weight}}"
    p.font.size = Pt(20)
    box2 = slide.shapes.add_textbox(Inches(0.8), Inches(3.0), Inches(8.5), Inches(1.2))
    box2.text_frame.text = "{{OMML:bce_loss}}"
    path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run end-to-end DOCX/PPTX OMML injection smoke tests.")
    parser.add_argument("--work-dir", default="tests/out")
    parser.add_argument("--formulas", default="examples/formulas.json")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    work = (root / args.work_dir).resolve() if not Path(args.work_dir).is_absolute() else Path(args.work_dir)
    formulas = (root / args.formulas).resolve() if not Path(args.formulas).is_absolute() else Path(args.formulas)
    scripts = root / "scripts"

    input_docx = work / "input_placeholders.docx"
    output_docx = work / "output_omml.docx"
    input_pptx = work / "input_placeholders.pptx"
    output_pptx = work / "output_omml.pptx"

    create_word_placeholder(input_docx)
    create_ppt_placeholder(input_pptx)

    run([sys.executable, str(scripts / "insert_word_omml.py"), "--input", str(input_docx), "--formulas", str(formulas), "--output", str(output_docx)])
    run([sys.executable, str(scripts / "inject_ppt_omml.py"), "--input", str(input_pptx), "--formulas", str(formulas), "--output", str(output_pptx)])
    run([sys.executable, str(scripts / "validate_office_math.py"), str(output_docx), "--strict", "--expect-min-omath", "4"])
    run([sys.executable, str(scripts / "validate_office_math.py"), str(output_pptx), "--strict", "--expect-min-omath", "3"])

    print(f"Smoke test passed. Outputs: {output_docx} and {output_pptx}")


if __name__ == "__main__":
    main()
