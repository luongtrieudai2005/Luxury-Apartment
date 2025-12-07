from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint("core", __name__)

@bp.route("/register-stay", methods=["GET", "POST"])
def register_stay():
    """Đăng ký lưu trú"""
    if request.method == "POST":
        fullname = request.form.get("fullname")
        flash(f"Đăng ký lưu trú cho {fullname} thành công (demo).", "success")
        return redirect(url_for("core.register_stay"))
    return render_template("register_stay.html")

@bp.route("/houses")
def manage_houses():
    """Quản lý nhà/hợp đồng"""
    return render_template("manage_houses.html")

@bp.route("/bookings")
def bookings():
    """Quản lý đặt phòng"""
    return render_template("booking_management.html")

@bp.route("/contracts")
def contracts():
    """Quản lý hợp đồng thuê"""
    from_booking = request.args.get("from_booking")
    return render_template("contract_management.html", from_booking=from_booking)

@bp.route("/utilities")
def utilities():
    """Quản lý chỉ số điện nước"""
    return render_template("electric_water_readings.html")

@bp.route("/parking")
def parking():
    """Quản lý phương tiện"""
    return render_template("parking_vehicles.html")

@bp.route("/services")
def services():
    """Quản lý dịch vụ khác"""
    return render_template("other_services.html")

@bp.route("/requests")
def requests_feedback():
    """Yêu cầu/Phản ánh"""
    return render_template("requests_feedback.html")
