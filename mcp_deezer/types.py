"""
Unified Pydantic types for Deezer API
Documentation: https://developers.deezer.com/api/
"""

from pydantic import BaseModel, HttpUrl, Field, AliasPath
from typing import List, Literal, Optional, Union
from datetime import date, datetime


# ============================================================================
# GENRE TYPES
# ============================================================================

class DeezerGenre(BaseModel):
    id: int
    name: str
    picture: Optional[HttpUrl] = None
    picture_small: Optional[HttpUrl] = None
    picture_medium: Optional[HttpUrl] = None
    picture_big: Optional[HttpUrl] = None
    picture_xl: Optional[HttpUrl] = None
    type: Optional[Literal["genre"]] = None


class DeezerGenreListResponse(BaseModel):
    """Response from /genre endpoint to get the list of genres"""
    data: List[DeezerGenre]


# ============================================================================
# USER TYPES
# ============================================================================

class DeezerUserBase(BaseModel):
    """Base user object with common fields"""
    id: int
    name: str
    link: Optional[HttpUrl] = None
    picture: Optional[HttpUrl] = None
    picture_small: Optional[HttpUrl] = None
    picture_medium: Optional[HttpUrl] = None
    picture_big: Optional[HttpUrl] = None
    picture_xl: Optional[HttpUrl] = None
    type: Literal["user"] = "user"


class DeezerUser(DeezerUserBase):
    """Complete user object as returned by the Deezer API"""
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = None
    birthday: Optional[date] = None
    inscription_date: Optional[date] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    lang: Optional[str] = None
    is_kid: Optional[bool] = None
    explicit_content_level: Optional[str] = None
    explicit_content_levels_available: Optional[List[str]] = []
    tracklist: HttpUrl


class DeezerUserListResponse(BaseModel):
    """Response from user list endpoints"""
    data: List[DeezerUser]


# ============================================================================
# ARTIST TYPES
# ============================================================================

class DeezerArtistBase(BaseModel):
    """Base artist object with common fields"""
    id: int
    name: str
    link: Optional[HttpUrl] = None
    share: Optional[HttpUrl] = None
    picture: Optional[HttpUrl] = None
    picture_small: Optional[HttpUrl] = None
    picture_medium: Optional[HttpUrl] = None
    picture_big: Optional[HttpUrl] = None
    picture_xl: Optional[HttpUrl] = None
    radio: Optional[bool] = None
    tracklist: Optional[HttpUrl] = None
    type: Optional[Literal["artist"]] = None


class DeezerArtist(DeezerArtistBase):
    """Complete artist object as returned by the Deezer API"""
    link: HttpUrl
    share: Optional[HttpUrl] = None
    picture: HttpUrl
    picture_small: HttpUrl
    picture_medium: HttpUrl
    picture_big: HttpUrl
    picture_xl: HttpUrl
    radio: bool
    tracklist: HttpUrl
    type: Literal["artist"] = "artist"

    nb_album: int
    nb_fan: int



class DeezerTrackArtist(DeezerArtistBase):
    """Artist object in track/album context (simplified)"""
    pass


class DeezerArtistListResponse(BaseModel):
    """Response from artist list endpoints"""
    data: List[DeezerArtist]


# ============================================================================
# ALBUM TYPES
# ============================================================================

class DeezerAlbumBase(BaseModel):
    """Base album object with common fields"""
    id: int
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
    genres: list[DeezerGenre] = Field(
        default_factory=list,
        validation_alias=AliasPath("genres", "data"),
    )
    label: str
    nb_tracks: int
    duration: int
    fans: int
    rating: Optional[int] = None
    record_type: str
    available: bool
    alternative: Optional["DeezerAlbum"] = None
    artist: DeezerTrackArtist
    tracks: list["DeezerTrackBase"] = Field(
        default_factory=list,
        validation_alias=AliasPath("tracks", "data"),
    )


class DeezerAlbumListResponse(BaseModel):
    """Response from album list endpoints"""
    data: List[DeezerAlbum]


# ============================================================================
# TRACK TYPES
# ============================================================================

class DeezerTrackContributor(DeezerTrackArtist):
    """Contributor object in track context (extends artist with role)"""
    role: str


class DeezerTrackBase(BaseModel):
    """Base track object with common fields"""
    id: int
    readable: bool
    title: str
    title_short: str
    title_version: Optional[str] = None
    isrc: Optional[str] = None
    link: HttpUrl
    duration: int
    track_position: Optional[int] = None
    disk_number: Optional[int] = None
    rank: int
    explicit_lyrics: bool
    explicit_content_lyrics: int
    explicit_content_cover: int
    preview: str
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


# ============================================================================
# PLAYLIST TYPES
# ============================================================================

class DeezerPlaylistBase(BaseModel):
    """Base playlist object with common fields"""
    id: int
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
    tracks: list["DeezerTrackBase"] = Field(
        default_factory=list,
        validation_alias=AliasPath("tracks", "data"),
    )


class DeezerPlaylistListResponse(BaseModel):
    """Response from playlist list endpoints"""
    data: List[DeezerPlaylist]


class DeezerPlaylistTracksResponse(BaseModel):
    """Response from playlist tracks endpoint"""
    data: List[DeezerTrackBase]
    total: Optional[int] = None
    next: Optional[str] = None

DeezerAlbum.model_rebuild()
DeezerTrack.model_rebuild()
DeezerPlaylist.model_rebuild()