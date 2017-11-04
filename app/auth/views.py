#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import url_for, render_template, redirect, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from ..models import User


@auth.before_app_request
def before_request():
    """在每次请求前运行的函数 钩子函数"""
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            print(request.endpoint)
            return redirect(url_for('auth.unconfirmed'))
        

@auth.route('/index')
def index():
    """用户资料首页"""
    return render_template('auth/index.html')


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/register')
def register():
    return render_template("auth/register.html")


@auth.route('/login')
def login():
    """用户登陆"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template("auth/login.html")


@auth.route('/logout/<username>')
def logout(username):
    """用户登出"""
    if current_user.username == username:
        logout_user()
        flash('你已登出！')
    return redirect(request.args.get('next') or url_for('auth.login'))


@auth.route('/register/ok')
def register_ok():
    flash('注册成功，请前往邮箱进行验证!')
    return render_template("auth/login.html")


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    # 查看用户的验证状态,如果为true 则去向首页
    if current_user.confirmed:
        return redirect(url_for('auth.index'))
    # 否则就进行验证
    if current_user.confirm(token):
        flash("完成验证，谢谢您的配合！")
    else:
        flash("验证无效或已过期，请重新验证邮箱！")
    return redirect(url_for('auth.index'))