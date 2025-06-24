from .base import BaseDeezerClient
from types.playlist import Playlist
from types.track import Track
from typing import List


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

    async def get_tracks(self, playlist_id: int) -> List[Track]:
        """
        Retrieve the list of tracks in a playlist.

        Args:
            playlist_id (int): The ID of the playlist.

        Returns:
            List[Track]: A list of tracks in the playlist.
        """
        response = await self._get(f"playlist/{playlist_id}/tracks")
        return [Track(**item) for item in response.get("data", [])]