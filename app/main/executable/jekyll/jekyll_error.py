from app.main.executable.executable_error import ExecutableError


class JekyllError(ExecutableError):
    def __init__(self, msg, return_code):
        super().__init__("jekyll", msg=msg, return_code=return_code)
