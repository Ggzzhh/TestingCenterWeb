# -*- coding: utf-8 -*-
import json
from flask import jsonify, request

from . import api
from .. import db
from ..models import WebSetting, SecondPageName


@api.route('/web_setting')
def web_setting():
    """获取网站设置"""
    setting = WebSetting.query.first()
    if setting is None:
        return jsonify({'value': 'None'})
    return jsonify(setting.to_json())


@api.route('/web_setting', methods=["POST", "PUT"])
def update_web_setting():
    """更新网站设置"""
    setting = WebSetting.query.first()
    if setting is None:
        setting = WebSetting()
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'value': 'None'})
    setting = setting.from_json(json_data)
    db.session.add(setting)
    db.session.commit()
    return jsonify(setting.to_json())


@api.route('/nav_setting', methods=["GET"])
def get_nav_setting():
    """更新导航设置"""
    nav_names = SecondPageName.query.all()
    if not nav_names:
        return jsonify({'num': 0})
    return jsonify(SecondPageName().to_json())

