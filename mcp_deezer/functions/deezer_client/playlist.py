from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerPlaylist
from typing import Optional, List


class PlaylistNameClient(BaseDeezerClient):
    """Client to retrieve playlists by their name."""

    async def get_playlist_by_name(
        self, 
        playlist_name: str, 
        limit: int = 1,
        strict: bool = True,
        order: str = "PLAYLIST_ASC"
    ) -> Optional[DeezerPlaylist]:
        """
        Retrieve a playlist using the Deezer search endpoint with enhanced parameters.
        This method uses Deezer's search functionality for reliable results optimized for MCP tools.

        Args:
            playlist_name (str): The playlist name to search for
            limit (int, optional): Number of results to return. Defaults to 1 for single result.
            strict (bool, optional): If True, use exact match search. If False, use fuzzy search. Defaults to True.
            order (str, optional): Sort order for results. Options: PLAYLIST_ASC, PLAYLIST_DESC, ARTIST_ASC, 
                                 ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, TRACK_ASC, TRACK_DESC, 
                                 DURATION_ASC, DURATION_DESC, RANKING. Defaults to "PLAYLIST_ASC".

        Returns:
            Optional[DeezerPlaylist]: The best matching playlist or None if not found
        """
        try:
            # Build search query based on strict parameter
            if strict:
                search_query = f'playlist:"{playlist_name}"'
            else:
                search_query = playlist_name
            
            # Prepare search parameters
            search_params = {
                "q": search_query,
                "limit": limit,
                "order": order
            }
            
            # Search using the search endpoint
            search_response = await self._get("search/playlist", params=search_params)
            
            if not search_response.get("data"):
                # If strict search fails, try fuzzy search
                if strict:
                    return await self.get_playlist_by_name(
                        playlist_name=playlist_name,
                        limit=limit,
                        strict=False,
                        order=order
                    )
                return None
                
            # Get the best match (first result)
            best_match = search_response["data"][0]
            playlist_id = best_match["id"]
            
            # For MCP tools, we want complete data, so fetch full details
            playlist_response = await self._get(f"playlist/{playlist_id}")
            return DeezerPlaylist(**playlist_response)
            
        except Exception as e:
            print(f"Error searching for playlist '{playlist_name}': {e}")
            return None

    async def search_playlists_by_name(
        self, 
        playlist_name: str, 
        limit: int = 10,
        order: str = "RANKING"
    ) -> List[DeezerPlaylist]:
        """
        Search for multiple playlists by name - useful for MCP tools that need multiple options.

        Args:
            playlist_name (str): The playlist name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            order (str, optional): Sort order for results. Defaults to "RANKING" for best matches first.

        Returns:
            List[DeezerPlaylist]: List of matching playlists, empty list if none found
        """
        try:
            search_params = {
                "q": playlist_name,
                "limit": limit,
                "order": order
            }
            
            search_response = await self._get("search/playlist", params=search_params)
            
            if not search_response.get("data"):
                return []
                
            # Return list of playlists from search results (these already have most needed data)
            return [DeezerPlaylist(**item) for item in search_response["data"]]
            
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
        order: str = "RANKING"
    ) -> List[DeezerPlaylist]:
        """
        Search specifically for public playlists by name.
        This is useful for MCP tools focusing on discoverable/shareable playlists.

        Args:
            playlist_name (str): The playlist name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            order (str, optional): Sort order for results. Defaults to "RANKING".

        Returns:
            List[DeezerPlaylist]: List of public playlists, empty list if none found
        """
        try:
            # Search for playlists and filter for public ones
            search_params = {
                "q": playlist_name,
                "limit": limit * 2,  # Get more results to filter
                "order": order
            }
            
            search_response = await self._get("search/playlist", params=search_params)
            
            if not search_response.get("data"):
                return []
            
            # Filter for public playlists and limit results
            public_playlists = []
            for item in search_response["data"]:
                if item.get("public", False) and len(public_playlists) < limit:
                    public_playlists.append(DeezerPlaylist(**item))
                    
            return public_playlists
            
        except Exception as e:
            print(f"Error searching for public playlists '{playlist_name}': {e}")
            return []