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


class Administrator(UserMixin, db.Model):
    """管理员表 整个网站只设置一个管理员"""

    def __init__(self, **kwargs):
        super(Administrator, self).__init__(**kwargs)
        try:
            Administrator.query.first()
        except:
            self.register_admin()

    __tablename__ = 'administrator'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
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
        db.drop_all()
        db.create_all()
        only_admin = Administrator(username=current_app.config['ADMIN_USERNAME'])
        only_admin.password = current_app.config['ADMIN_PASSWORD']
        db.session.add(only_admin)
        db.session.commit()
