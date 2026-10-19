import os
import json
import time
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Thiết lập font chữ hỗ trợ tiếng Việt trên Windows
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Tahoma', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
STATS_IMG = os.path.join(os.path.dirname(__file__), 'static', 'stats.png')


def load_entries():
    """Đọc dữ liệu từ file JSON nếu có (Yêu cầu Buổi 2)."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_entries(entries_list):
    """Ghi dữ liệu vào file JSON để không mất khi tắt app (Yêu cầu Buổi 2)."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries_list, f, ensure_ascii=False, indent=2)


# Khởi tạo dữ liệu từ file JSON khi ứng dụng khởi động
entries = load_entries()
next_id = max([e['id'] for e in entries], default=0) + 1


@app.route('/', methods=['GET'])
def index():
    """Trang chủ: hiển thị danh sách tất cả lời nhắn đã lưu."""
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Trang thêm lời nhắn mới (GET: form, POST: validate và lưu vào JSON)."""
    global next_id, entries
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()

        # Kiểm tra không để trống cả 2 trường
        if not name or not message:
            return render_template(
                'add.html',
                error="Vui lòng điền đầy đủ thông tin",
                name=name,
                message=message
            )

        # Thêm entry mới vào danh sách và lưu vào file JSON
        entries.append({
            'id': next_id,
            'name': name,
            'message': message
        })
        next_id += 1
        save_entries(entries)

        return redirect(url_for('index'))

    # GET request
    return render_template('add.html')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """Xóa lời nhắn theo ID và cập nhật lại file JSON."""
    global entries
    entries = [entry for entry in entries if entry['id'] != id]
    save_entries(entries)
    return redirect(url_for('index'))


@app.route('/stats', methods=['GET'])
def stats():
    """
    Trang thống kê và vẽ biểu đồ Matplotlib (Yêu cầu Buổi 2):
    1. Tổng số lời nhắn đã ghi
    2. Danh sách 5 người gửi nhiều lời nhắn nhất
    3. Biểu đồ cột lưu vào static/stats.png và nhúng vào HTML
    """
    total_messages = len(entries)
    sender_counts = Counter(e['name'] for e in entries)
    top_senders = sender_counts.most_common(5)

    # Đảm bảo thư mục static tồn tại
    os.makedirs(os.path.dirname(STATS_IMG), exist_ok=True)

    # Vẽ biểu đồ cột bằng matplotlib
    fig, ax = plt.subplots(figsize=(7, 4.5))

    if sender_counts:
        # Lấy danh sách người gửi để vẽ biểu đồ
        chart_data = sender_counts.most_common(8)
        names = [item[0] for item in chart_data]
        counts = [item[1] for item in chart_data]

        bars = ax.bar(names, counts, color='#3498db', edgecolor='#2980b9', width=0.55)

        # Hiển thị số lượng ngay trên đầu mỗi cột
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f'{int(height)}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=10, fontweight='bold'
            )

        ax.set_title('Số lượng lời nhắn theo người gửi', fontsize=13, fontweight='bold', pad=12)
        ax.set_xlabel('Người gửi', fontsize=11, labelpad=8)
        ax.set_ylabel('Số lượng lời nhắn', fontsize=11, labelpad=8)
        plt.xticks(rotation=20, ha='right')

        # Format trục Y luôn là số nguyên
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.set_ylim(0, max(counts) * 1.25)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
    else:
        ax.text(0.5, 0.5, 'Chưa có dữ liệu lời nhắn', ha='center', va='center', fontsize=12, color='#777')
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(STATS_IMG, dpi=120)
    plt.close()

    return render_template(
        'stats.html',
        total_messages=total_messages,
        top_senders=top_senders,
        timestamp=int(time.time())
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)