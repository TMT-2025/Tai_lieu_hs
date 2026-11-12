#!/usr/bin/env python3
"""Extract OMML snippets from DOCX/PPTX for debugging and regression review."""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from typing import Any, Dict, List

from lxml import etree

from omml_utils import NS

PPT_RE = re.compile(r"^ppt/(slides/slide\d+|notesSlides/notesSlide\d+|slideMasters/slideMaster\d+|slideLayouts/slideLayout\d+)\.xml$")
WORD_RE = re.compile(r"^word/(document|footnotes|endnotes|comments|glossary/document)\.xml$|^word/(header|footer)\d+\.xml$")


def include(path: Path, name: str) -> bool:
    if path.suffix.lower() == ".pptx":
        return bool(PPT_RE.match(name))
    if path.suffix.lower() == ".docx":
        return bool(WORD_RE.match(name))
    return False


def extract(path: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if not include(path, name):
                continue
            root = etree.fromstring(zf.read(name))
            for idx, node in enumerate(root.xpath(".//m:oMathPara | .//m:oMath", namespaces=NS), start=1):
                items.append(
                    {
                        "file": name,
                        "index": idx,
                        "tag": etree.QName(node).localname,
                        "text": "".join(node.itertext()),
                        "xml": etree.tostring(node, encoding="unicode", pretty_print=True),
                    }
                )
    return items


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract OMML snippets from a DOCX/PPTX.")
    parser.add_argument("file")
    parser.add_argument("--out", help="Write JSON to this path. If omitted, print to stdout.")
    args = parser.parse_args()
    items = extract(Path(args.file))
    payload = json.dumps({"file": args.file, "count": len(items), "items": items}, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
        print(f"Extracted {len(items)} math node(s) to {args.out}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
