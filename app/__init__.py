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

app = Flask(__name__)

bootstrap.init_app(app)
app.config.from_object(current_config)
current_config.init_app(app)

logger = RotatingFileHandler(current_config.LOG_PATH, maxBytes=10000, backupCount=10)
logger.setLevel(current_config.LOG_LEVEL)
app.logger.addHandler(logger)

db.init_app(app)
sentry.init_app(app, dsn=SENTRY_DSN)

from .controllers import jekyll, status

app.register_blueprint(jekyll, url_prefix='/jekyll')
app.register_blueprint(status, url_prefix='/status')
