from .base import BaseDeezerClient
from types.artist import Artist
from types.track import Track
from types.album import Album
from types.playlist import Playlist
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
        Get the 5 top tracks of a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[Track]: A list of the artist's most popular tracks.
        """
        response = await self._get(f"artist/{artist_id}/top")
        return [Track(**item) for item in response.get("data", [])]

    async def get_albums(self, artist_id: int) -> List[Album]:
        """
        Get all albums of a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[Album]: A list of the artist's albums.
        """
        response = await self._get(f"artist/{artist_id}/albums")
        return [Album(**item) for item in response.get("data", [])]

    async def get_related_artists(self, artist_id: int) -> List[Artist]:
        """
        Get related artists for a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[Artist]: A list of related artists.
        """
        response = await self._get(f"artist/{artist_id}/related")
        return [Artist(**item) for item in response.get("data", [])]

    async def get_playlists(self, artist_id: int) -> List[Playlist]:
        """
        Get playlists featuring a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[Playlist]: A list of playlists related to the artist.
        """
        response = await self._get(f"artist/{artist_id}/playlists")
        return [Playlist(**item) for item in response.get("data", [])]