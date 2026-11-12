import fs from 'fs';
import path from 'path';
import {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  Header,
  HeadingLevel,
  ImageRun,
  LevelFormat,
  Packer,
  PageBreak,
  PageNumber,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableRow,
  TextRun,
  WidthType,
} from 'docx';

// Page geometry (A4 in DXA: 1 cm = 567 DXA)
const PAGE_WIDTH = 11906;
const PAGE_HEIGHT = 16838;
const MARGIN_LEFT = 1417; // 2.5 cm
const MARGIN_RIGHT = 1134; // 2.0 cm
const MARGIN_TOP = 1134; // 2.0 cm
const MARGIN_BOTTOM = 1134; // 2.0 cm
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT; // 9355 DXA (~16.5 cm)

const FONT_NAME = 'Times New Roman';
const COLOR_PRIMARY = '1B365D';
const COLOR_ACCENT = '2B5B84';
const COLOR_TEXT = '111111';
const COLOR_MUTED = '555555';
const COLOR_HEADER_BG = 'E8EEF5';
const COLOR_ALT_ROW = 'F7F9FC';
const COLOR_BORDER = 'B8C4D4';
const COLOR_CALLOUT_BG = 'F0F6FC';

/**
 * Parse **bold**, _{sub}, ^{sup}, ->, <-> into styled TextRuns.
 */
function parseRichRuns(text, baseOpts = {}) {
  if (!text) return [new TextRun({ text: '', font: FONT_NAME, ...baseOpts })];
  const normalized = String(text).replace(/<->/g, '⇌').replace(/->/g, '→');
  const tokenRegex = /(\*\*[^*]+\*\*|_\{[^}]+\}|\^\{[^}]+\})/g;
  const runs = [];
  let lastIndex = 0;
  let match;

  while ((match = tokenRegex.exec(normalized)) !== null) {
    if (match.index > lastIndex) {
      runs.push(
        new TextRun({
          text: normalized.slice(lastIndex, match.index),
          font: FONT_NAME,
          ...baseOpts,
        })
      );
    }
    const token = match[0];
    if (token.startsWith('**') && token.endsWith('**')) {
      runs.push(...parseRichRuns(token.slice(2, -2), { ...baseOpts, bold: true }));
    } else if (token.startsWith('_{') && token.endsWith('}')) {
      runs.push(
        new TextRun({
          text: token.slice(2, -1),
          font: FONT_NAME,
          ...baseOpts,
          subScript: true,
        })
      );
    } else if (token.startsWith('^{') && token.endsWith('}')) {
      runs.push(
        new TextRun({
          text: token.slice(2, -1),
          font: FONT_NAME,
          ...baseOpts,
          superScript: true,
        })
      );
    }
    lastIndex = tokenRegex.lastIndex;
  }

  if (lastIndex < normalized.length) {
    runs.push(
      new TextRun({
        text: normalized.slice(lastIndex),
        font: FONT_NAME,
        ...baseOpts,
      })
    );
  }
  return runs.length ? runs : [new TextRun({ text: '', font: FONT_NAME, ...baseOpts })];
}

function makeParagraph(text, opts = {}) {
  const {
    alignment = AlignmentType.JUSTIFIED,
    spacingAfter = 90,
    spacingBefore = 0,
    runOpts = {},
    bullet = false,
    keepNext = false,
    indentLeft = 0,
  } = opts;

  return new Paragraph({
    alignment,
    keepNext,
    ...(bullet ? { numbering: { reference: 'bullet-list', level: 0 } } : {}),
    ...(indentLeft ? { indent: { left: indentLeft } } : {}),
    spacing: { before: spacingBefore, after: spacingAfter, line: 276 },
    children: parseRichRuns(text, { size: 24, color: COLOR_TEXT, ...runOpts }),
  });
}

