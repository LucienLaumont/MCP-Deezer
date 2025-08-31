from mcp_deezer.functions.deezer_client.base import BaseDeezerClient
from mcp_deezer.types import DeezerTrack, DeezerTrackSearch
from typing import Optional, List


class TrackNameClient(BaseDeezerClient):
    """Client to retrieve tracks by their name and ID."""


    async def get_track(self, track_id: int) -> Optional[DeezerTrack]:
        """
        Retrieve a complete track by its ID.

        Args:
            track_id (int): The Deezer track ID

        Returns:
            Optional[DeezerTrack]: The complete track data or None if not found
        """
        try:
            track_response = await self._get(f"track/{track_id}")
            return DeezerTrack(**track_response)
            
        except Exception as e:
            print(f"Error retrieving track with ID {track_id}: {e}")
            return None

    async def search_tracks_by_name(
        self, 
        track_name: str, 
        limit: int = 10,
        strict: Optional[bool] = None,
        order: Optional[str] = None
    ) -> List[DeezerTrackSearch]:
        """
        Search for multiple tracks by name - useful for MCP tools that need multiple options.

        Args:
            track_name (str): The track name to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            strict (bool, optional): If True, disable fuzzy mode. If None, uses default API behavior.
            order (str, optional): Sort order. Options: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, 
                                 ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, 
                                 DURATION_ASC, DURATION_DESC. If None, uses default API behavior.

        Returns:
            List[DeezerTrackSearch]: List of matching tracks, empty list if none found
        """
        try:
            search_params = {
                "q": track_name,
                "limit": limit
            }
            
            # Add optional parameters if provided
            if strict is not None:
                search_params["strict"] = "on" if strict else "off"
            if order is not None:
                search_params["order"] = order
            
            search_response = await self._get("search/track", params=search_params)
            
            if not search_response.get("data"):
                return []
                
            # Return list of tracks from search results using DeezerTrackSearch type
            return [DeezerTrackSearch(**item) for item in search_response["data"]]
            
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