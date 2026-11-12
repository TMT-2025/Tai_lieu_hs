# THIẾT KẾ QUY TRÌNH BIÊN SOẠN & KIẾN TRÚC HỆ THỐNG DOCX

> **Dự án:** AI STUDY DOCUMENT STUDIO  
> **Đối tượng phục vụ:** Giáo viên THPT Việt Nam tạo tài liệu Word (`.docx`) cho học sinh tự học (ưu tiên Hóa học 10–11–12 theo Chương trình GDPT 2018; mở rộng sang Toán, Vật lí, Sinh học, Ngữ văn, Lịch sử, Địa lí).

---

## 1. HAI CHẾ ĐỘ BIÊN SOẠN & QUY TRÌNH 10 BƯỚC TỐI ƯU

Hệ thống hỗ trợ 2 chế độ đầu vào/đầu ra rõ ràng:
- **Chế độ A — Tài liệu ôn tập theo Bài học:** Chọn Môn học, Khối lớp, Bộ sách giáo khoa (KNTT, CTST, Cánh Diều), Chương, Bài học → Xuất 1 file DOCX riêng cho bài học đó.
- **Chế độ B — Tài liệu tổng hợp ôn tập theo Chương:** Chọn Môn học, Khối lớp, Bộ sách, Chương → Tổng hợp toàn bộ các bài trong chương, làm rõ mối liên hệ, tránh lặp lại, có bảng tổng hợp/so sánh → Xuất 1 file DOCX ôn tập chương.

### Quy trình xử lý 10 bước (Tối ưu tốc độ & chất lượng)

```
[Tài liệu nguồn: PDF / DOCX / PPTX / Text]
        │
        ▼
BƯỚC 1: Đọc & trích xuất tài liệu nguồn (pdf cắt trang → docling / markitdown → Markdown sạch)
        │
        ▼
BƯỚC 2: Phân tích cấu trúc Chương / Bài & Yêu cầu cần đạt (GDPT 2018)
        │
        ▼
BƯỚC 3: Xác định nội dung trọng tâm (theo Chế độ A: 1 bài | Chế độ B: liên kết cả chương)
        │
        ▼
BƯỚC 4: Tóm tắt & hệ thống hóa kiến thức (ngắn gọn, súc tích, không chép nguyên văn SGK)
        │
        ▼
BƯỚC 5: Sinh Ý nghĩa thực tiễn + Ví dụ từng mục + Bảng so sánh + Ma trận câu hỏi (MCQ & Đúng/Sai)
        │
        ▼
BƯỚC 6: Kiểm tra kiến thức, công thức Hóa/Toán/Lý, tính toán & đáp án (1 vòng kiểm tra tập trung)
        │
        ▼
BƯỚC 7: Biên tập ngôn ngữ sư phạm (dễ hiểu cho học sinh THPT tự học, nhất quán thuật ngữ)
        │
        ▼
BƯỚC 8: Tạo file DOCX theo mẫu chuẩn (docx-js + Word Styles + OMML/Sub-Superscript)
        │
        ▼
BƯỚC 9: Kiểm tra kỹ thuật DOCX (validate.py XSD + kiểm tra bảng tràn lề, ngắt công thức)
        │
        ▼
BƯỚC 10: Xuất file Word (.docx) hoàn chỉnh sẵn sàng chỉnh sửa và in ấn
```

> **Tối ưu quy trình:** Gộp kiểm tra khoa học (Hóa/Toán) và đáp án ngay tại **Bước 6** bằng checklist có cấu trúc thay vì tạo nhiều tầng agent phản biện qua lại gây chậm và tốn token.

---

## 2. CẤU TRÚC TÀI LIỆU ÔN TẬP CHUẨN

### 2.1. Chế độ A — Cấu trúc bắt buộc cho Tài liệu theo Bài học

1. **TÊN BÀI HỌC** *(Style: `Title`, 16pt, Đậm)*
2. **A. MỤC TIÊU BÀI HỌC** *(Style: `Heading 1`)*
   - Kiến thức cần nắm.
   - Kỹ năng cần đạt.
   - Vấn đề học sinh cần giải thích hoặc vận dụng được.
