from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from app.config import configuration
from app.config.values import SENTRY_DSN

db = SQLAlchemy()
sentry = Sentry()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(configuration[config_name])
    configuration[config_name].init_app(app)

    logger = RotatingFileHandler(configuration[config_name].LOG_PATH, maxBytes=10000, backupCount=10)
    logger.setLevel(configuration[config_name].LOG_LEVEL)
    app.logger.addHandler(logger)

    db.init_app(app)
    sentry.init_app(app, dsn=SENTRY_DSN)

    return app