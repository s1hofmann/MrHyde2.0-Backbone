from os import getcwd
from os.path import join
from subprocess import run, PIPE, CalledProcessError

from app.utils import working_directory


class Executable(object):
    """Wraps an executable and provides an abstraction layer to handle program errors."""

    def __init__(self, name, *args, path=None, stdout=None, stderr=None):
        self._result = None
        self._name = name
        self._path = path
        self._arguments = []
        if stdout is not None:
            self._stdout = stdout
        else:
            self._stdout = PIPE
        if stderr is not None:
            self._stderr = stderr
        else:
            self._stderr = PIPE
        for arg in args:
            if isinstance(arg, Executable):
                for sub_arg in arg.cmd:
                    self._arguments.append(sub_arg)
            else:
                self._arguments.append(str(arg))

    def add_parameter(self, parameter, value=None):
        if isinstance(parameter, Executable):
            for sub_arg in parameter.cmd:
                self._arguments.append(sub_arg)
        else:
            self._arguments.append(parameter)
            if value is not None:
                self._arguments.append(value)

    @property
    def cmd(self):
        if self._path is not None:
            executable = [join(self._path, self._name)]
        else:
            executable = [self._name]

        [executable.append(arg) for arg in self._arguments]
        return executable

    def call(self, pwd=None):
        command = self.cmd
        if pwd is not None:
            working_dir = pwd
        else:
            working_dir = getcwd()
        if len(command) > 0:
            with working_directory(working_dir):
                try:
                    self._result = run(self.cmd, stdout=self._stdout, stderr=self._stderr, encoding='utf-8', check=True)
                except CalledProcessError as cp:
                    raise ExecutableError(self.cmd[0], cp.stdout, cp.returncode)
                except FileNotFoundError as fnf:
                    raise ExecutableError(self.cmd[0], fnf.strerror, -1)
                else:
                    return self
        else:
            raise ExecutableError('None', 'No executable given.', -1)

    def clear_cache(self):
        self._result = None
        self._arguments = []

    def output(self):
        if self._result is not None:
            return self._result.stdout
        return self._result

    def return_code(self):
        if self._result is not None:
            return self._result.returncode
        return -1


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
