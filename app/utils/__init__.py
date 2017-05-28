from contextlib import contextmanager
from os import getcwd, chdir

from app.utils.requestutils import authenticate
from app.utils.repositoryutils import RepoUtils
from app.utils.urlutils import flash_and_redirect_to_index


@contextmanager
def working_directory(path):
    current_dir = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(current_dir)
