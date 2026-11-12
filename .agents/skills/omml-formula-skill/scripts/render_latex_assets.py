#!/usr/bin/env python3
"""Optional fallback: render LaTeX formulas to transparent PNG assets.

This is presentation-only fallback. PNG formulas are visible but not editable as
Office Math. The script uses Matplotlib mathtext by default, so it has broader
availability than a full TeX toolchain but supports a smaller LaTeX subset.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from omml_utils import load_formulas


def render_png(formula_latex: str, output: Path, *, dpi: int = 300, fontsize: int = 28) -> None:
    import matplotlib.pyplot as plt  # imported lazily; optional dependency

    output.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0)
    text = fig.text(0, 0, f"${formula_latex}$", fontsize=fontsize)
    fig.canvas.draw()
    bbox = text.get_window_extent()
    width, height = bbox.width / dpi, bbox.height / dpi
    plt.close(fig)

    fig = plt.figure(figsize=(max(width, 0.1), max(height, 0.1)))
    fig.patch.set_alpha(0)
    fig.text(0, 0, f"${formula_latex}$", fontsize=fontsize)
    plt.axis("off")
    fig.savefig(output, dpi=dpi, transparent=True, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render formula PNG fallback assets.")
    parser.add_argument("--formulas", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--fontsize", type=int, default=28)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    manifest = []
    for formula in load_formulas(args.formulas, include_image_mode=True):
        output = out_dir / f"{formula.id}.png"
        render_png(formula.latex, output, dpi=args.dpi, fontsize=args.fontsize)
        manifest.append({"id": formula.id, "latex": formula.latex, "path": str(output), "editable": False})
    (out_dir / "manifest.json").write_text(json.dumps({"assets": manifest}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rendered {len(manifest)} PNG asset(s) to {out_dir}")


if __name__ == "__main__":
    main()
