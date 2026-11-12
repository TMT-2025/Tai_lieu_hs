---
name: study-docx-builder
description: >-
  Biên soạn tài liệu ôn tập Hóa học THPT Việt Nam (10, 11, 12 — GDPT 2018) từ thư mục SGK chính thức
  (KNTT, CTST, Cánh Diều) và xuất file Microsoft Word (.docx) chuẩn sư phạm (A4, Times New Roman,
  Word Styles thật, cấu trúc 2D RDKit, sơ đồ phân loại, giải thích thực tiễn liên kết phần C,
  5 MCQ + 2 Đúng/Sai cho Bài học hoặc 15 MCQ + 5 Đúng/Sai cho Chương).
---

# Study DOCX Builder (v3 — Tích hợp RDKit 2D, Sơ đồ & 9 Cấu hình SGK)

Skill điều phối trung tâm của **AI STUDY DOCUMENT STUDIO**.

## 1. Hệ sinh thái Skills phối hợp
- **`study-docx-builder`** (Điều phối trung tâm): Phân tích SGK theo `data/configs/SGK_HOA_<10|11|12>_<KNTT|CTST|CANH_DIEU>.json`, sinh nội dung chuẩn GDPT 2018, kiểm tra JSON.
- **`chem-vis`** (`.agents/skills/chem-vis/`): Dùng RDKit (`render_rdkit_2d_grid`) vẽ công thức cấu tạo 2D (đặc biệt Hóa hữu cơ). **Không** dùng `chem-vis` cho công thức Lewis; dùng `render_lewis_and_structures.py` (`verify_valence_electrons`) để kiểm tra electron hóa trị.
- **`markdown-mermaid-writing`** (`.agents/skills/markdown-mermaid-writing/`): Chuẩn hóa tư duy sơ đồ phân loại, luồng kiến thức và kết xuất sang ảnh 300 DPI qua `render_classification_diagram`.
- **`docx`** (`.agents/skills/docx/`): Chuẩn OOXML, `docx-js`, Word Styles thật, kiểm tra XSD.
- **`pdf`** (`.agents/skills/pdf/`): Cắt tách trang SGK nhanh bằng `PyMuPDF` (chỉ đọc đúng trang của bài/chương, không quét lại toàn bộ sách).

## 2. Lệnh thực thi chuẩn
```powershell
# 1. Kiểm tra JSON
python .agents/skills/study-docx-builder/scripts/validate_study_json.py <input.json> --mode lesson

# 2. Xuất DOCX
node .agents/skills/study-docx-builder/scripts/build_study_docx.mjs <input.json> <output.docx> --mode lesson
```
