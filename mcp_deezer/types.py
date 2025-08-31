"""
Unified Pydantic types for Deezer API
Documentation: https://developers.deezer.com/api/
"""

from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Literal, Optional, Union
from datetime import date, datetime


# ============================================================================
# GENRE TYPES
# ============================================================================

class DeezerGenre(BaseModel):
    """Deezer genre data model.
    
    Represents a music genre from the Deezer API.
    """
    id: int
    name: str
    picture: Optional[HttpUrl] = None
    type: Literal["genre"] = None


class DeezerGenreListResponse(BaseModel):
    """Response from /genre endpoint to get the list of genres"""
    data: List[DeezerGenre]


# ============================================================================
# USER TYPES
# ============================================================================

class DeezerUserBase(BaseModel):
    """Base user object with common fields.
    
    Contains the essential fields shared across different user contexts in the Deezer API.
    """
    id: int
    name: str
    tracklist: str
    type: Literal["user"] = "user"

class DeezerUserSearch(DeezerUserBase):
    """User object as returned in search contexts.
    
    Extends DeezerUserBase with additional picture fields for search results.
    """
    picture: Optional[HttpUrl] = None
    picture_small: Optional[HttpUrl] = None
    picture_medium: Optional[HttpUrl] = None
    picture_big: Optional[HttpUrl] = None
    picture_xl: Optional[HttpUrl] = None

class DeezerUser(DeezerUserBase):
    """Complete user object as returned by the Deezer API.
    
    Contains all available user information including profile pictures and country data.
    """
    picture: Optional[HttpUrl] = None
    picture_small: Optional[HttpUrl] = None
    picture_medium: Optional[HttpUrl] = None
    picture_big: Optional[HttpUrl] = None
    picture_xl: Optional[HttpUrl] = None
    country: str


class DeezerUserListResponse(BaseModel):
    """Response from user list endpoints"""
    data: List[DeezerUser]


# ============================================================================
# ARTIST TYPES
# ============================================================================

class DeezerArtistBase(BaseModel):
    """Base artist object with common fields.
    
    Contains the essential fields shared across different artist contexts in the Deezer API.
    """
    id: int
    name: str
    picture: Optional[HttpUrl] = None
    picture_small: Optional[HttpUrl] = None
    picture_medium: Optional[HttpUrl] = None
    picture_big: Optional[HttpUrl] = None
    picture_xl: Optional[HttpUrl] = None
    tracklist: str
    type: Literal["artist"]


class DeezerArtistSearch(DeezerArtistBase):
    """Artist object as returned in search contexts.
    
    Includes additional metadata like album count, fan count, and radio availability.
    """
    link: HttpUrl
    nb_album : int
    nb_fan : int
    radio: bool

class DeezerArtistContributors(DeezerArtistBase):
    """Artist object when appearing as a track contributor.
    
    Includes share URL, radio availability, and the artist's role in the track.
    """
    link: HttpUrl
    share : HttpUrl
    radio: bool
    role : str

class DeezerArtistTrack(DeezerArtistBase):
    """Artist object as it appears in track contexts.
    
    Simplified artist representation with share URL and radio availability.
    """
    link: HttpUrl
    share : HttpUrl
    radio : bool

class DeezerArtist(DeezerArtistBase):
    """Complete artist object with full metadata.
    
    Contains all available artist information including statistics and sharing options.
    """
    link: HttpUrl
    share : HttpUrl
    nb_album : int
    nb_fan : int
    radio: bool

class DeezerArtistListResponse(BaseModel):
    """Response from artist list endpoints"""
    data: List[DeezerArtistBase]


# ============================================================================
# ALBUM TYPES
# ============================================================================

class DeezerAlbumBase(BaseModel):
    """Base album object with common fields.
    
    Contains the essential fields shared across different album contexts in the Deezer API.
    """
    id: int
    title: str
    cover: str
    cover_small: Optional[HttpUrl] = None
    cover_medium: Optional[HttpUrl] = None
    cover_big: Optional[HttpUrl] = None
    cover_xl: Optional[HttpUrl] = None
    md5_image: str
    tracklist: str
    type: Literal["album"] = "album"


class DeezerAlbumSearch(DeezerAlbumBase):
    """Album object as returned in search contexts.
    
    Includes additional metadata like genre, track count, and artist information.
    """
    link: HttpUrl
    genre_id: int
    nb_tracks: int
    record_type: str
    explicit_lyrics : bool
    artist: DeezerArtistBase

