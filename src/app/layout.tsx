import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Study Document Studio — Tạo tài liệu ôn tập Hóa học THPT',
  description:
    'Ứng dụng AI hỗ trợ giáo viên biên soạn tài liệu ôn tập Hóa học lớp 10, 11, 12 theo Chương trình GDPT 2018 (KNTT, CTST, Cánh Diều) và xuất file Word (.docx).',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
