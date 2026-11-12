import json
import sys
from pathlib import Path


def validate_questions(qblock: dict, expected_mcq: int | None, expected_tf: int | None, errors: list[str]):
    mcqs = qblock.get("mcq", [])
    if expected_mcq is not None and len(mcqs) != expected_mcq:
        errors.append(f"Số câu MCQ phải là {expected_mcq} (hiện có {len(mcqs)}).")
    for q in mcqs:
        opts = q.get("lua_chon", {})
        if set(opts.keys()) != {"A", "B", "C", "D"}:
            errors.append(f"MCQ câu {q.get('cau_so')} thiếu phương án A/B/C/D.")
        if q.get("dap_an") not in {"A", "B", "C", "D"}:
            errors.append(f"MCQ câu {q.get('cau_so')} đáp án không hợp lệ.")
        if not q.get("giai_thich"):
            errors.append(f"MCQ câu {q.get('cau_so')} thiếu giải thích.")

    tfs = qblock.get("dung_sai", [])
    if expected_tf is not None and len(tfs) != expected_tf:
        errors.append(f"Số câu Đúng/Sai phải là {expected_tf} (hiện có {len(tfs)}).")
    for q in tfs:
        stmts = q.get("nhan_dinh", [])
        if len(stmts) != 4:
            errors.append(f"Câu Đúng/Sai {q.get('cau_so')} phải có 4 nhận định (hiện có {len(stmts)}).")
        if [s.get("ky_hieu") for s in stmts] != ["a", "b", "c", "d"]:
            errors.append(f"Câu Đúng/Sai {q.get('cau_so')} ký hiệu nhận định phải là a, b, c, d.")
        for s in stmts:
            if not isinstance(s.get("dap_an"), bool) or not s.get("giai_thich"):
                errors.append(f"Câu Đúng/Sai {q.get('cau_so')}{s.get('ky_hieu')} thiếu đáp án bool hoặc giải thích.")


def validate_lesson(data: dict) -> list[str]:
    errors: list[str] = []
    for k in ["meta", "muc_tieu", "y_nghia_thuc_tien", "kien_thuc_trong_tam", "he_thong_hoa", "cau_hoi_tu_kiem_tra"]:
        if k not in data:
            errors.append(f"Thiếu mục bắt buộc: {k}")
    if errors:
        return errors

    for i, item in enumerate(data.get("y_nghia_thuc_tien", []), 1):
        for f in ["hien_tuong", "cau_hoi", "giai_thich_hoa_hoc", "y_nghia_ung_dung", "lien_ket_muc_c"]:
            if not item.get(f):
                errors.append(f"Mục B.{i} thiếu trường '{f}'.")

    for i, sec in enumerate(data.get("kien_thuc_trong_tam", []), 1):
        if not sec.get("giai_thich_ban_chat"):
            errors.append(f"Mục C.{i} thiếu 'giai_thich_ban_chat'.")
        vi_du = sec.get("vi_du", {})
        if not vi_du.get("de_bai") or not vi_du.get("huong_dan"):
            errors.append(f"Mục C.{i} thiếu ví dụ minh họa hoặc hướng dẫn giải.")
        img = sec.get("hinh_anh")
        if img and img.get("path") and not Path(img["path"]).exists():
            errors.append(f"Mục C.{i} file ảnh không tồn tại: {img['path']}")

    mcqs = data["cau_hoi_tu_kiem_tra"].get("mcq", [])
    levels = [q.get("muc_do") for q in mcqs]
    if len(mcqs) == 5 and (levels.count("Nhận biết") != 2 or levels.count("Thông hiểu") != 2 or levels.count("Vận dụng") != 1):
        errors.append(f"Phân bố MCQ bài học chưa đúng 2 NB - 2 TH - 1 VD (hiện có {levels}).")
    validate_questions(data["cau_hoi_tu_kiem_tra"], 5, 2, errors)
    return errors


def validate_chapter(data: dict, expected_mcq: int = 15, expected_tf: int = 5) -> list[str]:
    errors: list[str] = []
    for k in ["meta", "muc_tieu_chuong", "y_nghia_thuc_tien", "he_thong_kien_thuc", "bang_tong_hop_lien_he", "vi_du_tong_hop", "cac_dang_bai_tap", "cau_hoi_tu_kiem_tra"]:
        if k not in data:
            errors.append(f"Thiếu mục bắt buộc (Chế độ B): {k}")
    if errors:
        return errors
    validate_questions(data["cau_hoi_tu_kiem_tra"], expected_mcq, expected_tf, errors)
    return errors


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python validate_study_json.py <input.json> [--mode lesson|chapter]")
        sys.exit(1)
    json_path = Path(args[0])
    mode = "lesson"
    if "--mode" in args:
        mode = args[args.index("--mode") + 1]
    data = json.loads(json_path.read_text(encoding="utf-8"))
    errs = validate_chapter(data) if mode == "chapter" else validate_lesson(data)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print(f"VALIDATION PASSED ({mode}): JSON hợp lệ theo chuẩn GDPT 2018.")
