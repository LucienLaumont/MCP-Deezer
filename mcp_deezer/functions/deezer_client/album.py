from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerAlbum
from typing import Optional, List


class AlbumNameClient(BaseDeezerClient):
    """Client to retrieve albums by their name."""

    async def get_album_by_name(
        self, 
        album_name: str, 
        limit: int = 1,
        strict: bool = True,
        order: str = "ALBUM_ASC"
    ) -> Optional[DeezerAlbum]:
        """
        Retrieve an album using the Deezer search endpoint with enhanced parameters.
        This method uses Deezer's search functionality for reliable results optimized for MCP tools.

        Args:
            album_name (str): The album name to search for
            limit (int, optional): Number of results to return. Defaults to 1 for single result.
            strict (bool, optional): If True, use exact match search. If False, use fuzzy search. Defaults to True.
            order (str, optional): Sort order for results. Options: ALBUM_ASC, ALBUM_DESC, ARTIST_ASC, 
                                 ARTIST_DESC, TRACK_ASC, TRACK_DESC, DURATION_ASC, DURATION_DESC, 
                                 RANKING. Defaults to "ALBUM_ASC".

        Returns:
            Optional[DeezerAlbum]: The best matching album or None if not found
        """
        try:
            # Build search query based on strict parameter
            if strict:
                search_query = f'album:"{album_name}"'
            else:
                search_query = album_name
            
            # Prepare search parameters
            search_params = {
                "q": search_query,
                "limit": limit,
                "order": order
            }
            
            # Search using the search endpoint
            search_response = await self._get("search/album", params=search_params)
            
            if not search_response.get("data"):
                # If strict search fails, try fuzzy search
                if strict:
                    return await self.get_album_by_name(
                        album_name=album_name,
                        limit=limit,
                        strict=False,
                        order=order
                    )
                return None
                
            # Get the best match (first result)
            best_match = search_response["data"][0]
            album_id = best_match["id"]
            
            # For MCP tools, we want complete data, so fetch full details
            album_response = await self._get(f"album/{album_id}")
            return DeezerAlbum(**album_response)
            
        except Exception as e:
            print(f"Error searching for album '{album_name}': {e}")
            return None

    async def search_albums_by_name(
        self, 
        album_name: str, 
        limit: int = 10,
        order: str = "RANKING"
    ) -> List[DeezerAlbum]:
        """
        Search for multiple albums by name - useful for MCP tools that need multiple options.

        Args:
            album_name (str): The album name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            order (str, optional): Sort order for results. Defaults to "RANKING" for best matches first.

        Returns:
            List[DeezerAlbum]: List of matching albums, empty list if none found
        """
        try:
            search_params = {
                "q": album_name,
                "limit": limit,
                "order": order
            }
            
            search_response = await self._get("search/album", params=search_params)
            
            if not search_response.get("data"):
                return []
                
            # Return list of albums from search results (these already have most needed data)
            return [DeezerAlbum(**item) for item in search_response["data"]]
            
        except Exception as e:
            print(f"Error searching for albums '{album_name}': {e}")
            return []