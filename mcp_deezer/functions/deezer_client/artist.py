from .base import BaseDeezerClient

class ArtistClient(BaseDeezerClient):
    async def search_artist(self, query: str) -> dict:
        return await self._get("search/artist", params={"q": query})

    async def get_artist(self, artist_id: int) -> dict:
        return await self._get(f"artist/{artist_id}")

    async def get_top_tracks(self, artist_id: int) -> dict:
        return await self._get(f"artist/{artist_id}/top")
