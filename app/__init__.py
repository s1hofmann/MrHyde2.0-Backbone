from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from app.config import configuration
from app.config.values import SENTRY_DSN

db = SQLAlchemy()
bootstrap = Bootstrap()
sentry = Sentry()
current_config = configuration['default']


def create_app(config_name):
    app = Flask(__name__)

    bootstrap.init_app(app)
    app.config.from_object(configuration[config_name])
    configuration[config_name].init_app(app)
    current_config = configuration[config_name]

    logger = RotatingFileHandler(configuration[config_name].LOG_PATH, maxBytes=10000, backupCount=10)
    logger.setLevel(configuration[config_name].LOG_LEVEL)
    app.logger.addHandler(logger)

    db.init_app(app)
    sentry.init_app(app, dsn=SENTRY_DSN)

    from .controllers import jekyll, status
    app.register_blueprint(jekyll, url_prefix='/jekyll')
    app.register_blueprint(status, url_prefix='/status')

    return app
