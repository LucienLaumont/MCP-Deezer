#!/usr/bin/env python3
"""
Test script for all Deezer API clients with popular content examples.
This script tests the TrackNameClient, ArtistNameClient, AlbumNameClient, and PlaylistNameClient
with well-known artists, tracks, albums, and playlists on Deezer.
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
    
    # Test individual track searches
    print("\n--- Individual Track Searches ---")
    for track_name in TEST_DATA["tracks"]:
        try:
            result = await client.get_track_by_name(track_name)
            print_result(f"Track: '{track_name}'", result, result is not None)
        except Exception as e:
            print_result(f"Track: '{track_name}'", None, False)
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
            print(f"   {i}. {track.title} by {track.artist.name}")
    except Exception as e:
        print(f"✗ Search 'Love' (multiple results): Error - {e}")


async def test_artist_client():
    """Test the ArtistNameClient with popular artists."""
    print_separator("TESTING ARTIST CLIENT")
    
    client = ArtistNameClient()
    
    # Test individual artist searches
    print("\n--- Individual Artist Searches ---")
    for artist_name in TEST_DATA["artists"]:
        try:
            result = await client.get_artist_by_name(artist_name)
            print_result(f"Artist: '{artist_name}'", result, result is not None)
            if result and hasattr(result, 'nb_fan'):
                print(f"   Fans: {result.nb_fan:,}")
        except Exception as e:
            print_result(f"Artist: '{artist_name}'", None, False)
            print(f"   Error: {e}")
    
    # Test multiple results search
    print("\n--- Multiple Artist Results ---")
    try:
        results = await client.search_artists_by_name("Michael", limit=3)
        print(f"\n✓ Search 'Michael' (multiple results): Found {len(results)} artists")
        for i, artist in enumerate(results[:3], 1):
            print(f"   {i}. {artist.name} ({artist.nb_fan:,} fans)")
    except Exception as e:
        print(f"✗ Search 'Michael' (multiple results): Error - {e}")


async def test_album_client():
    """Test the AlbumNameClient with popular albums."""
    print_separator("TESTING ALBUM CLIENT")
    
    client = AlbumNameClient()
    
    # Test individual album searches
    print("\n--- Individual Album Searches ---")
    for album_name in TEST_DATA["albums"]:
        try:
            result = await client.get_album_by_name(album_name)
            print_result(f"Album: '{album_name}'", result, result is not None)
            if result:
                if hasattr(result, 'nb_tracks'):
                    print(f"   Tracks: {result.nb_tracks}")
                if hasattr(result, 'release_date'):
                    print(f"   Release Date: {result.release_date}")
        except Exception as e:
            print_result(f"Album: '{album_name}'", None, False)
            print(f"   Error: {e}")
    
    # Test multiple results search
    print("\n--- Multiple Album Results ---")
    try:
        results = await client.search_albums_by_name("Greatest Hits", limit=3)
        print(f"\n✓ Search 'Greatest Hits' (multiple results): Found {len(results)} albums")
        for i, album in enumerate(results[:3], 1):
            print(f"   {i}. {album.title} by {album.artist.name}")
    except Exception as e:
        print(f"✗ Search 'Greatest Hits' (multiple results): Error - {e}")


async def test_playlist_client():
    """Test the PlaylistNameClient with popular playlists."""
    print_separator("TESTING PLAYLIST CLIENT")
    
    client = PlaylistNameClient()
    
    # Test individual playlist searches
    print("\n--- Individual Playlist Searches ---")
    for playlist_name in TEST_DATA["playlists"]:
        try:
            result = await client.get_playlist_by_name(playlist_name)
            print_result(f"Playlist: '{playlist_name}'", result, result is not None)
            if result:
                if hasattr(result, 'nb_tracks'):
                    print(f"   Tracks: {result.nb_tracks}")
                if hasattr(result, 'creation_date'):
                    print(f"   Created: {result.creation_date}")
                if hasattr(result, 'creator') and result.creator:
                    print(f"   Creator: {result.creator.name}")
        except Exception as e:
            print_result(f"Playlist: '{playlist_name}'", None, False)
            print(f"   Error: {e}")
    
    # Test multiple results search
    print("\n--- Multiple Playlist Results ---")
    try:
        results = await client.search_playlists_by_name("Rock", limit=3)
        print(f"\n✓ Search 'Rock' (multiple results): Found {len(results)} playlists")
        for i, playlist in enumerate(results[:3], 1):
            creator_name = playlist.creator.name if playlist.creator else "Unknown"
            print(f"   {i}. {playlist.title} by {creator_name}")
    except Exception as e:
        print(f"✗ Search 'Rock' (multiple results): Error - {e}")
    
    # Test public playlists search
    print("\n--- Public Playlist Search ---")
    try:
        results = await client.search_public_playlists_by_name("Pop", limit=3)
        print(f"\n✓ Search public 'Pop' playlists: Found {len(results)} public playlists")
        for i, playlist in enumerate(results[:3], 1):
            creator_name = playlist.creator.name if playlist.creator else "Unknown"
            print(f"   {i}. {playlist.title} by {creator_name} (Public)")
    except Exception as e:
        print(f"✗ Search public 'Pop' playlists: Error - {e}")


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