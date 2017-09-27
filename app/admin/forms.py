# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class AdminLoginForm(FlaskForm):
    """管理员登录表单"""
    username = StringField("账号:", validators=[DataRequired()])
    password = PasswordField("密码:", validators=[DataRequired()])
    submit = SubmitField("提交")
