import os
import pathlib
import sys

if sys.version_info >= (3, 5):
    home_dir = str(pathlib.Path.home())
else:
    home_dir = os.path.expanduser('~')

default_dir = os.path.join(home_dir, '.tdunofficial')