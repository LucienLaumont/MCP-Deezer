from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerArtist
from typing import Optional, List


class ArtistNameClient(BaseDeezerClient):
    """Client to retrieve artists by their name."""

    async def get_artist_by_name(
        self, 
        artist_name: str, 
        limit: int = 1,
        strict: bool = True,
        order: str = "ARTIST_ASC"
    ) -> Optional[DeezerArtist]:
        """
        Retrieve an artist using the Deezer search endpoint with enhanced parameters.
        This method uses Deezer's search functionality for reliable results optimized for MCP tools.

        Args:
            artist_name (str): The artist name to search for
            limit (int, optional): Number of results to return. Defaults to 1 for single result.
            strict (bool, optional): If True, use exact match search. If False, use fuzzy search. Defaults to True.
            order (str, optional): Sort order for results. Options: ARTIST_ASC, ARTIST_DESC, ALBUM_ASC, 
                                 ALBUM_DESC, TRACK_ASC, TRACK_DESC, DURATION_ASC, DURATION_DESC, 
                                 RANKING. Defaults to "ARTIST_ASC".

        Returns:
            Optional[DeezerArtist]: The best matching artist or None if not found
        """
        try:
            # Build search query based on strict parameter
            if strict:
                search_query = f'artist:"{artist_name}"'
            else:
                search_query = artist_name
            
            # Prepare search parameters
            search_params = {
                "q": search_query,
                "limit": limit,
                "order": order
            }
            
            # Search using the search endpoint
            search_response = await self._get("search/artist", params=search_params)
            
            if not search_response.get("data"):
                # If strict search fails, try fuzzy search
                if strict:
                    return await self.get_artist_by_name(
                        artist_name=artist_name,
                        limit=limit,
                        strict=False,
                        order=order
                    )
                return None
                
            # Get the best match (first result)
            best_match = search_response["data"][0]
            artist_id = best_match["id"]
            
            # For MCP tools, we want complete data, so fetch full details
            artist_response = await self._get(f"artist/{artist_id}")
            return DeezerArtist(**artist_response)
            
        except Exception as e:
            print(f"Error searching for artist '{artist_name}': {e}")
            return None

    async def search_artists_by_name(
        self, 
        artist_name: str, 
        limit: int = 10,
        order: str = "RANKING"
    ) -> List[DeezerArtist]:
        """
        Search for multiple artists by name - useful for MCP tools that need multiple options.

        Args:
            artist_name (str): The artist name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            order (str, optional): Sort order for results. Defaults to "RANKING" for best matches first.

        Returns:
            List[DeezerArtist]: List of matching artists, empty list if none found
        """
        try:
            search_params = {
                "q": artist_name,
                "limit": limit,
                "order": order
            }
            
            search_response = await self._get("search/artist", params=search_params)
            
            if not search_response.get("data"):
                return []
                
            # Return list of artists from search results (these already have most needed data)
            return [DeezerArtist(**item) for item in search_response["data"]]
            
        except Exception as e:
            print(f"Error searching for artists '{artist_name}': {e}")
            return []