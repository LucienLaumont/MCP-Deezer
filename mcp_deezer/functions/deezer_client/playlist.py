from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerPlaylist, DeezerPlaylistBase
from typing import Optional, List


class PlaylistNameClient(BaseDeezerClient):
    """Client to retrieve playlists by their name and ID."""


    async def get_playlist(self, playlist_id: int) -> Optional[DeezerPlaylist]:
        """
        Retrieve a complete playlist by its ID.

        Args:
            playlist_id (int): The Deezer playlist ID

        Returns:
            Optional[DeezerPlaylist]: The complete playlist data or None if not found
        """
        try:
            playlist_response = await self._get(f"playlist/{playlist_id}")
            return DeezerPlaylist(**playlist_response)
            
        except Exception as e:
            print(f"Error retrieving playlist with ID {playlist_id}: {e}")
            return None

    async def search_playlists_by_name(
        self, 
        playlist_name: str, 
        limit: int = 10,
        strict: Optional[bool] = None,
        order: Optional[str] = None
    ) -> List[DeezerPlaylistBase]:
        """
        Search for multiple playlists by name - useful for MCP tools that need multiple options.

        Args:
            playlist_name (str): The playlist name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            strict (bool, optional): If True, disable fuzzy mode. If None, uses default API behavior.
            order (str, optional): Sort order. Options: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, 
                                 ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, 
                                 DURATION_ASC, DURATION_DESC. If None, uses default API behavior.

        Returns:
            List[DeezerPlaylistBase]: List of matching playlists, empty list if none found
        """
        try:
            search_params = {
                "q": playlist_name,
                "limit": limit
            }
            
            # Add optional parameters if provided
            if strict is not None:
                search_params["strict"] = "on" if strict else "off"
            if order is not None:
                search_params["order"] = order
            
            search_response = await self._get("search/playlist", params=search_params)
            
            if not search_response.get("data"):
                return []
                
            # Return list of playlists from search results using DeezerPlaylistBase type
            return [DeezerPlaylistBase(**item) for item in search_response["data"]]
            
        except Exception as e:
            print(f"Error searching for playlists '{playlist_name}': {e}")
            return []

    async def get_playlist_by_name_and_creator(
        self, 
        playlist_name: str, 
        creator_name: str,
        limit: int = 1,
        order: str = "RANKING"
    ) -> Optional[DeezerPlaylist]:
        """
        Retrieve a playlist by combining playlist name and creator name for more precise results.
        This is particularly useful for MCP tools when you know the playlist creator.

        Args:
            playlist_name (str): The playlist name to search for
            creator_name (str): The creator/user name to narrow the search
            limit (int, optional): Number of results to return. Defaults to 1.
            order (str, optional): Sort order for results. Defaults to "RANKING".

        Returns:
            Optional[DeezerPlaylist]: The best matching playlist or None if not found
        """
        try:
            # Build combined search query
            search_query = f'playlist:"{playlist_name}" user:"{creator_name}"'
            
            search_params = {
                "q": search_query,
                "limit": limit,
                "order": order
            }
            
            search_response = await self._get("search/playlist", params=search_params)
            
            if not search_response.get("data"):
                return None
                
            # Get the best match (first result)
            best_match = search_response["data"][0]
            playlist_id = best_match["id"]
            
            # Fetch complete playlist details
            playlist_response = await self._get(f"playlist/{playlist_id}")
            return DeezerPlaylist(**playlist_response)
            
        except Exception as e:
            print(f"Error searching for playlist '{playlist_name}' by creator '{creator_name}': {e}")
            return None

    async def search_public_playlists_by_name(
        self, 
        playlist_name: str, 
        limit: int = 10,
        strict: Optional[bool] = None,
        order: Optional[str] = None
    ) -> List[DeezerPlaylistBase]:
        """
        Search specifically for public playlists by name.
        This is useful for MCP tools focusing on discoverable/shareable playlists.

        Args:
            playlist_name (str): The playlist name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            strict (bool, optional): If True, disable fuzzy mode. If None, uses default API behavior.
            order (str, optional): Sort order. Options: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, 
                                 ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, 
                                 DURATION_ASC, DURATION_DESC. If None, uses default API behavior.

        Returns:
            List[DeezerPlaylistBase]: List of public playlists, empty list if none found
        """
        try:
            # Search for playlists and filter for public ones
            search_params = {
                "q": playlist_name,
                "limit": limit * 2  # Get more results to filter
            }
            
            # Add optional parameters if provided
            if strict is not None:
                search_params["strict"] = "on" if strict else "off"
            if order is not None:
                search_params["order"] = order
            
            search_response = await self._get("search/playlist", params=search_params)
            
            if not search_response.get("data"):
                return []
            
            # Filter for public playlists and limit results
            public_playlists = []
            for item in search_response["data"]:
                if item.get("public", False) and len(public_playlists) < limit:
                    public_playlists.append(DeezerPlaylistBase(**item))
                    
            return public_playlists
            
        except Exception as e:
            print(f"Error searching for public playlists '{playlist_name}': {e}")
            return []