from flask import Blueprint, render_template, request, flash

bp = Blueprint("support", __name__)

@bp.route("/support", methods=["GET", "POST"])
def support():
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            flash("Yêu cầu của bạn đã được ghi nhận! Chúng tôi sẽ phản hồi sớm nhất có thể.", "success")
        else:
            flash("Vui lòng mô tả vấn đề bạn đang gặp.", "warning")
    return render_template("support.html")
