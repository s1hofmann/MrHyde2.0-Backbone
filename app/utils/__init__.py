from contextlib import contextmanager
from os import getcwd, chdir

from .repositoryutils import *
from .requestutils import *
from .urlutils import *


@contextmanager
def working_directory(path):
    current_dir = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(current_dir)
