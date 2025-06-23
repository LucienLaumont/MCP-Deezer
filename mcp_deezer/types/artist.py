# types/artist.py
from pydantic import BaseModel, HttpUrl


class Artist(BaseModel):
    id: int
    name: str
    link: HttpUrl
    share: HttpUrl
    picture: HttpUrl
    picture_small: HttpUrl
    picture_medium: HttpUrl
    picture_big: HttpUrl
    picture_xl: HttpUrl
    nb_album: int
    nb_fan: int
    radio: bool
    tracklist: HttpUrl
    type: str
