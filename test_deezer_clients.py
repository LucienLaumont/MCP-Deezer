#!/usr/bin/env python3
"""
Test script for all Deezer API clients with popular content examples.
This script tests the TrackNameClient, ArtistNameClient, AlbumNameClient, and PlaylistNameClient
with well-known artists, tracks, albums, and playlists on Deezer.

Copyright (c) 2025 Lucien Laumont
Licensed under the MIT License - see LICENSE file for details.
"""

import asyncio
import sys
from typing import Dict, Any

# Import all Deezer clients
from mcp_deezer.functions.deezer_client.track import TrackNameClient
from mcp_deezer.functions.deezer_client.artist import ArtistNameClient
from mcp_deezer.functions.deezer_client.album import AlbumNameClient
from mcp_deezer.functions.deezer_client.playlist import PlaylistNameClient


# Test data with popular content on Deezer
TEST_DATA = {
    "artists": [
        "Daft Punk",
        "The Weeknd", 
        "Ed Sheeran",
        "Taylor Swift",
        "Drake"
    ],
    "tracks": [
        "Blinding Lights",
        "Shape of You", 
        "One More Time",
        "Starboy",
        "Anti-Hero"
    ],
    "albums": [
        "Random Access Memories",
        "After Hours",
        "Divide",
        "Midnights",
        "Views"
    ],
    "playlists": [
        "Today's Hits",
        "Pop Hits",
        "Chill Hits",
        "Rap",
        "Electronic"
    ],
    "track_artist_combinations": [
        ("Blinding Lights", "The Weeknd"),
        ("One More Time", "Daft Punk"),
        ("Shape of You", "Ed Sheeran"),
        ("Starboy", "The Weeknd"),
        ("Anti-Hero", "Taylor Swift")
    ]
}


def print_separator(title: str):
    """Print a formatted separator for test sections."""
    print("\n" + "="*60)
    print(f" {title} ")
    print("="*60)


def print_result(name: str, result: Any, success: bool = True):
    """Print test result in a formatted way."""
    status = "✓" if success else "✗"
    print(f"\n{status} {name}:")
    if result:
        if hasattr(result, 'title'):
            print(f"   Title: {result.title}")
        if hasattr(result, 'name'):
            print(f"   Name: {result.name}")
        if hasattr(result, 'id'):
            print(f"   ID: {result.id}")
        if hasattr(result, 'link'):
            print(f"   Link: {result.link}")
        if hasattr(result, 'artist') and result.artist:
            print(f"   Artist: {result.artist.name}")
        if hasattr(result, 'album') and result.album:
            print(f"   Album: {result.album.title}")
    else:
        print(f"   Result: None (not found)")


async def test_track_client():
    """Test the TrackNameClient with popular tracks."""
    print_separator("TESTING TRACK CLIENT")
    
    client = TrackNameClient()
    
    # Test track search by name (returns DeezerTrackSearch)
    print("\n--- Track Search by Name (DeezerTrackSearch) ---")
    for track_name in TEST_DATA["tracks"]:
        try:
            results = await client.search_tracks_by_name(track_name, limit=1)
            if results:
                result = results[0]
                print_result(f"Track Search: '{track_name}'", result, True)
                print(f"   Type: DeezerTrackSearch")
            else:
                print_result(f"Track Search: '{track_name}'", None, False)
        except Exception as e:
            print_result(f"Track Search: '{track_name}'", None, False)
            print(f"   Error: {e}")
    
    # Test track by ID (returns DeezerTrack)
    print("\n--- Track by ID (DeezerTrack) ---")
    test_track_ids = [3135556, 1109731, 916424]  # Known track IDs
    for track_id in test_track_ids:
        try:
            result = await client.get_track(track_id)
            print_result(f"Track ID: {track_id}", result, result is not None)
            if result:
                print(f"   Type: DeezerTrack")
                if hasattr(result, 'duration'):
                    print(f"   Duration: {result.duration}")
        except Exception as e:
            print_result(f"Track ID: {track_id}", None, False)
            print(f"   Error: {e}")
    
    # Test track with artist combinations
    print("\n--- Track + Artist Searches ---")
    for track_name, artist_name in TEST_DATA["track_artist_combinations"]:
        try:
            result = await client.get_track_by_name_and_artist(track_name, artist_name)
            print_result(f"'{track_name}' by '{artist_name}'", result, result is not None)
        except Exception as e:
            print_result(f"'{track_name}' by '{artist_name}'", None, False)
            print(f"   Error: {e}")
    
    # Test multiple results search
    print("\n--- Multiple Track Results ---")
    try:
        results = await client.search_tracks_by_name("Love", limit=3)
        print(f"\n✓ Search 'Love' (multiple results): Found {len(results)} tracks")
        for i, track in enumerate(results[:3], 1):
            print(f"   {i}. {track.title} by {track.artist.name} (DeezerTrackSearch)")
    except Exception as e:
        print(f"✗ Search 'Love' (multiple results): Error - {e}")
    
    # Test optional parameters
    print("\n--- Track Search with Optional Parameters ---")
    try:
        # Test strict mode
        strict_results = await client.search_tracks_by_name("Blinding Lights", limit=2, strict=True, order="RANKING")
        print(f"✓ Strict search 'Blinding Lights': Found {len(strict_results)} tracks")
        
        # Test different order
        ordered_results = await client.search_tracks_by_name("Love", limit=2, order="TRACK_ASC")
        print(f"✓ Ordered search 'Love' (TRACK_ASC): Found {len(ordered_results)} tracks")
    except Exception as e:
        print(f"✗ Optional parameters test: Error - {e}")


