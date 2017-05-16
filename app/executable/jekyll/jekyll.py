from subprocess import PIPE

from app.main.executable.executable import Executable, ExecutableError

from app.executable.jekyll import JekyllError


class Jekyll(Executable):
    def __init__(self, path=None, source=None, dest=None, config=None, draft=False, *args, pwd=None, stdout=PIPE,
                 stderr=PIPE):
        super().__init__('jekyll', *args, path=path, pwd=pwd, stdout=stdout, stderr=stderr)
        self.add_parameter('build')
        if config is None:
            config = []
        if source is not None:
            self.add_parameter('--source', source)
        if dest is not None:
            self.add_parameter('--destination', dest)
        if config is not None and len(config):
            self.add_parameter('--config')
            for idx, conf in enumerate(config):
                if idx < len(config) - 1:
                    self.add_parameter(conf + ',')
                else:
                    self.add_parameter(conf)
        if draft:
            self.add_parameter('--drafts')

    def call(self):
        try:
            super().call()
        except ExecutableError as e:
            raise JekyllError(e.msg, e.return_code)
