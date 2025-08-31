from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerAlbum, DeezerAlbumSearch
from typing import Optional, List


class AlbumNameClient(BaseDeezerClient):
    """Client to retrieve albums by their name and ID."""


    async def get_album(self, album_id: int) -> Optional[DeezerAlbum]:
        """
        Retrieve a complete album by its ID.

        Args:
            album_id (int): The Deezer album ID

        Returns:
            Optional[DeezerAlbum]: The complete album data or None if not found
        """
        try:
            album_response = await self._get(f"album/{album_id}")
            return DeezerAlbum(**album_response)
            
        except Exception as e:
            print(f"Error retrieving album with ID {album_id}: {e}")
            return None

    async def search_albums_by_name(
        self, 
        album_name: str, 
        limit: int = 10,
        strict: Optional[bool] = None,
        order: Optional[str] = None
    ) -> List[DeezerAlbumSearch]:
        """
        Search for multiple albums by name - useful for MCP tools that need multiple options.

        Args:
            album_name (str): The album name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            strict (bool, optional): If True, disable fuzzy mode. If None, uses default API behavior.
            order (str, optional): Sort order. Options: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, 
                                 ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, 
                                 DURATION_ASC, DURATION_DESC. If None, uses default API behavior.

        Returns:
            List[DeezerAlbumSearch]: List of matching albums, empty list if none found
        """
        try:
            search_params = {
                "q": album_name,
                "limit": limit
            }
            
            # Add optional parameters if provided
            if strict is not None:
                search_params["strict"] = "on" if strict else "off"
            if order is not None:
                search_params["order"] = order
            
            search_response = await self._get("search/album", params=search_params)
            
            if not search_response.get("data"):
                return []
                
            # Return list of albums from search results using DeezerAlbumSearch type
            return [DeezerAlbumSearch(**item) for item in search_response["data"]]
            
        except Exception as e:
            print(f"Error searching for albums '{album_name}': {e}")
            return []