3. **B. Ý NGHĨA THỰC TIỄN** *(Bắt buộc — Style: `Heading 1`)*
   - Ứng dụng trong đời sống, sản xuất, khoa học, công nghệ (ưu tiên ví dụ gần gũi tại Việt Nam, có cơ sở khoa học, không khiên cưỡng).
4. **C. KIẾN THỨC TRỌNG TÂM** *(Style: `Heading 1`)*
   - Phân chia rõ: **I, II, III...** *(Style: `Heading 2`)*.
   - **Mỗi đề mục bắt buộc có đủ 5 thành phần:**
     1. Nội dung kiến thức cốt lõi.
     2. Giải thích ngắn gọn, dễ hiểu.
     3. Công thức, quy tắc hoặc định nghĩa quan trọng (nếu có).
     4. **Ít nhất 01 ví dụ minh họa** bám sát mục vừa trình bày (bài tính toán phải có hướng dẫn giải từng bước).
     5. Lưu ý / điểm dễ nhầm lẫn (nếu có).
5. **D. HỆ THỐNG HÓA KIẾN THỨC** *(Style: `Heading 1`)*
   - Lựa chọn linh hoạt: Bảng so sánh, Bảng tổng hợp, Sơ đồ kiến thức (nếu phù hợp), Quy tắc ghi nhớ, Lỗi thường gặp.
6. **E. CÂU HỎI TỰ KIỂM TRA** *(Style: `Heading 1` — Không lộ đáp án)*
   - **PHẦN I — 5 CÂU TRẮC NGHIỆM MCQ** *(Style: `Heading 2`)*: 4 phương án A, B, C, D; 1 đáp án đúng duy nhất. Phân bố mặc định: **2 Nhận biết – 2 Thông hiểu – 1 Vận dụng**.
   - **PHẦN II — 2 CÂU TRẮC NGHIỆM ĐÚNG/SAI** *(Style: `Heading 2`)*: Mỗi câu có đoạn dẫn/tình huống phù hợp + **4 nhận định a), b), c), d)** xác định Đúng/Sai độc lập, kiểm tra bản chất & thực tiễn.
7. **F. ĐÁP ÁN VÀ GIẢI THÍCH** *(Style: `Heading 1` — Đặt cuối tài liệu)*
   - Bảng tổng hợp đáp án 5 MCQ + 8 nhận định Đúng/Sai.
   - Giải thích ngắn gọn từng câu MCQ, từng nhận định Đúng/Sai và lời giải chi tiết bài tính toán.

### 2.2. Chế độ B — Cấu trúc Tài liệu Ôn tập theo Chương

1. **A. MỤC TIÊU ÔN TẬP CHƯƠNG**
2. **B. Ý NGHĨA THỰC TIỄN VÀ ỨNG DỤNG CỦA KIẾN THỨC TRONG CHƯƠNG**
3. **C. HỆ THỐNG KIẾN THỨC TRỌNG TÂM THEO BÀI / CHỦ ĐỀ** *(làm rõ liên kết giữa các bài, tránh lặp)*
4. **D. BẢNG TỔNG HỢP, SO SÁNH VÀ LIÊN HỆ KIẾN THỨC**
5. **E. VÍ DỤ MINH HỌA TỔNG HỢP**
6. **F. CÁC DẠNG BÀI TẬP THƯỜNG GẶP VÀ PHƯƠNG PHÁP GIẢI**
7. **G. CÂU HỎI TỰ KIỂM TRA** *(Mặc định: **15 câu MCQ** + **5 câu Đúng/Sai × 4 nhận định**; cho phép giáo viên tùy chỉnh số lượng; bao quát đều các bài trong chương)*
8. **H. ĐÁP ÁN VÀ HƯỚNG DẪN GIẢI** *(Đặt cuối tài liệu)*

### 2.3. Quy trình 8 bước bắt buộc khi AI tạo câu hỏi

