from contextlib import contextmanager
from os import getcwd, chdir


@contextmanager
def working_directory(path):
    current_dir = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(current_dir)
