"""
Pydantic types for Deezer Playlist API
Documentation: https://developers.deezer.com/api/playlist
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Literal, Optional
from datetime import datetime
from .track import DeezerTrackBase
from .user import DeezerUser  # Assuming we have a user type


class DeezerPlaylistBase(BaseModel):
    """Base playlist object with common fields"""
    id: str
    title: str
    description: Optional[str] = None
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
    checksum: str
    tracklist: HttpUrl
    creation_date: datetime
    md5_image: str
    picture_type: str
    type: Literal["playlist"] = "playlist"


class DeezerPlaylist(DeezerPlaylistBase):
    """Complete playlist object as returned by the Deezer API"""
    creator: DeezerUser
    tracks: Optional[List[DeezerTrackBase]] = None


class DeezerPlaylistListResponse(BaseModel):
    """Response from playlist list endpoints"""
    data: List[DeezerPlaylist]


class DeezerPlaylistTracksResponse(BaseModel):
    """Response from playlist tracks endpoint"""
    data: List[DeezerTrackBase]
    total: Optional[int] = None
    next: Optional[str] = None