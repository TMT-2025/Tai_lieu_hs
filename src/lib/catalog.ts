import hoa10Kntt from '../../data/configs/SGK_HOA_10_KNTT.json';
import hoa11Kntt from '../../data/configs/SGK_HOA_11_KNTT.json';
import hoa12Kntt from '../../data/configs/SGK_HOA_12_KNTT.json';
import hoa10Ctst from '../../data/configs/SGK_HOA_10_CTST.json';
import hoa11Ctst from '../../data/configs/SGK_HOA_11_CTST.json';
import hoa12Ctst from '../../data/configs/SGK_HOA_12_CTST.json';
import hoa10Cd from '../../data/configs/SGK_HOA_10_CANH_DIEU.json';
import hoa11Cd from '../../data/configs/SGK_HOA_11_CANH_DIEU.json';
import hoa12Cd from '../../data/configs/SGK_HOA_12_CANH_DIEU.json';

export interface LessonItem {
  so_bai: number;
  ten_bai: string;
  trang: string;
  is_on_tap?: boolean;
}

export interface ChapterItem {
  so_chuong: number;
  ten_chuong: string;
  trang_bat_dau: number;
  trang_ket_thuc: number;
  bai_hoc: LessonItem[];
  yeu_cau_can_dat: string[];
}

export interface TextbookConfig {
  id: string;
  mon_hoc: string;
  khoi_lop: string;
  bo_sach: string;
  chuong: ChapterItem[];
}

export const ALL_CONFIGS: TextbookConfig[] = [
  hoa10Kntt,
  hoa11Kntt,
  hoa12Kntt,
  hoa10Ctst,
  hoa11Ctst,
  hoa12Ctst,
  hoa10Cd,
  hoa11Cd,
  hoa12Cd,
] as TextbookConfig[];

export type BookSeriesOption =
  | 'Kết nối tri thức với cuộc sống'
  | 'Chân trời sáng tạo'
  | 'Cánh Diều'
  | 'ALL_3';

export function getChaptersForSelection(khoiLop: string, boSach: BookSeriesOption): ChapterItem[] {
  const gradeLabel = `Lớp ${khoiLop}`;
  if (boSach === 'ALL_3') {
    // Use KNTT as the primary chapter backbone, and merge YCCD across all 3 series
    const kntt = ALL_CONFIGS.find((c) => c.khoi_lop === gradeLabel && c.bo_sach === 'Kết nối tri thức với cuộc sống');
    const ctst = ALL_CONFIGS.find((c) => c.khoi_lop === gradeLabel && c.bo_sach === 'Chân trời sáng tạo');
    const cd = ALL_CONFIGS.find((c) => c.khoi_lop === gradeLabel && c.bo_sach === 'Cánh Diều');
    if (!kntt) return [];
    return kntt.chuong.map((ch) => {
      const matchCtst = ctst?.chuong.find((x) => x.so_chuong === ch.so_chuong);
      const matchCd = cd?.chuong.find((x) => x.so_chuong === ch.so_chuong);
      const mergedYccd = Array.from(
        new Set([...(ch.yeu_cau_can_dat || []), ...(matchCtst?.yeu_cau_can_dat || []), ...(matchCd?.yeu_cau_can_dat || [])])
      );
      return {
        ...ch,
        yeu_cau_can_dat: mergedYccd,
      };
    });
  }

  const cfg = ALL_CONFIGS.find((c) => c.khoi_lop === gradeLabel && c.bo_sach === boSach);
  return cfg ? cfg.chuong : [];
}
