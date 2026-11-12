import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams["font.family"] = "DejaVu Sans"

# Valence electrons for common main-group elements
VALENCE_E = {
    "H": 1, "C": 4, "N": 5, "O": 6, "F": 7, "Cl": 7, "Br": 7, "I": 7, "S": 6, "P": 5
}


def verify_valence_electrons(atom_counts: dict[str, int], charge: int = 0) -> int:
    """Tính và kiểm tra tổng số electron hóa trị cho công thức Lewis."""
    total = sum(VALENCE_E[el] * cnt for el, cnt in atom_counts.items()) - charge
    if total < 0 or total % 2 != 0:
        raise ValueError(f"Tổng electron hóa trị không hợp lệ ({total}) cho {atom_counts}, charge={charge}")
    return total


def render_classification_diagram(title: str, root_label: str, branches: list[tuple[str, list[str]]], out_path: str):
    """Vẽ sơ đồ phân loại / hệ thống hóa kiến thức dạng cây ngang sắc nét (300 DPI)."""
    fig, ax = plt.subplots(figsize=(9.5, max(3.6, 1.3 * len(branches))), dpi=300)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title(title, fontsize=11.5, fontweight="bold", color="#1B365D", pad=8)

    # Root node
    root_box = patches.FancyBboxPatch((0.3, 4.1), 2.3, 1.8, boxstyle="round,pad=0.18", fc="#1B365D", ec="#1B365D")
    ax.add_patch(root_box)
    ax.text(1.45, 5.0, root_label, ha="center", va="center", fontsize=10, fontweight="bold", color="white")

    n = len(branches)
    ys = [8.2 - i * (6.4 / max(1, n - 1)) for i in range(n)] if n > 1 else [5.0]

    for (b_title, b_items), y in zip(branches, ys):
        ax.annotate("", xy=(3.4, y), xytext=(2.7, 5.0), arrowprops=dict(arrowstyle="->", lw=1.8, color="#2B5B84"))
        b_box = patches.FancyBboxPatch((3.4, y - 0.65), 2.5, 1.3, boxstyle="round,pad=0.12", fc="#E8EEF5", ec="#2B5B84", lw=1.5)
        ax.add_patch(b_box)
        ax.text(4.65, y, b_title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#1B365D")

        ax.annotate("", xy=(6.4, y), xytext=(5.95, y), arrowprops=dict(arrowstyle="->", lw=1.5, color="#4A5568"))
        detail_text = "\n".join(f"• {it}" for it in b_items)
        d_box = patches.FancyBboxPatch((6.4, y - 0.75), 3.3, 1.5, boxstyle="round,pad=0.12", fc="#F7FAFC", ec="#A0AEC0", lw=1.2)
        ax.add_patch(d_box)
        ax.text(6.55, y, detail_text, ha="left", va="center", fontsize=8.5, color="#1A202C")

    plt.tight_layout()
    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def render_rdkit_2d_grid(smiles_list: list[tuple[str, str]], out_path: str):
    """Dùng RDKit (từ chem-vis) vẽ lưới cấu trúc phân tử 2D sắc nét để chèn vào Word."""
    from rdkit import Chem
    from rdkit.Chem import Draw

    mols = []
    legends = []
    for smi, label in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            raise ValueError(f"SMILES không hợp lệ: {smi}")
        mols.append(mol)
        legends.append(label)

    img = Draw.MolsToGridImage(mols, molsPerRow=min(3, len(mols)), subImgSize=(380, 260), legends=legends)
    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
