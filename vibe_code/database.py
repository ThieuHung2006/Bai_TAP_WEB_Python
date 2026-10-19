import sqlite3
import json
import os
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'vibe_guestbook.db')
JSON_PATH = os.path.join(BASE_DIR, 'data.json')

AVATAR_GRADIENTS = [
    "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
    "linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)",
    "linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)",
    "linear-gradient(135deg, #10b981 0%, #14b8a6 100%)",
    "linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)",
    "linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)",
]


def get_db_connection():
    """Tạo kết nối tới SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khởi tạo bảng và nạp dữ liệu mẫu ban đầu nếu trống."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                avatar_color TEXT
            )
        ''')
        conn.commit()

        # Kiểm tra nếu DB rỗng, thử đọc từ file JSON hoặc thêm dữ liệu mẫu vibe
        cursor.execute('SELECT COUNT(*) as count FROM messages')
        count = cursor.fetchone()['count']

        if count == 0:
            if os.path.exists(JSON_PATH):
                try:
                    with open(JSON_PATH, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for item in data:
                            cursor.execute(
                                'INSERT INTO messages (name, message, created_at, avatar_color) VALUES (?, ?, ?, ?)',
                                (
                                    item.get('name', 'Ẩn danh'),
                                    item.get('message', ''),
                                    item.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                                    item.get('avatar_color', random.choice(AVATAR_GRADIENTS))
                                )
                            )
                        conn.commit()
                except Exception:
                    pass

        # Nếu vẫn rỗng, thêm 3 lời nhắn mẫu cực cool
        cursor.execute('SELECT COUNT(*) as count FROM messages')
        if cursor.fetchone()['count'] == 0:
            sample_messages = [
                ("Vibe Coder", "Chào mừng đến với Guestbook phiên bản Vibe Code siêu mượt! Chúc các bạn làm đồ án đạt điểm A+ 🚀", "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)"),
                ("Thanh Thảo", "Giao diện glassmorphism đỉnh thật sự, màu sắc hiện đại và biểu đồ nhìn rất chuyên nghiệp! ✨", "linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)"),
                ("Minh Tuấn", "Test tính năng gửi lời nhắn và thống kê đồ thị Matplotlib. Chạy ngon lành không lỗi nha anh em 👍", "linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)")
            ]
            for name, msg, color in sample_messages:
                cursor.execute(
                    'INSERT INTO messages (name, message, created_at, avatar_color) VALUES (?, ?, ?, ?)',
                    (name, msg, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), color)
                )
            conn.commit()

    sync_db_to_json()


def sync_db_to_json():
    """Đồng bộ toàn bộ dữ liệu từ SQLite ra file data.json để đáp ứng yêu cầu lưu trữ file."""
    entries = get_all_entries()
    try:
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error syncing to JSON: {e}")


def get_all_entries():
    """Lấy danh sách tất cả lời nhắn, sắp xếp mới nhất lên đầu."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages ORDER BY id DESC')
        rows = cursor.fetchall()

        entries = []
        for row in rows:
            created_at_str = row['created_at']
            # Format ngày giờ thân thiện
            formatted_date = created_at_str
            try:
                dt = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
                formatted_date = dt.strftime('%H:%M • %d/%m/%Y')
            except Exception:
                pass

            entries.append({
                'id': row['id'],
                'name': row['name'],
                'message': row['message'],
                'created_at': created_at_str,
                'formatted_date': formatted_date,
                'avatar_color': row['avatar_color'] or AVATAR_GRADIENTS[0],
                'initials': ''.join([p[0].upper() for p in row['name'].split()[:2]]) if row['name'] else '?'
            })
        return entries


def add_entry(name, message):
    """Thêm một lời nhắn mới và đồng bộ ra file JSON."""
    name = name.strip()
    message = message.strip()
    if not name or not message:
        return False, "Tên và lời nhắn không được để trống."

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    avatar_color = random.choice(AVATAR_GRADIENTS)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO messages (name, message, created_at, avatar_color) VALUES (?, ?, ?, ?)',
            (name, message, created_at, avatar_color)
        )
        conn.commit()

    sync_db_to_json()
    return True, None


def delete_entry(entry_id):
    """Xóa lời nhắn theo ID và đồng bộ ra file JSON."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE id = ?', (entry_id,))
        conn.commit()

    sync_db_to_json()
    return True


def get_statistics():
    """Lấy các chỉ số thống kê tổng hợp."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tổng số lời nhắn
        cursor.execute('SELECT COUNT(*) as total FROM messages')
        total_messages = cursor.fetchone()['total']

        # Tổng số người gửi khác nhau
        cursor.execute('SELECT COUNT(DISTINCT name) as unique_senders FROM messages')
        unique_senders = cursor.fetchone()['unique_senders']

        # Top 5 người gửi nhiều lời nhắn nhất
        cursor.execute('''
            SELECT name, COUNT(*) as count 
            FROM messages 
            GROUP BY name 
            ORDER BY count DESC, name ASC 
            LIMIT 5
        ''')
        top_senders = [(row['name'], row['count']) for row in cursor.fetchall()]

        # Người gửi nhiều nhất
        top_contributor = top_senders[0][0] if top_senders else "Chưa có"

        return {
            'total_messages': total_messages,
            'unique_senders': unique_senders,
            'top_senders': top_senders,
            'top_contributor': top_contributor
        }
