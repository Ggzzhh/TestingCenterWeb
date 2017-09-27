# -*- coding: utf-8 -*-
import os
from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app.models import Administrator

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, admin=Administrator)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
