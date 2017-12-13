#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app.models import Administrator, WebSetting, \
    SecondPageName, Post, Activity, User

app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, admin=Administrator, web=WebSetting,
                spn=SecondPageName, post=Post, ac=Activity, user=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    """部署时运行"""
    from flask.ext.migrate import upgrade
    from app.models import User, Administrator

    # 把数据库迁移到最新版本
    upgrade()

    # 注册管理员账号
    Administrator.register_admin()

    # 注册前端管理员账号
    User.default_user()

if __name__ == "__main__":
    manager.run()
