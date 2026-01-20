# 🚀 Hướng Dẫn Chạy Crawler

## Chuẩn Bị

### 1. Cài đặt Dependencies
```bash
pip install aiohttp pandas matplotlib seaborn
```

### 2. Khởi động Backend
```bash
cd backend
uvicorn app.main:app --reload
```
Kiểm tra: http://localhost:8000/docs

### 3. Chạy Crawler
```bash
cd crawler/scripts
python craw_student.py
```

## Kết Quả
- **CSV**: `crawler/output/students_cleaned.csv` (dữ liệu được làm sạch)
- **Biểu Đồ**: `crawler/output/student_visualizations.png` (4 biểu đồ)

## Các Biểu Đồ
1. **Histogram**: Phân bổ điểm Toán/Anh/Văn
2. **Boxplot**: So sánh điểm theo vùng miền (Hometown)
3. **Scatter Plot**: Phát hiện học sinh lệch (Math vs English)
4. **Bar Chart**: Tỉ lệ sinh viên đạt >= 7 điểm

## Xử Lý Dữ Liệu
- Sinh viên thiếu điểm → Lấy trung bình theo Hometown
- Database không thay đổi (chỉ CSV được làm sạch)
- Xuất file CSV với tất cả 9 cột dữ liệu
