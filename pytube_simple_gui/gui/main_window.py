import os
import threading

from PySide6.QtCore import QSettings, QSize, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

TITLE = 'pytube simple gui'


class MainWindow(QMainWindow):
    progress = Signal(int)
    download_completed = Signal(str)
    error = Signal(str, str)

    def __init__(self, video_downloader, video_player, translator):
        super().__init__()

        self._video_downloader = video_downloader
        self._video_player = video_player
        self._translator = translator

        self.progress.connect(self._progress)
        self.download_completed.connect(self._download_completed)
        self.error.connect(self._error)

        assets_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../assets')
        window_icon = QPixmap(os.path.join(assets_path, 'video-recorder-icon-32.png'))

        self.setWindowTitle(TITLE)
        self.setWindowIcon(window_icon)

        self._source_line_edit = QLineEdit()
        self._source_line_edit.setPlaceholderText('https://www.youtube.com/watch?v=9FnG9lGLyEM')
        self._source_line_edit.textChanged.connect(self._on_source_changed)

        self._destination_line_edit = QLineEdit()
        self._destination_line_edit.setReadOnly(True)

        browse_button = QPushButton('...')
        browse_button.clicked.connect(self._on_browse_button_clicked)

        self._download_button = QPushButton(self.tr('Download'))
        self._download_button.clicked.connect(self._on_download_button_clicked)

        horizontal_layout = QHBoxLayout()

        horizontal_layout.addWidget(self._destination_line_edit)
        horizontal_layout.addWidget(browse_button)

        self._widget = QWidget()

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel(self.tr('Source:')), 0, 0)
        grid_layout.addWidget(self._source_line_edit, 0, 1)

        grid_layout.addWidget(QLabel(self.tr('Destination:')), 1, 0)
        grid_layout.addLayout(horizontal_layout, 1, 1)

        vertical_layout = QVBoxLayout()

        vertical_layout.addLayout(grid_layout)
        vertical_layout.addWidget(self._download_button)

        self._widget.setLayout(vertical_layout)

        self.setCentralWidget(self._widget)

        self._read_settings()

        self._update_ui()

    def closeEvent(self, event):
        self._write_settings()
        return super().closeEvent(event)

    def _read_settings(self):
        settings = QSettings('alroyer', 'pytube simple gui')
        settings.beginGroup('mainwindow')
        destination = settings.value('destination')
        if destination and isinstance(destination, str):
            self._destination_line_edit.setText(destination)
        size = settings.value('size')
        if size and isinstance(size, QSize):
            self.resize(size)
        settings.endGroup()

    def _write_settings(self):
        settings = QSettings('alroyer', 'pytube simple gui')
        settings.beginGroup('mainwindow')
        settings.setValue('destination', self._destination_line_edit.text())
        settings.setValue('size', self.size())
        settings.endGroup()

    def _on_browse_button_clicked(self):
        selected_directory = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select destination folder'),
            self._destination_line_edit.text(),
            QFileDialog.Option.ShowDirsOnly,
        )
        if selected_directory:
            self._destination_line_edit.setText(selected_directory)

    def _on_download_button_clicked(self):
        self._widget.setEnabled(False)

        self._progress(0)

        source_url = self._source_line_edit.text()
        destination_folder = self._destination_line_edit.text()

        self._async_download(source_url, destination_folder)

    def _on_source_changed(self):
        self._update_ui()

    def _update_ui(self):
        self._download_button.setEnabled(
            self._source_line_edit.text().lower().startswith('https://www.youtube.com/watch?v=')
        )

    def _progress(self, percentage_of_completion):
        self._download_button.setText(self.tr('{}% completed').format(percentage_of_completion))

    def _download_completed(self, file_path):
        self._ask_open_video(file_path)
        self._widget.setEnabled(True)

        self._download_button.setText(self.tr('Download'))

    def _ask_open_video(self, file_path):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Icon.Question)
        message_box.setWindowTitle(TITLE)
        message_box.setText(self.tr('Successfully downloaded.\n\n"{}"').format(file_path))
        message_box.addButton(self.tr('Play video'), QMessageBox.ButtonRole.AcceptRole)
        message_box.addButton(self.tr('Close'), QMessageBox.ButtonRole.RejectRole)

        result = message_box.exec()
        if result == 0:
            self._video_player(file_path)

    def _on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress.emit(percentage_of_completion)

    def _on_complete(self, stream, file_path):
        self.download_completed.emit(file_path)

    def _on_error(self, source_url, error_message):
        self.error.emit(source_url, error_message)

    def _error(self, source_url, error_message):
        text = self.tr('Error downloading "{}"\n\n(details "{}")').format(source_url, error_message)
        QMessageBox.warning(self, TITLE, text)

        self._update_ui()
        self._widget.setEnabled(True)

    def _download(self, source_url, destination_folder):
        self._video_downloader.download(
            source_url, destination_folder, self._on_progress, self._on_complete, self._on_error
        )

    def _async_download(self, source_url, destination_folder):
        thread = threading.Thread(
            target=self._download, args=[source_url, destination_folder], daemon=True
        )
        thread.start()
