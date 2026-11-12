#!/usr/bin/env python3
"""Shared utilities for LaTeX → OMML conversion and Office Open XML patching.

This module intentionally avoids python-docx/python-pptx for injection. Those
libraries are useful for authoring files, but editable Office Math requires
patching OOXML in the correct WordprocessingML / DrawingML context.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Tuple

from lxml import etree

NS: Dict[str, str] = {
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}

PLACEHOLDER_PREFIX = "{{OMML:"
PLACEHOLDER_SUFFIX = "}}"
FORMULA_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]+$")


@dataclass(frozen=True)
class Formula:
    """A formula entry loaded from formulas.json."""

    id: str
    latex: str
    display: bool = True
    mode: str = "omml"  # omml | image | auto. Current injectors only render OMML entries.
    alt: str = ""


@dataclass(frozen=True)
class FormulaConfig:
    formulas: List[Formula]
    macros: Dict[str, str]


@dataclass(frozen=True)
class OmmlResult:
    id: str
    latex: str
    display: bool
    o_math: etree._Element
    o_math_para: etree._Element
    pandoc_stderr: str = ""


class FormulaConversionError(RuntimeError):
    pass


def qn(prefix: str, local: str) -> str:
    return f"{{{NS[prefix]}}}{local}"


def clone(element: etree._Element) -> etree._Element:
    return etree.fromstring(etree.tostring(element))


def require_pandoc() -> None:
    if not shutil.which("pandoc"):
        raise RuntimeError(
            "Pandoc was not found on PATH. Install Pandoc and confirm `pandoc --version` works."
        )


def _coerce_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in {"false", "0", "no", "off", "inline"}
    return bool(value)


def load_formula_config(path: str | Path) -> FormulaConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    macros: Dict[str, str] = {}
    if isinstance(data, dict):
        raw_items = data.get("formulas", [])
        raw_macros = data.get("macros", {}) or {}
        if not isinstance(raw_macros, dict):
            raise ValueError("Top-level 'macros' must be an object mapping LaTeX snippets to replacements.")
        macros = {str(k): str(v) for k, v in raw_macros.items()}
    elif isinstance(data, list):
        raw_items = data
    else:
        raise ValueError("Formula JSON must be either a list or an object with a 'formulas' list.")

    formulas: List[Formula] = []
    seen: set[str] = set()
    for item in raw_items:
        if not isinstance(item, dict):
            raise ValueError("Each formula must be an object.")
        formula_id = str(item.get("id", "")).strip()
        latex = str(item.get("latex", "")).strip()
        if not formula_id or not latex:
            raise ValueError(f"Invalid formula entry: {item!r}")
        if not FORMULA_ID_RE.match(formula_id):
            raise ValueError(
                f"Invalid formula id {formula_id!r}. Use letters, digits, underscore, dot, colon or hyphen."
            )
        if formula_id in seen:
            raise ValueError(f"Duplicate formula id: {formula_id}")
        seen.add(formula_id)
        mode = str(item.get("mode", "omml")).strip().lower()
        if mode not in {"omml", "image", "auto"}:
            raise ValueError(f"Formula {formula_id!r} has invalid mode {mode!r}; use omml, image, or auto.")
        formulas.append(
            Formula(
                id=formula_id,
                latex=apply_macros(latex, macros),
                display=_coerce_bool(item.get("display"), default=True),
                mode=mode,
                alt=str(item.get("alt", "")).strip(),
            )
        )
    return FormulaConfig(formulas=formulas, macros=macros)


def load_formulas(path: str | Path, include_image_mode: bool = False) -> List[Formula]:
    formulas = load_formula_config(path).formulas
    if include_image_mode:
        return formulas
    return [f for f in formulas if f.mode in {"omml", "auto"}]


def formulas_by_id(path: str | Path) -> Dict[str, Formula]:
    return {formula.id: formula for formula in load_formulas(path, include_image_mode=True)}


def select_formulas_for_placeholders(path: str | Path, needed_ids: Iterable[str]) -> List[Formula]:
    """Return formula entries referenced by placeholders, with clear user-facing errors.

    This avoids converting every formula in a large manifest and prevents cryptic KeyError
    failures when a placeholder points at an image-only formula.
    """
    needed = list(dict.fromkeys(needed_ids))
    by_id = formulas_by_id(path)
    missing = [formula_id for formula_id in needed if formula_id not in by_id]
    if missing:
        raise KeyError(
            "Placeholder(s) reference formula id(s) not present in formulas JSON: "
            + ", ".join(missing)
        )
    image_only = [formula_id for formula_id in needed if by_id[formula_id].mode == "image"]
    if image_only:
        raise ValueError(
            "Placeholder(s) reference formula id(s) marked mode=image, which cannot be injected as editable OMML: "
            + ", ".join(image_only)
            + ". Render fallback assets or change mode to omml/auto."
        )
    return [by_id[formula_id] for formula_id in needed if by_id[formula_id].mode in {"omml", "auto"}]


def apply_macros(latex: str, macros: Mapping[str, str]) -> str:
    # Intentional simple preprocessor: deterministic literal replacements only.
    for src, dst in macros.items():
        latex = latex.replace(src, dst)
    return latex


def _pandoc_markdown(latex: str, display: bool) -> str:
    if display:
        return f"$$\n{latex}\n$$\n"
    return f"${latex}$\n"


def make_omath_para(o_math: etree._Element) -> etree._Element:
    para = etree.Element(qn("m", "oMathPara"), nsmap={"m": NS["m"]})
    para.append(clone(o_math))
    return para


def convert_latex_to_omml(formula: Formula, pandoc_path: str = "pandoc") -> OmmlResult:
    """Convert a single LaTeX formula to OMML by asking Pandoc to produce DOCX.

    Pandoc emits Office Math in the generated DOCX. We then extract m:oMath and
    m:oMathPara and reuse those nodes in target DOCX/PPTX files.
    """
    require_pandoc()
    with tempfile.TemporaryDirectory(prefix="latex_to_omml_") as tmp:
        tmp_path = Path(tmp)
        md_path = tmp_path / "formula.md"
        docx_path = tmp_path / "formula.docx"
        md_path.write_text(_pandoc_markdown(formula.latex, formula.display), encoding="utf-8")

        proc = subprocess.run(
            [pandoc_path, "--from", "markdown+tex_math_dollars", str(md_path), "-o", str(docx_path)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if proc.returncode != 0:
            raise FormulaConversionError(
                f"Pandoc failed for formula id={formula.id!r} with exit code {proc.returncode}:\n{proc.stderr}"
            )

        try:
            with zipfile.ZipFile(docx_path) as zf:
                document_xml = zf.read("word/document.xml")
        except Exception as exc:  # noqa: BLE001
            raise FormulaConversionError(f"Pandoc did not create a valid DOCX for formula id={formula.id!r}") from exc

    root = etree.fromstring(document_xml)
    o_math_para_nodes = root.xpath(".//m:oMathPara", namespaces=NS)
    o_math_nodes = root.xpath(".//m:oMath", namespaces=NS)

    if not o_math_nodes:
        raise FormulaConversionError(
            f"Pandoc did not produce OMML for formula id={formula.id!r}. "
            "Check that the LaTeX is math-only and does not depend on unsupported packages/macros."
        )

    if o_math_para_nodes:
        o_math_para = clone(o_math_para_nodes[0])
        o_math_inside = o_math_para.xpath(".//m:oMath", namespaces=NS)
        if not o_math_inside:
            raise FormulaConversionError(f"OMML paragraph has no m:oMath for formula id={formula.id!r}")
        o_math = clone(o_math_inside[0])
    else:
        o_math = clone(o_math_nodes[0])
        o_math_para = make_omath_para(o_math)

    return OmmlResult(
        id=formula.id,
        latex=formula.latex,
        display=formula.display,
        o_math=o_math,
        o_math_para=o_math_para,
        pandoc_stderr=proc.stderr,
    )


def convert_all(formulas: Iterable[Formula]) -> Dict[str, OmmlResult]:
    results: Dict[str, OmmlResult] = {}
    for formula in formulas:
        if formula.mode == "image":
            continue
        results[formula.id] = convert_latex_to_omml(formula)
    return results


def placeholder(formula_id: str) -> str:
    return f"{PLACEHOLDER_PREFIX}{formula_id}{PLACEHOLDER_SUFFIX}"


def find_placeholders(text: str) -> List[str]:
    ids: List[str] = []
    start = 0
    while True:
        left = text.find(PLACEHOLDER_PREFIX, start)
        if left < 0:
            break
        right = text.find(PLACEHOLDER_SUFFIX, left + len(PLACEHOLDER_PREFIX))
        if right < 0:
            break
        formula_id = text[left + len(PLACEHOLDER_PREFIX) : right].strip()
        if formula_id:
            ids.append(formula_id)
        start = right + len(PLACEHOLDER_SUFFIX)
    return ids


def split_by_placeholders(text: str) -> List[Tuple[str, str]]:
    """Return [('text', value), ('formula', id), ...]."""
    parts: List[Tuple[str, str]] = []
    cursor = 0
    while True:
        left = text.find(PLACEHOLDER_PREFIX, cursor)
        if left < 0:
            if cursor < len(text):
                parts.append(("text", text[cursor:]))
            break
        if left > cursor:
            parts.append(("text", text[cursor:left]))
        right = text.find(PLACEHOLDER_SUFFIX, left + len(PLACEHOLDER_PREFIX))
        if right < 0:
            parts.append(("text", text[left:]))
            break
        formula_id = text[left + len(PLACEHOLDER_PREFIX) : right].strip()
        parts.append(("formula", formula_id))
        cursor = right + len(PLACEHOLDER_SUFFIX)
    return parts


def parse_xml(data: bytes) -> etree._ElementTree:
    parser = etree.XMLParser(remove_blank_text=False, recover=False, resolve_entities=False)
    return etree.ElementTree(etree.fromstring(data, parser=parser))


def tostring_xml(tree_or_element: etree._ElementTree | etree._Element) -> bytes:
    return etree.tostring(
        tree_or_element,
        xml_declaration=True,
        encoding="UTF-8",
        standalone=False,
    )


def copy_zip_with_replacements(input_path: Path, output_path: Path, replacements: Mapping[str, bytes]) -> None:
    """Copy a zip-based Office file and replace selected internal entries."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(input_path, "r") as zin, zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        replaced = set()
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in replacements:
                data = replacements[item.filename]
                replaced.add(item.filename)
            zout.writestr(item, data)
        missing = set(replacements) - replaced
        if missing:
            raise RuntimeError(f"Internal files not found in archive: {sorted(missing)}")


