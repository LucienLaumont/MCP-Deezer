# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides access to the Deezer API. The project implements a Python-based wrapper around Deezer's REST API with proper type definitions using Pydantic models.

## Architecture

The codebase follows a modular structure:

- **`mcp_deezer/`**: Main package directory
  - **`functions/deezer_client/`**: API client implementations
    - `base.py`: Base HTTP client with shared functionality
    - Individual resource clients (`track.py`, `artist.py`, `album.py`, `playlist.py`)
  - **`types/`**: Pydantic models for API responses
    - Type definitions for each Deezer resource (track, artist, album, etc.)
- **`config.py`**: Configuration management using pydantic-settings
- **`requirements.txt`**: Python dependencies

## Development Commands

### Running the Application
```bash
python mcp_deezer/main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

The application requires environment variables set in a `.env` file:
- `MISTRAL_API_KEY`: API key for Mistral AI integration
- `MISTRAL_MODEL`: Mistral model to use
- `DEEZER_BASE_URL`: Defaults to "https://api.deezer.com"

Configuration is managed through the `Settings` class in `config.py` using pydantic-settings.

## Key Components

### BaseDeezerClient
Located in `mcp_deezer/functions/deezer_client/base.py:6`, this is the foundation class that all resource clients inherit from. It handles HTTP requests to the Deezer API using httpx.

### Type System
The project uses comprehensive Pydantic models for type safety. Each Deezer resource has corresponding types in the `types/` directory following the official Deezer API documentation.

### Resource Clients
Each Deezer resource (tracks, artists, albums, playlists) has its own client class that extends `BaseDeezerClient` and provides specific methods for that resource type.