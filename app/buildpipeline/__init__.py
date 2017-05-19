import threading
from os.path import join
from json import dumps

from app import current_config
from app.filehandling import deploy_error_page, dispatch_static_files
from app.repository import RepositoryError
from ..executable.bundle import Bundle, BundleError
from ..executable.jekyll import Jekyll


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
            self._repo.checkout()
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 1, "msg": 'Initialized repo ...'}))
            if diff is not None:
                self._repo.patch(diff)
            else:
                self._repo.patch(self._repo.diff)
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 1, "msg": 'Fetched updates ...'}))
        except OSError:
            raise
        except RepositoryError:
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
            bundler.install(gemfile=self._gemfile).call(pwd=self._repo.build_path)
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 1, "msg": 'Installed dependencies!'}))
        except BundleError as be:
            if be.return_code == 10:
                # Switch to using Gemfile template when no Gemfile is present in repo
                self._gemfile = join(current_config.TEMPLATEDIR, 'Gemfile')
                bundler.install(gemfile=self._gemfile).call()
                with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                    log_file.write(dumps({"status": 1, "msg": 'Installed dependencies!'}))
            else:
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
            with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                log_file.write(dumps({"status": 0, "msg": 'Starting build ...'}))
            jekyll = Jekyll(source=self._repo.build_path,
                            dest=self._repo.deploy_path,
                            config=[
                                join(self._repo.build_path, '_config.yml'),
                                join(current_config.TEMPLATEDIR, 'keep_files.yml')
                            ],
                            draft=self._repo.draft)

            try:
                bundler.exec(jekyll, gemfile=self._gemfile).call(pwd=self._repo.build_path)
                with open(join(self._repo.deploy_path, 'status.txt'), 'w') as log_file:
                    log_file.write(dumps({"status": 0, "msg": 'Deployed page!'}))
            except BundleError:
                raise
        except OSError as e:
            raise BundleError("Corrupt file setup: %s: %s" % (e.strerror, e.filename), self._bundle.return_code())

    def run(self):
        """
        Combines all pipeline steps into a single method to be run asynchronously
        :return: None
        """
        try:
            self.pull()
            self.prepare()
            self.build()
            if self._repo.static_files is not None and len(self._repo.static_files):
                dispatch_static_files(self._repo.deploy_path, self._repo.static_files)
        except RepositoryError:
            deploy_error_page(self._repo.deploy_path,
                              "Git error",
                              "We were unable to set up your repository.\nSorry for that, we'll have a look at it!")
        except BundleError:
            deploy_error_page(self._repo.deploy_path,
                              "Build error",
                              "We were unable to run our build pipeline on your repository. "
                              "We'll have to analyze our logs!")
        except OSError:
            deploy_error_page(self._repo.deploy_path,
                              "I/O error",
                              "We encountered internal problems which we be better take care of!")
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
