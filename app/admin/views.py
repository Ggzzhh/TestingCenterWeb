# -*- coding: utf-8 -*-

from flask import url_for, render_template, redirect, request
from flask_login import login_user, logout_user, login_required, current_user

from . import manage
from .forms import AdminLoginForm
from ..models import Administrator


@manage.route('/')
@login_required
def index():
    """管理页面首页"""
    return render_template('admin/index.html')


@manage.route('/login', methods=["POST", "GET"])
def login():
    """后台管理登录页面"""
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Administrator()
        admin = admin.query.filter_by(username=form.username.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            login_user(admin)
            return redirect(request.args.get('next') or url_for('manage.index'))
    return render_template('admin/login.html', form=form)
