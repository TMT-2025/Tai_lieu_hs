# BÁO CÁO ĐÁNH GIÁ GITHUB SKILLS — AI STUDY DOCUMENT STUDIO (GIAI ĐOẠN 1)

> **Phạm vi khảo sát:** Khảo sát thực tế các repository GitHub theo yêu cầu Prompt 01 & Bổ sung yêu cầu, kết hợp tìm kiếm bổ sung các Skills phù hợp cho trích xuất tài liệu, biên soạn học liệu GDPT 2018, tạo câu hỏi trắc nghiệm/đúng-sai, kiểm tra công thức Hóa–Toán–Lý và xuất file Microsoft Word (`.docx`) trên môi trường Windows + Google Antigravity.

---

## 1. TỔNG HỢP KẾT QUẢ KHẢO SÁT NHANH

| STT | Skill / Repository | Nhóm | Trạng thái GitHub | Giấy phép | Antigravity | Điểm (1–5) | Quyết định |
| :--- | :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | `Airmomo/skills` (`docling-document-intelligence`) | A | **404 Not Found** | Không xác định | Không | **1.0** | **Loại** (Link hỏng, thay bằng repo chính thức `docling-project/docling`) |
| 2 | `docling-project/docling` (`docling`) *(Mới đề xuất)* | A | Tồn tại (70.4k+ ★) | **MIT** | Tương thích | **4.5** | **Chọn** (Trích xuất đa định dạng PDF/DOCX/PPTX giữ cấu trúc) |
| 3 | `anthropics/skills` (`pdf`) | A | Tồn tại (193k+ ★) | **Apache 2.0** | Tương thích | **4.5** | **Chọn** (Xử lý PDF nhẹ, tách trang theo chương/bài) |
| 4 | `anthropics/skills` (`pptx`) | A | Tồn tại (đã cài sẵn local) | **Apache 2.0** | **Có sẵn** | **4.0** | **Dùng sẵn** (Đọc PPTX qua `markitdown`, không cần cài lại) |
| 5 | `anthropics/skills` (`docx`) | A & C | Tồn tại (193k+ ★) | **Apache 2.0** | Tương thích | **5.0** | **Chọn bắt buộc** (Tạo/sửa DOCX chuẩn OOXML, Styles, `validate.py`) |
| 6 | `hheydaroff/common-agent-skills` (`summarize`) | B | Tồn tại (0 ★) | **Không có License** | Cần sửa nhiều | **2.0** | **Loại** (Phụ thuộc CLI `pi` và `claude-haiku-4-5`, trùng chức năng) |
| 7 | `jacquardlabs/study-skills` (`topic-map`, `understanding-check`...) | B | Tồn tại (2 ★) | **MIT** | Tương thích | **2.5** | **Không cài** (Hướng nghiên cứu đại học; chỉ tham khảo kỹ thuật đặt câu hỏi) |
| 8 | `toddward/the-learning-skill` | B | Tồn tại (7 ★) | **MIT** | Tương thích | **2.5** | **Không cài** (Hướng gia sư chat 1-1; chỉ tham khảo nguyên tắc *Source beats invention*) |
| 9 | `anthropics/skills` (`doc-coauthoring`) | C | Tồn tại (193k+ ★) | **Apache 2.0** | Tương thích | **2.5** | **Không cài** (Thiết kế cho viết PRD/RFC kỹ thuật, không hợp học liệu THPT) |
| 10 | `anthropics/skills` (`skill-creator`) | C | Tồn tại (193k+ ★) | **Apache 2.0** | Tương thích | **4.5** | **Chọn** (Hỗ trợ tạo & đánh giá Skill điều phối `study-docx-builder`) |
| 11 | `sickn33/agentic-awesome-skills` (`examprep-ai`) | D | Tồn tại (49.5k+ ★) | **MIT** | Tương thích | **3.0** | **Tham khảo** (Có ma trận Easy/Medium/Hard & Syllabus Guardrail, nhưng xuất Markdown cho SV ôn thi) |
| 12 | `github/awesome-copilot` (`md-to-docx`) *(Mới khảo sát)* | Bổ sung | Tồn tại (41k+ ★) | **MIT** | Tương thích | **3.0** | **Loại** (Đơn giản, nhưng không hỗ trợ tốt OMML Equation, chỉ số Hóa học & kiểm tra XSD như `anthropics/docx`) |
| 13 | `ndpvt-web/latex-document-skill` *(Mới khảo sát)* | Bổ sung | Tồn tại (828 ★) | **Không có License** | Tương thích | **2.0** | **Loại** (Xuất LaTeX/PDF, không phục vụ mục tiêu xuất Word DOCX chỉnh sửa được) |

