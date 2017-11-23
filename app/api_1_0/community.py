# -*- coding: utf-8 -*-
from datetime import datetime
from flask import jsonify, request, flash, current_app, \
    url_for, abort, session, redirect
from flask_login import login_required, login_user, logout_user, current_user

from . import api
from .. import db
from ..models import User, Team, Info, Activity, Comment, \
    Post, CommunityComment, CommunityPost
from ..email import send_email


@api.route('/community-post', methods=["POST"])
@login_required
def add_community_post():
    """在论坛发布一篇新文章"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'null'})
    community_post = CommunityPost.from_json(json_data)
    community_post.author = current_user._get_current_object()
    db.session.add(community_post)
    try:
        db.session.commit()
        return jsonify({'result': 'ok'})
    except:
        return jsonify({'result': 'error'})


@api.route('/community-post/<int:id>', methods=["DELETE"])
@login_required
def delete_community_post(id):
    """删除论坛内某文章"""
    community_post = CommunityPost.query.get_or_404(id)
    if current_user.is_admin or current_user.id == community_post.author_id:
        db.session.delete(community_post)
        db.session.commit()
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/community-post/<int:id>', methods=["POST", "PUT"])
@login_required
def update_community_post(id):
    """修改论坛内某文章"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'null'})
    community_post = CommunityPost.query.get_or_404(id)
    if current_user.is_admin or current_user.id == community_post.author_id:
        community_post.timestamp = datetime.now()
        db.session.add(community_post.from_json(json_data))
        db.session.commit()
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/community-post/<int:id>')
def show_community_post(id):
    """返回论坛内某文章的内容"""
    community_post = CommunityPost.query.get_or_404(id)
    return jsonify({'community_post': community_post.to_json()})


@api.route('/community-comment', methods=["POST"])
@login_required
def add_community_comment():
    """在论坛发布新评论"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'null'})
    post = CommunityPost.query.get(json_data.get('post_id'))
    body = json_data.get('body')
    if post is not None and body is not None:
        post.last_comment_time = datetime.utcnow()
        community_comment = \
            CommunityComment(body=body,
                             post=post,
                             author=current_user._get_current_object())
        db.session.add(post)
        db.session.add(community_comment)
    try:
        db.session.commit()
        return jsonify({'result': 'ok'})
    except:
        return jsonify({'result': 'error'})


@api.route('/community-comment/<int:id>', methods=["DELETE"])
@login_required
def delete_community_comment(id):
    comment = CommunityComment.query.get_or_404(id)
    if current_user.is_admin or current_user.id == comment.author_id:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/community/hot')
def get_hot():
    """获取评论数最多的15个帖子"""
    all = CommunityPost.query.all()
    result = {}
    posts = []
    for post in all:
        result[post.id] = post.count()
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)[:15]
    for i in result:
        post = CommunityPost.query.get(i[0])
        posts.append(post.easy_to_json())
    return jsonify({'result': 'ok', 'posts': posts})


@api.route('/community/top')
@login_required
def do_top():
    """置顶某文章"""
    if current_user.is_admin:
        id = request.args.get('id')
        post = CommunityPost.query.get_or_404(id)
        post.top = 1
        db.session.add(post)
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/community/remove-top')
@login_required
def remove_top():
    """取消置顶某文章"""
    if current_user.is_admin:
        id = request.args.get('id')
        post = CommunityPost.query.get_or_404(id)
        post.top = 0
        db.session.add(post)
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})