async def test_artist_client():
    """Test the ArtistNameClient with popular artists."""
    print_separator("TESTING ARTIST CLIENT")
    
    client = ArtistNameClient()
    
    # Test artist search by name (returns DeezerArtistSearch)
    print("\n--- Artist Search by Name (DeezerArtistSearch) ---")
    for artist_name in TEST_DATA["artists"]:
        try:
            results = await client.search_artists_by_name(artist_name, limit=1)
            if results:
                result = results[0]
                print_result(f"Artist Search: '{artist_name}'", result, True)
                print(f"   Type: DeezerArtistSearch")
                if hasattr(result, 'nb_fan'):
                    print(f"   Fans: {result.nb_fan:,}")
            else:
                print_result(f"Artist Search: '{artist_name}'", None, False)
        except Exception as e:
            print_result(f"Artist Search: '{artist_name}'", None, False)
            print(f"   Error: {e}")
    
    # Test artist by ID (returns DeezerArtist)
    print("\n--- Artist by ID (DeezerArtist) ---")
    test_artist_ids = [27, 13, 75798]  # Known artist IDs
    for artist_id in test_artist_ids:
        try:
            result = await client.get_artist(artist_id)
            print_result(f"Artist ID: {artist_id}", result, result is not None)
            if result:
                print(f"   Type: DeezerArtist")
                if hasattr(result, 'nb_fan'):
                    print(f"   Fans: {result.nb_fan:,}")
        except Exception as e:
            print_result(f"Artist ID: {artist_id}", None, False)
            print(f"   Error: {e}")
    
    # Test multiple results search
    print("\n--- Multiple Artist Results ---")
    try:
        results = await client.search_artists_by_name("Michael", limit=3)
        print(f"\n✓ Search 'Michael' (multiple results): Found {len(results)} artists")
        for i, artist in enumerate(results[:3], 1):
            print(f"   {i}. {artist.name} ({artist.nb_fan:,} fans) (DeezerArtistSearch)")
    except Exception as e:
        print(f"✗ Search 'Michael' (multiple results): Error - {e}")
    
    # Test optional parameters
    print("\n--- Artist Search with Optional Parameters ---")
    try:
        # Test strict mode
        strict_results = await client.search_artists_by_name("Daft Punk", limit=2, strict=True, order="RANKING")
        print(f"✓ Strict search 'Daft Punk': Found {len(strict_results)} artists")
        
        # Test different order
        ordered_results = await client.search_artists_by_name("Taylor", limit=2, order="ARTIST_ASC")
        print(f"✓ Ordered search 'Taylor' (ARTIST_ASC): Found {len(ordered_results)} artists")
    except Exception as e:
        print(f"✗ Optional parameters test: Error - {e}")


async def test_album_client():
    """Test the AlbumNameClient with popular albums."""
    print_separator("TESTING ALBUM CLIENT")
    
    client = AlbumNameClient()
    
    # Test album search by name (returns DeezerAlbumSearch)
    print("\n--- Album Search by Name (DeezerAlbumSearch) ---")
    for album_name in TEST_DATA["albums"]:
        try:
            results = await client.search_albums_by_name(album_name, limit=1)
            if results:
                result = results[0]
                print_result(f"Album Search: '{album_name}'", result, True)
                print(f"   Type: DeezerAlbumSearch")
                if hasattr(result, 'nb_tracks'):
                    print(f"   Tracks: {result.nb_tracks}")
            else:
                print_result(f"Album Search: '{album_name}'", None, False)
        except Exception as e:
            print_result(f"Album Search: '{album_name}'", None, False)
            print(f"   Error: {e}")
    
    # Test album by ID (returns DeezerAlbum)
    print("\n--- Album by ID (DeezerAlbum) ---")
    test_album_ids = [302127, 103248, 75621]  # Known album IDs
    for album_id in test_album_ids:
        try:
            result = await client.get_album(album_id)
            print_result(f"Album ID: {album_id}", result, result is not None)
            if result:
                print(f"   Type: DeezerAlbum")
                if hasattr(result, 'genres') and result.genres:
                    print(f"   Genres: {[g.name for g in result.genres]}")
        except Exception as e:
            print_result(f"Album ID: {album_id}", None, False)
            print(f"   Error: {e}")
    
    # Test multiple results search
    print("\n--- Multiple Album Results ---")
    try:
        results = await client.search_albums_by_name("Greatest Hits", limit=3)
        print(f"\n✓ Search 'Greatest Hits' (multiple results): Found {len(results)} albums")
        for i, album in enumerate(results[:3], 1):
            print(f"   {i}. {album.title} by {album.artist.name} (DeezerAlbumSearch)")
    except Exception as e:
        print(f"✗ Search 'Greatest Hits' (multiple results): Error - {e}")
    
    # Test optional parameters
    print("\n--- Album Search with Optional Parameters ---")
    try:
        # Test strict mode
        strict_results = await client.search_albums_by_name("Random Access Memories", limit=2, strict=True, order="RANKING")
        print(f"✓ Strict search 'Random Access Memories': Found {len(strict_results)} albums")
        
        # Test different order
        ordered_results = await client.search_albums_by_name("Love", limit=2, order="ALBUM_ASC")
        print(f"✓ Ordered search 'Love' (ALBUM_ASC): Found {len(ordered_results)} albums")
    except Exception as e:
        print(f"✗ Optional parameters test: Error - {e}")