---

## 2. ĐÁNH GIÁ CHI TIẾT TỪNG SKILL (THEO 10 TIÊU CHÍ)

### Nhóm A — Đọc và xử lý tài liệu

#### 2.1. `Airmomo/skills` — `docling-document-intelligence`
- **Liên kết GitHub:** `https://github.com/Airmomo/skills/tree/main/docling-document-intelligence`
- **Tồn tại & truy cập:** **Không** (API GitHub trả về `404 Not Found` tại thời điểm khảo sát).
- **SKILL.md hợp lệ:** Không kiểm tra được do repository không tồn tại.
- **Khuyến nghị:** Loại bỏ và thay thế bằng Skill **chính chủ** từ đội ngũ IBM Docling (`docling-project/docling`).
- **Điểm đánh giá:** **1/5**.

#### 2.2. `docling-project/docling` — `docling` *(Đề xuất thay thế)*
- **Liên kết GitHub:** https://github.com/docling-project/docling/blob/main/docling/.agents/skills/docling/SKILL.md
- **Tồn tại & truy cập:** Có, repository chính thức của IBM Research (70.400+ stars).
- **SKILL.md hợp lệ:** Có (84 dòng, YAML frontmatter chuẩn `name`, `description`, `license: MIT`, `compatibility: Requires Python 3.10+`).
- **Tương thích Google Antigravity:** Tương thích tốt. Chỉ cần điều chỉnh nhẹ phần `allowed-tools` nếu cần khớp tên tool của Antigravity (`run_command`), hoặc giữ nguyên làm hướng dẫn CLI/SDK.
- **Chức năng:** Chuyển đổi PDF (cả PDF chữ và PDF scan/OCR), DOCX, PPTX, XLSX, HTML, ảnh thành cấu trúc `DoclingDocument` thống nhất (Markdown hoặc JSON bảo toàn cấu trúc phân cấp chương/bài và bảng biểu).
- **Trùng lặp:** Chồng lấn một phần việc đọc PDF/DOCX/PPTX với `anthropics/pdf` và `markitdown`, nhưng vượt trội về bảo toàn bố cục bảng biểu, công thức và cấu trúc phân cấp tài liệu giáo khoa dài.
- **Thư viện phụ thuộc:** Python ≥ 3.10, gói `docling` (hoặc `docling-slim` để giảm dung lượng phụ thuộc), `uv`/`pip`.
- **Giấy phép:** **MIT** — Cho phép sử dụng thương mại và chỉnh sửa tự do.
- **Phù hợp Windows:** Tốt trên Windows 10/11 với Python 3.10+ (lưu ý nếu bật OCR nặng thì cần thêm RAM/GPU hoặc dùng cấu hình `docling-slim` cho PDF text).
- **Nâng cao chất lượng DOCX:** Gián tiếp rất cao — đầu vào sạch, giữ đúng thứ tự chương/bài và bảng biểu giúp AI biên soạn nội dung và bảng so sánh chính xác hơn.
- **Điểm đánh giá:** **4.5/5**.

