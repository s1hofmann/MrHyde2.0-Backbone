from functools import wraps

from flask import request, abort, current_app

from app import current_config
from app.config import Constants


def authenticate(incoming):
    @wraps(incoming)
    def auth(*args, **kwargs):
        request_data = request.get_json()
        if request_data is not None and Constants.REQUEST_PARAMS['CLIENT_SECRET'] in request_data.keys():
            if request_data[Constants.REQUEST_PARAMS['CLIENT_SECRET']] in current_config.CLIENT_SECRET:
                return incoming(*args, **kwargs)
            current_app.logger.info("Invalid authentication request: Invalid client secret.")
            return abort(403, "Failed to authenticate.")
        current_app.logger.info("Invalid authentication request: Missing client request.")
        return abort(403, "Failed to authenticate.")

    return auth
