from flask import Blueprint, render_template, session, redirect, url_for, flash

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.route("/system-config")
def system_config():
    if "user_id" not in session:
        flash("Vui lòng đăng nhập để truy cập", "warning")
        return redirect(url_for("auth.login"))
    if session.get("role") != "admin":
        flash("Bạn không có quyền truy cập trang này", "danger")
        return redirect(url_for("main.home"))
    return render_template("system_config.html")

@bp.route("/user-management")
def user_management():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Bạn không có quyền truy cập", "danger")
        return redirect(url_for("main.home"))
    return render_template("user_management.html")

@bp.route("/price-config")
def price_config():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Bạn không có quyền truy cập", "danger")
        return redirect(url_for("main.home"))
    return render_template("price_config.html")

@bp.route("/backup-restore")
def backup_restore():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Bạn không có quyền truy cập", "danger")
        return redirect(url_for("main.home"))
    return render_template("backup_restore.html")
