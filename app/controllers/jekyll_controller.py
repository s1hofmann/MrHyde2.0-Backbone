from flask import redirect, url_for, abort, request, jsonify

from app.buildpipeline import BuildPipeline
from app.config import Constants
from app.repository import Repository
from app.utils import RepoUtils, RequestUtils
from . import jekyll


@jekyll.route('/', methods=['GET'])
def list_all_repositories():
    return redirect(url_for('static', filename='welcome.html'))


@jekyll.route('/', methods=['POST'])
def create_repo():
    request_data = request.get_json()
    if RequestUtils.validate_request(request_data):
        new_repo = Repository.from_request(request_data)

        (repo_id, repo_url) = new_repo.init()
        builder = BuildPipeline(new_repo)
        builder.execute()
        expires = RepoUtils.get_expiration_date(repo_id)
        return jsonify({Constants.RESPONSE_PARAMS['PREVIEW_URL']: repo_url,
                        Constants.RESPONSE_PARAMS['PREVIEW_EXPIRATION']: expires,
                        Constants.RESPONSE_PARAMS['PREVIEW_ID']: repo_id})
    else:
        abort(400, 'Bad request.')
