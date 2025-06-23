from .base import BaseDeezerClient
from types.artist import Artist
from types.track import Track
from typing import List


class ArtistClient(BaseDeezerClient):
    async def search_artist(self, name: str) -> List[Artist]:
        """
        Search for artists by name.

        Args:
            name (str): The artist name to search for.

        Returns:
            List[Artist]: A list of matching artists.
        """
        response = await self._get("search/artist", params={"q": name})
        return [Artist(**item) for item in response.get("data", [])]

    async def get_artist(self, artist_id: int) -> Artist:
        """
        Get detailed information about an artist by their ID.

        Args:
            artist_id (int): The unique ID of the artist.

        Returns:
            Artist: The artist data.
        """
        response = await self._get(f"artist/{artist_id}")
        return Artist(**response)

    async def get_top_tracks(self, artist_id: int) -> List[Track]:
        """
        Get the top tracks of a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[Track]: A list of the artist's most popular tracks.
        """
        response = await self._get(f"artist/{artist_id}/top")
        return [Track(**item) for item in response.get("data", [])]
