import json
from typing import Any, Dict, Literal
from uuid import UUID

from pydantic import BaseModel


class DownloaderFileSchema(BaseModel):
    url: str
    format: Literal["mp3", "mp4", "webm", "mkv", "wav"]