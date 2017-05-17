from os import listdir
from os.path import isdir, join
from random import SystemRandom
from string import ascii_lowercase, digits
from time import time

from app import db, current_config
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
        if isdir(join(current_config.REPO_PATH, identifier)):
            return True
        else:
            return False

    @staticmethod
    def get_current_repo_count():
        return len(listdir(current_config.REPO_PATH))
