"""
Pydantic types for Deezer User API
Documentation: https://developers.deezer.com/api/user
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Literal, Optional
from datetime import date


class DeezerUserBase(BaseModel):
    """Base user object with common fields"""
    id: str
    name: str
    link: HttpUrl
    picture: HttpUrl
    picture_small: HttpUrl
    picture_medium: HttpUrl
    picture_big: HttpUrl
    picture_xl: HttpUrl
    type: Literal["user"] = "user"


class DeezerUser(DeezerUserBase):
    """Complete user object as returned by the Deezer API"""
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    email: Optional[str] = None
    status: int
    birthday: Optional[date] = None
    inscription_date: date
    gender: Optional[str] = None
    country: str
    lang: Optional[str] = None
    is_kid: bool
    explicit_content_level: str
    explicit_content_levels_available: List[str]
    tracklist: HttpUrl


class DeezerUserListResponse(BaseModel):
    """Response from user list endpoints"""
    data: List[DeezerUser]