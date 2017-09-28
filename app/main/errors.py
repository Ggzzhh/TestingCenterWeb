#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(403)
def no_access_error(e):
    """处理403错误 禁止访问"""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    """检查Accept请求首部的值，决定客户端期望收到的响应格式"""
    # 首部中的MIME格式为json且不为html 就运行代码块
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        # 创建json格式的响应 内容是错误：未找到 响应码为404
        response = jsonify({'error': 'Not Found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """处理错误500 内部服务器错误"""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500



