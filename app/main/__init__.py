# -*- coding: utf-8 -*-

# 注册蓝本 必须用下列顺序 避免陷入循环依赖
from flask import Blueprint

main = Blueprint('admin', __name__)

from . import errors, views