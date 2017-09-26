# -*- coding: utf-8 -*-

# 导入依赖包
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail

# 导入配置
from config import config

# 初始化程序
bootstrap = Bootstrap()
login_manage = LoginManager()
db = SQLAlchemy()
moment = Moment()
mail = Mail()

# 设置登陆管理
# 用户会话安全等级
login_manage.session_protection = "strong"
# 要在用户登录时重定向到的视图的名称
login_manage.login_view = 'admin.login'
# 进行登录检查没有通过时显示的信息
login_manage.login_message = '该页面需要登录后才能访问'
# login_message的类型
login_manage.login_message_category = 'info'

app = Flask(__name__)