from os import getcwd
from shutil import copy2

from .. import Executable, ExecutableError


class Bundle(Executable):
    def __init__(self, *args, path=None, stdout=None, stderr=None):
        super().__init__('bundle', *args, path=path, stdout=stdout, stderr=stderr)
        self._gemfile = None

    def exec(self, executable, gemfile=None):
        super().clear_cache()
        super().add_parameter('exec')
        super().add_parameter(executable)
        self._gemfile = gemfile
        return self

    def install(self, gemfile=None):
        super().clear_cache()
        super().add_parameter('install')
        self._gemfile = gemfile
        return self

    def update(self, gemfile=None):
        super().clear_cache()
        super().add_parameter('update')
        self._gemfile = gemfile
        return self

    def call(self, pwd=None):
        if self._gemfile is not None:
            try:
                if pwd is None:
                    copy2(self._gemfile, getcwd())
                else:
                    copy2(self._gemfile, pwd)
            except IOError as e:
                raise BundleError(e.strerror + ": " + e.filename, self.return_code())
        if len(super().cmd) > 1:
            try:
                super().call(pwd=pwd)
            except ExecutableError as e:
                raise BundleError(e.msg, e.return_code)
        return self


class BundleError(ExecutableError):
    def __init__(self, msg, return_code):
        super().__init__("bundle", msg=msg, return_code=return_code)
