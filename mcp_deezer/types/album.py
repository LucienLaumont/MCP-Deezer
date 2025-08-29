"""
Pydantic types for Deezer Album API
Documentation: https://developers.deezer.com/api/album
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Literal, Optional
from datetime import date
from .artist import DeezerTrackArtist  # Artist in album context (same as track context)
from .genre import DeezerGenre
from .track import DeezerTrackBase


class DeezerAlbumBase(BaseModel):
    """Base album object with common fields"""
    id: str
    title: str
    link: HttpUrl
    cover: HttpUrl
    cover_small: HttpUrl
    cover_medium: HttpUrl
    cover_big: HttpUrl
    cover_xl: HttpUrl
    md5_image: str
    release_date: date
    tracklist: HttpUrl
    type: Literal["album"] = "album"


class DeezerAlbum(DeezerAlbumBase):
    """Complete album object as returned by the Deezer API"""
    upc: str
    share: HttpUrl
    genre_id: int
    genres: DeezerGenre
    label: str
    nb_tracks: int
    duration: int
    fans: int
    rating: int
    record_type: str
    available: bool
    alternative: Optional["DeezerAlbum"] = None
    artist: DeezerTrackArtist
    tracks: Optional[List[DeezerTrackBase]] = None


class DeezerAlbumListResponse(BaseModel):
    """Response from album list endpoints"""
    data: List[DeezerAlbum]