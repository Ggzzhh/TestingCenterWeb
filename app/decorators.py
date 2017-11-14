# -*- coding: utf-8 -*-
from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user, login_required, logout_user

from .models import Administrator


def super_admin_required(func):
    """检查是否是超级管理员"""
    @wraps(func)
    def decorator_function(*args, **kwargs):
        admin = Administrator.query.first()
        if current_user.id != admin.id or current_user.username != \
                admin.username:
            abort(403)
        return func(*args, **kwargs)
    return decorator_function


def user_required(func):
    """检查是否是普通用户"""
    @wraps(func)
    def decorator_function(*args, **kwargs):
        if hasattr(current_user, 'info_count'):
            pass
        else:
            logout_user()
        return func(*args, **kwargs)
    return decorator_function

