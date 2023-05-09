import os
import subprocess
import sys


def play_video(file_path):
    if sys.platform == 'win32':
        os.startfile(file_path)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, file_path])
