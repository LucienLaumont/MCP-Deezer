# types/track.py
from pydantic import BaseModel, HttpUrl
from typing import Optional


class Track(BaseModel):
    id: int
    readable: bool
    title: str
    title_short: str
    title_version: Optional[str]
    link: HttpUrl
    duration: int
    rank: int
    explicit_lyrics: bool
    preview: HttpUrl
    artist: dict
    album: dict
    type: str
