import json
from pathlib import Path
from build_kntt_configs import extract_yccd_text, extract_section_yccd


def build_all():
    out_dir = Path("data/configs")
    out_dir.mkdir(parents=True, exist_ok=True)

    y10 = extract_yccd_text("SGK/YEU CAU CAN DAT HOA 10.pdf")
    y11 = extract_yccd_text("SGK/YEU CAU CAN DAT HOA 11.pdf")
    y12 = extract_yccd_text("SGK/YEU CAU CAN DAT HOA 12.pdf")

    configs = [
        # ======================== CTST ========================
        {
            "id": "SGK_HOA_10_CTST",
            "mon_hoc": "Hóa học",
            "khoi_lop": "Lớp 10",
            "bo_sach": "Chân trời sáng tạo",
            "sgk_file": "SGK/SGK HOA 10 CTST.pdf",
            "sbt_file": "SGK/BAI TAP HOA 10 CTST.pdf",
            "sgv_file": "SGK/SGV HOA 10 CTST.pdf",
            "yccd_file": "SGK/YEU CAU CAN DAT HOA 10.pdf",
            "chuong": [
                {
                    "so_chuong": 0,
                    "ten_chuong": "Mở đầu",
                    "trang_bat_dau": 6,
                    "trang_ket_thuc": 12,
                    "bai_hoc": [{"so_bai": 1, "ten_bai": "Nhập môn hoá học", "trang": "6-12"}],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "Nhập môn hoá học", "CẤU TẠO NGUYÊN TỬ"),
                },
                {
                    "so_chuong": 1,
                    "ten_chuong": "Chương 1. Cấu tạo nguyên tử",
                    "trang_bat_dau": 13,
                    "trang_ket_thuc": 34,
                    "bai_hoc": [
                        {"so_bai": 2, "ten_bai": "Thành phần của nguyên tử", "trang": "13-19"},
                        {"so_bai": 3, "ten_bai": "Nguyên tố hoá học", "trang": "20-25"},
                        {"so_bai": 4, "ten_bai": "Cấu trúc lớp vỏ electron của nguyên tử", "trang": "26-34"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "CẤU TẠO NGUYÊN TỬ", "BẢNG TUẦN HOÀN"),
                },
                {
                    "so_chuong": 2,
                    "ten_chuong": "Chương 2. Bảng tuần hoàn các nguyên tố hoá học",
                    "trang_bat_dau": 35,
                    "trang_ket_thuc": 51,
                    "bai_hoc": [
                        {"so_bai": 5, "ten_bai": "Cấu tạo bảng tuần hoàn các nguyên tố hoá học", "trang": "35-42"},
                        {"so_bai": 6, "ten_bai": "Xu hướng biến đổi một số tính chất của nguyên tử các nguyên tố, thành phần và một số tính chất của hợp chất trong một chu kì và nhóm", "trang": "43-48"},
                        {"so_bai": 7, "ten_bai": "Định luật tuần hoàn – Ý nghĩa của bảng tuần hoàn các nguyên tố hoá học", "trang": "49-51"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "BẢNG TUẦN HOÀN CÁC NGUYÊN TỐ HOÁ HỌC", "LIÊN KẾT HOÁ HỌC"),
                },
                {
                    "so_chuong": 3,
                    "ten_chuong": "Chương 3. Liên kết hoá học",
                    "trang_bat_dau": 52,
                    "trang_ket_thuc": 71,
                    "bai_hoc": [
                        {"so_bai": 8, "ten_bai": "Quy tắc octet", "trang": "52-54"},
                        {"so_bai": 9, "ten_bai": "Liên kết ion", "trang": "55-58"},
                        {"so_bai": 10, "ten_bai": "Liên kết cộng hoá trị", "trang": "59-66"},
                        {"so_bai": 11, "ten_bai": "Liên kết hydrogen và tương tác van der Waals", "trang": "67-71"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "LIÊN KẾT HOÁ HỌC", "PHẢN ỨNG OXI HOÁ"),
                },
                {
                    "so_chuong": 4,
                    "ten_chuong": "Chương 4. Phản ứng oxi hoá – khử",
                    "trang_bat_dau": 72,
                    "trang_ket_thuc": 79,
                    "bai_hoc": [
                        {"so_bai": 12, "ten_bai": "Phản ứng oxi hoá – khử và ứng dụng trong cuộc sống", "trang": "72-79"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "PHẢN ỨNG OXI HOÁ – KHỬ", "NĂNG LƯỢNG HOÁ HỌC"),
                },
                {
                    "so_chuong": 5,
                    "ten_chuong": "Chương 5. Năng lượng hoá học",
                    "trang_bat_dau": 80,
                    "trang_ket_thuc": 93,
                    "bai_hoc": [
                        {"so_bai": 13, "ten_bai": "Enthalpy tạo thành và biến thiên enthalpy của phản ứng hoá học", "trang": "80-87"},
                        {"so_bai": 14, "ten_bai": "Tính biến thiên enthalpy của phản ứng hoá học", "trang": "88-93"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "NĂNG LƯỢNG HOÁ HỌC", "TỐC ĐỘ PHẢN ỨNG"),
                },
                {
                    "so_chuong": 6,
                    "ten_chuong": "Chương 6. Tốc độ phản ứng hoá học",
                    "trang_bat_dau": 94,
                    "trang_ket_thuc": 104,
                    "bai_hoc": [
                        {"so_bai": 15, "ten_bai": "Phương trình tốc độ phản ứng và hằng số tốc độ phản ứng", "trang": "94-97"},
                        {"so_bai": 16, "ten_bai": "Các yếu tố ảnh hưởng đến tốc độ phản ứng hoá học", "trang": "98-104"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "TỐC ĐỘ PHẢN ỨNG HOÁ HỌC", "NGUYÊN TỐ NHÓM VIIA"),
                },
                {
                    "so_chuong": 7,
                    "ten_chuong": "Chương 7. Nguyên tố nhóm VIIA – Halogen",
                    "trang_bat_dau": 105,
                    "trang_ket_thuc": 119,
                    "bai_hoc": [
                        {"so_bai": 17, "ten_bai": "Tính chất vật lí và hoá học các đơn chất nhóm VIIA", "trang": "105-113"},
                        {"so_bai": 18, "ten_bai": "Hydrogen halide và một số phản ứng của ion halide", "trang": "114-119"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "NGUYÊN TỐ NHÓM VIIA", None),
                },
            ],
        },
        {
            "id": "SGK_HOA_11_CTST",
            "mon_hoc": "Hóa học",
            "khoi_lop": "Lớp 11",
            "bo_sach": "Chân trời sáng tạo",
            "sgk_file": "SGK/SGK HOA 11 CTST.pdf",
            "sbt_file": "SGK/BAI TAP HOA 11 CTST.pdf",
            "sgv_file": None,
            "yccd_file": "SGK/YEU CAU CAN DAT HOA 11.pdf",
            "chuong": [
                {
                    "so_chuong": 1,
                    "ten_chuong": "Chương 1. Cân bằng hoá học",
                    "trang_bat_dau": 5,
                    "trang_ket_thuc": 19,
                    "bai_hoc": [
                        {"so_bai": 1, "ten_bai": "Khái niệm về cân bằng hoá học", "trang": "5-11"},
                        {"so_bai": 2, "ten_bai": "Cân bằng trong dung dịch nước", "trang": "12-19"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "CÂN BẰNG HOÁ HỌC", "NITROGEN"),
                },
                {
                    "so_chuong": 2,
                    "ten_chuong": "Chương 2. Nitrogen và Sulfur",
                    "trang_bat_dau": 20,
                    "trang_ket_thuc": 45,
                    "bai_hoc": [
                        {"so_bai": 3, "ten_bai": "Đơn chất nitrogen", "trang": "20-23"},
                        {"so_bai": 4, "ten_bai": "Ammonia và một số hợp chất ammonium", "trang": "24-29"},
                        {"so_bai": 5, "ten_bai": "Một số hợp chất với oxygen của nitrogen", "trang": "30-34"},
                        {"so_bai": 6, "ten_bai": "Sulfur và sulfur dioxide", "trang": "35-39"},
                        {"so_bai": 7, "ten_bai": "Sulfuric acid và muối sulfate", "trang": "40-45"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "NITROGEN – SULFUR", "ĐẠI CƯƠNG VỀ HOÁ HỌC HỮU CƠ"),
                },
                {
                    "so_chuong": 3,
                    "ten_chuong": "Chương 3. Đại cương hoá học hữu cơ",
                    "trang_bat_dau": 46,
                    "trang_ket_thuc": 65,
                    "bai_hoc": [
                        {"so_bai": 8, "ten_bai": "Hợp chất hữu cơ và hoá học hữu cơ", "trang": "46-51"},
                        {"so_bai": 9, "ten_bai": "Phương pháp tách và tinh chế hợp chất hữu cơ", "trang": "52-56"},
                        {"so_bai": 10, "ten_bai": "Công thức phân tử hợp chất hữu cơ", "trang": "57-60"},
                        {"so_bai": 11, "ten_bai": "Cấu tạo hoá học hợp chất hữu cơ", "trang": "61-65"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "ĐẠI CƯƠNG VỀ HOÁ HỌC HỮU CƠ", "HYDROCARBON"),
                },
                {
                    "so_chuong": 4,
                    "ten_chuong": "Chương 4. Hydrocarbon",
                    "trang_bat_dau": 66,
                    "trang_ket_thuc": 91,
                    "bai_hoc": [
                        {"so_bai": 12, "ten_bai": "Alkane", "trang": "66-73"},
                        {"so_bai": 13, "ten_bai": "Hydrocarbon không no", "trang": "74-84"},
                        {"so_bai": 14, "ten_bai": "Arene (Hydrocarbon thơm)", "trang": "85-91"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "HYDROCARBON", "DẪN XUẤT HALOGEN"),
                },
                {
                    "so_chuong": 5,
                    "ten_chuong": "Chương 5. Dẫn xuất halogen – Alcohol – Phenol",
                    "trang_bat_dau": 92,
                    "trang_ket_thuc": 114,
                    "bai_hoc": [
                        {"so_bai": 15, "ten_bai": "Dẫn xuất halogen", "trang": "92-98"},
                        {"so_bai": 16, "ten_bai": "Alcohol", "trang": "99-107"},
                        {"so_bai": 17, "ten_bai": "Phenol", "trang": "108-114"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "DẪN XUẤT HALOGEN – ALCOHOL – PHENOL", "HỢP CHẤT CARBONYL"),
                },
                {
                    "so_chuong": 6,
                    "ten_chuong": "Chương 6. Hợp chất carbonyl (Aldehyde – Ketone) – Carboxylic acid",
                    "trang_bat_dau": 115,
                    "trang_ket_thuc": 132,
                    "bai_hoc": [
                        {"so_bai": 18, "ten_bai": "Hợp chất carbonyl", "trang": "115-123"},
                        {"so_bai": 19, "ten_bai": "Carboxylic acid", "trang": "124-132"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "HỢP CHẤT CARBONYL – CARBOXYLIC ACID", None),
                },
            ],
        },
        {
            "id": "SGK_HOA_12_CTST",
            "mon_hoc": "Hóa học",
            "khoi_lop": "Lớp 12",
            "bo_sach": "Chân trời sáng tạo",
            "sgk_file": "SGK/SGK HOA 12 CTST.pdf",
            "sbt_file": "SGK/BAI TAP HOA 12 CTST.pdf",
            "sgv_file": "SGK/SGV HOA 12 CTST.pdf",
            "yccd_file": "SGK/YEU CAU CAN DAT HOA 12.pdf",
            "chuong": [
                {
                    "so_chuong": 1,
                    "ten_chuong": "Chương 1. Ester – Lipid. Xà phòng và chất giặt rửa",
                    "trang_bat_dau": 5,
                    "trang_ket_thuc": 14,
                    "bai_hoc": [
                        {"so_bai": 1, "ten_bai": "Ester – Lipid", "trang": "5-10"},
                        {"so_bai": 2, "ten_bai": "Xà phòng và chất giặt rửa", "trang": "11-14"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "ESTER – LIPID", "CARBOHYDRATE"),
                },
                {
                    "so_chuong": 2,
                    "ten_chuong": "Chương 2. Carbohydrate",
                    "trang_bat_dau": 15,
                    "trang_ket_thuc": 29,
                    "bai_hoc": [
                        {"so_bai": 3, "ten_bai": "Glucose và fructose", "trang": "15-20"},
                        {"so_bai": 4, "ten_bai": "Saccharose và maltose", "trang": "21-23"},
                        {"so_bai": 5, "ten_bai": "Tinh bột và cellulose", "trang": "24-29"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "CARBOHYDRATE", "HỢP CHẤT CHỨA NITROGEN"),
                },
                {
                    "so_chuong": 3,
                    "ten_chuong": "Chương 3. Hợp chất chứa nitrogen",
                    "trang_bat_dau": 30,
                    "trang_ket_thuc": 49,
                    "bai_hoc": [
                        {"so_bai": 6, "ten_bai": "Amine", "trang": "30-38"},
                        {"so_bai": 7, "ten_bai": "Amino acid và peptide", "trang": "39-44"},
                        {"so_bai": 8, "ten_bai": "Protein và enzyme", "trang": "45-49"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "HỢP CHẤT CHỨA NITROGEN", "POLYMER"),
                },
                {
                    "so_chuong": 4,
                    "ten_chuong": "Chương 4. Polymer",
                    "trang_bat_dau": 50,
                    "trang_ket_thuc": 63,
                    "bai_hoc": [
                        {"so_bai": 9, "ten_bai": "Đại cương về polymer", "trang": "50-54"},
                        {"so_bai": 10, "ten_bai": "Chất dẻo và vật liệu composite", "trang": "55-58"},
                        {"so_bai": 11, "ten_bai": "Tơ – Cao su – Keo dán tổng hợp", "trang": "59-63"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "POLYMER", "PIN ĐIỆN VÀ ĐIỆN PHÂN"),
                },
                {
                    "so_chuong": 5,
                    "ten_chuong": "Chương 5. Pin điện và điện phân",
                    "trang_bat_dau": 64,
                    "trang_ket_thuc": 74,
                    "bai_hoc": [
                        {"so_bai": 12, "ten_bai": "Thế điện cực và nguồn điện hoá học", "trang": "64-69"},
                        {"so_bai": 13, "ten_bai": "Điện phân", "trang": "70-74"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "PIN ĐIỆN VÀ ĐIỆN PHÂN", "ĐẠI CƯƠNG VỀ KIM LOẠI"),
                },
                {
                    "so_chuong": 6,
                    "ten_chuong": "Chương 6. Đại cương về kim loại",
                    "trang_bat_dau": 75,
                    "trang_ket_thuc": 90,
                    "bai_hoc": [
                        {"so_bai": 14, "ten_bai": "Đặc điểm cấu tạo và liên kết kim loại. Tính chất kim loại", "trang": "75-80"},
                        {"so_bai": 15, "ten_bai": "Các phương pháp tách kim loại", "trang": "81-84"},
                        {"so_bai": 16, "ten_bai": "Hợp kim – Sự ăn mòn kim loại", "trang": "85-90"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "ĐẠI CƯƠNG VỀ KIM LOẠI", "NGUYÊN TỐ NHÓM IA"),
                },
                {
                    "so_chuong": 7,
                    "ten_chuong": "Chương 7. Nguyên tố nhóm IA và nhóm IIA",
                    "trang_bat_dau": 91,
                    "trang_ket_thuc": 109,
                    "bai_hoc": [
                        {"so_bai": 17, "ten_bai": "Nguyên tố nhóm IA", "trang": "91-99"},
                        {"so_bai": 18, "ten_bai": "Nguyên tố nhóm IIA", "trang": "100-109"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "NGUYÊN TỐ NHÓM IA VÀ NHÓM IIA", "SƠ LƯỢC VỀ DÃY KIM LOẠI CHUYỂN TIẾP"),
                },
                {
                    "so_chuong": 8,
                    "ten_chuong": "Chương 8. Sơ lược về dãy kim loại chuyển tiếp thứ nhất và phức chất",
                    "trang_bat_dau": 110,
                    "trang_ket_thuc": 122,
                    "bai_hoc": [
                        {"so_bai": 19, "ten_bai": "Đại cương về kim loại chuyển tiếp dãy thứ nhất", "trang": "110-114"},
                        {"so_bai": 20, "ten_bai": "Sơ lược về phức chất và sự hình thành phức chất của ion kim loại chuyển tiếp trong dung dịch", "trang": "115-122"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "SƠ LƯỢC VỀ DÃY KIM LOẠI CHUYỂN TIẾP", None),
                },
            ],
        },
        # ======================== CÁNH DIỀU ========================
        {
            "id": "SGK_HOA_10_CANH_DIEU",
            "mon_hoc": "Hóa học",
            "khoi_lop": "Lớp 10",
            "bo_sach": "Cánh Diều",
            "sgk_file": "SGK/SGK HOA 10 CANH DIEU.pdf",
            "sbt_file": "SGK/BAI TAP HOA 10 CANH DIEU.pdf",
            "sgv_file": None,
            "yccd_file": "SGK/YEU CAU CAN DAT HOA 10.pdf",
            "chuong": [
                {
                    "so_chuong": 0,
                    "ten_chuong": "Mở đầu",
                    "trang_bat_dau": 6,
                    "trang_ket_thuc": 10,
                    "bai_hoc": [{"so_bai": 1, "ten_bai": "Nhập môn hoá học", "trang": "6-10"}],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "Nhập môn hoá học", "CẤU TẠO NGUYÊN TỬ"),
                },
                {
                    "so_chuong": 1,
                    "ten_chuong": "Chủ đề 1. Cấu tạo nguyên tử",
                    "trang_bat_dau": 11,
                    "trang_ket_thuc": 30,
                    "bai_hoc": [
                        {"so_bai": 2, "ten_bai": "Thành phần của nguyên tử", "trang": "11-15"},
                        {"so_bai": 3, "ten_bai": "Nguyên tố hoá học", "trang": "16-20"},
                        {"so_bai": 4, "ten_bai": "Mô hình nguyên tử và orbital nguyên tử", "trang": "21-25"},
                        {"so_bai": 5, "ten_bai": "Lớp, phân lớp và cấu hình electron", "trang": "26-30"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "CẤU TẠO NGUYÊN TỬ", "BẢNG TUẦN HOÀN"),
                },
                {
                    "so_chuong": 2,
                    "ten_chuong": "Chủ đề 2. Bảng tuần hoàn các nguyên tố hoá học",
                    "trang_bat_dau": 31,
                    "trang_ket_thuc": 48,
                    "bai_hoc": [
                        {"so_bai": 6, "ten_bai": "Cấu tạo của bảng tuần hoàn các nguyên tố hoá học", "trang": "31-37"},
                        {"so_bai": 7, "ten_bai": "Xu hướng biến đổi tính chất của đơn chất, biến đổi thành phần và tính chất của hợp chất trong một chu kì và trong một nhóm", "trang": "38-45"},
                        {"so_bai": 8, "ten_bai": "Định luật tuần hoàn và ý nghĩa của bảng tuần hoàn các nguyên tố hoá học", "trang": "46-48"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "BẢNG TUẦN HOÀN CÁC NGUYÊN TỐ HOÁ HỌC", "LIÊN KẾT HOÁ HỌC"),
                },
                {
                    "so_chuong": 3,
                    "ten_chuong": "Chủ đề 3. Liên kết hoá học",
                    "trang_bat_dau": 49,
                    "trang_ket_thuc": 69,
                    "bai_hoc": [
                        {"so_bai": 9, "ten_bai": "Quy tắc octet", "trang": "49-52"},
                        {"so_bai": 10, "ten_bai": "Liên kết ion", "trang": "53-56"},
                        {"so_bai": 11, "ten_bai": "Liên kết cộng hoá trị", "trang": "57-63"},
                        {"so_bai": 12, "ten_bai": "Liên kết hydrogen và tương tác van der Waals", "trang": "64-69"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "LIÊN KẾT HOÁ HỌC", "PHẢN ỨNG OXI HOÁ"),
                },
                {
                    "so_chuong": 4,
                    "ten_chuong": "Chủ đề 4. Phản ứng oxi – hoá khử",
                    "trang_bat_dau": 70,
                    "trang_ket_thuc": 76,
                    "bai_hoc": [
                        {"so_bai": 13, "ten_bai": "Phản ứng oxi hoá – khử", "trang": "70-76"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "PHẢN ỨNG OXI HOÁ – KHỬ", "NĂNG LƯỢNG HOÁ HỌC"),
                },
                {
                    "so_chuong": 5,
                    "ten_chuong": "Chủ đề 5. Năng lượng hoá học",
                    "trang_bat_dau": 77,
                    "trang_ket_thuc": 87,
                    "bai_hoc": [
                        {"so_bai": 14, "ten_bai": "Phản ứng hoá học và enthalpy", "trang": "77-81"},
                        {"so_bai": 15, "ten_bai": "Ý nghĩa và cách tính biến thiên enthalpy phản ứng hoá học", "trang": "82-87"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "NĂNG LƯỢNG HOÁ HỌC", "TỐC ĐỘ PHẢN ỨNG"),
                },
                {
                    "so_chuong": 6,
                    "ten_chuong": "Chủ đề 6. Tốc độ phản ứng hoá học",
                    "trang_bat_dau": 88,
                    "trang_ket_thuc": 98,
                    "bai_hoc": [
                        {"so_bai": 16, "ten_bai": "Tốc độ phản ứng hoá học", "trang": "88-98"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "TỐC ĐỘ PHẢN ỨNG HOÁ HỌC", "NGUYÊN TỐ NHÓM VIIA"),
                },
                {
                    "so_chuong": 7,
                    "ten_chuong": "Chủ đề 7. Nguyên tố nhóm VIIA (Nhóm halogen)",
                    "trang_bat_dau": 99,
                    "trang_ket_thuc": 114,
                    "bai_hoc": [
                        {"so_bai": 17, "ten_bai": "Nguyên tố và đơn chất halogen", "trang": "99-108"},
                        {"so_bai": 18, "ten_bai": "Hydrogen halide và hydrohalic acid", "trang": "109-114"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y10, "NGUYÊN TỐ NHÓM VIIA", None),
                },
            ],
        },
        {
            "id": "SGK_HOA_11_CANH_DIEU",
            "mon_hoc": "Hóa học",
            "khoi_lop": "Lớp 11",
            "bo_sach": "Cánh Diều",
            "sgk_file": "SGK/SGK HOA 11 CANH DIEU.pdf",
            "sbt_file": "SGK/BAI TAP HOA 11 CANH DIEU.pdf",
            "sgv_file": None,
            "yccd_file": "SGK/YEU CAU CAN DAT HOA 11.pdf",
            "chuong": [
                {
                    "so_chuong": 1,
                    "ten_chuong": "Chủ đề 1. Cân bằng hoá học",
                    "trang_bat_dau": 6,
                    "trang_ket_thuc": 25,
                    "bai_hoc": [
                        {"so_bai": 1, "ten_bai": "Mở đầu về cân bằng hoá học", "trang": "6-14"},
                        {"so_bai": 2, "ten_bai": "Sự điện li, thuyết Bronsted – Lowry về acid – base", "trang": "15-19"},
                        {"so_bai": 3, "ten_bai": "pH của dung dịch – chuẩn độ acid và base", "trang": "20-25"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "CÂN BẰNG HOÁ HỌC", "NITROGEN"),
                },
                {
                    "so_chuong": 2,
                    "ten_chuong": "Chủ đề 2. Nitrogen và Sulfur",
                    "trang_bat_dau": 26,
                    "trang_ket_thuc": 50,
                    "bai_hoc": [
                        {"so_bai": 4, "ten_bai": "Đơn chất nitrogen", "trang": "26-29"},
                        {"so_bai": 5, "ten_bai": "Một số hợp chất quan trọng của nitrogen", "trang": "30-38"},
                        {"so_bai": 6, "ten_bai": "Sulfur và sulfur dioxide", "trang": "39-43"},
                        {"so_bai": 7, "ten_bai": "Sulfuric acid và muối sulfate", "trang": "44-50"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "NITROGEN – SULFUR", "ĐẠI CƯƠNG VỀ HOÁ HỌC HỮU CƠ"),
                },
                {
                    "so_chuong": 3,
                    "ten_chuong": "Chủ đề 3. Đại cương hoá học hữu cơ",
                    "trang_bat_dau": 51,
                    "trang_ket_thuc": 71,
                    "bai_hoc": [
                        {"so_bai": 8, "ten_bai": "Hợp chất hữu cơ và hoá học hữu cơ", "trang": "51-56"},
                        {"so_bai": 9, "ten_bai": "Phương pháp tách biệt và tinh chế hợp chất hữu cơ", "trang": "57-62"},
                        {"so_bai": 10, "ten_bai": "Công thức phân tử hợp chất hữu cơ", "trang": "63-66"},
                        {"so_bai": 11, "ten_bai": "Cấu tạo hợp chất hữu cơ", "trang": "67-71"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "ĐẠI CƯƠNG VỀ HOÁ HỌC HỮU CƠ", "HYDROCARBON"),
                },
                {
                    "so_chuong": 4,
                    "ten_chuong": "Chủ đề 4. Hydrocarbon",
                    "trang_bat_dau": 72,
                    "trang_ket_thuc": 99,
                    "bai_hoc": [
                        {"so_bai": 12, "ten_bai": "Alkane", "trang": "72-80"},
                        {"so_bai": 13, "ten_bai": "Hydrocarbon không no", "trang": "81-91"},
                        {"so_bai": 14, "ten_bai": "Arene", "trang": "92-99"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "HYDROCARBON", "DẪN XUẤT HALOGEN"),
                },
                {
                    "so_chuong": 5,
                    "ten_chuong": "Chủ đề 5. Dẫn xuất halogen – Alcohol – Phenol",
                    "trang_bat_dau": 100,
                    "trang_ket_thuc": 121,
                    "bai_hoc": [
                        {"so_bai": 15, "ten_bai": "Dẫn xuất halogen", "trang": "100-106"},
                        {"so_bai": 16, "ten_bai": "Alcohol", "trang": "107-115"},
                        {"so_bai": 17, "ten_bai": "Phenol", "trang": "116-121"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "DẪN XUẤT HALOGEN – ALCOHOL – PHENOL", "HỢP CHẤT CARBONYL"),
                },
                {
                    "so_chuong": 6,
                    "ten_chuong": "Chủ đề 6. Hợp chất carbonyl (Aldehyde – Ketone) – Carboxylic acid",
                    "trang_bat_dau": 122,
                    "trang_ket_thuc": 139,
                    "bai_hoc": [
                        {"so_bai": 18, "ten_bai": "Hợp chất carbonyl", "trang": "122-131"},
                        {"so_bai": 19, "ten_bai": "Carboxylic acid", "trang": "132-139"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y11, "HỢP CHẤT CARBONYL – CARBOXYLIC ACID", None),
                },
            ],
        },
        {
            "id": "SGK_HOA_12_CANH_DIEU",
            "mon_hoc": "Hóa học",
            "khoi_lop": "Lớp 12",
            "bo_sach": "Cánh Diều",
            "sgk_file": "SGK/SGK HOA 12 CANH DIEU.pdf",
            "sbt_file": "SGK/BAI TAP HOA 12 CANH DIEU.pdf",
            "sgv_file": "SGK/SGV HOA 12 CANH DIEU.pdf",
            "yccd_file": "SGK/YEU CAU CAN DAT HOA 12.pdf",
            "chuong": [
                {
                    "so_chuong": 1,
                    "ten_chuong": "Chủ đề 1. Ester – Lipid",
                    "trang_bat_dau": 6,
                    "trang_ket_thuc": 19,
                    "bai_hoc": [
                        {"so_bai": 1, "ten_bai": "Ester – Lipid", "trang": "6-13"},
                        {"so_bai": 2, "ten_bai": "Xà phòng và chất giặt rửa tổng hợp", "trang": "14-19"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "ESTER – LIPID", "CARBOHYDRATE"),
                },
                {
                    "so_chuong": 2,
                    "ten_chuong": "Chủ đề 2. Carbohydrate",
                    "trang_bat_dau": 20,
                    "trang_ket_thuc": 34,
                    "bai_hoc": [
                        {"so_bai": 3, "ten_bai": "Giới thiệu về carbohydrate", "trang": "20-26"},
                        {"so_bai": 4, "ten_bai": "Tính chất hoá học của carbohydrate", "trang": "27-34"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "CARBOHYDRATE", "HỢP CHẤT CHỨA NITROGEN"),
                },
                {
                    "so_chuong": 3,
                    "ten_chuong": "Chủ đề 3. Hợp chất chứa nitrogen",
                    "trang_bat_dau": 35,
                    "trang_ket_thuc": 53,
                    "bai_hoc": [
                        {"so_bai": 5, "ten_bai": "Amine", "trang": "35-41"},
                        {"so_bai": 6, "ten_bai": "Amino acid", "trang": "42-46"},
                        {"so_bai": 7, "ten_bai": "Peptide, protein và enzyme", "trang": "47-53"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "HỢP CHẤT CHỨA NITROGEN", "POLYMER"),
                },
                {
                    "so_chuong": 4,
                    "ten_chuong": "Chủ đề 4. Polymer",
                    "trang_bat_dau": 54,
                    "trang_ket_thuc": 69,
                    "bai_hoc": [
                        {"so_bai": 8, "ten_bai": "Đại cương về polymer", "trang": "54-59"},
                        {"so_bai": 9, "ten_bai": "Vật liệu polymer", "trang": "60-69"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "POLYMER", "PIN ĐIỆN VÀ ĐIỆN PHÂN"),
                },
                {
                    "so_chuong": 5,
                    "ten_chuong": "Chủ đề 5. Pin điện và điện phân",
                    "trang_bat_dau": 70,
                    "trang_ket_thuc": 88,
                    "bai_hoc": [
                        {"so_bai": 10, "ten_bai": "Thế điện cực chuẩn của kim loại", "trang": "70-75"},
                        {"so_bai": 11, "ten_bai": "Nguồn điện hoá học", "trang": "76-82"},
                        {"so_bai": 12, "ten_bai": "Điện phân", "trang": "83-88"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "PIN ĐIỆN VÀ ĐIỆN PHÂN", "ĐẠI CƯƠNG VỀ KIM LOẠI"),
                },
                {
                    "so_chuong": 6,
                    "ten_chuong": "Chủ đề 6. Đại cương về kim loại",
                    "trang_bat_dau": 89,
                    "trang_ket_thuc": 112,
                    "bai_hoc": [
                        {"so_bai": 13, "ten_bai": "Cấu tạo và tính chất vật lí của kim loại", "trang": "89-94"},
                        {"so_bai": 14, "ten_bai": "Tính chất hoá học của kim loại", "trang": "95-99"},
                        {"so_bai": 15, "ten_bai": "Tách kim loại và tái chế kim loại", "trang": "100-104"},
                        {"so_bai": 16, "ten_bai": "Hợp kim – Sự ăn mòn kim loại", "trang": "105-112"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "ĐẠI CƯƠNG VỀ KIM LOẠI", "NGUYÊN TỐ NHÓM IA"),
                },
                {
                    "so_chuong": 7,
                    "ten_chuong": "Chủ đề 7. Nguyên tố nhóm IA và nhóm IIA",
                    "trang_bat_dau": 113,
                    "trang_ket_thuc": 134,
                    "bai_hoc": [
                        {"so_bai": 17, "ten_bai": "Nguyên tố nhóm IA", "trang": "113-120"},
                        {"so_bai": 18, "ten_bai": "Nguyên tố nhóm IIA", "trang": "121-130"},
                        {"so_bai": 19, "ten_bai": "Nước cứng và làm mềm nước cứng", "trang": "131-134"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "NGUYÊN TỐ NHÓM IA VÀ NHÓM IIA", "SƠ LƯỢC VỀ DÃY KIM LOẠI CHUYỂN TIẾP"),
                },
                {
                    "so_chuong": 8,
                    "ten_chuong": "Chủ đề 8. Sơ lược về kim loại chuyển tiếp dãy thứ nhất và phức chất",
                    "trang_bat_dau": 135,
                    "trang_ket_thuc": 150,
                    "bai_hoc": [
                        {"so_bai": 20, "ten_bai": "Sơ lược về kim loại chuyển tiếp dãy thứ nhất", "trang": "135-141"},
                        {"so_bai": 21, "ten_bai": "Sơ lược về phức chất", "trang": "142-145"},
                        {"so_bai": 22, "ten_bai": "Sơ lược về sự hình thành phức chất của ion kim loại chuyển tiếp trong dung dịch", "trang": "146-150"},
                    ],
                    "yeu_cau_can_dat": extract_section_yccd(y12, "SƠ LƯỢC VỀ DÃY KIM LOẠI CHUYỂN TIẾP", None),
                },
            ],
        },
    ]

    for cfg in configs:
        p = out_dir / f"{cfg['id']}.json"
        p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        total_lessons = sum(len(c["bai_hoc"]) for c in cfg["chuong"])
        total_yccd = sum(len(c["yeu_cau_can_dat"]) for c in cfg["chuong"])
        print(f"Saved {p} | chapters={len(cfg['chuong'])} | lessons={total_lessons} | yccd_items={total_yccd}")


if __name__ == "__main__":
    build_all()
