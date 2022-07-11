from .video_downloader import VideoDownloader
from PySide6.QtCore import (QPoint, QSettings, QSize)
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QFileDialog, QGridLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
                               QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget)
import os
import pathlib


TITLE = 'pytube simple gui'
ASSETS_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../assets')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._videos = {}

        self._video_downloader = VideoDownloader(
            self._on_progress, self._on_complete, self._on_error)

        self._video_downloader.progressed.connect(self._on_progress)
        self._video_downloader.completed.connect(self._on_complete)
        self._video_downloader.error.connect(self._on_error)

        self._source_line_edit = QLineEdit()
        self._source_line_edit.setPlaceholderText(
            'ex.: https://www.youtube.com/watch?v=ONj9cvHCado')
        self._source_line_edit.textChanged.connect(self._on_source_changed)

        self._destination_line_edit = QLineEdit()

        header_labels = ['', 'Title']

        self._download_queue_table = QTableWidget()
        self._download_queue_table.setColumnCount(len(header_labels))
        self._download_queue_table.verticalHeader().hide()
        self._download_queue_table.setHorizontalHeaderLabels(header_labels)
        self._download_queue_table.horizontalHeader().setStretchLastSection(True)

        browse_button = QPushButton('...')
        browse_button.clicked.connect(self._on_browse_button_clicked)

        self._download_button = QPushButton('Download')
        self._download_button.clicked.connect(self._on_download_button_clicked)
        self._download_button.setEnabled(False)

        horizontal_layout = QHBoxLayout()

        horizontal_layout.addWidget(self._destination_line_edit)
        horizontal_layout.addWidget(browse_button)

        widget = QWidget()

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel('Source:'), 0, 0)
        grid_layout.addWidget(self._source_line_edit, 0, 1)

        grid_layout.addWidget(QLabel('Destination:'), 1, 0)
        grid_layout.addLayout(horizontal_layout, 1, 1)

        vertical_layout = QVBoxLayout()

        vertical_layout.addLayout(grid_layout)
        vertical_layout.addWidget(self._download_button)
        vertical_layout.addWidget(self._download_queue_table)

        widget.setLayout(vertical_layout)

        icon = QPixmap(os.path.join(
            ASSETS_FOLDER, 'video-recorder-icon-32.png'))

        self.setWindowTitle(TITLE)
        self.setWindowIcon(icon)
        self.setCentralWidget(widget)

        self._read_settings()

    def closeEvent(self, event):
        self._write_settings()
        super().closeEvent(event)

    def _read_settings(self):
        settings = QSettings('alroyer', 'pytube simple gui')
        settings.beginGroup('mainwindow')
        destination = settings.value('destination', str(pathlib.Path().home()))
        size = settings.value('size', QSize(400, 400))
        position = settings.value('position', QPoint(300, 300))
        settings.endGroup()

        self._destination_line_edit.setText(destination)
        self.resize(size)
        self.move(position)

        # TODO validate visibility ?!

    def _write_settings(self):
        settings = QSettings('alroyer', 'pytube simple gui')
        settings.beginGroup('mainwindow')
        settings.setValue('destination', self._destination_line_edit.text())
        settings.setValue('size', self.size())
        settings.setValue('position', self.pos())
        settings.endGroup()

    def _update_table(self):
        self._download_queue_table.setRowCount(len(self._videos))
        row = 0
        for key in self._videos:
            percentage, title, _ = self._videos[key]
            self._download_queue_table.setItem(
                row, 0, QTableWidgetItem(f'{percentage}'))
            self._download_queue_table.setItem(
                row, 1, QTableWidgetItem(f'{title}'))
            row += 1

    def _on_source_changed(self, source_url):
        enabled = 'youtube' in source_url.lower()
        self._download_button.setEnabled(enabled)

    def _on_browse_button_clicked(self):
        selected_directory = QFileDialog.getExistingDirectory(
            self, 'Select destination folder', self._destination_line_edit.text(), QFileDialog.ShowDirsOnly)
        if selected_directory:
            self._destination_line_edit.setText(selected_directory)

    def _on_download_button_clicked(self):
        self._video_downloader.download(
            self._source_line_edit.text(), self._destination_line_edit.text())
        self._update_table()

    def _on_progress(self, percentage, source_url, destination_path):
        self._videos[destination_path] = (
            percentage, source_url, destination_path)
        self._update_table()

    def _on_complete(self, source_url, destination_path):
        print(f'on complete {source_url} {destination_path}')
        # TODO

    def _on_error(self, source_url):
        QMessageBox.critical(self, TITLE, f'Unable to download "{source_url}"')
