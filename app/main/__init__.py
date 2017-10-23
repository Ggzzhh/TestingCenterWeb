# -*- coding: utf-8 -*-

# 注册蓝本 必须用下列顺序 避免陷入循环依赖
from flask import Blueprint

main = Blueprint('main', __name__)

from . import errors, views

from ..models import SecondPageName
# 返回数据库内的页面标题以及url
@main.context_processor
def get_page_names():
    """获得二级页面的内容以及id"""
    data = SecondPageName.query.all()
    names = {}
    for name in data:
        names[name.page_name] = name.id
    return dict(names=names)
