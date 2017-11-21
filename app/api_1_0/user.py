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


@api.route('/login', methods=["GET"])
def get_login():
    return jsonify({'result': 'error', 'msg': '用户需要登陆！请进入登录页面登录!'})


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
    if user.disable_time is not None:
        return jsonify({'result': 'disable', 'disable_time': user.disable_time})
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


@api.route('/auth/edit/<int:id>', methods=["POST"])
@login_required
def edit_user(id):
    """修改用户资料"""
    user = User.query.get_or_404(id)
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error'})
    user = user.from_json(json_data)
    db.session.add(user)
    db.session.commit()
    return jsonify({'result': 'ok'})


@api.route('/team', methods=["POST"])
@login_required
def new_team():
    """创建新队伍"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error'})
    team = Team.from_json(json_data)
    if team is not None:
        name = team.name
        db.session.add(team)
        db.session.commit()
        team = Team.query.filter_by(name=name).first()
        captain_id = json_data.get('captain_id')
        user = User.query.get_or_404(captain_id)
        user.team_id = team.id
        db.session.add(user)
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/team/<int:id>')
def get_team(id):
    """获取队伍信息"""
    return jsonify(Team.query.get_or_404(id).to_json())


@api.route('/team-exist')
@login_required
def team_exist():
    """检验队伍名是否存在"""
    name = request.args.get('name')
    return jsonify({'result': Team.name_is_exist(name)})


@api.route('/team/<int:id>', methods=["POST"])
@login_required
def update_team(id):
    team = Team.query.get_or_404(id)
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error'})
    team = team.from_json(json_data)
    db.session.add(team)
    db.session.commit()
    return jsonify({'result': 'ok'})


@api.route('/team/<int:id>', methods=["DELETE"])
@login_required
def delete_team(id):
    """删除战队"""
    team = Team.query.get_or_404(id)
    if current_user.id == team.captain_id:
        db.session.delete(team)
        db.session.commit()
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/team/<int:id>/new-player', methods=["POST"])
@login_required
def add_player(id):
    """添加队员"""
    team = Team.query.get_or_404(id)
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'error1'})
    if current_user.id == team.captain_id:
        email = json_data.get('email')
        if email:
            user = User.query.filter_by(email=email).first()
            if user is None:
                return jsonify({'result': 'None'})
            user.team_id = team.id
            db.session.add(team)
            return jsonify({'result': 'ok'})
        return jsonify({'result': 'None'})
    return jsonify({'result': 'error2'})


@api.route('/player/<int:id>', methods=["DELETE"])
@login_required
def delete_player(id):
    """删除队员"""
    user = User.query.get_or_404(id)
    try:
        user.team_id = None
        db.session.add(user)
        db.session.commit()
        return jsonify({'result': 'ok'})
    except:
        return jsonify({'result': 'error'})


@api.route('/message', methods=["POST"])
def add_message():
    """给某用户发送信息"""
    json_data = request.get_json()
    if json_data is not None and json_data.get('user_id') is not None:
        info = Info.from_json(json_data)
        db.session.add(info)
        db.session.commit()
        return jsonify({'result': 'ok'})
    else:
        return jsonify({'result': 'error'})


@api.route('/message/<int:id>', methods=["DELETE"])
def delete_msg(id):
    """删除信息"""
    msg = Info.query.get_or_404(id)
    try:
        msg.team_id = None
        db.session.delete(msg)
        db.session.commit()
        return jsonify({'result': 'ok'})
    except:
        return jsonify({'result': 'error'})


@api.route('/sign_up/solo', methods=["POST"])
def sign_up_solo():
    """单人活动报名"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'null'})
    user_id = json_data.get('user_id')
    user = User.query.get_or_404(user_id)
    activity_id = json_data.get('activity_id')
    activity = Activity.query.get_or_404(activity_id)
    if user not in activity.is_solo:
        activity.is_solo.append(user)
        db.session.add(activity)
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/sign_up/many', methods=["POST"])
def sign_up_many():
    """多人活动报名"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'null'})
    team_id = json_data.get('team_id')
    team = Team.query.get_or_404(team_id)
    activity_id = json_data.get('activity_id')
    activity = Activity.query.get_or_404(activity_id)
    if team not in activity.is_team:
        activity.is_team.append(team)
        db.session.add(activity)
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


@api.route('/comment', methods=["POST"])
@login_required
def add_comment():
    """添加评论"""
    json_data = request.get_json()
    if json_data is None:
        return jsonify({'result': 'null'})
    body = json_data.get('body')
    post = Post.query.get_or_404(json_data.get('post_id'))
    comment = Comment(body=body,
                      post=post,
                      author=current_user._get_current_object())
    db.session.add(comment)
    try:
        db.session.commit()
        return jsonify({'result': 'ok'})
    except:
        return jsonify({'result': 'error'})


@api.route('/comment/<int:id>', methods=["DELETE"])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user.is_admin or current_user.id == comment.author_id:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'result': 'ok'})
    return jsonify({'result': 'error'})


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
        community_comment = \
            CommunityComment(body=body,
                             post=post,
                             author=current_user._get_current_object())
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