class DeezerAlbumTrack(DeezerAlbumBase):
    """Album object as it appears in track contexts.
    
    Simplified album representation with link and release date.
    """
    link : HttpUrl
    release_date : datetime

class DeezerAlbum(DeezerAlbumBase):
    """Complete album object with full metadata.
    
    Contains all available album information including UPC, genres, and artist data.
    """
    upc : str
    link: HttpUrl
    share : HttpUrl
    genre_id: int
    genres: List[DeezerGenre]  # Direct list after extraction
    artist: DeezerArtistBase

    @field_validator('genres', mode='before')
    @classmethod
    def extract_genres_data(cls, v):
        if isinstance(v, dict) and 'data' in v:
            return v['data']
        return v

class DeezerAlbumListResponse(BaseModel):
    """Response from album list endpoints"""
    data: List[DeezerAlbum]


# ============================================================================
# TRACK TYPES
# ============================================================================

class DeezerTrackBase(BaseModel):
    """Base track object with common fields.
    
    Contains the essential fields shared across different track contexts in the Deezer API.
    """
    id: int
    readable: bool
    title: str
    title_short: str
    title_version: str
    link: HttpUrl
    rank: int
    explicit_lyrics: bool
    explicit_content_lyrics: int
    explicit_content_cover: int
    preview: HttpUrl
    md5_image : str
    type: Literal["track"] = "track"

class DeezerTrackSearch(DeezerTrackBase):
    """Track object as returned in search contexts.
    
    Includes basic artist and album information for search results.
    """
    artist: DeezerArtistBase
    album : DeezerAlbumBase

class DeezerTrackPlaylist(DeezerTrackBase):
    """Track object as it appears in playlist contexts.
    
    Includes ISRC code, addition timestamp, and basic artist/album info.
    """
    isrc : str
    time_add : int
    artist: DeezerArtistBase
    album : DeezerAlbumBase

class DeezerTrack(DeezerTrackBase):
    """Complete track object with full metadata.
    
    Contains all available track information including technical details, contributors, and availability.
    """
    isrc : str
    share : HttpUrl
    duration : int
    track_position : int
    disk_number : int
    release_date : datetime
    bpm : float
    gain : float
    available_countries : List[str]
    contributors : List[DeezerArtistContributors]
    artist : DeezerArtistTrack
    album : DeezerAlbumTrack


class DeezerTrackListResponse(BaseModel):
    """Response from track list endpoints"""
    data: List[DeezerTrackBase]


# ============================================================================
# PLAYLIST TYPES
# ============================================================================

class DeezerPlaylistBase(BaseModel):
    """Base playlist object with common fields.
    
    Contains the essential fields shared across different playlist contexts in the Deezer API.
    """
    id: int
    title: str
    public: bool
    nb_tracks: int
    link: HttpUrl
    picture : Optional[HttpUrl] = None
    picture_small: Optional[HttpUrl] = None
    picture_medium: Optional[HttpUrl] = None
    picture_big: Optional[HttpUrl] = None
    picture_xl: Optional[HttpUrl] = None
    checksum: str
    tracklist: str
    creation_date: datetime
    add_date : Optional[datetime] = None
    mod_date : Optional[datetime] = None
    md5_image: str
    picture_type: str
    type: Literal["playlist"] = "playlist"

class DeezerPlaylistSearch(DeezerPlaylistBase):
    user: DeezerUserBase

class DeezerPlaylist(DeezerPlaylistBase):
    """Complete playlist object with full metadata and track list.
    
    Contains all available playlist information including description, collaboration settings, and tracks.
    """
    description: str
    duration: int
    public: bool
    is_loved_track: bool
    collaborative: bool
    fans: int
    share: HttpUrl
    creation_date: datetime
    add_date: Optional[datetime] = None
    mod_date: Optional[datetime] = None
    tracks: List[DeezerTrackPlaylist]
    
    @field_validator('tracks', mode='before')
    @classmethod
    def extract_tracks_data(cls, v):
        """Extract tracks from data container if necessary."""
        if isinstance(v, dict) and 'data' in v:
            return v['data']
        return v



DeezerAlbum.model_rebuild()
DeezerTrack.model_rebuild()
DeezerPlaylist.model_rebuild()