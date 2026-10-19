import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from database import (
    init_db,
    get_all_entries,
    add_entry,
    delete_entry,
    get_statistics,
    JSON_PATH
)

app = Flask(__name__)
app.secret_key = 'vibe-secret-guestbook-key-2026'

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
STATS_IMG = os.path.join(STATIC_DIR, 'stats.png')

# Khởi tạo Database khi server khởi động
init_db()


def generate_vibe_chart(top_senders):
    """
    Tạo biểu đồ Matplotlib với phong cách Dark Mode hiện đại (Vibe Aesthetic).
    Lưu trực tiếp vào vibe_code/static/stats.png.
    """
    os.makedirs(STATIC_DIR, exist_ok=True)

    # Cấu hình kích thước và font
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=140)
    fig.patch.set_facecolor('#0f172a')  # Nền tối hiện đại (slate-900)
    ax.set_facecolor('#1e293b')         # Nền trục slate-800

    if top_senders:
        names = [item[0] for item in top_senders]
        counts = [item[1] for item in top_senders]

        # Bảng màu neon pastel hiện đại
        vibe_colors = ['#8b5cf6', '#06b6d4', '#ec4899', '#10b981', '#f59e0b']
        colors = vibe_colors[:len(names)]

        # Vẽ bar chart
        bars = ax.bar(names, counts, color=colors, width=0.55, edgecolor='#334155', linewidth=1.2)

        # Hiển thị số lượng ngay trên đầu mỗi cột
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f'{int(height)}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=11, fontweight='bold',
                color='#f8fafc'
            )

        # Tiêu đề và nhãn
        ax.set_title('Top Người Gửi Lời Nhắn Nhiều Nhất', fontsize=14, fontweight='bold', color='#f8fafc', pad=18)
        ax.set_xlabel('Người gửi', fontsize=11, fontweight='600', color='#94a3b8', labelpad=10)
        ax.set_ylabel('Số lượng lời nhắn', fontsize=11, fontweight='600', color='#94a3b8', labelpad=10)

        # Format trục Y số nguyên
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.set_ylim(0, max(counts) * 1.25 if counts else 5)

        # Tùy chỉnh tick marks
        ax.tick_params(colors='#94a3b8', labelsize=10)
        plt.xticks(rotation=20, ha='right', color='#e2e8f0', fontweight='500')

        # Đường lưới mờ tinh tế
        ax.grid(axis='y', linestyle='--', alpha=0.25, color='#64748b')
        ax.set_axisbelow(True)

    else:
        # Khi chưa có lời nhắn
        ax.text(
            0.5, 0.5,
            '✨ Chưa có dữ liệu lời nhắn để vẽ biểu đồ ✨',
            ha='center', va='center',
            fontsize=13, fontweight='600',
            color='#94a3b8'
        )
        ax.set_xticks([])
        ax.set_yticks([])

    # Ẩn các đường viền cạnh trên và phải
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_color('#475569')

    plt.tight_layout()
    plt.savefig(STATS_IMG, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()


@app.route('/', methods=['GET'])
def index():
    """Trang chủ: hiển thị danh sách lời nhắn."""
    entries = get_all_entries()
    stats_data = get_statistics()
    return render_template(
        'index.html',
        entries=entries,
        stats=stats_data
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Trang thêm lời nhắn mới (GET: form, POST: xử lý và validate)."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()

        # Kiểm tra không để trống cả 2 trường
        if not name or not message:
            return render_template(
                'add.html',
                error="Vui lòng điền đầy đủ cả tên và nội dung lời nhắn!",
                name=name,
                message=message
            )

        success, err = add_entry(name, message)
        if not success:
            return render_template('add.html', error=err, name=name, message=message)

        flash('🎉 Lời nhắn của bạn đã được lưu vào Guestbook thành công!', 'success')
        return redirect(url_for('index'))

    # GET request
    return render_template('add.html')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """Xóa lời nhắn theo ID và chuyển hướng về trang chủ."""
    delete_entry(id)
    flash(f'🗑️ Đã xóa lời nhắn #{id} thành công.', 'info')
    return redirect(url_for('index'))


@app.route('/stats', methods=['GET'])
def stats():
    """Trang thống kê cơ bản và biểu đồ Matplotlib."""
    stats_data = get_statistics()
    
    # Tạo lại biểu đồ với dữ liệu mới nhất
    generate_vibe_chart(stats_data['top_senders'])

    return render_template(
        'stats.html',
        total_messages=stats_data['total_messages'],
        unique_senders=stats_data['unique_senders'],
        top_senders=stats_data['top_senders'],
        top_contributor=stats_data['top_contributor'],
        timestamp=int(time.time())
    )


@app.route('/export-data', methods=['GET'])
def export_data():
    """Tải xuống file data.json chứa toàn bộ lời nhắn."""
    if os.path.exists(JSON_PATH):
        return send_file(JSON_PATH, as_attachment=True, download_name='guestbook_data.json')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Chạy ở cổng 5001 để không xung đột với manual app
    app.run(debug=True, port=5001)
