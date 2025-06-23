from .base import BaseDeezerClient
from types.album import Album


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
