from flask import request

def form_any(*names, default=""):
    """Try multiple form field names and return the first non-empty value."""
    for n in names:
        v = request.form.get(n)
        if v is not None and str(v).strip() != "":
            return v.strip()
    return default
