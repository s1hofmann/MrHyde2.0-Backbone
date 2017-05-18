import threading
from os.path import join

from app import current_config
from ..executable.bundle import Bundle, BundleError
from ..executable.jekyll import Jekyll


class BuildPipeline:
    def __init__(self, repository):
        self._repo = repository
        self._gemfile = None
        self._bundle = Bundle()

    def pull(self):
        self._repo.checkout()
        self._repo.patch(self._repo.diff)

    def prepare(self):
        """
        Sets up a repository on the file system
        Involves the following:
            - Try to install required bundler packages if the are not already present
                - If no Gemfile was provided with the repo, rely on the default gh-pages one
        :return: None
        """
        self._bundle.clear_cache()
        try:
            self._bundle.install(gemfile=self._gemfile).call(pwd=self._repo.build_path)
        except BundleError as be:
            if be.return_code == 10:
                # Switch to using Gemfile template when no Gemfile is present in repo
                self._gemfile = join(current_config.TEMPLATEDIR, 'Gemfile')
                self._bundle.install(gemfile=self._gemfile).call()
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
        self._bundle.clear_cache()
        try:
            log_file = open(join(self._repo.deploy_path, 'input.txt'), 'w')
            jekyll = Jekyll(source=self._repo.build_path,
                            dest=self._repo.deploy_path,
                            config=[
                                join(self._repo.build_path, '_config.yml'),
                                join(current_config.TEMPLATEDIR, 'keep_files.yml')
                            ],
                            draft=self._repo.draft,
                            stdout=log_file,
                            stderr=log_file)

            try:
                self._bundle.exec(jekyll, gemfile=self._gemfile).call(pwd=self._repo.build_path)
                status_file = open(join(self._repo.deploy_path, 'statuscode.txt'), 'w')
                try:
                    status_file.write(str(self._bundle.return_code()))
                except OSError as e:
                    raise BundleError("Corrupt file setup: %s: %s" % (e.strerror, e.filename),
                                      self._bundle.return_code())
            except BundleError:
                raise
        except OSError as e:
            raise BundleError("Corrupt file setup: %s: %s" % (e.strerror, e.filename), self._bundle.return_code())

    def run(self):
        self.pull()
        self.prepare()
        self.build()

    def execute(self):
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()
