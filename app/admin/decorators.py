from flask import abort, redirect
from flask_login import current_user

from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/admin/login')

        if not current_user.is_admin:
            return abort(403)

        return view_func(*args, **kwargs)

    return decorated_view
