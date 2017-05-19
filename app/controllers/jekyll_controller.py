from flask import abort, request, jsonify, render_template, current_app

from app.buildpipeline import BuildPipeline
from app.config import Constants
from app.database.models import Repo
from app.repository import Repository, RepositoryError
from app.utils import RepoUtils, RequestUtils, flash_and_redirect_to_index
from bundle import BundleError
from filehandling import deploy_error_page
from . import jekyll


@jekyll.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')


@jekyll.route('/list', methods=['GET'])
def list_all_repos():
    if current_app.debug:
        repos = Repo.query.all()
        return render_template('repo_overview.html', repos=repos)
    return flash_and_redirect_to_index('Endpoint \'/jekyll/list\' only available in debug mode.', 'error')


@jekyll.route('/heartbeat', methods=['GET'])
def heartbeat():
    return ""


@jekyll.route('/', methods=['POST'])
def create_repo():
    request_data = request.get_json()
    if RequestUtils.validate_request(request_data):
        new_repo = None
        repo_id = None
        repo_url = None
        expires = None
        try:
            new_repo = Repository.from_request(request_data)
        except AttributeError as e:
            abort(400, 'Bad request. %s' % e.__cause__)

        try:
            if new_repo is not None:
                (repo_id, repo_url) = new_repo.init()
                builder = BuildPipeline(new_repo)
                builder.execute()
                expires = RepoUtils.get_expiration_date(repo_id)
                return jsonify({Constants.RESPONSE_PARAMS['PREVIEW_URL']: repo_url,
                                Constants.RESPONSE_PARAMS['PREVIEW_EXPIRATION']: expires,
                                Constants.RESPONSE_PARAMS['PREVIEW_ID']: repo_id})
        except RepositoryError:
            deploy_error_page(new_repo.deploy_path,
                              "Git error",
                              "We were unable to set up your repository.\nSorry for that, we'll have a look at it!")
        except BundleError:
            deploy_error_page(new_repo.deploy_path,
                              "Build error",
                              "We were unable to run our build pipeline on your repository. "
                              "We'll have to analyze our logs!")
        except OSError:
            deploy_error_page(new_repo.deploy_path,
                              "I/O error",
                              "We encountered internal problems which we be better take care of!")
        finally:
            if repo_url is not None and repo_id is not None and expires is not None:
                return jsonify({Constants.RESPONSE_PARAMS['PREVIEW_URL']: repo_url,
                                Constants.RESPONSE_PARAMS['PREVIEW_EXPIRATION']: expires,
                                Constants.RESPONSE_PARAMS['PREVIEW_ID']: repo_id})
            else:
                abort(502)
    else:
        abort(400)
