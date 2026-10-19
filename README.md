# Bài Tập Nhóm - Lập Trình Web Với Python (Guestbook)

Dự án xây dựng ứng dụng web **Sổ lưu bút (Guestbook)** phục vụ bài tập môn học Lập trình Web với Python, bao gồm đầy đủ yêu cầu của **Buổi 1** và **Buổi 2** với hai phiên bản:
1. **Phiên bản Vibe Code** (`vibe_code/`): Thiết kế giao diện hiện đại theo phong cách Glassmorphism & Cyber Dark, cơ sở dữ liệu SQLite kết hợp đồng bộ file JSON, tìm kiếm thời gian thực, modal xác nhận, bảng xếp hạng Top 5 và biểu đồ Matplotlib tùy biến cao cấp.
2. **Phiên bản Manual** (`manual/`): Cài đặt thủ công theo HTML cơ bản, lưu trữ file JSON, route thống kê `/stats` và biểu đồ Matplotlib cột truyền thống theo đúng yêu cầu đề bài.

---

## 📁 Cấu Trúc Dự Án

```text
Bai_TAP_WEB_Python/
│
├── vibe_code/                    # 🚀 PHIÊN BẢN VIBE CODE (Đề xuất chấm điểm chính)
│   ├── app.py                    # Flask server (Port 5001)
│   ├── database.py               # Module quản lý SQLite & JSON sync
│   ├── vibe_guestbook.db         # Database SQLite lưu trữ lời nhắn
│   ├── data.json                 # File dữ liệu JSON đồng bộ
│   ├── requirements.txt          # Thư viện cần thiết
│   ├── static/
│   │   ├── css/style.css         # Glassmorphism design system & micro-animations
│   │   ├── js/main.js            # Live search, đếm ký tự, modal xác nhận
│   │   └── stats.png             # Biểu đồ Matplotlib dark mode
│   └── templates/
│       ├── base.html             # Layout chính với navbar và toast
│       ├── index.html            # Trang chủ, feed lời nhắn, modal xóa
│       ├── add.html              # Form thêm lời nhắn + validation
│       └── stats.html            # 4 KPI cards, Top 5 leaderboard, biểu đồ
│
├── manual/                       # ✍️ PHIÊN BẢN MANUAL (Cơ bản theo đề bài)
│   ├── app.py                    # Flask server (Port 5000)
│   ├── data.json                 # File JSON lưu trữ
│   ├── requirements.txt
│   ├── static/
│   │   ├── style.css             # CSS cơ bản ban đầu
│   │   └── stats.png             # Biểu đồ Matplotlib
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── add.html
│       └── stats.html
│
├── tài liệu mô tả.txt             # File tài liệu yêu cầu gốc
├── requirements.txt              # Cài đặt thư viện chung
├── run_vibe.bat                  # Script click chạy nhanh bản Vibe Code
├── run_manual.bat                # Script click chạy nhanh bản Manual
└── README.md
```

---

## 🛠️ Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Cài đặt các thư viện cần thiết
Mở terminal tại thư mục gốc của dự án và chạy:
```bash
pip install -r requirements.txt
```
*(Yêu cầu: `Flask>=3.0.0`, `matplotlib>=3.8.0`)*

---

### 2. Chạy Phiên Bản Vibe Code (Port 5001)
**Cách 1:** Nhấp đúp vào file `run_vibe.bat`
**Cách 2:** Chạy lệnh terminal:
```bash
cd vibe_code
python app.py
```
👉 Truy cập trình duyệt: **[http://127.0.0.1:5001](http://127.0.0.1:5001)**

#### Các tính năng nổi bật của bản Vibe Code:
- **Trang chủ (`/`)**:
  - Giao diện Glassmorphism tối sang trọng, bo góc mượt mà, hiệu ứng glow.
  - Avatar màu gradient ngẫu nhiên cho từng người gửi.
  - Tìm kiếm trực tiếp (Live Search) theo tên người gửi hoặc nội dung lời nhắn.
  - Hộp thoại Modal Dialog xác nhận khi xóa lời nhắn.
- **Trang thêm lời nhắn (`/add`)**:
  - Kiểm tra tính hợp lệ dữ liệu (Server-side + Client-side validation).
  - Bộ đếm số lượng ký tự theo thời gian thực.
  - Thông báo Toast mượt mà khi gửi thành công.
- **Trang thống kê (`/stats`)**:
  - 4 Thẻ KPI: Tổng lời nhắn, Người gửi duy nhất, Người tích cực nhất, Trạng thái DB.
  - Bảng xếp hạng Top 5 người gửi nhiều lời nhắn nhất kèm huy chương 🥇 🥈 🥉 và thanh tiến trình.
  - Biểu đồ Matplotlib chất lượng cao (140 DPI) chuẩn Dark Theme đồng bộ với UI.
  - Nút tải trực tiếp file `data.json`.
- **Cơ sở dữ liệu**:
  - Sử dụng SQLite (`vibe_guestbook.db`) kết hợp tự động đồng bộ ra file `data.json`.

---

### 3. Chạy Phiên Bản Manual (Port 5000)
**Cách 1:** Nhấp đúp vào file `run_manual.bat`
**Cách 2:** Chạy lệnh terminal:
```bash
cd manual
python app.py
```
👉 Truy cập trình duyệt: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📋 So Sánh Đáp Ứng Yêu Cầu Đề Bài

| Yêu cầu đề bài | Phiên bản Manual | Phiên bản Vibe Code |
| :--- | :---: | :---: |
| **Buổi 1: Route `/` (GET)** hiển thị lời nhắn | ✅ Có | ✅ Có + Avatar + Live Search |
| **Buổi 1: Route `/add` (GET, POST)** form + validate | ✅ Có | ✅ Có + Đếm ký tự + Toast |
| **Buổi 1: Route `/delete/<id>`** xóa theo ID | ✅ Có | ✅ Có + Dialog xác nhận |
| **Buổi 1: Lưu trữ dữ liệu** | ✅ File JSON | ✅ SQLite DB + File JSON |
| **Buổi 2: Đọc/Ghi dữ liệu file JSON** | ✅ Có (`data.json`) | ✅ Tự động đồng bộ 2 chiều |
| **Buổi 2: Route `/stats` (GET)** | ✅ Có | ✅ 4 Thẻ KPI hiện đại |
| **Buổi 2: Top 5 người gửi nhiều nhất** | ✅ Danh sách ol | ✅ Bảng xếp hạng + Huy chương |
| **Buổi 2: Biểu đồ cột Matplotlib lưu PNG** | ✅ `stats.png` | ✅ `stats.png` chuẩn Dark Neon |