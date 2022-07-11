from PySide6.QtCore import QObject, Signal
from pytube import YouTube

import os
import threading


class VideoDownloader(QObject):
    progressed = Signal(int, str, str)
    completed = Signal(str, str)
    error = Signal(str)

    def __init__(self, on_progress_callback, on_complete_callback, on_error_callback):
        super().__init__()

        self.on_progress_callback = on_progress_callback
        self.on_complete_callback = on_complete_callback
        self.on_error_callback = on_error_callback

        self._queue = {}

    def download(self, source_url, destination_folder):
        thread = threading.Thread(
            target=self._async_download,
            args=[source_url, destination_folder],
            daemon=True)
        thread.start()

    def _async_download(self, source_url, destination_folder):
        try:
            you_tube = YouTube(
                source_url,
                self._on_progress_callback,
                self._on_complete_callback)

            stream = you_tube.streams.get_highest_resolution()
            if stream:
                filename = self._get_filename(
                    destination_folder, stream.default_filename)
                self._queue[stream] = (stream.title, os.path.join(
                    destination_folder, filename))
                stream.download(destination_folder, filename)
        except Exception:
            self._on_error_callback(source_url)

    def _get_filename(self, destination_folder, filename):
        filename_without_ext, extension = filename.split('.')
        destination_path = os.path.join(destination_folder, filename)
        index = 1
        while os.path.exists(destination_path):
            destination_path = f'{os.path.join(destination_folder, filename_without_ext)} ({index}).{extension}'
            index += 1
        return os.path.basename(destination_path)

    def _on_progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        title, destination_path = self._queue[stream]
        self.progressed.emit(percentage_of_completion, title, destination_path)

    def _on_complete_callback(self, stream, destination_path):
        source_url, destination_path = self._queue[stream]
        self._queue.pop(stream)
        self.completed.emit(source_url, destination_path)

    def _on_error_callback(self, source_url):
        self.error.emit(source_url)
