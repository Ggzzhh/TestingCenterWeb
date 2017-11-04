#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 注册蓝本 必须用下列顺序 避免陷入循环依赖
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views


from ..models import SecondPageName, WebSetting, FriendLink, User


# 返回数据库内的页面标题以及url
@auth.context_processor
def get_page_names():
    """获得二级页面的内容以及id"""
    data = SecondPageName.query.all()
    names = {}
    for name in data:
        names[name.page_name] = name.id
    return dict(names=names)


@auth.context_processor
def get_setting():
    """获得设置"""
    data = WebSetting.query.get(1)
    if data is not None:
        data = data.to_json()
        return dict(setting=data)
    return dict(setting=None)


@auth.context_processor
def get_links():
    """获得设置"""
    links = FriendLink.query.all()
    return dict(links=[link.to_json() for link in links])