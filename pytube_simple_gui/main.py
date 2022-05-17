from pytube import YouTube
from PySide6.QtWidgets import QApplication, QCheckBox, QGridLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

import os
import sys


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('pytube simple gui')

        self._source_line_edit = QLineEdit()
        self._destination_line_edit = QLineEdit()

        self._video_check_box = QCheckBox('video')
        self._video_check_box.setChecked(True)

        self._audio_check_box = QCheckBox('audio')
        self._audio_check_box.setChecked(True)

        download_button = QPushButton('download')
        download_button.clicked.connect(self._on_download_button_clicked)

        widget = QWidget()

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel('source'), 0, 0)
        grid_layout.addWidget(self._source_line_edit, 0, 1)

        grid_layout.addWidget(QLabel('destination'), 1, 0)
        grid_layout.addWidget(self._destination_line_edit, 1, 1)

        grid_layout.addWidget(self._video_check_box, 2, 0)
        grid_layout.addWidget(self._audio_check_box, 3, 0)

        vertical_layout = QVBoxLayout()

        vertical_layout.addLayout(grid_layout)
        vertical_layout.addWidget(download_button)

        widget.setLayout(vertical_layout)

        self.setCentralWidget(widget)

    def _on_download_button_clicked(self):
        if not self._video_check_box.isChecked() and not self._audio_check_box.isChecked():
            return

        you_tube = YouTube(self._source_line_edit.text())

        if self._video_check_box.isChecked():
            stream = you_tube.streams.get_highest_resolution()
            if stream:
                stream.download(os.path.join(
                    self._destination_line_edit.text(), 'video'))

        if self._audio_check_box.isChecked():
            stream = you_tube.streams.get_audio_only()
            if stream:
                stream.download(os.path.join(
                    self._destination_line_edit.text(), 'audio'))


def main():
    application = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(application.exec())


if __name__ == '__main__':
    main()
