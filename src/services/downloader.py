import yt_dlp as ytdlp
import urllib.parse

from src.schemas.downloader import DownloaderFileSchema


class DownloaderService(object):
    def __init__(self, body: DownloaderFileSchema) -> None:
        self.url = body.url
        self.format = body.format

    def download(self) -> str:
        if self.format in ["mp3", "wav"]:
            ydl_opts = {
                "format": "bestaudio",
                "outtmpl": "media/%(title)s.%(ext)s",
                "overwrites": False,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.format,
                }],
            }
        else:
            ydl_opts = {
                "format": self.format,
                "outtmpl": "media/%(title)s.%(ext)s",
                "overwrites": False
            }

        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            
        return urllib.parse.quote(f"media/{info['title']}.{self.format}")