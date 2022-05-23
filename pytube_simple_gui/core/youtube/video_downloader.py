from pytube import YouTube


class VideoDownloader:
    def __init__(self) -> None:
        pass

    def download(self, source_url: str, destination_folder: str, on_progress_callback=None, on_complete_callback=None) -> None:
        you_tube = YouTube(source_url, on_progress_callback=on_progress_callback, on_complete_callback=on_complete_callback)
        stream = you_tube.streams.get_highest_resolution()
        if stream:
            stream.download(destination_folder)
