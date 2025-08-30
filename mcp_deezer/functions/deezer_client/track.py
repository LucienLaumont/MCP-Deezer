from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerTrack
from typing import Optional, List


class TrackNameClient(BaseDeezerClient):
    """Client to retrieve tracks by their name."""

    async def get_track_by_name(
        self, 
        track_name: str, 
        limit: int = 1,
        strict: bool = True,
        order: str = "TRACK_ASC"
    ) -> Optional[DeezerTrack]:
        """
        Retrieve a track using the Deezer search endpoint with enhanced parameters.
        This method uses Deezer's search functionality for reliable results optimized for MCP tools.

        Args:
            track_name (str): The track name to search for
            limit (int, optional): Number of results to return. Defaults to 1 for single result.
            strict (bool, optional): If True, use exact match search. If False, use fuzzy search. Defaults to True.
            order (str, optional): Sort order for results. Options: TRACK_ASC, TRACK_DESC, ARTIST_ASC, 
                                 ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, DURATION_ASC, DURATION_DESC, 
                                 RANKING. Defaults to "TRACK_ASC".

        Returns:
            Optional[DeezerTrack]: The best matching track or None if not found
        """
        try:
            # Build search query based on strict parameter
            if strict:
                search_query = f'track:"{track_name}"'
            else:
                search_query = track_name
            
            # Prepare search parameters
            search_params = {
                "q": search_query,
                "limit": limit,
                "order": order
            }
            
            # Search using the search endpoint
            search_response = await self._get("search/track", params=search_params)
            
            if not search_response.get("data"):
                # If strict search fails, try fuzzy search
                if strict:
                    return await self.get_track_by_name(
                        track_name=track_name,
                        limit=limit,
                        strict=False,
                        order=order
                    )
                return None
                
            # Get the best match (first result)
            best_match = search_response["data"][0]
            track_id = best_match["id"]
            
            # For MCP tools, we want complete data, so fetch full details
            track_response = await self._get(f"track/{track_id}")
            return DeezerTrack(**track_response)
            
        except Exception as e:
            print(f"Error searching for track '{track_name}': {e}")
            return None

    async def search_tracks_by_name(
        self, 
        track_name: str, 
        limit: int = 10,
        order: str = "RANKING"
    ) -> List[DeezerTrack]:
        """
        Search for multiple tracks by name - useful for MCP tools that need multiple options.

        Args:
            track_name (str): The track name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            order (str, optional): Sort order for results. Defaults to "RANKING" for best matches first.

        Returns:
            List[DeezerTrack]: List of matching tracks, empty list if none found
        """
        try:
            search_params = {
                "q": track_name,
                "limit": limit,
                "order": order
            }
            
            search_response = await self._get("search/track", params=search_params)
            
            if not search_response.get("data"):
                return []
                
            # Return list of tracks from search results (these already have most needed data)
            return [DeezerTrack(**item) for item in search_response["data"]]
            
        except Exception as e:
            print(f"Error searching for tracks '{track_name}': {e}")
            return []

    async def get_track_by_name_and_artist(
        self, 
        track_name: str, 
        artist_name: str,
        limit: int = 1,
        order: str = "RANKING"
    ) -> Optional[DeezerTrack]:
        """
        Retrieve a track by combining track name and artist name for more precise results.
        This is particularly useful for MCP tools when you have both pieces of information.

        Args:
            track_name (str): The track name to search for
            artist_name (str): The artist name to narrow the search
            limit (int, optional): Number of results to return. Defaults to 1.
            order (str, optional): Sort order for results. Defaults to "RANKING".

        Returns:
            Optional[DeezerTrack]: The best matching track or None if not found
        """
        try:
            # Build combined search query
            search_query = f'track:"{track_name}" artist:"{artist_name}"'
            
            search_params = {
                "q": search_query,
                "limit": limit,
                "order": order
            }
            
            search_response = await self._get("search/track", params=search_params)
            
            if not search_response.get("data"):
                return None
                
            # Get the best match (first result)
            best_match = search_response["data"][0]
            track_id = best_match["id"]
            
            # Fetch complete track details
            track_response = await self._get(f"track/{track_id}")
            return DeezerTrack(**track_response)
            
        except Exception as e:
            print(f"Error searching for track '{track_name}' by artist '{artist_name}': {e}")
            return None