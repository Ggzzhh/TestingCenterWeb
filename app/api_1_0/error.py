# -*- coding: utf-8 -*-

from flask import jsonify
from app.exceptions import ValidationError
from . import api


def bad_request(message):
    """400状态码错误处理 错误的请求"""
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    """401状态码错误处理 未经授权的访问"""
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    """403状态码错误处理 禁止访问"""
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    """验证错误处理机制"""
    return bad_request(e.args[0])