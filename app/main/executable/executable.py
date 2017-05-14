#!/usr/bin/env python

from os import getcwd
from os.path import join
from subprocess import run, PIPE, CalledProcessError

from app.main.executable.executable_error import ExecutableError
from app.main.working_directory import working_directory


class Executable(object):
    """Wraps an executable and provides an abstraction layer to handle program errors."""

    def __init__(self, name, *args, path=None, pwd=None, stdout=None, stderr=None):
        self._result = None
        self._name = name
        self._path = path
        if pwd is not None:
            self._pwd = pwd
        else:
            self._pwd = getcwd()
        self._arguments = []
        self._stdout = stdout
        self._stderr = stderr
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

    def call(self):
        command = self.cmd
        if len(command) > 0:
            with working_directory(self._pwd):
                try:
                    if self._stdout is not None and self._stderr is not None:
                        self._result = run(self.cmd, stdout=self._stdout, stderr=self._stderr, encoding='utf-8',
                                           check=True)
                    elif self._stdout is not None:
                        self._result = run(self.cmd, stdout=self._stdout, stderr=PIPE, encoding='utf-8', check=True)
                    elif self._stderr is not None:
                        self._result = run(self.cmd, stdout=PIPE, stderr=self._stderr, encoding='utf-8', check=True)
                    else:
                        self._result = run(self.cmd, stdout=PIPE, stderr=PIPE, encoding='utf-8', check=True)
                except CalledProcessError as cp:
                    raise ExecutableError(self.cmd[0], cp.returncode, cp.returncode)
                except FileNotFoundError as fnf:
                    raise ExecutableError(self.cmd[0], fnf.strerror, -1)
                else:
                    return self
        else:
            raise ExecutableError('None', 'No executable given.', -1)

    def output(self):
        if self._result is not None:
            return self._result.stdout
        return self._result

    def return_code(self):
        if self._result is not None:
            return self._result.returncode
        return self._result


if __name__ == "__main__":
    e = Executable("ls", "-la", pwd='/Users/zimi/Downloads')
    print(e.call().output())
