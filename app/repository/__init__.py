from os.path import join
from shutil import copytree
from sqlite3 import DatabaseError
from time import time

import git

from app import db, current_config
from app.config import Constants
from app.database.models import Repo
from app.filehandling import create_diff_file
from app.utils import RepoUtils, working_directory


class Repository:
    def __init__(self, url, diff, static_files, draft=True):
        self._url = url
        self._repo_diff = diff
        self._static_files = static_files
        self._draft = draft
        self._repo_id = None
        self._build_path = None
        self._deploy_path = None

    @staticmethod
    def from_request(request_data):
        """
        Creates a new repository given data from an incoming request
        :param request_data: Incoming request data
        :return: Repository
        """
        for param in Constants.REQUEST_PARAMS.values():
            if param not in request_data.keys():
                raise AttributeError('%s parameter missing in request. Aborting.' % param)

        return Repository(request_data[Constants.REQUEST_PARAMS['GIT_URL']],
                          request_data[Constants.REQUEST_PARAMS['DIFF']],
                          request_data[Constants.REQUEST_PARAMS['PAYLOAD']],
                          request_data[Constants.REQUEST_PARAMS['DRAFT']])

    @property
    def repo_id(self):
        return self._repo_id

    @property
    def build_path(self):
        return self._build_path

    @property
    def deploy_path(self):
        return self._deploy_path

    @property
    def diff(self):
        return self._repo_diff

    @property
    def static_files(self):
        return self._static_files

    @property
    def draft(self):
        return self._draft

    def init(self):
        """
        Performs initialization steps for a local repository
        -> Generates an unique repo id and assembles path variables, which are then persisted
        -> Returns repo id and its query url
        :return: 
        """
        self._repo_id = RepoUtils.generate_id(current_config.ID_LENGTH)
        self._build_path = join(current_config.REPO_PATH, self._repo_id)
        self._deploy_path = ''.join([current_config.DEPLOY_PATH, self._repo_id, current_config.DEPLOY_PATH_APPEND])

        if RepoUtils.repository_exists(self._repo_id):
            raise RepositoryError("File conflict for repository with id %s. Please retry." % self._repo_id)

        repo_dao = Repo(identifier=self._repo_id,
                        path=self._build_path,
                        deploy_path=self._deploy_path,
                        url=self._url,
                        last_used=int(time()),
                        active=True)
        try:
            db.session.add(repo_dao)
            db.session.commit()
            copytree(join(current_config.TEMPLATEDIR, 'redirect'), self._deploy_path)
        except DatabaseError as dbe:
            raise RepositoryError("Unable to communicate with database. Reason: %s" % dbe.__str__())
        except OSError as e:
            raise RepositoryError("Unable to dispatch redirector files. Reason: %s" % e.strerror)
        finally:
            return self._repo_id, ''.join(['https://', self._repo_id, '.', current_config.URL, '/progress.html'])

    def checkout(self):
        """
        Clones a repository from its given git URL
        :return: None
        """
        try:
            gitter = git.Git()
            gitter.clone(self._url, self._build_path)
        except git.GitCommandError as e:
            raise RepositoryError("Failed to patch repository %s. Reason: %s" % (self._build_path, e.__str__()))
        except OSError as e:
            raise RepositoryError("Failed to patch repository %s. Reason: %s" % (self._build_path, e.strerror))

    def patch(self, diff):
        """
        Applies a diff to a cloned repository
        :param diff: Diff to apply, e.g. the patch received from a request
        :return: None
        """
        if diff is not None and len(diff):
            with working_directory(self._build_path):
                try:
                    gitter = git.Git()
                    diff_file = create_diff_file(self._repo_id, diff)
                    gitter.apply(diff_file)
                except git.GitCommandError as e:
                    raise RepositoryError("Failed to patch repository %s. Reason: %s" % (self._build_path, e.__str__()))
                except OSError as e:
                    raise RepositoryError("Failed to patch repository %s. Reason: %s" % (self._build_path, e.strerror))


class RepositoryError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
