#!/usr/bin/env python

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_script import Shell

from app import create_app, db
from app.database.models import Repo

app = create_app(os.getenv('flask_environment') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def create_shell_context():
    return dict(app=app, db=db, Repo=Repo)


manager.add_command('shell', Shell(make_context=create_shell_context()))
manager.add_command('database', MigrateCommand)

if __name__ == "__main__":
    manager.run()
