# -*- coding: utf-8 -*-

from flask import url_for, render_template, redirect, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from . import manage
from .forms import AdminLoginForm
from ..models import Administrator, Post, SecondPageName, Activity, WebSetting
from ..decorators import super_admin_required


@manage.route('/')
@login_required
@super_admin_required
def index():
    """管理页面首页"""
    return render_template('admin/index.html')


@manage.route('/login', methods=["POST", "GET"])
def login():
    """管理系统登录页面"""
    admin = Administrator.query.first()
    if admin is None:
        Administrator.register_admin()
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Administrator.query.filter_by(username=form.username.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            login_user(admin)
            return redirect(request.args.get('next') or url_for('manage.index'))
        flash('用户名或密码错误！')
    return render_template('admin/login.html', form=form)


@manage.route('/logout')
@login_required
@super_admin_required
def logout():
    """管理系统登出"""
    logout_user()
    flash('退出成功')
    return redirect(url_for('manage.login'))


@manage.route('/setting')
@login_required
@super_admin_required
def web_setting():
    """管理系统相关设置"""
    return render_template('admin/setting.html')


@manage.route('/nav_setting')
@login_required
@super_admin_required
def nav_setting():
    """导航栏相关设置"""
    return render_template('admin/nav-setting.html')


@manage.route('/posts/<int:category_id>')
@login_required
@super_admin_required
def posts(category_id):
    """根据类别展示相应的页面"""
    category = SecondPageName.query.get_or_404(category_id)
    return render_template('admin/posts.html', category=category)


@manage.route('/new-posts/<category_id>', methods=["GET","POST"])
@login_required
@super_admin_required
def new_post(category_id):
    """发布一篇新文章的页面"""
    category = SecondPageName.query.get_or_404(category_id)
    return render_template('admin/post.html', category=category, id=0)


@manage.route('/post/<int:id>')
@login_required
@super_admin_required
def get_post(id):
    """获得某文章的编辑页面"""
    post = Post.query.get_or_404(id)
    return render_template('admin/post.html', category=post.category,
                           id=post.id)


@manage.route('/activities')
@login_required
@super_admin_required
def show_activities():
    """显示活动页面"""
    return render_template('admin/activity.html')


@manage.route('/new-activity')
@login_required
@super_admin_required
def new_activity():
    """新建一个活动"""
    return render_template('admin/new-activity.html')


@manage.route('/activity/<int:id>')
@login_required
@super_admin_required
def edit_activity(id):
    """展示页面"""
    activity = Activity.query.get_or_404(id)
    return render_template('admin/edit-activity.html', activity=activity)


@manage.route('/other')
@login_required
@super_admin_required
def other():
    """其余设置"""
    return render_template('admin/other.html')


# todo: 打印/生成活动报名表
