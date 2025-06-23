from .base import BaseDeezerClient
from types.track import Track


class TrackClient(BaseDeezerClient):
    async def get_track(self, track_id: int) -> Track:
        """
        Retrieve full details of a track by its ID.

        Args:
            track_id (int): The unique identifier of the track.

        Returns:
            Track: A Pydantic model containing track information.
        """
        response = await self._get(f"track/{track_id}")
        return Track(**response)
