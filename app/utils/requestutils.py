from app import current_config
from app.config import Constants


class RequestUtils:
    @staticmethod
    def validate_request(request_data):
        if request_data is not None and Constants.REQUEST_PARAMS['CLIENT_SECRET'] in request_data.keys():
            if request_data[Constants.REQUEST_PARAMS['CLIENT_SECRET']] in current_config.CLIENT_SECRET:
                return True
        return False
