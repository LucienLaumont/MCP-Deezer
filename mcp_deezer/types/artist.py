"""
Pydantic types for Deezer Artist API
Documentation: https://developers.deezer.com/api/artist
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Literal


class DeezerArtistBase(BaseModel):
    """Artist object as returned by the Deezer API"""
    id: str
    name: str
    link: HttpUrl
    share: HttpUrl
    picture: HttpUrl
    picture_small: HttpUrl
    picture_medium: HttpUrl
    picture_big: HttpUrl
    picture_xl: HttpUrl
    radio: bool
    tracklist: HttpUrl
    type: Literal["artist"] = "artist"

class DeezerArtist(DeezerArtistBase):
    nb_album: int
    nb_fan: int

class DeezerTrackArtist(DeezerArtistBase):
    pass

class DeezerArtistListResponse(BaseModel):
    """Response from artist list endpoints"""
    data: List[DeezerArtist]