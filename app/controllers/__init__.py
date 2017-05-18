from flask import Blueprint

from app import current_config

jekyll = Blueprint('jekyll',
                   __name__,
                   static_folder=current_config.STATICDIR,
                   template_folder=current_config.TEMPLATEDIR)

status = Blueprint('status',
                   __name__,
                   static_folder=current_config.STATICDIR,
                   template_folder=current_config.TEMPLATEDIR)

from .status_controller import status
from .jekyll_controller import jekyll
