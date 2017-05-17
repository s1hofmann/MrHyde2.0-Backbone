from contextlib import contextmanager
from os import getcwd, chdir

from .repositoryutils import RepoUtils
from .requestutils import RequestUtils


@contextmanager
def working_directory(path):
    current_dir = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(current_dir)
