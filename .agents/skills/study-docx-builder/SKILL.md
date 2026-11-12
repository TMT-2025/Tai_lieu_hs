---
name: study-docx-builder
description: >-
  Biên soạn tài liệu ôn tập chuẩn GDPT 2018 cho THPT (Hóa học, Vật lí, Sinh học lớp 10, 11, 12)
  và THCS (Khoa học tự nhiên lớp 6, 7, 8, 9) từ thư mục SGK chính thức (KNTT, CTST, Cánh Diều)
  và xuất file Microsoft Word (.docx) chuẩn sư phạm (A4, Times New Roman, Word Styles thật,
  hình minh họa 300 DPI, giải thích thực tiễn liên kết phần C, 5 MCQ + 2 Đúng/Sai cho Bài học
  hoặc 15 MCQ + 5 Đúng/Sai cho Chương).
---

# Study DOCX Builder (v4 — Đa môn GDPT 2018: Hóa học, Vật lí, Sinh học & KHTN 6–9)

Skill điều phối trung tâm của **AI STUDY DOCUMENT STUDIO**.

## 1. Phạm vi môn học & Bộ sách hỗ trợ
- **THPT (Lớp 10, 11, 12)**: Hóa học, Vật lí, Sinh học.
- **THCS (Lớp 6, 7, 8, 9)**: Khoa học tự nhiên (tích hợp Vật lí – Hóa học – Sinh học).
- **Bộ sách**: Kết nối tri thức với cuộc sống (KNTT), Chân trời sáng tạo (CTST), Cánh Diều, hoặc **Tổng hợp cả 3 bộ sách**.

## 2. Hệ sinh thái Skills & Công cụ theo từng môn
- **`study-docx-builder`** (Điều phối trung tâm):
  - Tra cấu hình SGK tại `data/configs/SGK_<MON>_<LOP>_<BO_SACH>.json` (nếu chưa có cho môn mới, quét `SGK/` bằng `index_sgk.py` và trích xuất mục lục).
  - Sinh JSON theo `templates/study_schema.json` (Chế độ A — Bài học: 5 MCQ [2 NB, 2 TH, 1 VD] + 2 Đúng/Sai) hoặc `templates/chapter_schema.json` (Chế độ B — Chương: 15 MCQ + 5 Đúng/Sai).
  - Quy ước ký hiệu chung: dùng `_{...}` cho chỉ số dưới (`H_{2}O`, `v_{0}`, `CO_{2}`), `^{...}` cho chỉ số trên/điện tích/đơn vị (`Fe^{3+}`, `m/s^{2}`, `10^{-3}`), `->` cho mũi tên.
- **`pdf`** (`.agents/skills/pdf/`): Cắt tách đúng trang của bài/chương từ `SGK/` bằng `PyMuPDF` (kể cả sách scan ảnh bằng cách render PNG đọc trực tiếp).
- **Hóa học** *(và phân môn Hóa KHTN 6–9)*:
  - Dùng `chem-vis` (`.agents/skills/chem-vis/`) vẽ cấu trúc phân tử 2D (RDKit); dùng `render_lewis_and_structures.py` cho công thức Lewis; dùng `render_chem_diagrams.py` cho sơ đồ hóa học.
- **Vật lí** *(và phân môn Lí KHTN 6–9)*:
  - Dùng `render_science_diagrams.py` (`render_physics_harmonic_graph`, `render_classification_diagram`) hoặc `matplotlib` vẽ đồ thị (`x-t`, `v-t`, sóng), giản đồ vector, sơ đồ nguyên lí (300 DPI).
- **Sinh học** *(và phân môn Sinh KHTN 6–9)*:
  - Dùng `render_science_diagrams.py` (`render_biology_cycle`, `render_classification_diagram`) hoặc `markdown-mermaid-writing` vẽ chu trình sinh học (nguyên phân, giảm phân, phiên mã – dịch mã, chuỗi thức ăn) 300 DPI.
- **`docx`** (`.agents/skills/docx/`): Chuẩn OOXML, Word Styles thật, tự động tách xuống dòng và thụt lề từng `Bước 1:`, `Bước 2:`, `Bước 3:` trong phần Hướng dẫn giải.

## 3. Lệnh thực thi chuẩn
```powershell
# 1. Kiểm tra JSON (lesson hoặc chapter)
python .agents/skills/study-docx-builder/scripts/validate_study_json.py <input.json> --mode lesson

# 2. Xuất DOCX chuẩn sư phạm
node .agents/skills/study-docx-builder/scripts/build_study_docx.mjs <input.json> <output.docx> --mode lesson
```
*(Đổi `--mode lesson` thành `--mode chapter` cho Chế độ B — Tổng hợp Chương).*
