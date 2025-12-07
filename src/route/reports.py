from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint("reports", __name__, url_prefix="/reports")

@bp.route("")
@bp.route("/")
def index():
    return render_template("reports_dashboard.html")

@bp.route("/revenue")
def revenue_report():
    return render_template("revenue_report.html")

@bp.route("/generate", methods=["POST"])
def generate_report():
    report_type = request.form.get("report_type")
    flash(f"Đã tạo báo cáo {report_type} (demo).", "success")
    return redirect(url_for("reports.index"))

@bp.route("/export/<format>/<report_type>")
def export_report(format, report_type):
    flash(f"Đang xuất báo cáo {report_type} dạng {format.upper()}... (demo)", "info")
    return redirect(url_for("reports.index"))
