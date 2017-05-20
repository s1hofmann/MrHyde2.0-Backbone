import logging

from .values import *
from .constants import *


class Config:
    # Prevent cross site request forgerie
    WTF_CSRF_ENABLED = True
    SECRET_KEY = SECRET_VALUE

    # Development
    DEBUG = False

    BASEDIR = BASEDIR_VALUE
    APPDIR = APPDIR_VALUE
    DBDIR = DBDIR_VALUE
    TEMPLATEDIR = TEMPLATEDIR_VALUE
    STATICDIR = STATICDIR_VALUE

    # database connection
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(BASEDIR, 'mr_hyde.db')
    # database migration repo folder
    SQLALCHEMY_MIGRATE_REPO = join(DBDIR, 'migrations')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Root folder of cloned repos
    REPO_PATH = REPO_PATH_VALUE
    # Root folder of rendered previews
    DEPLOY_PATH = DEPLOY_PATH_VALUE
    # Needed to publish previews
    DEPLOY_PATH_APPEND = DEPLOY_PATH_APPEND_VALUE
    URL = URL_VALUE

    # Client keys for app
    CLIENT_SECRET = CLIENT_KEYS

    # Length of repo ids
    ID_LENGTH = ID_LENGTH_VALUE

    # Max preview lifetime
    MAX_LIFETIME = MAX_LIFETIME_VALUE

    LOG_PATH = join(APPDIR, 'logs/mr_hyde.log')
    LOG_LEVEL = logging.DEBUG

    @staticmethod
    def init_app(app):
        pass


configuration = {
    'production': Config,

    'default': Config
}
