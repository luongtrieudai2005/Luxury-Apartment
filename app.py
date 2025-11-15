from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['SECRET_KEY'] = 'dev-secret-key'  # đổi trong production hoặc load từ .env

# Demo dữ liệu
listings = [
    {"id":1, "title":"Căn hộ 2PN - Trung tâm", "price":"7.000.000 VND/tháng", "location":"Quận 1", "img":"/static/img/house1.jpg", "summary":"Gần chợ, đầy đủ nội thất"},
    {"id":2, "title":"Nhà trệt 3PN - Yên tĩnh", "price":"10.000.000 VND/tháng", "location":"Thủ Đức", "img":"/static/img/house2.jpg", "summary":"Sân vườn, có gara"},
]

@app.route('/')
def home():
    return render_template('home.html', listings=listings)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            flash('Đăng nhập thành công (demo)', 'success')
            return redirect(url_for('home'))
        flash('Vui lòng nhập đầy đủ thông tin', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # demo: chỉ flash và redirect
        name = request.form.get('name')
        email = request.form.get('email')
        flash('Đăng ký thành công (demo). Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

from flask import Flask, render_template, request, redirect, url_for, flash, session

# Quên mật khẩu

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    step = request.args.get('step', 'email')  # bước hiện tại, mặc định là nhập email

    if step == 'email' and request.method == 'POST':
        email = request.form.get('email')
        if email:
            # Giả lập gửi mã xác thực
            session['reset_email'] = email
            session['verification_code'] = '123456'  # demo cố định
            flash(f'Mã xác thực đã được gửi đến {email} (demo: 123456).', 'info')
            return redirect(url_for('forgot_password', step='verify'))

    elif step == 'verify' and request.method == 'POST':
        code = request.form.get('code')
        if code == session.get('verification_code'):
            flash('Mã xác thực hợp lệ. Vui lòng nhập mật khẩu mới.', 'success')
            return redirect(url_for('forgot_password', step='reset'))
        else:
            flash('Mã xác thực không đúng. Vui lòng thử lại.', 'danger')

    elif step == 'reset' and request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password == confirm_password:
            email = session.get('reset_email')
            flash(f'Mật khẩu cho tài khoản {email} đã được đặt lại (demo).', 'success')
            session.pop('reset_email', None)
            session.pop('verification_code', None)
            return redirect(url_for('login'))
        else:
            flash('Mật khẩu không khớp, vui lòng nhập lại.', 'danger')

    return render_template('forgot_password.html', step=step)


# Logout
@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# Phân quyền đăng nhập
@app.route('/select-role')
def select_role():
    return render_template('select_role.html')

@app.route('/login/<role>')
def login_by_role(role):
    return render_template('login.html', role=role)

# Đăng kí lưu trú
@app.route('/register-stay', methods=['GET', 'POST'])
def register_stay():
    if request.method == 'POST':
        # Lấy dữ liệu demo
        fullname = request.form.get('fullname')
        flash(f'Đăng ký lưu trú cho {fullname} thành công (demo).', 'success')
        return redirect(url_for('register_stay'))
    return render_template('register_stay.html')

# Quản lý nhà, hợp đồng 
@app.route('/manage-houses')
def manage_houses():
    return render_template('manage_houses.html')

#Quản lý chỉ số điện nước
@app.route('/dien-nuoc')
def el_water():
    return render_template('el_water.html')

#Quản lý phương tiện 
@app.route('/phuong-tien')
def ql_xe():
    return render_template('ql_xe.html')

#Quản lý dịch vụ khác

@app.route('/dich-vu')
def ql_dichvukhac():
    return render_template('ql_dichvukhac.html')


#Yêu cầu/Phản ánh
@app.route('/yc-pa')
def yc_phananh():
    return render_template('yc_phananh.html')


# Cần hỗ trợ
@app.route('/sp', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        message = request.form.get('message')

        if message:
            flash("Yêu cầu của bạn đã được ghi nhận! Chúng tôi sẽ phản hồi sớm nhất có thể.", "success")
        else:
            flash("Vui lòng mô tả vấn đề bạn đang gặp.", "warning")

    return render_template('support.html')








if __name__ == '__main__':
    app.run(debug=True)
