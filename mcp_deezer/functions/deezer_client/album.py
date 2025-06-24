from .base import BaseDeezerClient
from types.album import Album
from types.track import Track
from typing import List


class AlbumClient(BaseDeezerClient):
    async def get_album(self, album_id: int) -> Album:
        """
        Retrieve full details of an album by its ID.

        Args:
            album_id (int): The unique identifier of the album.

        Returns:
            Album: A Pydantic model containing album metadata.
        """
        response = await self._get(f"album/{album_id}")
        return Album(**response)

    async def get_tracks(self, album_id: int) -> List[Track]:
        """
        Retrieve the list of tracks in an album.

        Args:
            album_id (int): The ID of the album.

        Returns:
            List[Track]: A list of tracks in the album.
        """
        response = await self._get(f"album/{album_id}/tracks")
        return [Track(**item) for item in response.get("data", [])]