function appendSolutionParagraphs(children, label, text, spacingAfter = 55) {
  const normalized = String(text || '')
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]+(?=(?:Bước\s+\d+[:.]))/gi, '\n')
    .trim();
  const lines = normalized
    .split('\n')
    .map((l) => l.trim().replace(/^(Bước\s+\d+[:.])(?!\*\*)/i, '**$1**'))
    .filter(Boolean);
  if (lines.length <= 1) {
    children.push(makeParagraph(`**${label}:** ${lines[0] || ''}`, { spacingAfter }));
    return;
  }
  const startsWithStep = /^\*{0,2}Bước\s+\d+[:.]/i.test(lines[0]);
  if (startsWithStep) {
    children.push(makeParagraph(`**${label}:**`, { spacingAfter: 25, keepNext: true }));
    lines.forEach((line, idx) => {
      const isLast = idx === lines.length - 1;
      children.push(makeParagraph(line, { indentLeft: 320, spacingAfter: isLast ? spacingAfter : 30 }));
    });
  } else {
    children.push(makeParagraph(`**${label}:** ${lines[0]}`, { spacingAfter: 30 }));
    lines.slice(1).forEach((line, idx) => {
      const isLast = idx === lines.length - 2;
      children.push(makeParagraph(line, { indentLeft: 320, spacingAfter: isLast ? spacingAfter : 30 }));
    });
  }
}

function makeHeading(text, level) {
  return new Paragraph({
    heading: level,
    keepNext: true,
    children: parseRichRuns(text, { font: FONT_NAME }),
  });
}

