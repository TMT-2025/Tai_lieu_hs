import 'dotenv/config';
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import { GoogleGenAI } from '@google/genai';
import { buildStudyDocx } from './build_study_docx.mjs';

function findSgkFile(khoiLop, boSach) {
  const idxPath = path.resolve('data/sgk_index.json');
  if (!fs.existsSync(idxPath)) {
    throw new Error('Chưa có data/sgk_index.json. Hãy chạy: python .agents/skills/study-docx-builder/scripts/index_sgk.py');
  }
  const idx = JSON.parse(fs.readFileSync(idxPath, 'utf-8'));
  const sgk = idx.files.find(
    (f) => f.khoi_lop === String(khoiLop) && f.bo_sach.toLowerCase().includes(boSach.toLowerCase()) && f.loai === 'Sách giáo khoa'
  );
  const yccd = idx.files.find((f) => f.khoi_lop === String(khoiLop) && f.loai === 'Yêu cầu cần đạt');
  return { sgk, yccd };
}

function extractPages(pdfPath, startPage, endPage) {
  const script = path.resolve(import.meta.dirname, 'index_sgk.py');
  return execFileSync('python', [script, '--extract', pdfPath, String(startPage), String(endPage)], {
    encoding: 'utf-8',
    maxBuffer: 20 * 1024 * 1024,
  });
}

async function callGeminiWithRetry(ai, model, prompt, schema, maxRetries = 2) {
  let lastErr;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await ai.models.generateContent({
        model,
        contents: prompt,
        config: {
          responseMimeType: 'application/json',
          responseJsonSchema: schema,
          temperature: 0.2,
        },
      });
      return JSON.parse(response.text);
    } catch (err) {
      lastErr = err;
      console.error(`Attempt ${attempt + 1} failed: ${err.message}`);
    }
  }
  throw lastErr;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 6) {
    console.error('Usage: node generate_from_source.mjs "<Khoi>" "<BoSach>" "<Chuong>" "<TenBai>" <startPage> <endPage> [lesson|chapter]');
    process.exit(1);
  }
  const [khoiLop, boSach, chuong, tenBai, startPage, endPage, mode = 'lesson'] = args;
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey || apiKey === 'your_gemini_api_key_here') {
    console.error('ERROR: Thiếu GEMINI_API_KEY trong file .env.');
    process.exit(1);
  }

  const { sgk, yccd } = findSgkFile(khoiLop, boSach);
  if (!sgk) throw new Error(`Không tìm thấy SGK Hóa ${khoiLop} (${boSach}) trong data/sgk_index.json`);

  let sourceText = extractPages(sgk.path, startPage, endPage);
  if (yccd) {
    sourceText += '\n\n=== YÊU CẦU CẦN ĐẠT CHƯƠNG TRÌNH ===\n' + extractPages(yccd.path, 1, yccd.pages);
  }

  const schemaFile = mode === 'chapter' ? '../templates/chapter_schema.json' : '../templates/study_schema.json';
  const schema = JSON.parse(fs.readFileSync(path.resolve(import.meta.dirname, schemaFile), 'utf-8'));

  const prompt = `Bạn là chuyên gia Hóa học THPT Việt Nam (GDPT 2018).
Biên soạn tài liệu chế độ "${mode}" cho: Hóa học ${khoiLop} | ${boSach} | ${chuong} | ${tenBai}.
Nguồn chính thức: ${sgk.filename} (trang ${startPage}-${endPage}).
TÀI LIỆU NGUỒN:\n${sourceText.slice(0, 120000)}\n
YÊU CẦU BẮT BUỘC:
- Mục B: 2–4 hiện tượng thực tiễn theo đủ 5 ý (hien_tuong, cau_hoi, giai_thich_hoa_hoc, y_nghia_ung_dung, lien_ket_muc_c).
- Mục C: Đầy đủ phân loại, điều kiện áp dụng, giải thích bản chất, ví dụ từng đề mục, và trường lien_he_thuc_tien nối lại với mục B.
- Công thức hóa học dùng _{...} và ^{...}, mũi tên ->. Kiểm tra cân bằng PTPU và phép tính trước khi xuất JSON.
- Câu hỏi: ${mode === 'chapter' ? '15 MCQ + 5 Đúng/Sai (4 ý)' : '5 MCQ (2 NB, 2 TH, 1 VD) + 2 Đúng/Sai (4 ý)'}.`;

  const ai = new GoogleGenAI({ apiKey });
  const data = await callGeminiWithRetry(ai, process.env.GEMINI_MODEL || 'gemini-2.5-flash', prompt, schema, 2);

  const safeName = `${khoiLop}_${boSach}_${tenBai}`.replace(/[^a-zA-Z0-9_-]+/g, '_').toUpperCase();
  const jsonOut = path.resolve('data', `${safeName}.json`);
  const docxOut = path.resolve('output', `ON_TAP_HOA_${safeName}.docx`);

  fs.mkdirSync(path.dirname(jsonOut), { recursive: true });
  fs.writeFileSync(jsonOut, JSON.stringify(data, null, 2), 'utf-8');
  await buildStudyDocx(data, docxOut, mode);
  console.log(`DONE (${mode}): ${docxOut}`);
}

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
