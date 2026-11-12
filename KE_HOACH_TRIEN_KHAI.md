# KẾ HOẠCH TRIỂN KHAI — AI STUDY DOCUMENT STUDIO

> **Trạng thái hiện tại:** Hoàn thành **Giai đoạn 1 (Khảo sát & Thiết kế)**. Đang chờ phê duyệt trước khi cài đặt Skills, viết code hoặc sử dụng API trả phí.

---

## 1. LỘ TRÌNH CÁC GIAI ĐOẠN TIẾP THEO

| Giai đoạn | Công việc trọng tâm | Đầu ra (Deliverables) | Thời gian ước tính |
| :--- | :--- | :--- | :---: |
| **Giai đoạn 2: Cài đặt hạ tầng & Skills** *(Chờ duyệt)* | - Kiểm tra môi trường Windows (Python 3.10+, Node.js ≥ 18).<br>- Cài đặt chọn lọc 4 Skills từ GitHub (`docling`, `pdf`, `docx`, `skill-creator`) vào `.agents/skills/`.<br>- Cài đặt thư viện phụ thuộc (`docx` npm, `pypdf`, `pymupdf`, `docling-slim`). | Môi trường chạy ổn định trên Windows; `validate.py` và `docx-js` test thành công 1 file mẫu. | **2 – 3 ngày** |
| **Giai đoạn 3: Xây dựng `study-docx-builder` & Adapter API** | - Xây dựng `study_schema.json` và `validate_study_json.py`.<br>- Viết `build_study_docx.mjs` chuẩn hóa A4, Times New Roman, Word Styles, Hóa học sub/superscript, bảng DXA, bảng đáp án.<br>- Tích hợp `LLMProviderAdapter` (Gemini API & OpenAI API qua `.env`).<br>- Viết `SKILL.md` và bộ `references/` cho Hóa học 10–11–12 GDPT 2018. | Skill `study-docx-builder` hoàn chỉnh cho **Chế độ A (Theo Bài)** và **Chế độ B (Theo Chương)**. | **5 – 7 ngày** |
| **Giai đoạn 4: Kiểm thử thực tế & Mở rộng đa môn** | - Chạy thử nghiệm trên 3 bài học + 1 chương Hóa học (10, 11, 12) từ SGK/giáo án thực tế.<br>- Đánh giá trực quan trên Microsoft Word & in thử PDF.<br>- Tích hợp module `inject_omml_equations.py` cho Toán & Vật lí.<br>- Tinh chỉnh prompt/template cho Sinh, Văn, Sử, Địa. | Bộ tài liệu mẫu đạt chuẩn + tài liệu hướng dẫn sử dụng cho giáo viên. | **4 – 5 ngày** |

**Tổng thời gian dự kiến (Giai đoạn 2 → 4):** Khoảng **11 – 15 ngày làm việc**.

---

## 2. NHỮNG KHÓ KHĂN DỰ KIẾN & PHƯƠNG ÁN XỬ LÝ

| Khó khăn dự kiến | Mức độ | Phương án khắc phục |
| :--- | :---: | :--- |
| **1. File SGK PDF nặng, có PDF dạng scan hoặc 2 cột** | Cao | Dùng `pdf` (`pymupdf`) cắt đúng số trang của Bài/Chương trước, sau đó mới đưa qua `docling-slim` (giảm thời gian đọc từ vài phút xuống vài giây). Chỉ bật OCR khi phát hiện trang không có text layer. |
| **2. Công thức Hóa học bị gãy dòng hoặc sai chỉ số/điện tích** | Cao | Quy định cú pháp đánh dấu thống nhất trong JSON trung gian (ví dụ `_{2}`, `^{2+}`), hàm parser trong `build_study_docx.mjs` tự động tách thành `TextRun` `subScript`/`superScript` và dùng Non-breaking space (`\u00A0`) giữ liền khối công thức. |
| **3. AI sinh sai đáp án tính toán Hóa học hoặc tạo nhiễu trùng lặp** | Cao | Áp dụng quy trình 8 bước tạo câu hỏi + checklist kiểm tra bắt buộc tại Bước 6 (yêu cầu AI ghi rõ các bước tính số mol/cân bằng phương trình trong trường nháp trước khi chốt đáp án A/B/C/D). |
| **4. Lệnh bash trong `anthropics/skills/docx` không chạy trực tiếp trên Windows** | Trung bình | Viết wrapper Python thuần (`zipfile`, `pathlib`) thay cho `unzip`/`rm`/`zip` khi cần chỉnh sửa XML hoặc chèn OMML; dùng `validate.py` chạy trực tiếp bằng Python trên Windows. |
| **5. Chèn công thức Word Equation (OMML) cho Toán/Vật lí** | Trung bình | Tách làm module độc lập (`inject_omml_equations.py`): dùng `latex2mathml` + XSLT chuẩn chuyển sang OMML, đặt placeholder trong `docx-js` rồi thay thế XML ở bước hậu xử lý. |

---

## 3. PHƯƠNG ÁN TỐI ƯU TỐC ĐỘ XỬ LÝ

1. **Tách biệt "Trí tuệ nội dung" và "Kỹ thuật dựng Word":** AI chỉ sinh **1 file JSON duy nhất** (`study_schema.json`) thay vì viết code JavaScript `docx-js` mới mỗi lần. Việc dùng chung 1 engine `build_study_docx.mjs` giúp giảm >60% lượng token đầu ra và loại bỏ lỗi cú pháp code khi xuất DOCX.
2. **Cache tài liệu nguồn đã trích xuất:** Khi giáo viên tạo nhiều bài học từ cùng 1 cuốn SGK PDF hoặc cùng 1 Chương (Chế độ B), kết quả trích xuất Markdown/JSON từ `docling` được lưu cache cục bộ để tái sử dụng ngay lập tức.
3. **Cắt trang thông minh trước khi gọi AI:** Chỉ gửi phần văn bản thuộc đúng Bài học/Chương được chọn vào LLM API, giúp giảm chi phí API và giữ AI tập trung, không bị nhiễu kiến thức bài khác.
4. **Kiểm tra cấu trúc bằng code trước khi dùng AI sửa:** `validate_study_json.py` kiểm tra tức thì (trong < 0.1 giây) các lỗi thiếu mục (ví dụ thiếu Ý nghĩa thực tiễn, thiếu ví dụ, không đủ 5 MCQ hoặc 2 Đúng/Sai 4 ý) trước khi xuất DOCX.
