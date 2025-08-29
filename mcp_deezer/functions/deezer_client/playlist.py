from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerPlaylist, DeezerTrackBase
from typing import List


class PlaylistClient(BaseDeezerClient):
    async def get_playlist(self, playlist_id: int) -> DeezerPlaylist:
        """
        Retrieve full details of a playlist by its ID.

        Args:
            playlist_id (int): The unique identifier of the playlist.

        Returns:
            DeezerPlaylist: A Pydantic model containing playlist metadata.
        """
        response = await self._get(f"playlist/{playlist_id}")
        return DeezerPlaylist(**response)

    async def get_tracks(self, playlist_id: int) -> List[DeezerTrackBase]:
        """
        Retrieve the list of tracks in a playlist.

        Args:
            playlist_id (int): The ID of the playlist.

        Returns:
            List[DeezerTrackBase]: A list of tracks in the playlist.
        """
        response = await self._get(f"playlist/{playlist_id}/tracks")
        return [DeezerTrackBase(**item) for item in response.get("data", [])]