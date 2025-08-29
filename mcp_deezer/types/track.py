"""
Pydantic types for Deezer Track API
Documentation: https://developers.deezer.com/api/track
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Literal
from datetime import date
from .artist import DeezerTrackArtist
from .album import DeezerAlbumBase


class DeezerTrackContributor(DeezerTrackArtist):
    """Contributor object in track context (extends artist with role)"""
    role: str


class DeezerTrackBase(BaseModel):
    """Base track object with common fields"""
    id: str
    readable: bool
    title: str
    title_short: str
    title_version: str
    isrc: str
    link: HttpUrl
    duration: str
    track_position: int
    disk_number: int
    rank: str
    explicit_lyrics: bool
    explicit_content_lyrics: int
    explicit_content_cover: int
    preview: HttpUrl
    artist: DeezerTrackArtist
    type: Literal["track"] = "track"


class DeezerTrack(DeezerTrackBase):
    """Complete track object as returned by the Deezer API"""
    share: HttpUrl
    release_date: date
    bpm: float
    gain: float
    available_countries: List[str]
    contributors: List[DeezerTrackContributor]
    md5_image: str
    track_token: str
    album: DeezerAlbumBase


class DeezerTrackListResponse(BaseModel):
    """Response from track list endpoints"""
    data: List[DeezerTrack]