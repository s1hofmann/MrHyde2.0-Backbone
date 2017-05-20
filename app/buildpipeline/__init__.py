import threading
from json import dumps
from os.path import join

from app import current_config
from app import util_logger as logger
from app.executable.bundle import Bundle, BundleError
from app.executable.jekyll import Jekyll
from app.filehandling import deploy_error_page, dispatch_static_files
from app.repository import RepositoryError


class BuildPipeline:
    def __init__(self, repository):
        self._repo = repository
        self._gemfile = None
        with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
            log_file.write(dumps({"status": 1, "msg": 'Initializing repo ...'}))

    def pull(self, diff=None):
        """
        Clones and updates a git repository
        :param diff: Diff file to apply, e.g. patch received in request
        :return: None
        """
        try:
            logger.debug("Checking out repository.")
            self._repo.checkout()
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 1, "msg": 'Initialized repo ...'}))
            if diff is not None:
                logger.debug("Patching repository.")
                self._repo.patch(diff)
            else:
                self._repo.patch(self._repo.diff)
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 1, "msg": 'Fetched updates ...'}))
        except RepositoryError:
            raise
        except OSError:
            raise

    def prepare(self):
        """
        Sets up a repository on the file system
        Involves the following:
            - Try to install required bundler packages if the are not already present
                - If no Gemfile was provided with the repo, rely on the default gh-pages one
        :return: None
        """
        bundler = Bundle()
        try:
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 1, "msg": 'Installing dependencies ...\nThis might take a bit ...'}))
            logger.debug("Installing dependencies.")
            bundler.install(gemfile=self._gemfile).call(pwd=self._repo.build_path)
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 1, "msg": 'Installed dependencies!'}))
        except BundleError as be:
            if be.return_code == 10:
                # Switch to using Gemfile template when no Gemfile is present in repo
                logger.debug("Switching to default Gemfile.")
                self._gemfile = join(current_config.TEMPLATEDIR, 'Gemfile')
                bundler.install(gemfile=self._gemfile).call()
                with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                    log_file.write(dumps({"status": 1, "msg": 'Installed dependencies!'}))
            else:
                raise
        except OSError:
            raise

    def build(self):
        """
        Runs a jekyll build within a defined bundler environment
        Involves the following:
            - Try to run a jekyll build within a defined bundler environment
                - Once again, either use the one provided with the repository or the gh-pages one
        :param draft: Include drafts?
        :return: 
        """
        bundler = Bundle()
        try:
            logger.debug("Starting Jekyll build.")
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 0, "msg": 'Starting build ...'}))
            jekyll = Jekyll(source=self._repo.build_path,
                            dest=self._repo.deploy_path,
                            config=[
                                join(self._repo.build_path, '_config.yml'),
                                join(current_config.TEMPLATEDIR, 'keep_files.yml')
                            ],
                            draft=self._repo.draft)

            bundler.exec(jekyll, gemfile=self._gemfile).call(pwd=self._repo.build_path)
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 0, "msg": 'Deployed page!'}))
        except BundleError:
            raise
        except OSError:
            raise

    def run(self):
        """
        Combines all pipeline steps into a single method to be run asynchronously
        :return: None
        """
        logger.debug("Pipeline start.")
        try:
            self.pull()
            self.prepare()
            self.build()
            logger.debug("Dispatching static files.")
            if self._repo.static_files is not None and len(self._repo.static_files):
                dispatch_static_files(self._repo.deploy_path, self._repo.static_files)
            logger.debug("Pipeline end.")
        except RepositoryError or BundleError or OSError:
            deploy_error_page(self._repo.deploy_path)
        finally:
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 0, "msg": 'Build failed!'}))

    def execute(self):
        """
        Executes a pipeline for a certain repository by running its 'run' method asynchronously
        :return: None
        """
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()
