# -*- coding: utf-8 -*-
import os
from datetime import datetime

from flask import url_for, render_template, redirect, \
    jsonify, request, current_app, flash, session
from werkzeug.utils import secure_filename
from flask_login import logout_user, login_user, current_user

from . import main
from ..models import WebSetting, User, Info, Activity, SecondPageName, Post
from ..decorators import user_required

# 允许的类型
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@main.route('/')
@user_required
def index():
    setting = WebSetting.query.first()
    return render_template("index.html", setting=setting)


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


@main.route('/activity')
@user_required
def show_activity():
    """展示所有活动"""
    condition = request.args.get('condition')
    if condition is None:
        condition = 'all'
    now = datetime.now()
    page = request.args.get('page', 1, type=int)
    if condition == 'start':
        pagination = Activity.query \
            .filter(Activity.start_date < now, Activity.end_date > now) \
            .order_by(Activity.timestamp.desc()) \
            .paginate(page, per_page=current_app.config['POSTS_PER_PAGE'],
                      error_out=True)
    elif condition == 'end':
        pagination = Activity.query \
            .filter(Activity.end_date < now) \
            .order_by(Activity.timestamp.desc()) \
            .paginate(page, per_page=current_app.config['POSTS_PER_PAGE'],
                      error_out=True)
    elif condition == 'future':
        pagination = Activity.query \
            .filter(Activity.start_date > now) \
            .order_by(Activity.timestamp.desc()) \
            .paginate(page, per_page=current_app.config['POSTS_PER_PAGE'],
                      error_out=True)
    else:
        pagination = Activity.query.order_by(
            Activity.timestamp.desc()).paginate(
            page, per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=True)
    activities = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = page - 1
    next_page = None
    if pagination.has_next:
        next_page = page + 1
    count = len(activities)
    return render_template('activity.html', activities=activities,
                           pagination=pagination, next_page=next_page,
                           prev_page=prev_page, count=count)


@main.route('/activity/<int:id>')
@user_required
def activity(id):
    """活动详情页"""
    ac = Activity.query.get_or_404(id)
    return render_template('show-activity.html', ac=ac)


@main.route('/posts/<int:id>')
@user_required
def show_posts(id):
    """展示某类文章"""
    name = SecondPageName.query.filter_by(id=id).first().page_name
    return render_template('posts.html', id=id, name=name)


@main.route('/post/<int:id>')
@user_required
def show_post(id):
    """展示某文章"""
    post = Post.query.get_or_404(id)
    author = WebSetting.query.first().corporate_name
    return render_template('post.html', post=post, author=author,
                           comments=post.comments)
