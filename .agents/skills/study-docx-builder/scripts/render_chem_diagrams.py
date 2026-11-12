import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams["font.family"] = "DejaVu Sans"


def render_exo_endo_exchange(out_path: str):
    """Sơ đồ trao đổi nhiệt giữa hệ phản ứng và môi trường (Tỏa nhiệt vs Thu nhiệt)."""
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6), dpi=300)
    fig.patch.set_facecolor("white")

    # Left: Exothermic
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_title("Phản ứng tỏa nhiệt (ΔrH°298 < 0)", fontsize=11, fontweight="bold", color="#B22222", pad=8)

    box = patches.FancyBboxPatch((3.0, 2.7), 4.0, 2.4, boxstyle="round,pad=0.2", fc="#FDE8E8", ec="#C53030", lw=2)
    ax.add_patch(box)
    ax.text(5.0, 3.9, "Hệ phản ứng\n(Giải phóng nhiệt)", ha="center", va="center", fontsize=10, fontweight="bold", color="#7B1D1D")

    arrows = [((5.0, 5.3), (5.0, 6.8)), ((5.0, 2.5), (5.0, 1.0)), ((2.8, 3.9), (1.0, 3.9)), ((7.2, 3.9), (9.0, 3.9))]
    for s, e in arrows:
        ax.annotate("", xy=e, xytext=s, arrowprops=dict(arrowstyle="->", lw=2, color="#C53030"))
    ax.text(5.0, 7.2, "Môi trường (nóng lên)", ha="center", fontsize=9.5, color="#333333")
    ax.text(5.0, 0.4, "Môi trường nhận nhiệt", ha="center", fontsize=9.5, color="#333333")

    # Right: Endothermic
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_title("Phản ứng thu nhiệt (ΔrH°298 > 0)", fontsize=11, fontweight="bold", color="#1A4E8A", pad=8)

    box2 = patches.FancyBboxPatch((3.0, 2.7), 4.0, 2.4, boxstyle="round,pad=0.2", fc="#E8F2FC", ec="#2B6CB0", lw=2)
    ax.add_patch(box2)
    ax.text(5.0, 3.9, "Hệ phản ứng\n(Hấp thụ nhiệt)", ha="center", va="center", fontsize=10, fontweight="bold", color="#1A365D")

    arrows2 = [((5.0, 6.8), (5.0, 5.3)), ((5.0, 1.0), (5.0, 2.5)), ((1.0, 3.9), (2.8, 3.9)), ((9.0, 3.9), (7.2, 3.9))]
    for s, e in arrows2:
        ax.annotate("", xy=e, xytext=s, arrowprops=dict(arrowstyle="->", lw=2, color="#2B6CB0"))
    ax.text(5.0, 7.2, "Môi trường (lạnh đi)", ha="center", fontsize=9.5, color="#333333")
    ax.text(5.0, 0.4, "Môi trường cung cấp nhiệt", ha="center", fontsize=9.5, color="#333333")

    plt.tight_layout()
    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def render_enthalpy_diagram(out_path: str):
    """Giản đồ biến thiên enthalpy chuẩn (ΔrH°298) cho phản ứng tỏa nhiệt và thu nhiệt."""
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.0), dpi=300)
    fig.patch.set_facecolor("white")

    # Left: Exothermic
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("Tiến trình phản ứng", fontsize=9.5)
    ax.set_ylabel("Enthalpy (H)", fontsize=9.5)
    ax.set_title("a) Phản ứng tỏa nhiệt (ΔrH°298 < 0)", fontsize=10.5, fontweight="bold", color="#B22222", pad=8)

    ax.plot([1.2, 4.0], [7.2, 7.2], color="#1A365D", lw=2.5)
    ax.plot([6.0, 8.8], [3.0, 3.0], color="#1A365D", lw=2.5)
    ax.plot([4.0, 6.0], [7.2, 3.0], color="#718096", lw=1.5, ls="--")
    ax.annotate("", xy=(5.0, 3.0), xytext=(5.0, 7.2), arrowprops=dict(arrowstyle="->", lw=2.2, color="#C53030"))
    ax.text(2.6, 7.6, "Chất đầu (cđ)", ha="center", fontsize=9.5, fontweight="bold")
    ax.text(7.4, 3.4, "Sản phẩm (sp)", ha="center", fontsize=9.5, fontweight="bold")
    ax.text(5.3, 5.1, "ΔrH°298 < 0\n(Tỏa nhiệt)", ha="left", va="center", fontsize=9, fontweight="bold", color="#C53030")

    # Right: Endothermic
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("Tiến trình phản ứng", fontsize=9.5)
    ax.set_ylabel("Enthalpy (H)", fontsize=9.5)
    ax.set_title("b) Phản ứng thu nhiệt (ΔrH°298 > 0)", fontsize=10.5, fontweight="bold", color="#1A4E8A", pad=8)

    ax.plot([1.2, 4.0], [3.0, 3.0], color="#1A365D", lw=2.5)
    ax.plot([6.0, 8.8], [7.2, 7.2], color="#1A365D", lw=2.5)
    ax.plot([4.0, 6.0], [3.0, 7.2], color="#718096", lw=1.5, ls="--")
    ax.annotate("", xy=(5.0, 7.2), xytext=(5.0, 3.0), arrowprops=dict(arrowstyle="->", lw=2.2, color="#2B6CB0"))
    ax.text(2.6, 3.4, "Chất đầu (cđ)", ha="center", fontsize=9.5, fontweight="bold")
    ax.text(7.4, 7.6, "Sản phẩm (sp)", ha="center", fontsize=9.5, fontweight="bold")
    ax.text(5.3, 5.1, "ΔrH°298 > 0\n(Thu nhiệt)", ha="left", va="center", fontsize=9, fontweight="bold", color="#2B6CB0")

    plt.tight_layout()
    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    render_exo_endo_exchange("output/assets/hoa10_b17_trao_doi_nhiet.png")
    render_enthalpy_diagram("output/assets/hoa10_b17_gian_do_enthalpy.png")
    print("Generated diagrams in output/assets/")
