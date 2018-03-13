from os.path import isdir
from random import SystemRandom
from shutil import rmtree
from string import ascii_lowercase, digits
from time import time

from app import db
from app import util_logger as logger
from app.database.models import Repo


class RepoUtils:
    @staticmethod
    def update_timestamp(identifier):
        Repo.query.filter_by(id=identifier).update(dict(last_used='%s' % int(time())))
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
    def get_repo_count(active: bool = None) -> int:
        if active is not None:
            return len(Repo.query.filter_by(active=active).all())
        else:
            return len(Repo.query.all())

    @staticmethod
    def clean_repositories(repos):
        cleaned = 0
        for repo in repos:
            if repo is not None and isdir(repo.path):
                try:
                    rmtree(repo.deploy_path)
                    cleaned += 1
                except OSError as exception:
                    logger.error(exception.strerror)
                finally:
                    repo.active = False
                    db.session.commit()

        return cleaned
