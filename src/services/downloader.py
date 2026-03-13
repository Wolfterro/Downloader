import os
import time

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
                "format": "bestaudio/best",
                "outtmpl": "media/%(title)s.%(ext)s",
                "overwrites": False,
                "noplaylist": True,
                "restrictfilenames": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.format,
                }],
            }
        else:
            ydl_opts = {
                "format": self.format,
                "outtmpl": "media/%(title)s.%(ext)s",
                "overwrites": False,
                "noplaylist": True,
                "restrictfilenames": True
            }

        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            filename = ydl.prepare_filename(info)

        if self.format in ["mp3", "wav"]:
            filename = os.path.splitext(filename)[0] + f".{self.format}"

        return urllib.parse.quote(filename)
