# -*- coding: utf-8 -*-
from datetime import datetime
from flask import jsonify, request, flash, current_app, url_for, abort, session
from flask_login import login_required, login_user, logout_user

from . import api
from .. import db
from ..models import User
from ..email import send_email


@api.route('/repeat', methods=["POST"])
def repeat():
    """检验用户名或者邮箱是否存在"""
    json_data = request.get_json()
    data = None
    if json_data is not None:
        if json_data.get('username') is not None:
            data = User.query.filter_by(username=json_data['username']).first()
        if json_data.get('email') is not None:
            data = User.query.filter_by(email=json_data['email']).first()
    if data is not None:
        return jsonify({'repeat': True})
    return jsonify({'repeat': False})


@api.route('/register', methods=['POST'])
def register():
    """用户注册"""
    if User.query.get(999) is None:
        User.default_user()
    json_data = request.get_json()
    if json_data is not None:
        user = User.from_json(json_data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认你的账户', 'auth/email/confirm', user=user,
                   token=token)
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/login', methods=["POST"])
def login():
    """用户登陆"""
    session.permanent = True
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'null'})
    username = json_data.get('username')
    password = json_data.get('password')
    if username is None:
        email = json_data.get('email')
        user = User.query.filter_by(email=email).first()
    else:
        user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'result': 'error'})
    if user.verify_password(password) and user.id >= 999:
        login_user(user)
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/reset-password', methods=["POST"])
def reset_password():
    """重置密码接口"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error'})
    email = json_data.get('email')
    user = User.query.filter_by(email=email).first()
    if user is not None:
        token = user.generate_confirmation_token()
        send_email(user.email, '重置密码', 'auth/email/reset_password',
                   user=user, token=token)
        return jsonify({'result': '有一封确认邮件发送到了你的邮箱，请去邮箱查看并完成密码重置！'})
    return jsonify({'result': 'None'})


@api.route('/change-password/<int:id>', methods=["POST"])
@login_required
def change_password(id):
    """修改密码"""
    json_data = request.get_json()
    user = User.query.get_or_404(id)
    if json_data is None:
        return jsonify({'result': 'error'})
    password = json_data.get('password')
    if password is not None:
        user.password = password
        db.session.add(user)
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/auth/<int:id>')
def get_user(id):
    """获取用户信息"""
    user = User.query.get_or_404(id)
    return jsonify(user.easy_to_json())