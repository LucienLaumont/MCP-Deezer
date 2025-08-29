from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerTrack


class TrackClient(BaseDeezerClient):
    async def get_track(self, track_id: int) -> DeezerTrack:
        """
        Retrieve full details of a track by its ID.

        Args:
            track_id (int): The unique identifier of the track.

        Returns:
            DeezerTrack: A Pydantic model containing track information.
        """
        response = await self._get(f"track/{track_id}")
        return DeezerTrack(**response)
