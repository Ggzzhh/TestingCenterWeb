# -*- coding: utf-8 -*-

from flask import url_for, request, jsonify

from . import manage


@manage.route('/')
def admin_index():
    """管理页面首页"""

    message = {
        'msg1': '这是信息1',
        'msg2': {
            'msg2-1': '信息2-1',
            'msg2-2': '信息2-2'
        }
    }

    return jsonify(message)


@manage.route('/', methods=["POST", "PUT"])
def admin_test_new():
    """测试用"""
    data = request.json
    print(data)
    if data.get('msg') is not None:
        return jsonify({'msg': '成功'}, 201)
