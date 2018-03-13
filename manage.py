#!./venv/bin/python3

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import app, db
from app.database.models import Repo

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Repo=Repo)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


manager.add_command('database', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
