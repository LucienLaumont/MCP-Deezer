#!/usr/bin/env python3
"""
MCP Server for Deezer API integration.
Provides tools to search and retrieve information about tracks, artists, albums, and playlists from Deezer.

Copyright (c) 2025 Lucien Laumont
Licensed under the MIT License - see LICENSE file for details.
"""

import asyncio
import logging
from typing import Any, Sequence

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.server.stdio

from .functions.deezer_client.track import TrackNameClient
from .functions.deezer_client.artist import ArtistNameClient
from .functions.deezer_client.album import AlbumNameClient
from .functions.deezer_client.playlist import PlaylistNameClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("deezer-mcp-server")

# Initialize the MCP server
server = Server("deezer-api-server")

# Initialize Deezer clients
track_client = TrackNameClient()
artist_client = ArtistNameClient()
album_client = AlbumNameClient()
playlist_client = PlaylistNameClient()


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_track",
            description="Search for tracks by name on Deezer with optional parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_name": {
                        "type": "string",
                        "description": "The name of the track to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 25
                    },
                    "strict": {
                        "type": "boolean",
                        "description": "If true, disable fuzzy mode for exact matches only (optional)"
                    },
                    "order": {
                        "type": "string",
                        "description": "Sort order: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, DURATION_ASC, DURATION_DESC (optional)",
                        "enum": ["RANKING", "TRACK_ASC", "TRACK_DESC", "ARTIST_ASC", "ARTIST_DESC", "ALBUM_ASC", "ALBUM_DESC", "RATING_ASC", "RATING_DESC", "DURATION_ASC", "DURATION_DESC"]
                    }
                },
                "required": ["track_name"]
            }
        ),
        Tool(
            name="get_track",
            description="Get a track by its Deezer ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_id": {
                        "type": "integer",
                        "description": "The Deezer track ID"
                    }
                },
                "required": ["track_id"]
            }
        ),
        Tool(
            name="search_track_by_artist",
            description="Search for a track by name and artist on Deezer",
            inputSchema={
                "type": "object",
                "properties": {
                    "track_name": {
                        "type": "string",
                        "description": "The name of the track to search for"
                    },
                    "artist_name": {
                        "type": "string",
                        "description": "The name of the artist"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 1)",
                        "default": 1,
                        "minimum": 1,
                        "maximum": 25
                    },
                    "order": {
                        "type": "string",
                        "description": "Sort order (default: RANKING)",
                        "default": "RANKING",
                        "enum": ["RANKING", "TRACK_ASC", "TRACK_DESC", "ARTIST_ASC", "ARTIST_DESC", "ALBUM_ASC", "ALBUM_DESC", "RATING_ASC", "RATING_DESC", "DURATION_ASC", "DURATION_DESC"]
                    }
                },
                "required": ["track_name", "artist_name"]
            }
        ),
        Tool(
            name="search_artist",
            description="Search for artists by name on Deezer with optional parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "artist_name": {
                        "type": "string",
                        "description": "The name of the artist to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 25
                    },
                    "strict": {
                        "type": "boolean",
                        "description": "If true, disable fuzzy mode for exact matches only (optional)"
                    },
                    "order": {
                        "type": "string",
                        "description": "Sort order: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, DURATION_ASC, DURATION_DESC (optional)",
                        "enum": ["RANKING", "TRACK_ASC", "TRACK_DESC", "ARTIST_ASC", "ARTIST_DESC", "ALBUM_ASC", "ALBUM_DESC", "RATING_ASC", "RATING_DESC", "DURATION_ASC", "DURATION_DESC"]
                    }
                },
                "required": ["artist_name"]
            }
        ),
        Tool(
            name="get_artist",
            description="Get an artist by their Deezer ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "artist_id": {
                        "type": "integer",
                        "description": "The Deezer artist ID"
                    }
                },
                "required": ["artist_id"]
            }
        ),
        Tool(
            name="search_album",
            description="Search for albums by name on Deezer with optional parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "album_name": {
                        "type": "string",
                        "description": "The name of the album to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 25
                    },
                    "strict": {
                        "type": "boolean",
                        "description": "If true, disable fuzzy mode for exact matches only (optional)"
                    },
                    "order": {
                        "type": "string",
                        "description": "Sort order: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, DURATION_ASC, DURATION_DESC (optional)",
                        "enum": ["RANKING", "TRACK_ASC", "TRACK_DESC", "ARTIST_ASC", "ARTIST_DESC", "ALBUM_ASC", "ALBUM_DESC", "RATING_ASC", "RATING_DESC", "DURATION_ASC", "DURATION_DESC"]
                    }
                },
                "required": ["album_name"]
            }
        ),
        Tool(
            name="get_album",
            description="Get an album by its Deezer ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "album_id": {
                        "type": "integer",
                        "description": "The Deezer album ID"
                    }
                },
                "required": ["album_id"]
            }
        ),
        Tool(
            name="search_playlist",
            description="Search for playlists by name on Deezer with optional parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_name": {
                        "type": "string",
                        "description": "The name of the playlist to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 25
                    },
                    "strict": {
                        "type": "boolean",
                        "description": "If true, disable fuzzy mode for exact matches only (optional)"
                    },
                    "order": {
                        "type": "string",
                        "description": "Sort order: RANKING, TRACK_ASC, TRACK_DESC, ARTIST_ASC, ARTIST_DESC, ALBUM_ASC, ALBUM_DESC, RATING_ASC, RATING_DESC, DURATION_ASC, DURATION_DESC (optional)",
                        "enum": ["RANKING", "TRACK_ASC", "TRACK_DESC", "ARTIST_ASC", "ARTIST_DESC", "ALBUM_ASC", "ALBUM_DESC", "RATING_ASC", "RATING_DESC", "DURATION_ASC", "DURATION_DESC"]
                    },
                    "public_only": {
                        "type": "boolean",
                        "description": "Search only public playlists (default: false)",
                        "default": False
                    }
                },
                "required": ["playlist_name"]
            }
        ),
        Tool(
            name="get_playlist",
            description="Get a playlist by its Deezer ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_id": {
                        "type": "integer",
                        "description": "The Deezer playlist ID"
                    }
                },
                "required": ["playlist_id"]
            }
        ),
        Tool(
            name="search_playlist_by_creator",
            description="Search for a playlist by name and creator for more precise results",
            inputSchema={
                "type": "object",
                "properties": {
                    "playlist_name": {
                        "type": "string",
                        "description": "The name of the playlist to search for"
                    },
                    "creator_name": {
                        "type": "string",
                        "description": "The creator/user name to narrow the search"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default: 1)",
                        "default": 1,
                        "minimum": 1,
                        "maximum": 25
                    },
                    "order": {
                        "type": "string",
                        "description": "Sort order (default: RANKING)",
                        "default": "RANKING",
                        "enum": ["RANKING", "TRACK_ASC", "TRACK_DESC", "ARTIST_ASC", "ARTIST_DESC", "ALBUM_ASC", "ALBUM_DESC", "RATING_ASC", "RATING_DESC", "DURATION_ASC", "DURATION_DESC"]
                    }
                },
                "required": ["playlist_name", "creator_name"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    try:
        if name == "search_track":
            track_name = arguments.get("track_name")
            limit = arguments.get("limit", 10)
            strict = arguments.get("strict")
            order = arguments.get("order")
            
            results = await track_client.search_tracks_by_name(track_name, limit=limit, strict=strict, order=order)
            if results:
                tracks_text = f"🎵 **{len(results)} Tracks Found for '{track_name}'**\n\n"
                for i, track in enumerate(results, 1):
                    tracks_text += f"**{i}.** {track.title} by {track.artist.name}\n"
                    tracks_text += f"   ID: {track.id}\n"
                    tracks_text += f"   Album: {track.album.title}\n"
                    tracks_text += f"   Duration: {track.duration}s\n"
                    tracks_text += f"   Link: {track.link}\n\n"
                return [TextContent(type="text", text=tracks_text)]
            else:
                return [TextContent(type="text", text=f"❌ No tracks found for '{track_name}'")]
        
        elif name == "get_track":
            track_id = arguments.get("track_id")
            result = await track_client.get_track(track_id)
            if result:
                return [TextContent(
                    type="text",
                    text=f"🎵 **Track Found**\n\n"
                         f"**ID:** {result.id}\n"
                         f"**Title:** {result.title}\n"
                         f"**Artist:** {result.artist.name}\n"
                         f"**Album:** {result.album.title}\n"
                         f"**Duration:** {result.duration}s\n"
                         f"**Release Date:** {result.release_date}\n"
                         f"**Link:** {result.link}\n"
                         f"**Preview:** {result.preview or 'N/A'}"
                )]
            else:
                return [TextContent(type="text", text=f"❌ No track found with ID {track_id}")]

        elif name == "search_track_by_artist":
            track_name = arguments.get("track_name")
            artist_name = arguments.get("artist_name")
            limit = arguments.get("limit", 1)
            order = arguments.get("order", "RANKING")
            
            result = await track_client.get_track_by_name_and_artist(track_name, artist_name, limit=limit, order=order)
            if result:
                return [TextContent(
                    type="text",
                    text=f"🎵 **Track Found**\n\n"
                         f"**ID:** {result.id}\n"
                         f"**Title:** {result.title}\n"
                         f"**Artist:** {result.artist.name}\n"
                         f"**Album:** {result.album.title}\n"
                         f"**Duration:** {result.duration}s\n"
                         f"**Release Date:** {result.release_date}\n"
                         f"**Link:** {result.link}\n"
                         f"**Preview:** {result.preview or 'N/A'}"
                )]
            else:
                return [TextContent(type="text", text=f"❌ No track found for '{track_name}' by '{artist_name}'")]

        elif name == "search_artist":
            artist_name = arguments.get("artist_name")
            limit = arguments.get("limit", 10)
            strict = arguments.get("strict")
            order = arguments.get("order")
            
            results = await artist_client.search_artists_by_name(artist_name, limit=limit, strict=strict, order=order)
            if results:
                artists_text = f"🎤 **{len(results)} Artists Found for '{artist_name}'**\n\n"
                for i, artist in enumerate(results, 1):
                    artists_text += f"**{i}.** {artist.name}\n"
                    artists_text += f"   ID: {artist.id}\n"
                    artists_text += f"   Fans: {artist.nb_fan:,}\n"
                    artists_text += f"   Albums: {artist.nb_album}\n"
                    artists_text += f"   Link: {artist.link}\n\n"
                return [TextContent(type="text", text=artists_text)]
            else:
                return [TextContent(type="text", text=f"❌ No artists found for '{artist_name}'")]
        
        elif name == "get_artist":
            artist_id = arguments.get("artist_id")
            result = await artist_client.get_artist(artist_id)
            if result:
                return [TextContent(
                    type="text",
                    text=f"🎤 **Artist Found**\n\n"
                         f"**ID:** {result.id}\n"
                         f"**Name:** {result.name}\n"
                         f"**Fans:** {result.nb_fan:,}\n"
                         f"**Albums:** {result.nb_album}\n"
                         f"**Link:** {result.link}\n"
                         f"**Picture:** {result.picture_medium or 'N/A'}"
                )]
            else:
                return [TextContent(type="text", text=f"❌ No artist found with ID {artist_id}")]

        elif name == "search_album":
            album_name = arguments.get("album_name")
            limit = arguments.get("limit", 10)
            strict = arguments.get("strict")
            order = arguments.get("order")
            
            results = await album_client.search_albums_by_name(album_name, limit=limit, strict=strict, order=order)
            if results:
                albums_text = f"💿 **{len(results)} Albums Found for '{album_name}'**\n\n"
                for i, album in enumerate(results, 1):
                    albums_text += f"**{i}.** {album.title} by {album.artist.name}\n"
                    albums_text += f"   ID: {album.id}\n"
                    albums_text += f"   Tracks: {album.nb_tracks}\n"
                    albums_text += f"   Release Date: {album.release_date}\n"
                    albums_text += f"   Link: {album.link}\n\n"
                return [TextContent(type="text", text=albums_text)]
            else:
                return [TextContent(type="text", text=f"❌ No albums found for '{album_name}'")]
        
        elif name == "get_album":
            album_id = arguments.get("album_id")
            result = await album_client.get_album(album_id)
            if result:
                return [TextContent(
                    type="text",
                    text=f"💿 **Album Found**\n\n"
                         f"**ID:** {result.id}\n"
                         f"**Title:** {result.title}\n"
                         f"**Artist:** {result.artist.name}\n"
                         f"**Tracks:** {result.nb_tracks}\n"
                         f"**Duration:** {result.duration}s\n"
                         f"**Release Date:** {result.release_date}\n"
                         f"**Link:** {result.link}\n"
                         f"**Cover:** {result.cover_medium or 'N/A'}"
                )]
            else:
                return [TextContent(type="text", text=f"❌ No album found with ID {album_id}")]

        elif name == "search_playlist":
            playlist_name = arguments.get("playlist_name")
            limit = arguments.get("limit", 10)
            strict = arguments.get("strict")
            order = arguments.get("order")
            public_only = arguments.get("public_only", False)
            
            if public_only:
                results = await playlist_client.search_public_playlists_by_name(playlist_name, limit=limit, strict=strict, order=order)
            else:
                results = await playlist_client.search_playlists_by_name(playlist_name, limit=limit, strict=strict, order=order)
            
            if results:
                playlist_type = "Public Playlists" if public_only else "Playlists"
                playlists_text = f"🎼 **{len(results)} {playlist_type} Found for '{playlist_name}'**\n\n"
                for i, playlist in enumerate(results, 1):
                    creator_name = playlist.creator.name if playlist.creator else "Unknown"
                    playlists_text += f"**{i}.** {playlist.title} by {creator_name}\n"
                    playlists_text += f"   ID: {playlist.id}\n"
                    playlists_text += f"   Tracks: {playlist.nb_tracks}\n"
                    playlists_text += f"   Fans: {playlist.fans:,}\n" if playlist.fans is not None else "   Fans: N/A\n"
                    playlists_text += f"   Public: {'Yes' if playlist.public else 'No'}\n"
                    playlists_text += f"   Link: {playlist.link}\n\n"
                return [TextContent(type="text", text=playlists_text)]
            else:
                playlist_type = "public playlists" if public_only else "playlists"
                return [TextContent(type="text", text=f"❌ No {playlist_type} found for '{playlist_name}'")]
        
        elif name == "get_playlist":
            playlist_id = arguments.get("playlist_id")
            result = await playlist_client.get_playlist(playlist_id)
            if result:
                creator_name = result.creator.name if result.creator else "Unknown"
                return [TextContent(
                    type="text",
                    text=f"🎼 **Playlist Found**\n\n"
                         f"**ID:** {result.id}\n"
                         f"**Title:** {result.title}\n"
                         f"**Creator:** {creator_name}\n"
                         f"**Tracks:** {result.nb_tracks}\n"
                         f"**Duration:** {result.duration}s\n"
                         f"**Fans:** {result.fans:,}\n" if result.fans is not None else "**Fans:** N/A\n"
                         f"**Public:** {'Yes' if result.public else 'No'}\n"
                         f"**Link:** {result.link}\n"
                         f"**Picture:** {result.picture_medium or 'N/A'}"
                )]
            else:
                return [TextContent(type="text", text=f"❌ No playlist found with ID {playlist_id}")]
        
        elif name == "search_playlist_by_creator":
            playlist_name = arguments.get("playlist_name")
            creator_name = arguments.get("creator_name")
            limit = arguments.get("limit", 1)
            order = arguments.get("order", "RANKING")
            
            result = await playlist_client.get_playlist_by_name_and_creator(playlist_name, creator_name, limit=limit, order=order)
            if result:
                return [TextContent(
                    type="text",
                    text=f"🎼 **Playlist Found**\n\n"
                         f"**ID:** {result.id}\n"
                         f"**Title:** {result.title}\n"
                         f"**Creator:** {result.creator.name if result.creator else 'Unknown'}\n"
                         f"**Tracks:** {result.nb_tracks}\n"
                         f"**Duration:** {result.duration}s\n"
                         f"**Fans:** {result.fans:,}\n" if result.fans is not None else "**Fans:** N/A\n"
                         f"**Public:** {'Yes' if result.public else 'No'}\n"
                         f"**Link:** {result.link}\n"
                         f"**Picture:** {result.picture_medium or 'N/A'}"
                )]
            else:
                return [TextContent(type="text", text=f"❌ No playlist found for '{playlist_name}' by '{creator_name}'")]

        else:
            return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error in tool '{name}': {e}")
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def main():
    """Main entry point for the server."""
    try:
        # Run the server using stdin/stdout streams
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="deezer-api-server",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())