1. Xác định nội dung trọng tâm từ nguồn đã phân tích (tuyệt đối bám sát nguồn).
2. Lập **Ma trận câu hỏi** (Đơn vị kiến thức × Mức độ nhận thức × Loại câu hỏi).
3. Sinh câu hỏi theo đúng ma trận.
4. Tạo đáp án và lời giải/giải thích chi tiết.
5. **Kiểm tra tính chính xác:** Với Hóa học bắt buộc kiểm tra công thức hóa học, cân bằng phương trình, kết quả tính toán, đảm bảo không có 2 phương án nhiễu cùng đúng.
6. Kiểm tra mức độ nhận thức (tránh câu nhận biết quá lắt léo hoặc câu vận dụng không đủ dữ kiện).
7. Loại bỏ câu hỏi trùng lặp ý.
8. Đưa vào cấu trúc DOCX chuẩn.

---

## 3. QUY CHUẨN ĐỊNH DẠNG FILE WORD (`.docx`)

| Thông số | Quy chuẩn mặc định | Cách thực hiện trong `docx-js` / OOXML |
| :--- | :--- | :--- |
| **Khổ giấy** | A4 (`210 × 297 mm`) | `width: 11906, height: 16838` (DXA) |
| **Lề trang** | Trái `2.5 cm`, Phải/Trên/Dưới `2.0 cm` | `left: 1417`, `right/top/bottom: 1134` (DXA) |
| **Font chữ** | `Times New Roman` toàn tài liệu | Cấu hình trong `styles.default.document.run.font` |
| **Cỡ chữ & Giãn dòng** | Nội dung `12 pt` (hoặc `13 pt`), giãn dòng `1.15`, căn đều 2 lề (`JUSTIFIED`) | `size: 24` (half-pt), `line: 276`, `spacing.after: 120` |
| **Word Styles thực sự** | `Title` (16pt, Đậm), `Heading 1` (14pt, Đậm), `Heading 2` (13pt, Đậm), `Heading 3` (12pt, Đậm), `Normal` | Khai báo `styles.paragraphStyles` + `outlineLevel` (0, 1, 2) để hỗ trợ Navigation Pane & TOC |
| **Bảng biểu** | Rõ ràng, không tràn lề (`9355 DXA` vùng khả dụng), lặp tiêu đề bảng khi qua trang | `WidthType.DXA`, set `columnWidths` + `cell.width`, `cantSplit: true`, `tableHeader: true` |
| **Header / Footer / Số trang** | Có số trang ở Footer; Header ghi tên bài/chương (ẩn ở trang đầu nếu cần) | `PageNumber.CURRENT` trong Footer |
| **Mục lục tự động (TOC)** | Bật cho tài liệu dài (đặc biệt Chế độ B — Ôn tập chương) | `TableOfContents` đọc từ `Heading 1–3` |
| **Hóa học** | Chỉ số dưới (`H₂O`), chỉ số trên & điện tích ion (`Fe³⁺`, `SO₄²⁻`), PTPU rõ ràng, không ngắt dòng giữa công thức | `TextRun({ subScript: true / superScript: true })`; dùng Non-breaking space (`\u00A0`) hoặc `keepNext`/`cantSplit` hợp lý để tránh gãy công thức |
| **Toán & Vật lí** | Công thức **Word Equation (OMML)** chỉnh sửa được, không biến thành ảnh nếu không cần | Chuyển LaTeX → MathML → OMML (qua XSLT chuẩn) và nhúng `<m:oMath>` vào `word/document.xml` |

---

## 4. KIẾN TRÚC TÍCH HỢP AI API (ĐA NHÀ CUNG CẤP)

Hệ thống sử dụng lớp trừu tượng **`LLMProviderAdapter`** để giáo viên/nhà phát triển có thể chuyển đổi linh hoạt giữa **Google Gemini API** và **OpenAI API** qua file cấu hình (`.env`), **không hardcode API key**.

### 4.1. Phân tầng Model theo tác vụ

