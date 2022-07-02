import os
import sys
import subprocess


def open_file(file_path):
    if sys.platform == 'win32':
        os.startfile(file_path)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, file_path])
