from app.main.executable.executable import Executable, ExecutableError

from app.executable.bundle.bundle_error import BundleError


class Bundle(Executable):
    def __init__(self, *args, path=None, pwd=None, stdout=None, stderr=None):
        super().__init__('bundle', *args, path=path, pwd=pwd, stdout=stdout, stderr=stderr)

    def exec(self, executable):
        super().add_parameter('exec')
        super().add_parameter(executable)
        return self

    def install(self):
        super().add_parameter('install')
        return self

    def update(self):
        super().add_parameter('update')
        return self

    def call(self):
        if len(super().cmd) > 1:
            try:
                super().call()
            except ExecutableError as e:
                raise BundleError(e.msg, e.return_code)
        return self
