from contextlib import contextmanager
from os import getcwd, chdir

from .requestutils import RequestUtils
from .repositoryutils import RepoUtils
from .urlutils import flash_and_redirect_to_index


@contextmanager
def working_directory(path):
    current_dir = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(current_dir)
