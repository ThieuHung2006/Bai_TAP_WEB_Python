from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dữ liệu lưu trữ in-memory (list toàn cục)
entries = []
next_id = 1


@app.route('/', methods=['GET'])
def index():
    """Trang chủ: hiển thị danh sách lời nhắn."""
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Trang thêm lời nhắn mới (GET: hiển thị form, POST: xử lý dữ liệu)."""
    global next_id
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()

        # Validate không rỗng
        if not name or not message:
            return render_template(
                'add.html',
                error="Vui lòng điền đầy đủ thông tin",
                name=name,
                message=message
            )

        # Thêm entry mới vào danh sách toàn cục
        entries.append({
            'id': next_id,
            'name': name,
            'message': message
        })
        next_id += 1

        return redirect(url_for('index'))

    # GET request
    return render_template('add.html')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """Xóa lời nhắn theo id và chuyển hướng về trang chủ."""
    global entries
    entries = [entry for entry in entries if entry['id'] != id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)