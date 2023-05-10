import sys

from core.helpers import play_video
from core.youtube.video_downloader import VideoDownloader
from gui.main_window import MainWindow
from PySide6.QtCore import QLocale, QTranslator
from PySide6.QtWidgets import QApplication


def main():
    application = QApplication(sys.argv)

    translator = QTranslator()
    if translator.load(QLocale(), 'tr', '.', 'pytube_simple_gui/translations', '.qm'):
        application.installTranslator(translator)

    video_downloader = VideoDownloader()

    main_window = MainWindow(video_downloader, play_video, translator)
    main_window.show()

    sys.exit(application.exec())


if __name__ == '__main__':
    main()