def iter_zip_xml_parts(path: Path, predicate) -> Iterator[Tuple[str, bytes]]:
    with zipfile.ZipFile(path, "r") as zf:
        for name in zf.namelist():
            if name.endswith(".xml") and predicate(name):
                yield name, zf.read(name)


def local_name(element: etree._Element) -> str:
    return etree.QName(element).localname


def has_ancestor(element: etree._Element, qname: str) -> bool:
    parent = element.getparent()
    while parent is not None:
        if parent.tag == qname:
            return True
        parent = parent.getparent()
    return False


def ensure_root_namespaces(tree: etree._ElementTree, prefixes: Iterable[str]) -> etree._Element:
    """Ensure selected namespace prefixes are declared on the document root.

    Markup-compatibility attributes such as mc:Ignorable="a14" refer to prefixes
    that must be in scope on the element carrying the attribute. A child-level
    xmlns:a14 declaration is not sufficient for the root's mc:Ignorable value.
    """
    root = tree.getroot()
    missing = {prefix: NS[prefix] for prefix in prefixes if root.nsmap.get(prefix) != NS[prefix]}
    if not missing:
        return root

    nsmap = dict(root.nsmap)
    nsmap.update(missing)
    new_root = etree.Element(root.tag, nsmap=nsmap)
    for key, value in root.attrib.items():
        new_root.set(key, value)
    for child in list(root):
        root.remove(child)
        new_root.append(child)
    text, tail = root.text, root.tail
    new_root.text = text
    new_root.tail = tail
    tree._setroot(new_root)
    return new_root


def ensure_mc_ignorable(tree: etree._ElementTree, token: str) -> etree._Element:
    """Add token to mc:Ignorable on the root and ensure prefixes are in scope."""
    root = ensure_root_namespaces(tree, ["mc", token])
    attr = qn("mc", "Ignorable")
    current = root.get(attr, "")
    tokens = current.split()
    if token not in tokens:
        tokens.append(token)
    root.set(attr, " ".join(t for t in tokens if t))
    return root


def main_latex_to_omml() -> None:
    parser = argparse.ArgumentParser(description="Convert a LaTeX formula to OMML and print XML.")
    parser.add_argument("latex", help="LaTeX formula without surrounding $ delimiters")
    parser.add_argument("--id", default="formula")
    parser.add_argument("--inline", action="store_true", help="Return m:oMath instead of m:oMathPara")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print XML")
    args = parser.parse_args()

    formula = Formula(id=args.id, latex=args.latex, display=not args.inline)
    result = convert_latex_to_omml(formula)
    node = result.o_math if args.inline else result.o_math_para
    print(etree.tostring(node, encoding="unicode", pretty_print=args.pretty))


if __name__ == "__main__":
    main_latex_to_omml()
