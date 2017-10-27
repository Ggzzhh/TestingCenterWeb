# -*- coding: utf-8 -*-
import json
from datetime import datetime
from flask import jsonify, request, flash, current_app, url_for, abort
from flask_login import login_required

from . import api
from .. import db
from ..models import WebSetting, SecondPageName, Post, Activity, FriendLink


@api.route('/web-setting')
@login_required
def web_setting():
    """获取网站设置"""
    setting = WebSetting.query.first()
    if setting is None:
        return jsonify({'value': 'None'})
    return jsonify(setting.to_json())


@api.route('/web-setting', methods=["POST", "PUT"])
@login_required
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


@api.route('/nav-setting', methods=["GET"])
@login_required
def get_nav_setting():
    """获取导航设置"""
    nav_names = SecondPageName.query.all()
    if not nav_names:
        return jsonify({'num': 0, 'lacks': [1, 2, 3]})
    return jsonify(SecondPageName().to_json())


@api.route('/nav-setting', methods=['POST', 'PUT'])
@login_required
def update_nav_setting():
    """更新导航设置"""
    json_data = request.get_json()
    nav_settings = SecondPageName().from_json(json_data)
    if json_data is None or nav_settings is None or json_data['num'] > 3:
        return jsonify({'result': 'error'})
    for nav_setting in nav_settings:
        db.session.add(nav_setting)
    db.session.commit()
    return jsonify({'result': 'ok'})


@api.route('/nav-setting/<int:id>', methods=['DELETE'])
@login_required
def delete_nav_setting(id):
    """删除导航设置"""
    nav = SecondPageName.query.filter_by(id=id).first()
    if nav is not None:
        db.session.delete(nav)
        db.session.commit()
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/posts/<int:id>')
def get_posts(id):
    """获取某类别的文章"""
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(category_id=id).order_by(
        Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=True)
    posts = pagination.items
    # 上一页
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', id=id, page=page-1, _external=True)
    # 下一页
    next = None
    new_page = None
    if pagination.has_next:
        next = url_for('api.get_posts', id=id, page=page+1, _external=True)
        new_page = page + 1

    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total,
        'new_page': new_page
    })


@api.route('/post/<int:id>')
def get_post(id):
    """获得某文章"""
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/new-post/<int:id>', methods=["POST", "PUT"])
@login_required
def new_post(id):
    """新建一篇文章"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error'}), 400
    post = Post.from_json(json_data)
    if SecondPageName.query.filter_by(id=id).first():
        post.category_id = id
        db.session.add(post)
        db.session.commit()
        return jsonify({'result': 'ok'}), 201
    return jsonify({'result': 'error'}), 400


@api.route('/posts/<int:id>', methods=["DELETE"])
@login_required
def delete_post(id):
    """删除某类别中的指定文章"""
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'result': 'ok'})


@api.route('/edit-post/<int:id>', methods=["POST", "PUT"])
@login_required
def edit_post(id):
    """编辑文章"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error'})
    post = Post.from_json(json_data)
    db.session.add(post)
    db.session.commit()
    return jsonify({'result': 'ok'})


@api.route('/activity', methods=["POST"])
@login_required
def activity():
    """新增活动或修改"""
    json_data = request.get_json()
    if json_data is None or json_data.get('title') == '':
        return jsonify({'result': 'error'})
    activity = Activity.from_json(json_data)
    db.session.add(activity)
    db.session.commit()
    return jsonify({'result': 'ok'})


@api.route('/activities')
def get_activities():
    """获得所有活动的分页"""
    condition = request.args.get('condition')
    now = datetime.now()
    page = request.args.get('page', 1, type=int)
    if condition == 'start':
        pagination = Activity.query\
            .filter(Activity.start_date < now, Activity.end_date > now)\
            .order_by(Activity.timestamp.desc())\
            .paginate(page, per_page=current_app.config['POSTS_PER_PAGE'],
                      error_out=True)
    if condition == 'end':
        pagination = Activity.query\
            .filter(Activity.end_date < now)\
            .order_by(Activity.timestamp.desc())\
            .paginate(page, per_page=current_app.config['POSTS_PER_PAGE'],
                      error_out=True)
    if condition == 'future':
        pagination = Activity.query \
            .filter(Activity.start_date > now) \
            .order_by(Activity.timestamp.desc()) \
            .paginate(page, per_page=current_app.config['POSTS_PER_PAGE'],
                      error_out=True)
    if condition == 'all':
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
    return jsonify({
        'activities': [activity.to_json(brief=True) for activity in activities],
        'prev_page': prev_page,
        'next_page': next_page
    })


@api.route('/activity/<int:id>')
def get_activity(id):
    """获取某活动内容"""
    activity = Activity.query.get_or_404(id)
    return jsonify(activity.to_json())


@api.route('/activity/<int:id>', methods=["DELETE"])
@login_required
def delete_activity(id):
    """删除某活动"""
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return jsonify({'result': 'ok'})


@api.route('/friend-links')
def get_links():
    """获得友情链接"""
    links = FriendLink.query.all()
    return jsonify({'links': [link.to_json() for link in links]})


@api.route('/new-link', methods=["POST"])
@login_required
def new_link():
    """新增友情链接"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error'})
    link = FriendLink.from_json(json_data)
    db.session.add(link)
    db.session.commit()
    return jsonify({'result': 'ok'})


@api.route('/link/<int:id>', methods=["POST", "PUT"])
@login_required
def update_link(id):
    """修改友情链接"""
    link = FriendLink.query.get_or_404(id)
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error'})
    link.name = json_data.get('name')
    link.url = json_data.get('url')
    db.session.add(link)
    db.session.commit()
    return jsonify({'result': 'ok'}), 201


@api.route('/link/<int:id>', methods=["DELETE"])
@login_required
def delete_link(id):
    link = FriendLink.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    return jsonify({'result': 'ok'}), 201
