from subprocess import PIPE

from .. import Executable, ExecutableError


class Bundle(Executable):
    def __init__(self, *args, path=None, pwd=None, stdout=PIPE, stderr=PIPE):
        super().__init__('bundle', *args, path=path, pwd=pwd, stdout=stdout, stderr=stderr)

    def exec(self, executable, gemfile=None):
        super().clear_cache()
        super().add_parameter('exec')
        if gemfile is not None:
            super().add_parameter("--gemfile=%s" % gemfile)
        super().add_parameter(executable)
        return self

    def install(self, gemfile=None):
        super().clear_cache()
        super().add_parameter('install')
        if gemfile is not None:
            super().add_parameter("--gemfile=%s" % gemfile)
        return self

    def update(self, gemfile=None):
        super().clear_cache()
        super().add_parameter('update')
        if gemfile is not None:
            super().add_parameter("--gemfile=%s" % gemfile)
        return self

    def call(self):
        if len(super().cmd) > 1:
            try:
                super().call()
            except ExecutableError as e:
                raise BundleError(e.msg, e.return_code)
        return self


class BundleError(ExecutableError):
    def __init__(self, msg, return_code):
        super().__init__("bundle", msg=msg, return_code=return_code)
