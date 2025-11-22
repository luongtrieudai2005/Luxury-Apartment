from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__, static_folder="static", template_folder="app/templates")
app.config['SECRET_KEY'] = 'dev-secret-key'

# Demo data
listings = [
    {"id":1, "title":"Căn hộ 2PN - Trung tâm", "price":"7.000.000 VND/tháng", "location":"Quận 1", "img":"../static/img/Vector.png", "summary":"Gần chợ, đầy đủ nội thất"},
    {"id":2, "title":"Nhà trệt 3PN - Yên tĩnh", "price":"10.000.000 VND/tháng", "location":"Thủ Đức", "img":"../static/img/Vector.png", "summary":"Sân vườn, có gara"},
]

@app.route('/')
def home():
    return render_template('home.html', listings=listings)

# ============== AUTH ROUTES ==============
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
        flash('Đăng ký thành công (demo). Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    step = request.args.get('step', 'email')
    
    if step == 'email' and request.method == 'POST':
        email = request.form.get('email')
        if email:
            session['reset_email'] = email
            session['verification_code'] = '123456'
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

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/select-role')
def select_role():
    return render_template('select_role.html')

@app.route('/login/<role>')
def login_by_role(role):
    return render_template('login.html', role=role)

# ============== ACCOMMODATION MANAGEMENT (QUẢN LÝ LƯU TRÚ) ==============
@app.route('/register-stay', methods=['GET', 'POST'])
def register_stay():
    """Đăng ký lưu trú"""
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        flash(f'Đăng ký lưu trú cho {fullname} thành công (demo).', 'success')
        return redirect(url_for('register_stay'))
    return render_template('register_stay.html')

@app.route('/houses')
def manage_houses():
    """Quản lý nhà/hợp đồng"""
    return render_template('manage_houses.html')

# ============== BOOKING & CONTRACT MANAGEMENT (ĐẶT PHÒNG & HỢP ĐỒNG) ==============
@app.route('/bookings')
def bookings():
    """Quản lý đặt phòng"""
    return render_template('booking_management.html')

@app.route('/contracts')
def contracts():
    """Quản lý hợp đồng thuê"""
    from_booking = request.args.get('from_booking')
    return render_template('contract_management.html', from_booking=from_booking)

# ============== SERVICE MANAGEMENT (QUẢN LÝ DỊCH VỤ) ==============
@app.route('/utilities')
def utilities():
    """Quản lý chỉ số điện nước - electric_water_readings.html"""
    return render_template('electric_water_readings.html')

@app.route('/parking')
def parking():
    """Quản lý phương tiện - parking_vehicles.html"""
    return render_template('parking_vehicles.html')

@app.route('/services')
def services():
    """Quản lý dịch vụ khác - other_services.html"""
    return render_template('other_services.html')

@app.route('/requests')
def requests_feedback():
    """Yêu cầu/Phản ánh - requests_feedback.html"""
    return render_template('requests_feedback.html')

# ============== REPORTS & ANALYTICS (BÁO CÁO & THỐNG KÊ) ==============
@app.route('/reports')
def reports():
    """Dashboard tổng quan báo cáo và thống kê"""
    return render_template('reports_dashboard.html')

@app.route('/reports/revenue')
def revenue_report():
    """Báo cáo doanh thu chi tiết"""
    return render_template('revenue_detail.html')

@app.route('/reports/generate', methods=['POST'])
def generate_report():
    """API endpoint để tạo báo cáo động"""
    report_type = request.form.get('report_type')
    time_range = request.form.get('time_range')
    house_id = request.form.get('house_id')
    export_format = request.form.get('export_format')
    
    # TODO: Xử lý logic tạo báo cáo
    flash(f'Báo cáo {report_type} đã được tạo thành công (demo).', 'success')
    return redirect(url_for('reports'))

@app.route('/reports/export/<format>/<report_type>')
def export_report(format, report_type):
    """Xuất báo cáo ra PDF hoặc Excel"""
    # TODO: Implement export logic
    flash(f'Đang xuất báo cáo {report_type} dạng {format.upper()}... (demo)', 'info')
    return redirect(url_for('reports'))

# ============== SUPPORT (HỖ TRỢ) ==============
@app.route('/support', methods=['GET', 'POST'])
def support():
    """Trung tâm hỗ trợ"""
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            flash("Yêu cầu của bạn đã được ghi nhận! Chúng tôi sẽ phản hồi sớm nhất có thể.", "success")
        else:
            flash("Vui lòng mô tả vấn đề bạn đang gặp.", "warning")
    return render_template('support.html')

if __name__ == '__main__':
    app.run(debug=True)