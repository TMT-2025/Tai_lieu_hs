import json
import re
import sys
from pathlib import Path
import pymupdf


def detect_meta(filename: str) -> dict:
    upper = filename.upper()
    # Grade
    khoi = "Không rõ"
    for g in ["10", "11", "12"]:
        if re.search(rf"\b{g}\b", upper):
            khoi = g
            break

    # Textbook series
    if "KNTT" in upper:
        bo_sach = "Kết nối tri thức"
    elif "CTST" in upper:
        bo_sach = "Chân trời sáng tạo"
    elif "CANH DIEU" in upper:
        bo_sach = "Cánh Diều"
    else:
        bo_sach = "Chung (GDPT 2018)"

    # Document type
    if "YEU CAU CAN DAT" in upper:
        loai = "Yêu cầu cần đạt"
    elif "BAI TAP" in upper:
        loai = "Sách bài tập"
    elif "CHUYEN DE" in upper:
        loai = "Chuyên đề học tập"
    elif "SGV" in upper:
        loai = "Sách giáo viên"
    elif "SGK" in upper:
        loai = "Sách giáo khoa"
    else:
        loai = "Tài liệu khác"

    return {"khoi_lop": khoi, "bo_sach": bo_sach, "loai": loai}


def build_index(sgk_dir: Path, out_path: Path) -> dict:
    entries = []
    for pdf_path in sorted(sgk_dir.glob("*.pdf")):
        meta = detect_meta(pdf_path.name)
        doc = pymupdf.open(pdf_path)
        pages = len(doc)
        # Check text layer on up to 5 sample pages
        sample_indices = [i for i in [0, 1, 2, 3, min(10, pages - 1)] if i < pages]
        text_chars = sum(len(doc[i].get_text().strip()) for i in sample_indices)
        has_text = text_chars > 80

        # Extract embedded TOC bookmarks if available
        raw_toc = doc.get_toc(simple=True)
        toc = [{"level": lvl, "title": title.strip(), "page": pg} for lvl, title, pg in raw_toc]

        # Fallback: parse text-based Mục lục in first 6 pages if no PDF bookmarks
        toc_text = ""
        if not toc and has_text:
            for i in range(min(6, pages)):
                t = doc[i].get_text()
                if "MỤC LỤC" in t.upper() or "CHƯƠNG" in t.upper():
                    toc_text += f"\n--- Page {i + 1} ---\n" + t

        entries.append({
            "filename": pdf_path.name,
            "path": str(pdf_path.relative_to(sgk_dir.parent)).replace("\\", "/"),
            **meta,
            "pages": pages,
            "has_text_layer": has_text,
            "toc_count": len(toc),
            "toc": toc,
            "toc_text_preview": toc_text[:3000] if toc_text else "",
        })
        doc.close()

    index_data = {"total_files": len(entries), "files": entries}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(index_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return index_data


def extract_pages(pdf_path: Path, start_page: int, end_page: int) -> str:
    """Extract 1-based inclusive page range from a PDF."""
    doc = pymupdf.open(pdf_path)
    s = max(0, start_page - 1)
    e = min(len(doc), end_page)
    chunks = []
    for i in range(s, e):
        chunks.append(f"=== TRANG {i + 1} ===\n{doc[i].get_text()}")
    doc.close()
    return "\n".join(chunks)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--extract":
        pdf_file = Path(sys.argv[2])
        sp, ep = int(sys.argv[3]), int(sys.argv[4])
        print(extract_pages(pdf_file, sp, ep))
    else:
        sgk_folder = Path("SGK")
        out_file = Path("data/sgk_index.json")
        idx = build_index(sgk_folder, out_file)
        print(f"Indexed {idx['total_files']} PDF files -> {out_file}")
        for f in idx["files"]:
            print(f" - [{f['khoi_lop']} | {f['bo_sach']} | {f['loai']}] {f['filename']} (pages={f['pages']}, text={f['has_text_layer']}, toc={f['toc_count']})")
