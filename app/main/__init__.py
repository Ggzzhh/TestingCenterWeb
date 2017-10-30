# -*- coding: utf-8 -*-

# 注册蓝本 必须用下列顺序 避免陷入循环依赖
from flask import Blueprint, current_app

main = Blueprint('main', __name__)

from . import errors, views

from .. import db
from ..models import SecondPageName, WebSetting, FriendLink, User


# 返回数据库内的页面标题以及url
@main.context_processor
def get_page_names():
    """获得二级页面的内容以及id"""
    data = SecondPageName.query.all()
    names = {}
    for name in data:
        names[name.page_name] = name.id
    return dict(names=names)


@main.context_processor
def get_setting():
    """获得设置"""
    data = WebSetting.query.get(1)
    if data is not None:
        data = data.to_json()
        return dict(setting=data)
    return dict(setting=None)


@main.context_processor
def get_links():
    """获得设置"""
    links = FriendLink.query.all()
    return dict(links=[link.to_json() for link in links])


def default_user():
    """自动注册一个id为999的管理者， 之后注册的用户id从1000开始"""
    user = User(id=999, is_admin=True,
                email=current_app.config['ADMIN_USERNAME'],
                username='admin')
    user.password = current_app.config['ADMIN_PASSWORD']
    db.session.add(user)
    db.session.commit()
