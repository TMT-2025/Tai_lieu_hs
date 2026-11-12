# DANH SÁCH SKILLS ĐỀ XUẤT — AI STUDY DOCUMENT STUDIO

> **Nguyên tắc lựa chọn:** Tối giản số lượng (**6 Skills cốt lõi**), không cài trùng lặp chức năng, không cài toàn bộ repository khi chỉ cần 1 Skill, ưu tiên giấy phép mở rõ ràng (MIT / Apache 2.0) và tương thích hoàn toàn với **Google Antigravity trên Windows**.

---

## 1. BỘ 6 SKILLS CỐT LÕI ĐỀ XUẤT

| STT | Tên Skill | Nguồn gốc | Vai trò chính trong hệ thống | Trạng thái cài đặt |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `docling` | `docling-project/docling` (MIT) | Trích xuất cấu trúc chương/bài, bảng biểu, văn bản từ PDF/DOCX/PPTX/ảnh | Cần cài chọn lọc |
| **2** | `pdf` | `anthropics/skills` (Apache 2.0) | Xử lý PDF nhanh, cắt tách trang theo chương/bài từ SGK PDF lớn | Cần cài chọn lọc |
| **3** | `pptx` | `anthropics/skills` (Apache 2.0) | Đọc nội dung slide bài giảng PowerPoint (`.pptx`) làm tài liệu nguồn | **Đã có sẵn** (`~/.gemini/config/skills/pptx`) |
| **4** | `docx` | `anthropics/skills` (Apache 2.0) | Tạo file `.docx` chuẩn OOXML (`docx-js`), Word Styles, bảng DXA, kiểm tra XSD (`validate.py`) | Cần cài chọn lọc |
| **5** | `skill-creator` | `anthropics/skills` (Apache 2.0) | Thiết kế, đóng gói và viết bộ kiểm thử (evals) cho Skill điều phối | Cần cài chọn lọc (dùng khi phát triển) |
| **6** | `study-docx-builder` | **Tự xây dựng** (Dự án nội bộ) | **Skill điều phối trung tâm**: phân tích chương/bài, sinh nội dung theo 2 chế độ (Bài/Chương), tạo ma trận MCQ & Đúng/Sai 4 ý, kiểm tra công thức Hóa–Toán–Lý, gọi `docx` xuất Word chuẩn | Thiết kế ở GĐ1, xây dựng ở GĐ2 |

> **Lưu ý về tính gọn nhẹ:** Thay vì tách thêm Skill riêng cho kiểm tra công thức Hóa/Toán hoặc tóm tắt, các quy tắc sư phạm và kiểm tra công thức Hóa–Toán–Lý được tích hợp thành các module `references/` và `scripts/` ngay bên trong `study-docx-builder`. Điều này giúp bộ Skills giữ ở mức **6 Skills**, giảm chi phí nạp context và tránh điều phối chồng chéo.

---

## 2. VAI TRÒ & LÝ DO LỰA CHỌN TỪNG SKILL

### 2.1. `docling` (từ `docling-project/docling`)
- **Vai trò:** Bộ đọc và phân tích cấu trúc tài liệu nguồn đa định dạng (đặc biệt mạnh với SGK PDF có nhiều bảng biểu, cột, công thức hoặc PDF scan).
- **Lý do lựa chọn:**
  - Thay thế hoàn hảo cho `Airmomo/skills` (đã bị 404).
  - Được bảo trì chính chủ bởi IBM Research (MIT License), xuất ra `DoclingDocument` (Markdown/JSON) giữ nguyên cấp độ tiêu đề (Chương → Bài → Mục), giúp Bước 2 (Phân tích chương/bài) chính xác hơn hẳn `pdftotext` thông thường.
- **Phụ thuộc:** Python ≥ 3.10, `docling-slim` (khuyên dùng bản slim trước để nhẹ máy Windows, chỉ cài thêm OCR engine khi gặp file scan).

### 2.2. `pdf` (từ `anthropics/skills`)
- **Vai trò:** Công cụ bổ trợ tốc độ cao cho PDF: cắt tách riêng các trang thuộc Bài học hoặc Chương cần biên soạn từ file SGK dày hàng trăm trang trước khi phân tích.
- **Lý do lựa chọn:**
  - Nếu đưa nguyên file SGK PDF 200 trang vào `docling` mỗi lần tạo 1 bài học sẽ rất chậm. Dùng `pdf` (`pypdf`/`pymupdf`) cắt đúng 5–10 trang của bài học rồi mới trích xuất giúp tăng tốc độ gấp nhiều lần.
- **Phụ thuộc:** Python 3, `pypdf`, `pdfplumber`, `pymupdf`.

