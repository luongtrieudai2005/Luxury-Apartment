import sqlite3
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, Response
from ..extensions.db import get_db
from ..utils.decorators import login_required

bp = Blueprint("profile", __name__)

@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    db = get_db()

    if request.method == "POST":
        f = request.files.get("avatar")
        if not f or f.filename == "":
            flash("Vui lòng chọn ảnh.", "warning")
            return redirect(url_for("profile.profile"))

        if f.mimetype not in {"image/png", "image/jpeg", "image/webp"}:
            flash("Chỉ hỗ trợ PNG / JPEG / WEBP.", "danger")
            return redirect(url_for("profile.profile"))

        data = f.read()
        if len(data) > 2 * 1024 * 1024:
            flash("Ảnh quá lớn (tối đa 2MB).", "danger")
            return redirect(url_for("profile.profile"))

        db.execute(
            "UPDATE TAIKHOAN SET Avatar = ?, AvatarMime = ? WHERE MaTK = ?",
            (sqlite3.Binary(data), f.mimetype, session["user_id"]),
        )
        db.commit()
        flash("Đã cập nhật avatar.", "success")
        return redirect(url_for("profile.profile"))

    user = db.execute(
        """
        SELECT tk.MaTK, tk.TenDangNhap, tk.VaiTro,
               COALESCE(cn.TenCN, nv.TenNV, kt.TenKT) AS HoTen,
               COALESCE(cn.SDT, kt.SDT) AS SDT,
               COALESCE(cn.Email, nv.Email, kt.Email) AS Email
        FROM TAIKHOAN tk
        LEFT JOIN CHUNHA   cn ON cn.MaTK = tk.MaTK
        LEFT JOIN NHANVIEN nv ON nv.MaTK = tk.MaTK
        LEFT JOIN KHACHTHUE kt ON kt.MaTK = tk.MaTK
        WHERE tk.MaTK = ?
        """,
        (session["user_id"],),
    ).fetchone()

    return render_template("profile.html", user=user)

@bp.route("/profile/avatar")
@login_required
def avatar_me():
    db = get_db()
    row = db.execute(
        "SELECT Avatar, AvatarMime FROM TAIKHOAN WHERE MaTK = ?",
        (session["user_id"],),
    ).fetchone()

    if not row or row["Avatar"] is None:
        return redirect(url_for("static", filename="img/avtmacdinh.jpg"))
        # hoặc: "img/avt.png"

    resp = Response(row["Avatar"], mimetype=row["AvatarMime"] or "application/octet-stream")
    resp.headers["Cache-Control"] = "no-store"
    return resp
