"""
Pydantic types for Deezer Genre API
Documentation: https://developers.deezer.com/api/genre
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Literal


class DeezerGenre(BaseModel):
    """Genre object as returned by the Deezer API"""
    id: int
    name: str
    picture: HttpUrl
    picture_small: HttpUrl
    picture_medium: HttpUrl
    picture_big: HttpUrl
    picture_xl: HttpUrl
    type: Literal["genre"] = "genre"


class DeezerGenreListResponse(BaseModel):
    """Response from /genre endpoint to get the list of genres"""
    data: List[DeezerGenre]