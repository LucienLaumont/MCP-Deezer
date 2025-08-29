from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerArtist, DeezerTrackBase, DeezerAlbumBase, DeezerPlaylistBase
from typing import List


class ArtistClient(BaseDeezerClient):
    async def search_artist(self, name: str) -> List[DeezerArtist]:
        """
        Search for artists by name.

        Args:
            name (str): The artist name to search for.

        Returns:
            List[DeezerArtist]: A list of matching artists.
        """
        response = await self._get("search/artist", params={"q": name})
        return [DeezerArtist(**item) for item in response.get("data", [])]

    async def get_artist(self, artist_id: int) -> DeezerArtist:
        """
        Get detailed information about an artist by their ID.

        Args:
            artist_id (int): The unique ID of the artist.

        Returns:
            DeezerArtist: The artist data.
        """
        response = await self._get(f"artist/{artist_id}")
        return DeezerArtist(**response)

    async def get_top_tracks(self, artist_id: int) -> List[DeezerTrackBase]:
        """
        Get the 5 top tracks of a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[DeezerTrackBase]: A list of the artist's most popular tracks.
        """
        response = await self._get(f"artist/{artist_id}/top")
        return [DeezerTrackBase(**item) for item in response.get("data", [])]

    async def get_albums(self, artist_id: int) -> List[DeezerAlbumBase]:
        """
        Get all albums of a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[DeezerAlbumBase]: A list of the artist's albums.
        """
        response = await self._get(f"artist/{artist_id}/albums")
        return [DeezerAlbumBase(**item) for item in response.get("data", [])]

    async def get_related_artists(self, artist_id: int) -> List[DeezerArtist]:
        """
        Get related artists for a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[DeezerArtist]: A list of related artists.
        """
        response = await self._get(f"artist/{artist_id}/related")
        return [DeezerArtist(**item) for item in response.get("data", [])]

    async def get_playlists(self, artist_id: int) -> List[DeezerPlaylistBase]:
        """
        Get playlists featuring a given artist.

        Args:
            artist_id (int): The artist's ID.

        Returns:
            List[DeezerPlaylistBase]: A list of playlists related to the artist.
        """
        response = await self._get(f"artist/{artist_id}/playlists")
        return [DeezerPlaylistBase(**item) for item in response.get("data", [])]