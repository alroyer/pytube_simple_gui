from gui.main_window import MainWindow
from core.youtube.video_downloader import VideoDownloader
from PySide6.QtWidgets import QApplication

import sys


def main():
    application = QApplication(sys.argv)

    video_downloader = VideoDownloader()

    main_window = MainWindow(video_downloader)
    main_window.show()

    sys.exit(application.exec())


if __name__ == '__main__':
    main()
