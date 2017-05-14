import logging
import sys
# from flask_bootstrap import Bootstrap
from logging.handlers import RotatingFileHandler
from os import chdir
from os.path import join

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import BASEDIR

sys.path.insert(0, BASEDIR)
chdir(BASEDIR)

app = Flask(__name__)

app.config.from_object('config')
# app.jinja_env.add_extension('jinja2.ext.do')
db = SQLAlchemy(app)
# login_manager = LoginManager(app)
migrate = Migrate(app, db)

logger = RotatingFileHandler(join(BASEDIR, 'logs/MrHyde.log'), maxBytes=10000, backupCount=10)
logger.setLevel(logging.WARNING)
app.logger.addHandler(logger)

# from app.main import views
from app.main import models
