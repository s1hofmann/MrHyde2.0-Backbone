from os.path import join
from json import loads

from flask import jsonify

from app.database.models import Repo
from app.utils import RepoUtils, flash_and_redirect_to_index
from . import status


@status.route('/<path:repo_id>', methods=['GET'])
def poll_status(repo_id):
    if not RepoUtils.repository_exists(repo_id):
        return flash_and_redirect_to_index("Repository %s was not found." % repo_id, 'error')
    deploy_path = Repo.query.filter_by(id=repo_id).first().deploy_path
    with open(join(deploy_path, 'status.txt'), 'r') as status_file:
        content = status_file.readlines()
        if len(content):
            return jsonify(loads(content[0]))
    return jsonify(msg="Build failed! :(", status=0)


@status.route('/clean', methods=['GET'])
def cleanup():
    return jsonify(removed=RepoUtils.clean_repositories())


@status.route('/stats', methods=['GET'])
def stats():
    return jsonify(active=RepoUtils.get_repo_count(True), inactive=RepoUtils.get_repo_count(False))
