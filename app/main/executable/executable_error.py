class ExecutableError(Exception):
    def __init__(self, cmd, msg, return_code):
        self._cmd = cmd
        self._msg = msg
        self._return_code = return_code
        if cmd is not None and return_code is not None and msg is not None:
            Exception.__init__(self, "Error executing %s. Return code was %s, message was %s" % (cmd, return_code, msg))
        elif cmd is not None and return_code is not None:
            Exception.__init__(self, "Error executing %s. Return code was %s" % (cmd, return_code))
        else:
            Exception.__init__(self, "Missing executable.")

    @property
    def msg(self):
        return self._msg

    @property
    def return_code(self):
        return self._return_code

    @property
    def cmd(self):
        return self._cmd
