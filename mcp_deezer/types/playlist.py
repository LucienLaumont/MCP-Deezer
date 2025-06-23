# types/playlist.py
from pydantic import BaseModel, HttpUrl
from typing import Optional


class Playlist(BaseModel):
    id: int
    title: str
    description: Optional[str]
    duration: int
    public: bool
    is_loved_track: bool
    collaborative: bool
    nb_tracks: int
    fans: int
    link: HttpUrl
    share: HttpUrl
    picture: HttpUrl
    picture_small: HttpUrl
    picture_medium: HttpUrl
    picture_big: HttpUrl
    picture_xl: HttpUrl
    checksum: Optional[str]
    tracklist: HttpUrl
    creation_date: Optional[str]
    type: str
