from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions.db import get_db
from ..utils.helpers import form_any

bp = Blueprint("auth", __name__)

@bp.route("/select-role")
def select_role():
    if "user_id" in session:
        return redirect(url_for("main.home"))
    return render_template("select_role.html")

@bp.route("/login/<role>")
def login_by_role(role):
    return render_template("login.html", role=role)

@bp.route("/login", methods=["GET", "POST"])
def login():
    role = request.args.get("role")  # optional
    if request.method == "POST":
        username = form_any("email", "username", "TenDangNhap").lower()
        password = form_any("password", "MatKhau")

        db = get_db()
        user = db.execute(
            "SELECT MaTK, TenDangNhap, MatKhau, VaiTro FROM TAIKHOAN WHERE TenDangNhap = ?",
            (username,),
        ).fetchone()

        if user and check_password_hash(user["MatKhau"], password):
            session.clear()
            session["user_id"] = user["MaTK"]
            session["username"] = user["TenDangNhap"]
            session["role"] = user["VaiTro"]
            row = db.execute(
        "SELECT TenCN FROM CHUNHA WHERE MaTK = ?",
        (user["MaTK"],)
        ).fetchone()
            session["full_name"] = row["TenCN"] if row else user["TenDangNhap"]
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("main.home"))

        flash("Sai tài khoản hoặc mật khẩu.", "danger")

    return render_template("login.html", role=role)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    """Tạm thời: signup dùng để tạo tài khoản CHỦ NHÀ (TAIKHOAN + CHUNHA)."""
    if request.method == "POST":
        ten_cn = form_any("name", "TenCN", default="Chủ nhà")
        sdt = form_any("phone", "SDT", default=None)
        email = form_any("email", "TenDangNhap").lower()
        pw = form_any("password", "MatKhau")

        if not email or not pw:
            flash("Vui lòng nhập email & mật khẩu.", "danger")
            return render_template("signup.html")

        db = get_db()
        existed = db.execute(
            "SELECT 1 FROM TAIKHOAN WHERE TenDangNhap = ?",
            (email,),
        ).fetchone()
        if existed:
            flash("Email đã tồn tại.", "warning")
            return render_template("signup.html")

        pw_hash = generate_password_hash(pw)

        cur = db.cursor()
        # Chủ nhà: tạm map vào VaiTro='admin' theo schema hiện có
        cur.execute(
            "INSERT INTO TAIKHOAN (TenDangNhap, MatKhau, VaiTro) VALUES (?, ?, ?)",
            (email, pw_hash, "admin"),
        )
        ma_tk = cur.lastrowid

        cur.execute(
            "INSERT INTO CHUNHA (TenCN, SDT, Email, MaTK) VALUES (?, ?, ?, ?)",
            (ten_cn, sdt, email, ma_tk),
        )

        db.commit()
        flash("Đăng ký chủ nhà thành công. Vui lòng đăng nhập.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")

@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    step = request.args.get("step", "email")

    if step == "email" and request.method == "POST":
        email = request.form.get("email")
        if email:
            session["reset_email"] = email
            session["verification_code"] = "123456"
            flash(f"Mã xác thực đã được gửi đến {email} (demo: 123456).", "info")
            return redirect(url_for("auth.forgot_password", step="verify"))

    elif step == "verify" and request.method == "POST":
        code = request.form.get("code")
        if code == session.get("verification_code"):
            flash("Mã xác thực hợp lệ. Vui lòng nhập mật khẩu mới.", "success")
            return redirect(url_for("auth.forgot_password", step="reset"))
        else:
            flash("Mã xác thực không đúng. Vui lòng thử lại.", "danger")

    elif step == "reset" and request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        if new_password == confirm_password:
            email = session.get("reset_email")
            # Demo: chỉ flash, chưa update DB
            flash(f"Mật khẩu cho tài khoản {email} đã được đặt lại (demo).", "success")
            session.pop("reset_email", None)
            session.pop("verification_code", None)
            return redirect(url_for("auth.login"))
        else:
            flash("Mật khẩu không khớp, vui lòng nhập lại.", "danger")

    return render_template("forgot_password.html", step=step)

@bp.route("/logout")
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("auth.login"))