### 2.3. `pptx` (đã cài sẵn)
- **Vai trò:** Trích xuất nội dung từ file bài giảng PowerPoint (`.pptx`) do giáo viên cung cấp thông qua `markitdown`.
- **Lý do lựa chọn:** Đã có sẵn trong môi trường Antigravity của người dùng, không phát sinh công sức cài đặt hay xung đột.

### 2.4. `docx` (từ `anthropics/skills`)
- **Vai trò:** Động cơ xuất bản Word `.docx` chuyên nghiệp.
- **Lý do lựa chọn:**
  - Sử dụng `docx` (`docx-js`) cho phép lập trình chính xác từng thông số: khổ giấy A4, lề `2.5 / 2.0 / 2.0 / 2.0 cm` (tính bằng DXA), font `Times New Roman`, **Word Styles thực sự** (`Title`, `Heading 1`, `Heading 2`, `Heading 3`, `Normal`), chỉ số trên/dưới (`superScript`/`subScript`) cho Hóa học, bảng biểu `WidthType.DXA` không tràn lề, đánh số trang, Header/Footer và Mục lục tự động (TOC).
  - Có sẵn `scripts/office/validate.py` để kiểm tra schema OOXML, đảm bảo file xuất ra mở sạch sẽ trên Microsoft Word, WPS và Google Docs.
- **Phụ thuộc:** Node.js (≥ 18) + gói npm `docx`; Python 3 (chạy `validate.py`); tùy chọn LibreOffice + Poppler nếu muốn render PDF/JPG kiểm tra trực quan.

### 2.5. `skill-creator` (từ `anthropics/skills`)
- **Vai trò:** Công cụ chuẩn hóa khi viết `study-docx-builder/SKILL.md`, tối ưu phần `description` để Antigravity kích hoạt đúng ngữ cảnh và viết test cases kiểm tra chất lượng đầu ra.
- **Phụ thuộc:** Không có phụ thuộc nặng (chủ yếu hướng dẫn & script Python kiểm tra cấu trúc skill).

### 2.6. `study-docx-builder` (Skill tự thiết kế)
- **Vai trò:** "Nhạc trưởng" toàn bộ quy trình biên soạn học liệu:
  1. Tiếp nhận yêu cầu giáo viên (Môn, Khối, Bộ sách, Chương/Bài, Chế độ A hay B).
  2. Gọi `pdf` / `docling` / `pptx` trích xuất nguồn.
  3. Phân tích kiến thức trọng tâm, liên hệ **Ý nghĩa thực tiễn** (Việt Nam), tạo ví dụ cho từng đề mục.
  4. Lập **ma trận câu hỏi** và sinh **5 MCQ + 2 Đúng/Sai (4 nhận định)** cho Bài học, hoặc **15 MCQ + 5 Đúng/Sai** cho Chương.
  5. Chạy **kiểm tra chất lượng nội dung & công thức** (cân bằng phương trình Hóa học, kiểm tra đáp án tính toán, loại bỏ nhiễu trùng đáp án đúng).
  6. Sinh script `docx-js` (hoặc chèn OMML Equation cho Toán/Lý) thông qua chuẩn của skill `docx` để xuất file `.docx` hoàn chỉnh.

---

## 3. PHƯƠNG ÁN TÍCH HỢP VÀO GOOGLE ANTIGRAVITY (CHƯA THỰC THI Ở GĐ1)

Theo chuẩn Antigravity (`.agents/skills/` ở cấp dự án hoặc `~/.gemini/config/skills/` ở cấp máy):
1. **Lưu trữ cục bộ theo dự án** tại `<workspace>/.agents/skills/` để dễ quản lý phiên bản (Git) và không ảnh hưởng các dự án khác:
   - `.agents/skills/docling/` (chỉ copy thư mục skill `docling`, không clone cả repo 70k stars).
   - `.agents/skills/pdf/` (chỉ copy `skills/pdf` từ `anthropics/skills`).
   - `.agents/skills/docx/` (chỉ copy `skills/docx` từ `anthropics/skills`).
   - `.agents/skills/skill-creator/` (tùy chọn đặt ở global hoặc workspace khi phát triển).
   - `.agents/skills/study-docx-builder/` (Skill điều phối tự xây dựng).
   - Riêng `pptx` dùng bản đã có sẵn tại `~/.gemini/config/skills/pptx/`.
2. **Adapter cho môi trường Windows:**
   - Thay các lệnh shell Linux trong hướng dẫn (`unzip`, `rm -f`, `pdftoppm`) bằng script Python chuẩn (`zipfile`, `pathlib`) hoặc PowerShell để chạy trơn tru 100% trên Windows mà không cần WSL.
   - Bổ sung module Python nhỏ dùng `latex2mathml` + `mathml2omml` (hoặc XSLT `MML2OMML.XSL` chuẩn của Word) để chuyển công thức Toán/Vật lí thành **Word Equation (OMML)** chỉnh sửa được trong `.docx`.
