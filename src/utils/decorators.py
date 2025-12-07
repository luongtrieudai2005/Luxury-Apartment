from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Vui lòng đăng nhập trước.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            role = session.get("role")
            if role not in roles:
                flash("Bạn không có quyền truy cập.", "danger")
                return redirect(url_for("main.home"))
            return view(*args, **kwargs)
        return wrapped
    return decorator
