# HƯỚNG DẪN SỬ DỤNG NHANH — AI STUDY DOCUMENT STUDIO

## 1. Lập chỉ mục SGK trong thư mục `SGK/` (chạy 1 lần khi thêm sách mới)
```powershell
python .agents/skills/study-docx-builder/scripts/index_sgk.py
```
Kết quả lưu tại [sgk_index.json](file:///e:/.%20UNG%20DUNG%20MOI/Tao_Tai_lieu_Hoc_Tap-hs/data/sgk_index.json) (36 file Hóa 10–11–12: KNTT, CTST, Cánh Diều).

## 2. Tạo tài liệu ôn tập theo Bài học (Chế độ A) hoặc theo Chương (Chế độ B)
### Cách 1 — Tự động qua Gemini API (cấu hình `GEMINI_API_KEY` trong `.env`):
```powershell
# Chế độ A (Bài học)
node .agents/skills/study-docx-builder/scripts/generate_from_source.mjs "10" "Kết nối tri thức" "Chương 5" "Bài 17" 81 87 lesson

# Chế độ B (Tổng hợp Chương: 15 MCQ + 5 Đúng/Sai)
node .agents/skills/study-docx-builder/scripts/generate_from_source.mjs "10" "Kết nối tri thức" "Chương 5" "Ôn tập Chương 5" 81 90 chapter
```

### Cách 2 — Xuất DOCX từ file JSON đã kiểm duyệt:
```powershell
python .agents/skills/study-docx-builder/scripts/validate_study_json.py <input.json> --mode lesson
node .agents/skills/study-docx-builder/scripts/build_study_docx.mjs <input.json> <output.docx> --mode lesson
```
*(Đổi `--mode lesson` thành `--mode chapter` cho Chế độ B).*
