from contextlib import contextmanager
from os import getcwd, chdir

from app.utils.repositoryutils import *
from app.utils.requestutils import *
from app.utils.urlutils import *

__all__ = ['working_directory', 'authenticate', 'RepoUtils', 'flash_and_redirect_to_index']


@contextmanager
def working_directory(path):
    current_dir = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(current_dir)
