from main_window import MainWindow
from youtube_video_downloader import YoutubeVideoDownloader
from PySide6.QtWidgets import QApplication

import sys


def main():
    application = QApplication(sys.argv)

    video_downloader = YoutubeVideoDownloader()

    main_window = MainWindow(video_downloader)
    main_window.show()

    sys.exit(application.exec())


if __name__ == '__main__':
    main()