function makeCalloutBox(label, text) {
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [CONTENT_WIDTH],
    borders: {
      top: { style: BorderStyle.NONE },
      bottom: { style: BorderStyle.NONE },
      right: { style: BorderStyle.NONE },
      left: { style: BorderStyle.SINGLE, size: 18, color: COLOR_ACCENT },
    },
    rows: [
      new TableRow({
        cantSplit: true,
        children: [
          new TableCell({
            width: { size: CONTENT_WIDTH, type: WidthType.DXA },
            shading: { fill: COLOR_CALLOUT_BG, type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 160, right: 120 },
            children: [
              new Paragraph({
                alignment: AlignmentType.JUSTIFIED,
                spacing: { before: 20, after: 20, line: 260 },
                children: parseRichRuns(`**${label}:** ${text}`, { size: 23, color: COLOR_TEXT }),
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function makeBorderSet(color = COLOR_BORDER) {
  const b = { style: BorderStyle.SINGLE, size: 4, color };
  return { top: b, bottom: b, left: b, right: b, insideHorizontal: b, insideVertical: b };
}

function makeStyledTable(headers, rows, colWidths) {
  const tableRows = [
    new TableRow({
      tableHeader: true,
      cantSplit: true,
      children: headers.map(
        (h, idx) =>
          new TableCell({
            width: { size: colWidths[idx], type: WidthType.DXA },
            shading: { fill: COLOR_HEADER_BG, type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { before: 20, after: 20, line: 240 },
                children: parseRichRuns(h, { bold: true, size: 22, color: COLOR_PRIMARY }),
              }),
            ],
          })
      ),
    }),
    ...rows.map(
      (row, rIdx) =>
        new TableRow({
          cantSplit: true,
          children: row.map(
            (cell, cIdx) =>
              new TableCell({
                width: { size: colWidths[cIdx], type: WidthType.DXA },
                ...(rIdx % 2 === 1 ? { shading: { fill: COLOR_ALT_ROW, type: ShadingType.CLEAR } } : {}),
                margins: { top: 70, bottom: 70, left: 120, right: 120 },
                children: [
                  new Paragraph({
                    alignment: AlignmentType.LEFT,
                    spacing: { before: 20, after: 20, line: 250 },
                    children: parseRichRuns(cell, { size: 22, color: COLOR_TEXT }),
                  }),
                ],
              })
          ),
        })
    ),
  ];

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: colWidths,
    borders: makeBorderSet(),
    rows: tableRows,
  });
}

function computeColWidths(numCols) {
  const base = Math.floor(CONTENT_WIDTH / numCols);
  const widths = Array(numCols).fill(base);
  widths[numCols - 1] += CONTENT_WIDTH - base * numCols;
  return widths;
}

function readPngDimensions(buf) {
  // PNG IHDR width/height at bytes 16..24
  if (buf.length >= 24 && buf[0] === 0x89 && buf[1] === 0x50) {
    return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
  }
  return { width: 800, height: 400 };
}

function appendImageBlock(children, imgObj) {
  if (!imgObj || !imgObj.path || !fs.existsSync(imgObj.path)) return;
  const buf = fs.readFileSync(imgObj.path);
  const ext = path.extname(imgObj.path).toLowerCase().replace('.', '') === 'jpg' ? 'jpg' : 'png';
  const dims = readPngDimensions(buf);
  const maxWidthPx = Math.min(Math.round((imgObj.width_cm || 14.5) * 37.8), 580);
  const targetWidth = maxWidthPx;
  const targetHeight = Math.round((dims.height / dims.width) * targetWidth);

  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER,
      keepNext: true,
      spacing: { before: 100, after: 40 },
      children: [
        new ImageRun({
          type: ext,
          data: buf,
          transformation: { width: targetWidth, height: targetHeight },
        }),
      ],
    })
  );
  const captionText = imgObj.source ? `${imgObj.caption} *(Nguồn: ${imgObj.source})*` : imgObj.caption;
  children.push(
    makeParagraph(captionText, {
      alignment: AlignmentType.CENTER,
      spacingAfter: 100,
      runOpts: { italics: true, size: 22, color: COLOR_MUTED },
    })
  );
}

function appendPracticalSection(children, items, monHoc = 'Hóa học') {
  const explainLabel = /h[oó]a/i.test(monHoc || '') ? 'Giải thích Hóa học' : 'Giải thích khoa học';
  items.forEach((item, idx) => {
    children.push(makeHeading(`${idx + 1}. ${item.hien_tuong}`, HeadingLevel.HEADING_2));
    children.push(makeParagraph(`- **Vấn đề đặt ra:** ${item.cau_hoi}`, { spacingAfter: 40 }));
    children.push(makeParagraph(`- **${explainLabel}:** ${item.giai_thich_khoa_hoc || item.giai_thich_hoa_hoc || ''}`, { spacingAfter: 40 }));
    children.push(makeParagraph(`- **Ý nghĩa & Ứng dụng:** ${item.y_nghia_ung_dung}`, { spacingAfter: 40 }));
    children.push(makeParagraph(`- **Kết nối kiến thức:** ${item.lien_ket_muc_c}`, { spacingAfter: 80 }));
  });
}

function appendQuestionsAndAnswers(children, qblock, secQuestionsTitle, secAnswersTitle) {
  children.push(makeHeading(secQuestionsTitle, HeadingLevel.HEADING_1));
  children.push(makeHeading(`Phần I. Câu hỏi trắc nghiệm nhiều lựa chọn (${qblock.mcq.length} câu)`, HeadingLevel.HEADING_2));
  qblock.mcq.forEach((q) => {
    children.push(
      makeParagraph(`**Câu ${q.cau_so}** *(${q.muc_do})*: ${q.cau_hoi}`, { spacingBefore: 60, spacingAfter: 35, keepNext: true })
    );
    ['A', 'B', 'C', 'D'].forEach((opt) => {
      children.push(makeParagraph(`**${opt}.** ${q.lua_chon[opt]}`, { spacingAfter: 20, alignment: AlignmentType.LEFT }));
    });
  });

  children.push(makeHeading(`Phần II. Câu hỏi trắc nghiệm Đúng/Sai (${qblock.dung_sai.length} câu)`, HeadingLevel.HEADING_2));
  children.push(
    makeParagraph('*(Trong mỗi ý a, b, c, d ở mỗi câu, học sinh chọn Đúng hoặc Sai)*', {
      spacingAfter: 60,
      runOpts: { italics: true, color: COLOR_MUTED },
    })
  );
  qblock.dung_sai.forEach((q) => {
    children.push(makeParagraph(`**Câu ${q.cau_so}.** ${q.dan_nhap}`, { spacingBefore: 60, spacingAfter: 35, keepNext: true }));
    q.nhan_dinh.forEach((nd) => {
      children.push(makeParagraph(`**${nd.ky_hieu})** ${nd.noi_dung}`, { spacingAfter: 25 }));
    });
  });

  // Page break before Answers
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(makeHeading(secAnswersTitle, HeadingLevel.HEADING_1));

  // MCQ answer table (split into rows of 5 if >5)
  children.push(makeHeading('1. Bảng đáp án Phần I (Trắc nghiệm MCQ)', HeadingLevel.HEADING_2));
  for (let start = 0; start < qblock.mcq.length; start += 5) {
    const slice = qblock.mcq.slice(start, start + 5);
    const headers = ['Câu', ...slice.map((q) => String(q.cau_so))];
    const row = ['Đáp án', ...slice.map((q) => `**${q.dap_an}**`)];
    children.push(makeStyledTable(headers, [row], computeColWidths(headers.length)));
    children.push(makeParagraph('', { spacingAfter: 60 }));
  }

  children.push(makeHeading('2. Bảng đáp án Phần II (Trắc nghiệm Đúng/Sai)', HeadingLevel.HEADING_2));
  const tfHeaders = ['Câu', 'Ý a)', 'Ý b)', 'Ý c)', 'Ý d)'];
  const tfRows = qblock.dung_sai.map((q) => [
    `**Câu ${q.cau_so}**`,
    ...q.nhan_dinh.map((nd) => (nd.dap_an ? '**Đúng**' : 'Sai')),
  ]);
  children.push(makeStyledTable(tfHeaders, tfRows, computeColWidths(5)));
  children.push(makeParagraph('', { spacingAfter: 80 }));

  children.push(makeHeading('3. Giải thích chi tiết Phần I (MCQ)', HeadingLevel.HEADING_2));
  qblock.mcq.forEach((q) => {
    children.push(makeParagraph(`**Câu ${q.cau_so} (Đáp án ${q.dap_an}):** ${q.giai_thich}`, { spacingAfter: 55 }));
  });

  children.push(makeHeading('4. Giải thích chi tiết Phần II (Đúng/Sai)', HeadingLevel.HEADING_2));
  qblock.dung_sai.forEach((q) => {
    children.push(makeParagraph(`**Câu ${q.cau_so}:**`, { spacingAfter: 30, keepNext: true }));
    q.nhan_dinh.forEach((nd) => {
      children.push(makeParagraph(`- **${nd.ky_hieu}) ${nd.dap_an ? 'Đúng' : 'Sai'}:** ${nd.giai_thich}`, { spacingAfter: 35 }));
    });
  });
}

function buildLessonChildren(data) {
  const { meta, muc_tieu, y_nghia_thuc_tien, kien_thuc_trong_tam, he_thong_hoa, cau_hoi_tu_kiem_tra } = data;
  const children = [];

  const titleLabel = meta.is_demo ? `${meta.ten_bai.toUpperCase()} [BẢN DEMO]` : meta.ten_bai.toUpperCase();
  children.push(
    new Paragraph({
      heading: HeadingLevel.TITLE,
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 120 },
      children: [new TextRun({ text: titleLabel, font: FONT_NAME, size: 32, bold: true, color: COLOR_PRIMARY })],
    })
  );

  const metaRows = [
    [`**Môn học:** ${meta.mon_hoc} (${meta.khoi_lop})`, `**Bộ sách:** ${meta.bo_sach}`],
    [`**Chương:** ${meta.chuong}`, `**Chế độ:** Ôn tập theo bài học (Chế độ A)`],
  ];
  if (meta.nguon_sgk) {
    metaRows.push([`**Nguồn SGK:** ${meta.nguon_sgk}`, `**Chuẩn:** GDPT 2018`]);
  }
  children.push(makeStyledTable(['Thông tin tài liệu', 'Phạm vi biên soạn'], metaRows, [4678, 4677]));
  children.push(makeParagraph('', { spacingAfter: 80 }));

  // A
  children.push(makeHeading('A. MỤC TIÊU ÔN TẬP', HeadingLevel.HEADING_1));
  children.push(makeParagraph('**1. Kiến thức cần nắm:**', { spacingAfter: 40, keepNext: true }));
  muc_tieu.kien_thuc.forEach((i) => children.push(makeParagraph(i, { bullet: true, spacingAfter: 40 })));
  children.push(makeParagraph('**2. Kỹ năng cần đạt:**', { spacingBefore: 50, spacingAfter: 40, keepNext: true }));
  muc_tieu.ky_nang.forEach((i) => children.push(makeParagraph(i, { bullet: true, spacingAfter: 40 })));

  // B
  children.push(makeHeading('B. Ý NGHĨA THỰC TIỄN', HeadingLevel.HEADING_1));
  appendPracticalSection(children, y_nghia_thuc_tien, meta.mon_hoc);

  // C
  children.push(makeHeading('C. KIẾN THỨC TRỌNG TÂM', HeadingLevel.HEADING_1));
  kien_thuc_trong_tam.forEach((sec) => {
    children.push(makeHeading(`${sec.muc_so}. ${sec.tieu_de}`, HeadingLevel.HEADING_2));

    children.push(makeHeading('1. Kiến thức cốt lõi', HeadingLevel.HEADING_3));
    sec.cot_loi.forEach((p) => children.push(makeParagraph(p, { bullet: true, spacingAfter: 45 })));

    children.push(makeHeading('2. Giải thích bản chất', HeadingLevel.HEADING_3));
    children.push(makeParagraph(sec.giai_thich_ban_chat, { spacingAfter: 55 }));

    if (sec.cong_thuc_quy_tac?.length) {
      children.push(makeHeading('3. Công thức & Điều kiện áp dụng', HeadingLevel.HEADING_3));
      sec.cong_thuc_quy_tac.forEach((ct) => children.push(makeParagraph(ct, { bullet: true, spacingAfter: 45 })));
    }

    children.push(makeHeading('4. Ví dụ minh họa', HeadingLevel.HEADING_3));
    children.push(makeParagraph(`**Đề bài:** ${sec.vi_du.de_bai}`, { spacingAfter: 35 }));
    appendSolutionParagraphs(children, 'Hướng dẫn giải', sec.vi_du.huong_dan, 55);

    if (sec.hinh_anh) {
      appendImageBlock(children, sec.hinh_anh);
    }

    if (sec.lien_he_thuc_tien) {
      children.push(makeCalloutBox('Liên hệ thực tiễn', sec.lien_he_thuc_tien));
      children.push(makeParagraph('', { spacingAfter: 60 }));
    }

    if (sec.luu_y?.length) {
      children.push(makeHeading('5. Lưu ý & Kiến thức dễ nhầm', HeadingLevel.HEADING_3));
      sec.luu_y.forEach((ly) => children.push(makeParagraph(ly, { bullet: true, spacingAfter: 45 })));
    }
  });

  // D
  children.push(makeHeading('D. HỆ THỐNG HÓA KIẾN THỨC', HeadingLevel.HEADING_1));
  if (he_thong_hoa.bang_so_sanh) {
    const { tieu_de, headers, rows } = he_thong_hoa.bang_so_sanh;
    children.push(makeParagraph(`**${tieu_de}**`, { spacingAfter: 55, keepNext: true }));
    children.push(makeStyledTable(headers, rows, computeColWidths(headers.length)));
    children.push(makeParagraph('', { spacingAfter: 80 }));
  }
  if (he_thong_hoa.so_do_tong_hop) {
    appendImageBlock(children, he_thong_hoa.so_do_tong_hop);
  }
  if (he_thong_hoa.quy_tac_ghi_nho?.length) {
    children.push(makeHeading('Quy tắc ghi nhớ nhanh', HeadingLevel.HEADING_2));
    he_thong_hoa.quy_tac_ghi_nho.forEach((q) => children.push(makeParagraph(q, { bullet: true, spacingAfter: 45 })));
  }
  if (he_thong_hoa.loi_thuong_gap?.length) {
    children.push(makeHeading('Lỗi học sinh thường mắc', HeadingLevel.HEADING_2));
    he_thong_hoa.loi_thuong_gap.forEach((l) => children.push(makeParagraph(l, { bullet: true, spacingAfter: 45 })));
  }

  // E & F
  appendQuestionsAndAnswers(children, cau_hoi_tu_kiem_tra, 'E. CÂU HỎI TỰ KIỂM TRA', 'F. ĐÁP ÁN VÀ GIẢI THÍCH');
  return children;
}

function buildChapterChildren(data) {
  const {
    meta,
    muc_tieu_chuong,
    y_nghia_thuc_tien,
    he_thong_kien_thuc,
    bang_tong_hop_lien_he,
    vi_du_tong_hop,
    cac_dang_bai_tap,
    cau_hoi_tu_kiem_tra,
  } = data;
  const children = [];

  children.push(
    new Paragraph({
      heading: HeadingLevel.TITLE,
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 120 },
      children: [
        new TextRun({
          text: `ÔN TẬP ${meta.chuong.toUpperCase()}`,
          font: FONT_NAME,
          size: 32,
          bold: true,
          color: COLOR_PRIMARY,
        }),
      ],
    })
  );

  const metaRows = [
    [`**Môn học:** ${meta.mon_hoc} (${meta.khoi_lop})`, `**Bộ sách:** ${meta.bo_sach}`],
    [`**Nguồn SGK:** ${meta.nguon_sgk || 'SGK GDPT 2018'}`, `**Chế độ:** Ôn tập tổng hợp chương (Chế độ B)`],
  ];
  children.push(makeStyledTable(['Thông tin tài liệu', 'Phạm vi biên soạn'], metaRows, [4678, 4677]));
  children.push(makeParagraph('', { spacingAfter: 80 }));

  children.push(makeHeading('A. MỤC TIÊU ÔN TẬP CHƯƠNG', HeadingLevel.HEADING_1));
  children.push(makeParagraph('**1. Kiến thức:**', { spacingAfter: 40, keepNext: true }));
  muc_tieu_chuong.kien_thuc.forEach((i) => children.push(makeParagraph(i, { bullet: true, spacingAfter: 40 })));
  children.push(makeParagraph('**2. Kỹ năng:**', { spacingBefore: 50, spacingAfter: 40, keepNext: true }));
  muc_tieu_chuong.ky_nang.forEach((i) => children.push(makeParagraph(i, { bullet: true, spacingAfter: 40 })));

  children.push(makeHeading('B. Ý NGHĨA THỰC TIỄN CỦA KIẾN THỨC TRONG CHƯƠNG', HeadingLevel.HEADING_1));
  appendPracticalSection(children, y_nghia_thuc_tien, meta.mon_hoc);

  children.push(makeHeading('C. HỆ THỐNG KIẾN THỨC TRỌNG TÂM THEO CHỦ ĐỀ', HeadingLevel.HEADING_1));
  he_thong_kien_thuc.forEach((sec) => {
    children.push(makeHeading(`${sec.muc_so}. ${sec.chu_de}`, HeadingLevel.HEADING_2));
    sec.cot_loi.forEach((p) => children.push(makeParagraph(p, { bullet: true, spacingAfter: 45 })));
    children.push(makeParagraph(`**Giải thích bản chất:** ${sec.giai_thich_ban_chat}`, { spacingAfter: 55 }));
    if (sec.hinh_anh) appendImageBlock(children, sec.hinh_anh);
    children.push(makeParagraph(`**Ví dụ:** ${sec.vi_du.de_bai}`, { spacingAfter: 35 }));
    appendSolutionParagraphs(children, 'Hướng dẫn', sec.vi_du.huong_dan, 55);
  });

  children.push(makeHeading('D. BẢNG TỔNG HỢP VÀ LIÊN HỆ GIỮA CÁC BÀI', HeadingLevel.HEADING_1));
  children.push(makeParagraph(`**${bang_tong_hop_lien_he.tieu_de}**`, { spacingAfter: 50, keepNext: true }));
  children.push(makeStyledTable(bang_tong_hop_lien_he.headers, bang_tong_hop_lien_he.rows, computeColWidths(bang_tong_hop_lien_he.headers.length)));
  children.push(makeParagraph('', { spacingAfter: 80 }));

  children.push(makeHeading('E. VÍ DỤ MINH HỌA TỔNG HỢP', HeadingLevel.HEADING_1));
  vi_du_tong_hop.forEach((vd, idx) => {
    children.push(makeHeading(`Ví dụ ${idx + 1}. ${vd.tieu_de}`, HeadingLevel.HEADING_2));
    children.push(makeParagraph(`**Đề bài:** ${vd.de_bai}`, { spacingAfter: 35 }));
    appendSolutionParagraphs(children, 'Hướng dẫn giải', vd.huong_dan, 60);
  });

  children.push(makeHeading('F. CÁC DẠNG BÀI TẬP VÀ PHƯƠNG PHÁP GIẢI', HeadingLevel.HEADING_1));
  cac_dang_bai_tap.forEach((d, idx) => {
    children.push(makeHeading(`Dạng ${idx + 1}. ${d.ten_dang}`, HeadingLevel.HEADING_2));
    children.push(makeParagraph(`**Phương pháp giải:** ${d.phuong_phap}`, { spacingAfter: 40 }));
    children.push(makeParagraph(`**Ví dụ áp dụng:** ${d.vi_du_minh_hoa}`, { spacingAfter: 60 }));
  });

  appendQuestionsAndAnswers(children, cau_hoi_tu_kiem_tra, 'G. CÂU HỎI TỰ KIỂM TRA', 'H. ĐÁP ÁN VÀ HƯỚNG DẪN GIẢI');
  return children;
}

export async function buildStudyDocx(data, outputPath, mode = 'auto') {
  const resolvedMode = mode === 'auto' ? (data.muc_tieu_chuong ? 'chapter' : 'lesson') : mode;
  const children = resolvedMode === 'chapter' ? buildChapterChildren(data) : buildLessonChildren(data);
  const headerTitle =
    resolvedMode === 'chapter'
      ? `${data.meta.mon_hoc} ${data.meta.khoi_lop} — ${data.meta.chuong}`
      : `${data.meta.mon_hoc} ${data.meta.khoi_lop} — ${data.meta.ten_bai}`;

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { font: FONT_NAME, size: 24, color: COLOR_TEXT },
          paragraph: { spacing: { line: 276, after: 90 } },
        },
      },
      paragraphStyles: [
        {
          id: 'Title',
          name: 'Title',
          basedOn: 'Normal',
          next: 'Normal',
          run: { font: FONT_NAME, size: 32, bold: true, color: COLOR_PRIMARY },
          paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 0, after: 140 } },
        },
        {
          id: 'Heading1',
          name: 'Heading 1',
          basedOn: 'Normal',
          next: 'Normal',
          quickFormat: true,
          run: { font: FONT_NAME, size: 28, bold: true, color: COLOR_PRIMARY },
          paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 0 },
        },
        {
          id: 'Heading2',
          name: 'Heading 2',
          basedOn: 'Normal',
          next: 'Normal',
          quickFormat: true,
          run: { font: FONT_NAME, size: 26, bold: true, color: COLOR_ACCENT },
          paragraph: { spacing: { before: 140, after: 60 }, outlineLevel: 1 },
        },
        {
          id: 'Heading3',
          name: 'Heading 3',
          basedOn: 'Normal',
          next: 'Normal',
          quickFormat: true,
          run: { font: FONT_NAME, size: 24, bold: true, color: COLOR_TEXT },
          paragraph: { spacing: { before: 80, after: 35 }, outlineLevel: 2 },
        },
      ],
    },
    numbering: {
      config: [
        {
          reference: 'bullet-list',
          levels: [
            {
              level: 0,
              format: LevelFormat.BULLET,
              text: '•',
              alignment: AlignmentType.LEFT,
              style: { paragraph: { indent: { left: 540, hanging: 260 } } },
            },
          ],
        },
      ],
    },
    sections: [
      {
        properties: {
          page: {
            size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
            margin: { left: MARGIN_LEFT, right: MARGIN_RIGHT, top: MARGIN_TOP, bottom: MARGIN_BOTTOM },
          },
        },
        headers: {
          default: new Header({
            children: [
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                children: [new TextRun({ text: headerTitle, font: FONT_NAME, size: 20, italics: true, color: COLOR_MUTED })],
              }),
            ],
          }),
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({ text: 'Trang ', font: FONT_NAME, size: 20, color: COLOR_MUTED }),
                  new TextRun({ children: [PageNumber.CURRENT], font: FONT_NAME, size: 20, color: COLOR_MUTED }),
                  new TextRun({ text: ' / ', font: FONT_NAME, size: 20, color: COLOR_MUTED }),
                  new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT_NAME, size: 20, color: COLOR_MUTED }),
                ],
              }),
            ],
          }),
        },
        children,
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, buffer);
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(import.meta.filename)) {
  const args = process.argv.slice(2);
  const inputJson = args[0];
  const outputDocx = args[1];
  const modeIdx = args.indexOf('--mode');
  const mode = modeIdx !== -1 ? args[modeIdx + 1] : 'auto';
  if (!inputJson || !outputDocx) {
    console.error('Usage: node build_study_docx.mjs <input.json> <output.docx> [--mode lesson|chapter]');
    process.exit(1);
  }
  const data = JSON.parse(fs.readFileSync(inputJson, 'utf-8'));
  await buildStudyDocx(data, outputDocx, mode);
  console.log(`DOCX generated successfully: ${outputDocx}`);
}