#### 2.3. `anthropics/skills` — `pdf`
- **Liên kết GitHub:** https://github.com/anthropics/skills/tree/main/skills/pdf
- **Tồn tại & truy cập:** Có.
- **SKILL.md hợp lệ:** Có (315 dòng, có `scripts/` gồm 8 script Python hỗ trợ kiểm tra/trích xuất form và chuyển trang ảnh).
- **Tương thích Google Antigravity:** Tương thích tốt (chuẩn Agent Skills).
- **Cần adapter không:** Có thể dùng trực tiếp; trên Windows cần đảm bảo cài Python packages (`pypdf`, `pdfplumber`, `pymupdf`) và tránh các lệnh Linux thuần như `pdftotext` nếu chưa cài Poppler.
- **Chức năng:** Đọc/trích xuất text và bảng từ PDF, tách/gộp trang PDF (rất hữu ích để cắt riêng từng Chương hoặc Bài từ file SGK PDF lớn), OCR PDF scan.
- **Trùng lặp:** Bổ trợ cho `docling` (nhanh và nhẹ hơn khi chỉ cần cắt trang PDF hoặc đọc PDF thuần văn bản).
- **Thư viện phụ thuộc:** `pypdf`, `pdfplumber`, `pymupdf`, `pdf2image`, `pytesseract` (tùy tác vụ).
- **Giấy phép:** **Apache 2.0** (theo `LICENSE.txt` trong thư mục skill).
- **Phù hợp Windows:** Tốt (Python thuần chạy ổn định; phần OCR cần cài thêm Tesseract/Poppler cho Windows nếu xử lý file scan).
- **Nâng cao chất lượng DOCX:** Gián tiếp — giúp tách đúng phạm vi bài học/chương trước khi đưa vào AI, tránh lẫn kiến thức bài khác.
- **Điểm đánh giá:** **4.5/5**.

#### 2.4. `anthropics/skills` — `pptx`
- **Liên kết GitHub:** https://github.com/anthropics/skills/tree/main/skills/pptx
- **Tồn tại & truy cập:** Có, và **đã được cài đặt sẵn** trên máy cục bộ tại `C:\Users\ADMIN\.gemini\config\skills\pptx\SKILL.md`.
- **SKILL.md hợp lệ:** Có (238 dòng).
- **Tương thích Google Antigravity:** Tương thích 100% (đang hoạt động sẵn).
- **Chức năng:** Đọc nội dung slide bài giảng PowerPoint (`.pptx`, `.potx`) theo từng slide (`markitdown deck.pptx`), hữu ích khi giáo viên cung cấp giáo án điện tử làm tài liệu nguồn.
- **Trùng lặp:** Không cần cài đặt thêm từ GitHub vì đã có sẵn.
- **Thư viện phụ thuộc:** `markitdown` (để đọc PPTX).
- **Giấy phép:** **Apache 2.0**.
- **Phù hợp Windows:** Tốt.
- **Nâng cao chất lượng DOCX:** Giúp khai thác giáo án PPTX của giáo viên đầy đủ theo từng slide.
- **Điểm đánh giá:** **4.0/5**.

---

### Nhóm B — Tóm tắt và tổ chức kiến thức

#### 2.5. `hheydaroff/common-agent-skills` — `summarize`
- **Liên kết GitHub:** https://github.com/hheydaroff/common-agent-skills/tree/main/skills/summarize
- **Tồn tại & truy cập:** Có (0 stars).
- **SKILL.md hợp lệ:** Có (75 dòng), kèm `to-markdown.mjs`.
- **Tương thích Google Antigravity:** **Kém** — script `to-markdown.mjs` gọi CLI `pi` (`claude-haiku-4-5`) và `uvx markitdown`. Không chạy trực tiếp được nếu không cài hệ sinh thái Pi agent.
- **Cần adapter không:** Cần viết lại hoàn toàn phần gọi LLM nếu muốn dùng.
- **Chức năng:** Chuyển URL/PDF/DOCX sang Markdown bằng `markitdown` và tóm tắt ngắn.
- **Trùng lặp:** Trùng hoàn toàn với `docling` / `markitdown` trong đọc file, còn phần tóm tắt quá chung chung, không theo cấu trúc sư phạm (Mục tiêu, Ý nghĩa thực tiễn, Kiến thức trọng tâm, Ví dụ, MCQ/Đúng-Sai).
- **Thư viện phụ thuộc:** Node.js, `uvx`, `markitdown`, `yt-dlp`, CLI `pi`.
- **Giấy phép:** **Không có file License** (rủi ro pháp lý khi dùng lâu dài).
- **Phù hợp Windows:** Trung bình (cần `uvx` + Node.js).
- **Nâng cao chất lượng DOCX:** Không.
- **Điểm đánh giá:** **2.0/5** — **Loại**.

