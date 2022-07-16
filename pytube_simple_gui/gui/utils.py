import os
import sys
import subprocess


def open_file(path):
    if sys.platform == 'win32':
        os.startfile(path)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, path])
