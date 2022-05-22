from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

import os


class MainWindow(QMainWindow):
    def __init__(self, video_downloader) -> None:
        super().__init__()

        self._video_downloader = video_downloader

        assets_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), '../assets')
        window_icon = QPixmap(os.path.join(
            assets_path, 'video-recorder-icon-32.png'))

        self.setWindowTitle('pytube simple gui')
        self.setWindowIcon(window_icon)

        self._source_line_edit = QLineEdit()
        self._destination_line_edit = QLineEdit()
        self._destination_line_edit.setReadOnly(True)

        browse_button = QPushButton('...')
        browse_button.clicked.connect(self._on_browse_button_clicked)

        download_button = QPushButton('download')
        download_button.clicked.connect(self._on_download_button_clicked)

        horizontal_layout = QHBoxLayout()

        horizontal_layout.addWidget(self._destination_line_edit)
        horizontal_layout.addWidget(browse_button)

        widget = QWidget()

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel('source'), 0, 0)
        grid_layout.addWidget(self._source_line_edit, 0, 1)

        grid_layout.addWidget(QLabel('destination'), 1, 0)
        grid_layout.addLayout(horizontal_layout, 1, 1)

        vertical_layout = QVBoxLayout()

        vertical_layout.addLayout(grid_layout)
        vertical_layout.addWidget(download_button)

        widget.setLayout(vertical_layout)

        self.setCentralWidget(widget)

    def _load_settings(self):
        # TODO
        pass

    def _save_settings(self):
        # TODO
        pass

    def _on_browse_button_clicked(self):
        selected_directory = QFileDialog.getExistingDirectory(
            self, 'select destination folder', self._destination_line_edit.text(), QFileDialog.ShowDirsOnly)
        if selected_directory:
            self._destination_line_edit.setText(selected_directory)

    def _on_download_button_clicked(self):
        source_uri = self._source_line_edit.text()
        destination_folder = self._destination_line_edit.text()

        self._video_downloader.download(source_uri, destination_folder)

    # def _on_progress(self, stream, chunk, file_handle, bytes_remaining):
    #     pass