#### 2.6. `jacquardlabs/study-skills`
- **Liên kết GitHub:** https://github.com/jacquardlabs/study-skills
- **Tồn tại & truy cập:** Có (2 stars), gồm 5 skills: `topic-map`, `paper-reader`, `paper-critique`, `literature-map`, `understanding-check`.
- **SKILL.md hợp lệ:** Có.
- **Tương thích Google Antigravity:** Tương thích (thuần prompt/markdown workflow).
- **Cần adapter không:** Cần viết lại gần như toàn bộ nếu muốn dùng cho THPT Việt Nam, vì thiết kế cho sinh viên sau đại học đọc bài báo khoa học (academic papers).
- **Chức năng:** Lập bản đồ chủ đề (`topic-map`) và kiểm tra mức độ hiểu (`understanding-check` với 5 dạng câu hỏi: *Apply to a new case, Explain the why, Connect, Spot the error, Predict or compare*).
- **Trùng lặp:** Không tạo file DOCX, không hỗ trợ ma trận MCQ/Đúng-Sai 4 nhận định.
- **Thư viện phụ thuộc:** Không có (pure prompt skill).
- **Giấy phép:** **MIT**.
- **Phù hợp Windows:** Tốt.
- **Nâng cao chất lượng DOCX:** Không trực tiếp, chỉ hữu ích ở tư duy thiết kế câu hỏi hiểu bản chất trong `understanding-check`.
- **Điểm đánh giá:** **2.5/5** — **Không cài nguyên repo, chỉ trích lọc ý tưởng sư phạm**.

#### 2.7. `toddward/the-learning-skill`
- **Liên kết GitHub:** https://github.com/toddward/the-learning-skill (file nằm tại `the-learning-skill/SKILL.md`).
- **Tồn tại & truy cập:** Có (7 stars).
- **SKILL.md hợp lệ:** Có (278 dòng).
- **Tương thích Google Antigravity:** Tương thích.
- **Cần adapter không:** Có — skill này được thiết kế như một gia sư tương tác từng bước (*"Stop and ask. Wait for their answer"*), ngược với mục tiêu tạo tài liệu ôn tập Word hoàn chỉnh cho giáo viên.
- **Chức năng:** Dạy học 1-1 theo phương pháp Feynman, Active Recall, Spaced Repetition, tạo flashcard/Anki.
- **Điểm sáng:** Nguyên tắc số 4 **"Source beats invention"** (mọi kiến thức trong tài liệu sinh ra phải truy vết được về tài liệu nguồn, không bịa đặt dữ kiện).
- **Thư viện phụ thuộc:** Không bắt buộc (có thư mục `scripts/`, `references/`).
- **Giấy phép:** **MIT**.
- **Phù hợp Windows:** Tốt.
- **Nâng cao chất lượng DOCX:** Không trực tiếp.
- **Điểm đánh giá:** **2.5/5** — **Không cài, chỉ kế thừa nguyên tắc "Source beats invention"**.

---

### Nhóm C — Biên soạn và chuẩn hóa tài liệu

#### 2.8. `anthropics/skills` — `docx`
- **Liên kết GitHub:** https://github.com/anthropics/skills/tree/main/skills/docx
- **Tồn tại & truy cập:** Có.
- **SKILL.md hợp lệ:** Có (92 dòng hướng dẫn súc tích + thư mục `scripts/` gồm `merge_runs.py`, `comment.py`, `accept_changes.py`, `office/validate.py`, `office/soffice.py`).
- **Tương thích Google Antigravity:** Tương thích rất tốt.
- **Cần adapter không:** Cần bổ sung **template/profile cấu hình chuẩn Việt Nam** (A4, lề 2.5/2/2/2 cm, Times New Roman, Word Styles thật `Title`/`Heading 1..3`/`Normal`, bảng DXA, hàm render công thức Hóa học sub/superscript + OMML Toán/Lý) trong `study-docx-builder`.
- **Chức năng:**
  - Tạo mới `.docx` chất lượng cao bằng thư viện `docx` (`docx-js` trên Node.js).
  - Chỉnh sửa `.docx` có sẵn qua giải nén XML (`unzip` → sửa `word/document.xml` → `zip`).
  - Kiểm tra hợp lệ cấu trúc OOXML/XSD bằng `scripts/office/validate.py`.
  - Hỗ trợ chuyển PDF (`soffice.py`) + ảnh (`pdftoppm`) để kiểm tra trực quan bố cục trang.
