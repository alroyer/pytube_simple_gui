from pytube import YouTube
import os


class VideoDownloader:
    def __init__(self) -> None:
        pass

    def download(
            self,
            source_url: str,
            destination_folder: str,
            on_progress_callback=None,
            on_complete_callback=None,
            on_error_callback=None) -> None:
        try:
            you_tube = YouTube(
                url=source_url,
                on_progress_callback=on_progress_callback,
                on_complete_callback=on_complete_callback)

            stream = you_tube.streams.get_highest_resolution()
            if stream:
                filename = self._get_filename(
                    destination_folder, stream.default_filename)
                stream.download(destination_folder, filename)
        except Exception:
            if on_error_callback:
                on_error_callback(f'Error downloading "{source_url}"')

    def _get_filename(self, destination_folder: str, filename: str):
        filename_without_ext, extension = filename.split('.')
        destination_path = os.path.join(destination_folder, filename)
        index = 1
        while os.path.exists(destination_path):
            destination_path = f'{os.path.join(destination_folder, filename_without_ext)} ({index}).{extension}'
            index += 1
        return os.path.basename(destination_path)
