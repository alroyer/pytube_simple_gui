import sys

from core.youtube.video_downloader import VideoDownloader
from core.helpers import play_video
from gui.main_window import MainWindow
from PySide6.QtWidgets import QApplication


def main():
    application = QApplication(sys.argv)

    video_downloader = VideoDownloader()

    main_window = MainWindow(video_downloader, play_video)
    main_window.show()

    sys.exit(application.exec())


if __name__ == '__main__':
    main()
