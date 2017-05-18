from flask import jsonify

from app.utils import RepoUtils, flash_and_redirect_to_index
from . import status


@status.route('/<path:repo_id>', methods=['GET'])
def poll_status(repo_id):
    if not RepoUtils.repository_exists(repo_id):
        return flash_and_redirect_to_index("Repository %s was not found." % repo_id, 'error')
    return jsonify(status=repo_id, msg='Processing')
