from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint("iot", __name__, url_prefix="/iot")
api = Blueprint("iot_api", __name__, url_prefix="/api/iot")

@bp.route("/dashboard")
def dashboard():
    return render_template("iot_dashboard.html")

@bp.route("/devices")
def devices():
    return render_template("iot_devices.html")

@bp.route("/energy-monitoring")
def energy_monitoring():
    return render_template("energy_monitoring.html")

@bp.route("/alerts")
def alerts():
    return render_template("iot_alerts.html")

@bp.route("/simulator")
def simulator():
    return render_template("iot_simulator.html")

@api.route("/readings", methods=["POST"])
def receive_iot_data():
    """Nhận dữ liệu từ cảm biến IoT (demo)"""
    data = request.get_json()
    return {"status": "success", "message": "Data received", "data": data}

@api.route("/control", methods=["POST"])
def control_device():
    """Điều khiển thiết bị IoT (demo)"""
    device_id = request.form.get("device_id")
    action = request.form.get("action")
    flash(f"Đã gửi lệnh {action} đến thiết bị {device_id}", "success")
    return redirect(request.referrer or url_for("iot.devices"))
