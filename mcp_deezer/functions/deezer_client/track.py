from .base import BaseDeezerClient

class TrackClient(BaseDeezerClient):
    async def get_track(self, track_id: int) -> dict:
        return await self._get(f"track/{track_id}")
