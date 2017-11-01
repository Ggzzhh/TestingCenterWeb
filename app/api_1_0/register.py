# -*- coding: utf-8 -*-
from datetime import datetime
from flask import jsonify, request, flash, current_app, url_for, abort
from flask_login import login_required

from . import api
from .. import db
from ..models import User


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
    json_data = request.get_json()
    if json_data is not None:
        user = User.from_json(json_data)
        db.session.add(user)
        db.session.commit()
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})
