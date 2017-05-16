import random
import string
import time
from os import listdir
from os.path import isdir
from os.path import join

from app import db
from app.database.models import Repo


class RepoUtils:
    @staticmethod
    def update_timestamp(identifier):
        repo = Repo.query.filter_by(id=identifier).update(dict(last_used='%s' % int(time.time())))
        db.session.commit()

    @staticmethod
    def get_expiration_date(identifier):
        repo = Repo.query.filter_by(id=identifier).first()
        return repo.last_used + (24 * 3600)

    @staticmethod
    def generate_id(length=16, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

    @staticmethod
    def repository_exists(identifier):
        if isdir(join(app.config['REPO_DIR'], identifier)):
            return True
        else:
            return False

    @staticmethod
    def get_current_repo_count():
        return len(listdir(app.config['REPO_DIR']))
