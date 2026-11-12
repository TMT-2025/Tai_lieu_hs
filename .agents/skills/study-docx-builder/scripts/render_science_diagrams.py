"""
Render publication-quality 300 DPI science diagrams for Physics, Biology,
and Natural Sciences (KHTN 6-9) using Matplotlib.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Sequence

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


def render_classification_diagram(
    title: str,
    branches: Sequence[tuple[str, Sequence[str]]],
    out_path: str | Path,
) -> Path:
    """Render a clean hierarchical classification diagram (300 DPI)."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    n = max(1, len(branches))
    fig_w = max(8.5, n * 2.5)
    fig, ax = plt.subplots(figsize=(fig_w, 4.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    def draw_box(x, y, w, h, text, fc, ec, tc="#111827", fs=9.0, bold=False):
        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.1,rounding_size=0.14",
            facecolor=fc,
            edgecolor=ec,
            linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(
            x + w / 2,
            y + h / 2,
            text,
            ha="center",
            va="center",
            fontsize=fs,
            color=tc,
            fontweight="bold" if bold else "normal",
            family="DejaVu Sans",
        )

    draw_box(2.2, 4.15, 5.6, 0.72, title, "#1e3a8a", "#1e3a8a", tc="white", fs=10, bold=True)

    palette = [
        ("#eff6ff", "#2563eb"),
        ("#ecfdf5", "#059669"),
        ("#fffbeb", "#d97706"),
        ("#fdf2f8", "#db2777"),
    ]
    margin = 0.25
    gap = 0.25
    total_w = 10 - 2 * margin - (n - 1) * gap
    box_w = total_w / n

    for i, (b_title, items) in enumerate(branches):
        fc, ec = palette[i % len(palette)]
        x = margin + i * (box_w + gap)
        draw_box(x, 2.6, box_w, 0.85, b_title, fc, ec, fs=8.8, bold=True)
        ax.annotate(
            "",
            xy=(x + box_w / 2, 3.56),
            xytext=(5.0, 4.08),
            arrowprops=dict(arrowstyle="->", color="#475569", lw=1.3),
        )
        body = "\n".join(f"• {it}" for it in items)
        draw_box(x, 0.45, box_w, 1.75, body, "#ffffff", ec, fs=8.0, bold=False)
        ax.annotate(
            "",
            xy=(x + box_w / 2, 2.3),
            xytext=(x + box_w / 2, 2.52),
            arrowprops=dict(arrowstyle="->", color=ec, lw=1.3),
        )

    plt.tight_layout(pad=0.2)
    plt.savefig(out, dpi=300)
    plt.close(fig)
    return out


def render_biology_cycle(
    title: str,
    steps: Sequence[str],
    out_path: str | Path,
) -> Path:
    """Render a circular biological process/cycle diagram (300 DPI)."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=300)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-2.6, 2.8)
    ax.axis("off")

    ax.text(0, 2.45, title, ha="center", va="center", fontsize=11, fontweight="bold", color="#1e3a8a", family="DejaVu Sans")

    n = len(steps)
    rx, ry = 2.0, 1.45
    coords = []
    for i in range(n):
        angle = math.pi / 2 - 2 * math.pi * i / n
        coords.append((rx * math.cos(angle), ry * math.sin(angle)))

    for i, (x, y) in enumerate(coords):
        rect = patches.FancyBboxPatch(
            (x - 0.82, y - 0.34),
            1.64,
            0.68,
            boxstyle="round,pad=0.08,rounding_size=0.14",
            facecolor="#ecfdf5",
            edgecolor="#059669",
            linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(x, y, steps[i], ha="center", va="center", fontsize=8.5, fontweight="bold", color="#064e3b", family="DejaVu Sans")

        nx, ny = coords[(i + 1) % n]
        dx, dy = nx - x, ny - y
        dist = math.hypot(dx, dy) or 1.0
        sx, sy = x + 0.55 * dx / dist, y + 0.42 * dy / dist
        ex, ey = nx - 0.55 * dx / dist, ny - 0.42 * dy / dist
        ax.annotate(
            "",
            xy=(ex, ey),
            xytext=(sx, sy),
            arrowprops=dict(arrowstyle="->", color="#059669", lw=1.6, connectionstyle="arc3,rad=-0.18"),
        )

    plt.tight_layout(pad=0.2)
    plt.savefig(out, dpi=300)
    plt.close(fig)
    return out


def render_physics_harmonic_graph(
    title: str,
    amplitude: float,
    period: float,
    out_path: str | Path,
    ylabel: str = "Li độ x (cm)",
) -> Path:
    """Render a harmonic oscillation graph x(t) = A cos(2*pi*t/T) at 300 DPI."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    t = np.linspace(0, 2 * period, 500)
    x = amplitude * np.cos(2 * math.pi * t / period)

    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=300)
    ax.plot(t, x, color="#1d4ed8", linewidth=2.2, label=f"A = {amplitude}, T = {period} s")
    ax.axhline(0, color="#475569", linewidth=0.9)
    ax.axhline(amplitude, color="#94a3b8", linestyle="--", linewidth=0.8)
    ax.axhline(-amplitude, color="#94a3b8", linestyle="--", linewidth=0.8)
    ax.set_title(title, fontsize=10.5, fontweight="bold", color="#0f172a", family="DejaVu Sans")
    ax.set_xlabel("Thời gian t (s)", fontsize=9.5, family="DejaVu Sans")
    ax.set_ylabel(ylabel, fontsize=9.5, family="DejaVu Sans")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", fontsize=8.5)

    plt.tight_layout(pad=0.3)
    plt.savefig(out, dpi=300)
    plt.close(fig)
    return out


if __name__ == "__main__":
    print("render_science_diagrams.py ready (classification, biology_cycle, physics_harmonic_graph).")
