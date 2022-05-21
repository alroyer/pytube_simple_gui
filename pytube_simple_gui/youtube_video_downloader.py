from pytube import YouTube


class YoutubeVideoDownloader:
    def __init__(self) -> None:
        pass

    def download(self, source_url: str, destination_folder: str, progree_callback=None, complete_callback=None) -> None:
        you_tube = YouTube(source_url)
        stream = you_tube.streams.get_highest_resolution()
        if stream:
            stream.download(destination_folder)