async def test_playlist_client():
    """Test the PlaylistNameClient with popular playlists."""
    print_separator("TESTING PLAYLIST CLIENT")
    
    client = PlaylistNameClient()
    
    # Test playlist search by name (returns DeezerPlaylistBase)
    print("\n--- Playlist Search by Name (DeezerPlaylistBase) ---")
    for playlist_name in TEST_DATA["playlists"]:
        try:
            results = await client.search_playlists_by_name(playlist_name, limit=1)
            if results:
                result = results[0]
                print_result(f"Playlist Search: '{playlist_name}'", result, True)
                print(f"   Type: DeezerPlaylistBase")
                if hasattr(result, 'nb_tracks'):
                    print(f"   Tracks: {result.nb_tracks}")
                if hasattr(result, 'user') and result.user:
                    print(f"   Creator: {result.user.name}")
            else:
                print_result(f"Playlist Search: '{playlist_name}'", None, False)
        except Exception as e:
            print_result(f"Playlist Search: '{playlist_name}'", None, False)
            print(f"   Error: {e}")
    
    # Test playlist by ID (returns DeezerPlaylist)
    print("\n--- Playlist by ID (DeezerPlaylist) ---")
    test_playlist_ids = [1313621735, 2274923946, 908622995]  # Known playlist IDs
    for playlist_id in test_playlist_ids:
        try:
            result = await client.get_playlist(playlist_id)
            print_result(f"Playlist ID: {playlist_id}", result, result is not None)
            if result:
                print(f"   Type: DeezerPlaylist")
                if hasattr(result, 'tracks') and result.tracks:
                    print(f"   Tracks loaded: {len(result.tracks)}")
        except Exception as e:
            print_result(f"Playlist ID: {playlist_id}", None, False)
            print(f"   Error: {e}")
    
    # Test multiple results search
    print("\n--- Multiple Playlist Results ---")
    try:
        results = await client.search_playlists_by_name("Rock", limit=3)
        print(f"\n✓ Search 'Rock' (multiple results): Found {len(results)} playlists")
        for i, playlist in enumerate(results[:3], 1):
            creator_name = playlist.user.name if playlist.user else "Unknown"
            print(f"   {i}. {playlist.title} by {creator_name} (DeezerPlaylistBase)")
    except Exception as e:
        print(f"✗ Search 'Rock' (multiple results): Error - {e}")
    
    # Test public playlists search
    print("\n--- Public Playlist Search ---")
    try:
        results = await client.search_public_playlists_by_name("Pop", limit=3)
        print(f"\n✓ Search public 'Pop' playlists: Found {len(results)} public playlists")
        for i, playlist in enumerate(results[:3], 1):
            creator_name = playlist.user.name if playlist.user else "Unknown"
            print(f"   {i}. {playlist.title} by {creator_name} (Public, DeezerPlaylistBase)")
    except Exception as e:
        print(f"✗ Search public 'Pop' playlists: Error - {e}")
    
    # Test optional parameters
    print("\n--- Playlist Search with Optional Parameters ---")
    try:
        # Test strict mode
        strict_results = await client.search_playlists_by_name("Today's Hits", limit=2, strict=True, order="RANKING")
        print(f"✓ Strict search 'Today's Hits': Found {len(strict_results)} playlists")
        
        # Test different order
        ordered_results = await client.search_playlists_by_name("Pop", limit=2, order="DURATION_ASC")
        print(f"✓ Ordered search 'Pop' (DURATION_ASC): Found {len(ordered_results)} playlists")
    except Exception as e:
        print(f"✗ Optional parameters test: Error - {e}")


async def run_all_tests():
    """Run all client tests."""
    print("🎵 DEEZER API CLIENTS TEST SUITE 🎵")
    print("Testing all clients with popular content...")
    
    try:
        await test_track_client()
        await test_artist_client() 
        await test_album_client()
        await test_playlist_client()
        
        print_separator("TEST SUITE COMPLETED")
        print("✓ All tests completed successfully!")
        print("\nNote: Some searches may return None if the content is not available")
        print("in your region or if the search terms don't match exactly.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the test suite
    asyncio.run(run_all_tests())