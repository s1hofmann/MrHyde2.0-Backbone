from app.executable.executable_error import ExecutableError


class BundleError(ExecutableError):
    def __init__(self, msg, return_code):
        super().__init__("bundle", msg=msg, return_code=return_code)
