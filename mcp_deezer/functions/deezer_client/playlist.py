from .base import BaseDeezerClient
from types.playlist import Playlist


class PlaylistClient(BaseDeezerClient):
    async def get_playlist(self, playlist_id: int) -> Playlist:
        """
        Retrieve full details of a playlist by its ID.

        Args:
            playlist_id (int): The unique identifier of the playlist.

        Returns:
            Playlist: A Pydantic model containing playlist metadata.
        """
        response = await self._get(f"playlist/{playlist_id}")
        return Playlist(**response)
