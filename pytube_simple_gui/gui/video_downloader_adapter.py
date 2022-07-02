from PySide6.QtCore import Signal


class VideoDownloaderAdapter():
    progress = Signal()
    complete = Signal()
    error = Signal()

    def __init__(self, on_progress_callback, on_complete_callback, on_error_callback) -> None:
        self.on_progress_callback = on_progress_callback
        self.on_complete_callback = on_complete_callback
        self.on_error_callback = on_error_callback

    def download(self, source_url, destination_file_path):
        pass

    def _on_progress(self):
        pass

    def _on_complete(self):
        pass

    def _on_error(self):
        pass
