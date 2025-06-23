# types/album.py
from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import Optional


class Album(BaseModel):
    id: int
    title: str
    upc: Optional[str]
    link: HttpUrl
    share: HttpUrl
    cover: HttpUrl
    cover_small: HttpUrl
    cover_medium: HttpUrl
    cover_big: HttpUrl
    cover_xl: HttpUrl
    genre_id: Optional[int]
    fans: Optional[int]
    release_date: date
    record_type: str
    available: bool
    tracklist: HttpUrl
    explicit_lyrics: bool
    type: str
