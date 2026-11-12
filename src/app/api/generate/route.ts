import { NextRequest, NextResponse } from 'next/server';
import { GoogleGenAI } from '@google/genai';
import lessonSchema from '../../../../.agents/skills/study-docx-builder/templates/study_schema.json';
import chapterSchema from '../../../../.agents/skills/study-docx-builder/templates/chapter_schema.json';
import { buildStudyDocxBuffer } from '@/lib/docxBuilder';

export const maxDuration = 60;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const {
      apiKey,
      model = 'gemini-3.8-flash',
      mode = 'lesson',
      khoiLop,
      boSach,
      tenChuong,
      tenBai,
      yeuCauCanDat = [],
      ghiChuThem = '',
    } = body;

    const resolvedKey = (apiKey && String(apiKey).trim()) || process.env.GEMINI_API_KEY;
    if (!resolvedKey) {
      return NextResponse.json(
        { error: 'Thiếu Gemini API Key. Vui lòng nhập API Key trên giao diện hoặc cấu hình GEMINI_API_KEY trên Vercel.' },
        { status: 400 }
      );
    }

    const boSachLabel = boSach === 'ALL_3' ? 'Tổng hợp 3 bộ sách (KNTT, CTST, Cánh Diều)' : boSach;
    const yccdText = Array.isArray(yeuCauCanDat) && yeuCauCanDat.length ? yeuCauCanDat.map((x: string) => `- ${x}`).join('\n') : '- Theo chuẩn GDPT 2018';

    const prompt =
      mode === 'lesson'
        ? `Bạn là chuyên gia giáo dục Hóa học THPT Việt Nam (GDPT 2018).
Hãy biên soạn tài liệu ôn tập CHẾ ĐỘ A (THEO BÀI HỌC) cho học sinh tự học:
- Môn học: Hóa học | Khối: Lớp ${khoiLop}
- Bộ sách: ${boSachLabel}
- Chương: ${tenChuong}
- Bài học: ${tenBai}
Yêu cầu cần đạt (GDPT 2018):
${yccdText}
${ghiChuThem ? `\nYêu cầu bổ sung của giáo viên: ${ghiChuThem}` : ''}

QUY TẮC BẮT BUỘC:
1. Ký hiệu Hóa học: dùng _{...} cho chỉ số dưới (H_{2}O, CO_{2}), ^{...} cho chỉ số trên/điện tích (Fe^{3+}, SO_{4}^{2-}), -> cho mũi tên phản ứng.
2. Mục B (Ý nghĩa thực tiễn): 2–4 hiện tượng thực tế gần gũi Việt Nam, mỗi hiện tượng đủ 5 trường (hien_tuong, cau_hoi, giai_thich_hoa_hoc, y_nghia_ung_dung, lien_ket_muc_c).
3. Mục C (Kiến thức trọng tâm): đầy đủ phân loại, điều kiện áp dụng, giai_thich_ban_chat, ít nhất 1 vi_du có lời giải từng bước cho mỗi đề mục, và trường lien_he_thuc_tien nối về mục B.
4. Mục E: Chính xác 5 câu MCQ (2 Nhận biết, 2 Thông hiểu, 1 Vận dụng) + 2 câu Đúng/Sai (mỗi câu 4 nhận định a, b, c, d). Kiểm tra kỹ phương trình, phép tính và đáp án.`
        : `Bạn là chuyên gia giáo dục Hóa học THPT Việt Nam (GDPT 2018).
Hãy biên soạn tài liệu ôn tập CHẾ ĐỘ B (TỔNG HỢP CHƯƠNG) cho học sinh tự học:
- Môn học: Hóa học | Khối: Lớp ${khoiLop}
- Bộ sách: ${boSachLabel}
- Chương: ${tenChuong}
Yêu cầu cần đạt của chương:
${yccdText}
${ghiChuThem ? `\nYêu cầu bổ sung của giáo viên: ${ghiChuThem}` : ''}

QUY TẮC BẮT BUỘC:
1. Ký hiệu Hóa học dùng _{...}, ^{...}, ->.
2. Tổng hợp và kết nối kiến thức giữa các bài trong chương, có bảng tổng hợp liên hệ, ví dụ tổng hợp và các dạng bài tập thường gặp.
3. Câu hỏi tự kiểm tra: 15 câu MCQ (bao quát đều các bài trong chương, phân hóa Nhận biết/Thông hiểu/Vận dụng) + 5 câu Đúng/Sai (mỗi câu 4 nhận định a, b, c, d). Kiểm tra kỹ phép tính và đáp án.`;

    const ai = new GoogleGenAI({ apiKey: resolvedKey });
    const schema = mode === 'chapter' ? chapterSchema : lessonSchema;

    const response = await ai.models.generateContent({
      model,
      contents: prompt,
      config: {
        responseMimeType: 'application/json',
        responseJsonSchema: schema as Record<string, unknown>,
        temperature: 0.2,
      },
    });

    const data = JSON.parse(response.text || '{}');
    if (!data.meta) {
      data.meta = {
        mon_hoc: 'Hóa học',
        khoi_lop: `Lớp ${khoiLop}`,
        bo_sach: boSachLabel,
        chuong: tenChuong,
        ten_bai: tenBai || tenChuong,
        is_demo: false,
      };
    }

    const buffer = await buildStudyDocxBuffer(data, mode === 'chapter' ? 'chapter' : 'lesson');
    const rawName = mode === 'chapter' ? `ON_TAP_HOA_${khoiLop}_${tenChuong}` : `ON_TAP_HOA_${khoiLop}_${tenBai}`;
    const safeFile = rawName.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_|_$/g, '').toUpperCase() + '.docx';

    return new NextResponse(new Uint8Array(buffer), {
      status: 200,
      headers: {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'Content-Disposition': `attachment; filename="${safeFile}"`,
      },
    });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || 'Lỗi tạo tài liệu DOCX.' }, { status: 500 });
  }
}
