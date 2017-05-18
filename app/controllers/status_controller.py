from flask import jsonify

from app.utils import RepoUtils
from . import status


@status.route('/<path:repo_id>', methods=['GET'])
def poll_status(repo_id):
    if not RepoUtils.repository_exists(repo_id):
        return jsonify(status=-1, msg='Repository %s not found.' % repo_id)
    return jsonify(status=repo_id, msg='Processing')