| Tác vụ | Yêu cầu kỹ thuật | Gợi ý nhóm Model Gemini | Gợi ý nhóm Model OpenAI |
| :--- | :--- | :--- | :--- |
| **Đọc tài liệu dài & Phân tách chương/bài** | Context window lớn (128k–1M+ tokens), chi phí thấp | Gemini Flash / Pro (bản mới nhất hỗ trợ ngữ cảnh dài) | GPT-4o-mini / GPT-4.1-mini |
| **Tóm tắt, Hệ thống hóa & Sinh câu hỏi theo ma trận** | Structured Output (JSON Schema ổn định), tuân thủ chỉ dẫn chặt | Gemini Pro / Flash (chế độ JSON Schema) | GPT-4o / GPT-4.1 |
| **Kiểm tra công thức Hóa–Toán–Lý, Đáp án & Biên tập** | Suy luận logic/tính toán chính xác cao | Gemini Pro (bật Reasoning/Thinking nếu cần) | o3-mini / GPT-4.1 |

### 4.2. Quản lý cấu hình & Bảo mật API Key
- Toàn bộ key lưu trong biến môi trường: `GEMINI_API_KEY`, `OPENAI_API_KEY`, `DEFAULT_LLM_PROVIDER=gemini|openai`, `MODEL_EXTRACTOR`, `MODEL_WRITER`, `MODEL_VERIFIER`.
- File `.env` nằm trong `.gitignore`, tuyệt đối không đưa vào mã nguồn, prompt hoặc file báo cáo.

---

## 5. THIẾT KẾ CẤU TRÚC SKILL ĐIỀU PHỐI `study-docx-builder`

```text
.agents/skills/study-docx-builder/
├── SKILL.md                          # Hướng dẫn điều phối 10 bước, kích hoạt Chế độ A/B
├── references/
│   ├── cau_truc_bai_hoc.md           # Khuôn mẫu Chế độ A (A→F) & phân bố 5 MCQ + 2 Đ/S
│   ├── cau_truc_chuong.md            # Khuôn mẫu Chế độ B (A→H) & phân bố 15 MCQ + 5 Đ/S
│   ├── quy_chuan_hoa_hoc_gdpt2018.md # Quy tắc danh pháp IUPAC, ion, PTPU, kiểm tra tính toán
│   └── quy_chuan_docx_vn.md          # Thông số DXA A4, Times New Roman, Styles, OMML
├── scripts/
│   ├── extract_router.py             # Điều phối pdf (cắt trang) + docling/markitdown
│   ├── validate_study_json.py        # Kiểm tra JSON nội dung đủ mục, đủ 5 MCQ + 2 Đ/S trước khi render
│   ├── build_study_docx.mjs          # Script Node.js (docx-js) tạo file DOCX chuẩn từ JSON
│   └── inject_omml_equations.py      # Chèn công thức Toán/Lý OMML vào DOCX (nếu có LaTeX)
└── templates/
    └── study_schema.json             # JSON Schema chuẩn hóa dữ liệu trung gian giữa AI và DOCX
```

### Cơ chế hoạt động của `study-docx-builder`:
1. **Nhận đầu vào:** Tiếp nhận file nguồn (PDF/DOCX/PPTX/TXT) + thông tin chọn lọc của giáo viên (Môn, Khối, Sách, Chế độ A/B, tên Bài/Chương).
2. **Trích xuất có chọn lọc:** Gọi `extract_router.py` (kết hợp `pdf` cắt trang + `docling`/`pptx`) để lấy đúng phạm vi văn bản nguồn sạch.
3. **Biên soạn & Kiểm tra qua JSON trung gian:** AI sinh dữ liệu tuân thủ `study_schema.json` (tách biệt hoàn toàn **nội dung sư phạm** khỏi **mã định dạng Word**). Sau đó `validate_study_json.py` kiểm tra tự động: đủ mục Ý nghĩa thực tiễn chưa? Mỗi mục C có ví dụ chưa? Đủ chính xác 5 MCQ & 2 Đúng/Sai (mỗi câu 4 ý a,b,c,d) chưa?
4. **Xuất & Xác thực DOCX:** `build_study_docx.mjs` đọc JSON đã kiểm duyệt để dựng `.docx` bằng `docx-js` (dùng Word Styles thực sự, công thức Hóa học sub/superscript chuẩn), chạy `inject_omml_equations.py` nếu có công thức Toán/Lý phức tạp, cuối cùng gọi `validate.py` (từ skill `docx`) xác nhận file không lỗi XSD trước khi bàn giao cho giáo viên.
