from PySide6.QtCore import (QSettings, Signal)
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QFileDialog, QGridLayout, QHBoxLayout, QLabel,
                               QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget)

import os
import subprocess
import sys
import threading


def open_file(file_path):
    if sys.platform == 'win32':
        os.startfile(file_path)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, file_path])


class MainWindow(QMainWindow):
    progress = Signal(int)
    download_completed = Signal(str)
    error = Signal(str)

    def __init__(self, video_downloader):
        super().__init__()

        self._video_downloader = video_downloader

        self.progress.connect(self._progress)
        self.download_completed.connect(self._download_completed)
        self.error.connect(self._error)

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

        self._download_button = QPushButton('Download')
        self._download_button.clicked.connect(self._on_download_button_clicked)

        horizontal_layout = QHBoxLayout()

        horizontal_layout.addWidget(self._destination_line_edit)
        horizontal_layout.addWidget(browse_button)

        self._widget = QWidget()

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel('Source:'), 0, 0)
        grid_layout.addWidget(self._source_line_edit, 0, 1)

        grid_layout.addWidget(QLabel('Destination:'), 1, 0)
        grid_layout.addLayout(horizontal_layout, 1, 1)

        vertical_layout = QVBoxLayout()

        vertical_layout.addLayout(grid_layout)
        vertical_layout.addWidget(self._download_button)

        self._widget.setLayout(vertical_layout)

        self.setCentralWidget(self._widget)

        self._read_settings()

    def closeEvent(self, event):
        self._write_settings()
        return super().closeEvent(event)

    def _read_settings(self):
        settings = QSettings('alroyer', 'pytube simple gui')
        settings.beginGroup('mainwindow')
        destination = settings.value('destination')
        if destination:
            self._destination_line_edit.setText(destination)
        # TODO resize and move
        # geometry = settings.value('geometry')
        # if geometry:
        #     pass
        settings.endGroup()

    def _write_settings(self):
        settings = QSettings('alroyer', 'pytube simple gui')
        settings.beginGroup('mainwindow')
        settings.setValue('destination', self._destination_line_edit.text())
        # TODO
        # settings.setValue('geometry', self.geometry)
        settings.endGroup()
        pass

    def _on_browse_button_clicked(self):
        selected_directory = QFileDialog.getExistingDirectory(
            self, 'Select destination folder', self._destination_line_edit.text(), QFileDialog.ShowDirsOnly)
        if selected_directory:
            self._destination_line_edit.setText(selected_directory)

    def _on_download_button_clicked(self):
        self._widget.setEnabled(False)

        source_url = self._source_line_edit.text()
        destination_folder = self._destination_line_edit.text()

        self._async_download(source_url, destination_folder)

    def _progress(self, percentage_of_completion):
        self._download_button.setText(
            f'{percentage_of_completion:.0f}% completed')

    def _download_completed(self, file_path):
        self._ask_open_video(file_path)
        self._widget.setEnabled(True)
        self._download_button.setText('download')

    def _ask_open_video(self, file_path):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Question)
        message_box.setWindowTitle('pytube simple gui')
        message_box.setText(
            f'Successfully downloaded.\n\n"{file_path}"')
        message_box.addButton('Open video', QMessageBox.AcceptRole)
        message_box.addButton('OK', QMessageBox.RejectRole)

        result = message_box.exec()
        if result == QMessageBox.AcceptRole:
            open_file(file_path)

    def _on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress.emit(percentage_of_completion)

    def _on_complete(self, stream, file_path):
        self.download_completed.emit(file_path)

    def _on_error(self, error_message):
        self.error.emit(error_message)

    def _error(self, error_message):
        QMessageBox.warning(self, 'pytube simple gui', error_message)
        self._widget.setEnabled(True)

    def _download(self, source_url, destination_folder):
        self._video_downloader.download(
            source_url, destination_folder, self._on_progress, self._on_complete, self._on_error)

    def _async_download(self, source_url, destination_folder):
        thread = threading.Thread(
            target=self._download,
            args=[source_url, destination_folder],
            daemon=True)
        thread.start()
