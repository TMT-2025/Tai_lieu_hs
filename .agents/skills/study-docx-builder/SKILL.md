---
name: study-docx-builder
description: >-
  Biên soạn tài liệu ôn tập chuẩn GDPT 2018 cho THPT (Toán học, Vật lí, Hóa học, Sinh học lớp 10, 11, 12)
  và THCS (Khoa học tự nhiên lớp 6, 7, 8, 9) từ thư mục SGK chính thức (KNTT, CTST, Cánh Diều)
  và xuất file Microsoft Word (.docx) chuẩn sư phạm (A4, Times New Roman, Word Styles thật,
  công thức Word Equation OMML chỉnh sửa trực tiếp, hình minh họa 300 DPI, 5 MCQ + 2 Đúng/Sai cho Bài học
  hoặc 15 MCQ + 5 Đúng/Sai cho Chương).
---

# Study DOCX Builder (v5 — Tích hợp OMML Word Equation cho Toán, Vật lí & Hóa–Sinh–KHTN)

Skill điều phối trung tâm của **AI STUDY DOCUMENT STUDIO**.

## 1. Phạm vi môn học & Bộ sách hỗ trợ
- **THPT (Lớp 10, 11, 12)**: Toán học, Vật lí, Hóa học, Sinh học.
- **THCS (Lớp 6, 7, 8, 9)**: Khoa học tự nhiên.
- **Bộ sách**: Kết nối tri thức với cuộc sống (KNTT), Chân trời sáng tạo (CTST), Cánh Diều, hoặc **Tổng hợp cả 3 bộ sách**.

## 2. Hệ sinh thái Skills & Công cụ công thức
- **`math-physics-equation-engine`** (`scripts/math_physics_equation_engine.py`, phối hợp **`omml-formula-skill`**):
  - Tự động chuyển mọi biểu thức `$...$` (inline) và `$$...$$` (block) thành **Word Equation OMML thật** (`<m:oMath>`, `<m:oMathPara>`) chỉnh sửa được trong Microsoft Word.
  - **Không dùng ảnh cho công thức** khi Word Equation biểu diễn được chính xác (phân số, căn thức, vector `\vec{F}`, tích phân, đạo hàm, giới hạn, ma trận, hệ phương trình `\begin{cases}...\end{cases}`, chữ cái Hy Lạp, đơn vị SI chữ đứng `\mathrm{m/s^2}`).
  - Tự động chạy khi `build_study_docx.mjs` phát hiện ký hiệu `$`. Nếu chuyển đổi thất bại phải báo lỗi rõ ràng, không âm thầm bỏ công thức.
- **`latex-omml-docx-audit`** (`.agents/skills/latex-omml-docx-audit/scripts/audit_docx_formula_state.py`):
  - Kiểm tra sau khi xuất DOCX: bắt buộc đạt trạng thái `native-omml`, `raw_latex_residue == 0`.
- **Quy tắc riêng cho Toán học**: Bảo toàn giả thiết và điều kiện xác định; hiển thị đúng dấu ngoặc, phân số, căn thức; kiểm tra phép biến đổi đại số và kết quả (SymPy); trình bày lời giải từng bước.
- **Quy tắc riêng cho Vật lí**: Phân biệt đại lượng vô hướng và vector (`\vec{F}`, `\vec{a}`); đơn vị SI chữ đứng (`\mathrm{N}`, `\mathrm{kg}`, `\mathrm{m/s^2}`); kiểm tra thứ nguyên, điều kiện áp dụng công thức và kết quả tính toán.
- **Công cụ chuyên môn khác**: `pdf` (PyMuPDF), `chem-vis` (RDKit 2D cho Hóa), `render_science_diagrams.py` (Matplotlib 300 DPI cho đồ thị Vật lí, chu trình Sinh học, sơ đồ phân loại), `docx` (OOXML).

## 3. Lệnh thực thi chuẩn
```powershell
# 1. Kiểm tra JSON (lesson hoặc chapter)
python .agents/skills/study-docx-builder/scripts/validate_study_json.py <input.json> --mode lesson

# 2. Xuất DOCX (tự động gọi math-physics-equation-engine chuyển LaTeX -> OMML)
node .agents/skills/study-docx-builder/scripts/build_study_docx.mjs <input.json> <output.docx> --mode lesson

# 3. Kiểm tra công thức Word Equation (bắt buộc cho Toán, Vật lí)
python .agents/skills/latex-omml-docx-audit/scripts/audit_docx_formula_state.py <output.docx> --json
```
