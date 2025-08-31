from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerArtist, DeezerArtistSearch
from typing import Optional, List


class ArtistNameClient(BaseDeezerClient):
    """Client to retrieve artists by their name and ID."""


    async def get_artist(self, artist_id: int) -> Optional[DeezerArtist]:
        """
        Retrieve a complete artist by its ID.

        Args:
            artist_id (int): The Deezer artist ID

        Returns:
            Optional[DeezerArtist]: The complete artist data or None if not found
        """
        try:
            artist_response = await self._get(f"artist/{artist_id}")
            return DeezerArtist(**artist_response)
            
        except Exception as e:
            print(f"Error retrieving artist with ID {artist_id}: {e}")
            return None

    async def search_artists_by_name(
        self, 
        artist_name: str, 
        limit: int = 10,
        strict: Optional[bool] = None,
        order: Optional[str] = None
    ) -> List[DeezerArtistSearch]:
        """
        Search for multiple artists by name - useful for MCP tools that need multiple options.

        Args:
            artist_name (str): The artist name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            strict (bool, optional): If True, disable fuzzy mode. If None, uses default API behavior.
            order (str, optional): Sort order. Options: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, 
                                 ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, 
                                 DURATION_ASC, DURATION_DESC. If None, uses default API behavior.

        Returns:
            List[DeezerArtistSearch]: List of matching artists, empty list if none found
        """
        try:
            search_params = {
                "q": artist_name,
                "limit": limit
            }
            
            # Add optional parameters if provided
            if strict is not None:
                search_params["strict"] = "on" if strict else "off"
            if order is not None:
                search_params["order"] = order
            
            search_response = await self._get("search/artist", params=search_params)
            
            if not search_response.get("data"):
                return []
                
            # Return list of artists from search results using DeezerArtistSearch type
            return [DeezerArtistSearch(**item) for item in search_response["data"]]
            
        except Exception as e:
            print(f"Error searching for artists '{artist_name}': {e}")
            return []