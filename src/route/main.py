from flask import Blueprint, render_template, session, redirect, url_for
from ..model.demo_data import LISTINGS

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    # CHƯA đăng nhập -> đi chọn vai trò
    if "user_id" not in session:
        return redirect(url_for("auth.select_role"))
    # ĐÃ đăng nhập -> vào trang home bình thường
    return render_template("home.html", listings=LISTINGS)