- **Trùng lặp:** Mạnh và đầy đủ hơn hẳn `md-to-docx`.
- **Thư viện phụ thuộc:** Node.js + npm `docx`; Python 3 + `lxml`/`defusedxml` (cho `validate.py`); LibreOffice + Poppler nếu muốn render ảnh kiểm tra bố cục tự động.
- **Giấy phép:** **Apache 2.0**.
- **Phù hợp Windows:** Tốt cho tạo file (`node` + `docx`) và kiểm tra XML (`python validate.py`). Lưu ý các lệnh shell ví dụ trong `SKILL.md` dùng cú pháp bash (`rm`, `unzip`, `pdftoppm`), trên Windows cần chạy qua PowerShell/Python `zipfile` hoặc WSL/Git Bash khi dùng bước unzip/render.
- **Nâng cao chất lượng DOCX:** **Trực tiếp quyết định chất lượng DOCX** (Styles thực sự, bảng không tràn lề, không lỗi font/file hỏng).
- **Điểm đánh giá:** **5.0/5** — **Cốt lõi bắt buộc**.

#### 2.9. `anthropics/skills` — `doc-coauthoring`
- **Liên kết GitHub:** https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring
- **Tồn tại & truy cập:** Có.
- **SKILL.md hợp lệ:** Có (376 dòng).
- **Tương thích Google Antigravity:** Tương thích.
- **Chức năng:** Quy trình 3 bước đồng tác giả tài liệu kỹ thuật (Context Gathering → Refinement → Reader Testing) cho PRD, RFC, Design Doc.
- **Hạn chế:** Thiết kế cho tài liệu kỹ thuật phần mềm, quy trình hỏi đáp nhiều vòng sẽ làm chậm tốc độ tạo tài liệu ôn tập hàng tuần của giáo viên.
- **Giấy phép:** **Apache 2.0**.
- **Điểm đánh giá:** **2.5/5** — **Không chọn**.

#### 2.10. `anthropics/skills` — `skill-creator`
- **Liên kết GitHub:** https://github.com/anthropics/skills/tree/main/skills/skill-creator
- **Tồn tại & truy cập:** Có.
- **SKILL.md hợp lệ:** Có (486 dòng).
- **Tương thích Google Antigravity:** Tương thích (lưu ý một số ví dụ CLI gọi `claude`, khi dùng trong Antigravity chỉ cần dùng phần hướng dẫn thiết kế `SKILL.md`, evals và tối ưu `description`).
- **Chức năng:** Chuẩn hóa cấu trúc khi xây dựng `study-docx-builder`, thiết kế test prompts (evals) kiểm tra xem Skill có tạo đúng cấu trúc Bài học/Chương và đúng định dạng DOCX không.
- **Giấy phép:** **Apache 2.0**.
- **Điểm đánh giá:** **4.5/5** — **Chọn dùng ở giai đoạn xây dựng Skill điều phối**.

---

### Nhóm D — Hỗ trợ ôn tập & Khảo sát mở rộng

#### 2.11. `sickn33/agentic-awesome-skills` — `examprep-ai`
- **Liên kết GitHub:** https://github.com/sickn33/agentic-awesome-skills/blob/main/skills/examprep-ai/SKILL.md
- **Tồn tại & truy cập:** Có.
- **SKILL.md hợp lệ:** Có (459 dòng, frontmatter đầy đủ).
- **Tương thích Google Antigravity:** Tương thích.
- **Chức năng:** Phân tích đề cương/tài liệu theo mức độ Dễ → Trung bình → Khó, hỗ trợ câu hỏi lý thuyết, tính toán, MCQ, Đúng/Sai và có *Syllabus Guardrail* (ánh xạ mọi câu hỏi vào đúng đơn vị kiến thức nguồn).
- **Hạn chế:** Tập trung vào sinh viên ôn thi cấp tốc (Emergency/Sprint mode), xuất Markdown trong chat, không có chuẩn GDPT 2018 (mục Ý nghĩa thực tiễn, câu Đúng/Sai 4 nhận định kiểu thi THPT 2025+), không xuất DOCX.
- **Giấy phép:** **MIT**.
- **Phù hợp Windows:** Tốt.
- **Điểm đánh giá:** **3.0/5** — **Không cài nguyên bản, kế thừa cơ chế Syllabus Guardrail & phân hóa nhận thức vào `study-docx-builder`**.

