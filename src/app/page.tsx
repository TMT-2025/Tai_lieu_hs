'use client';

import React, { useEffect, useMemo, useState } from 'react';
import {
  BookOpen,
  CheckCircle2,
  Download,
  Eye,
  EyeOff,
  FileText,
  KeyRound,
  Layers,
  Loader2,
  Sparkles,
  AlertCircle,
} from 'lucide-react';
import { BookSeriesOption, getChaptersForSelection } from '@/lib/catalog';

const API_KEY_STORAGE = 'ai_study_doc_gemini_api_key';

const BOOK_OPTIONS: { value: BookSeriesOption; label: string }[] = [
  { value: 'Kết nối tri thức với cuộc sống', label: 'Kết nối tri thức với cuộc sống (KNTT)' },
  { value: 'Chân trời sáng tạo', label: 'Chân trời sáng tạo (CTST)' },
  { value: 'Cánh Diều', label: 'Cánh Diều' },
  { value: 'ALL_3', label: 'Tổng hợp cả 3 bộ sách (KNTT + CTST + Cánh Diều)' },
];

export default function HomePage() {
  const [khoiLop, setKhoiLop] = useState<string>('10');
  const [boSach, setBoSach] = useState<BookSeriesOption>('Kết nối tri thức với cuộc sống');
  const [selectedChapterNo, setSelectedChapterNo] = useState<number>(1);
  const [selectedLessonNo, setSelectedLessonNo] = useState<number>(1);
  const [ghiChuThem, setGhiChuThem] = useState<string>('');

  const [apiKey, setApiKey] = useState<string>('');
  const [showApiKey, setShowApiKey] = useState<boolean>(false);
  const [model, setModel] = useState<string>('gemini-2.5-flash');

  const [loadingMode, setLoadingMode] = useState<'lesson' | 'chapter' | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(API_KEY_STORAGE);
      if (saved) setApiKey(saved);
    } catch {
      // ignore localStorage access error
    }
  }, []);

  const handleApiKeyChange = (val: string) => {
    setApiKey(val);
    try {
      if (val.trim()) {
        window.localStorage.setItem(API_KEY_STORAGE, val.trim());
      } else {
        window.localStorage.removeItem(API_KEY_STORAGE);
      }
    } catch {
      // ignore localStorage access error
    }
  };

  const chapters = useMemo(() => {
    return getChaptersForSelection(khoiLop, boSach);
  }, [khoiLop, boSach]);

  const currentChapter = useMemo(() => {
    return chapters.find((c) => c.so_chuong === selectedChapterNo) || chapters[0] || null;
  }, [chapters, selectedChapterNo]);

  useEffect(() => {
    if (chapters.length > 0 && !chapters.some((c) => c.so_chuong === selectedChapterNo)) {
      setSelectedChapterNo(chapters[0].so_chuong);
    }
  }, [chapters, selectedChapterNo]);

  const lessons = currentChapter?.bai_hoc || [];

  const currentLesson = useMemo(() => {
    return lessons.find((l) => l.so_bai === selectedLessonNo) || lessons[0] || null;
  }, [lessons, selectedLessonNo]);

  useEffect(() => {
    if (lessons.length > 0 && !lessons.some((l) => l.so_bai === selectedLessonNo)) {
      setSelectedLessonNo(lessons[0].so_bai);
    }
  }, [lessons, selectedLessonNo]);

  const handleGenerate = async (mode: 'lesson' | 'chapter') => {
    if (!currentChapter) return;
    if (mode === 'lesson' && !currentLesson) return;

    setLoadingMode(mode);
    setErrorMsg(null);
    setSuccessMsg(null);

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          apiKey: apiKey.trim() || undefined,
          model,
          mode,
          khoiLop,
          boSach,
          tenChuong: `Chương ${currentChapter.so_chuong}: ${currentChapter.ten_chuong}`,
          tenBai:
            mode === 'lesson' && currentLesson
              ? `Bài ${currentLesson.so_bai}: ${currentLesson.ten_bai}`
              : undefined,
          yeuCauCanDat: currentChapter.yeu_cau_can_dat || [],
          ghiChuThem: ghiChuThem.trim() || undefined,
        }),
      });

      if (!res.ok) {
        let message = `Lỗi máy chủ (${res.status})`;
        try {
          const errJson = await res.json();
          if (errJson?.error) message = errJson.error;
        } catch {
          // ignore
        }
        throw new Error(message);
      }

      const blob = await res.blob();
      const disposition = res.headers.get('Content-Disposition') || '';
      const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
      const asciiMatch = disposition.match(/filename="([^"]+)"/i);
      const rawName = utf8Match
        ? decodeURIComponent(utf8Match[1])
        : asciiMatch
          ? asciiMatch[1]
          : `ON_TAP_HOA_${khoiLop}.docx`;

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = rawName;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      setSuccessMsg(
        `Đã tạo và tải xuống thành công: ${rawName} (${
          mode === 'lesson' ? '5 MCQ + 2 Đúng/Sai' : '15 MCQ + 5 Đúng/Sai'
        }).`,
      );
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Đã xảy ra lỗi khi tạo tài liệu.';
      setErrorMsg(msg);
    } finally {
      setLoadingMode(null);
    }
  };

  return (
    <main className="container">
      <header className="header">
        <div className="header-title-wrap">
          <div className="header-icon">
            <Sparkles size={26} />
          </div>
          <div>
            <h1>AI STUDY DOCUMENT STUDIO</h1>
            <p>Biên soạn tài liệu ôn tập Hóa học THPT (GDPT 2018) — Xuất file Word (.docx) chuẩn sư phạm</p>
          </div>
        </div>
        <div className="badge">
          <BookOpen size={15} />
          <span>Hóa học 10 · 11 · 12</span>
        </div>
      </header>

      <div className="grid">
        <section className="card">
          <h2 className="card-title">
            <Layers size={19} color="#1d4ed8" />
            <span>1. Chọn nội dung cần biên soạn</span>
          </h2>

          <div className="form-grid">
            <div className="field">
              <label htmlFor="khoi-lop">Khối lớp</label>
              <select
                id="khoi-lop"
                value={khoiLop}
                onChange={(e) => setKhoiLop(e.target.value)}
                disabled={loadingMode !== null}
              >
                <option value="10">Lớp 10</option>
                <option value="11">Lớp 11</option>
                <option value="12">Lớp 12</option>
              </select>
            </div>

            <div className="field">
              <label htmlFor="bo-sach">Bộ sách giáo khoa</label>
              <select
                id="bo-sach"
                value={boSach}
                onChange={(e) => setBoSach(e.target.value as BookSeriesOption)}
                disabled={loadingMode !== null}
              >
                {BOOK_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="field field-full">
              <label htmlFor="chuong">Chương</label>
              <select
                id="chuong"
                value={currentChapter?.so_chuong ?? ''}
                onChange={(e) => setSelectedChapterNo(Number(e.target.value))}
                disabled={loadingMode !== null || chapters.length === 0}
              >
                {chapters.map((c) => (
                  <option key={c.so_chuong} value={c.so_chuong}>
                    Chương {c.so_chuong}: {c.ten_chuong}
                  </option>
                ))}
              </select>
            </div>

            <div className="field field-full">
              <label htmlFor="bai-hoc">Bài học (dùng cho nút &quot;Tạo tài liệu cho bài&quot;)</label>
              <select
                id="bai-hoc"
                value={currentLesson?.so_bai ?? ''}
                onChange={(e) => setSelectedLessonNo(Number(e.target.value))}
                disabled={loadingMode !== null || lessons.length === 0}
              >
                {lessons.map((l) => (
                  <option key={l.so_bai} value={l.so_bai}>
                    Bài {l.so_bai}: {l.ten_bai} {l.trang ? `(Trang ${l.trang})` : ''}
                  </option>
                ))}
              </select>
            </div>

            <div className="field field-full">
              <label htmlFor="ghi-chu">Ghi chú / Yêu cầu riêng của giáo viên (tùy chọn)</label>
              <textarea
                id="ghi-chu"
                placeholder="Ví dụ: Tập trung vào học sinh trung bình - khá, nhấn mạnh phương pháp bảo toàn electron, thêm ví dụ thực tế..."
                value={ghiChuThem}
                onChange={(e) => setGhiChuThem(e.target.value)}
                disabled={loadingMode !== null}
              />
            </div>
          </div>

          <div className="actions">
            <button
              type="button"
              className="btn btn-primary"
              disabled={loadingMode !== null || !currentLesson}
              onClick={() => handleGenerate('lesson')}
            >
              {loadingMode === 'lesson' ? (
                <>
                  <Loader2 size={18} className="spin" />
                  <span>Đang tạo tài liệu bài...</span>
                </>
              ) : (
                <>
                  <FileText size={18} />
                  <span>Tạo tài liệu cho bài</span>
                </>
              )}
            </button>

            <button
              type="button"
              className="btn btn-accent"
              disabled={loadingMode !== null || !currentChapter}
              onClick={() => handleGenerate('chapter')}
            >
              {loadingMode === 'chapter' ? (
                <>
                  <Loader2 size={18} className="spin" />
                  <span>Đang tạo tài liệu chương...</span>
                </>
              ) : (
                <>
                  <Download size={18} />
                  <span>Tạo tài liệu cho chương</span>
                </>
              )}
            </button>
          </div>

          {errorMsg && (
            <div className="alert alert-error" role="alert">
              <AlertCircle size={18} style={{ flexShrink: 0, marginTop: 2 }} />
              <div>{errorMsg}</div>
            </div>
          )}

          {successMsg && (
            <div className="alert alert-success" role="status">
              <CheckCircle2 size={18} style={{ flexShrink: 0, marginTop: 2 }} />
              <div>{successMsg}</div>
            </div>
          )}
        </section>

        <aside className="card">
          <h2 className="card-title">
            <KeyRound size={19} color="#0f766e" />
            <span>2. Cấu hình API Key &amp; Xem trước</span>
          </h2>

          <div className="field">
            <label htmlFor="gemini-key">Gemini API Key</label>
            <div className="input-group">
              <input
                id="gemini-key"
                type={showApiKey ? 'text' : 'password'}
                placeholder="AIzaSy... (tự động lưu trên trình duyệt của bạn)"
                value={apiKey}
                onChange={(e) => handleApiKeyChange(e.target.value)}
                disabled={loadingMode !== null}
              />
              <button
                type="button"
                className="icon-btn"
                onClick={() => setShowApiKey((v) => !v)}
                aria-label={showApiKey ? 'Ẩn API Key' : 'Hiện API Key'}
              >
                {showApiKey ? <EyeOff size={17} /> : <Eye size={17} />}
              </button>
            </div>
            <span className="hint">
              Key chỉ lưu cục bộ trong <code>localStorage</code> trình duyệt và gửi trực tiếp khi tạo file. Nếu
              máy chủ đã cấu hình sẵn biến môi trường <code>GEMINI_API_KEY</code>, bạn có thể để trống ô này.
            </span>
          </div>

          <div className="field">
            <label htmlFor="model-select">Mô hình Gemini</label>
            <select
              id="model-select"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              disabled={loadingMode !== null}
            >
              <option value="gemini-2.5-flash">gemini-2.5-flash (Nhanh, khuyên dùng)</option>
              <option value="gemini-2.5-pro">gemini-2.5-pro (Chuyên sâu, chi tiết hơn)</option>
            </select>
          </div>

          {currentChapter && (
            <>
              <div className="meta-box">
                <div className="meta-row">
                  <span className="meta-label">Chế độ Bài học:</span>
                  <span className="meta-val">5 Trắc nghiệm + 2 Đúng/Sai</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">Chế độ Chương:</span>
                  <span className="meta-val">15 Trắc nghiệm + 5 Đúng/Sai</span>
                </div>
                <div className="meta-row">
                  <span className="meta-label">Số bài trong chương:</span>
                  <span className="meta-val">{lessons.length} bài</span>
                </div>
              </div>

              <div className="field" style={{ marginBottom: 0 }}>
                <label>Yêu cầu cần đạt (GDPT 2018) của chương</label>
                {currentChapter.yeu_cau_can_dat.length > 0 ? (
                  <ul className="yccd-list">
                    {currentChapter.yeu_cau_can_dat.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                ) : (
                  <div className="alert alert-warning" style={{ marginTop: 4 }}>
                    Chương này chưa có danh sách YCCD chi tiết trong file cấu hình; AI sẽ tự tổng hợp theo chuẩn GDPT 2018.
                  </div>
                )}
              </div>
            </>
          )}
        </aside>
      </div>
    </main>
  );
}
