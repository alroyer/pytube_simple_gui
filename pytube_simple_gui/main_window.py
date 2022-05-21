from PySide6.QtWidgets import QCheckBox, QGridLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self, video_downloader) -> None:
        super().__init__()

        self._video_downloader = video_downloader

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

    def _on_download_button_clicked(self):
        if not self._video_check_box.isChecked() and not self._audio_check_box.isChecked():
            return

        source_uri = self._source_line_edit.text()
        destination_folder = self._destination_line_edit.text()

        self._video_downloader.download(source_uri, destination_folder)

    # def _on_progress(self, stream, chunk, file_handle, bytes_remaining):
    #     pass
