import json
import re
from pathlib import Path
import pymupdf


def extract_yccd_text(pdf_path: str) -> str:
    doc = pymupdf.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    # Stop before CHUYÊN ĐỀ HỌC TẬP so core textbook chapters stay clean
    idx = text.find("CHUYÊN ĐỀ HỌC TẬP")
    return text[:idx] if idx != -1 else text


def extract_section_yccd(full_text: str, start_marker: str, end_marker: str | None) -> list[str]:
    s_idx = full_text.lower().find(start_marker.lower())
    if s_idx == -1:
        return []
    sub = full_text[s_idx:]
    if end_marker:
        e_idx = sub.lower().find(end_marker.lower(), len(start_marker))
        if e_idx != -1:
            sub = sub[:e_idx]
    # Group bullet lines starting with – or -
    items = []
    cur = ""
    for line in sub.splitlines():
        line = line.strip()
        if not line or line in {"Nội dung", "Yêu cầu cần đạt"}:
            continue
        if line.startswith(("–", "-", "•")):
            if cur:
                items.append(cur)
            cur = line.lstrip("–-• ").strip()
        elif cur:
            cur += " " + line
    if cur:
        items.append(cur)
    return items


def build_configs():
    out_dir = Path("data/configs")
    out_dir.mkdir(parents=True, exist_ok=True)

    y10 = extract_yccd_text("SGK/YEU CAU CAN DAT HOA 10.pdf")
    y11 = extract_yccd_text("SGK/YEU CAU CAN DAT HOA 11.pdf")
    y12 = extract_yccd_text("SGK/YEU CAU CAN DAT HOA 12.pdf")

    cfg_10 = {
        "id": "SGK_HOA_10_KNTT",
        "mon_hoc": "Hóa học",
        "khoi_lop": "Lớp 10",
        "bo_sach": "Kết nối tri thức với cuộc sống",
        "sgk_file": "SGK/SGK HOA 10 KNTT.pdf",
        "sbt_file": "SGK/BAI TAP HOA 10 KNTT.pdf",
        "sgv_file": "SGK/SGV HOA 10 KNTT.pdf",
        "yccd_file": "SGK/YEU CAU CAN DAT HOA 10.pdf",
        "page_offset_pdf_vs_printed": 1,
        "chuong": [
            {
                "so_chuong": 1,
                "ten_chuong": "Chương 1. Cấu tạo nguyên tử",
                "trang_bat_dau": 12,
                "trang_ket_thuc": 27,
                "bai_hoc": [
                    {"so_bai": 1, "ten_bai": "Thành phần của nguyên tử", "trang": "13-16"},
                    {"so_bai": 2, "ten_bai": "Nguyên tố hoá học", "trang": "17-20"},
                    {"so_bai": 3, "ten_bai": "Cấu trúc lớp vỏ electron nguyên tử", "trang": "21-25"},
                    {"so_bai": 4, "ten_bai": "Ôn tập chương 1", "trang": "26-27", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y10, "CẤU TẠO NGUYÊN TỬ", "BẢNG TUẦN HOÀN"),
            },
            {
                "so_chuong": 2,
                "ten_chuong": "Chương 2. Bảng tuần hoàn các nguyên tố hoá học và định luật tuần hoàn",
                "trang_bat_dau": 28,
                "trang_ket_thuc": 47,
                "bai_hoc": [
                    {"so_bai": 5, "ten_bai": "Cấu tạo của bảng tuần hoàn các nguyên tố hoá học", "trang": "30-33"},
                    {"so_bai": 6, "ten_bai": "Xu hướng biến đổi một số tính chất của nguyên tử các nguyên tố trong một chu kì và trong một nhóm", "trang": "34-39"},
                    {"so_bai": 7, "ten_bai": "Xu hướng biến đổi thành phần và một số tính chất của hợp chất trong một chu kì", "trang": "40-42"},
                    {"so_bai": 8, "ten_bai": "Định luật tuần hoàn. Ý nghĩa của bảng tuần hoàn các nguyên tố hoá học", "trang": "43-44"},
                    {"so_bai": 9, "ten_bai": "Ôn tập chương 2", "trang": "45-47", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y10, "BẢNG TUẦN HOÀN CÁC NGUYÊN TỐ HOÁ HỌC", "LIÊN KẾT HOÁ HỌC"),
            },
            {
                "so_chuong": 3,
                "ten_chuong": "Chương 3. Liên kết hoá học",
                "trang_bat_dau": 48,
                "trang_ket_thuc": 69,
                "bai_hoc": [
                    {"so_bai": 10, "ten_bai": "Quy tắc octet", "trang": "49-50"},
                    {"so_bai": 11, "ten_bai": "Liên kết ion", "trang": "51-54"},
                    {"so_bai": 12, "ten_bai": "Liên kết cộng hoá trị", "trang": "55-63"},
                    {"so_bai": 13, "ten_bai": "Liên kết hydrogen và tương tác van der Waals", "trang": "64-67"},
                    {"so_bai": 14, "ten_bai": "Ôn tập chương 3", "trang": "68-69", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y10, "LIÊN KẾT HOÁ HỌC", "PHẢN ỨNG OXI HOÁ"),
            },
            {
                "so_chuong": 4,
                "ten_chuong": "Chương 4. Phản ứng oxi hoá – khử",
                "trang_bat_dau": 70,
                "trang_ket_thuc": 79,
                "bai_hoc": [
                    {"so_bai": 15, "ten_bai": "Phản ứng oxi hoá – khử", "trang": "71-77"},
                    {"so_bai": 16, "ten_bai": "Ôn tập chương 4", "trang": "78-79", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y10, "PHẢN ỨNG OXI HOÁ – KHỬ", "NĂNG LƯỢNG HOÁ HỌC"),
            },
            {
                "so_chuong": 5,
                "ten_chuong": "Chương 5. Năng lượng hoá học",
                "trang_bat_dau": 80,
                "trang_ket_thuc": 90,
                "bai_hoc": [
                    {"so_bai": 17, "ten_bai": "Biến thiên enthalpy trong các phản ứng hoá học", "trang": "81-88"},
                    {"so_bai": 18, "ten_bai": "Ôn tập chương 5", "trang": "89-90", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y10, "NĂNG LƯỢNG HOÁ HỌC", "TỐC ĐỘ PHẢN ỨNG"),
            },
            {
                "so_chuong": 6,
                "ten_chuong": "Chương 6. Tốc độ phản ứng",
                "trang_bat_dau": 91,
                "trang_ket_thuc": 102,
                "bai_hoc": [
                    {"so_bai": 19, "ten_bai": "Tốc độ phản ứng", "trang": "92-100"},
                    {"so_bai": 20, "ten_bai": "Ôn tập chương 6", "trang": "101-102", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y10, "TỐC ĐỘ PHẢN ỨNG HOÁ HỌC", "NGUYÊN TỐ NHÓM VIIA"),
            },
            {
                "so_chuong": 7,
                "ten_chuong": "Chương 7. Nguyên tố nhóm halogen",
                "trang_bat_dau": 103,
                "trang_ket_thuc": 118,
                "bai_hoc": [
                    {"so_bai": 21, "ten_bai": "Nhóm halogen", "trang": "104-111"},
                    {"so_bai": 22, "ten_bai": "Hydrogen halide - Muối halide", "trang": "112-116"},
                    {"so_bai": 23, "ten_bai": "Ôn tập chương 7", "trang": "117-118", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y10, "NGUYÊN TỐ NHÓM VIIA", None),
            },
        ],
    }

    cfg_11 = {
        "id": "SGK_HOA_11_KNTT",
        "mon_hoc": "Hóa học",
        "khoi_lop": "Lớp 11",
        "bo_sach": "Kết nối tri thức với cuộc sống",
        "sgk_file": "SGK/SGK HOA 11 KNTT.pdf",
        "sbt_file": "SGK/BAI TAP HOA 11 KNTT.pdf",
        "sgv_file": "SGK/SGV HOA 11 KNTT.pdf",
        "yccd_file": "SGK/YEU CAU CAN DAT HOA 11.pdf",
        "chuong": [
            {
                "so_chuong": 1,
                "ten_chuong": "Chương 1. Cân bằng hoá học",
                "trang_bat_dau": 6,
                "trang_ket_thuc": 28,
                "bai_hoc": [
                    {"so_bai": 1, "ten_bai": "Khái niệm về cân bằng hoá học", "trang": "6-15"},
                    {"so_bai": 2, "ten_bai": "Cân bằng trong dung dịch nước", "trang": "16-26"},
                    {"so_bai": 3, "ten_bai": "Ôn tập chương 1", "trang": "27-28", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y11, "CÂN BẰNG HOÁ HỌC", "NITROGEN"),
            },
            {
                "so_chuong": 2,
                "ten_chuong": "Chương 2. Nitrogen – Sulfur",
                "trang_bat_dau": 29,
                "trang_ket_thuc": 56,
                "bai_hoc": [
                    {"so_bai": 4, "ten_bai": "Nitrogen", "trang": "29-32"},
                    {"so_bai": 5, "ten_bai": "Ammonia • Muối ammonium", "trang": "33-37"},
                    {"so_bai": 6, "ten_bai": "Một số hợp chất của nitrogen với oxygen", "trang": "38-41"},
                    {"so_bai": 7, "ten_bai": "Sulfur và sulfur dioxide", "trang": "42-47"},
                    {"so_bai": 8, "ten_bai": "Sulfuric acid và muối sulfate", "trang": "48-54"},
                    {"so_bai": 9, "ten_bai": "Ôn tập chương 2", "trang": "55-56", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y11, "NITROGEN – SULFUR", "ĐẠI CƯƠNG VỀ HOÁ HỌC HỮU CƠ"),
            },
            {
                "so_chuong": 3,
                "ten_chuong": "Chương 3. Đại cương về hoá học hữu cơ",
                "trang_bat_dau": 57,
                "trang_ket_thuc": 81,
                "bai_hoc": [
                    {"so_bai": 10, "ten_bai": "Hợp chất hữu cơ và hoá học hữu cơ", "trang": "57-62"},
                    {"so_bai": 11, "ten_bai": "Phương pháp tách biệt và tinh chế hợp chất hữu cơ", "trang": "63-69"},
                    {"so_bai": 12, "ten_bai": "Công thức phân tử hợp chất hữu cơ", "trang": "70-73"},
                    {"so_bai": 13, "ten_bai": "Cấu tạo hoá học hợp chất hữu cơ", "trang": "74-79"},
                    {"so_bai": 14, "ten_bai": "Ôn tập chương 3", "trang": "80-81", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y11, "ĐẠI CƯƠNG VỀ HOÁ HỌC HỮU CƠ", "HYDROCARBON"),
            },
            {
                "so_chuong": 4,
                "ten_chuong": "Chương 4. Hydrocarbon",
                "trang_bat_dau": 82,
                "trang_ket_thuc": 111,
                "bai_hoc": [
                    {"so_bai": 15, "ten_bai": "Alkane", "trang": "82-91"},
                    {"so_bai": 16, "ten_bai": "Hydrocarbon không no", "trang": "92-101"},
                    {"so_bai": 17, "ten_bai": "Arene (Hydrocarbon thơm)", "trang": "102-109"},
                    {"so_bai": 18, "ten_bai": "Ôn tập chương 4", "trang": "110-111", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y11, "HYDROCARBON", "DẪN XUẤT HALOGEN"),
            },
            {
                "so_chuong": 5,
                "ten_chuong": "Chương 5. Dẫn xuất halogen – Alcohol – Phenol",
                "trang_bat_dau": 112,
                "trang_ket_thuc": 135,
                "bai_hoc": [
                    {"so_bai": 19, "ten_bai": "Dẫn xuất halogen", "trang": "112-118"},
                    {"so_bai": 20, "ten_bai": "Alcohol", "trang": "119-128"},
                    {"so_bai": 21, "ten_bai": "Phenol", "trang": "129-133"},
                    {"so_bai": 22, "ten_bai": "Ôn tập chương 5", "trang": "134-135", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y11, "DẪN XUẤT HALOGEN – ALCOHOL – PHENOL", "HỢP CHẤT CARBONYL"),
            },
            {
                "so_chuong": 6,
                "ten_chuong": "Chương 6. Hợp chất carbonyl – Carboxylic acid",
                "trang_bat_dau": 136,
                "trang_ket_thuc": 154,
                "bai_hoc": [
                    {"so_bai": 23, "ten_bai": "Hợp chất carbonyl", "trang": "136-144"},
                    {"so_bai": 24, "ten_bai": "Carboxylic acid", "trang": "145-152"},
                    {"so_bai": 25, "ten_bai": "Ôn tập chương 6", "trang": "153-154", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y11, "HỢP CHẤT CARBONYL – CARBOXYLIC ACID", None),
            },
        ],
    }

    cfg_12 = {
        "id": "SGK_HOA_12_KNTT",
        "mon_hoc": "Hóa học",
        "khoi_lop": "Lớp 12",
        "bo_sach": "Kết nối tri thức với cuộc sống",
        "sgk_file": "SGK/SGK HOA 12 - KNTT .pdf",
        "sbt_file": "SGK/BAI TAP HOA 12 KNTT.pdf",
        "sgv_file": "SGK/SGV HOA 12 KNTT.pdf",
        "yccd_file": "SGK/YEU CAU CAN DAT HOA 12.pdf",
        "chuong": [
            {
                "so_chuong": 1,
                "ten_chuong": "Chương 1. Ester – Lipid",
                "trang_bat_dau": 6,
                "trang_ket_thuc": 19,
                "bai_hoc": [
                    {"so_bai": 1, "ten_bai": "Ester – Lipid", "trang": "6-13"},
                    {"so_bai": 2, "ten_bai": "Xà phòng và chất giặt rửa", "trang": "14-17"},
                    {"so_bai": 3, "ten_bai": "Ôn tập chương 1", "trang": "18-19", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y12, "ESTER – LIPID", "CARBOHYDRATE"),
            },
            {
                "so_chuong": 2,
                "ten_chuong": "Chương 2. Carbohydrate",
                "trang_bat_dau": 20,
                "trang_ket_thuc": 34,
                "bai_hoc": [
                    {"so_bai": 4, "ten_bai": "Giới thiệu về carbohydrate. Glucose và fructose", "trang": "20-24"},
                    {"so_bai": 5, "ten_bai": "Saccharose và maltose", "trang": "25-27"},
                    {"so_bai": 6, "ten_bai": "Tinh bột và cellulose", "trang": "28-32"},
                    {"so_bai": 7, "ten_bai": "Ôn tập chương 2", "trang": "33-34", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y12, "CARBOHYDRATE", "HỢP CHẤT CHỨA NITROGEN"),
            },
            {
                "so_chuong": 3,
                "ten_chuong": "Chương 3. Hợp chất chứa nitrogen",
                "trang_bat_dau": 35,
                "trang_ket_thuc": 50,
                "bai_hoc": [
                    {"so_bai": 8, "ten_bai": "Amine", "trang": "35-40"},
                    {"so_bai": 9, "ten_bai": "Amino acid và peptide", "trang": "41-45"},
                    {"so_bai": 10, "ten_bai": "Protein và enzyme", "trang": "46-48"},
                    {"so_bai": 11, "ten_bai": "Ôn tập chương 3", "trang": "49-50", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y12, "HỢP CHẤT CHỨA NITROGEN", "POLYMER"),
            },
            {
                "so_chuong": 4,
                "ten_chuong": "Chương 4. Polymer",
                "trang_bat_dau": 51,
                "trang_ket_thuc": 66,
                "bai_hoc": [
                    {"so_bai": 12, "ten_bai": "Đại cương về polymer", "trang": "51-55"},
                    {"so_bai": 13, "ten_bai": "Vật liệu polymer", "trang": "56-64"},
                    {"so_bai": 14, "ten_bai": "Ôn tập chương 4", "trang": "65-66", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y12, "POLYMER", "PIN ĐIỆN VÀ ĐIỆN PHÂN"),
            },
            {
                "so_chuong": 5,
                "ten_chuong": "Chương 5. Pin điện và điện phân",
                "trang_bat_dau": 67,
                "trang_ket_thuc": 86,
                "bai_hoc": [
                    {"so_bai": 15, "ten_bai": "Thế điện cực và nguồn điện hoá học", "trang": "67-77"},
                    {"so_bai": 16, "ten_bai": "Điện phân", "trang": "78-84"},
                    {"so_bai": 17, "ten_bai": "Ôn tập chương 5", "trang": "85-86", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y12, "PIN ĐIỆN VÀ ĐIỆN PHÂN", "ĐẠI CƯƠNG VỀ KIM LOẠI"),
            },
            {
                "so_chuong": 6,
                "ten_chuong": "Chương 6. Đại cương về kim loại",
                "trang_bat_dau": 87,
                "trang_ket_thuc": 107,
                "bai_hoc": [
                    {"so_bai": 18, "ten_bai": "Cấu tạo và liên kết trong tinh thể kim loại", "trang": "87-88"},
                    {"so_bai": 19, "ten_bai": "Tính chất vật lí và tính chất hoá học của kim loại", "trang": "89-93"},
                    {"so_bai": 20, "ten_bai": "Kim loại trong tự nhiên và phương pháp tách kim loại", "trang": "94-98"},
                    {"so_bai": 21, "ten_bai": "Hợp kim", "trang": "99-101"},
                    {"so_bai": 22, "ten_bai": "Sự ăn mòn kim loại", "trang": "102-105"},
                    {"so_bai": 23, "ten_bai": "Ôn tập chương 6", "trang": "106-107", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y12, "ĐẠI CƯƠNG VỀ KIM LOẠI", "NGUYÊN TỐ NHÓM IA"),
            },
            {
                "so_chuong": 7,
                "ten_chuong": "Chương 7. Nguyên tố nhóm IA và nhóm IIA",
                "trang_bat_dau": 108,
                "trang_ket_thuc": 127,
                "bai_hoc": [
                    {"so_bai": 24, "ten_bai": "Nguyên tố nhóm IA", "trang": "108-115"},
                    {"so_bai": 25, "ten_bai": "Nguyên tố nhóm IIA", "trang": "116-125"},
                    {"so_bai": 26, "ten_bai": "Ôn tập chương 7", "trang": "126-127", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y12, "NGUYÊN TỐ NHÓM IA VÀ NHÓM IIA", "SƠ LƯỢC VỀ DÃY KIM LOẠI CHUYỂN TIẾP"),
            },
            {
                "so_chuong": 8,
                "ten_chuong": "Chương 8. Sơ lược về dãy kim loại chuyển tiếp thứ nhất và phức chất",
                "trang_bat_dau": 128,
                "trang_ket_thuc": 144,
                "bai_hoc": [
                    {"so_bai": 27, "ten_bai": "Đại cương về kim loại chuyển tiếp dãy thứ nhất", "trang": "128-133"},
                    {"so_bai": 28, "ten_bai": "Sơ lược về phức chất", "trang": "134-137"},
                    {"so_bai": 29, "ten_bai": "Một số tính chất và ứng dụng của phức chất", "trang": "138-141"},
                    {"so_bai": 30, "ten_bai": "Ôn tập chương 8", "trang": "142-144", "is_on_tap": True},
                ],
                "yeu_cau_can_dat": extract_section_yccd(y12, "SƠ LƯỢC VỀ DÃY KIM LOẠI CHUYỂN TIẾP", None),
            },
        ],
    }

    for cfg in [cfg_10, cfg_11, cfg_12]:
        p = out_dir / f"{cfg['id']}.json"
        p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        total_lessons = sum(len(c["bai_hoc"]) for c in cfg["chuong"])
        total_yccd = sum(len(c["yeu_cau_can_dat"]) for c in cfg["chuong"])
        print(f"Saved {p} | chapters={len(cfg['chuong'])} | lessons={total_lessons} | yccd_items={total_yccd}")


if __name__ == "__main__":
    build_configs()
