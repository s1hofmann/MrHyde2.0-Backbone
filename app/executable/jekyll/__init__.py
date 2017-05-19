from app.executable import Executable, ExecutableError


class Jekyll(Executable):
    def __init__(self, path=None, source=None, dest=None, config=None, draft=False, *args, stdout=None, stderr=None):
        super().__init__('jekyll', *args, path=path, stdout=stdout, stderr=stderr)
        self.add_parameter('build')
        if config is None:
            config = []
        if source is not None:
            self.add_parameter('--source', source)
        if dest is not None:
            self.add_parameter('--destination', dest)
        if config is not None and len(config):
            self.add_parameter('--config', ','.join(config))
        if draft:
            self.add_parameter('--drafts')

    def call(self, pwd=None):
        try:
            super().call(pwd=pwd)
        except ExecutableError as e:
            raise JekyllError(e.msg, e.return_code)


class JekyllError(ExecutableError):
    def __init__(self, msg, return_code):
        super().__init__("jekyll", msg=msg, return_code=return_code)