#### 2.12. Các Skills mở rộng đã khảo sát thêm
1. **`github/awesome-copilot` (`md-to-docx`)** — https://github.com/github/awesome-copilot/blob/HEAD/skills/md-to-docx/SKILL.md
   - *Ưu điểm:* Pure JS (`docx` + `marked`), không cần Pandoc/LibreOffice, MIT license.
   - *Hạn chế:* Chuyển đổi thụ động từ Markdown sang DOCX nên rất khó kiểm soát tinh vi Word Styles tiếng Việt, chỉ số trên/dưới Hóa học trong bảng/phương trình, Word Equation (OMML) cho Toán–Lý, và thiếu bộ `validate.py` kiểm tra XSD. -> **Loại (3.0/5)** vì `anthropics/skills/docx` mạnh hơn toàn diện.
2. **`ndpvt-web/latex-document-skill`** — https://github.com/ndpvt-web/latex-document-skill
   - *Hạn chế:* Không có License, chuyên xuất LaTeX/PDF, không phục vụ mục tiêu xuất file Word `.docx` để giáo viên chỉnh sửa. -> **Loại (2.0/5)**.

---

## 3. ĐÁNH GIÁ KHOẢNG TRỐNG ĐỐI CHIẾU VỚI YÊU CẦU BỔ SUNG

Khi đối chiếu tất cả Skills công khai trên GitHub với **8 năng lực bắt buộc trong phần Bổ sung yêu cầu**, thực tế khảo sát cho thấy:

| Năng lực yêu cầu | Skills GitHub có sẵn đáp ứng được? | Mức độ đáp ứng |
| :--- | :--- | :---: |
| 1. Tự động xác định cấu trúc chương và bài học | `docling` + `pdf` trích xuất được mục lục/heading, nhưng chưa tự phân tách theo SGK GDPT 2018 | Trung bình (60%) |
| 2. Tạo ví dụ minh họa phù hợp từng đề mục | Chưa có Skill nào bắt buộc mỗi đề mục phải có ví dụ gắn thực tiễn THPT VN | Thấp (20%) |
| 3. Tạo câu hỏi MCQ theo ma trận (2 NB - 2 TH - 1 VD / 15 câu chương) | `examprep-ai` có ý tưởng phân hóa, nhưng chưa có ma trận chuẩn GDPT 2018 | Thấp (30%) |
| 4. Tạo câu hỏi Đúng/Sai gồm 4 nhận định a, b, c, d | **Không có Skill GitHub nào** hỗ trợ đúng format thi THPT mới của Việt Nam | Rất thấp (0%) |
| 5. Kiểm tra đáp án và lời giải (đặc biệt Hóa học: PTPU, mol, ion) | **Không có Skill GitHub nào** kiểm tra logic sư phạm & hóa học THPT | Rất thấp (0%) |
| 6. Định dạng câu hỏi trong Word (A, B, C, D gọn đẹp, không vỡ trang) | `anthropics/docx` làm tốt ở tầng kỹ thuật `docx-js`, cần mẫu bố cục riêng | Trung bình (50%) |
| 7. Tạo bảng đáp án rõ ràng cuối tài liệu | `anthropics/docx` hỗ trợ bảng DXA chuẩn, cần template bảng đáp án | Trung bình (50%) |
| 8. Tạo tài liệu theo Bài (Chế độ A) & tổng hợp Chương (Chế độ B) | **Chưa có**, cần thiết kế riêng trong Skill điều phối | Rất thấp (0%) |

**Kết luận quan trọng:** Không thể chỉ ghép các Skills GitHub có sẵn mà chạy được ngay. Chiến lược tối ưu nhất là chọn lọc **các Skills hạ tầng tốt nhất** (`docling`, `pdf`, `pptx` có sẵn, `docx`, `skill-creator`) và **tự xây dựng Skill điều phối chuyên biệt `study-docx-builder`** để lấp đầy toàn bộ 8 khoảng trống sư phạm và chuẩn hóa DOCX cho giáo dục THPT Việt Nam.
