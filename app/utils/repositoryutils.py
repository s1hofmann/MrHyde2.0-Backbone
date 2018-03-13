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
    def calc_expiration_date(last_used: int) -> int:
        return last_used + (24 * 3600)

    @staticmethod
    def update_timestamp(identifier: str):
        logger.info("Updating timestamp for repo '%s'" % identifier)
        new_timestamp = int(time())
        Repo.query.filter_by(id=identifier).update(dict(last_used='%s' % new_timestamp))
        db.session.commit()
        logger.info("Updated timestamp for repo '%s', new timestamp: %s" % (identifier, new_timestamp))

    @staticmethod
    def get_expiration_date(identifier: str) -> int:
        repo = Repo.query.filter_by(id=identifier).first()
        expiry = RepoUtils.calc_expiration_date(repo.last_used)
        logger.info("Repo '%s' will expire at %s" % (identifier, expiry))
        return expiry

    @staticmethod
    def generate_id(length: int = 16, chars: str = ascii_lowercase + digits):
        return ''.join(SystemRandom().choice(chars) for _ in range(length))

    @staticmethod
    def repository_exists(identifier: str) -> bool:
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
    def get_inactive_repos():
        return Repo.query.filter_by(active=False).all()

    @staticmethod
    def get_expired_repos():
        return Repo.query.filter(RepoUtils.calc_expiration_date(Repo.last_used) < int(time())).all()

    @staticmethod
    def deactivate_expired_repos(repos: Repo):
        for repo in repos:
            repo.active = False
            db.session.commit()

    @staticmethod
    def clean_repositories(repos):
        cleaned = 0
        for repo in repos:
            if repo is not None and isdir(repo.path):
                logger.info("Trying to clean repo '%s'" % repo.id)
                try:
                    rmtree(repo.deploy_path)
                    cleaned += 1
                except OSError as exception:
                    logger.error(exception.strerror)
                finally:
                    repo.active = False
                    db.session.commit()

        return cleaned
