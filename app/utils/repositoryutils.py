from os.path import isdir
from random import SystemRandom
from string import ascii_lowercase, digits
from time import time

from app import db
from app.database.models import Repo


class RepoUtils:
    @staticmethod
    def update_timestamp(identifier):
        repo = Repo.query.filter_by(id=identifier).update(dict(last_used='%s' % int(time())))
        db.session.commit()

    @staticmethod
    def get_expiration_date(identifier):
        repo = Repo.query.filter_by(id=identifier).first()
        return repo.last_used + (24 * 3600)

    @staticmethod
    def generate_id(length=16, chars=ascii_lowercase + digits):
        return ''.join(SystemRandom().choice(chars) for _ in range(length))

    @staticmethod
    def repository_exists(identifier):
        repo = Repo.query.filter_by(id=identifier).first()
        if repo is not None and isdir(repo.path):
            return True
        return False

    @staticmethod
    def get_current_repo_count():
        return len(Repo.query.filter_by(active=True).all())
