from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerAlbum, DeezerTrackBase
from typing import List


class AlbumClient(BaseDeezerClient):
    async def get_album(self, album_id: int) -> DeezerAlbum:
        """
        Retrieve full details of an album by its ID.

        Args:
            album_id (int): The unique identifier of the album.

        Returns:
            DeezerAlbum: A Pydantic model containing album metadata.
        """
        response = await self._get(f"album/{album_id}")
        return DeezerAlbum(**response)

    async def get_tracks(self, album_id: int) -> List[DeezerTrackBase]:
        """
        Retrieve the list of tracks in an album.

        Args:
            album_id (int): The ID of the album.

        Returns:
            List[DeezerTrackBase]: A list of tracks in the album.
        """
        response = await self._get(f"album/{album_id}/tracks")
        return [DeezerTrackBase(**item) for item in response.get("data", [])]
