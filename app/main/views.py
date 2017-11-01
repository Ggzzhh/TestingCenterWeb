# -*- coding: utf-8 -*-
import os
from flask import url_for, render_template, redirect, \
    jsonify, request, current_app, flash
from werkzeug.utils import secure_filename
from flask_login import logout_user, login_user, current_user

from . import main
from ..models import WebSetting, User

# 允许的类型
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@main.route('/')
def index():
    setting = WebSetting.query.first()
    return render_template("index.html", setting=setting)


@main.route('/register')
def register():
    return render_template("register.html")


@main.route('/login')
def login():
    return render_template("login.html")


@main.route('/register_ok')
def register_ok():
    flash('注册成功，请前往邮箱进行验证后登录!')
    return render_template("login.html")


def allowed_file(filename):
    """验证文件类型是否符合条件"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/upload', methods=["POST", "GET"])
def upload():
    """配合wongEditor多图片上传"""
    file_urls = []
    if request.method == 'POST':
        files = request.files.getlist("File")
        print(files)
        for file in files:
            print(file)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_url = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                        filename)
                file.save(file_url)
                file_url = url_for('static', filename='image/' + filename)
                file_urls.append(file_url)
    json_data = {
        'errno': 0,
        'data': file_urls,
        'status': 'true'
    }
    return jsonify(json_data)
