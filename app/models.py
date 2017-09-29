# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    """使用flask_login时必须实现的函数 返回None?"""
    return Administrator.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
    """匿名用户类"""
    def can(self):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class Administrator(UserMixin, db.Model):
    """管理员表 整个网站只设置一个管理员账号, 需要在命令行手动注册"""

    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("这不是一个可读属性")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码，返回布尔值"""
        return check_password_hash(self.password_hash, password)

    def register_admin(self):
        """注册管理员账号"""
        db.create_all()
        only_admin = Administrator(username=current_app.config['ADMIN_USERNAME'])
        only_admin.password = current_app.config['ADMIN_PASSWORD']
        db.session.add(only_admin)
        db.session.commit()


class WebSetting(db.Model):
    """网站设置"""
    __tablename__ = 'web_settings'
    id = db.Column(db.Integer, primary_key=True)
    corporate_name = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    address = db.Column(db.String(128))
    phone_num = db.Column(db.Integer)
    WeChat = db.Column(db.String(32))
    WeChat_img = db.Column(db.Text)
    sina_blog = db.Column(db.String(64))
    email = db.Column(db.String(32))
    contacts = db.Column(db.String(32))


class SecondPageName(db.Model):
    """发布文章二级页面名称管理表"""
    id = db.Column(db.Integer, primary_key=True)
    second_page_name = db.Column(db.String(32))